"""Replicate the three charts in the 17 Nov 2026 thread on US trade with ASEAN:
the monthly US goods trade deficit with ASEAN and with China, the effective
tariff rate on imports from each, and the deficit with ASEAN next to the part
of it that is AI-related products.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes three PNGs (chart_1_deficit_asean_vs_china.png,
chart_2_tariff_asean_vs_china.png, chart_3_asean_deficit_total_vs_ai.png) into
the current folder, overwriting the shipped copies. They should come out
identical.

Data: US Census Bureau monthly imports and exports (FT900 / USA Trade Online)
at the 10-digit level, summed over the seven ASEAN members described in
README.md and for China (imports = customs value, duties = calculated duties,
exports = FAS value).
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

X_START = pd.Timestamp("2024-01-01")        # the charts start here; data.csv starts in 2023
X_PAD_MONTHS = 6                            # runway after the last month so the end labels fit
TARIFF_ERA = (pd.Timestamp("2025-01-01"), "2025 tariff era")
LW, ALPHA = 3.5, 0.9

ASEAN, CHINA = "ASEAN", "China"
# ASEAN dark blue against China's flag red; black for a total, dark blue for the part
COLOR = {ASEAN: "darkblue", CHINA: "#DE2910"}
TOTAL_COLOR, AI_COLOR = "black", "darkblue"


# ----------------------------------------------------------------------------- #
# number helpers
# ----------------------------------------------------------------------------- #
def dollars(x):
    """$47.2B, $759.3M, ..."""
    sign = "-" if x < 0 else ""
    x = abs(x)
    for div, suf in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if x >= div:
            return f"{sign}${x / div:.1f}{suf}"
    return f"{sign}${x:,.0f}"


def yoy(s, latest):
    """Latest value vs the same month a year earlier, in percent."""
    prior = s.get(latest - pd.DateOffset(months=12))
    return (float(s.loc[latest]) / prior - 1) * 100


# ----------------------------------------------------------------------------- #
# the house style (tradewartracker.com charts)
# ----------------------------------------------------------------------------- #
def style(ax, latest, percent=False):
    ax.set_facecolor("#ffffff")
    ax.figure.set_facecolor("#ffffff")
    ax.grid(True, alpha=0.3, linewidth=0.6)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    x_end = latest + pd.DateOffset(months=X_PAD_MONTHS)
    # dashed vertical rule at the start of the 2025 tariff era
    t, label = TARIFF_ERA
    ax.axvline(t, color="red", alpha=0.55, lw=1.8, ls=(0, (6, 4)), zorder=0)
    ax.annotate(label, xy=(t, 1), xycoords=("data", "axes fraction"),
                xytext=(4, -4), textcoords="offset points",
                fontsize=7.5, color="red", alpha=0.75, ha="left", va="top", zorder=0)
    ax.set_xlim(X_START, x_end)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    if percent:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:.0f}%"))
    else:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: dollars(x)))


def end_label(ax, x, y, color, text, fontsize=11, dy=0.0):
    """Bold, colour-matched label at the end of a line; dy nudges it (points)."""
    ax.annotate(text, xy=(x, y), xytext=(8, dy), textcoords="offset points",
                fontsize=fontsize, fontweight="bold", color=color, alpha=1.0,
                va="center", zorder=5)


def end_labels(ax, latest, items, fontsize=9):
    """End-of-line labels for several lines, nudged apart where they would
    overprint. items = [(y, color, text)]; call once the axis limits are final."""
    x = mdates.date2num(latest)
    to_pt = 72.0 / ax.figure.dpi
    rows = sorted(([ax.transData.transform((x, y))[1] * to_pt, y, c, t] for y, c, t in items),
                  key=lambda r: r[0])
    pos = [r[0] for r in rows]
    half = [0.62 * fontsize * (r[3].count("\n") + 1) for r in rows]   # half-height of each label, points
    for _ in range(50):
        for i in range(1, len(pos)):
            short = (half[i] + half[i - 1] + 1.5) - (pos[i] - pos[i - 1])
            if short > 0:
                pos[i - 1] -= short / 2
                pos[i] += short / 2
    for (p0, y, c, t), p in zip(rows, pos):
        end_label(ax, latest, y, c, t, fontsize=fontsize, dy=p - p0)


def finish(fig, ax, title, name):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    fig.text(0.99, 0.01, "tradewartracker.com  ·  Source: US Census Bureau",
             ha="right", va="bottom", fontsize=7, color="#999999")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(name, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", name)


# ----------------------------------------------------------------------------- #
# charts
# ----------------------------------------------------------------------------- #
def chart_1(deficit, latest, name):
    """Monthly goods trade deficit (imports minus exports) with ASEAN and with
    China, the latest month's value as the end label."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for who in (ASEAN, CHINA):
        s = deficit[who].loc[X_START:]
        ax.plot(s.index, s.values, color=COLOR[who], lw=LW, alpha=ALPHA, label=who)
    style(ax, latest)
    end_labels(ax, latest, [(float(deficit[who].loc[latest]), COLOR[who], dollars(deficit[who].loc[latest]))
                            for who in (ASEAN, CHINA)])
    finish(fig, ax, "US goods trade deficit with ASEAN vs China (monthly)", name)


def chart_2(rate, latest, name):
    """Effective tariff rate (calculated duties / customs value) on imports from
    ASEAN and from China, the latest month's rate as the end label."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for who in (ASEAN, CHINA):
        s = rate[who].loc[X_START:]
        ax.plot(s.index, s.values, color=COLOR[who], lw=LW, alpha=ALPHA, label=who)
    style(ax, latest, percent=True)
    ax.set_ylim(bottom=0)
    end_labels(ax, latest, [(float(rate[who].loc[latest]), COLOR[who], f"{rate[who].loc[latest]:.1f}%")
                            for who in (ASEAN, CHINA)])
    finish(fig, ax, "US imports from ASEAN and China — effective tariff rate (duties ÷ value)", name)


def chart_3(total, ai, latest, name):
    """The deficit with ASEAN and the part of it that is AI-related products,
    each with the latest month's value and its change on a year earlier."""
    parts = [(total, "Total", TOTAL_COLOR), (ai, "AI-related products", AI_COLOR)]
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for s, label, color in parts:
        shown = s.loc[X_START:]
        ax.plot(shown.index, shown.values, color=color, lw=LW, alpha=ALPHA, label=label)
    style(ax, latest)
    end_labels(ax, latest, [(float(s.loc[latest]), color, f"{dollars(s.loc[latest])}\n{yoy(s, latest):+.1f}% YoY")
                            for s, _, color in parts])
    finish(fig, ax, "US goods trade deficit with ASEAN — total and AI-related products (monthly)", name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    latest = df["month"].max()
    wide = lambda col: df.pivot(index="month", columns="partner", values=col).sort_index().astype(float)
    imports, exports, duties = wide("imports_usd"), wide("exports_usd"), wide("duties_usd")
    ai_imports, ai_exports = wide("ai_imports_usd"), wide("ai_exports_usd")

    deficit = imports - exports                     # the deficit drawn as a positive number
    rate = 100 * duties / imports
    ai_deficit = ai_imports[ASEAN] - ai_exports[ASEAN]

    chart_1(deficit, latest, "chart_1_deficit_asean_vs_china.png")
    chart_2(rate, latest, "chart_2_tariff_asean_vs_china.png")
    chart_3(deficit[ASEAN], ai_deficit, latest, "chart_3_asean_deficit_total_vs_ai.png")


if __name__ == "__main__":
    main()
