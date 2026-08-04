"""HTTP helpers built on the standard library only.

The bounty rewards solutions that need no API keys and no third-party packages,
so everything here goes through urllib rather than requests/httpx.
"""

import json
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
