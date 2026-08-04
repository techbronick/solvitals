"""On-chain metrics collected directly from Solana RPC.

No API key required -- every method here is available on the public mainnet
endpoint. Each collector degrades independently: a failure records an error for
that metric rather than aborting the run.
"""

from typing import Any, Dict, List, Optional

from .. import config
from ..net import FetchError, request_json

LAMPORTS_PER_SOL = 1_000_000_000


def _call(method: str, params: Optional[List[Any]] = None) -> Any:
    """Issue a JSON-RPC call, falling back to secondary endpoints on failure."""
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}
    errors = []
    for url in [config.RPC_URL] + config.RPC_FALLBACKS:
        try:
            body = request_json(url, payload=payload)
        except FetchError as exc:
            errors.append(str(exc))
            continue
        if "error" in body:
            errors.append("{} -> {}".format(method, body["error"]))
            continue
        return body.get("result")
    raise FetchError("all RPC endpoints failed for {}: {}".format(method, "; ".join(errors)))


def health() -> Dict[str, Any]:
    try:
        return {"status": _call("getHealth")}
    except FetchError as exc:
        # An unhealthy node answers with an error rather than "ok", so a failure
        # here is itself the signal worth reporting.
        return {"status": "unhealthy", "detail": str(exc)}


def network_performance() -> Dict[str, Any]:
    """TPS, slot time and block height.

    Solana counts consensus votes as transactions. Raw TPS therefore runs far
    above the figure people mean colloquially, so both are reported and the
    non-vote number is the one surfaced in headlines.
    """
    samples = _call("getRecentPerformanceSamples", [config.PERF_SAMPLE_COUNT])
    if not samples:
        return {"error": "no performance samples returned"}

    total_secs = sum(s["samplePeriodSecs"] for s in samples)
    total_txns = sum(s["numTransactions"] for s in samples)
    total_slots = sum(s["numSlots"] for s in samples)
    # numNonVoteTransactions is absent on older validator versions.
    total_non_vote = sum(s.get("numNonVoteTransactions", 0) for s in samples)

    latest = samples[0]
    return {
        "tps_total": round(total_txns / total_secs, 2) if total_secs else None,
        "tps_non_vote": round(total_non_vote / total_secs, 2) if total_secs and total_non_vote else None,
        "vote_share_pct": round(100 * (1 - total_non_vote / total_txns), 2)
        if total_txns and total_non_vote
        else None,
        "avg_slot_time_secs": round(total_secs / total_slots, 4) if total_slots else None,
        "latest_sample_slot": latest.get("slot"),
        "samples_used": len(samples),
        "block_height": _safe(lambda: _call("getBlockHeight")),
        "current_slot": _safe(lambda: _call("getSlot")),
    }


def epoch() -> Dict[str, Any]:
    info = _call("getEpochInfo")
    slot_index = info.get("slotIndex", 0)
    slots_in_epoch = info.get("slotsInEpoch", 0) or 1
    progress = 100 * slot_index / slots_in_epoch
    # ~400ms target slot time gives a usable estimate of time remaining.
    remaining_secs = (slots_in_epoch - slot_index) * 0.4
    return {
        "epoch": info.get("epoch"),
        "slot_index": slot_index,
        "slots_in_epoch": slots_in_epoch,
        "progress_pct": round(progress, 2),
        "eta_hours": round(remaining_secs / 3600, 1),
        "transaction_count": info.get("transactionCount"),
    }


def validators() -> Dict[str, Any]:
    """Validator counts, stake concentration and the Nakamoto coefficient."""
    accounts = _call("getVoteAccounts")
    current = accounts.get("current", [])
    delinquent = accounts.get("delinquent", [])

    staked = sorted(
        ((v.get("activatedStake", 0) / LAMPORTS_PER_SOL, v) for v in current),
        key=lambda pair: pair[0],
        reverse=True,
    )
    total_stake = sum(stake for stake, _ in staked)
    delinquent_stake = sum(v.get("activatedStake", 0) for v in delinquent) / LAMPORTS_PER_SOL

    # Nakamoto coefficient: validators needed to reach 33% of stake and halt
    # consensus. The single most useful decentralisation number.
    running, nakamoto = 0.0, 0
    for stake, _ in staked:
        running += stake
        nakamoto += 1
        if total_stake and running / total_stake >= 0.33:
            break

    top = [
        {
            "vote_account": v.get("votePubkey"),
            "stake_sol": round(stake, 2),
            "stake_pct": round(100 * stake / total_stake, 3) if total_stake else None,
            "commission": v.get("commission"),
        }
        for stake, v in staked[:10]
    ]

    commissions = [v.get("commission", 0) for _, v in staked]
    return {
        "active_count": len(current),
        "delinquent_count": len(delinquent),
        "delinquent_pct": round(100 * len(delinquent) / (len(current) + len(delinquent)), 2)
        if current or delinquent
        else None,
        "delinquent_stake_sol": round(delinquent_stake, 2),
        "delinquent_stake_pct": round(100 * delinquent_stake / (total_stake + delinquent_stake), 3)
        if total_stake
        else None,
        "total_active_stake_sol": round(total_stake, 2),
        "nakamoto_coefficient": nakamoto,
        "median_commission": sorted(commissions)[len(commissions) // 2] if commissions else None,
        "zero_commission_count": sum(1 for c in commissions if c == 0),
        "top_validators": top,
    }


def supply() -> Dict[str, Any]:
    result = _call("getSupply", [{"excludeNonCirculatingAccountsList": True}])
    value = result.get("value", {})
    total = value.get("total", 0) / LAMPORTS_PER_SOL
    circulating = value.get("circulating", 0) / LAMPORTS_PER_SOL
    return {
        "total_sol": round(total, 2),
        "circulating_sol": round(circulating, 2),
        "non_circulating_sol": round(value.get("nonCirculating", 0) / LAMPORTS_PER_SOL, 2),
        "circulating_pct": round(100 * circulating / total, 2) if total else None,
    }


def active_addresses() -> Dict[str, Any]:
    """Unique fee payers observed across a sample of recent blocks.

    Deliberately *not* called "daily active addresses". A true daily unique
    count requires deduplicating signers across every block in 24 hours --
    roughly 216,000 blocks -- which no keyless source exposes and which would be
    absurd to fetch per run. Extrapolating a sample would also overcount badly,
    because active addresses reappear in many blocks over a day.

    What this measures is honest and still useful: how many distinct addresses
    are transacting right now, and what share of transactions are votes. Tracked
    over time it shows the shape of activity even though the absolute number is
    not a daily figure.
    """
    tip = _call("getSlot")
    sampled, signers, tx_total, vote_total = [], set(), 0, 0

    for i in range(config.ADDRESS_SAMPLE_BLOCKS):
        # Step back from the tip: recent enough to still be served, spaced so the
        # sample isn't one contiguous burst of near-identical blocks.
        slot = tip - 200 - (i * config.ADDRESS_SAMPLE_SPACING)
        try:
            block = _call(
                "getBlock",
                [slot, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0,
                        "transactionDetails": "accounts", "rewards": False}],
            )
        except FetchError:
            continue  # skipped slots and pruned history are both normal
        if not block:
            continue

        txs = block.get("transactions") or []
        tx_total += len(txs)
        sampled.append(slot)
        for tx in txs:
            keys = (tx.get("transaction") or {}).get("accountKeys") or []
            for key in keys:
                if key.get("signer"):
                    signers.add(key.get("pubkey"))
            # Vote transactions carry exactly one signer and touch the vote program.
            if any(k.get("pubkey") == "Vote111111111111111111111111111111111111111" for k in keys):
                vote_total += 1

    if not sampled:
        return {"error": "no blocks could be sampled"}

    non_vote = tx_total - vote_total
    return {
        "unique_signers_sampled": len(signers),
        "blocks_sampled": len(sampled),
        "transactions_sampled": tx_total,
        "non_vote_transactions_sampled": non_vote,
        "signers_per_block": round(len(signers) / len(sampled), 1),
        "non_vote_share_pct": round(100 * non_vote / tx_total, 2) if tx_total else None,
        "sampled_slots": sampled,
        "note": (
            "Unique fee payers across sampled blocks -- an activity indicator, "
            "not a 24h unique-address count."
        ),
    }


def _safe(fn):
    try:
        return fn()
    except FetchError:
        return None


def collect() -> Dict[str, Any]:
    """Run every on-chain collector, isolating failures per section."""
    out = {}
    for name, fn in (
        ("health", health),
        ("performance", network_performance),
        ("epoch", epoch),
        ("validators", validators),
        ("supply", supply),
        ("activity", active_addresses),
    ):
        try:
            out[name] = fn()
        except FetchError as exc:
            out[name] = {"error": str(exc)}
    return out
