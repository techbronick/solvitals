# SolVitals — submission

**Repo:** https://github.com/techbronick/solvitals
**Live dashboard:** https://techbronick.github.io/solvitals/
**Sample outputs:** [`docs/report.md`](https://github.com/techbronick/solvitals/blob/main/docs/report.md) · [`docs/report.json`](https://github.com/techbronick/solvitals/blob/main/docs/report.json)

---

SolVitals is an auto-updating report on the state of the Solana ecosystem. One
command collects on-chain and economic data, checks it for anomalies, and writes
an interactive dashboard, a Markdown report and structured JSON.

It runs on the **Python standard library alone** — no pip install, no API keys,
no accounts. Clone and run. The live dashboard above refreshes itself every 15
minutes through GitHub Actions with no server involved.

```bash
git clone https://github.com/techbronick/solvitals && cd solvitals
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
broken out separately**, with xStocks and Ondo Global Markets identified as
the equity issuers. Live figures are in the linked report rather than quoted
here, so this document cannot go stale.

**Ecosystem growth (solana.com/data):** daily active addresses, daily fee
payers, transaction counts split by vote/non-vote and success/failure, DEX
volume and traders, transfer volume, total stake, validator count, Top-3 ASN
share — each with 30 days of history and per-metric provider attribution.

**News (solana.com/news RSS):** latest ecosystem and community announcements.

**Upcoming upgrades (SIMD repo + Agave + live RPC):** all 123 improvement
proposals with status breakdown, the 25 carrying feature gates, and live
activation state for each gate across mainnet, testnet and devnet — plus
per-cluster Agave versions.

**Address activity (Solana JSON-RPC):** live unique signers sampled from recent
blocks, signers per block, non-vote transaction share.

## Three judgement calls worth explaining

**Non-vote TPS leads, not raw TPS.** Solana counts consensus votes as
transactions, so raw TPS runs well above the figure people mean -- about 1.8x
at the time of writing. Both are reported; the honest one is the headline.

**Tokenized equities are separated from RWA.** The RWA category is dominated by
treasuries and private credit — BlackRock BUIDL alone is $676M — so a single RWA
total buries what's happening in equities. Equity issuers are identified,
tagged in the dashboard, and reported both absolutely and as a share.

**Fees are labelled the fee component of REV, not REV.** REV conventionally
includes out-of-protocol MEV tips. I checked whether Jito's API could supply
them keylessly: it responds without a key, but ignores the epoch parameter and
returns zeroed reward fields, so the data isn't retrievable. Rather than present
fees as full REV, the report says exactly what it measured.

**Two active-address numbers, not one.** Daily active addresses come from
solana.com's feed, deduplicated across the full day by the provider .
Sampled live signers come from `getBlock` and measure who is transacting *right
now* — which the daily figure can't show, because it lags a day. Both are
reported, each labelled for what it is. Collapsing them into one number would
have meant either a stale figure presented as live, or a sample presented as a
daily count.

## Multi-source correlation: where providers disagree

solana.com's feed carries the same metric from several providers, and their
methodologies don't agree. Rather than silently picking one, the collector flags
any metric where same-day readings diverge past a threshold.

This is live, not theoretical. Dune and Allium currently differ materially on daily active addresses. DEX
volume is deliberately excluded from this check -- providers there count
entirely different venue sets, so the gap reflects scope, not methodology, and
reporting it as a disagreement would be noise. A dashboard reporting a single number without that
caveat is quietly misleading, and the disagreement is genuinely more informative
than either figure alone.

## Tracking upgrades to actual activation

The brief names Alpenglow and SIMD-525 under "upcoming upgrades". Rather than
hardcode a list that goes stale, this joins the SIMD repository, Agave's
feature-set source, and `getMultipleAccounts` against three clusters — so it
reports what is genuinely switched on where, and keeps working as new proposals
land.

It surfaces two things a static list wouldn't. Mainnet is running a different
Agave version from testnet and devnet, which is a rollout in progress. And
Alpenglow has **no feature gate assigned on any cluster** — it isn't merely
pending, it hasn't reached the point of being switchable at all. That's a more
precise and more useful statement than "coming soon".

(Small note: the brief writes SIMD-525; the repo zero-pads, so it's SIMD-0525,
"Reduce Slot Times", currently Draft.)

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

## On Dune, and on Twitter

**Dune is covered, without a key.** Dune's own API is hard-closed — `api.dune.com`
returns 401, embed routes hit a Cloudflare challenge, and the cheapest API tier
is $399/month. But solana.com's data feed *republishes Dune-computed metrics
keylessly* with per-row provider attribution, so Dune-sourced figures (including
the headline daily active addresses number) are ingested and labelled as such.

**X/Twitter is covered, keylessly.** X has no free API, but the public
syndication endpoint that renders embedded timelines returns recent posts with
no key and no account. It rate-limits roughly one request in five — which is
exactly the failure profile the per-collector isolation was built for, so a miss
costs this section alone and the cached copy is reused. Announcements from
@solana, @solanalabs and @SuperteamDAO are pulled; replies and retweets are
filtered out. Other keyless routes were tested and are genuinely dead:
nitter.poast.org 403, xcancel.com returns a not-whitelisted stub, nitter.net
returned a 0-byte body.

I deliberately do **not** attempt sentiment scoring. Without a model, that would
be keyword counting presented as analysis, and the announcements themselves are
the honest deliverable.

## Honest notes for the sponsor

A few things I ran into that are worth knowing regardless of who wins:

- **`getRecentPerformanceSamples` is easy to misread.** It counts vote
  transactions, so naive TPS reporting overstates user activity by nearly 2x.
  Several public Solana dashboards quote the inflated figure.
- **Provider disagreement on core metrics is larger than I expected** — 25% on
  daily active addresses between two reputable providers. Anyone building
  ecosystem reporting should treat single-source numbers with suspicion.
- **The bounty references "SIMD-525"**; the repo zero-pads to four digits, so
  the proposal is SIMD-0525. Minor, but it makes searching harder.
- **The brief's "autonomous agent concept of SolPulse"** has no single canonical
  referent I could find — the name is shared by a faucet token, a trading-bot
  site, several dashboards and a musician. I built to the described behaviour
  (self-scheduling, self-publishing, judgment layer) rather than to any one
  product.
- **The public mainnet RPC rate-limits hard** under a 15-minute cadence from
  shared CI IPs. Anyone deploying this pattern should budget for a private
  endpoint.
