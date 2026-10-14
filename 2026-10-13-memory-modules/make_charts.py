"""Replicate the three charts in the 13 Oct 2026 thread on US imports of
memory modules and computer parts (HS 847330): total value, unit value of all
imports, and the three largest source countries.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes three PNGs (chart_1_total_value.png,
chart_2_unit_value_all_sources.png, chart_3_top_3_sources.png) into the current
folder, overwriting the shipped copies. They should come out identical.

Data: US Census Bureau monthly imports (FT900 / USA Trade Online), all HTS10
lines under HS 847330, general imports (value = customs value). See README.md.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

PRODUCT = "Computer Parts & Memory Modules (HS847330)"
TOTAL = "TOTAL FOR ALL COUNTRIES"
# chart 3: the three largest sources by August-2026 value, in legend order.
# Vietnam and Taiwan draw in their flag colours; South Korea's flag blue is
# Taiwan's blue, so it is drawn gold on this chart.
SOURCES = [
    ("VIETNAM",      "Vietnam",      "#DA251D"),
    ("TAIWAN",       "Taiwan",       "#000095"),
    ("KOREA, SOUTH", "Korea, South", "#D4A017"),
]
X_START = pd.Timestamp("2023-01-01")
X_PAD_MONTHS = 6                # runway after the last month so the end labels fit
TARIFF_ERA = (pd.Timestamp("2025-01-01"), "2025 tariff era")
LW, ALPHA = 3.5, 0.9


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


def fmt_unit_value(x):
    """Exact dollars with commas; cents only under $10 ($1,357 must not print as $1.4K)."""
    return f"${x:,.2f}" if abs(x) < 10 else f"${x:,.0f}"


def yoy_pct(s):
    """Latest value vs the same month a year earlier, in percent."""
    latest_t = s.index[-1]
    prior_t = latest_t - pd.DateOffset(months=12)
    return 100 * (s.iloc[-1] / s.loc[prior_t] - 1)


# ----------------------------------------------------------------------------- #
# the house style (tradewartracker.com charts)
# ----------------------------------------------------------------------------- #
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


def end_label(ax, x, y, color, text, fontsize=11):
    ax.annotate(text, xy=(x, y), xytext=(8, 0), textcoords="offset points",
                fontsize=fontsize, fontweight="bold", color=color, va="center", zorder=5)


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
def chart_aggregate(s, value_kind, title, name, end_text):
    """One black line for all US imports of the product, y-axis cropped to the
    data (not zero-based), latest value + YoY as the end-of-line label."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.plot(s.index, s.values, color="black", lw=LW, alpha=ALPHA)
    style(ax, s.index[-1], value_kind)
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + 0.10 * (hi - lo))          # headroom for the marker label
    if value_kind == "unit_value":
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    end_label(ax, s.index[-1], s.iloc[-1], "black", end_text)
    finish(fig, ax, title, name)


def chart_top_sources(df, name):
    """Customs value of imports from the three largest sources. No end-of-line
    labels on this one, as posted; the legend carries the names."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for entity, label, color in SOURCES:
        s = df.loc[df["entity"] == entity].set_index("month")["imports_usd"].astype(float)
        ax.plot(s.index, s.values, color=color, lw=LW, alpha=ALPHA, label=label)
    style(ax, s.index[-1], "dollars")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    finish(fig, ax, f"{PRODUCT} — top 3 sources", name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    tot = df.loc[df["entity"] == TOTAL].set_index("month")

    value = tot["imports_usd"].astype(float)
    chart_aggregate(value, "dollars", f"{PRODUCT} — total US imports",
                    "chart_1_total_value.png",
                    f"{fmt_dollars(value.iloc[-1])}\n{yoy_pct(value):+.1f}% YoY")

    uv = tot["unit_value_usd"]
    chart_aggregate(uv, "unit_value", f"{PRODUCT} — unit value, all sources ($ per unit)",
                    "chart_2_unit_value_all_sources.png",
                    f"{fmt_unit_value(uv.iloc[-1])}\n{yoy_pct(uv):+.1f}% YoY")

    chart_top_sources(df, "chart_3_top_3_sources.png")


if __name__ == "__main__":
    main()
