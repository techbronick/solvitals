"""Official Solana ecosystem metrics from solana.com's own data API.

This is the endpoint behind solana.com/data. It is public, keyless, and
unauthenticated, and it republishes metrics computed by thirteen providers --
including Dune, Allium, Blockworks, Artemis and Token Terminal -- each row
carrying its own provider attribution.

That matters for two reasons:

1. It supplies a genuine **daily active addresses** figure, deduplicated across
   a full day by the provider. Sampling blocks over RPC cannot produce that
   number; this can.
2. It gives Dune-computed metrics without a Dune API key. Dune's own API is
   closed (401 without a key, paid tiers only), so this is the honest route to
   the same underlying analytics.

Because several providers publish the same metric with different
methodologies, disagreement between them is itself signal -- see `divergence`.
"""

from typing import Any, Dict, List, Optional

from .. import config
from ..net import FetchError, request_json_cached

# Metrics worth surfacing, mapped to the key used in the report.
TRACKED = {
    "Active Addresses": "active_addresses",
    "Fee Payers": "fee_payers",
    "Fees": "fees",
    "DEX Volume": "dex_volume",
    "DEX Traders": "dex_traders",
    "Transaction Count (Total)": "transactions_total",
    "Non Vote Transaction Count (Success)": "non_vote_success",
    "Non Vote Transaction Count (Failed)": "non_vote_failed",
    "Total Stake": "total_stake",
    "Validator Count": "validator_count",
    "Transfer Volume": "transfer_volume",
    "Top 3 ASN Share": "top3_asn_share",
}

# Preferred provider when several publish the same metric, so the headline
# number is stable run to run rather than flipping between methodologies.
PROVIDER_PREFERENCE = ("Dune", "Allium", "Top Ledger", "Artemis", "Blockworks")


def _latest_by_provider(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Most recent row per provider for one metric."""
    best: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        provider = row.get("providerName") or "unknown"
        if provider not in best or (row.get("date") or "") > (best[provider].get("date") or ""):
            best[provider] = row
    return best


def _pick(by_provider: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    for provider in PROVIDER_PREFERENCE:
        if provider in by_provider:
            return by_provider[provider]
    return next(iter(by_provider.values()), None)


def _series(rows: List[Dict[str, Any]], provider: str, limit: int = 90) -> List[Dict[str, Any]]:
    points = sorted(
        (r for r in rows if r.get("providerName") == provider),
        key=lambda r: r.get("date") or "",
    )
    return [{"date": p["date"], "value": p["value"]} for p in points[-limit:]]


def collect() -> Dict[str, Any]:
    """Fetch and reshape solana.com's metric feed.

    Cached: the payload is ~340 KB for 30 days and the underlying figures update
    daily, so refetching every 15 minutes would be pointless traffic.
    """
    try:
        body = request_json_cached(
            config.SOLANA_DATA_URL, ttl_secs=config.SOLANA_DATA_CACHE_TTL, timeout=60.0
        )
    except FetchError as exc:
        return {"error": str(exc)}

    rows = body.get("rows") or []
    if not rows:
        return {"error": "solana.com/data returned no rows"}

    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row.get("metricName"), []).append(row)

    metrics: Dict[str, Any] = {}
    divergence: List[Dict[str, Any]] = []

    for metric_name, key in TRACKED.items():
        metric_rows = grouped.get(metric_name)
        if not metric_rows:
            continue
        by_provider = _latest_by_provider(metric_rows)
        chosen = _pick(by_provider)
        if not chosen:
            continue

        metrics[key] = {
            "label": metric_name,
            "value": chosen.get("value"),
            "unit": chosen.get("unit"),
            "date": chosen.get("date"),
            "provider": chosen.get("providerName"),
            "providers_reporting": sorted(by_provider),
            "history": _series(metric_rows, chosen.get("providerName")),
        }

        # Multi-source correlation: where two providers measure the same thing
        # on the same day and disagree materially, that gap is worth surfacing
        # rather than hiding behind a single chosen number.
        same_day = {
            p: r["value"]
            for p, r in by_provider.items()
            if r.get("date") == chosen.get("date") and r.get("value") is not None
        }
        if len(same_day) > 1:
            lo, hi = min(same_day.values()), max(same_day.values())
            if lo > 0 and (hi - lo) / lo >= config.DIVERGENCE_THRESHOLD:
                divergence.append(
                    {
                        "metric": metric_name,
                        "date": chosen.get("date"),
                        "spread_pct": round(100 * (hi - lo) / lo, 1),
                        "by_provider": {p: v for p, v in sorted(same_day.items())},
                    }
                )

    return {
        "metrics": metrics,
        "provider_divergence": divergence,
        "providers": sorted({r.get("providerName") for r in rows if r.get("providerName")}),
        "metric_count": len(metrics),
        "generated_at": body.get("generatedAt"),
        "range_days": body.get("rangeDays"),
        "source": "solana.com/data",
        "note": (
            "Official solana.com metric feed. Keyless and unauthenticated; "
            "republishes provider-computed analytics including Dune."
        ),
    }
