"""Replicate the two charts in the 7 Oct 2026 thread on US imports of laptops
and portable computers (HS 847130) from Vietnam and China: monthly import value,
and the effective tariff rate each country's shipments paid.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes two PNGs (chart_1_imports_vietnam_vs_china.png,
chart_2_tariff_vietnam_vs_china.png) into the current folder, overwriting the
shipped copies. They should come out identical.

Data: US Census Bureau monthly imports (FT900 / USA Trade Online), all HS10
lines under HS 847130, general imports (customs value) and calculated duties.
See README.md.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

PRODUCT = "Laptops & Portable Computers (HS847130)"
SOURCES = ["VIETNAM", "CHINA"]          # legend order; first-listed line is drawn on top
COLORS = {
    "VIETNAM": "darkblue",              # both flags are red, so Vietnam is drawn dark blue
    "CHINA": "#DE2910",
}
X_START = pd.Timestamp("2023-01-01")
X_PAD_MONTHS = 6                        # runway after the last month
TARIFF_ERA = (pd.Timestamp("2025-01-01"), "2025 tariff era")
LW, ALPHA = 3.5, 0.9


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
def chart_imports(df, name):
    """Monthly import value from each source."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for e in SOURCES:
        s = df.loc[df["entity"] == e].set_index("month")["imports_usd"]
        ax.plot(s.index, s.values, color=COLORS[e], lw=LW, alpha=ALPHA, label=e.title())
    style(ax, s.index[-1], "dollars")
    finish(fig, ax, f"{PRODUCT} — Vietnam vs China", name)


def chart_tariff(df, name):
    """Effective tariff rate = calculated duties / customs value, by source.
    Lines are stacked so the first-listed country sits on top: where the two
    rates coincide (both zero before 2025) the lead line stays visible."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for i, e in enumerate(SOURCES):
        s = df.loc[df["entity"] == e].set_index("month")["tariff_rate_pct"]
        ax.plot(s.index, s.values, color=COLORS[e], lw=LW, alpha=ALPHA,
                label=e.title(), zorder=3 + len(SOURCES) - i)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))   # whole-number ticks
    style(ax, s.index[-1], "percent")
    finish(fig, ax, f"{PRODUCT} — effective tariff rate, Vietnam vs China", name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    chart_imports(df, "chart_1_imports_vietnam_vs_china.png")
    chart_tariff(df, "chart_2_tariff_vietnam_vs_china.png")


if __name__ == "__main__":
    main()
