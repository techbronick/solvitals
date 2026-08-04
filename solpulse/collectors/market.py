"""Off-chain economic data: price, TVL, DEX volume and stablecoin supply.

All three sources expose free, keyless endpoints. Each is isolated so a single
provider outage degrades one section instead of the whole report.
"""

from typing import Any, Dict

from .. import config
from ..net import FetchError, request_json, request_json_cached

# Categories DeFiLlama uses for tokenized real-world assets.
RWA_CATEGORIES = ("RWA", "RWA Lending")

# Protocols that tokenize listed equities specifically, as opposed to treasuries,
# credit or commodities. The bounty asks for equities in particular, and the
# category alone doesn't separate them.
EQUITY_PROTOCOLS = ("xstocks", "ondo global markets", "remora", "swarm")


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


def fees() -> Dict[str, Any]:
    """Network fees -- the fee half of Real Economic Value.

    REV is conventionally fees plus out-of-protocol MEV tips (Jito). Tip data
    isn't available without a keyed source, so what's reported here is the fee
    component, labelled as such rather than passed off as full REV.
    """
    body = request_json(config.DEFILLAMA_FEES_URL)
    total_24h = body.get("total24h")
    protocols = body.get("protocols") or []
    top = sorted(protocols, key=lambda p: p.get("total24h") or 0, reverse=True)[:5]
    return {
        "fees_24h_usd": total_24h,
        "fees_7d_usd": body.get("total7d"),
        "fees_30d_usd": body.get("total30d"),
        "change_24h_pct": body.get("change_1d"),
        "annualised_usd": round(total_24h * 365, 2) if total_24h else None,
        "protocol_count": len(protocols),
        "top_fee_earners": [
            {"name": p.get("name"), "fees_24h_usd": p.get("total24h")} for p in top
        ],
        "note": "Fee component of REV; excludes out-of-protocol MEV tips.",
        "source": "defillama",
    }


def tokenized_assets() -> Dict[str, Any]:
    """Tokenized real-world assets on Solana, with equities broken out.

    Sourced from the full protocol list, which is large and slow-moving, so it
    is cached (see config.PROTOCOLS_CACHE_TTL) rather than refetched each run.
    """
    protocols = request_json_cached(
        config.DEFILLAMA_PROTOCOLS_URL, ttl_secs=config.PROTOCOLS_CACHE_TTL, timeout=60.0
    )
    rows = []
    for p in protocols:
        if "Solana" not in (p.get("chains") or []):
            continue
        if (p.get("category") or "") not in RWA_CATEGORIES:
            continue
        value = (p.get("chainTvls") or {}).get("Solana")
        if not value:
            continue
        name = p.get("name") or ""
        rows.append(
            {
                "name": name,
                "tvl_usd": round(value, 2),
                "change_24h_pct": round(p["change_1d"], 3) if p.get("change_1d") is not None else None,
                "category": p.get("category"),
                "is_equity": any(k in name.lower() for k in EQUITY_PROTOCOLS),
            }
        )

    rows.sort(key=lambda r: r["tvl_usd"], reverse=True)
    equities = [r for r in rows if r["is_equity"]]
    total = sum(r["tvl_usd"] for r in rows)
    return {
        "total_rwa_usd": round(total, 2),
        "protocol_count": len(rows),
        "equities_usd": round(sum(r["tvl_usd"] for r in equities), 2),
        "equities_share_pct": round(100 * sum(r["tvl_usd"] for r in equities) / total, 2)
        if total
        else None,
        "equity_protocols": equities,
        "top_protocols": rows[:10],
        "source": "defillama",
    }


def collect() -> Dict[str, Any]:
    out = {}
    for name, fn in (
        ("price", price),
        ("tvl", tvl),
        ("dex_volume", dex_volume),
        ("stablecoins", stablecoins),
        ("fees", fees),
        ("tokenized_assets", tokenized_assets),
    ):
        try:
            out[name] = fn()
        except FetchError as exc:
            out[name] = {"error": str(exc)}
    return out
