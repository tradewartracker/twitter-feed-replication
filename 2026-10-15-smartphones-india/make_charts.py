"""Replicate the three charts in the 15 Oct 2026 thread on US smartphone
imports (HS 851713): total imports with yearly averages, the trailing-12-month
share of imports from India, Vietnam and China, and the effective tariff rate
each of those sources pays.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes three PNGs (chart_1_total_imports.png,
chart_2_share_12m.png, chart_3_tariff_by_source.png) into the current folder,
overwriting the shipped copies. They should come out identical.

Data: US Census Bureau monthly imports (FT900 / USA Trade Online), general
imports of HTS 8517.13.0000 by source country (value = customs value,
duties = calculated duties). See README.md for the column definitions.
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
# India = its flag saffron; Vietnam = the house dark blue (its flag red is the
# same hue as China's); China = its flag red; the total is black.
SOURCES = [
    ("india",   "India",   "#FF9933"),
    ("vietnam", "Vietnam", "darkblue"),
    ("china",   "China",   "#DE2910"),
]
ALL = ("all", "All sources", "black")
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


def finish(fig, ax, title, name, legend=True, legend_loc="upper left"):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    if legend:
        ax.legend(loc=legend_loc, fontsize=9, frameon=False)
    fig.text(0.99, 0.01, "tradewartracker.com  ·  Source: US Census Bureau",
             ha="right", va="bottom", fontsize=7, color="#999999")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(name, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", name)


# ----------------------------------------------------------------------------- #
# charts
# ----------------------------------------------------------------------------- #
def chart_total(s, latest, name):
    """One black line for all US smartphone imports, y-axis cropped to the data
    (not zero-based), the latest value as the end label, and a dashed segment per
    calendar year at that year's average monthly value. No YoY: August 2025 was
    the trough of the tariff hit, so the year-on-year change is a base effect."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.plot(s.index, s.values, color="black", lw=LW, alpha=ALPHA)
    style(ax, latest, "dollars", pd.Timestamp("2023-01-01"))
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + 0.10 * (hi - lo))          # headroom for the marker label
    end_label(ax, latest, float(s.iloc[-1]), "black", fmt_dollars(s.iloc[-1]))
    yearly = s.groupby(s.index.year).mean()
    for year, mean in yearly.items():
        x0 = pd.Timestamp(year, 1, 1)
        x1 = min(pd.Timestamp(year, 12, 1), latest)
        ax.hlines(mean, x0, x1, color=YEAR_LINE, lw=1.4, ls=(0, (5, 3)), alpha=0.85, zorder=2)
        tag = f"{year} YTD" if x1 < pd.Timestamp(year, 12, 1) else f"{year} avg"
        # the label sits ON the segment in a white box, so it never collides with the line
        ax.annotate(f"{tag}: {fmt_dollars(mean)}/mo", (x0 + (x1 - x0) / 2, mean),
                    ha="center", va="center", fontsize=8, color=YEAR_LINE,
                    fontweight="bold", zorder=4,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.9))
    finish(fig, ax, "Smartphones (HS851713) — total US imports", name, legend=False)


def chart_share(share, latest, name):
    """Each source's share of US smartphone imports over the trailing 12 months.
    Drawn from January 2024 (the first 12-month window ends December 2023)."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for key, label, color in SOURCES:
        s = share[key]["2024-01-01":]
        ax.plot(s.index, s.values, color=color, lw=LW, alpha=ALPHA, label=label)
        end_label(ax, latest, float(s.iloc[-1]), color, f"{s.iloc[-1]:.0f}%", fontsize=9)
    style(ax, latest, "percent", pd.Timestamp("2024-01-01"))
    finish(fig, ax, "Smartphones (HS851713) — share of US imports, trailing 12 months",
           name, legend_loc="upper right")


def chart_tariff(rate, latest, name):
    """Effective tariff rate (calculated duties / customs value) on smartphones
    from all sources and from each of the three. The lines end within half a
    point of each other, so they share one stacked end label."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for key, label, color in [ALL] + SOURCES:
        s = rate[key]["2024-01-01":]
        ax.plot(s.index, s.values, color=color, lw=LW, alpha=ALPHA, label=label)
    ends = {key: float(rate[key].iloc[-1]) for key, _, _ in SOURCES}
    end_label(ax, latest, max(ends.values()), "black",
              "\n".join(f"{label} {ends[key]:.1f}%" for key, label, _ in SOURCES), fontsize=8)
    style(ax, latest, "percent", pd.Timestamp("2024-01-01"))
    finish(fig, ax, "Smartphones (HS851713) — effective tariff rate by source (duties ÷ value)",
           name, legend_loc="upper right")


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    latest = df["month"].max()
    val = df.pivot(index="month", columns="source", values="imports_usd").sort_index()
    rate = df.pivot(index="month", columns="source", values="tariff_rate_pct").sort_index()
    # the share column is empty for "all" (it is the denominator) and for the
    # first eleven months (no full 12-month window yet)
    share = (df[df["source"] != "all"]
             .pivot(index="month", columns="source", values="share_12m_pct")
             .sort_index().dropna())

    chart_total(val["all"], latest, "chart_1_total_imports.png")
    chart_share(share, latest, "chart_2_share_12m.png")
    chart_tariff(rate, latest, "chart_3_tariff_by_source.png")


if __name__ == "__main__":
    main()
