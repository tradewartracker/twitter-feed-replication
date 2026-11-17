# The US trade deficit with ASEAN and China: tariffs and AI-related products, September 2026

Replication package for the three-post thread of **17 November 2026** (text and
links in `tweet.md`). Three charts were posted, one per post:

| File | Post | What it shows |
|---|---|---|
| `chart_1_deficit_asean_vs_china.png` | 1 | The US goods trade deficit with ASEAN and with China, monthly |
| `chart_2_tariff_asean_vs_china.png` | 2 | The effective tariff rate (calculated duties ÷ customs value) on US imports from ASEAN and from China |
| `chart_3_asean_deficit_total_vs_ai.png` | 3 | The deficit with ASEAN again, next to the part of it that is AI-related products |

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

One row per partner-month, January 2023 to September 2026, 90 rows (two
partners, 45 months). The charts start in January 2024; the 2023 rows are there
for comparison.

| Column | Meaning |
|---|---|
| `partner` | `ASEAN` (seven members, see below) or `China` |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | US imports from the partner, customs value, US dollars |
| `exports_usd` | US exports to the partner, FAS value, US dollars |
| `duties_usd` | Calculated duties on those imports, US dollars |
| `ai_imports_usd` | The part of `imports_usd` that is AI-related products. ASEAN only |
| `ai_exports_usd` | The part of `exports_usd` that is AI-related products. ASEAN only |
| `deficit_usd` | `imports_usd - exports_usd` |
| `tariff_rate_pct` | `100 * duties_usd / imports_usd` |
| `ai_deficit_usd` | `ai_imports_usd - ai_exports_usd`. ASEAN only |

The script recomputes the last three columns from the dollar columns; they are
in the file so the charts can be drawn without it.

**"ASEAN" here is seven of its eleven members:** Vietnam, Thailand, Malaysia,
Singapore, Indonesia, the Philippines and Cambodia, added together. Brunei,
Laos, Myanmar and Timor-Leste are left out because the dataset behind these
charts keeps the largest US trading partners (every country in the top 50 by
imports or the top 50 by exports in 2025, 60 countries in all) and none of the
four is among them. That also bounds what is missing: each of the four was below the
50th-ranked partner in 2025 ($5.6B of imports, $4.5B of exports), so the seven
are at least 95% of US imports from ASEAN. That is a worst case, not an
estimate.

**The deficit is imports minus exports, drawn as a positive number.** Imports
are imports for consumption at customs value. Exports are total exports at FAS
value: goods made in the US plus re-exports of foreign goods. The trade balance
Census publishes uses general imports, which count goods when they arrive
rather than when they clear customs, so its monthly figures differ somewhat
from these.

**"AI-related" is our classification, not a Census category.** It comes from
the paper [Trade in AI-Related Products](https://www.minneapolisfed.org/research/quarterly-review/trade-in-ai-related-products),
which tags every 10-digit code as High, Medium or Low relevance to AI data
center infrastructure. AI-related is every High-relevance code.

- Imports use the import file,
  [`hs10_classification_final_v3.csv`](https://github.com/tradewartracker/ai-trade-index/blob/main/data-input/hs10_classification_final_v3.csv),
  matched on the 10-digit HTS code (645 codes after the exclusions below).
  Exports use the combined import and export file,
  [`hs10_classification_imports_exports.csv`](https://github.com/tradewartracker/ai-trade-index/blob/main/data-input/hs10_classification_imports_exports.csv),
  matched on the 10-digit Schedule B code (819 codes).
- HS chapters 27 (mineral fuels), 71 (precious metals and stones), 98 and 99
  (special provisions) are never counted as AI-related. They are still in the
  total deficit.
- Everything that is not AI-related is in the gap between the two lines of
  chart 3: Low relevance, Medium relevance and untagged codes alike.

## Source and vintage

- **US Census Bureau**, monthly merchandise trade by 10-digit code and country
  (the data behind the FT900 release and USA Trade Online): imports for
  consumption, customs value and calculated duties; total exports, FAS value.
- **Vintage:** the September 2026 release (FT900 published 4 November 2026).
  The 2026 months were pulled on 2026-11-04; the 2023 to 2025 months were
  pulled on 2026-08-13 and carry the revisions published up to then. Census
  revises monthly data, so a fresh pull will not match this file exactly.
- Values and duties are the Census total row for each line, not the sum of
  its components.

## How to read it, and what it cannot tell you

- **The figures behind chart 1:**

  | Month | ASEAN deficit | Imports | Exports | China deficit | Imports | Exports |
  |---|---:|---:|---:|---:|---:|---:|
  | Jan 2024 | $16.7B | $25.3B | $8.6B | $23.3B | $35.4B | $12.1B |
  | Sep 2024 | $22.2B | $33.1B | $10.9B | $31.0B | $42.1B | $11.1B |
  | Sep 2025 | $29.9B | $39.9B | $10.0B | $14.5B | $22.9B | $8.4B |
  | Sep 2026 | $47.2B | $63.1B | $15.9B | $21.2B | $30.8B | $9.6B |

  Average monthly deficit by year, ASEAN then China: $16.52B and $22.79B in
  2023, $19.10B and $23.98B in 2024, $26.90B and $16.15B in 2025, $37.82B and
  $13.66B in January to September 2026.
- **"3X" in post 1.** The deficit with ASEAN in September 2026 ($47.2B) is 2.8
  times January 2024 ($16.7B), where the chart starts, 2.9 times the 2023
  monthly average and 3.1 times February 2024 ($15.4B), the lowest month on
  the chart. Against September 2024 it is 2.1 times, and against September
  2025 1.6 times.
- **The deficit with China fell, then turned up.** It averaged $24.0B a month
  in 2024, fell to $8.2B in June 2025 and to $8.8B in March 2026, and was
  $21.2B in September 2026. That is 46% above September 2025 and 32% below
  September 2024. Chart 1 carries no year-on-year labels for this reason: the
  year-ago month sits in the trough, so the change reads as growth while the
  level is well below 2024.
- **The lines crossed in March 2025.** The deficit with ASEAN was below the
  deficit with China in every month from January 2023 to February 2025 and
  has been above it in every month since. In September 2026 it is 2.2 times
  as large.
- **Both sides of the ASEAN ledger grew.** Against September 2025, imports
  from ASEAN were up 58.1% and exports to ASEAN up 58.5%. The deficit widened
  because imports are four times exports.
- **The figures behind chart 2,** the year's duties divided by the year's
  imports:

  | | ASEAN | China |
  |---|---:|---:|
  | 2023 | 2.61% | 10.52% |
  | 2024 | 2.62% | 10.93% |
  | 2025 | 7.85% | 30.60% |
  | Jan–Sep 2026 | 7.24% | 23.46% |
  | Highest month | 12.17%, Sep 2025 | 47.92%, May 2025 |
  | Sep 2026 | 6.37% | 19.87% |

  In September 2026 imports from China paid $6.1B of duties on $30.8B;
  imports from ASEAN paid $4.0B on $63.1B.
- **"The average tariff" in post 2.** The rate on US imports from all
  countries in September 2026 was 6.49%, against 6.37% for ASEAN. The
  all-country line is not on the chart or in `data.csv`.
- **The ASEAN rate is an average over very different members and products.**
  In September 2026 the rates were Cambodia 20.7%, Indonesia 14.2%, Vietnam
  6.9%, Thailand 4.7%, the Philippines 4.5%, Malaysia 3.8% and Singapore 2.0%.
  AI-related products, more than half of imports from ASEAN that month, paid
  1.2%; everything else paid 12.3%.
- **What moved the rates.** The charts mark only January 2025. The steps
  after it follow the tariff actions documented in the
  [Tracking U.S. Tariffs](https://github.com/tradewartracker/trade-war-redux-2025)
  repository: the IEEPA tariffs of 2025 (the reciprocal tariffs from April,
  country-specific rates from 7 August, a reduction for China from
  1 November); the Supreme Court ruling of 20 February 2026 that ended them;
  a 10% Section 122 surcharge from 24 February to 23 July 2026; and, from
  24 July 2026, Section 301 duties over forced-labor enforcement of 12.5% on
  China, Vietnam, Thailand, Singapore and the Philippines and 10% on
  Malaysia, Indonesia and Cambodia. Section 232 duties and the 2018–19
  Section 301 duties on China ran throughout.
- **The effective rate is not the statutory rate.** It is calculated duties
  divided by customs value for goods entered in the month, so it reflects
  every exemption as actually applied and the mix of goods that came in.
- **The figures behind chart 3,** the deficit with ASEAN:

  | Month | Total | AI-related products | Share | Everything else |
  |---|---:|---:|---:|---:|
  | Jan 2024 | $16.72B | $3.87B | 23.1% | $12.85B |
  | Sep 2024 | $22.19B | $6.18B | 27.9% | $16.01B |
  | Sep 2025 | $29.90B | $10.31B | 34.5% | $19.59B |
  | Sep 2026 | $47.22B | $28.71B | 60.8% | $18.51B |

  By year the AI-related share of the deficit was 26.8% in 2023, 26.2% in
  2024, 33.9% in 2025 and 54.6% in January to September 2026.
- **"Accounted for by flows of AI-related products" in post 3.** From
  September 2025 to September 2026 the monthly deficit with ASEAN rose
  $17.3B. The AI-related part rose $18.4B and everything else fell $1.1B.
  Over the whole chart, January 2024 to September 2026, the deficit rose
  $30.5B: $24.8B AI-related and $5.7B everything else. The gap between the
  two lines, the deficit in everything else, has stayed between $11.7B and
  $22.0B since January 2024.
- **It is the import side.** In September 2026 the US imported $33.7B of
  AI-related products from ASEAN and exported $5.0B to it ($12.9B and $2.6B a
  year earlier).
- **What the AI-related imports are.** In September 2026: networking
  equipment (HS 851762) $9.7B, computer parts including memory modules
  (HS 847330) $8.8B, solid-state storage (HS 852351) $5.6B, servers
  (HS 847150) $4.0B and storage units (HS 847170) $1.8B. A year earlier
  the same five were $4.6B, $2.0B, $0.7B, $1.2B and $0.9B. By member: Vietnam
  $14.3B, Thailand $10.0B, Malaysia $5.6B, the Philippines $2.0B, Singapore
  $1.4B.
- **The same is true of the US deficit as a whole.** Over the 12 months to
  September 2026, AI-related products were 52.3% of the deficit with ASEAN
  and 53.6% of the US deficit with all countries (17.6% in calendar 2024).
  For China the figure is 7.9%.
- **An accounting statement, not a cause.** Chart 3 splits the deficit by
  product. It does not say why imports of these products rose or what the
  deficit would have been without them.
- **A category is a tag on a product, not a record of where it went.** A
  switch, a memory module or a storage drive is counted as AI-related because
  that kind of product is used in data centers. The data cannot say whether a
  given shipment was bound for one.
- **Some new 2026 codes are untagged.** Census replaced a number of 10-digit
  codes during 2026 and the new codes are not in the classification files.
  They count as not AI-related even where the code they replaced was. For
  imports from ASEAN that is $1.0B in September 2026 (1.6%). Giving each new
  code the tag of the main code under the same 8 digits would put the
  AI-related part of the deficit at $29.3B instead of $28.7B.
- **A bilateral deficit is recorded by country of origin.** Goods assembled in
  an ASEAN country count as imports from that country whatever the origin of
  their components. The data cannot say how much of the rise replaced goods
  that used to come from China.
- Nothing is seasonally adjusted. The deficit with ASEAN dips every February
  ($15.4B in 2024, $20.7B in 2025, $25.6B in 2026) and the deficit with China
  used to peak in the autumn ($31.0B in September 2024).
- The y-axes of charts 1 and 3 do not start at zero; chart 2 does. The dashed
  rule at January 2025 marks the start of the 2025 tariff era, for
  orientation only.
- The all-country tariff rate, the rates by member and by product group, the
  product and member detail of AI-related imports, the untagged-code figures
  and the all-country and China shares come from the underlying 10-digit
  data; they cannot be recomputed from `data.csv`.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
