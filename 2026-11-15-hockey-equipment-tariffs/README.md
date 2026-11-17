# Hockey equipment and the Section 338 tariffs on Canada, September 2026

Replication package for the two-post thread of **15 November 2026** (text and
links in `tweet.md`). Three charts were posted, one in the first post and two
in the reply:

| File | Post | What it shows |
|---|---|---|
| `chart_1_tariff_china_vs_canada.png` | 1 | The effective tariff rate (calculated duties ÷ customs value) on hockey sticks, skates and gear imported from China and from Canada |
| `chart_2_imports_index.png` | 2 | US imports of the same goods from each country, monthly, as an index (2024 = 100) |
| `chart_3_imports_3mo_average.png` | 2 | The same imports in dollars: a 3-month average, with the monthly figures as thin lines behind it |

This follows the thread of 14 November
([`2026-11-14-canada-338-tariffs`](../2026-11-14-canada-338-tariffs/)), which
showed every good on the Section 338 list together. That README describes the
three proclamations and their lists.

## Reproduce

```
pip install pandas matplotlib
python make_charts.py
```

`make_charts.py` reads `data.csv` and rewrites the three PNGs. On the machine
that produced the thread (matplotlib 3.10.6, pandas 2.3.3) the output is
byte-identical to the shipped files. Other versions may differ in font
rendering, not in the data.

## Data (`data.csv`)

One row per source-month, January 2022 to September 2026, 114 rows (two
sources, 57 months).

| Column | Meaning |
|---|---|
| `source` | `China` or `Canada` |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | US imports of the three lines below from that country, customs value, US dollars |
| `duties_usd` | Calculated duties on those imports, US dollars |
| `tariff_rate_pct` | `100 * duties_usd / imports_usd` |
| `index_2024_100` | `100 * imports_usd /` the source's average monthly imports in 2024 |
| `imports_usd_3mo` | Average of `imports_usd` over the month and the two before it |

The script recomputes the last three columns from the dollar columns; they are
in the file so the charts can be drawn without it. Chart 1 starts in January
2024 and charts 2 and 3 in January 2023; the file starts in 2022 because the
charts were drawn from the whole series.

**The product group is three 10-digit HTS lines, added together:**

| HTS10 | Description | US imports, all sources, 2024 |
|---|---|---:|
| 9506.99.25.40 | Ice-hockey sticks | $79.2M |
| 9506.99.25.80 | Other ice-hockey and field-hockey articles and equipment (not balls or skates) | $56.9M |
| 9506.70.40.00 | Ice skates with footwear permanently attached | $28.9M |

All three are on a Section 338 list at 50% from **22 August 2026**: 9506.99.25
on the list of Proclamation 11046 (the action answering provincial bans on US
alcohol) and 9506.70.40 on the list of Proclamation 11048 (the motor-vehicle
action). Both stayed on after the 15 September rewrite. The lists are in the
[`tariff-lists`](https://github.com/tradewartracker/trade-war-redux-2025/tree/main/tariff-lists)
folder of the Tracking U.S. Tariffs repository.

The group is added up in dollars, not units: skates are counted in pairs and
the rest in pieces.

## Source and vintage

- **US Census Bureau**, monthly merchandise trade by HTS10 and country (the
  data behind the FT900 release and USA Trade Online), imports for
  consumption, customs value and calculated duties.
- **Vintage:** the September 2026 release (FT900 published 4 November 2026).
  The 2026 months were pulled on 2026-11-04; the 2022 to 2025 months were
  pulled on 2026-08-13 and carry the revisions published up to then. Census
  revises monthly data, so a fresh pull will not match this file exactly.
- Values and duties are the Census total row for each line, not the sum of
  rate-provision components.

## How to read it, and what it cannot tell you

- **The figures behind the three charts:**

  | Month | China, imports | Index | Tariff rate | Canada, imports | Index | Tariff rate |
  |---|---:|---:|---:|---:|---:|---:|
  | Sep 2024 | $9.69M | 126 | 7.8% | $0.93M | 106 | 0.1% |
  | Sep 2025 | $9.89M | 128 | 37.9% | $2.58M | 293 | 7.7% |
  | Jul 2026 | $6.96M | 90 | 18.0% | $2.90M | 330 | 0.7% |
  | Aug 2026 | $7.83M | 102 | 19.8% | $3.39M | 385 | 1.7% |
  | Sep 2026 | $6.35M | 82 | 20.3% | $0.73M | 83 | 50.4% |

  The 2024 monthly averages behind the index are $7.7M for China and $0.9M
  for Canada, as the legend of chart 2 says.
- **These are small numbers.** The three lines together were $165.0M of US
  imports in 2024. A single shipment moves a monthly figure, and imports from
  China usually peak between July and October, ahead of the season.
- **"Two top sources" in post 1.** Over the 12 months to September 2026 China
  supplied 44.4% of the group and Canada 14.2%, ahead of Thailand (12.2%),
  Vietnam (11.8%) and Mexico (8.8%). In 2024 Canada was fifth, with 6.4%,
  behind China (56.1%), Vietnam, Thailand and Mexico.
- **The two countries sell different things.** Over the same 12 months, $45.5M
  of the $69.9M from China was sticks. Of the $22.5M from Canada, $21.5M was
  other hockey equipment, $0.5M skates and $0.4M sticks.
- **Chart 1.** In September 2026, the first full month of the duty, goods from
  Canada paid 50.4% and goods from China 20.3%. It is the first month in the
  file in which Canada's rate is above China's. August is a partial month:
  the duty applied from the 22nd, and Canada's rate for the month was 1.7%.
- **How the two rates got there.** By year, duties over imports: China 7.8%
  in 2024, 33.6% in 2025 and 20.2% in January to September 2026, with a peak
  of 88.3% in May 2025 and about 38% from June to October 2025. Canada 0.4%
  in 2024 and 7.5% in 2025: between 3.9% and 11.4% a month from March 2025 to
  March 2026, then under 2% from April to August 2026.
- **The effective rate is not the statutory rate.** It is calculated duties
  divided by customs value for goods entered in the month. In September 2026
  it was 49.1% on other hockey equipment from Canada, 54.7% on sticks and
  60.7% on skates: the 50% comes on top of whatever else applied. The data do
  not say which duty an entry paid.
- **"Clobbered" in post 2.** Imports from Canada were $0.73M in September
  2026, 78.5% below August and 71.8% below September 2025. From August to
  September they had moved +3.3%, +12.3%, −24.5% and −10.2% in 2022 to 2025.
- **Some of the fall is timing.** The duties were announced on 20 July, and
  July ($2.90M) and August ($3.39M) are two of the three highest months for
  Canada in the file. That is why the 3-month average in chart 3 is still
  $2.3M, 12.6% below a year earlier, while the single month is down 71.8%.
  One full month of data cannot separate goods brought in early from trade
  that has stopped.
- **Canada's imports had already doubled.** They were $10.5M in 2024 and
  $20.2M in 2025; the index was above 130 in every month from May 2025 to
  August 2026. The rise began in May 2025, the month China's rate peaked.
- **"Back toward sourcing from China" in post 2 is about incentives, not yet
  about trade.** The rates now favour China over Canada by 30 points. Imports
  from China have not risen so far: September 2026 was $6.35M, 35.7% below a
  year earlier and 18.9% below August, and January to September 2026 was
  $51.1M against $69.0M in the same months of 2025. Their 3-month average has
  climbed from $4.5M in April to $7.0M, which is also what the season does.
- **Everyone else.** All other countries together shipped $6.78M of the group
  in September 2026, up from $5.25M in August and 38.6% above September 2025.
  Imports from all sources were $13.9M, 20.1% below a year earlier.
- **An index shows growth, not size.** In chart 2 the lines end at 82 and 83:
  by coincidence, both countries were 17 to 18% below their own 2024 average
  in September 2026. In dollars China was almost nine times Canada that month.
- The source shares, the split by line, the rates by line and the figures for
  other countries and all sources come from the underlying HTS10 data; they
  cannot be recomputed from `data.csv`.
- Nothing is seasonally adjusted. The dashed rules mark January 2025 (the
  start of the 2025 tariff era, for orientation) and 22 August 2026 (the
  Section 338 duty in force). The y-axes start at zero.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
