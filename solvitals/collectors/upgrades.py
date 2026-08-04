"""Upcoming protocol upgrades, tracked from proposal through live activation.

Most ecosystem dashboards report what the chain *is doing*. This reports what is
about to change, by joining three keyless sources:

1. **The SIMD repository** -- every Solana Improvement Document, with its
   status and (where assigned) the feature-gate pubkey that switches it on.
   Fetched as a single tarball, which avoids GitHub's unauthenticated API rate
   limit entirely -- that matters because CI runners share IPs and the 60/hour
   budget is routinely exhausted by other tenants.
2. **Agave's feature-set source** -- maps gate pubkeys to human-readable names.
3. **The chain itself** -- `getMultipleAccounts` on those gate pubkeys says
   whether each feature is live, and at which slot.

The result answers a question no static list can: not "what has been proposed"
but "what is actually switched on, on which cluster, right now". A gate that
exists on devnet and not mainnet is a change in flight.
"""

import io
import re
import tarfile
from typing import Any, Dict, List, Optional

from .. import config
from ..net import DATA_ERRORS, FetchError, request_bytes_cached, request_text_cached, request_json

# `pub mod some_feature { solana_pubkey::declare_id!("Base58..."); }`
FEATURE_RE = re.compile(
    r"pub mod\s+(\w+)\s*\{[^}]*?declare_id!\(\s*\"([1-9A-HJ-NP-Za-km-z]{32,44})\"", re.S
)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.S)

# Proposals worth calling out by name. The bounty writes "SIMD-525"; the repo
# zero-pads to four digits, so the file is 0525.
HIGHLIGHT = ("0326", "0525")


def _parse_frontmatter(text: str) -> Dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t", "-")):
            continue
        key, _, value = line.partition(":")
        fields[key.strip().lower()] = value.strip().strip("'\"")
    return fields


def _load_simds() -> List[Dict[str, Any]]:
    """Every SIMD from one tarball fetch -- no per-file API calls."""
    raw = request_bytes_cached(
        config.SIMD_TARBALL_URL, ttl_secs=config.UPGRADES_CACHE_TTL, timeout=90.0
    )
    proposals = []
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        for member in archive.getmembers():
            if not member.isfile() or "/proposals/" not in member.name:
                continue
            if not member.name.endswith(".md"):
                continue
            handle = archive.extractfile(member)
            if handle is None:
                continue
            meta = _parse_frontmatter(handle.read().decode("utf-8", errors="replace"))
            if not meta.get("simd"):
                continue
            proposals.append(
                {
                    "simd": str(meta.get("simd")).zfill(4),
                    "title": meta.get("title"),
                    "status": meta.get("status"),
                    "category": meta.get("category"),
                    "created": meta.get("created"),
                    "feature_gate": meta.get("feature") or None,
                }
            )
    proposals.sort(key=lambda p: p["simd"])
    return proposals


def _load_feature_gates() -> Dict[str, str]:
    """gate pubkey -> feature name, from Agave's feature-set source."""
    source = request_text_cached(
        config.AGAVE_FEATURES_URL, ttl_secs=config.UPGRADES_CACHE_TTL, timeout=60.0
    )
    return {pubkey: name for name, pubkey in FEATURE_RE.findall(source)}


def _activation_status(pubkeys: List[str], rpc_url: str) -> Dict[str, Optional[Dict[str, Any]]]:
    """Read feature-gate accounts. Absent account = gate not yet created.

    The account is 9 bytes: a one-byte Option tag (1 = activated) followed by a
    little-endian u64 activation slot.
    """
    import base64

    out: Dict[str, Optional[Dict[str, Any]]] = {}
    for start in range(0, len(pubkeys), 100):  # getMultipleAccounts caps at 100
        batch = pubkeys[start : start + 100]
        body = request_json(
            rpc_url,
            payload={
                "jsonrpc": "2.0", "id": 1, "method": "getMultipleAccounts",
                "params": [batch, {"encoding": "base64"}],
            },
            timeout=45.0,
        )
        values = ((body.get("result") or {}).get("value")) or []
        for pubkey, account in zip(batch, values):
            if not account:
                out[pubkey] = None  # gate does not exist on this cluster
                continue
            data = account.get("data") or ["", ""]
            try:
                blob = base64.b64decode(data[0])
            except Exception:
                out[pubkey] = {"activated": False}
                continue
            if blob and blob[0] == 1 and len(blob) >= 9:
                slot = int.from_bytes(blob[1:9], "little")
                out[pubkey] = {"activated": True, "activation_slot": slot}
            else:
                out[pubkey] = {"activated": False}
    return out


def _collect() -> Dict[str, Any]:
    proposals = _load_simds()
    if not proposals:
        return {"error": "no SIMDs parsed"}

    try:
        gate_names = _load_feature_gates()
    except (FetchError,) + DATA_ERRORS:
        gate_names = {}

    gated = [p for p in proposals if p.get("feature_gate") in gate_names]
    pubkeys = [p["feature_gate"] for p in gated]

    # Query every configured cluster: a gate live on devnet but absent on
    # mainnet is precisely "an upcoming upgrade".
    clusters: Dict[str, Dict[str, Any]] = {}
    for name, url in config.CLUSTER_RPCS.items():
        try:
            clusters[name] = _activation_status(pubkeys, url)
        except (FetchError,) + DATA_ERRORS as exc:
            clusters[name] = {}

    tracked = []
    for p in gated:
        gate = p["feature_gate"]
        per_cluster = {}
        for cluster, statuses in clusters.items():
            state = statuses.get(gate)
            if state is None:
                per_cluster[cluster] = "not created"
            elif state.get("activated"):
                per_cluster[cluster] = "active (slot {:,})".format(state["activation_slot"])
            else:
                per_cluster[cluster] = "pending"
        tracked.append(
            {
                "simd": p["simd"], "title": p["title"], "status": p["status"],
                "feature_name": gate_names.get(gate), "feature_gate": gate,
                "clusters": per_cluster,
            }
        )

    by_status: Dict[str, int] = {}
    for p in proposals:
        by_status[p.get("status") or "Unknown"] = by_status.get(p.get("status") or "Unknown", 0) + 1

    highlights = [
        p for p in proposals
        if p["simd"] in HIGHLIGHT or "alpenglow" in (p.get("title") or "").lower()
    ]
    for h in highlights:
        gate = h.get("feature_gate")
        h["clusters"] = (
            {c: ("not created" if s.get(gate) is None
                 else "active" if s.get(gate, {}).get("activated") else "pending")
             for c, s in clusters.items()}
            if gate and gate in gate_names else {}
        )

    # Live cluster versions: divergence between clusters is itself a rollout signal.
    versions = {}
    for name, url in config.CLUSTER_RPCS.items():
        try:
            result = request_json(
                url, payload={"jsonrpc": "2.0", "id": 1, "method": "getVersion"}, timeout=30.0
            )
            versions[name] = (result.get("result") or {}).get("solana-core")
        except (FetchError,) + DATA_ERRORS:
            versions[name] = None

    active_mainnet = sum(
        1 for t in tracked if str(t["clusters"].get("mainnet", "")).startswith("active")
    )
    return {
        "proposal_count": len(proposals),
        "by_status": dict(sorted(by_status.items(), key=lambda kv: -kv[1])),
        "gated_count": len(tracked),
        "active_on_mainnet": active_mainnet,
        "pending_on_mainnet": len(tracked) - active_mainnet,
        "cluster_versions": versions,
        "highlights": highlights,
        "recently_pending": [
            t for t in tracked
            if not str(t["clusters"].get("mainnet", "")).startswith("active")
        ][:12],
        "source": "solana-improvement-documents + agave feature-set + live RPC",
    }


def collect() -> Dict[str, Any]:
    try:
        return _collect()
    except FetchError as exc:
        return {"error": str(exc)}
    except DATA_ERRORS as exc:
        return {"error": "unexpected upgrade data: {}: {}".format(type(exc).__name__, exc)}
    except tarfile.TarError as exc:
        return {"error": "could not read SIMD archive: {}".format(exc)}
