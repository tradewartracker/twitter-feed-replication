# twitter-feed-replication

Data and code to replicate the charts posted on the
[@tradewartracker](https://tradewartracker.com) feed. One folder per post,
named by date. Each folder holds the tweet text, the images as posted, a
`data.csv` with exactly the series the charts draw, a standalone
`make_charts.py` that rebuilds them from that CSV, and a README with the
source, the Census data vintage and the caveats.

The scripts need only `pandas` and `matplotlib`:

```
cd 2026-10-08-ssd-imports
python make_charts.py
```

All data is from the US Census Bureau (monthly merchandise trade by HTS10 and
country) and is public domain. Code is MIT licensed (see `LICENSE`).

## Posts

| Date | Folder | Subject |
|---|---|---|
| 2026-10-07 | [`2026-10-07-laptops-vietnam-china`](2026-10-07-laptops-vietnam-china/) | US imports of laptops (HS 847130) from Vietnam vs China: value and effective tariff rate ([post 1](https://x.com/tradewartracker/status/2107861273492799888), [post 2](https://x.com/tradewartracker/status/2107861276214878562)) |
| 2026-10-08 | [`2026-10-08-ssd-imports`](2026-10-08-ssd-imports/) | US imports of solid-state storage (HS 852351): value, volume, unit value by source ([post 1](https://x.com/tradewartracker/status/2108203779187478987), [post 2](https://x.com/tradewartracker/status/2108203781565317196)) |
| 2026-10-09 | [`2026-10-09-servers-mexico`](2026-10-09-servers-mexico/) | US imports of servers (HS 847150): total vs top sources, and Mexico's server line vs its whole vehicle chapter (HS 87) ([post 1](https://x.com/tradewartracker/status/2108566699138335228), [post 2](https://x.com/tradewartracker/status/2108566700719538300)) |
| 2026-10-13 | [`2026-10-13-memory-modules`](2026-10-13-memory-modules/) | US imports of memory modules and computer parts (HS 847330): total value, unit value of all imports, top 3 sources ([post 1](https://x.com/tradewartracker/status/2110016882522706260), [post 2](https://x.com/tradewartracker/status/2110016885656076587); [post 3](https://x.com/tradewartracker/status/2110037288176833001) carried an IMF WEO figure, not replicated) |
| 2026-10-14 | [`2026-10-14-thailand`](2026-10-14-thailand/) | US imports from Thailand: total, six datacenter product lines vs everything else, and the effective tariff rate on each ([post 1](https://x.com/tradewartracker/status/2110369861356646724), [post 2](https://x.com/tradewartracker/status/2110369864842195045)) |
| 2026-10-15 | [`2026-10-15-smartphones-india`](2026-10-15-smartphones-india/) | US smartphone imports (HS 851713): total with yearly averages, trailing-12-month share from India, Vietnam and China, and the effective tariff rate each source pays ([post 1](https://x.com/tradewartracker/status/2110740499980079587), [post 2](https://x.com/tradewartracker/status/2110740503473918135)) |
| 2026-10-16 | [`2026-10-16-cars-japan`](2026-10-16-cars-japan/) | US passenger-car imports (HS 8703): number of cars with yearly averages, the effective tariff rate, cars from Japan, and the average customs value of a car from Japan ([post 1](https://x.com/tradewartracker/status/2111112695101391296), [post 2](https://x.com/tradewartracker/status/2111112696900755605), [post 3](https://x.com/tradewartracker/status/2111112699874816035), [post 4](https://x.com/tradewartracker/status/2111112702290477501)) |
| 2026-11-06 | [`2026-11-06-ai-trade-index`](2026-11-06-ai-trade-index/) | The AI trade index: US imports of AI-related vs non-AI products (index, 2023 = 100), electrical power and cooling equipment against non-AI, the effective tariff rate by AI category, and each category's share of AI-related imports vs its share of the tariffs paid ([post 1](https://x.com/tradewartracker/status/2118724557028704694), [post 2](https://x.com/tradewartracker/status/2118724558957990339), [post 3](https://x.com/tradewartracker/status/2118724561969836159), [post 4](https://x.com/tradewartracker/status/2118724564330938720); [post 5](https://x.com/tradewartracker/status/2118724567418163581) carried links only) |
