"""Off-chain economic data: price, TVL, DEX volume and stablecoin supply.

All three sources expose free, keyless endpoints. Each is isolated so a single
provider outage degrades one section instead of the whole report.
"""

from typing import Any, Dict

from .. import config
from ..net import FetchError, request_json


def price() -> Dict[str, Any]:
    body = request_json(config.COINGECKO_URL)
    sol = body.get("solana", {})
    return {
        "usd": sol.get("usd"),
        "change_24h_pct": round(sol.get("usd_24h_change"), 2)
        if sol.get("usd_24h_change") is not None
        else None,
        "market_cap_usd": sol.get("usd_market_cap"),
        "volume_24h_usd": sol.get("usd_24h_vol"),
        "source": "coingecko",
    }


def tvl() -> Dict[str, Any]:
    chains = request_json(config.DEFILLAMA_CHAINS_URL)
    solana = next((c for c in chains if c.get("name") == "Solana"), None)
    if not solana:
        raise FetchError("Solana not present in DeFiLlama chain list")

    ranked = sorted(chains, key=lambda c: c.get("tvl") or 0, reverse=True)
    rank = next((i + 1 for i, c in enumerate(ranked) if c.get("name") == "Solana"), None)
    total = sum(c.get("tvl") or 0 for c in chains)
    value = solana.get("tvl") or 0
    return {
        "tvl_usd": round(value, 2),
        "rank_by_tvl": rank,
        "share_of_all_chains_pct": round(100 * value / total, 2) if total else None,
        "source": "defillama",
    }


def dex_volume() -> Dict[str, Any]:
    body = request_json(config.DEFILLAMA_DEX_URL)
    protocols = body.get("protocols") or []
    top = sorted(protocols, key=lambda p: p.get("total24h") or 0, reverse=True)[:5]
    return {
        "volume_24h_usd": body.get("total24h"),
        "volume_7d_usd": body.get("total7d"),
        "change_24h_pct": body.get("change_1d"),
        "protocol_count": len(protocols),
        "top_dexes": [
            {"name": p.get("name"), "volume_24h_usd": p.get("total24h")} for p in top
        ],
        "source": "defillama",
    }


def stablecoins() -> Dict[str, Any]:
    chains = request_json(config.DEFILLAMA_STABLES_URL)
    solana = next(
        (c for c in chains if (c.get("name") or "").lower() == "solana"), None
    )
    if not solana:
        raise FetchError("Solana not present in DeFiLlama stablecoin data")
    circulating = solana.get("totalCirculatingUSD") or {}
    return {
        "total_usd": round(sum(circulating.values()), 2) if circulating else None,
        "by_peg": {k: round(v, 2) for k, v in circulating.items()},
        "source": "defillama",
    }


def collect() -> Dict[str, Any]:
    out = {}
    for name, fn in (
        ("price", price),
        ("tvl", tvl),
        ("dex_volume", dex_volume),
        ("stablecoins", stablecoins),
    ):
        try:
            out[name] = fn()
        except FetchError as exc:
            out[name] = {"error": str(exc)}
    return out
