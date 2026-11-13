"""Replicate the two charts in the 12 Nov 2026 thread on tariffs by end use:
the effective tariff rate on consumer, intermediate and capital goods, and the
capital-goods rate split into AI-related and other capital goods.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes two PNGs (chart_1_tariff_by_end_use.png,
chart_2_tariff_capital_ai_vs_other.png) into the current folder, overwriting
the shipped copies. They should come out identical.

Data: US Census Bureau monthly imports (FT900 / USA Trade Online), all
countries, at HTS10, summed into the end-use groups described in README.md
(value = customs value, duties = calculated duties).
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

X_START = pd.Timestamp("2023-01-01")
X_PAD_MONTHS = 6                # runway after the last month so the end labels fit
TARIFF_ERA = (pd.Timestamp("2025-01-01"), "2025 tariff era")
LW, ALPHA = 3.5, 0.9

CONS, INT, CAP = "Consumer goods", "Intermediate goods", "Capital goods"
CAP_AI, CAP_OTHER = "AI-related capital goods", "Other capital goods"
# house palette: dark red contrast, dark blue primary, gold third series, grey remainder
COLOR = {CONS: "#8B0000", INT: "#D4A017", CAP: "darkblue", CAP_AI: "darkblue", CAP_OTHER: "#7F7F7F"}


# ----------------------------------------------------------------------------- #
# the house style (tradewartracker.com charts)
# ----------------------------------------------------------------------------- #
def style(ax, latest):
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
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:.0f}%"))


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
def chart_tariff(rate, latest, groups, title, name):
    """Effective tariff rate (calculated duties / customs value), one line per
    group, with the latest month's rate as the end label."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for g in groups:
        ax.plot(rate.index, rate[g].values, color=COLOR[g], lw=LW, alpha=ALPHA, label=g)
    style(ax, latest)
    end_labels(ax, latest, [(float(rate[g].iloc[-1]), COLOR[g], f"{rate[g].iloc[-1]:.1f}%") for g in groups])
    finish(fig, ax, title, name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    latest = df["month"].max()
    rate = df.pivot(index="month", columns="group", values="tariff_rate_pct").sort_index()

    chart_tariff(rate, latest, [CONS, INT, CAP],
                 "US imports — effective tariff rate by end use (duties ÷ value)",
                 "chart_1_tariff_by_end_use.png")
    chart_tariff(rate, latest, [CONS, CAP_AI, CAP_OTHER],
                 "US imports — effective tariff rate, consumer goods vs capital goods",
                 "chart_2_tariff_capital_ai_vs_other.png")


if __name__ == "__main__":
    main()
