"""Replicate the two charts in the 9 Oct 2026 thread on US imports of servers
(HS 847150): total vs the three largest sources, and Mexico's server line
against Mexico's entire vehicle chapter (HS 87).

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes two PNGs (chart_1_all_sources_vs_top_suppliers.png,
chart_2_mexico_servers_vs_vehicles.png) into the current folder, overwriting
the shipped copies. They should come out identical.

Data: US Census Bureau monthly imports (FT900 / USA Trade Online), general
imports (value = customs value). See README.md.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

PRODUCT = "Servers & Data-Center Compute (HS847150)"
TOTAL = "TOTAL FOR ALL COUNTRIES"
X_START = pd.Timestamp("2023-01-01")
X_PAD_MONTHS = 6                # runway after the last month so the end labels fit
TARIFF_ERA = (pd.Timestamp("2025-01-01"), "2025 tariff era")
LW, ALPHA = 3.5, 0.9

# chart 1: the Census all-countries total (black) and the three largest sources
# by August-2026 value, in flag colours
CHART1 = [
    (TOTAL,      "All sources", "black"),
    ("MEXICO",   "Mexico",      "#006847"),
    ("TAIWAN",   "Taiwan",      "#000095"),
    ("THAILAND", "Thailand",    "#2D2A4A"),
]
# chart 2: both lines are Mexico, so the house palette for non-country series
# (dark blue primary, dark red contrast)
CHART2 = [
    ("HS847150", "Servers & data-center compute (one line, HS847150)", "darkblue"),
    ("HS87",     "All vehicles & parts (whole chapter, HS87)",         "#8B0000"),
]


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


def yoy_pct(s):
    """Latest value vs the same month a year earlier, in percent."""
    latest_t = s.index[-1]
    prior_t = latest_t - pd.DateOffset(months=12)
    return 100 * (s.iloc[-1] / s.loc[prior_t] - 1)


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
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: fmt_dollars(x)))


def end_label(ax, x, y, color, text, fontsize=11):
    ax.annotate(text, xy=(x, y), xytext=(8, 0), textcoords="offset points",
                fontsize=fontsize, fontweight="bold", color=color, va="center", zorder=5)


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
def chart_1(df, name):
    """Total US imports of HS 847150 (black) over the three largest sources.
    No end-of-line labels on this one, as posted."""
    d = df[df["chart"] == 1]
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for entity, label, color in CHART1:
        s = d.loc[d["entity"] == entity].set_index("month")["imports_usd"].astype(float)
        ax.plot(s.index, s.values, color=color, lw=LW, alpha=ALPHA, label=label)
    style(ax, s.index[-1])
    finish(fig, ax, f"{PRODUCT} — all sources vs top suppliers", name)


def chart_2(df, name):
    """US imports from Mexico: one HS6 line (servers) against the whole HS 87
    chapter (vehicles and parts), with latest value + YoY as end labels."""
    d = df[df["chart"] == 2]
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for product, label, color in CHART2:
        s = d.loc[d["product"] == product].set_index("month")["imports_usd"].astype(float)
        ax.plot(s.index, s.values, color=color, lw=LW, alpha=ALPHA, label=label)
        end_label(ax, s.index[-1], s.iloc[-1], color,
                  f"{fmt_dollars(s.iloc[-1])}\n{yoy_pct(s):+.1f}% YoY", fontsize=9)
    style(ax, s.index[-1])
    finish(fig, ax, "US imports from Mexico — one server line vs the whole vehicle chapter", name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    chart_1(df, "chart_1_all_sources_vs_top_suppliers.png")
    chart_2(df, "chart_2_mexico_servers_vs_vehicles.png")


if __name__ == "__main__":
    main()
