"""Entry point: collect, detect anomalies, render, repeat."""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Any, Dict

from . import __version__, anomalies, config, store
from .collectors import ecosystem, market, news, rpc, upgrades
from .render import html as html_render
from .render import markdown as md_render


def _utc_now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def collect() -> Dict[str, Any]:
    return {
        "captured_at": _utc_now(),
        "generator": "solvitals/{}".format(__version__),
        "chain": rpc.collect(),
        "market": market.collect(),
        "ecosystem": ecosystem.collect(),
        "news": news.collect(),
        "upgrades": upgrades.collect(),
    }


def _count_errors(snapshot: Dict[str, Any]) -> int:
    total = 0
    for group in ("chain", "market"):
        for section in snapshot.get(group, {}).values():
            if isinstance(section, dict) and "error" in section:
                total += 1
    for group in ("ecosystem", "news", "upgrades"):
        if "error" in (snapshot.get(group) or {}):
            total += 1
    return total


def run_once(output_dir: str, quiet: bool = False) -> Dict[str, Any]:
    os.makedirs(output_dir, exist_ok=True)

    snapshot = collect()
    history = store.load()
    current = store._flatten(snapshot)
    findings = anomalies.detect(snapshot, current, history)
    snapshot["anomalies"] = findings

    # Append after detection so the current reading is not part of its own baseline.
    store.append(snapshot)
    history = history + [current]

    outputs = {
        "report.json": json.dumps(snapshot, indent=2),
        "report.md": md_render.render(snapshot, findings),
        "index.html": html_render.render(snapshot, findings, history),
    }
    for name, body in outputs.items():
        with open(os.path.join(output_dir, name), "w", encoding="utf-8") as handle:
            handle.write(body)

    if not quiet:
        errors = _count_errors(snapshot)
        critical = sum(1 for f in findings if f["severity"] == "critical")
        warnings = sum(1 for f in findings if f["severity"] == "warning")
        print(
            "[{}] wrote {} -- {} critical, {} warning, {} source error(s)".format(
                snapshot["captured_at"], output_dir, critical, warnings, errors
            )
        )
        for f in findings:
            print("    {:>8}  {}".format(f["severity"].upper(), f["message"]))

    return snapshot


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="solvitals",
        description="Auto-updating report on the state of the Solana ecosystem.",
    )
    parser.add_argument("--output-dir", default=config.OUTPUT_DIR,
                        help="where to write report.json, report.md and index.html")
    parser.add_argument("--history-path", default=None,
                        help="metric history file (default: <output-dir>/history.jsonl)")
    parser.add_argument("--watch", action="store_true",
                        help="refresh continuously instead of running once")
    parser.add_argument("--interval", type=int, default=config.REFRESH_INTERVAL,
                        help="seconds between refreshes in --watch mode")
    parser.add_argument("--quiet", action="store_true", help="suppress progress output")
    parser.add_argument("--version", action="version", version="solvitals {}".format(__version__))
    args = parser.parse_args(argv)

    # History follows the output directory unless pinned explicitly. Without
    # this, --output-dir docs would still write history to output/, which is
    # gitignored -- so a CI runner would lose its anomaly baseline every run.
    if args.history_path:
        config.HISTORY_PATH = args.history_path
    elif not os.environ.get("SOLVITALS_HISTORY_PATH"):
        config.HISTORY_PATH = os.path.join(args.output_dir, "history.jsonl")

    if not args.watch:
        run_once(args.output_dir, args.quiet)
        return 0

    if not args.quiet:
        print("Refreshing every {}s. Ctrl-C to stop.".format(args.interval))
    while True:
        try:
            run_once(args.output_dir, args.quiet)
        except KeyboardInterrupt:
            print("\nStopped.")
            return 0
        except Exception as exc:  # keep the daemon alive across transient failures
            print("[{}] run failed: {}".format(_utc_now(), exc), file=sys.stderr)
        try:
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nStopped.")
            return 0
