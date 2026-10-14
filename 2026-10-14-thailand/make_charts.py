"""Replicate the three charts in the 14 Oct 2026 thread on US imports from
Thailand: all products, datacenter hardware vs everything else, and the
effective tariff rate on each of those plus the total.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes three PNGs (chart_1_total_imports.png,
chart_2_datacenter_vs_other.png, chart_3_tariff_three_lines.png) into the
current folder, overwriting the shipped copies. They should come out identical.

Data: US Census Bureau monthly imports (FT900 / USA Trade Online), general
imports from Thailand at HTS10, summed into the groups in README.md
(value = customs value, duties = calculated duties).
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

X_START = pd.Timestamp("2023-01-01")
X_PAD_MONTHS = 6                # runway after the last month so the end labels fit
TARIFF_ERA = (pd.Timestamp("2025-01-01"), "2025 tariff era")
LW, ALPHA = 3.5, 0.9
# the house palette for non-country series: black aggregate, dark blue primary,
# dark red contrast
GROUPS = [
    ("datacenter", "Datacenter hardware (6 product lines)", "darkblue"),
    ("other",      "Everything else",                       "#8B0000"),
]
ALL = ("all", "All imports from Thailand", "black")


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
    elif value_kind == "percent":
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:.0f}%"))


def end_label(ax, x, y, color, text, fontsize=11):
    ax.annotate(text, xy=(x, y), xytext=(8, 0), textcoords="offset points",
                fontsize=fontsize, fontweight="bold", color=color, va="center", zorder=5)


def finish(fig, ax, title, name, legend=True):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    if legend:
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
def chart_total(s, latest, name):
    """One black line for all US imports from Thailand, y-axis cropped to the
    data (not zero-based), latest value + YoY as the end-of-line label."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.plot(s.index, s.values, color="black", lw=LW, alpha=ALPHA)
    style(ax, latest, "dollars")
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + 0.10 * (hi - lo))          # headroom for the marker label
    end_label(ax, latest, float(s.iloc[-1]), "black",
              f"{fmt_dollars(s.iloc[-1])}\n{yoy_pct(s):+.1f}% YoY")
    finish(fig, ax, "US imports from Thailand — all products", name, legend=False)


def chart_groups(val, latest, name):
    """Customs value of the two groups, latest value + YoY as end labels."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for key, label, color in GROUPS:
        s = val[key]
        ax.plot(s.index, s.values, color=color, lw=LW, alpha=ALPHA, label=label)
        end_label(ax, latest, float(s.iloc[-1]), color,
                  f"{fmt_dollars(s.iloc[-1])}\n{yoy_pct(s):+.1f}% YoY", fontsize=9)
    style(ax, latest, "dollars")
    finish(fig, ax, "US imports from Thailand — datacenter hardware vs everything else", name)


def chart_tariff(rate, latest, name):
    """Effective tariff rate (calculated duties / customs value) on all imports
    from Thailand and on each group."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for key, label, color in [ALL] + GROUPS:
        s = rate[key]
        ax.plot(s.index, s.values, color=color, lw=LW, alpha=ALPHA, label=label)
        end_label(ax, latest, float(s.iloc[-1]), color, f"{s.iloc[-1]:.1f}%", fontsize=9)
    style(ax, latest, "percent")
    finish(fig, ax, "US imports from Thailand — effective tariff rate (duties ÷ value)", name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    latest = df["month"].max()
    val = df.pivot(index="month", columns="group", values="imports_usd").sort_index()
    rate = df.pivot(index="month", columns="group", values="tariff_rate_pct").sort_index()

    chart_total(val["all"], latest, "chart_1_total_imports.png")
    chart_groups(val, latest, "chart_2_datacenter_vs_other.png")
    chart_tariff(rate, latest, "chart_3_tariff_three_lines.png")


if __name__ == "__main__":
    main()
