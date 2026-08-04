"""Anomaly detection over the collected metrics.

Two complementary checks:

1. Absolute thresholds -- conditions that are bad regardless of history
   (a stalled chain, mass validator delinquency).
2. Statistical deviation -- a metric more than N standard deviations from its
   own recent mean, which catches drift that no fixed threshold would.

Both are needed. Thresholds alone miss a TVL collapse that stays "large";
z-scores alone stay quiet when a metric is consistently bad.
"""

from typing import Any, Dict, List, Optional

SEVERITY_ORDER = {"critical": 0, "warning": 1, "info": 2}

# metric -> (warning, critical), compared as "value at or above is worse"
UPPER_THRESHOLDS = {
    "delinquent_pct": (5.0, 10.0),
    "avg_slot_time_secs": (0.65, 0.9),
}
# metric -> (warning, critical), compared as "value at or below is worse"
LOWER_THRESHOLDS = {
    "tps_non_vote": (800.0, 400.0),
    "nakamoto_coefficient": (20, 15),
}

Z_SCORE_METRICS = ("tps_non_vote", "price_usd", "tvl_usd", "stablecoins_usd")
Z_WARNING = 2.0
Z_CRITICAL = 3.0
MIN_HISTORY = 8


def _mean(values: List[float]) -> float:
    return sum(values) / len(values)


def _stdev(values: List[float], mean: float) -> float:
    if len(values) < 2:
        return 0.0
    variance = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
    return variance ** 0.5


def _finding(metric, severity, message, value, expected=None) -> Dict[str, Any]:
    return {
        "metric": metric,
        "severity": severity,
        "message": message,
        "value": value,
        "expected": expected,
    }


def _check_thresholds(current: Dict[str, Any]) -> List[Dict[str, Any]]:
    found = []
    for metric, (warn, crit) in UPPER_THRESHOLDS.items():
        value = current.get(metric)
        if value is None:
            continue
        if value >= crit:
            found.append(_finding(metric, "critical", "{} is {} (critical above {})".format(metric, value, crit), value, "< {}".format(warn)))
        elif value >= warn:
            found.append(_finding(metric, "warning", "{} is {} (elevated above {})".format(metric, value, warn), value, "< {}".format(warn)))

    for metric, (warn, crit) in LOWER_THRESHOLDS.items():
        value = current.get(metric)
        if value is None:
            continue
        if value <= crit:
            found.append(_finding(metric, "critical", "{} is {} (critical below {})".format(metric, value, crit), value, "> {}".format(warn)))
        elif value <= warn:
            found.append(_finding(metric, "warning", "{} is {} (below {})".format(metric, value, warn), value, "> {}".format(warn)))
    return found


def _check_deviation(current: Dict[str, Any], history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    found = []
    for metric in Z_SCORE_METRICS:
        value = current.get(metric)
        if value is None:
            continue
        series = [row[metric] for row in history if row.get(metric) is not None]
        if len(series) < MIN_HISTORY:
            continue
        mean = _mean(series)
        stdev = _stdev(series, mean)
        if stdev == 0:
            continue
        z = (value - mean) / stdev
        direction = "above" if z > 0 else "below"
        severity = None
        if abs(z) >= Z_CRITICAL:
            severity = "critical"
        elif abs(z) >= Z_WARNING:
            severity = "warning"
        if severity:
            found.append(
                _finding(
                    metric,
                    severity,
                    "{} is {:.1f} sigma {} its {}-point mean".format(metric, abs(z), direction, len(series)),
                    value,
                    round(mean, 4),
                )
            )
    return found


def _check_health(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    status = snapshot.get("chain", {}).get("health", {}).get("status")
    if status and status != "ok":
        return [_finding("rpc_health", "critical", "RPC reports node status '{}'".format(status), status, "ok")]
    return []


def detect(snapshot: Dict[str, Any], current: Dict[str, Any], history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return findings ordered most severe first."""
    findings = _check_health(snapshot) + _check_thresholds(current) + _check_deviation(current, history)
    findings.sort(key=lambda f: SEVERITY_ORDER.get(f["severity"], 9))
    return findings
