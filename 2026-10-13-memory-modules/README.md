# US imports of memory modules and computer parts (HS 847330), August 2026

Replication package for the three-post thread of **13 October 2026** (text and
links in `tweet.md`). Three charts were posted, two in the first post and one
in the first reply. The second reply carried a figure from the IMF's October
2026 World Economic Outlook, which is the IMF's own chart and is not
replicated here.

| File | Post | What it shows |
|---|---|---|
| `chart_1_total_value.png` | 1 | Total US imports of HS 847330, monthly, customs value |
| `chart_2_unit_value_all_sources.png` | 1 | Unit value (value ÷ Census quantity) of all US imports of the line |
| `chart_3_top_3_sources.png` | 2 | Customs value of imports from the three largest source countries |

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

One row per entity-month, January 2023 to August 2026, 176 rows.

| Column | Meaning |
|---|---|
| `entity` | `TOTAL FOR ALL COUNTRIES` (Census's published total) or the source country |
| `month` | Calendar month, `YYYY-MM` |
| `imports_usd` | General imports, customs value, US dollars |
| `quantity` | Census first quantity, summed over the HTS10 lines |
| `unit` | Census unit of quantity (`NO` = number of units) |
| `unit_value_usd` | `imports_usd / quantity` |

Chart 3 draws Vietnam, Taiwan and South Korea, the three largest sources by
August 2026 value. Malaysia, the fourth at $2.1B, was left off. The total is
Census's own all-countries figure, not a sum of the countries shown. South
Korea is drawn gold because its flag blue is the same blue as Taiwan's.

## Source and vintage

- **US Census Bureau**, monthly merchandise trade by HTS10 and country
  (the data behind the FT900 release and USA Trade Online), general imports.
- **Vintage:** the August 2026 release (FT900 published 6 October 2026),
  pulled on 2026-10-06. Earlier months carry the revisions published through
  that release. Census revises monthly data, so a fresh pull will not match
  this file exactly.
- **Product:** every HTS10 line whose first six digits are 847330, "parts and
  accessories of automatic data processing machines" (parts of computers,
  excluding the computers themselves). Values are the Census total row for
  each line, not the sum of rate-provision components. Every line under the
  HS6 reports quantity in number of units, and in August 2026 every dollar of
  value carried a quantity, which is the condition for the unit value to be
  printed at all.

## How to read it, and what it cannot tell you

- Headline figures for August 2026: total imports $16.9B (+211.0% YoY),
  44.1M units (+32.8%), unit value $383 per unit (+134.2%). Dollars rose about
  three times as fast as units, which is the point of post 1. Chart 3's
  sources: Vietnam $5.2B (+430.6%), Taiwan $4.5B (+77.9%), South Korea $2.5B
  (+247.4%). Vietnam was the largest source in June and again in August
  2026; Taiwan was ahead in July. The two have traded places month to month
  since mid-2026.
- **Unit value is an average transaction value, not a price index.** It is
  total dollars divided by total units. It moves when prices change and also
  when the mix of goods changes, and one HTS10 line can mix grades.
- **"Mostly memory modules" is true of the dollars.** HS 847330 has five
  HTS10 lines. The memory-module line, 8473.30.1140, was 66% of August 2026
  value, and the next line, 8473.30.1180 (other printed circuit assemblies for
  computers: boards, not DIMMs), was 29%. The remaining three lines, which are
  mostly mechanical parts at $40 to $100 a unit, were about 5% of value but
  about a third of units. So the all-sources unit value in chart 2 is pulled
  down by a large count of cheap parts; the memory-module line on its own
  averaged $528 per unit in August 2026.
- **The three sources do not ship the same thing.** South Korea's line is
  essentially all memory modules (99.8% of its value). Vietnam's is 87% memory
  modules. Taiwan's is 83% the "other printed circuit assemblies" line at
  about $2,600 a unit and only 12% memory modules. Taiwan's share of chart 3,
  and its contribution to the unit value in chart 2, is therefore mostly
  boards rather than DIMMs.
- **South Korea's August 2026 quantity looks like a reporting artifact.**
  Korea's memory-module line reports 12.1M units in August against 2.4M in
  July and 3.1M in June, on fewer dollars ($2.5B vs $3.5B). Its unit value
  drops from $1,458 to $205 as a result. That one line is enough to move the
  all-sources unit value: the total was $548 in July and $383 in August;
  computed from `data.csv` with South Korea removed it is $478 in July and
  $450 in August, a far smaller dip. The all-sources series in chart 2
  therefore understates the latest month, and most of the July-to-August
  fall should not be read as a price fall. None of this affects the dollar
  series in charts 1 and 3. Census may revise the quantity in a later
  release.
- Charts start in 2023 and carry a dashed rule at January 2025, the start of
  the 2025 tariff era, for orientation only. The effective tariff on HS
  847330 was 0.2% in August 2026 (down 1.1 points on the year); tariffs are
  not the story here.

Charts are in the house style of [tradewartracker.com](https://tradewartracker.com).
