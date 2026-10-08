"""Replicate the three charts in the 8 Oct 2026 tweet on US imports of
solid-state storage (HS 852351): total value, total volume, and unit value by
source country.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes three PNGs (chart_1_total_value.png,
chart_2_total_volume.png, chart_3_unit_value_by_source.png) into the current
folder, overwriting the shipped copies. They should come out identical.

Data: US Census Bureau monthly imports (FT900 / USA Trade Online), all HS10
lines under HS 852351, general imports (value = customs value). See README.md.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

PRODUCT = "Solid-State Storage (SSD/Flash) (HS852351)"
TOTAL = "TOTAL FOR ALL COUNTRIES"
SOURCES = ["KOREA, SOUTH", "TAIWAN", "VIETNAM", "MALAYSIA"]   # ranked by Aug-2026 value
COLORS = {                      # flag colours; Malaysia drawn gold so it is not Vietnam's red
    "KOREA, SOUTH": "#003478",
    "TAIWAN": "#000095",
    "VIETNAM": "#DA251D",
    "MALAYSIA": "#D4A017",
}
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


def fmt_number(x):
    """Scale like dollars but without the $ (used for unit counts)."""
    sign = "-" if x < 0 else ""
    a = abs(x)
    for div, suf in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if a >= div:
            return f"{sign}{a/div:.1f}{suf}"
    return f"{sign}{a:,.0f}"


def fmt_unit_value(x):
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
    """One black line for total US imports, y-axis cropped to the data (not
    zero-based), latest value + YoY as the end-of-line label."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.plot(s.index, s.values, color="black", lw=LW, alpha=ALPHA)
    style(ax, s.index[-1], value_kind)
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + 0.10 * (hi - lo))          # headroom for the marker label
    if value_kind == "quantity":
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: fmt_number(x)))
    end_label(ax, s.index[-1], s.iloc[-1], "black", end_text)
    finish(fig, ax, title, name)


def chart_unit_value_by_source(df, name):
    """Unit value (customs value / Census quantity) for the four largest
    sources. Linear y on purpose: the spread between sources is the point."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for i, e in enumerate(SOURCES):
        s = df.loc[df["entity"] == e].set_index("month")["unit_value_usd"]
        color = COLORS[e]
        ax.plot(s.index, s.values, color=color, lw=LW, alpha=ALPHA,
                label=e.title(), zorder=3 + len(SOURCES) - i)
        end_label(ax, s.index[-1], s.iloc[-1], color, fmt_unit_value(s.iloc[-1]), fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    style(ax, s.index[-1], None)
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    finish(fig, ax, f"{PRODUCT} — unit value by source ($ per unit)", name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    tot = df.loc[df["entity"] == TOTAL].set_index("month")

    value = tot["imports_usd"].astype(float)
    chart_aggregate(value, "dollars", f"{PRODUCT} — total US imports",
                    "chart_1_total_value.png",
                    f"{fmt_dollars(value.iloc[-1])}\n{yoy_pct(value):+.1f}% YoY")

    volume = tot["quantity"].astype(float)
    chart_aggregate(volume, "quantity", f"{PRODUCT} — total US imports by volume (units)",
                    "chart_2_total_volume.png",
                    f"{fmt_number(volume.iloc[-1])} units\n{yoy_pct(volume):+.1f}% YoY")

    chart_unit_value_by_source(df, "chart_3_unit_value_by_source.png")


if __name__ == "__main__":
    main()
