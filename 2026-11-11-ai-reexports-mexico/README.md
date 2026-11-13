# US exports of AI-related products: re-exports, and Mexico, September 2026

Replication package for the two-post thread of **11 November 2026** (text and
links in `tweet.md`). Two charts were posted, one per post:

| File | Post | What it shows |
|---|---|---|
| `chart_1_domestic_vs_reexports.png` | 1 | US exports of AI-related products to all countries, split into goods made in the US and re-exports, monthly and as a 3-month average |
| `chart_2_reexports_by_destination.png` | 2 | The re-exports alone, split into those going to Mexico and those going to every other country combined, monthly and as a 3-month average |

This thread follows the one of 10 November
([`2026-11-10-mexico-border-crossings`](../2026-11-10-mexico-border-crossings/)),
which showed servers coming north over the Mexican border.

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

Long format, one row per chart, series and month, January 2022 to September
2026: 3,705 rows.

| Column | Meaning |
|---|---|
| `chart` | 1 or 2 |
| `series` | Chart 1: `ai_domestic`, `ai_reexports`, `all_goods_domestic`, `all_goods_reexports`, each for exports to all countries. Chart 2: a destination, named as Census names it (60 countries), or `TOTAL FOR ALL COUNTRIES` |
| `month` | Calendar month, `YYYY-MM` |
| `value` | Export value, US dollars. Chart 2 rows are re-exports of AI-related products only |

- Chart 1 draws `ai_domestic` and `ai_reexports`. The two `all_goods` series
  are there only for the "all US goods exports: 23%" comparison in the
  annotation.
- Chart 2 draws `MEXICO` and `TOTAL FOR ALL COUNTRIES` minus `MEXICO`. The
  other 59 countries are there for the "Next:" line in the annotation, which
  ranks destinations on January to September 2026. The 60 countries are the
  ones the underlying dataset tracks; they do not sum to the total (they carry
  $146.6B of the $148.0B for January to September 2026). The chart's "every
  other country" line uses the Census total, so it is complete.
- `TOTAL FOR ALL COUNTRIES` in chart 2 equals `ai_reexports` in chart 1 in
  every month.
- The bold lines are 3-month averages (the month and the two before it); the
  thin pale lines are the monthly values. The charts start in January 2023; the
  2022 rows are there so the averages and the year-earlier comparisons exist.

**Domestic exports and re-exports are Census's split.** Domestic exports are
goods grown, produced or manufactured in the US, including foreign goods that
were substantially transformed here. Re-exports (Census calls them foreign
exports) are goods of foreign origin that entered the US and left again in
substantially the same condition.

**"AI-related" is our classification, not a Census category.** It comes from
the paper [Trade in AI-Related Products](https://www.minneapolisfed.org/research/quarterly-review/trade-in-ai-related-products),
which tags every 10-digit code as High, Medium or Low relevance to AI data
center infrastructure. Exports use the combined import and export file,
[`hs10_classification_imports_exports.csv`](https://github.com/tradewartracker/ai-trade-index/blob/main/data-input/hs10_classification_imports_exports.csv),
matched on the 10-digit Schedule B code: `ai_*` is every High-relevance code
(819 after the exclusions below). The import side of the paper and of the
[10 November thread](../2026-11-10-mexico-border-crossings/) uses a separate
file for HTS codes, so import and export figures are not symmetric code for
code.

- HS chapters 27 (mineral fuels), 71 (precious metals and stones), 98 and 99
  (special provisions) are left out of the AI-related series and of the
  `all_goods` series alike. On all chapters the re-export share of US goods
  exports is lower, about 20%.
- Schedule B codes introduced in 2026 that are not in the classification file
  belong to no group: 48 codes, $8.7B or 0.6% of January to September 2026
  exports (after the chapter exclusions), mostly aluminium scrap, turbine parts
  and catalysts.

## Source and vintage

- **US Census Bureau**, monthly merchandise trade: exports by Schedule B
  (10-digit) code and country (`timeseries/intltrade/exports/hs`, the data
  behind the FT900 release and USA Trade Online), FAS value, with the
  domestic/foreign flag.
- **Vintage:** the September 2026 release (FT900 published 4 November 2026).
  The 2026 months were pulled on 2026-11-04; the 2022 to 2025 months were
  pulled on 2026-08-13 and carry the revisions published up to then. Census
  revises monthly data, so a fresh pull will not match this file exactly.
- Values are the Census domestic and foreign component rows for each line,
  which sum to its total row.

## How to read it, and what it cannot tell you

- **Chart 1, 3-month average to September 2026:** re-exports $16.90B a month
  (+38.5% on a year earlier, from $12.20B), made in the US $16.24B (+19.5%,
  from $13.59B). For September alone: $18.05B and $17.54B.
- **Re-exports passed US-made exports at the turn of the year:** in the
  monthly data first in December 2025, on the 3-month average in January 2026.
- **January to September 2026:** AI-related exports were $282.8B, of which
  $148.0B (52.4%) were re-exports. In the same months of 2025 they were $220.4B
  and 45.7%. Of the $62.4B rise, $47.4B is re-exports and $15.0B is goods made
  in the US. The re-export share by full year: 43.1% (2022), 41.3%, 41.9%,
  46.4% (2025).
- **The comparison with all goods:** 22.7% of US goods exports were re-exports
  in January to September 2026 ($303.6B of $1,335.8B, on the same chapter
  exclusions); by full year 17.7% (2022), 18.3%, 19.4%, 20.7% (2025). The
  all-goods series includes the AI-related products.
- **Chart 2, 3-month average to September 2026:** re-exports to Mexico $7.59B
  a month (+32.1% on a year earlier, from $5.75B), to every other country
  $9.31B (+44.2%, from $6.45B). For September alone: $7.45B and $10.60B.
- **"More than 50%" in post 2.** For January to September 2026 Mexico took
  $73.6B of the $148.0B, which is 49.7% (the chart's annotation rounds it to
  50%). Month by month the share was above half in January (58.2%), February
  (52.7%) and April (56.7%) and below it since, ending at 41.3% in September.
  By full year it was 40.6% (2022), 40.2%, 42.1%, 45.6% (2025). Re-exports to
  Mexico peaked at $10.55B in January 2026 and, on the 3-month average, at
  $8.85B in March.
- **The next destinations,** January to September 2026: Canada $10.6B, Taiwan
  $7.5B, the Netherlands $7.0B, Malaysia $5.0B, Singapore $3.9B.
- **What is in the Mexico line.** $60.3B of the $73.6B is computer hardware,
  led by four Schedule B lines: parts and accessories of computers
  (8473300002, $24.9B), servers (8471500150, $9.4B), solid-state storage
  (8523510000, $8.4B) and central processing units (8542310045, $6.5B).
  Counting US-made goods as well, the US shipped $96.1B of AI-related products
  to Mexico, 76.5% of it re-exports. (These figures come from the underlying
  Schedule B data; they cannot be recomputed from `data.csv`.)
- **A re-export is a customs classification, not a measure of value added.**
  It says the good was foreign-made and left in substantially the same
  condition. It does not say how long the good stayed, what was done to it
  short of substantial transformation, or what it was sold for on the way in:
  export value (FAS) and import value (customs) are measured differently, and
  an export record is not matched to the import that preceded it.
- **The charts show where re-exports go, not what happens next.** That the
  goods sent to Mexico are assembled into servers that return to the US is the
  reading of the 10 November thread; nothing in this file traces a component
  into a server.
- **A category is a tag on a product, not a record of where it went.** A chip,
  a board or a transformer is counted as AI-related because that kind of
  product is used in data centers. The data cannot say whether a given
  shipment was bound for one.
- Nothing is seasonally adjusted. The y-axes do not start at zero. The dashed
  rule at January 2025 marks the start of the 2025 tariff era, for orientation
  only.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
