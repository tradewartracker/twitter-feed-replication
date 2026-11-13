"""Replicate the three charts in the 10 Nov 2026 thread on servers crossing the
Mexican border: the share of all US server imports that enter over the border and
the value by crossing, the monthly flow through the four big crossings, and the
value / units / unit value of servers from Mexico as an index.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes three PNGs (chart_1_border_crossings.png,
chart_2_servers_by_crossing.png, chart_3_value_units_unit_value.png) into the
current folder, overwriting the shipped copies. They should come out identical.

Data: US Census Bureau. Charts 1 and 2 use the port-of-entry series (general
imports, HS6 847150); chart 3 uses the country series (imports for consumption,
customs value and number of units, HTS10 lines under 847150, summed). See README.md.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

LATEST = pd.Timestamp("2026-09-01")
X_START = pd.Timestamp("2023-01-01")
X_PAD_MONTHS = 6                        # runway after the last month so the end labels fit
TARIFF_ERA = (pd.Timestamp("2025-01-01"), "2025 tariff era")
LW, ALPHA = 3.5, 0.9
MX_GREEN = "#006847"                    # Mexico's colour on tradewartracker.com
BLUE, RED, GREEN, GOLD = "darkblue", "#8B0000", "darkgreen", "#DAA520"
FOOT = "tradewartracker.com  ·  Source: US Census Bureau"
CROSSING_LABEL = {"YSLETA, TX": "Ysleta, TX  (Juárez)", "LAREDO, TX": "Laredo, TX  (Nuevo Laredo)",
                  "SANTA TERESA, NM": "Santa Teresa, NM  (Juárez)", "FABENS, TX": "Fabens, TX  (Juárez)",
                  "EL PASO, TX": "El Paso, TX  (Bridge of the Americas)"}


# ----------------------------------------------------------------------------- #
# number formatting
# ----------------------------------------------------------------------------- #
def fmt_dollars(x):
    sign = "-" if x < 0 else ""
    x = abs(x)
    for div, suf in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if x >= div:
            return f"{sign}${x / div:.1f}{suf}"
    return f"{sign}${x:,.0f}"


def fmt_pct(x):
    return f"{x:+.1f}%"


def esc(s):
    """Two '$' in one string switch matplotlib into mathtext; escape them."""
    return s.replace("$", r"\$")


def yoy(s, t=LATEST):
    """Latest value vs the same month a year earlier, in percent."""
    prior, now = s.get(t - pd.DateOffset(months=12)), s.get(t)
    return (now / prior - 1) * 100 if prior and now and prior > 0 else np.nan


def spread(ends, span, gap=0.075):
    """Vertical nudges (points) for end labels whose y values sit within `gap` of the
    axis span of each other, so two-line labels do not overprint."""
    order = sorted(range(len(ends)), key=lambda i: ends[i])
    dy = [0.0] * len(ends)
    for a, b in zip(order, order[1:]):
        if ends[b] - ends[a] < gap * span:
            dy[a] -= 11
            dy[b] += 11
    return dy


# ----------------------------------------------------------------------------- #
# the house style (tradewartracker.com charts)
# ----------------------------------------------------------------------------- #
def end_label(ax, x, y, color, text, fontsize=11, dy=0.0):
    """Bold, colour-matched value label at the end of a line; dy nudges it (points)."""
    if y is None or (isinstance(y, float) and np.isnan(y)):
        return
    ax.annotate(text, xy=(x, y), xytext=(8, dy), textcoords="offset points",
                fontsize=fontsize, fontweight="bold", color=color, alpha=1.0,
                va="center", zorder=5)


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


def bar_axes(ax):
    ax.set_facecolor("#ffffff")
    ax.figure.set_facecolor("#ffffff")
    ax.grid(True, axis="x", alpha=0.3, linewidth=0.6)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: fmt_dollars(x)))


def finish(fig, ax, title, name):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    fig.text(0.99, 0.01, FOOT, ha="right", va="bottom", fontsize=7, color="#999999")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(name, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", name)


# ----------------------------------------------------------------------------- #
# charts
# ----------------------------------------------------------------------------- #
def chart_1(c1, name):
    """A strip with the Mexican crossings' share of ALL US server imports, then one
    bar per crossing (the five that matter; the rest of the land border carries
    about $36M and gets no row)."""
    s = c1.groupby("series")["value"].sum().sort_values(ascending=False)
    crossings = set(c1.loc[c1["kind"] == "Mexican border crossing", "series"])
    total = s.sum()
    land = s[s.index.isin(crossings)]
    bars = land.head(5)
    share = 100 * land.sum() / total

    fig = plt.figure(figsize=(9, 5.2), dpi=150)
    fig.set_facecolor("#ffffff")
    ax0 = fig.add_axes([0.03, 0.75, 0.94, 0.14])       # the strip spans the figure
    ax1 = fig.add_axes([0.30, 0.09, 0.67, 0.56])       # the bars leave room for crossing names
    fig.text(0.03, 0.945, "Servers (HS847150) — nearly half of US imports cross the Mexican border",
             fontsize=12, fontweight="bold", ha="left", va="center")
    fig.text(0.03, 0.675, "Servers entering over the Mexican border, by crossing, Jan–Sep 2026",
             fontsize=9, color="#333333", ha="left", va="center")

    ax0.barh(0, share, color=MX_GREEN, height=0.7)
    ax0.barh(0, 100 - share, left=share, color="#D9D9D9", height=0.7)
    ax0.text(share / 2, 0, esc(f"Mexican border crossings  {share:.0f}%  ({fmt_dollars(land.sum())})"),
             ha="center", va="center", fontsize=9, fontweight="bold", color="white")
    ax0.text(share + (100 - share) / 2, 0, esc(f"All other US ports  {100 - share:.0f}%  ({fmt_dollars(total - land.sum())})"),
             ha="center", va="center", fontsize=9, fontweight="bold", color="#333333")
    ax0.text(0, 0.55, esc(f"Share of all US server imports, Jan–Sep 2026 ({fmt_dollars(total)})"),
             ha="left", va="bottom", fontsize=8, color="#555555")
    ax0.set_xlim(0, 100)
    ax0.set_ylim(-0.5, 1.05)
    ax0.set_axis_off()

    y = np.arange(len(bars))[::-1]
    ax1.barh(y, bars.values, color=MX_GREEN, height=0.65, alpha=0.9)
    for yi, v in zip(y, bars.values):
        ax1.text(v + bars.max() * 0.012, yi, fmt_dollars(v), va="center", ha="left", fontsize=9, fontweight="bold")
    ax1.set_yticks(y)
    ax1.set_yticklabels([CROSSING_LABEL.get(p, p) for p in bars.index], fontsize=9)
    bar_axes(ax1)
    ax1.set_xlim(0, bars.max() * 1.14)
    fig.text(0.99, 0.01, FOOT, ha="right", va="bottom", fontsize=7, color="#999999")
    fig.savefig(name, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", name)


def chart_2(c2, name):
    """Servers from Mexico by port of entry, monthly, four crossings."""
    lines = [("YSLETA, TX", "Ysleta, TX", BLUE), ("LAREDO, TX", "Laredo, TX", RED),
             ("SANTA TERESA, NM", "Santa Teresa, NM", GREEN), ("FABENS, TX", "Fabens, TX", GOLD)]
    m = c2.pivot(index="month", columns="series", values="value").sort_index()
    m = m.reindex(pd.date_range(m.index.min(), LATEST, freq="MS")).fillna(0)[[p for p, _, _ in lines]].astype(float)
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ends = [m[p].loc[LATEST] for p, _, _ in lines]
    dys = spread(ends, m.max().max())
    for (p, label, color), dy in zip(lines, dys):
        s = m[p]
        ax.plot(s.index, s.values, color=color, lw=LW, alpha=ALPHA, label=label)
        g = yoy(s)
        # Fabens carried almost nothing a year earlier, so its YoY is a base effect and is left off
        text = fmt_dollars(s.loc[LATEST]) + (f"\n{fmt_pct(g)} YoY" if p != "FABENS, TX" and np.isfinite(g) else "")
        end_label(ax, LATEST, s.loc[LATEST], color, text, fontsize=9, dy=dy)
    style(ax, LATEST, "dollars")
    finish(fig, ax, "Servers from Mexico by port of entry (HS847150) — monthly, Jan 2023 → Sep 2026", name)


def chart_3(c3, name):
    """Value, units and unit value of servers from Mexico, monthly, each as an index
    on its own 2023 monthly average. The end labels carry the actual levels."""
    m = c3.set_index("month").sort_index()[["value", "units"]].astype(float)
    m = m.reindex(pd.date_range(m.index.min(), LATEST, freq="MS"))
    m["unit_value"] = m["value"] / m["units"]
    idx = 100 * m / m.loc["2023"].mean()
    lines = [("value", "Value ($)", BLUE, lambda v: fmt_dollars(v)),
             ("units", "Units shipped (number)", RED, lambda v: f"{v / 1e3:,.0f}K units"),
             ("unit_value", "Unit value ($ per unit)", GREEN, lambda v: f"${v:,.0f} per unit")]
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.axhline(100, color="#999999", lw=0.8, ls=":", zorder=0)
    ends = [idx[c].loc[LATEST] for c, _, _, _ in lines]
    dys = spread(ends, idx.loc["2023":].max().max())
    for (col, label, color, fmt), dy in zip(lines, dys):
        s = idx[col]
        ax.plot(s.index, s.values, color=color, lw=LW, alpha=ALPHA, label=label)
        g = yoy(m[col])
        text = fmt(m[col].loc[LATEST]) + (f"\n{fmt_pct(g)} YoY" if np.isfinite(g) else "")
        end_label(ax, LATEST, s.loc[LATEST], color, text, fontsize=9, dy=dy)
    style(ax, LATEST, None)
    ax.set_ylim(top=idx.loc["2023":].max().max() * 1.12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:,.0f}"))
    ax.set_ylabel("Index, 2023 average = 100", fontsize=9)
    finish(fig, ax, "Servers from Mexico (HS847150) — dollars up, units down (monthly)", name)


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip", keep_default_na=False,
                     na_values={"units": [""]}, dtype={"kind": str})
    df["month"] = pd.to_datetime(df["month"])
    chart_1(df[df["chart"] == 1], "chart_1_border_crossings.png")
    chart_2(df[df["chart"] == 2], "chart_2_servers_by_crossing.png")
    chart_3(df[df["chart"] == 3], "chart_3_value_units_unit_value.png")


if __name__ == "__main__":
    main()
