"""Replicate the four charts in the 16 Oct 2026 thread on US passenger-car
imports (HS 8703): the number of cars imported from all sources with yearly
averages, the effective tariff rate on all of them, the number of cars from
Japan, and the average customs value of a car from Japan.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes four PNGs (chart_1_total_units.png,
chart_2_tariff.png, chart_3_japan_units.png, chart_4_japan_unit_value.png)
into the current folder, overwriting the shipped copies. They should come
out identical.

Data: US Census Bureau monthly imports (FT900 / USA Trade Online), general
imports of every HTS10 line under HS 8703 summed per source and month
(value = customs value, duties = calculated duties, units = number of
vehicles). See README.md for the column definitions.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

X_PAD_MONTHS = 6                # runway after the last month so the end labels fit
TARIFF_ERA = (pd.Timestamp("2025-01-01"), "2025 tariff era")
LW, ALPHA = 3.5, 0.9
JAPAN = "#BC002D"               # Japan's flag red; the all-sources lines are black
YEAR_LINE = "#8B0000"           # the house contrast colour, for the yearly-average segments


# ----------------------------------------------------------------------------- #
# number formatting
# ----------------------------------------------------------------------------- #
def fmt_dollars(x):
    sign = "-" if x < 0 else ""
    x = abs(x)
    for div, suf in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if x >= div:
            return f"{sign}${x/div:.1f}{suf}"
    return f"{sign}${x:,.0f}"


def fmt_units(x):
    return f"{x/1e3:,.0f}K"


def fmt_per_car(x):
    return f"${x/1e3:,.1f}K"


# ----------------------------------------------------------------------------- #
# the house style (tradewartracker.com charts)
# ----------------------------------------------------------------------------- #
def style(ax, latest, value_kind, x_start):
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
    if value_kind == "dollars":
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: fmt_dollars(x)))
    elif value_kind == "percent":
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:.0f}%"))


def end_label(ax, x, y, color, text, fontsize=11):
    ax.annotate(text, xy=(x, y), xytext=(8, 0), textcoords="offset points",
                fontsize=fontsize, fontweight="bold", color=color, va="center", zorder=5)


def year_segment(ax, year, mean, latest, text):
    """One dashed segment at `mean` spanning the calendar year (or to the latest
    month for a partial year), labelled in a white box. A partial year's label
    sits just under its segment so it clears the end label."""
    x0 = pd.Timestamp(year, 1, 1)
    x1 = min(pd.Timestamp(year, 12, 1), latest)
    partial = x1 < pd.Timestamp(year, 12, 1)
    ax.hlines(mean, x0, x1, color=YEAR_LINE, lw=1.4, ls=(0, (5, 3)), alpha=0.85, zorder=2)
    tag = f"{year} YTD" if partial else f"{year} avg"
    ax.annotate(f"{tag}: {text}", (x0 + (x1 - x0) / 2, mean), ha="center", va="center",
                xytext=(0, -12 if partial else 0), textcoords="offset points",
                fontsize=8, color=YEAR_LINE, fontweight="bold", zorder=4,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.9))


def finish(fig, ax, title, name):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    fig.text(0.99, 0.01, "tradewartracker.com  ·  Source: US Census Bureau",
             ha="right", va="bottom", fontsize=7, color="#999999")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(name, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", name)


# ----------------------------------------------------------------------------- #
# charts
# ----------------------------------------------------------------------------- #
def chart_units(s, latest, color, title, name):
    """Number of cars per month, y-axis cropped to the data (not zero-based),
    the latest value as the end label, and a dashed segment per calendar year
    at that year's average monthly count. No year-on-year figure: the yearly
    segments are the comparison."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.plot(s.index, s.values, color=color, lw=LW, alpha=ALPHA)
    style(ax, latest, "count", pd.Timestamp("2023-01-01"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: fmt_units(x)))
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + 0.10 * (hi - lo))          # headroom for the marker label
    end_label(ax, latest, float(s.iloc[-1]), color, fmt_units(s.iloc[-1]))
    for year, mean in s.groupby(s.index.year).mean().items():
        year_segment(ax, year, mean, latest, f"{fmt_units(mean)}/mo")
    finish(fig, ax, title, name)


def chart_tariff(rate, latest, name):
    """Effective tariff rate (calculated duties / customs value) on cars from
    all sources, with the peak month marked. The whole series (2023 on) is
    plotted and the x-axis is cropped to start in January 2024, so the y-axis
    autoscale sees the 2023 months too; slicing first changes the limits."""
    s = rate
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.plot(s.index, s.values, color="black", lw=LW, alpha=ALPHA)
    style(ax, latest, "percent", pd.Timestamp("2024-01-01"))
    end_label(ax, latest, float(s.iloc[-1]), "black", f"{s.iloc[-1]:.1f}%")
    peak = s.idxmax()
    ax.annotate(f"peak {s.max():.1f}%" + "\n" + peak.strftime("%b %Y"), (peak, s.max()),
                xytext=(0, 8), textcoords="offset points", ha="center", va="bottom",
                fontsize=8, color=YEAR_LINE, fontweight="bold")
    ax.set_ylim(bottom=0, top=ax.get_ylim()[1] + 2)
    finish(fig, ax, "Passenger cars (HS8703) — effective tariff rate (duties ÷ value)", name)


def chart_unit_value(uv, value, units, latest, name):
    """Average customs value per car from Japan. The yearly segment is the
    year's value divided by the year's units, not a mean of monthly ratios."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.plot(uv.index, uv.values, color=JAPAN, lw=LW, alpha=ALPHA)
    style(ax, latest, "dollars", pd.Timestamp("2023-01-01"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: fmt_per_car(x)))
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + 0.10 * (hi - lo))
    end_label(ax, latest, float(uv.iloc[-1]), JAPAN, fmt_per_car(uv.iloc[-1]))
    for year in sorted(set(uv.index.year)):
        mean = value[str(year)].sum() / units[str(year)].sum()
        year_segment(ax, year, mean, latest, fmt_per_car(mean))
    finish(fig, ax, "Passenger cars (HS8703) — US imports from Japan, $ per car", name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    latest = df["month"].max()
    piv = lambda col: df.pivot(index="month", columns="source", values=col).sort_index()
    units, value = piv("units"), piv("imports_usd")
    rate, uv = piv("tariff_rate_pct"), piv("unit_value_usd")

    chart_units(units["all"], latest, "black",
                "Passenger cars (HS8703) — US imports, number of vehicles", "chart_1_total_units.png")
    chart_tariff(rate["all"], latest, "chart_2_tariff.png")
    chart_units(units["japan"], latest, JAPAN,
                "Passenger cars (HS8703) — US imports from Japan, number of vehicles", "chart_3_japan_units.png")
    chart_unit_value(uv["japan"], value["japan"], units["japan"], latest, "chart_4_japan_unit_value.png")


if __name__ == "__main__":
    main()
