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
| 2026-10-08 | [`2026-10-08-ssd-imports`](2026-10-08-ssd-imports/) | US imports of solid-state storage (HS 852351): value, volume, unit value by source ([post 1](https://x.com/tradewartracker/status/2108203779187478987), [post 2](https://x.com/tradewartracker/status/2108203781565317196)) |
