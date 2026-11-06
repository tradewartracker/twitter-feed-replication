# US passenger-car imports: the missing cars, and Japan's response, August 2026

Replication package for the four-post thread of **16 October 2026** (text and
links in `tweet.md`). One chart per post:

| File | Post | What it shows |
|---|---|---|
| `chart_1_total_units.png` | 1 | Number of passenger cars imported into the US per month, all sources, with each calendar year's average drawn as a dashed segment |
| `chart_2_tariff.png` | 2 | Effective tariff rate (calculated duties ÷ customs value) on those cars, all sources, from January 2024, peak marked |
| `chart_3_japan_units.png` | 3 | Number of passenger cars imported from Japan per month, with yearly averages |
| `chart_4_japan_unit_value.png` | 4 | Average customs value per car imported from Japan (value ÷ units), with yearly averages |

## Reproduce

```
pip install pandas matplotlib
python make_charts.py
```

`make_charts.py` reads `data.csv` and rewrites the four PNGs. On the machine
that produced the thread (matplotlib 3.10.6, pandas 2.3.3) the output is
byte-identical to the shipped files. Other versions may differ in font
rendering, not in the data.

## Data (`data.csv`)

One row per source-month, January 2023 to August 2026, 88 rows.

| Column | Meaning |
|---|---|
| `source` | `all` (every source country, the Census total) or `japan` |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | General imports of every HTS10 line under HS 8703, customs value, US dollars, summed over the lines |
| `duties_usd` | Calculated duties on those imports, US dollars |
| `units` | Number of vehicles (the Census first quantity, unit `NO`, reported on every HS 8703 line) |
| `tariff_rate_pct` | `100 * duties_usd / imports_usd` |
| `unit_value_usd` | `imports_usd / units`, the average customs value of a car that month |

**What HS 8703 is.** "Motor cars and other motor vehicles principally
designed for the transport of persons": sedans, hatchbacks, wagons,
crossovers, SUVs and minivans, new and used. The 10-digit lines split cars by
engine size, cylinder count and powertrain (petrol, hybrid, plug-in, electric),
never by body style, so the series cannot distinguish an SUV from a sedan.
Pickups and other goods vehicles are HS 8704 and are not included. Every
line under 8703 reports its quantity in vehicles, so the units sum cleanly
and no value is missing a quantity.

## Source and vintage

- **US Census Bureau**, monthly merchandise trade by HTS10 and country
  (the data behind the FT900 release and USA Trade Online), general imports,
  customs value, calculated duties and first quantity.
- **Vintage:** the August 2026 release (FT900 published 6 October 2026),
  pulled on 2026-10-06. Earlier months carry the revisions published through
  that release. Census revises monthly data, so a fresh pull will not match
  this file exactly.
- Values, duties and units are the Census total row for each line, not the
  sum of rate-provision components.

## How to read it, and what it cannot tell you

- **The missing cars.** US car imports averaged 768K a month in 2023 and
  784K in 2024, then 613K in 2025 and 560K in the first eight months of
  2026. Against 2024 that is 225K fewer cars a month, a 29% fall (the post
  rounds it to "about 200K"). Annual totals: 9.22M, 9.41M, 7.36M, and 4.48M
  for January to August 2026. The chart deliberately carries no
  year-on-year figure: August 2026 is 553K against 569K in August 2025, a
  comparison between two post-tariff months that says nothing about the
  level shift. Read the dashed yearly segments.
- **The tariff.** Duties on imported cars were 1.6% of customs value in 2024.
  The rate jumped in April 2025, peaked at 24.2% in May 2025 (the post says
  "25%"), and fell through the second half of 2025 as the Japan, EU and
  Korea deals took effect. It has sat between 13.3% and 15.5% in every month
  of 2026 and was 15.0% in August 2026. The dip to 13.3% in November 2025 is
  a refund month on cars from Korea (Korea's own rate printed 2.5% that
  month), not a change in policy.
- **Japan.** Cars from Japan averaged 197K a month in 2024 and 115K so far in
  2026, 82K fewer a month, a 42% fall. On the latest twelve months the gap is
  84K (the post's "about 85K"). Japan alone is 37% of the total fall in
  cars, more than its 25% share of 2024 imports. Its share of the cars the
  US imports has gone from 25% in 2024 to 20% in 2026.
- **The other sources in post 3** (Germany, then Mexico) are not in
  `data.csv`. From the same Census release, on the same 2024-average to
  latest-12-months comparison: Germany sent 31K fewer cars a month and Mexico
  29K fewer, against Japan's 84K.
- **Japan's unit value.** The average customs value of a car from Japan was
  $16.7K in 2023 and $17.7K in 2024, $21.9K in 2025 and $26.5K so far in
  2026, a 49% rise on 2024 (47% on the latest twelve months). The rise is
  visible inside every engine and powertrain line, not just between them:
  the cheap lines (1.0 to 1.5L petrol cars, sub-$16K hybrids) lost the most
  units. Because of it, the dollar value of cars from Japan is down only 13%
  on 2024 ($3.49B to $3.03B a month) while the number of cars is down 42%.
- **Customs value excludes the duty.** The $ per car is what the importer
  declares before tariffs, so the rise is not the tariff being counted in.
  It is some mix of cheaper models leaving the export lineup and higher
  prices on the models that remain, and the data cannot separate the two.
  It also cannot show whether the shift is toward SUVs (see the HS 8703 note
  above).
- **The yen is not the explanation.** It weakened against the dollar over
  the same period (about 151 yen per dollar on average in 2024, about 157 on
  the latest twelve months), which pushes dollar prices down, not up.
- **The yearly unit-value segments** are the year's value divided by the
  year's units, not the mean of the monthly ratios. The yearly unit
  segments are the mean of the monthly counts.
- The effective tariff rate is calculated duties divided by customs value
  for goods entered in the month. It reflects exemptions and chapter-99
  actions as actually applied, which is why it differs from statutory rates.
- The unit charts start in 2023. The tariff chart starts in 2024 because
  nothing happens on it before 2025. All four carry a dashed rule at
  January 2025, the start of the 2025 tariff era, for orientation.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
