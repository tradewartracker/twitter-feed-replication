# The Section 338 tariffs on Canada: listed goods vs everything else, September 2026

Replication package for the two-post thread of **14 November 2026** (text and
links in `tweet.md`). Two charts were posted, one in each post:

| File | Post | What it shows |
|---|---|---|
| `chart_1_338_goods_vs_other_index.png` | 1 | US imports from Canada of the goods on the Section 338 list against all other goods from Canada, each as an index (2025 = 100), monthly |
| `chart_2_338_goods_tariff_rate.png` | 2 | The effective tariff rate (calculated duties ÷ customs value) on the same two groups |

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

One row per group-month, January 2023 to September 2026, 90 rows (two groups,
45 months).

| Column | Meaning |
|---|---|
| `group` | `Section 338 goods` or `All other goods` |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | US imports from Canada, customs value, US dollars |
| `duties_usd` | Calculated duties on those imports, US dollars |
| `index_2025_100` | `100 * imports_usd /` the group's average monthly imports in 2025 |
| `tariff_rate_pct` | `100 * duties_usd / imports_usd` |

The script recomputes the last two columns from the dollar columns; they are in
the file so the charts can be drawn without it. Both charts plot the whole
series and start the x-axis in July 2025.

**The Section 338 actions.** Section 338 of the Tariff Act of 1930 (19 U.S.C.
§1338) lets the president put duties of up to 50% on a country that
discriminates against US commerce. Three proclamations dated 20 July 2026 used
it against Canada, each with its own list of products and all at 50%:
Proclamation 11046 (answering provincial bans on US alcohol), 11047 (Canada's
allocation of its cheese import quotas) and 11048 (Canada's motor-vehicle
tariffs and quotas). The duties were to start on 19 August; Proclamation 11056
of 18 August deferred them three days for talks, and they took effect on
**22 August 2026**. The lists were rewritten
on 15 September (Proclamations 11064 and 11065) and again on 30 October.

**The lists are public.** They were extracted from the proclamation annexes
for the [Tracking U.S. Tariffs](https://github.com/tradewartracker/trade-war-redux-2025)
repository and sit in its [`tariff-lists`](https://github.com/tradewartracker/trade-war-redux-2025/tree/main/tariff-lists)
folder: `canada-338-autos.csv`, `canada-338-alcohol.csv` and
`canada-338-dairy.csv` are the lists of 22 August (554 codes), the files dated
`2026-09-15` and `2026-10-30` are the rewrites (666 and 744 codes), and
`canada-338-aircraft-exempt.csv` is the civil-aircraft carve-out. Codes are
8-digit HTS subheadings; the rewrites also name a few 10-digit lines. A 10-digit
import line is on a list if its first 8 digits or all 10 are.

**The two groups are fixed for the whole series,** so each index compares the
same products over time:

- **`Section 338 goods`** are the lines on a 50% list from 22 August that were
  still on one after the 15 September rewrite, without the lines that fall
  under the civil-aircraft carve-out. The data end in September, so these are
  the goods that faced the duty from its first day to the end of the data.
- **`All other goods`** are the lines that were never on any version of the
  lists (22 August, 15 September or 30 October).
- **Lines in neither group:** those the 15 September rewrite took off or put
  on, those first listed on 30 October, and the listed lines under the aircraft
  carve-out. Over August 2025 to July 2026 the two groups are 4.15% and 93.37%
  of US imports from Canada and these lines the remaining 2.49%.

The three lists are named for the Canadian measures they answer, not for what
they cover. Almost all of the listed value is on the motor-vehicle list, and it
is not cars: by HS chapter, the charted group is electrical equipment (16%),
plastics (16%), furniture (9%), machinery (9%), precious metals and jewellery
(9%), wood (8%) and paper (7%), with beverages at 4%.

## Source and vintage

- **US Census Bureau**, monthly merchandise trade by HTS10 and country (the
  data behind the FT900 release and USA Trade Online), imports for consumption
  from Canada, customs value and calculated duties.
- **Vintage:** the September 2026 release (FT900 published 4 November 2026).
  The 2026 months were pulled on 2026-11-04; the 2023 to 2025 months were
  pulled on 2026-08-13 and carry the revisions published up to then. Census
  revises monthly data, so a fresh pull will not match this file exactly.
- Values and duties are the Census total row for each line, not the sum of
  rate-provision components.

## How to read it, and what it cannot tell you

- **The figures behind both charts:**

  | Month | 338 goods, imports | Index | Tariff rate | Duties | All other goods, imports | Index | Tariff rate |
  |---|---:|---:|---:|---:|---:|---:|---:|
  | Sep 2025 | $1.31B | 105.9 | 1.69% | $22.1M | $29.6B | 99.5 | 3.89% |
  | Jun 2026 | $1.50B | 121.3 | 0.55% | $8.2M | $34.8B | 116.8 | 2.94% |
  | Jul 2026 | $1.55B | 125.3 | 0.49% | $7.6M | $31.1B | 104.5 | 2.93% |
  | Aug 2026 | $1.58B | 128.4 | 5.67% | $89.8M | $33.2B | 111.3 | 2.99% |
  | Sep 2026 | $759M | 61.5 | 44.33% | $336.6M | $33.6B | 112.8 | 2.98% |

  The 2025 monthly averages behind the index are $1.23B and $29.8B.
- **"More than 40%" in post 1 is the change on a year earlier.** Imports of
  the listed goods in September 2026 were 41.9% below September 2025. Against
  August 2026 they were 52.1% lower. All other goods from Canada were 13.4%
  above a year earlier and 1.3% above August.
- **September does not usually fall.** From August to September the listed
  goods moved −3.2% in 2023, +10.6% in 2024 and +15.6% in 2025. The lowest
  month before this one was April 2025, at 84.9.
- **One full month, and some of it is timing.** The duties were announced a
  month before they began, and July (125.3) and August (128.4) are the two
  highest months in the series, so part of September's fall is goods brought in
  early. Over July to September 2026 together the listed goods averaged 105.1,
  against 99.0 in the same three months of 2025. The months after September
  will show how much of the fall lasts. August is also a partial month: the
  duty applied from the 22nd, which is why its rate is 5.67%.
- **"About 17 billion dollars" in post 1.** Over August 2025 to July 2026, the
  12 months before the duty, US imports from Canada of goods on the 22 August
  lists were $21.4B (5.6% of the $385.3B total), or $17.7B (4.6%) without the
  lines under the aircraft carve-out. The charted group, which also leaves out
  the lines the 15 September rewrite moved, is $16.0B.
- **An index shows growth, not size.** The listed goods are about one dollar
  in 24 of what the US imports from Canada. In September 2026 they were $759M
  against $33.6B for everything else.
- **A third of "all other goods" is energy.** Mineral fuels (HS chapter 27)
  are 33.7% of that group, and their value moves with the oil price. Without
  them the group's September index is 108.5 (+6.6% on a year earlier) instead
  of 112.8.
- **It is the tariff, not the products.** The same listed goods from every
  other country, weighted by Canada's 2025 product mix, stood at 104.5 in
  July, 107.6 in August and 107.0 in September on the same index.
- **It is not goods waiting in warehouses.** The series is imports for
  consumption, which leaves out goods entered into bonded warehouses and
  foreign-trade zones until they are withdrawn. On general imports, which count
  goods on arrival, the listed index for September is 61.7.
- **The fall is broad but not uniform.** Lines that carried 73% of the listed
  value before the duty were more than 25% below their August 2025 to July
  2026 average in September. Precious metals and jewellery (HS chapter 71)
  went from $116.9M a month to $3.8M; beverages (chapter 22) rose, from $58.5M
  to $72.9M.
- **The effective rate is not the statutory rate.** It is calculated duties
  divided by customs value for goods entered in the month, so it reflects
  every exemption as actually applied. The listed goods paid 0.16% in 2024 and
  1.42% in 2025, and 44.3% in September 2026, below the 50% on top of ordinary
  duties that the proclamations set. One reason is in the rules: until 15
  September the actions exempted goods already under Section 232 duties
  (steel, aluminum, copper, autos and parts, timber). The data do not say which
  entries were exempt or why.
- **The lines left out were hit too.** In September 2026 the listed lines
  under the aircraft carve-out paid 39.2% and their imports were $175M, down
  from $336M in August: the carve-out is for civil-aircraft use, and most of
  what enters under those codes is something else. The lines the 15 September
  rewrite took off the list fell from $288M to $115M and paid 11.8%; the lines
  it put on were flat ($154M, then $155M) and paid 25.0%.
- **An import ban followed.** From 29 September a further set of proclamations
  banned imports of some goods that were already on the lists (packaged beer,
  wine and spirits; whey, molasses and non-alcoholic beer; motorcycles over
  800cc). The ban covers the last two days of the data.
- **A group is a list of product codes, not a record of what was charged.** A
  line is in the listed group because its code is on a list. The data cannot
  say which entries paid the Section 338 duty rather than another one.
- The shares of imports from Canada, the dollar values of the lists, the
  breakdown by HS chapter, the energy, other-country, general-import and
  line-level figures, and those for the lines in neither group come from the
  underlying HTS10 data; they cannot be recomputed from `data.csv`.
- Nothing is seasonally adjusted. The y-axis of chart 1 does not start at
  zero. The dashed rules mark 20 July 2026 (the proclamations) and 22 August
  2026 (the duty in force).

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
