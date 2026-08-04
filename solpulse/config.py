"""Configuration. Every value can be overridden by an environment variable so
the collector runs unchanged in cron, systemd, or a CI schedule."""

import os
from typing import List

# Public mainnet RPC. Swap for a private endpoint via SOLPULSE_RPC_URL when
# running frequently -- the public node rate-limits aggressively.
RPC_URL = os.environ.get("SOLPULSE_RPC_URL", "https://api.mainnet-beta.solana.com")

# Fallbacks tried in order if the primary RPC fails or reports unhealthy.
RPC_FALLBACKS: List[str] = [
    u for u in os.environ.get("SOLPULSE_RPC_FALLBACKS", "").split(",") if u
] or ["https://solana-rpc.publicnode.com"]

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=solana&vs_currencies=usd"
    "&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"
)
DEFILLAMA_CHAINS_URL = "https://api.llama.fi/v2/chains"
DEFILLAMA_DEX_URL = (
    "https://api.llama.fi/overview/dexs/solana"
    "?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true"
)
DEFILLAMA_STABLES_URL = "https://stablecoins.llama.fi/stablecoinchains"
DEFILLAMA_FEES_URL = (
    "https://api.llama.fi/overview/fees/solana"
    "?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true"
)
# ~8 MB. Cached rather than refetched every run -- see net.request_json_cached.
DEFILLAMA_PROTOCOLS_URL = "https://api.llama.fi/protocols"
PROTOCOLS_CACHE_TTL = int(os.environ.get("SOLPULSE_PROTOCOLS_TTL", "21600"))  # 6h

# The public, keyless API behind solana.com/data. Republishes metrics from 13
# providers including Dune, with per-row provider attribution.
SOLANA_DATA_URL = "https://solana.com/api/databricks/data?days={}".format(
    os.environ.get("SOLPULSE_ECOSYSTEM_DAYS", "90")
)
SOLANA_DATA_CACHE_TTL = int(os.environ.get("SOLPULSE_ECOSYSTEM_TTL", "21600"))  # 6h
# History points embedded per ecosystem metric. Enough for a readable sparkline
# without inflating report.json, which is committed on every refresh.
ECOSYSTEM_SERIES_POINTS = int(os.environ.get("SOLPULSE_ECOSYSTEM_SERIES_POINTS", "30"))
# Relative spread between providers measuring the same metric on the same day
# before it is reported as a divergence.
DIVERGENCE_THRESHOLD = float(os.environ.get("SOLPULSE_DIVERGENCE_THRESHOLD", "0.15"))

# Official Solana news feed (RSS, keyless).
SOLANA_NEWS_URL = "https://solana.com/news/rss.xml"
NEWS_CACHE_TTL = int(os.environ.get("SOLPULSE_NEWS_TTL", "3600"))
NEWS_ITEMS = int(os.environ.get("SOLPULSE_NEWS_ITEMS", "8"))

# Recent blocks sampled to estimate active addresses, and how far apart they sit.
# Spacing them spreads the sample over time instead of one contiguous burst.
ADDRESS_SAMPLE_BLOCKS = int(os.environ.get("SOLPULSE_ADDRESS_SAMPLE_BLOCKS", "3"))
ADDRESS_SAMPLE_SPACING = int(os.environ.get("SOLPULSE_ADDRESS_SAMPLE_SPACING", "1500"))

# How many 60-second performance samples to average TPS over.
PERF_SAMPLE_COUNT = int(os.environ.get("SOLPULSE_PERF_SAMPLES", "5"))

# Seconds between refreshes in --watch mode.
REFRESH_INTERVAL = int(os.environ.get("SOLPULSE_REFRESH_INTERVAL", "300"))

OUTPUT_DIR = os.environ.get("SOLPULSE_OUTPUT_DIR", "output")
HISTORY_PATH = os.environ.get("SOLPULSE_HISTORY_PATH", "output/history.jsonl")

# Retained history points used as the baseline for anomaly detection.
HISTORY_WINDOW = int(os.environ.get("SOLPULSE_HISTORY_WINDOW", "288"))
