# US imports of laptops and portable computers (HS 847130): Vietnam vs China

Replication package for the two-post thread of **7 October 2026** (text and
links in `tweet.md`). One chart per post:

| File | Post | What it shows |
|---|---|---|
| `chart_1_imports_vietnam_vs_china.png` | 1 | Monthly US imports of HS 847130 from Vietnam and from China, customs value |
| `chart_2_tariff_vietnam_vs_china.png` | 2 | Effective tariff rate (calculated duties ÷ customs value) on those same shipments |

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

One row per country-month, January 2023 to August 2026.

| Column | Meaning |
|---|---|
| `entity` | `VIETNAM` or `CHINA` |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | General imports, customs value, US dollars |
| `duty_usd` | Calculated duties, US dollars (Census's estimate of duty owed on these entries) |
| `tariff_rate_pct` | `100 * duty_usd / imports_usd` |

## Source and vintage

- **US Census Bureau**, monthly merchandise trade by HTS10 and country
  (the data behind the FT900 release and USA Trade Online), general imports
  and calculated duties.
- **Vintage:** the August 2026 release (FT900 published 6 October 2026),
  pulled on 2026-10-06. Earlier months carry the revisions published through
  that release. Census revises monthly data, so a fresh pull will not match
  this file exactly.
- **Product:** every HTS10 line whose first six digits are 847130 (portable
  automatic data processing machines weighing not more than 10 kg: laptops,
  notebooks, tablets). Values are the Census total row for each line, not the
  sum of rate-provision components.

## How to read it, and what it cannot tell you

- **The effective tariff rate is realised, not statutory.** It is the duty
  Census calculates on the entries that actually cleared, divided by their
  value. It falls when an exemption applies, when goods enter under a
  provision that carries no duty, or when the mix of entries shifts. It is
  not the headline rate in any proclamation.
- **China's rate was 0% in January 2025, 13% by March, between 16% and 19%
  from April to October 2025, then stepped down (13% in November, 9.5% in
  December) and has been about 0.2% since April 2026.** Vietnam's never
  exceeds 0.7%. Both series are in `data.csv` month by month.
- **The value chart shows the shift, not its cause.** US imports from Vietnam
  rose from about $0.3B a month in early 2023 to about $3.5B by August 2026,
  while imports from China fell from about $2.8B a month to under $0.5B. Trade
  data records the country of origin declared at entry. Whether that reflects
  relocated assembly, routing of Chinese-made goods, or both, is not something
  this series can settle on its own.
- Charts start in 2023 and carry a dashed rule at January 2025, the start of
  the 2025 tariff era, for orientation only.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
