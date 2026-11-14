"""Replicate the two charts in the 14 Nov 2026 thread on the Section 338 duties
on Canada: US imports from Canada of the goods on the 50% list against all other
goods, as an index (2025 = 100), and the effective tariff rate on the same two
groups.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes two PNGs (chart_1_338_goods_vs_other_index.png,
chart_2_338_goods_tariff_rate.png) into the current folder, overwriting the
shipped copies. They should come out identical.

Data: US Census Bureau monthly imports from Canada (FT900 / USA Trade Online) at
HTS10, summed into the two groups described in README.md (value = customs value,
duties = calculated duties).
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

BASE_YEAR = "2025"                          # index: this year's monthly average = 100
X_START = pd.Timestamp("2025-07-01")        # both charts show a year of run-up, then the duty
X_PAD_MONTHS = 3                            # runway after the last month so the end labels fit
IN_FORCE = pd.Timestamp("2026-08-22")       # the 50% duties took effect
ANNOUNCED = pd.Timestamp("2026-07-20")      # date of the three proclamations
LW, ALPHA = 3.5, 0.9

LISTED, OTHER = "Section 338 goods", "All other goods"
COLOR = {LISTED: "#8B0000", OTHER: "darkblue"}
LABEL = {LISTED: "Goods on the Section 338 list (50% duty)", OTHER: "All other goods"}
FOOT = "tradewartracker.com  ·  Source: US Census Bureau"


# ----------------------------------------------------------------------------- #
# number helpers
# ----------------------------------------------------------------------------- #
def index_base_year(s):
    """Index with the base year's monthly average = 100."""
    return 100 * 12 * s / s.loc[BASE_YEAR].sum()


def yoy(s, latest):
    """Latest value vs the same month a year earlier, in percent."""
    prior = s.get(latest - pd.DateOffset(months=12))
    return (float(s.iloc[-1]) / prior - 1) * 100


# ----------------------------------------------------------------------------- #
# the house style (tradewartracker.com charts)
# ----------------------------------------------------------------------------- #
def rule(ax, t, color):
    """Dashed vertical rule at an event date."""
    ax.axvline(t, color=color, alpha=0.55, lw=1.8, ls=(0, (6, 4)), zorder=0)


def rule_label(ax, t, color, text, side):
    """Small label at the top of a rule, to its right or (side="left") its left."""
    left = side == "left"
    ax.annotate(text, xy=(t, 1), xycoords=("data", "axes fraction"),
                xytext=(-4 if left else 4, -4), textcoords="offset points",
                fontsize=7.5, color=color, alpha=0.75, ha="right" if left else "left", va="top", zorder=0)


def style(ax, latest, announced=False, percent=False):
    ax.set_facecolor("#ffffff")
    ax.figure.set_facecolor("#ffffff")
    ax.grid(True, alpha=0.3, linewidth=0.6)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    rule(ax, IN_FORCE, "#8B0000")
    rule_label(ax, IN_FORCE, "#8B0000", "Sec. 338 50% duty", "right")
    if announced:
        rule(ax, ANNOUNCED, "#555555")      # its label goes on once the y-limits are set
    ax.set_xlim(X_START, latest + pd.DateOffset(months=X_PAD_MONTHS))
    if percent:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:.0f}%"))


def month_ticks(ax):
    """Quarterly month ticks."""
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))


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


def finish(fig, ax, title, name, legend_loc):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    ax.legend(loc=legend_loc, fontsize=9, frameon=False)
    fig.text(0.99, 0.01, FOOT, ha="right", va="bottom", fontsize=7, color="#999999")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(name, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", name)


# ----------------------------------------------------------------------------- #
# charts
# ----------------------------------------------------------------------------- #
def chart_1(imports, latest, name):
    """Imports from Canada of the listed goods and of all other goods, each as an
    index (2025 monthly average = 100). The whole series from 2023 is plotted and
    the x-axis starts in July 2025; the y-limits are set from the months shown."""
    idx = imports.apply(index_base_year)
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.axhline(100, color="#999999", lw=0.8, ls="--", zorder=0)
    for g in (LISTED, OTHER):
        ax.plot(idx.index, idx[g].values, color=COLOR[g], lw=LW, alpha=ALPHA, label=LABEL[g])
    style(ax, latest, announced=True)
    shown = idx.loc[X_START:, [LISTED, OTHER]]
    ax.set_ylim(shown.min().min() - 8, shown.max().max() + 12)
    month_ticks(ax)
    rule_label(ax, ANNOUNCED, "#555555", f"Announced {ANNOUNCED:%b} {ANNOUNCED.day}", "left")
    ax.set_ylabel(f"Index ({BASE_YEAR} monthly average = 100)", fontsize=9)
    end_labels(ax, latest, [(float(idx[g].iloc[-1]), COLOR[g],
                             f"{idx[g].iloc[-1]:.0f}\n{yoy(idx[g], latest):+.1f}% YoY") for g in (LISTED, OTHER)])
    finish(fig, ax, f"US imports from Canada — Section 338 goods vs all other goods (index, {BASE_YEAR} = 100)",
           name, "lower left")


def chart_2(imports, duties, latest, name):
    """Effective tariff rate (calculated duties / customs value) on the same two
    groups, with the latest month's rate as the end label."""
    rate = 100 * duties / imports
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for g in (LISTED, OTHER):
        ax.plot(rate.index, rate[g].values, color=COLOR[g], lw=LW, alpha=ALPHA, label=LABEL[g])
    style(ax, latest, percent=True)
    ax.set_ylim(top=rate.loc[X_START:, [LISTED, OTHER]].max().max() * 1.14)   # room for the rule's label
    month_ticks(ax)
    end_labels(ax, latest, [(float(rate[g].iloc[-1]), COLOR[g], f"{rate[g].iloc[-1]:.1f}%") for g in (LISTED, OTHER)])
    finish(fig, ax, "US imports from Canada — effective tariff rate, Section 338 goods vs all other goods",
           name, "upper left")


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    latest = df["month"].max()
    imports = df.pivot(index="month", columns="group", values="imports_usd").sort_index().astype(float)
    duties = df.pivot(index="month", columns="group", values="duties_usd").sort_index().astype(float)

    chart_1(imports, latest, "chart_1_338_goods_vs_other_index.png")
    chart_2(imports, duties, latest, "chart_2_338_goods_tariff_rate.png")


if __name__ == "__main__":
    main()
