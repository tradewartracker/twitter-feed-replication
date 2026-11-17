"""Replicate the three charts in the 15 Nov 2026 thread on hockey equipment and
the Section 338 duties on Canada: the effective tariff rate on hockey sticks,
skates and gear from China and from Canada, and US imports of them from each
country as an index (2024 = 100) and in dollars as a 3-month average.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes three PNGs (chart_1_tariff_china_vs_canada.png,
chart_2_imports_index.png, chart_3_imports_3mo_average.png) into the current
folder, overwriting the shipped copies. They should come out identical.

Data: US Census Bureau monthly imports (FT900 / USA Trade Online) of three
HTS10 lines, summed: ice-hockey sticks, other hockey equipment and ice skates
(value = customs value, duties = calculated duties).
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

BASE_YEAR = "2024"                          # index: this year's monthly average = 100
X_START = pd.Timestamp("2023-01-01")        # charts 2 and 3; data.csv starts in 2022
X_START_TARIFF = pd.Timestamp("2024-01-01") # chart 1: nothing happens before 2025
X_PAD_MONTHS = 6                            # runway after the last month so the end labels fit
# dashed vertical rules: (date, colour, label)
EVENTS = [(pd.Timestamp("2025-01-01"), "red", "2025 tariff era"),
          (pd.Timestamp("2026-08-22"), "#8B0000", "Sec. 338 50% duty")]
LW, ALPHA = 3.5, 0.9

CHINA, CANADA = "China", "Canada"
# China keeps its flag red; Canada's flag is the same red, so it draws dark blue
PAIR = [(CHINA, "#DE2910"), (CANADA, "darkblue")]


# ----------------------------------------------------------------------------- #
# number helpers
# ----------------------------------------------------------------------------- #
def dollars(x):
    """$7.0M, $727.5K, ..."""
    sign = "-" if x < 0 else ""
    x = abs(x)
    for div, suf in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if x >= div:
            return f"{sign}${x / div:.1f}{suf}"
    return f"{sign}${x:,.0f}"


def yoy(s, latest):
    """Latest value vs the same month a year earlier, in percent."""
    prior = s.get(latest - pd.DateOffset(months=12))
    return (float(s.iloc[-1]) / prior - 1) * 100


# ----------------------------------------------------------------------------- #
# the house style (tradewartracker.com charts)
# ----------------------------------------------------------------------------- #
def style(ax, latest, x_start, kind=None):
    ax.set_facecolor("#ffffff")
    ax.figure.set_facecolor("#ffffff")
    ax.grid(True, alpha=0.3, linewidth=0.6)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    x_end = latest + pd.DateOffset(months=X_PAD_MONTHS)
    for t, color, label in EVENTS:
        ax.axvline(t, color=color, alpha=0.55, lw=1.8, ls=(0, (6, 4)), zorder=0)
        ax.annotate(label, xy=(t, 1), xycoords=("data", "axes fraction"),
                    xytext=(4, -4), textcoords="offset points",
                    fontsize=7.5, color=color, alpha=0.75, ha="left", va="top", zorder=0)
    ax.set_xlim(x_start, x_end)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    if kind == "dollars":
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: dollars(x)))
    elif kind == "percent":
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:.0f}%"))


def end_label(ax, x, y, color, text, fontsize=11, dy=0.0):
    """Bold, colour-matched label at the end of a line; dy nudges it (points)."""
    ax.annotate(text, xy=(x, y), xytext=(8, dy), textcoords="offset points",
                fontsize=fontsize, fontweight="bold", color=color, alpha=1.0,
                va="center", zorder=5)


def end_labels(ax, latest, items, fontsize=9):
    """End-of-line labels, nudged apart where they would overprint and kept
    above the x-axis. items = [(y, color, text)]; call once the y-limits are
    final."""
    x = mdates.date2num(latest)
    to_pt = 72.0 / ax.figure.dpi
    floor = ax.transData.transform((x, ax.get_ylim()[0]))[1] * to_pt
    rows = sorted(([ax.transData.transform((x, y))[1] * to_pt, y, c, t] for y, c, t in items),
                  key=lambda r: r[0])
    pos = [r[0] for r in rows]
    half = [0.62 * fontsize * (r[3].count("\n") + 1) for r in rows]   # half-height of each label, points
    pos[0] = max(pos[0], floor + half[0] + 1.5)
    for i in range(1, len(pos)):
        pos[i] = max(pos[i], pos[i - 1] + half[i] + half[i - 1] + 1.5)
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
def chart_1(imports, duties, latest, name):
    """Effective tariff rate (calculated duties / customs value) on the three
    lines together, from China and from Canada, from January 2024."""
    rate = 100 * duties / imports
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for e, color in PAIR:
        x = rate[e]["2024-01-01":]
        ax.plot(x.index, x.values, color=color, lw=LW, alpha=ALPHA, label=e)
    style(ax, latest, X_START_TARIFF, "percent")
    ax.set_ylim(bottom=0)
    end_labels(ax, latest, [(float(rate[e].iloc[-1]), color, f"{rate[e].iloc[-1]:.1f}%") for e, color in PAIR],
               fontsize=10)
    finish(fig, ax, "Hockey sticks, skates and gear (HS 9506.99.25, 9506.70.40) — effective tariff rate", name)


def chart_2(imports, latest, name):
    """Imports from each country as an index on its own 2024 monthly average.
    The legend carries the dollar scale the index drops."""
    idx = 100 * imports / imports.loc[BASE_YEAR].mean()
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.axhline(100, color="#999999", lw=0.8, ls="--", zorder=0)
    for e, color in PAIR:
        ax.plot(idx.index, idx[e].values, color=color, lw=LW, alpha=ALPHA, zorder=3,
                label=f"{e} ({BASE_YEAR} average: ${imports[e].loc[BASE_YEAR].mean() / 1e6:.1f}M a month)")
    style(ax, latest, X_START)
    ax.set_ylim(0, idx[[e for e, _ in PAIR]].loc[X_START:].max().max() * 1.12)
    ax.set_ylabel(f"Index ({BASE_YEAR} monthly average = 100)", fontsize=9)
    end_labels(ax, latest, [(float(idx[e].iloc[-1]), color,
                             f"{idx[e].iloc[-1]:.0f}\n{yoy(idx[e], latest):+.1f}% YoY") for e, color in PAIR])
    finish(fig, ax, f"Hockey sticks, skates and gear — US imports, {BASE_YEAR} = 100", name)


def chart_3(imports, latest, name):
    """Imports in dollars: the 3-month average (the month and the two before
    it) as the heavy line, the monthly series thin and faint behind it. Only
    the average is labelled."""
    avg = imports.rolling(3).mean()
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for e, color in PAIR:
        ax.plot(imports.index, imports[e].values, color=color, lw=1.3, alpha=0.35, zorder=1)
        ax.plot(avg.index, avg[e].values, color=color, lw=LW, alpha=ALPHA, zorder=3, label=e)
    ax.plot([], [], color="#777777", lw=1.3, alpha=0.6, label="Thin lines: monthly")
    style(ax, latest, X_START, "dollars")
    ax.set_ylim(0, imports[[e for e, _ in PAIR]].loc[X_START:].max().max() * 1.12)
    end_labels(ax, latest, [(float(avg[e].iloc[-1]), color,
                             f"{dollars(avg[e].iloc[-1])}\n{yoy(avg[e], latest):+.1f}% YoY") for e, color in PAIR])
    finish(fig, ax, "Hockey sticks, skates and gear — US imports, 3-month average", name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    latest = df["month"].max()
    imports = df.pivot(index="month", columns="source", values="imports_usd").sort_index().astype(float)
    duties = df.pivot(index="month", columns="source", values="duties_usd").sort_index().astype(float)

    chart_1(imports, duties, latest, "chart_1_tariff_china_vs_canada.png")
    chart_2(imports, latest, "chart_2_imports_index.png")
    chart_3(imports, latest, "chart_3_imports_3mo_average.png")


if __name__ == "__main__":
    main()
