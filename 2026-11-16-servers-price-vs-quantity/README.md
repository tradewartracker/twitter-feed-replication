# US imports of servers (HS 847150): price or quantity? September 2026

Replication package for the two-post thread of **16 November 2026** (text and
links in `tweet.md`). Two charts were posted, one per post:

| File | Post | What it shows |
|---|---|---|
| `chart_1_value_units_unit_value.png` | 1 | US imports of servers from all sources: customs value, number of units and unit value, each as an index (2023 = 100), 3-month averages, with the actual levels as end labels |
| `chart_2_unit_value_by_source.png` | 2 | The unit value in dollars per unit from all sources and from Mexico, Taiwan and Thailand, 3-month averages |

Earlier threads on the same product:
[`2026-10-09-servers-mexico`](../2026-10-09-servers-mexico/) (value by source)
and [`2026-11-10-mexico-border-crossings`](../2026-11-10-mexico-border-crossings/)
(value, units and unit value of servers from Mexico alone).

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

One row per source-month, January 2023 to September 2026, 180 rows (four
sources, 45 months).

| Column | Meaning |
|---|---|
| `source` | `All sources` (every source country, the Census total), `Mexico`, `Taiwan` or `Thailand` |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | US imports of HS 847150, customs value, US dollars |
| `units` | Number of units (the Census first quantity, unit `NO`, summed over the HTS10 lines under 847150) |
| `unit_value_usd` | `imports_usd / units` for the month |
| `imports_usd_3mo` | Average of `imports_usd` over the month and the two before it |
| `units_3mo` | The same average of `units` |
| `unit_value_3mo_usd` | `imports_usd_3mo / units_3mo` |

The script recomputes the last four columns from the first two; they are in the
file so the charts can be drawn without it. The `All sources` row is the Census
total, not the sum of the three countries.

- **The 3-month unit value is a ratio of averages,** 3-month value over
  3-month units, not the average of three monthly unit values. A month with
  many units counts for what it is worth.
- **The index in chart 1** divides each 3-month series by its own average
  over 2023 (the ten 3-month averages that end in March to December 2023):
  $3.09B a month, 1.41M units a month and $2,189 per unit.

**The product.** HS 847150 is "digital processing units other than those of
8471.41 or 8471.49", a computer's processing unit sold without being a
complete system. In practice this is where servers, GPU boxes and rack compute
land. Effectively all of the value is in one HTS10 line, 8471.50.0150 (all
but $0.08B of the $505.3B imported since January 2023).

## Source and vintage

- **US Census Bureau**, monthly merchandise trade by HTS10 and country (the
  data behind the FT900 release and USA Trade Online), imports for
  consumption: customs value and first quantity.
- **Vintage:** the September 2026 release (FT900 published 4 November 2026).
  The 2026 months were pulled on 2026-11-04; the 2023 to 2025 months were
  pulled on 2026-08-13 and carry the revisions published up to then. Census
  revises monthly data, so a fresh pull will not match this file exactly.
- Values and units are the Census total row for each line, not the sum of
  rate-provision components. Every dollar of this product is reported with a
  quantity.

## How to read it, and what it cannot tell you

- **Chart 1, 3-month average to September 2026, all sources:** value $33.8B a
  month (+112.5% on a year earlier, from $15.9B), 1.76M units a month (−2.6%,
  from 1.81M), $19,192 per unit (+118.2%, from $8,797). As index values:
  1,095, 125 and 877. A year earlier they were 515, 129 and 402.
- **September alone:** $38.3B (+176.9%), 1.735M units (+2.8%), $22,107 per
  unit (+169.3%). September 2026 is the highest month for value in the file.
- **The years:**

  | | Value | Units | Unit value |
  |---|---:|---:|---:|
  | 2023 | $36.9B | 16.61M | $2,223 |
  | 2024 | $61.6B | 17.05M | $3,615 |
  | 2025 | $163.6B | 27.37M | $5,978 |
  | Jan–Sep 2026 | $243.2B | 17.18M | $14,155 |

  January to September 2025 was $104.3B on 19.99M units, $5,216 per unit.
- **"All price" in post 1.** Over the past year the number of units barely
  moved and the dollars more than doubled, so on this arithmetic the whole
  rise is the unit value. The unit value is not a price: see the next three
  points.
- **Units are the Census "number" for these lines.** A unit can be a single
  server or an assembled rack. The unit value is an average transaction value
  that moves with what is being shipped as well as with what it costs. A
  shift from ordinary servers to GPU systems raises it without any price
  rising.
- **Chart 2, 3-month average to September 2026:**

  | Source | $ per unit | A year earlier | Change | September alone |
  |---|---:|---:|---:|---:|
  | All sources | $19,192 | $8,797 | +118.2% | $22,107 |
  | Mexico | $22,647 | $7,023 | +222.5% | $30,950 |
  | Taiwan | $51,066 | $21,425 | +138.4% | $54,638 |
  | Thailand | $23,918 | $13,539 | +76.7% | $21,682 |

  By year, Mexico, Taiwan, Thailand: $2,469, $6,191 and $2,185 in 2023;
  $3,761, $10,779 and $1,937 in 2024; $5,709, $9,399 and $14,857 in 2025;
  $14,906, $27,214 and $21,257 in January to September 2026.
- **"2X" for Taiwan in post 2.** For September alone the unit value from
  Taiwan is $54,638 against $27,153 a year earlier (+101.2%). On the 3-month
  average in the chart it is 2.4 times.
- **The rise is inside each source, not a shift between sources.** A Fisher
  index over all 59 source countries splits the change in the all-sources
  unit value into the change within sources and the change in the mix of
  sources. September 2026 on September 2025: +187% within sources, −6% from
  mix. The latest three months on a year earlier: +170% and −19%. Units moved
  toward the cheaper sources, which holds the all-sources figure down. This
  says nothing about the mix of products inside a source, which is the
  quality variation post 2 raises.
- **Three months of Taiwan's unit counts look like reporting artifacts.**
  Taiwan's count was 97K to 146K a month in 2024. It was 2.98M in May 2025,
  1.59M in December 2025 and 1.68M in February 2026, on ordinary dollar
  values ($5.9B, $10.5B and $11.9B). Those months pull Taiwan's unit value
  down sharply (the 3-month figure is $2,737 in May 2025 and $9,230 in
  February 2026) and account for much of the jaggedness of its line. They
  also inflate the all-sources unit count: its highest 3-month average,
  3.2M, is May 2025. Taiwan's 2025 full-year unit value ($9,399) is depressed
  for the same reason.
- **Taiwan's year-ago base is low as well.** The 3-month window a year
  earlier includes August 2025, when Taiwan reported 642K units against 185K
  in September. Part of the +138.4% is that month.
- **The three sources are most of the product.** In September 2026 Mexico
  was 53.1% of the value, Taiwan 30.3% and Thailand 7.5%, together 90.8%. By
  units they were 37.9%, 12.2% and 7.6%.
- **Each source is a different story.** On the 3-month average, Mexico's
  value is up 174.6% on 14.8% fewer units; Taiwan's is up 22.8% on 48.5%
  fewer; Thailand's is up 369.3% on 165.7% more. Thailand's unit value jumped
  in the second half of 2025 (its 3-month figure went from $3,549 in June to
  a peak of $32,782 in December 2025) and has been between $18,063 and
  $24,738 since January 2026.
- **Customs value is the price at the border.** A server assembled in Mexico
  or Thailand is valued whole, including chips and boards made elsewhere.
- The Fisher split and the HTS10 breakdown come from the underlying data for
  every source country; they cannot be recomputed from `data.csv`.
- Nothing is seasonally adjusted. Chart 1 is an index, so it shows growth,
  not size; chart 2's y-axis starts at zero. The dashed rule at January 2025
  marks the start of the 2025 tariff era, for orientation only.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
