# SolPulse — submission

**Repo:** https://github.com/techbronick/solpulse
**Live dashboard:** https://techbronick.github.io/solpulse/
**Sample outputs:** [`docs/report.md`](https://github.com/techbronick/solpulse/blob/main/docs/report.md) · [`docs/report.json`](https://github.com/techbronick/solpulse/blob/main/docs/report.json)

---

SolPulse is an auto-updating report on the state of the Solana ecosystem. One
command collects on-chain and economic data, checks it for anomalies, and writes
an interactive dashboard, a Markdown report and structured JSON.

It runs on the **Python standard library alone** — no pip install, no API keys,
no accounts. Clone and run. The live dashboard above refreshes itself every 15
minutes through GitHub Actions with no server involved.

```bash
git clone https://github.com/techbronick/solpulse && cd solpulse
python3 main.py && open output/index.html
```

## What it covers

**On-chain (Solana JSON-RPC):** non-vote and total TPS, average slot time, block
height, current slot, epoch progress with time-to-completion, active and
delinquent validator counts, delinquent *stake*, total active stake, Nakamoto
coefficient, median and zero commission counts, top validators by stake,
circulating vs total supply, node health.

**Economic (CoinGecko, DeFiLlama):** SOL price with 24h change, market cap, DeFi
TVL and cross-chain rank, DEX volume with top venues, stablecoin supply by peg,
network fees across 24h/7d/30d with an annualised run-rate and top fee earners.

**Tokenized assets (DeFiLlama):** total tokenized RWA on Solana with **equities
broken out separately** — currently $394M across xStocks and Ondo Global
Markets, 22% of a $1.78B RWA total.

**Address activity (Solana JSON-RPC):** unique fee payers sampled from recent
blocks, signers per block, non-vote transaction share.

## Three judgement calls worth explaining

**Non-vote TPS leads, not raw TPS.** Solana counts consensus votes as
transactions, so raw TPS runs roughly 1.5× the figure people mean. Both are
reported; the honest one is the headline.

**Tokenized equities are separated from RWA.** The RWA category is dominated by
treasuries and private credit — BlackRock BUIDL alone is $676M — so a single RWA
total buries what's happening in equities. Equity issuers are identified,
tagged in the dashboard, and reported both absolutely and as a share.

**Fees are labelled the fee component of REV, not REV.** REV conventionally
includes out-of-protocol MEV tips. I checked whether Jito's API could supply
them keylessly: it responds without a key, but ignores the epoch parameter and
returns zeroed reward fields, so the data isn't retrievable. Rather than present
fees as full REV, the report says exactly what it measured.

The same principle governs address activity. A true daily-unique-address count
requires deduplicating signers across ~216,000 blocks — no keyless source
exposes it, and extrapolating a sample overcounts badly because active addresses
recur across blocks all day. So the report gives unique fee payers across a
configurable sample and labels it an activity indicator, not a 24h count. I'd
rather ship a number that's true than one that's impressive.

## Automation

Three deployment shapes, documented with working config:

1. **GitHub Actions → Pages** — what's running now. Refreshes every 15 minutes,
   commits output, redeploys. No server. History accumulates in a committed
   JSONL file so anomaly baselines and sparklines survive across ephemeral
   runners.
2. **systemd** — unit file included for a long-running watch process.
3. **cron** — single-run invocation for periodic refresh.

Refresh interval, RPC endpoints, sample widths, cache TTL and output paths are
all environment variables, so the same code runs unchanged in every shape.

## Maintainability

**Failures are isolated per source.** A DeFiLlama outage costs one section, not
the run — the rest renders and the failed section reports why. RPC calls fail
over to secondary endpoints; transport errors and 429/5xx retry with backoff.

**Caching where it matters.** DeFiLlama's protocol list is ~8MB and its RWA
figures move daily. Refetching that every 15 minutes would dominate runtime and
abuse a free API, so it's cached with a 6-hour TTL, atomic writes, and a
*stale-cache fallback* when the network call fails.

**Collectors don't know about renderers.** Both sides talk through a plain
snapshot dict, so adding a data source or an output format touches one file.

## Anomaly detection

Two complementary checks, because either alone has a blind spot — fixed
thresholds miss a TVL collapse that stays numerically large, and z-scores stay
quiet when a metric is consistently bad.

- **Absolute thresholds:** delinquent validators, slot time, non-vote TPS,
  Nakamoto coefficient, RPC health.
- **Statistical deviation:** 2σ warning / 3σ critical against each metric's own
  trailing mean, across eight series. Requires 8 history points before firing,
  so a fresh install doesn't alarm on itself.

The current reading is appended to history *after* detection, so a value is
never part of the baseline it's measured against. Findings sort most-severe
first and lead both outputs — if something is wrong it should be the first thing
you read.

## Presentation

Dark theme by default with a working light mode — separately chosen steps
validated against the light surface, not an automatic inversion. Sparklines on
every historical series with hover crosshair, value and timestamp. A tile with
fewer than two readings says so rather than drawing a misleading flat line.
Severity is always paired with a text label, and every tile value also appears
in a full metrics table, so nothing depends on colour alone. Fully
self-contained: no CDN, no fonts, no network calls at view time.

## Not covered

Dune-sourced metrics and Twitter sentiment. Dune's API returns 401 without a key
and starts at $399/month, which conflicts with the no-API-key preference. I chose
to go deeper on keyless sources rather than add a paid dependency — but if a Dune
key is acceptable, the collector interface is a single function returning a dict,
so it slots in without touching anything else.
