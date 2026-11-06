"""Replicate the four charts in the 6 Nov 2026 thread on the AI trade index:
AI-related vs non-AI imports (index), electrical power and cooling vs non-AI
(index, 3-month average), the effective tariff rate by AI category, and each
category's share of AI-related imports against its share of the tariffs paid.

Requires only pandas and matplotlib. Run from this folder:

    python make_charts.py

It reads data.csv and writes four PNGs (chart_1_ai_vs_nonai_index.png,
chart_2_power_cooling_index.png, chart_3_tariff_by_category.png,
chart_4_imports_vs_duties.png) into the current folder, overwriting the shipped
copies. They should come out identical.

Data: US Census Bureau monthly imports (FT900 / USA Trade Online), all
countries, at HTS10, summed into the AI-relevance groups described in
README.md (value = customs value, duties = calculated duties).
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

X_START = pd.Timestamp("2023-01-01")
X_START_3MO = pd.Timestamp("2023-03-01")    # first month a 3-month average exists
X_PAD_MONTHS = 6                # runway after the last month so the end labels fit
TARIFF_ERA = (pd.Timestamp("2025-01-01"), "2025 tariff era")
LW, ALPHA = 4.0, 0.85

AI, NONAI = "AI-related", "Non-AI"
CATEGORIES = ["Compute Hardware", "Networking & Telecom", "Electrical Power", "Cooling & HVAC",
              "Building & Structure", "Fire Safety & Security", "Specialty Materials"]
# AI-related / non-AI follow the house palette (dark blue primary, dark red
# contrast); the category colours are the ones tradewartracker.com uses
COLOR = {AI: "darkblue", NONAI: "#8B0000", "Compute Hardware": "#2ca02c",
         "Networking & Telecom": "#9467bd", "Electrical Power": "#ff7f0e", "Cooling & HVAC": "#8c564b"}


# ----------------------------------------------------------------------------- #
# number formatting
# ----------------------------------------------------------------------------- #
def yoy_pct(s, latest):
    """Latest value vs the same month a year earlier, in percent."""
    prior = s.get(latest - pd.DateOffset(months=12))
    return (float(s.iloc[-1]) / prior - 1) * 100


# ----------------------------------------------------------------------------- #
# the house style (tradewartracker.com charts)
# ----------------------------------------------------------------------------- #
def style(ax, latest, value_kind, x_start=X_START):
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
    if value_kind == "percent":
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"{x:.0f}%"))


def end_label(ax, x, y, color, text, fontsize=11, dy=0.0):
    """Bold, colour-matched label at the end of a line; dy nudges it (points)."""
    ax.annotate(text, xy=(x, y), xytext=(8, dy), textcoords="offset points",
                fontsize=fontsize, fontweight="bold", color=color, alpha=1.0,
                va="center", zorder=5)


def end_labels(ax, latest, items, fontsize=9):
    """End-of-line labels for several lines, nudged apart where they would
    overprint. items = [(y, color, text)]; call once the axis limits are final."""
    x = mdates.date2num(latest)
    to_pt = 72.0 / ax.figure.dpi
    rows = sorted(([ax.transData.transform((x, y))[1] * to_pt, y, c, t] for y, c, t in items),
                  key=lambda r: r[0])
    pos = [r[0] for r in rows]
    half = [0.62 * fontsize * (r[3].count("\n") + 1) for r in rows]   # half-height of each label, points
    for _ in range(50):
        for i in range(1, len(pos)):
            short = (half[i] + half[i - 1] + 1.5) - (pos[i] - pos[i - 1])
            if short > 0:
                pos[i - 1] -= short / 2
                pos[i] += short / 2
    for (p0, y, c, t), p in zip(rows, pos):
        end_label(ax, latest, y, c, t, fontsize=fontsize, dy=p - p0)


def finish(fig, ax, title, name, legend_loc="upper left"):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left")
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
def chart_ai_vs_nonai(idx, latest, name):
    """Import index (2023 monthly average = 100) for AI-related and non-AI
    products, latest value + YoY as end labels."""
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.axhline(100, color="#999999", lw=0.8, ls="--", zorder=0)
    for g in (AI, NONAI):
        ax.plot(idx.index, idx[g].values, color=COLOR[g], lw=LW, alpha=ALPHA, label=f"{g} products")
    style(ax, latest, "index")
    ax.set_ylabel("Index (2023 monthly average = 100)", fontsize=9)
    end_labels(ax, latest, [(float(idx[g].iloc[-1]), COLOR[g],
                             f"{idx[g].iloc[-1]:.0f}\n{yoy_pct(idx[g], latest):+.1f}% YoY") for g in (AI, NONAI)])
    finish(fig, ax, "US imports — AI-related vs non-AI products (index, 2023 = 100)", name)


def chart_power_cooling(idx, latest, name):
    """The same index for Electrical Power, Cooling & HVAC and non-AI products,
    as a 3-month moving average. The whole series is plotted and the x-axis
    starts at the average's first month (March 2023)."""
    trio = ["Electrical Power", "Cooling & HVAC", NONAI]
    names = {"Electrical Power": "AI-related Electrical Power",
             "Cooling & HVAC": "AI-related Cooling & HVAC", NONAI: "Non-AI products"}
    ma = idx[trio].rolling(3).mean()
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.axhline(100, color="#999999", lw=0.8, ls="--", zorder=0)
    for g in trio:
        ax.plot(ma.index, ma[g].values, color=COLOR[g], lw=LW, alpha=ALPHA, label=names[g])
    style(ax, latest, "index", x_start=X_START_3MO)
    ax.set_ylabel("Index (2023 monthly average = 100)", fontsize=9)
    end_labels(ax, latest, [(float(ma[g].iloc[-1]), COLOR[g],
                             f"{ma[g].iloc[-1]:.0f}\n{yoy_pct(ma[g], latest):+.1f}% YoY") for g in trio])
    finish(fig, ax, "US imports — electrical power & cooling vs non-AI (index, 3-month average)", name)


def chart_tariff(rate, latest, name):
    """Effective tariff rate (calculated duties / customs value) on four AI
    categories and on non-AI products."""
    five = ["Compute Hardware", "Networking & Telecom", "Electrical Power", "Cooling & HVAC", NONAI]
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    for g in five:
        ax.plot(rate.index, rate[g].values, color=COLOR[g], lw=LW, alpha=ALPHA,
                label=g if g != NONAI else "Non-AI products")
    style(ax, latest, "percent")
    end_labels(ax, latest, [(float(rate[g].iloc[-1]), COLOR[g], f"{rate[g].iloc[-1]:.1f}%") for g in five])
    finish(fig, ax, "US imports — effective tariff rate by AI category (duties ÷ value)", name)


def chart_shares(imp, dut, latest, name):
    """Each category's share of AI-related imports next to its share of the
    duties paid on AI-related imports, over the latest 12 months. The five
    largest categories by imports are drawn; shares are of all seven."""
    i12, d12 = imp[CATEGORIES].iloc[-12:].sum(), dut[CATEGORIES].iloc[-12:].sum()
    sh = pd.DataFrame({"imports_usd": i12, "share_imports_pct": 100 * i12 / i12.sum(),
                       "share_duties_pct": 100 * d12 / d12.sum()})
    bars = sh.sort_values("imports_usd", ascending=False).head(5)
    first12 = imp.index[-12]

    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=150)
    ax.set_facecolor("#ffffff")
    fig.set_facecolor("#ffffff")
    xs = range(len(bars))
    w = 0.36
    for off, key, color, label in ((-w / 2, "share_imports_pct", "darkblue", "Share of AI-related imports"),
                                   (w / 2, "share_duties_pct", "#8B0000", "Share of tariffs paid on them")):
        b = ax.bar([x + off for x in xs], bars[key].values, w, color=color, alpha=ALPHA,
                   edgecolor="black", linewidth=1.0, label=label)
        for rect, v in zip(b, bars[key].values):
            ax.text(rect.get_x() + rect.get_width() / 2, v + 1.0, f"{v:.0f}%", ha="center", va="bottom",
                    fontsize=10, fontweight="bold", color=color)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([n.replace(" & ", " &\n").replace("Compute H", "Compute\nH").replace("Electrical P", "Electrical\nP")
                        for n in bars.index], fontsize=9, fontweight="bold")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{v:.0f}%"))
    ax.set_ylim(0, max(bars["share_imports_pct"].max(), bars["share_duties_pct"].max()) * 1.15)
    ax.grid(True, axis="y", alpha=0.3, linewidth=0.6)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.set_xlabel(f"{first12:%B %Y} – {latest:%B %Y}", fontsize=9)
    finish(fig, ax, "AI-related US imports by category — share of imports vs share of tariffs paid", name,
           legend_loc="upper right")


def main():
    df = pd.read_csv("data.csv", float_precision="round_trip")
    df["month"] = pd.to_datetime(df["month"])
    latest = df["month"].max()

    def wide(classification, column):
        d = df[df["classification"] == classification]
        return d.pivot(index="month", columns="group", values=column).sort_index()

    # charts 1, 3 and 4 use the classification as published; chart 2 uses the
    # version in which HTS10 codes created in 2026 inherit a tag (see README.md)
    chart_ai_vs_nonai(wide("published", "index_2023_100"), latest, "chart_1_ai_vs_nonai_index.png")
    chart_power_cooling(wide("new_codes", "index_2023_100"), latest, "chart_2_power_cooling_index.png")
    chart_tariff(wide("published", "tariff_rate_pct"), latest, "chart_3_tariff_by_category.png")
    chart_shares(wide("published", "imports_usd"), wide("published", "duties_usd"), latest,
                 "chart_4_imports_vs_duties.png")


if __name__ == "__main__":
    main()
