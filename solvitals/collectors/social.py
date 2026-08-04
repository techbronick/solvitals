"""Announcements from key Solana X/Twitter accounts.

X has no free API. The one keyless route that works is the public syndication
endpoint used to render embedded timelines: it returns a Next.js data blob
containing recent posts, with no key and no account.

It is not fully reliable -- roughly one request in five returns 429. That is
precisely the failure profile the per-collector isolation exists for: a miss
costs this section and nothing else, and the previous run's cached copy is
served in the meantime. Treating an 80%-reliable source as unusable would be
stricter than the architecture requires.

Sentiment analysis is deliberately not attempted. Scoring tone without a model
would be keyword counting dressed up as analysis, and the honest deliverable is
the announcements themselves.
"""

import html as html_lib
import json
import re
from email.utils import parsedate_to_datetime
from typing import Any, Dict, List

from .. import config
from ..net import DATA_ERRORS, FetchError, request_text_cached

NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.S
)
WS_RE = re.compile(r"\s+")


def _extract(payload: Any) -> List[Dict[str, Any]]:
    """Walk the blob for tweet objects. The shape is not contractual, so this
    searches rather than indexing a fixed path."""
    found: List[Dict[str, Any]] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("full_text") and node.get("created_at"):
                found.append(node)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(payload)
    return found


def _clean(text: str, limit: int = 240) -> str:
    # Timeline text arrives HTML-escaped (&gt;, &amp;). Unescape once here so the
    # renderers escape exactly once, instead of showing literal "&amp;gt;".
    text = html_lib.unescape(text or "")
    text = WS_RE.sub(" ", text).strip()
    return text[: limit - 1] + "…" if len(text) > limit else text


def _timestamp(created_at: Any) -> float:
    """Parse X's RFC-2822-ish timestamp for sorting. Unparseable sorts oldest."""
    try:
        return parsedate_to_datetime(created_at).timestamp()
    except Exception:
        return 0.0


def _for_handle(handle: str) -> List[Dict[str, Any]]:
    body = request_text_cached(
        config.X_TIMELINE_URL.format(handle=handle),
        ttl_secs=config.SOCIAL_CACHE_TTL,
        timeout=30.0,
    )
    match = NEXT_DATA_RE.search(body)
    if not match:
        raise FetchError("no timeline data for @{}".format(handle))

    posts = []
    for tweet in _extract(json.loads(match.group(1))):
        text = tweet.get("full_text") or ""
        # Replies and retweets are noise for an announcements feed.
        if text.startswith(("@", "RT ")):
            continue
        posts.append(
            {
                "handle": handle,
                "text": _clean(text),
                "created_at": tweet.get("created_at"),
                "_sort": _timestamp(tweet.get("created_at")),
                "url": "https://x.com/{}/status/{}".format(handle, tweet.get("id_str") or ""),
            }
        )
        if len(posts) >= config.SOCIAL_POSTS_PER_ACCOUNT:
            break
    return posts


def _collect() -> Dict[str, Any]:
    posts: List[Dict[str, Any]] = []
    reached, failed = [], []
    for handle in config.X_ACCOUNTS:
        try:
            posts.extend(_for_handle(handle))
            reached.append(handle)
        except (FetchError,) + DATA_ERRORS as exc:
            failed.append({"handle": handle, "reason": str(exc)[:120]})

    if not posts:
        if failed:
            return {"error": "no usable posts; accounts failed: {}".format(
                ", ".join(f["handle"] for f in failed))}
        return {"error": "accounts reachable but returned no usable announcements"}

    # Newest first across all accounts -- otherwise a stale post from one
    # account outranks today's from another.
    posts.sort(key=lambda p: p.get("_sort") or 0, reverse=True)
    for p in posts:
        p.pop("_sort", None)
    posts = posts[: config.SOCIAL_TOTAL_POSTS]

    return {
        "posts": posts,
        "accounts_reached": reached,
        "accounts_failed": failed,
        "count": len(posts),
        "source": "x.com syndication timeline (keyless)",
        "note": (
            "Announcements only; replies and retweets filtered. The endpoint "
            "rate-limits intermittently, so a failed account degrades this "
            "section alone and the cached copy is reused."
        ),
    }


def collect() -> Dict[str, Any]:
    try:
        return _collect()
    except FetchError as exc:
        return {"error": str(exc)}
    except DATA_ERRORS as exc:
        return {"error": "unexpected timeline shape: {}: {}".format(type(exc).__name__, exc)}
    except RecursionError:
        return {"error": "timeline payload nested too deeply to parse"}
