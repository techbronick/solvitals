"""HTTP helpers built on the standard library only.

The bounty rewards solutions that need no API keys and no third-party packages,
so everything here goes through urllib rather than requests/httpx.
"""

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

USER_AGENT = "solpulse/1.0 (+https://github.com/)"


class FetchError(Exception):
    """Raised when a source cannot be reached after retries."""


def _open(req: urllib.request.Request, timeout: float) -> bytes:
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def request_json(
    url: str,
    payload: Optional[Dict[str, Any]] = None,
    timeout: float = 20.0,
    retries: int = 3,
    backoff: float = 1.5,
) -> Any:
    """GET (or POST when payload is given) and decode JSON.

    Retries on transport errors and on 429/5xx, which the public Solana RPC and
    the free DeFiLlama/CoinGecko tiers all return under load.
    """
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"

    last_error = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers=headers)
        try:
            return json.loads(_open(req, timeout))
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in (429, 500, 502, 503, 504):
                break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            last_error = exc
        if attempt < retries - 1:
            time.sleep(backoff ** attempt)

    raise FetchError("{}: {}".format(url, last_error))


def request_json_cached(url: str, ttl_secs: int, cache_dir: str = ".cache", **kwargs) -> Any:
    """Fetch with an on-disk TTL cache.

    Some upstream payloads are large and slow-moving -- DeFiLlama's full
    protocol list is roughly 8 MB and its RWA figures move on a daily cadence.
    Re-downloading that every refresh would be rude to a free API and would
    dominate the run time, so responses are cached and reused until stale.
    A stale-but-present cache is also the fallback when the fetch fails, which
    keeps the section populated through a transient outage.
    """
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, hashlib.sha256(url.encode()).hexdigest()[:16] + ".json")

    if os.path.exists(path) and (time.time() - os.path.getmtime(path)) < ttl_secs:
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, OSError):
            pass  # corrupt cache is not fatal -- fall through and refetch

    try:
        body = request_json(url, **kwargs)
    except FetchError:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    return json.load(handle)
            except (json.JSONDecodeError, OSError):
                pass
        raise

    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(body, handle)
    os.replace(tmp, path)  # atomic: a reader never sees a half-written cache
    return body
