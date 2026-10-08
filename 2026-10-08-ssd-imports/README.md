# US imports of solid-state storage (HS 852351), August 2026

Replication package for the two-post thread of **8 October 2026** (text and
links in `tweet.md`). Three charts were posted, two in the first post and one
in the reply:

| File | Post | What it shows |
|---|---|---|
| `chart_1_total_value.png` | 1 | Total US imports of HS 852351, monthly, customs value |
| `chart_2_total_volume.png` | 1 | The same imports by volume (Census quantity, number of units) |
| `chart_3_unit_value_by_source.png` | 2 | Unit value (value ÷ quantity) for the four largest source countries |

## Reproduce

```
pip install pandas matplotlib
python make_charts.py
```

`make_charts.py` reads `data.csv` and rewrites the three PNGs. On the machine
that produced the tweet (matplotlib 3.10.6, pandas 2.3.3) the output is
byte-identical to the shipped files. Other versions may differ in font
rendering, not in the data.

## Data (`data.csv`)

One row per country-month, January 2023 to August 2026.

| Column | Meaning |
|---|---|
| `entity` | `TOTAL FOR ALL COUNTRIES` (Census's published total) or the source country |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | General imports, customs value, US dollars |
| `quantity` | Census first quantity, summed over the HS10 lines |
| `unit` | Census unit of quantity (`NO` = number of units) |
| `unit_value_usd` | `imports_usd / quantity` |

The four sources (South Korea, Taiwan, Vietnam, Malaysia) are the four largest
by August 2026 value. The total is Census's own all-countries figure, not a
sum of the countries shown.

## Source and vintage

- **US Census Bureau**, monthly merchandise trade by HTS10 and country
  (the data behind the FT900 release and USA Trade Online), general imports.
- **Vintage:** the August 2026 release (FT900 published 6 October 2026),
  pulled on 2026-10-06. Earlier months carry the revisions published through
  that release. Census revises monthly data, so a fresh pull will not match
  this file exactly.
- **Product:** every HTS10 line whose first six digits are 852351
  (solid-state non-volatile storage devices). Values are the Census total row
  for each line, not the sum of rate-provision components.

## How to read it, and what it cannot tell you

- **Unit value is an average transaction value, not a price index.** It is
  total dollars divided by total units. It moves when prices change and also
  when the mix of goods changes. A $90 consumer drive and a $1,200 enterprise
  drive are both one unit.
- **The spread between sources is the point of chart 3.** Taiwan ships tens of
  millions of low-value consumer drives; South Korea and Vietnam ship a tenth
  of the units at over $1,000 each. The aggregate unit value in chart 1 ÷
  chart 2 rises on this mix shift as well as on any within-source price change.
- Headline figures for August 2026: value $8.2B (+591.8% YoY), volume 30.8M
  units (+64.4% YoY), unit value $265 per unit (+320.9% YoY). All three are
  computed in `make_charts.py` from the CSV.
- Charts start in 2023 and carry a dashed rule at January 2025, the start of
  the 2025 tariff era, for orientation only. The effective tariff on these
  goods never exceeded 0.5% in this window.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
