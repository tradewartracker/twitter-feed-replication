"""Replicate the two charts in the 13 Nov 2026 thread on US exports of AI-related
products leaving through the El Paso customs district: an index of those exports
against the index for the other Texas districts and for every district outside
Texas, and El Paso's share of US exports of AI-related and of non-AI products.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes two PNGs (chart_1_el_paso_vs_rest_index.png,
chart_2_el_paso_share.png) into the current folder, overwriting the shipped
copies. They should come out identical.

Data: US Census Bureau, monthly exports by Schedule B (10-digit) code and customs
district of export. "AI-related" is the High-relevance tag from the paper "Trade in
AI-Related Products", "non-AI" the Low-relevance tag. See README.md.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

LATEST = pd.Timestamp("2026-09-01")
X_START_3MO = pd.Timestamp("2023-03-01")    # first month a 3-month average exists
X_PAD_MONTHS = 6                            # runway after the last month so the end labels fit
TARIFF_ERA = (pd.Timestamp("2025-01-01"), "2025 tariff era")
LW, ALPHA = 3.5, 0.9
BLUE, RED, GOLD = "darkblue", "#8B0000", "#DAA520"
FOOT = "tradewartracker.com  ·  Source: US Census Bureau"


# ----------------------------------------------------------------------------- #
# number helpers
# ----------------------------------------------------------------------------- #
def index_2023(s):
    """Index with the 2023 monthly average = 100."""
    return 100 * 12 * s / s.loc["2023"].sum()


def yoy(s, t=LATEST):
    """Latest value vs the same month a year earlier, in percent."""
    prior, now = s.get(t - pd.DateOffset(months=12)), s.get(t)
    return (now / prior - 1) * 100


# ----------------------------------------------------------------------------- #
# the house style (tradewartracker.com charts)
# ----------------------------------------------------------------------------- #
def style(ax, latest, x_start):
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
    ax.set_xlim(x_start, x_end)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


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
    fig.text(0.99, 0.01, FOOT, ha="right", va="bottom", fontsize=7, color="#999999")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(name, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", name)


def wide(c):
    """month x series matrix of export values, US dollars."""
    return c.pivot(index="month", columns="series", values="value").sort_index().astype(float)


# ----------------------------------------------------------------------------- #
# charts
# ----------------------------------------------------------------------------- #
def chart_1(c1, name):
    """Exports of AI-related products by district of export, as an index (2023
    monthly average = 100) and a 3-month moving average. The whole series is
    plotted and the x-axis starts at the average's first month (March 2023)."""
    spec = [("ai_el_paso", "Through the El Paso district", BLUE),
            ("ai_other_texas", "Through the other Texas districts", GOLD),
            ("ai_outside_texas", "Through every district outside Texas", RED)]
    ma = wide(c1).apply(index_2023).rolling(3).mean()
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.axhline(100, color="#999999", lw=0.8, ls="--", zorder=0)
    for col, label, color in spec:
        ax.plot(ma.index, ma[col].values, color=color, lw=LW, alpha=ALPHA, label=label)
    style(ax, LATEST, X_START_3MO)
    ax.set_ylabel("Index (2023 monthly average = 100)", fontsize=9)
    end_labels(ax, LATEST, [(float(ma[col].loc[LATEST]), color,
                             f"{ma[col].loc[LATEST]:.0f}\n{yoy(ma[col]):+.1f}% YoY") for col, _, color in spec])
    finish(fig, ax, "US exports of AI-related products — El Paso vs everywhere else (index, 3-mo average)", name)


def chart_2(c2, name):
    """The El Paso district's share of US exports of AI-related products next to
    its share of US exports of non-AI products, by calendar year (the last pair
    is the year to date)."""
    yr = wide(c2)
    yr = yr.groupby(yr.index.year).sum()
    sh = pd.DataFrame({"share_ai_pct": 100 * yr["ai_el_paso"] / yr["ai_us"],
                       "share_nonai_pct": 100 * yr["nonai_el_paso"] / yr["nonai_us"]})
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.set_facecolor("#ffffff")
    fig.set_facecolor("#ffffff")
    xs = range(len(sh))
    w = 0.36
    for off, key, color, label in ((-w / 2, "share_ai_pct", BLUE, "El Paso's share of US exports of AI-related products"),
                                   (w / 2, "share_nonai_pct", RED, "El Paso's share of US exports of non-AI products")):
        b = ax.bar([x + off for x in xs], sh[key].values, w, color=color, alpha=ALPHA,
                   edgecolor="black", linewidth=1.0, label=label)
        for rect, val in zip(b, sh[key].values):
            ax.text(rect.get_x() + rect.get_width() / 2, val + 0.3, f"{val:.1f}%", ha="center", va="bottom",
                    fontsize=10, fontweight="bold", color=color)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([f"{y}" if y < LATEST.year or LATEST.month == 12 else f"{y}\nJan–{LATEST:%b}" for y in sh.index],
                       fontsize=10, fontweight="bold")
    ax.yaxis.set_major_locator(mticker.MultipleLocator(5))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda val, p: f"{val:.0f}%"))
    ax.set_ylim(0, sh["share_ai_pct"].max() * 1.25)
    ax.grid(True, axis="y", alpha=0.3, linewidth=0.6)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    finish(fig, ax, "El Paso customs district — share of US exports, AI-related vs non-AI products", name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    chart_1(df[df["chart"] == 1], "chart_1_el_paso_vs_rest_index.png")
    chart_2(df[df["chart"] == 2], "chart_2_el_paso_share.png")


if __name__ == "__main__":
    main()
