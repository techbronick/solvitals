"""Ecosystem and community news from the official Solana RSS feed.

Parsed with the standard library's XML module -- no feedparser, no dependency.
"""

import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List

from .. import config
from ..net import DATA_ERRORS, FetchError, request_text_cached

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def _clean(text: str, limit: int = 220) -> str:
    """Strip markup and collapse whitespace from a feed description."""
    if not text:
        return ""
    text = WS_RE.sub(" ", TAG_RE.sub(" ", text)).strip()
    return text[: limit - 1] + "…" if len(text) > limit else text


def _collect() -> Dict[str, Any]:
    try:
        body = request_text_cached(
            config.SOLANA_NEWS_URL, ttl_secs=config.NEWS_CACHE_TTL, timeout=30.0
        )
    except FetchError as exc:
        return {"error": str(exc)}

    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        return {"error": "could not parse RSS: {}".format(exc)}

    items: List[Dict[str, Any]] = []
    for node in root.iterfind(".//item"):
        title = (node.findtext("title") or "").strip()
        if not title:
            continue
        items.append(
            {
                "title": title,
                "link": (node.findtext("link") or "").strip(),
                "published": (node.findtext("pubDate") or "").strip(),
                "summary": _clean(node.findtext("description") or ""),
            }
        )
        if len(items) >= config.NEWS_ITEMS:
            break

    if not items:
        return {"error": "feed contained no items"}

    return {
        "items": items,
        "count": len(items),
        "source": "solana.com/news",
    }


def collect() -> Dict[str, Any]:
    try:
        return _collect()
    except FetchError as exc:
        return {"error": str(exc)}
    except DATA_ERRORS as exc:
        return {"error": "unexpected feed shape: {}: {}".format(type(exc).__name__, exc)}
