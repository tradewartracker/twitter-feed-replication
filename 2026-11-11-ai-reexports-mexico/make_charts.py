"""Replicate the two charts in the 11 Nov 2026 thread on US exports of AI-related
products: exports made in the US against re-exports, and re-exports to Mexico
against re-exports to every other country combined.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes two PNGs (chart_1_domestic_vs_reexports.png,
chart_2_reexports_by_destination.png) into the current folder, overwriting the
shipped copies. They should come out identical.

Data: US Census Bureau, monthly exports by Schedule B (10-digit) code and country,
split into domestic exports and foreign exports (re-exports). "AI-related" is the
High-relevance tag from the paper "Trade in AI-Related Products". See README.md.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

LATEST = pd.Timestamp("2026-09-01")
X_START = pd.Timestamp("2023-01-01")
X_PAD_MONTHS = 6                        # runway after the last month so the end labels fit
TARIFF_ERA = (pd.Timestamp("2025-01-01"), "2025 tariff era")
YTD_START = "2026-01-01"                # the annotations sum January to September 2026
LW, ALPHA = 3.5, 0.9
MX_GREEN = "#006847"                    # Mexico's colour on tradewartracker.com
BLUE, RED, GREY = "darkblue", "#8B0000", "#7F7F7F"
TOTAL = "TOTAL FOR ALL COUNTRIES"
FOOT = "tradewartracker.com  ·  Source: US Census Bureau"


# ----------------------------------------------------------------------------- #
# number formatting
# ----------------------------------------------------------------------------- #
def fmt_dollars(x):
    sign = "-" if x < 0 else ""
    x = abs(x)
    for div, suf in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if x >= div:
            return f"{sign}${x / div:.1f}{suf}"
    return f"{sign}${x:,.0f}"


def fmt_pct(x):
    return f"{x:+.1f}%"


def esc(s):
    """Two '$' in one string switch matplotlib into mathtext; escape them."""
    return s.replace("$", r"\$")


def yoy(s, t=LATEST):
    """Latest value vs the same month a year earlier, in percent."""
    prior, now = s.get(t - pd.DateOffset(months=12)), s.get(t)
    return (now / prior - 1) * 100 if prior and now and prior > 0 else np.nan


def spread(ends, span, gap=0.075):
    """Vertical nudges (points) for end labels whose y values sit within `gap` of the
    axis span of each other, so two-line labels do not overprint."""
    order = sorted(range(len(ends)), key=lambda i: ends[i])
    dy = [0.0] * len(ends)
    for a, b in zip(order, order[1:]):
        if ends[b] - ends[a] < gap * span:
            dy[a] -= 11
            dy[b] += 11
    return dy


# ----------------------------------------------------------------------------- #
# the house style (tradewartracker.com charts)
# ----------------------------------------------------------------------------- #
def end_label(ax, x, y, color, text, fontsize=11, dy=0.0):
    """Bold, colour-matched value label at the end of a line; dy nudges it (points)."""
    if y is None or (isinstance(y, float) and np.isnan(y)):
        return
    ax.annotate(text, xy=(x, y), xytext=(8, dy), textcoords="offset points",
                fontsize=fontsize, fontweight="bold", color=color, alpha=1.0,
                va="center", zorder=5)


def style(ax, latest, value_kind):
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
    if value_kind == "dollars":
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: fmt_dollars(x)))


def lines(ax, m, spec):
    """Each series twice: the monthly values thin and pale, the 3-month average bold.
    The end label is the latest 3-month average and its change on a year earlier."""
    ma = m.rolling(3).mean()
    ends = [ma[c].loc[LATEST] for c, _, _ in spec]
    dys = spread(ends, ma.loc["2023":].max().max())
    for (col, label, color), dy in zip(spec, dys):
        ax.plot(m.index, m[col], color=color, lw=1.2, alpha=0.25)
        ax.plot(ma.index, ma[col], color=color, lw=LW, alpha=ALPHA, label=label)
        end_label(ax, LATEST, ma[col].loc[LATEST], color,
                  fmt_dollars(ma[col].loc[LATEST]) + f"\n{fmt_pct(yoy(ma[col]))} YoY", fontsize=9, dy=dy)
    style(ax, LATEST, "dollars")


def note(ax, text, xy):
    ax.text(*xy, esc(text), transform=ax.transAxes, ha="left", va="top", fontsize=9, color="#333333",
            linespacing=1.5)


def finish(fig, ax, title, name):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    fig.text(0.99, 0.01, FOOT, ha="right", va="bottom", fontsize=7, color="#999999")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(name, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", name)


def wide(c):
    """series x month matrix on a full monthly index."""
    m = c.pivot(index="month", columns="series", values="value").sort_index()
    return m.reindex(pd.date_range(m.index.min(), LATEST, freq="MS")).fillna(0).astype(float)


# ----------------------------------------------------------------------------- #
# charts
# ----------------------------------------------------------------------------- #
def chart_1(c1, name):
    """AI-related exports to all countries: made in the US vs re-exports."""
    w = wide(c1)
    m = pd.DataFrame({"domestic": w["ai_domestic"], "reexports": w["ai_reexports"]})
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    lines(ax, m, [("domestic", "Made in the US", BLUE),
                  ("reexports", "Re-exports: foreign-made, imported, shipped out again", RED)])
    y = m.loc[YTD_START:].sum()
    g = w.loc[YTD_START:, ["all_goods_domestic", "all_goods_reexports"]].sum()
    share = 100 * y["reexports"] / y.sum()
    share_all = 100 * g["all_goods_reexports"] / g.sum()
    note(ax, f"Jan–Sep 2026: {share:.0f}% of AI-related exports were re-exports\n"
             f"(all US goods exports: {share_all:.0f}%)", (0.02, 0.70))
    finish(fig, ax, "US exports of AI-related products — made in the US vs re-exports (3-mo averages)", name)


def chart_2(c2, name):
    """AI-related re-exports: to Mexico vs to every other country combined."""
    w = wide(c2)
    m = pd.DataFrame({"mexico": w["MEXICO"], "all_other": w[TOTAL] - w["MEXICO"]})
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    lines(ax, m, [("mexico", "Re-exported to Mexico", MX_GREEN),
                  ("all_other", "Re-exported to every other country combined", GREY)])
    y = m.loc[YTD_START:].sum()
    d = w.loc[YTD_START:].drop(columns=TOTAL).sum().sort_values(ascending=False)
    a, b, c = (f"{e.title()} {fmt_dollars(v)}" for e, v in d.iloc[1:4].items())
    note(ax, f"Jan–Sep 2026: Mexico took {fmt_dollars(y['mexico'])},\n{100 * y['mexico'] / y.sum():.0f}% of all "
             f"AI-related re-exports\nNext: {a} ·\n{b} · {c}", (0.02, 0.76))
    finish(fig, ax, "Where the AI-related re-exports go — Mexico vs the rest of the world (3-mo averages)", name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    chart_1(df[df["chart"] == 1], "chart_1_domestic_vs_reexports.png")
    chart_2(df[df["chart"] == 2], "chart_2_reexports_by_destination.png")


if __name__ == "__main__":
    main()
