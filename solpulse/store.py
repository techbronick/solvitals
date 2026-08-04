"""Append-only history used as the baseline for anomaly detection.

JSONL rather than a database: it survives partial writes, is trivially
inspectable, and keeps the zero-dependency promise.
"""

import json
import os
from typing import Any, Dict, List

from . import config


def _flatten(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    """Reduce a full snapshot to the scalar series worth tracking over time."""
    chain = snapshot.get("chain", {})
    market = snapshot.get("market", {})
    perf = chain.get("performance", {})
    validators = chain.get("validators", {})
    return {
        "captured_at": snapshot.get("captured_at"),
        "tps_non_vote": perf.get("tps_non_vote"),
        "tps_total": perf.get("tps_total"),
        "avg_slot_time_secs": perf.get("avg_slot_time_secs"),
        "delinquent_pct": validators.get("delinquent_pct"),
        "nakamoto_coefficient": validators.get("nakamoto_coefficient"),
        "price_usd": market.get("price", {}).get("usd"),
        "tvl_usd": market.get("tvl", {}).get("tvl_usd"),
        "stablecoins_usd": market.get("stablecoins", {}).get("total_usd"),
    }


def append(snapshot: Dict[str, Any]) -> None:
    path = config.HISTORY_PATH
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(_flatten(snapshot)) + "\n")


def load(limit: int = None) -> List[Dict[str, Any]]:
    """Read history, skipping any corrupt lines from an interrupted write."""
    path = config.HISTORY_PATH
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    window = limit if limit is not None else config.HISTORY_WINDOW
    return rows[-window:]
