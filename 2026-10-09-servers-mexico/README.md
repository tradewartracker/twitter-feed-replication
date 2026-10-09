# US imports of servers (HS 847150), August 2026

Replication package for the two-post thread of **9 October 2026** (text and
links in `tweet.md`). One chart per post:

| File | Post | What it shows |
|---|---|---|
| `chart_1_all_sources_vs_top_suppliers.png` | 1 | Total US imports of HS 847150 (black) and the three largest source countries, monthly, customs value |
| `chart_2_mexico_servers_vs_vehicles.png` | 2 | US imports from Mexico: the single HS6 line 847150 against the whole vehicle chapter (every HTS10 line beginning 87) |

## Reproduce

```
pip install pandas matplotlib
python make_charts.py
```

`make_charts.py` reads `data.csv` and rewrites the two PNGs. On the machine
that produced the thread (matplotlib 3.10.6, pandas 2.3.3) the output is
byte-identical to the shipped files. Other versions may differ in font
rendering, not in the data.

## Data (`data.csv`)

One row per series-month, January 2023 to August 2026, in long format.

| Column | Meaning |
|---|---|
| `chart` | `1` or `2`, which chart the row feeds |
| `entity` | `TOTAL FOR ALL COUNTRIES` (Census's published total) or the source country |
| `product` | `HS847150` (all HTS10 lines beginning 847150) or `HS87` (all HTS10 lines beginning 87) |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | General imports, customs value, US dollars |

Chart 1 draws Mexico, Taiwan and Thailand, the three largest sources by
August 2026 value. The total is Census's own all-countries figure, not a sum
of the countries shown. Vietnam, the fourth-largest source at $0.3B, was left
off because it sat flat on the zero axis. China is not drawn because it has
no footprint in this product: $20M to $55M a month across the whole window,
about 0.1% of US imports of the line.

The Mexico HS847150 series appears in both charts and is the same numbers.

## Source and vintage

- **US Census Bureau**, monthly merchandise trade by HTS10 and country
  (the data behind the FT900 release and USA Trade Online), general imports.
- **Vintage:** the August 2026 release (FT900 published 6 October 2026),
  pulled on 2026-10-06. Earlier months carry the revisions published through
  that release. Census revises monthly data, so a fresh pull will not match
  this file exactly.
- **Product:** HS 847150 is "digital processing units other than those of
  8471.41 or 8471.49", i.e. a computer's processing unit sold without being a
  complete system. In practice this is where servers, GPU boxes and rack
  compute land. Effectively all of the value is in one HTS10 line,
  8471.50.0150. Values are the Census total row for each line, not the sum of
  rate-provision components.

## How to read it, and what it cannot tell you

- Headline figures for August 2026 (chart 1): total US imports $29.8B,
  +70.4% YoY; Mexico $18.8B (+142.0%), Taiwan $7.4B (-12.9%), Thailand $1.8B
  (+246.4%). Mexico alone is 63% of the total.
- The "about 10% of US imports" in post 1: $29.8B against total US goods
  imports of $330.7B in August 2026 is 9.0%; against imports excluding
  mineral fuels (HS 27, $20.7B) it is 9.6%. Those denominators are not in
  `data.csv`; they are Census's published totals for the month.
- Chart 2's end labels: Mexico servers $18.8B (+142.0% YoY), Mexico vehicles
  and parts $10.8B (+3.5% YoY). Servers first exceeded vehicles in January
  2026, fell back below for February and March, and have been ahead every
  month since April 2026. Both YoY labels are computed in `make_charts.py`
  from the CSV.
- Chart 2 compares one HS6 line with an entire HS2 chapter on purpose. The
  vehicle chapter has run between $7.6B and $12.3B a month since 2023, with
  no trend; it did not fall. The change is the server line growing nine-fold on top of a flat
  vehicle trade, not a rotation out of vehicles.
- Customs value is the price at the border, so a server assembled in Mexico
  from imported chips is counted at its full value when it enters the US. The
  supply-chain description in post 2 (chips in, chips re-exported to Mexico,
  racks back) is not something these two series show on their own.
- Charts start in 2023 and carry a dashed rule at January 2025, the start of
  the 2025 tariff era, for orientation only. The effective tariff on HS
  847150 was 0.1% in August 2026.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
