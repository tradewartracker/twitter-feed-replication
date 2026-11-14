# US exports of AI-related products through El Paso, September 2026

Replication package for the two-post thread of **13 November 2026** (text and
links in `tweet.md`). Two charts were posted, one per post:

| File | Post | What it shows |
|---|---|---|
| `chart_1_el_paso_vs_rest_index.png` | 1 | US exports of AI-related products by the customs district they left through: the El Paso district, the other Texas districts, and every district outside Texas, each as an index (2023 = 100), 3-month average |
| `chart_2_el_paso_share.png` | 2 | The El Paso district's share of US exports of AI-related products next to its share of US exports of non-AI products, by year |

This thread follows the ones of 10 November
([`2026-11-10-mexico-border-crossings`](../2026-11-10-mexico-border-crossings/)),
which showed servers coming north over the Mexican border, and 11 November
([`2026-11-11-ai-reexports-mexico`](../2026-11-11-ai-reexports-mexico/)),
which showed that most US exports of AI-related products are re-exports and
that half of those go to Mexico.

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

Long format, one row per chart, series and month, January 2023 to September
2026: 315 rows.

| Column | Meaning |
|---|---|
| `chart` | 1 or 2 |
| `series` | Chart 1: `ai_el_paso`, `ai_other_texas`, `ai_outside_texas`. Chart 2: `ai_el_paso`, `ai_us`, `nonai_el_paso`, `nonai_us` |
| `month` | Calendar month, `YYYY-MM` |
| `value` | Export value to all destinations, US dollars |

- `ai_*` is exports of AI-related products, `nonai_*` exports of non-AI
  products. `_us` is the national total; `_el_paso`, `_other_texas` and
  `_outside_texas` are the exports that left through those customs districts.
- The three chart 1 series add up to `ai_us` in every month. `ai_el_paso` is
  the same series in both charts.
- **Chart 1** divides each series by its own 2023 monthly average (times 100)
  and then takes a 3-month average (the month and the two before it). The
  x-axis starts in March 2023, the first month that average exists.
- **Chart 2** sums each series over the calendar year and divides El Paso by
  the US total. The 2026 bars are January to September.

**A customs district is Census's grouping of ports, and the district of export
is where the goods left the country.** For a truck that is the border
crossing. It is not where the goods were made, where they were stored or where
the exporter is. The groups in chart 1:

- **El Paso district:** the El Paso, Ysleta, Fabens and Presidio crossings in
  Texas, and Santa Teresa, Columbus and Albuquerque in New Mexico. The post
  calls it the "El Paso, TX corridor"; the district does not stop at the state
  line. Santa Teresa NM is the largest single exit port for the computer parts
  (HS 847330, 38.5%) and processors (HS 854231, 43.2%) the US shipped to
  Mexico in January to September 2026, ahead of Ysleta TX (30.4% and 31.4%).
- **The other Texas districts:** Laredo (which also covers Hidalgo,
  Brownsville, Eagle Pass, Del Rio, Roma, Progreso and Rio Grande City),
  Houston-Galveston, Dallas-Fort Worth (which also covers Oklahoma City and
  Tulsa) and Port Arthur.
- **Every district outside Texas:** the US total minus those five.

**"AI-related" and "non-AI" are our classification, not Census categories.**
They come from the paper [Trade in AI-Related Products](https://www.minneapolisfed.org/research/quarterly-review/trade-in-ai-related-products),
which tags every 10-digit code as High, Medium or Low relevance to AI data
center infrastructure. Exports use the combined import and export file,
[`hs10_classification_imports_exports.csv`](https://github.com/tradewartracker/ai-trade-index/blob/main/data-input/hs10_classification_imports_exports.csv),
matched on the 10-digit Schedule B code.

- AI-related is every High-relevance code (819 after the exclusions below).
  Non-AI is every Low-relevance code (19,751). The Medium-relevance codes
  (3,198; $229.5B of exports in January to September 2026) are in neither
  group, so "non-AI" is not "everything else" in the strict sense.
- HS chapters 27 (mineral fuels), 71 (precious metals and stones), 98 and 99
  (special provisions) are left out of every series.
- Schedule B codes introduced in 2026 that are not in the classification file
  belong to no group: 48 codes, $8.7B or 0.6% of January to September 2026
  exports nationally, and 0.1% of what left through El Paso.

## Source and vintage

- **US Census Bureau**, monthly merchandise trade: exports by Schedule B
  (10-digit) code (`timeseries/intltrade/exports/hs`, the data behind the
  FT900 release and USA Trade Online), FAS value. The national series use the
  cut by country (total for all countries); the district series use the cut by
  customs district of export (`DISTRICT`), all destinations.
- **Vintage:** the September 2026 release (FT900 published 4 November 2026).
  The district series were pulled from the Census API on 2026-11-13, all
  months. For the national series the 2026 months were pulled on 2026-11-04
  and the 2023 to 2025 months on 2026-08-13. The two pulls were checked
  against each other: a national pull on 2026-11-13 matched the earlier one to
  the dollar on every Schedule B line in each of the six months tested (June
  2023, June 2024, June and December 2025, March and September 2026). Census
  revises monthly data, so a fresh pull will not match this file exactly.
- Values are the Census domestic and foreign (re-export) component rows for
  each line, which sum to its total row.
- The port shares for Santa Teresa and Ysleta quoted above are from Census's
  port-level export file (`exports/porths`, 6-digit), pulled on 2026-11-10.
  They are not in `data.csv`.

## How to read it, and what it cannot tell you

- **Chart 1, 3-month average to September 2026:** El Paso 293 (+82.0% on a
  year earlier, from 161), the other Texas districts 164 (+27.4%, from 129),
  every district outside Texas 166 (+19.3%, from 139). For September alone:
  299, 191 and 177.
- **An index shows growth, not size.** In dollars, on the same 3-month
  average, El Paso is $5.86B a month (2023 average: $2.00B), the other Texas
  districts $5.61B ($3.43B) and the rest of the country $21.67B ($13.03B). El
  Paso was the smallest of the three in 2023; over January to September 2026
  it carried more than the rest of Texas combined ($49.0B against $47.0B).
- **AI-related exports grew everywhere.** The index for the whole country is
  180 on the same basis. The other Texas districts and the rest of the country
  are both about 65% above 2023; El Paso has nearly tripled.
- **Most of the past year's rise came between November 2025 and February
  2026.** El Paso's 3-month index sat between 158 and 165 from March to
  November 2025, reached 249 in February 2026 and 293 in September. Monthly, El Paso carried $2.92B in September
  2025, $5.49B in January 2026 and $5.98B in September 2026.
- **Chart 2, the dollars behind the bars.** AI-related: $24.0B of $221.5B in
  2023 (10.8%), $31.9B of $257.1B in 2024 (12.4%), $39.9B of $298.3B in 2025
  (13.4%), $49.0B of $282.8B in January to September 2026 (17.3%). Non-AI:
  $15.8B of $1,034.8B (1.5%), $15.8B of $1,046.1B (1.5%), $14.4B of $1,064.9B
  (1.4%), $11.1B of $814.8B (1.4%).
- **The last pair of bars is nine months, the others twelve.** In January to
  September 2025 the shares were 13.0% and 1.3%, close to the full-year
  figures, so the comparison holds. Over the latest 12 months they are 16.7%
  and 1.4%.
- **"One dollar in six" and "one in seventy" in post 2.** 17.3% is one dollar
  in 5.8 (16.7%, the latest 12 months, is one in six). 1.36% is one dollar in
  74.
- **El Paso's part of the national rise.** AI-related exports rose from
  $220.4B in January to September 2025 to $282.8B in the same months of 2026.
  El Paso went from $28.6B to $49.0B, a third of that rise (32.7%).
- **What is in the El Paso line.** In January to September 2026, 99.9% of it
  went to Mexico and 86% was re-exports: foreign-made goods that entered the
  US and left again in substantially the same condition (78% in 2023). Four
  Schedule B lines are 70% of it: parts and accessories of computers
  (8473300002, $20.2B, up from $10.3B in the same months of 2025), solid-state
  storage (8523510000, $6.2B, from $2.9B), central processing units
  (8542310045, $6.1B, from $5.6B) and other storage units (8471709000, $1.7B,
  from $0.8B). AI-related products were 73% of everything that left through El
  Paso, against 50% in 2023; for the country as a whole they were 21% and 14%.
  El Paso's share of all goods went from 3.1% in 2023 to 5.0%. (These figures come
  from the underlying Schedule B data, with the four chapters above left out;
  they cannot be recomputed from `data.csv`.)
- **The data names the exit and the destination country, nothing finer.** It
  says these goods left through the El Paso district and were bound for
  Mexico. It does not say they went to Ciudad Juarez, which is the reading in
  post 1, and it does not say where in the US they came from or, for a
  re-export, where they first entered.
- **The charts show what leaves, not what happens next.** That the goods sent
  to Mexico are assembled into servers that return to the US is the reading of
  the 10 November thread; nothing in this file traces a component into a
  server.
- **A category is a tag on a product, not a record of where it went.** A chip,
  a board or a transformer is counted as AI-related because that kind of
  product is used in data centers. The data cannot say whether a given
  shipment was bound for one.
- **The AI tag cannot be applied port by port.** Census publishes exports by
  individual port at 6 digits only, and the classification needs 10, so the
  district is the finest geography these series can use.
- Nothing is seasonally adjusted. The y-axis of chart 1 does not start at
  zero. The dashed rule at January 2025 marks the start of the 2025 tariff
  era, for orientation only.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
