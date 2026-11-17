"""Replicate the two charts in the 16 Nov 2026 thread on US imports of servers
(HS 847150): value, units and unit value from all sources as an index, and the
unit value by source, both as 3-month averages.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes two PNGs (chart_1_value_units_unit_value.png,
chart_2_unit_value_by_source.png) into the current folder, overwriting the
shipped copies. They should come out identical.

Data: US Census Bureau monthly imports (FT900 / USA Trade Online), HTS10 lines
under 8471.50, customs value and first quantity (number of units).
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

X_START = pd.Timestamp("2023-01-01")
X_PAD_MONTHS = 6                            # runway after the last month so the end labels fit
TARIFF_ERA = (pd.Timestamp("2025-01-01"), "2025 tariff era")
LW, ALPHA = 3.5, 0.9
FOOT = "tradewartracker.com  ·  Source: US Census Bureau"

ALL = "All sources"
BLUE, RED, GREEN = "darkblue", "#8B0000", "darkgreen"
# black for the total, flag colours for the three sources
SOURCES = [(ALL, "black"), ("Mexico", "#006847"), ("Taiwan", "#000095"), ("Thailand", "#2D2A4A")]


# ----------------------------------------------------------------------------- #
# number helpers
# ----------------------------------------------------------------------------- #
def dollars(x):
    """$33.8B, $759.3M, ..."""
    sign = "-" if x < 0 else ""
    x = abs(x)
    for div, suf in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if x >= div:
            return f"{sign}${x / div:.1f}{suf}"
    return f"{sign}${x:,.0f}"


def yoy(s, latest):
    """Latest value vs the same month a year earlier, in percent."""
    prior, now = s.get(latest - pd.DateOffset(months=12)), s.get(latest)
    return (now / prior - 1) * 100 if prior and now and prior > 0 else np.nan


def smooth(value, units):
    """3-month averages of value and of units, and their ratio. The unit value
    is the ratio of the two averages, not the average of three monthly unit
    values, so a big month counts for what it is worth."""
    v, q = value.rolling(3).mean(), units.rolling(3).mean()
    return v, q, v / q


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
    ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))


def end_label(ax, x, y, color, text, fontsize=11, dy=0.0):
    """Bold, colour-matched label at the end of a line; dy nudges it (points)."""
    ax.annotate(text, xy=(x, y), xytext=(8, dy), textcoords="offset points",
                fontsize=fontsize, fontweight="bold", color=color, alpha=1.0,
                va="center", zorder=5)


def label_dys(ax, ends, fontsize=9, nlines=2, pad=3):
    """Vertical nudges (points) so two-line end labels neither overprint each
    other nor run below the x-axis. Works in points, after the limits and the
    layout are set, so the gap is the same whatever the y scale. Labels are
    stacked from the bottom up."""
    fig = ax.figure
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    k = 72 / fig.dpi
    h = nlines * fontsize * 1.25 + pad
    ys = [ax.transData.transform((0, y))[1] * k for y in ends]
    floor = ax.transAxes.transform((0, 0))[1] * k + h / 2
    placed, prev = {}, None
    for i in sorted(range(len(ys)), key=lambda i: ys[i]):
        y = max(ys[i], floor) if prev is None else max(ys[i], floor, prev + h)
        placed[i] = prev = y
    return [placed[i] - ys[i] for i in range(len(ys))]


def finish(fig, ax, name):
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    fig.text(0.99, 0.01, FOOT, ha="right", va="bottom", fontsize=7, color="#999999")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(name, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", name)


# ----------------------------------------------------------------------------- #
# charts
# ----------------------------------------------------------------------------- #
def chart_1(value, units, latest, name):
    """All sources: value, units and unit value, 3-month averages, each as an
    index on its own 2023 average. The end labels carry the actual levels and
    their change on a year earlier."""
    v, q, uv = smooth(value[ALL], units[ALL])
    m = pd.DataFrame({"value": v, "units": q, "unit_value": uv})
    idx = 100 * m / m.loc["2023"].mean()
    lines = [("value", "Value ($)", BLUE, lambda x: dollars(x)),
             ("units", "Units (number)", RED, lambda x: f"{x / 1e6:,.1f}M units"),
             ("unit_value", "Unit value ($ per unit)", GREEN, lambda x: f"${x:,.0f} per unit")]
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.axhline(100, color="#999999", lw=0.8, ls=":", zorder=0)
    for col, label, color, _ in lines:
        ax.plot(idx.index, idx[col].values, color=color, lw=LW, alpha=ALPHA, label=label)
    style(ax, latest)
    ax.set_ylim(top=idx.max().max() * 1.12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:,.0f}"))
    ax.set_ylabel("Index, 2023 average = 100", fontsize=9)
    ax.set_title("Servers (HS847150), all sources — value, units and unit value (3-mo averages)",
                 fontsize=12, fontweight="bold", loc="left")
    ends = [idx[c].loc[latest] for c, _, _, _ in lines]
    for (col, label, color, fmt), dy in zip(lines, label_dys(ax, ends)):
        gr = yoy(m[col], latest)
        end_label(ax, latest, idx[col].loc[latest], color,
                  fmt(m[col].loc[latest]) + (f"\n{gr:+.1f}% YoY" if np.isfinite(gr) else ""),
                  fontsize=9, dy=dy)
    finish(fig, ax, name)


def chart_2(value, units, latest, name):
    """Unit value (3-month value / 3-month units) from all sources and from
    the three largest source countries, in dollars per unit."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    data = {e: smooth(value[e], units[e])[2] for e, _ in SOURCES}
    top = max(s.max() for s in data.values())
    for e, color in SOURCES:
        ax.plot(data[e].index, data[e].values, color=color, lw=LW, alpha=ALPHA, label=e)
    style(ax, latest)
    ax.set_ylim(bottom=0, top=top * 1.08)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    ax.set_ylabel("$ per unit", fontsize=9)
    ax.set_title("Servers (HS847150) — unit value by source, $ per unit (3-mo averages)",
                 fontsize=12, fontweight="bold", loc="left")
    ends = [data[e].loc[latest] for e, _ in SOURCES]
    for (e, color), dy in zip(SOURCES, label_dys(ax, ends)):
        s = data[e]
        gr = yoy(s, latest)
        end_label(ax, latest, s.loc[latest], color,
                  f"${s.loc[latest]:,.0f}" + (f"\n{gr:+.1f}% YoY" if np.isfinite(gr) else ""),
                  fontsize=9, dy=dy)
    finish(fig, ax, name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    latest = df["month"].max()
    value = df.pivot(index="month", columns="source", values="imports_usd").sort_index().astype(float)
    units = df.pivot(index="month", columns="source", values="units").sort_index().astype(float)

    chart_1(value, units, latest, "chart_1_value_units_unit_value.png")
    chart_2(value, units, latest, "chart_2_unit_value_by_source.png")


if __name__ == "__main__":
    main()
