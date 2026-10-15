# US smartphone imports: the rotation from China to India, August 2026

Replication package for the two-post thread of **15 October 2026** (text and
links in `tweet.md`). Three charts were posted, two in the first post and one
in the reply:

| File | Post | What it shows |
|---|---|---|
| `chart_1_total_imports.png` | 1 | All US smartphone imports, monthly, customs value, with each calendar year's average monthly value drawn as a dashed segment |
| `chart_2_share_12m.png` | 1 | India's, Vietnam's and China's share of US smartphone imports over the trailing 12 months |
| `chart_3_tariff_by_source.png` | 2 | Effective tariff rate (calculated duties ÷ customs value) on smartphones from all sources and from each of the three |

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

One row per source-month, January 2023 to August 2026, 176 rows.

| Column | Meaning |
|---|---|
| `source` | `all` (every source country, the Census total), `india`, `vietnam` or `china` |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | General imports of HTS 8517.13.0000 (smartphones), customs value, US dollars |
| `duties_usd` | Calculated duties on those imports, US dollars |
| `tariff_rate_pct` | `100 * duties_usd / imports_usd` |
| `share_12m_pct` | The source's imports over the trailing 12 months as a percent of `all` over the same 12 months. Empty for `all` and for the first eleven months, which have no full window |

**Smartphones are one HTS line.** HS 851713 ("smartphones for cellular
networks or other wireless networks") has a single 10-digit code, 8517.13.0000,
so there is no product mix inside the series. The code was created in the 2022
HS revision; before that smartphones sat inside 8517.12, which is why the
charts start in 2023. India, Vietnam and China together are 96% of August
2026 imports; the `all` row is the Census total, not the sum of the three.

## Source and vintage

- **US Census Bureau**, monthly merchandise trade by HTS10 and country
  (the data behind the FT900 release and USA Trade Online), general imports,
  customs value and calculated duties.
- **Vintage:** the August 2026 release (FT900 published 6 October 2026),
  pulled on 2026-10-06. Earlier months carry the revisions published through
  that release. Census revises monthly data, so a fresh pull will not match
  this file exactly.
- Values and duties are the Census total row for each line, not the sum of
  rate-provision components.

## How to read it, and what it cannot tell you

- **The total has not moved.** Average monthly imports were $4.67B in 2023,
  $4.68B in 2024, $4.90B in 2025 and $4.63B so far in 2026 (January to
  August). Annual totals: $56.1B, $56.1B, $58.9B. The chart deliberately
  carries no year-on-year figure: August 2026 is $5.1B against $2.7B in
  August 2025, a +91% that reflects the trough of the tariff hit, not growth.
- **The month-to-month swings are launch seasonality.** Shipments from China
  peaked each autumn (October 2024 was $6.6B, the highest month in the
  file), and the same shape appears in 2023. Read the dashed yearly
  segments, not the peaks.
- **The rotation, on trailing-12-month shares:** China was 78% of US
  smartphone imports in calendar 2023 and 73% in 2024; it is 32% in the
  twelve months to August 2026. India went from 8% to 12% to 44%, Vietnam
  from 12% to 14% to 19%. India's trailing share first exceeded China's in
  January 2026 and peaked at 47% in April 2026. On the single month of
  August 2026 the shares are India 44%, Vietnam 32%, China 20%.
- **Imports from China collapsed, then partly came back.** They averaged
  $3.4B a month in 2024, $0.5B a month from April to August 2025, and $1.0B
  a month so far in 2026. India averaged $0.6B a month in 2024 and $2.3B so
  far in 2026.
- **The tariff lines differ because of which tariff applied.** Smartphones
  were exempted from the April 2025 reciprocal ("Liberation Day") tariffs,
  but that exemption did not cover the IEEPA fentanyl tariff on China. So
  phones from China paid about 19% from March to October 2025 (the fentanyl
  tariff at 20%), about 11% from November 2025 to January 2026 after the
  rate was halved, and effectively nothing from March 2026, when it was
  removed. India and Vietnam never paid more than a fraction of a point
  (India's highest month was 2.0% in December 2025). Of the $3.0B of duties
  collected on smartphones in 2025, $2.96B was on phones from China.
- **The all-sources line is mostly mix.** It peaked at 12.4% in September
  2025 not because any rate rose but because China's launch-season shipments
  temporarily lifted China's share of the month's imports.
- The effective tariff rate is calculated duties divided by customs value
  for goods entered in the month. It reflects exemptions and chapter-99
  actions as actually applied, which is why it differs from statutory rates.
- The total chart starts in 2023. The share and tariff charts start in 2024:
  the share needs a full 12-month window (the first ends December 2023) and
  nothing happens on the tariff chart before 2025. All three carry a dashed
  rule at January 2025, the start of the 2025 tariff era, for orientation.
- Not in the charts or in `data.csv`, but from the same Census release
  (value divided by the reported number of units): India ships the more
  expensive phones. In August 2026 the average customs value per phone was $593 from
  India, $405 from Vietnam and $336 from China.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
