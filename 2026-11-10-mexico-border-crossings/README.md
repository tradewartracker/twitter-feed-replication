# Servers crossing the Mexican border, September 2026

Replication package for the three-post thread of **10 November 2026** (text and
links in `tweet.md`). Three charts were posted, one per post:

| File | Post | What it shows |
|---|---|---|
| `chart_1_border_crossings.png` | 1 | A strip splitting all US server imports (HS 847150), January–September 2026, between Mexican border crossings and every other US port; below it, the value entering through each of the five big crossings |
| `chart_2_servers_by_crossing.png` | 2 | Servers imported from Mexico, monthly, through Ysleta, Laredo, Santa Teresa and Fabens, with the latest month and its change on a year earlier as end labels |
| `chart_3_value_units_unit_value.png` | 3 | Servers imported from Mexico, monthly: customs value, number of units and unit value, each as an index on its own 2023 monthly average, with the actual levels as end labels |

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

Long format, one row per chart, series and month: 1,307 rows.

| Column | Meaning |
|---|---|
| `chart` | 1, 2 or 3 |
| `series` | Chart 1: a US port of entry, named as Census names it (128 ports carry some value). Chart 2: one of the four crossings. Chart 3: `MEXICO` |
| `kind` | Chart 1 only: `Mexican border crossing` (the 13 ports on the Mexican land border that carry any value) or `other port` |
| `month` | Calendar month, `YYYY-MM`. Chart 1: January to September 2026. Charts 2 and 3: January 2022 to September 2026 |
| `value` | Charts 1 and 2: general import value, US dollars. Chart 3: customs value of imports for consumption, US dollars |
| `units` | Chart 3 only: number of units (the Census first quantity, unit `NO`, summed over the HTS10 lines under 847150) |

**Two Census series, on purpose.** Charts 1 and 2 use the port-of-entry
series, which Census publishes only at the 6-digit level and only as general
imports; chart 1 covers all origins, chart 2 imports from Mexico. Chart 3 uses
the country series at HTS10 (imports for consumption), summed over the lines
under 847150, because that is the series that carries units. For servers from
Mexico the two agree within 0.5%: January to September 2026 is $120.0B on the
port series and $119.4B on the country series.

- Chart 1 sums each port's nine months. The strip divides the sum over the
  `Mexican border crossing` ports by the sum over all ports. Five crossings are
  drawn; the other eight land ports together carry $36M.
- Chart 2 keeps the zero months (Fabens carried nothing before 2024).
- Chart 3: unit value is `value / units` for the month. The index divides each
  of the three series by its own 2023 monthly average: $2.083B, 844K units and
  $2,476 per unit.

## Source and vintage

- **US Census Bureau**, monthly merchandise trade. Charts 1 and 2: imports by
  port of entry and HS6 (`timeseries/intltrade/imports/porths`, general
  imports). Chart 3: imports by country and HTS10 (`timeseries/intltrade/imports/hs`,
  the data behind the FT900 release and USA Trade Online), customs value and
  first quantity.
- **Vintage:** the September 2026 release (FT900 published 4 November 2026).
  The port series was pulled from the Census API on 2026-11-10 for 2025 and
  2026 and on 2026-07-28 for 2022 to 2024. The country series' 2026 months were
  pulled on 2026-11-04 and its 2023 to 2025 months on 2026-08-13. Census
  revises monthly data, so a fresh pull will not match this file exactly.
- Chart 3 values and units are the Census total row for each line, not the sum
  of rate-provision components.

## How to read it, and what it cannot tell you

- **Chart 1, January to September 2026:** $243.4B of servers entered the US.
  $119.3B (49.0%) came through Mexican border crossings: Ysleta $45.9B, Laredo
  $44.1B, Santa Teresa $21.1B, Fabens $6.8B, the Bridge of the Americas in El
  Paso $1.4B. The largest ports not drawn are airports: Chicago $38.2B,
  Dallas–Fort Worth $22.7B, San Francisco $17.9B, Los Angeles $17.1B. (In 2025
  the crossings' share was 48.9%, and servers from Taiwan arrived 99% by air;
  neither figure can be recomputed from `data.csv`.)
- **Port of entry is where the goods crossed, not where they were made,** and
  chart 1 counts every origin: a server of Taiwanese origin trucked in through
  Laredo is counted at Laredo. For these crossings the difference from
  Mexico-origin-only is under 1% (Ysleta $45.9B all origins against $45.8B from
  Mexico). Ysleta, Santa Teresa, Fabens and the Bridge of the Americas all face
  Ciudad Juárez; Laredo faces Nuevo Laredo and funnels all of central Mexico,
  so it says little about which plant a shipment came from.
- **Chart 2, September 2026:** Ysleta $7.72B (+143.4% on a year earlier, from
  $3.17B), Laredo $7.85B (+185.2%, from $2.75B), Santa Teresa $3.86B (+306.2%,
  from $0.95B), Fabens $598M (from $56M; no change shown because it is a base
  effect). Ysleta carried $9.01B in July 2026 and $32.7B in all of 2025, which
  is $2.7B a month, the post's "about $3B". In 2022 the four carried $13.3B,
  $6.3B, $13.4B and nothing.
- **Chart 3, September 2026:** $20.4B (+186.5% on a year earlier), 657,831
  units (−37.6%), $30,950 per unit (+358.9%); as index values 977, 78 and
  1,250. January to September 2026 against the same months of 2025: $119.43B
  against $56.15B (+112.7%), 8.012M units against 10.884M (−26.4%), $14,906
  per unit against $5,159. Full years: 2023 $25.0B, 10.1M units, $2,469 per
  unit; 2024 $41.6B, 11.1M, $3,761; 2025 $80.6B, 14.1M, $5,709. The post's
  "$5K in 2025 → $31K in September 2026" is the 2025 full-year unit value
  against the September 2026 month.
- **Units are the Census "number" for these lines.** A unit can be a single
  server or an assembled rack, so the unit value is an average transaction
  value that moves with the mix of what is shipped as well as with prices.
  Monthly units are noisy (650K in February 2026, 1.14M in June 2026); the
  year-to-date comparison is the robust one.
- Nothing is seasonally adjusted. The dashed rule at January 2025 marks the
  start of the 2025 tariff era, for orientation only.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
