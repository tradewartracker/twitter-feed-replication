# US imports from Thailand: datacenter hardware vs everything else, August 2026

Replication package for the two-post thread of **14 October 2026** (text and
links in `tweet.md`). Three charts were posted, two in the first post and one
in the reply:

| File | Post | What it shows |
|---|---|---|
| `chart_1_total_imports.png` | 1 | All US imports from Thailand, monthly, customs value |
| `chart_2_datacenter_vs_other.png` | 1 | The same imports split into six datacenter product lines and everything else |
| `chart_3_tariff_three_lines.png` | 2 | Effective tariff rate (calculated duties ÷ customs value) on the total and on each group |

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

One row per group-month, January 2023 to August 2026, 132 rows.

| Column | Meaning |
|---|---|
| `group` | `all` (every HTS10 line imported from Thailand), `datacenter` (the six lines below) or `other` (every line not in those six) |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | General imports from Thailand, customs value, US dollars |
| `duties_usd` | Calculated duties on those imports, US dollars |
| `tariff_rate_pct` | `100 * duties_usd / imports_usd` |

`all` equals `datacenter` plus `other` in every month, for both dollars and
duties. The `all` tariff rate is therefore the value-weighted average of the
other two.

**The "datacenter hardware" group is our basket, not a Census category.** It
is every HTS10 line whose first six digits are one of:

| HS6 | What it is | Imports from Thailand, Sep 2025 to Aug 2026 |
|---|---|---|
| 851762 | Networking and telecom equipment (switches, routers, modems) | $30.4B, +124% |
| 847150 | Servers and other processing units sold without a complete system | $24.1B, +1,200% (from $1.9B) |
| 847170 | Hard disk drives and other storage units | $9.3B, +46% |
| 847130 | Laptops and portable computers | $5.8B, +124% |
| 847330 | Memory modules and other computer parts | $3.5B, +221% |
| 852351 | Solid-state storage (SSDs, flash) | $3.4B, +341% |

These six were chosen because they are the six biggest lines in Thailand's
year-on-year growth. Thailand is 42% of US hard-drive imports and 26% of US
networking-equipment imports.

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

- Headline figures for August 2026: all imports from Thailand $11.8B
  (+60.5% YoY); datacenter hardware $7.2B (+129.0%); everything else $4.7B
  (+9.9%). Over the last 12 months the datacenter group is $76.4B against
  $26.2B in the prior 12, and the rest is $52.5B against $50.5B.
- **The datacenter share of Thailand's shipments went from about a fifth to
  three fifths.** It averaged 22% of the total in 2023, was 42% in August
  2025 and 61% in August 2026. The crossover month, when datacenter hardware
  first exceeded everything else, was October 2025.
- **Effective tariff, August 2026:** all imports 5.8%, datacenter hardware
  0.3%, everything else 14.3%. A year earlier the three were 8.2%, 0.1% and
  14.2%. The "everything else" rate peaked at 20.9% in January 2026 and
  stepped down to around 14% from March 2026; the total peaked at 10.1% in
  the same month.
- **Most of the fall in Thailand's headline rate is mix, but not all of it.**
  Holding each group's August 2026 rate fixed, the headline rate at the
  August 2025 shares would be about 8.4% rather than 5.8%, so the shift
  toward zero-tariff goods accounts for most of the decline on the year. The
  early-2026 drop in the "everything else" line from 21% to 14% is a real
  change in the rate paid on that basket, not mix.
- **"Everything else" is a long tail, not one product.** Its largest line is
  under 6% of it. The biggest, over the last 12 months: motor drives and
  inverters ($3.0B, 12.9% tariff), car and light-truck tires ($2.9B, 28%,
  down 18 to 30% YoY), security cameras ($1.2B, 13.6%), air conditioners
  and coils ($1.7B, 20%), dog and cat food ($1.0B, 13.8%), rice ($0.8B,
  14.5%), printers ($0.8B, 13.8%), compact refrigerators ($0.7B, 23.6%),
  silver and gold jewelry ($1.1B, 18 to 19%), canned tuna ($0.5B, 24.8%).
  It also holds some electronics outside the six lines, notably computer
  monitors ($0.7B, +286%, 0% tariff), so it is not purely "low-tech".
- The effective tariff rate is calculated duties divided by customs value
  for goods entered in the month. It reflects exemptions, free-trade
  treatment and chapter-99 actions as actually applied, which is why it
  differs from statutory rates. Datacenter hardware is largely exempt from
  the 2025 reciprocal tariffs (the semiconductor and electronics
  exemptions), which is the gap between the blue line and the red one.
- Charts start in 2023 and carry a dashed rule at January 2025, the start of
  the 2025 tariff era, for orientation only.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
