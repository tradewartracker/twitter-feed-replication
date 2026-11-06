# The AI trade index: beyond chips and servers, September 2026

Replication package for the five-post thread of **6 November 2026** (text and
links in `tweet.md`). Four charts were posted, one in each of the first four
posts:

| File | Post | What it shows |
|---|---|---|
| `chart_1_ai_vs_nonai_index.png` | 1 | US imports of AI-related and non-AI products, monthly, as an index (2023 monthly average = 100) |
| `chart_2_power_cooling_index.png` | 2 | The same index for two AI-related categories, Electrical Power and Cooling & HVAC, against non-AI products, as a 3-month average |
| `chart_3_tariff_by_category.png` | 3 | Effective tariff rate (calculated duties ÷ customs value) on four AI-related categories and on non-AI products |
| `chart_4_imports_vs_duties.png` | 4 | Each category's share of AI-related imports next to its share of the duties paid on them, October 2025 to September 2026 |

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

One row per classification-group-month, January 2023 to September 2026, 540
rows.

| Column | Meaning |
|---|---|
| `classification` | `published` or `new_codes`: which version of the product classification the row uses (explained below) |
| `group` | `AI-related`, `Non-AI`, or one of the seven AI-related categories |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | US imports from all countries, customs value, US dollars |
| `duties_usd` | Calculated duties on those imports, US dollars |
| `index_2023_100` | `100 * imports_usd / (the group's average monthly imports in 2023)` |
| `tariff_rate_pct` | `100 * duties_usd / imports_usd` |

**The groups are our classification, not a Census category.** They come from
the paper [Trade in AI-Related Products](https://www.minneapolisfed.org/research/quarterly-review/trade-in-ai-related-products),
which tags every 10-digit HTS code as High, Medium or Low relevance to AI data
center infrastructure and gives each High code one of seven categories. The
tags, with the written reason for each code, are public:
[`hs10_classification_final_v3.csv`](https://github.com/tradewartracker/ai-trade-index/blob/main/data-input/hs10_classification_final_v3.csv).

- `AI-related` is every High-relevance code. It equals the sum of the seven
  categories in every month, for both dollars and duties: Compute Hardware,
  Networking & Telecom, Electrical Power, Cooling & HVAC, Building & Structure,
  Fire Safety & Security, Specialty Materials.
- `Non-AI` is every Low-relevance code. Medium-relevance codes are in neither
  group, so `AI-related` plus `Non-AI` is less than total imports.
- HS chapters 27 (mineral fuels), 71 (precious metals and stones), 98 and 99
  (special provisions) are left out of every group.

**The two values of `classification`.** During 2026 Census replaced a number
of HTS10 codes with new ones, and the new codes are not in the classification
file: 433 codes, $11.7B or 3.8% of September 2026 imports (after the chapter
exclusions).

- `published` uses the file as it stands, so the new codes belong to no group.
  This is the series the [AI trade tracker](https://www.tradewartracker.com/ai-trade-tracker.html)
  shows. All nine groups are in the file on this basis.
- `new_codes` gives each new code the tag of the classified code with the
  largest 2025 import value among those sharing its first eight digits. Only
  the three groups that chart 2 draws are in the file on this basis.

Charts 1, 3 and 4 use `published`. Chart 2 uses `new_codes`, because the
renumbering falls hardest on the two categories it shows. The clearest case is
lithium-ion batteries: code 8507600020 (Electrical Power) ends in January 2026
and continues from February as 8507600030 and 8507600090, which carry no tag.
Heat-pump parts, inverters and pump parts were renumbered the same way. On the
`published` basis that trade drops out of the category on the changeover month
although nothing changed at the border.

## Source and vintage

- **US Census Bureau**, monthly merchandise trade by HTS10 (the data behind the
  FT900 release and USA Trade Online), imports from all countries, customs
  value and calculated duties.
- **Vintage:** the September 2026 release (FT900 published 4 November 2026).
  The 2026 months were pulled on 2026-11-04; the 2023 to 2025 months were
  pulled on 2026-08-13 and carry the revisions published up to then. Census
  revises monthly data, so a fresh pull will not match this file exactly.
- Values and duties are the Census total row for each line, not the sum of
  rate-provision components.

## How to read it, and what it cannot tell you

- **Chart 1, September 2026:** the AI-related index is 369.2, up 120.0% on the
  year ($116.6B against $53.0B). Non-AI is 99.2, down 4.8% ($151.7B against
  $159.4B). The AI-related index averaged 122.9 in 2024 and 172.4 in 2025,
  first passed 200 in October 2025 and 300 in July 2026.
- **Chart 2, 3-month average to September 2026:** Electrical Power 162.0
  (+29.8% on the year), Cooling & HVAC 140.0 (+18.7%), non-AI 101.4 (+2.6%).
  The index levels are in the hundreds; growth over the year is in the tens of
  percent, and against the 2023 average it is +62% and +40%. For September
  alone the three are 162.7, 138.3 and 104.1.
- **The choice of classification matters for chart 2.** On the `published`
  basis the same 3-month averages are 145.4 (+16.6%), 118.9 (+0.8%) and 96.5
  (−2.4%). In dollars for September 2026: Electrical Power $15.86B with the new
  codes and $14.28B without, Cooling & HVAC $4.79B and $4.06B, non-AI $159.12B
  and $151.68B. The two bases are identical through January 2026 for the two
  categories; the gap opens in February and widens in July, the two months in
  which most of the new codes appear.
- **Charts 1 and 2 are therefore on different bases**, which is why non-AI
  ends at 99 in chart 1 and 101 in chart 2 (the second is also a 3-month
  average). With the new codes included, chart 1's non-AI line would end at
  104 rather than 99, and its AI-related line at 378 rather than 369.
- **Chart 3, September 2026:** Compute Hardware 0.48%, Networking & Telecom
  1.93%, Electrical Power 10.25%, Cooling & HVAC 10.23%, non-AI 9.25%. The
  monthly rates in 2024 averaged 0.58%, 1.56%, 3.48%, 3.06% and 2.71%. Electrical Power
  peaked at 16.72% in November 2025, Cooling & HVAC at 16.54% in September
  2025, non-AI at 13.60% in October 2025. AI-related imports as a whole paid
  2.44% in September 2026. Building & Structure, not drawn, paid 28.02%.
- **Chart 4, October 2025 to September 2026.** AI-related imports were
  $969.3B and paid $32.45B in duties (3.35%):

  | Category | Imports | Duties | Share of imports | Share of duties | Rate |
  |---|---:|---:|---:|---:|---:|
  | Compute Hardware | $619.3B | $3.83B | 63.9% | 11.8% | 0.62% |
  | Electrical Power | $147.7B | $16.89B | 15.2% | 52.1% | 11.44% |
  | Networking & Telecom | $144.8B | $3.36B | 14.9% | 10.4% | 2.32% |
  | Cooling & HVAC | $46.7B | $5.80B | 4.8% | 17.9% | 12.41% |
  | Building & Structure | $9.4B | $2.49B | 1.0% | 7.7% | 26.58% |

  Electrical Power and Cooling & HVAC together are 20.1% of AI-related imports
  and 69.9% of the duties; adding Building & Structure makes it 21.0% and
  77.6%. Compute Hardware and Networking & Telecom are 78.8% of the imports and
  22.2% of the duties. The two smallest categories (Fire Safety & Security,
  Specialty Materials) are in the denominators but not drawn; each is under
  0.2% of both. Non-AI imports over the same 12 months paid 10.25%.
- **A category is a tag on a product, not a record of where it went.** A
  transformer, a chiller or a battery is counted as AI-related because that
  kind of product is used in data centers. The data cannot say whether a given
  shipment was bound for one.
- **Electrical Power includes refined copper cathodes** (HTS 7403110000):
  $2.9B of the category's $14.3B in September 2026, at close to a zero tariff,
  and volatile around the 2025 copper tariff. Without that one line the
  `published` Electrical Power index for September 2026 is 124.0 rather than
  146.6 and its tariff rate 12.82% rather than 10.25%. (These figures, and the
  count of new codes above, come from the underlying HTS10 data; they cannot
  be recomputed from `data.csv`.)
- The effective tariff rate is calculated duties divided by customs value for
  goods entered in the month. It reflects exemptions, free-trade treatment and
  chapter-99 actions as actually applied, which is why it differs from
  statutory rates. Compute and networking hardware are largely covered by the
  2025 exemptions for semiconductors and electronics; power and cooling
  equipment largely are not. The data do not say which tariff action a duty
  was paid under.
- Nothing is seasonally adjusted. Chart 2 uses a 3-month average because
  cooling equipment is seasonal; its x-axis starts in March 2023, the first
  month the average exists.
- Charts carry a dashed rule at January 2025, the start of the 2025 tariff
  era, for orientation only.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
