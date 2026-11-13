# Tariffs by end use: consumer, intermediate and capital goods, September 2026

Replication package for the two-post thread of **12 November 2026** (text and
links in `tweet.md`). Two charts were posted, one in each post:

| File | Post | What it shows |
|---|---|---|
| `chart_1_tariff_by_end_use.png` | 1 | Effective tariff rate (calculated duties ÷ customs value) on US imports of consumer, intermediate and capital goods, monthly |
| `chart_2_tariff_capital_ai_vs_other.png` | 2 | The same rate for consumer goods against capital goods split in two: AI-related capital goods and all other capital goods |

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

One row per group-month, January 2023 to September 2026, 225 rows (five groups,
45 months).

| Column | Meaning |
|---|---|
| `group` | `Consumer goods`, `Intermediate goods`, `Capital goods`, `AI-related capital goods` or `Other capital goods` |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | US imports from all countries, customs value, US dollars |
| `duties_usd` | Calculated duties on those imports, US dollars |
| `tariff_rate_pct` | `100 * duties_usd / imports_usd` |

`AI-related capital goods` plus `Other capital goods` equals `Capital goods` in
every month, for both dollars and duties.

**End use is the United Nations classification, applied by us.** Each product
is assigned to an end-use class by its first six HTS digits, using the UN's
Classification by Broad Economic Categories (BEC, Revision 5) and its
HS-to-BEC concordance. The mapping, and the notebook that builds it, are
public: [`hs6-enduse.parquet`](https://github.com/tradewartracker/trade-by-enduse/blob/main/data/hs6-enduse.parquet)
in the [trade-by-enduse](https://github.com/tradewartracker/trade-by-enduse)
repository.

- The mapping covers 5,387 six-digit codes: 3,246 intermediate, 1,441
  consumer, 698 capital, 2 unassigned.
- Some products are dual-classified in the concordance (for example
  `CAP/CONS`). They take the first class listed. This is a simplification, and
  it matters for a few large products: passenger cars are counted as consumer
  goods and much computer hardware as capital goods.
- HS chapters 98 and 99 (special provisions) are left out. Chapters 27
  (mineral fuels) and 71 (precious metals and stones) are kept, so the series
  here differ from the ones the trade-by-enduse repository publishes, which
  drop those two chapters as well.
- Six-digit codes that are not in the concordance carry no end-use class and
  are in none of the groups. In September 2026 the three classes cover 94.1%
  of import value ($318.5B of $338.6B, chapters 98 and 99 excluded). The rest
  ($20.1B) paid 5.3%.

**AI-related is our classification, not a Census category.** It comes from the
paper [Trade in AI-Related Products](https://www.minneapolisfed.org/research/quarterly-review/trade-in-ai-related-products),
which tags every 10-digit HTS code as High, Medium or Low relevance to AI data
center infrastructure. The tags, with the written reason for each code, are
public: [`hs10_classification_final_v3.csv`](https://github.com/tradewartracker/ai-trade-index/blob/main/data-input/hs10_classification_final_v3.csv).

- `AI-related capital goods` is every High-relevance HTS10 code whose
  six-digit code is a capital good.
- `Other capital goods` is every other capital good: Low relevance, Medium
  relevance, and codes with no tag.

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

- **The figures behind both charts:**

  | Group | Imports, Sep 2026 | Duties, Sep 2026 | Rate, Sep 2026 | Rate, 2024 | Rate, 2025 | Peak month |
  |---|---:|---:|---:|---:|---:|---|
  | Consumer goods | $68.6B | $8.27B | 12.06% | 3.80% | 12.49% | 17.09%, Sep 2025 |
  | Intermediate goods | $147.7B | $9.72B | 6.58% | 2.11% | 7.18% | 10.77%, Oct 2025 |
  | Capital goods | $102.2B | $3.88B | 3.79% | 1.55% | 5.12% | 7.79%, Sep 2025 |
  | AI-related capital goods | $67.0B | $1.00B | 1.49% | 1.36% | 2.86% | 3.91%, Sep 2025 |
  | Other capital goods | $35.2B | $2.88B | 8.17% | 1.64% | 6.96% | 12.19%, Jan 2026 |

  The 2024 and 2025 columns are the year's duties divided by the year's
  imports.
- **Chart 1.** Before 2025 the three classes sat between 1.5% and 4%, in the
  same order as now. In September 2026 consumer goods pay about three times
  the rate on capital goods. Over the latest 12 months (October 2025 to
  September 2026) the rates are 12.82%, 8.02% and 4.95%.
- **Chart 2.** The capital goods rate is an average of two very different
  groups. AI-related capital goods were 65.6% of capital goods imports in
  September 2026 (30.7% in 2023, 34.4% in 2024, 44.9% in 2025) and paid 1.49%.
  The other third paid 8.17%. Over the latest 12 months the two rates are
  2.01% and 9.32%.
- **Two products set the AI-related rate.** Servers (HS 847150) were $38.3B of
  the $67.0B in September 2026 and paid 0.06%; networking equipment
  (HS 851762) was $14.8B and paid 0.31%.
- **"Other" does not mean unrelated to computing.** Laptops (HS 847130, $5.2B
  in September 2026, 0.04%) are tagged Low relevance to data centers, so they
  are in `Other capital goods` and pull its rate down. By tag, September 2026:
  Low relevance $25.1B at 7.16%, Medium relevance $9.0B at 10.33%.
- **Some new 2026 codes are untagged.** Census replaced a number of HTS10
  codes during 2026 and the new codes are not in the classification file.
  Among capital goods that is $1.1B in September 2026, paying 13.47%. They are
  counted in `Other capital goods` even where the code they replaced was
  AI-related, so the AI-related line is slightly understated in value from
  February 2026.
- **End use is a tag on a product, not a record of who bought it.** A product
  is a capital good because that kind of product is mostly used as one. The
  data cannot say whether a given shipment went to a firm or a household.
- **The effective rate is not the statutory rate, and it is not who bears the
  cost.** It is calculated duties divided by customs value for goods entered
  in the month. It reflects exemptions, free-trade treatment and chapter-99
  actions as actually applied. It says what was collected at the border on
  each class of goods, not how much of that was passed on in prices. The data
  do not say which tariff action a duty was paid under.
- The product-level and tag-level figures above (servers, networking
  equipment, laptops, the Low and Medium split, the untagged codes) and the
  94.1% coverage come from the underlying HTS10 data; they cannot be
  recomputed from `data.csv`.
- Nothing is seasonally adjusted. Charts carry a dashed rule at January 2025,
  the start of the 2025 tariff era, for orientation only.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
