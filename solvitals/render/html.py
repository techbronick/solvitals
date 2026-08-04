"""Self-contained interactive HTML dashboard.

Everything is inlined -- no CDN, no build step, no network calls at view time.
Open the file directly or serve it statically.

Colour roles follow a validated palette: one hue for every sparkline (each tile
is its own single series, so hue never encodes identity), and a reserved status
palette for alerts, always paired with a text label so severity is never carried
by colour alone.
"""

import html as html_escape
import json
from typing import Any, Dict, List, Optional

CSS = """
*, *::before, *::after { box-sizing: border-box; }
:root {
  color-scheme: dark;
  --page:        #0d0d0d;
  --surface:     #1a1a19;
  --ink:         #ffffff;
  --ink-2:       #c3c2b7;
  --muted:       #898781;
  --grid:        #2c2c2a;
  --axis:        #383835;
  --border:      rgba(255,255,255,0.10);
  --series:      #3987e5;
  --good:        #0ca30c;
  --warning:     #fab219;
  --critical:    #d03b3b;
}
:root[data-theme="light"] {
  color-scheme: light;
  --page: #f9f9f7; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e;
  --muted: #6b6a66; --grid: #e1e0d9; --axis: #c3c2b7;
  --border: rgba(11,11,11,0.10); --series: #2a78d6; --good: #006300;
  /* Status steps re-chosen for the light surface: the dark-mode values drop
     to 1.8:1 here, which would make the WARNING label effectively invisible. */
  --warning: #8a5a00; --critical: #b32020;
}
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
    color-scheme: light;
    --page: #f9f9f7; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e;
    --muted: #6b6a66; --grid: #e1e0d9; --axis: #c3c2b7;
    --border: rgba(11,11,11,0.10); --series: #2a78d6; --good: #006300;
    --warning: #8a5a00; --critical: #b32020;
  }
}
body {
  margin: 0; padding: 32px 24px 64px;
  background: var(--page); color: var(--ink);
  font: 15px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif;
}
.wrap { max-width: 1180px; margin: 0 auto; }
header { display: flex; flex-wrap: wrap; gap: 12px; align-items: baseline;
         justify-content: space-between; margin-bottom: 28px; }
h1 { font-size: 22px; font-weight: 620; margin: 0; letter-spacing: -0.01em; }
h3 { font-size: 13.5px; font-weight: 600; margin: 22px 0 10px; color: var(--ink-2); }
h2 { font-size: 13px; font-weight: 600; letter-spacing: 0.07em;
     text-transform: uppercase; color: var(--muted); margin: 36px 0 14px; }
.stamp { color: var(--ink-2); font-size: 13px; font-variant-numeric: tabular-nums; }
button.toggle {
  background: transparent; color: var(--ink-2); border: 1px solid var(--border);
  border-radius: 7px; padding: 5px 11px; font: inherit; font-size: 13px; cursor: pointer;
}
button.toggle:hover { color: var(--ink); }

.grid { display: grid; gap: 12px;
        grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }
.tile { background: var(--surface); border: 1px solid var(--border);
        border-radius: 11px; padding: 15px 16px 12px; min-width: 0; }
.tile .label { font-size: 12px; color: var(--muted); letter-spacing: 0.02em;
               display: flex; align-items: center; gap: 6px; }
.tile .value { font-size: 27px; font-weight: 600; margin-top: 5px;
               letter-spacing: -0.02em; line-height: 1.15; overflow-wrap: anywhere; }
.tile .sub { font-size: 12.5px; color: var(--ink-2); margin-top: 3px;
             font-variant-numeric: tabular-nums; }
.delta.up { color: var(--good); } .delta.down { color: var(--critical); }
.spark { margin-top: 9px; display: block; width: 100%; height: 34px; overflow: visible; }
.spark .line { fill: none; stroke: var(--series); stroke-width: 2;
               stroke-linecap: round; stroke-linejoin: round; }
.spark .dot { fill: var(--series); stroke: var(--surface); stroke-width: 2; }
.spark .hit { fill: transparent; cursor: crosshair; }
.spark .cross { stroke: var(--axis); stroke-width: 1; display: none; }
.spark.on .cross { display: block; }
.spark-src { font-size: 10.5px; color: var(--muted); margin-top: 2px; letter-spacing: 0.02em; }
.spark-provider .line { stroke-dasharray: none; }
.spark-local .line { stroke-dasharray: 3 2; }
.no-history { font-size: 12px; color: var(--muted); margin-top: 9px;
              padding: 8px 0 2px; border-top: 1px solid var(--grid); }

.alerts { display: flex; flex-direction: column; gap: 8px; }
.alert { display: flex; gap: 11px; align-items: flex-start; background: var(--surface);
         border: 1px solid var(--border); border-left-width: 3px;
         border-radius: 9px; padding: 11px 14px; }
.alert.critical { border-left-color: var(--critical); }
.alert.warning  { border-left-color: var(--warning); }
.alert.info     { border-left-color: var(--series); }
.alert .icon { font-weight: 700; font-size: 12px; letter-spacing: 0.04em;
               padding-top: 1px; white-space: nowrap; }
.alert.critical .icon { color: var(--critical); }
.alert.warning  .icon { color: var(--warning); }
.alert.info     .icon { color: var(--series); }
.alert .body { min-width: 0; }
.alert .metric { font-weight: 600; }
.alert .detail { color: var(--ink-2); font-size: 13.5px; }
.ok { background: var(--surface); border: 1px solid var(--border);
      border-left: 3px solid var(--good); border-radius: 9px;
      padding: 11px 14px; color: var(--ink-2); }
.ok strong { color: var(--good); }

table { width: 100%; border-collapse: collapse; background: var(--surface);
        border: 1px solid var(--border); border-radius: 11px; overflow: hidden;
        font-variant-numeric: tabular-nums; font-size: 13.5px; }
th, td { text-align: left; padding: 9px 14px; border-bottom: 1px solid var(--grid); }
th { color: var(--muted); font-weight: 600; font-size: 11.5px;
     letter-spacing: 0.06em; text-transform: uppercase; }
tbody tr:last-child td { border-bottom: none; }
td.num, th.num { text-align: right; }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; }
.tag { display: inline-block; font-size: 10.5px; letter-spacing: 0.05em;
       text-transform: uppercase; color: var(--series); border: 1px solid var(--series);
       border-radius: 4px; padding: 1px 5px; margin-left: 6px; vertical-align: 1px; }
.scroll { overflow-x: auto; }
.note { color: var(--muted); font-size: 12.5px; margin-top: 9px; }
.err { color: var(--warning); font-size: 13px; }

#tip { position: fixed; pointer-events: none; opacity: 0; transition: opacity .1s;
       background: var(--surface); color: var(--ink); border: 1px solid var(--border);
       border-radius: 7px; padding: 6px 9px; font-size: 12.5px;
       font-variant-numeric: tabular-nums; box-shadow: 0 4px 14px rgba(0,0,0,.4); z-index: 9; }
footer { margin-top: 44px; padding-top: 18px; border-top: 1px solid var(--grid);
         color: var(--muted); font-size: 12.5px; }
footer p { margin: 0 0 8px; }
footer a { color: var(--series); }
ul.news { list-style: none; margin: 0; padding: 0; display: flex;
          flex-direction: column; gap: 8px; }
ul.news li { background: var(--surface); border: 1px solid var(--border);
             border-radius: 9px; padding: 11px 14px; }
ul.news a { color: var(--ink); text-decoration: none; font-weight: 560; }
ul.news a:hover { color: var(--series); }
.news-sub { color: var(--ink-2); font-size: 13px; margin-top: 3px; }
"""

JS = """
(function () {
  var root = document.documentElement, tip = document.getElementById('tip');
  document.getElementById('themeBtn').addEventListener('click', function () {
    var dark = getComputedStyle(root).getPropertyValue('color-scheme').trim() === 'dark';
    root.setAttribute('data-theme', dark ? 'light' : 'dark');
  });

  document.querySelectorAll('.spark').forEach(function (svg) {
    var pts = JSON.parse(svg.dataset.points || '[]');
    if (!pts.length) return;
    var line = svg.querySelector('.cross'), dot = svg.querySelector('.dot');
    var hit = svg.querySelector('.hit');

    hit.addEventListener('pointermove', function (e) {
      var box = svg.getBoundingClientRect();
      var ratio = (e.clientX - box.left) / box.width;
      var i = Math.max(0, Math.min(pts.length - 1, Math.round(ratio * (pts.length - 1))));
      var p = pts[i];
      svg.classList.add('on');
      line.setAttribute('x1', p.x); line.setAttribute('x2', p.x);
      dot.setAttribute('cx', p.x); dot.setAttribute('cy', p.y);
      tip.textContent = p.v + '  ' + p.t;
      tip.style.opacity = 1;
      var w = tip.offsetWidth;
      tip.style.left = Math.min(window.innerWidth - w - 8, Math.max(8, e.clientX - w / 2)) + 'px';
      tip.style.top = (e.clientY - tip.offsetHeight - 12) + 'px';
    });
    hit.addEventListener('pointerleave', function () {
      svg.classList.remove('on');
      tip.style.opacity = 0;
      var last = pts[pts.length - 1];
      dot.setAttribute('cx', last.x); dot.setAttribute('cy', last.y);
    });
  });
})();
"""


def _esc(value: Any) -> str:
    return html_escape.escape(str(value), quote=True)


def _safe_url(url: Any) -> str:
    """Allow only http(s) links. Feed items are third-party content, and
    escaping alone would still permit a clickable javascript: URL."""
    text = str(url or "")
    return text if text.startswith(("https://", "http://")) else ""


def _fmt_usd(value: Any, decimals: int = 0) -> str:
    if value is None:
        return "n/a"
    try:
        value = float(value)
    except (TypeError, ValueError):
        return _esc(value)
    for unit, size in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(value) >= size:
            return "${:,.2f}{}".format(value / size, unit)
    return "${:,.{}f}".format(value, decimals)


def _fmt_num(value: Any, decimals: int = 0) -> str:
    """Format a number, tolerating whatever an upstream actually sent.

    Third-party values are not guaranteed numeric; a string here used to raise
    ValueError out of the renderer and take the whole run down.
    """
    if value is None:
        return "n/a"
    try:
        return "{:,.{}f}".format(float(value), decimals)
    except (TypeError, ValueError):
        return _esc(value)


def _sparkline(series: List[Dict[str, Any]], key: str, fmt, provenance: str = "local") -> str:
    """Single-series sparkline. Width 100% via viewBox; 34px tall.

    Draws nothing when there is no trend to show. Two cases count as "no
    trend": fewer than two readings, and every reading identical. The second
    matters more than it sounds -- slow-moving metrics repeat their value for
    hours, and a flat line sitting under a "+11.9% 24h" delta reads as a broken
    chart. Saying "no movement recorded" is both honest and more informative.

    `provenance` separates a provider's own daily series from this instance's
    polling history. They are different kinds of evidence and should not look
    identical: one is a month of real daily data, the other may be an hour of
    self-polling.
    """
    points = [(row.get("captured_at"), row.get(key)) for row in series if row.get(key) is not None]
    if len(points) < 2:
        return '<div class="no-history">Trend appears after 2+ readings</div>'
    try:
        distinct = len({v for _, v in points})
    except TypeError:
        distinct = 2  # unhashable values: treat as varying rather than crashing
    if distinct == 1:
        return '<div class="no-history">No movement across {} readings</div>'.format(len(points))

    w, h, pad = 240.0, 34.0, 4.0
    values = [v for _, v in points]
    lo, hi = min(values), max(values)
    step = w / (len(points) - 1)
    flat = hi == lo
    span = (hi - lo) or 1.0

    coords = []
    for i, (stamp, value) in enumerate(points):
        x = i * step
        # A perfectly stable series is drawn through the middle of the tile.
        # Normalising it against an artificial span pinned it to the bottom,
        # which reads as "bottomed out" rather than "unchanged".
        frac = 0.5 if flat else (value - lo) / span
        y = pad + (h - 2 * pad) * (1 - frac)
        coords.append({"x": round(x, 2), "y": round(y, 2), "v": fmt(value), "t": stamp or ""})

    path = " ".join("{},{}".format(c["x"], c["y"]) for c in coords)
    last = coords[-1]
    label = ("{} daily points from the data provider".format(len(coords))
             if provenance == "provider" else
             "{} readings collected by this instance".format(len(coords)))
    return (
        '<svg class="spark spark-{prov}" viewBox="0 0 {w} {h}" preserveAspectRatio="none" '
        'role="img" aria-label="{label}" '
        "data-points='{pts}'>"
        '<polyline class="line" points="{path}"/>'
        '<line class="cross" y1="0" y2="{h}" x1="0" x2="0"/>'
        '<circle class="dot" r="3" cx="{cx}" cy="{cy}"/>'
        '<rect class="hit" x="0" y="0" width="{w}" height="{h}"/>'
        "</svg>"
        '<div class="spark-src">{srctext}</div>'
    ).format(
        w=w, h=h, prov=provenance, label=label, pts=json.dumps(coords).replace("'", "&#39;"),
        path=path, cx=last["x"], cy=last["y"],
        srctext=("provider daily series" if provenance == "provider" else "collected here"),
    )


def _sparkline_from_series(points: List[Dict[str, Any]], fmt) -> str:
    """Sparkline over a provider-supplied {date, value} series.

    Distinct from _sparkline, which reads this instance's own run history. Data
    sourced from solana.com carries months of real history, so those tiles show
    a genuine trend from the first run rather than waiting for local readings to
    accumulate.
    """
    rows = [
        {"captured_at": p.get("date"), "v": p.get("value")}
        for p in points
        if p.get("value") is not None
    ]
    return _sparkline(rows, "v", fmt, provenance="provider")


def _tile(label: str, value: str, sub: str = "", spark: str = "") -> str:
    # value/sub carry pre-built markup from callers (deltas, sparklines), so they
    # are composed from already-escaped parts rather than escaped wholesale here.
    sub_html = '<div class="sub">{}</div>'.format(sub) if sub else ""
    return (
        '<div class="tile"><div class="label">{}</div>'
        '<div class="value">{}</div>{}{}</div>'
    ).format(_esc(label), value, sub_html, spark)


def _delta(value: Optional[float]) -> str:
    if value is None:
        return ""
    cls = "up" if value >= 0 else "down"
    arrow = "&#9650;" if value >= 0 else "&#9660;"
    return '<span class="delta {}">{} {:.2f}%</span> 24h'.format(cls, arrow, abs(value))


def render(snapshot: Dict[str, Any], findings: List[Dict[str, Any]], history: List[Dict[str, Any]]) -> str:
    chain = snapshot.get("chain", {})
    market = snapshot.get("market", {})
    perf = chain.get("performance", {})
    ep = chain.get("epoch", {})
    val = chain.get("validators", {})
    sup = chain.get("supply", {})
    price = market.get("price", {})
    tvl = market.get("tvl", {})
    dex = market.get("dex_volume", {})
    stables = market.get("stablecoins", {})
    fees = market.get("fees", {})
    rwa = market.get("tokenized_assets", {})
    act = chain.get("activity", {})
    tf = chain.get("transaction_fees", {})
    st = chain.get("slot_timing", {})
    eco = snapshot.get("ecosystem") or {}
    eco_metrics = eco.get("metrics") or {}
    news = snapshot.get("news") or {}
    up = snapshot.get("upgrades") or {}
    soc = snapshot.get("social") or {}

    # --- Alerts -----------------------------------------------------------
    if findings:
        alerts = "".join(
            '<div class="alert {sev}"><span class="icon">{label}</span>'
            '<span class="body"><span class="metric">{metric}</span> '
            '<span class="detail">{msg}</span></span></div>'.format(
                sev=_esc(f["severity"]),
                label=_esc(f["severity"].upper()),
                metric=_esc(f["metric"]),
                msg=_esc(f["message"]),
            )
            for f in findings
        )
    else:
        alerts = (
            '<div class="ok"><strong>All clear.</strong> '
            "No metric breached a threshold or deviated significantly from recent history.</div>"
        )

    # --- Headline tiles ---------------------------------------------------
    tiles = [
        _tile(
            "Non-vote TPS",
            _fmt_num(perf.get("tps_non_vote"), 1),
            "excludes consensus votes",
            _sparkline(history, "tps_non_vote", lambda v: "{:,.1f} TPS".format(v)),
        ),
        _tile(
            "SOL price",
            _fmt_usd(price.get("usd"), 2),
            _delta(price.get("change_24h_pct")),
            _sparkline(history, "price_usd", lambda v: "${:,.2f}".format(v)),
        ),
        _tile(
            "DeFi TVL",
            _fmt_usd(tvl.get("tvl_usd")),
            "rank #{} across chains".format(tvl.get("rank_by_tvl") or "?"),
            _sparkline(history, "tvl_usd", _fmt_usd),
        ),
        _tile(
            "Stablecoin supply",
            _fmt_usd(stables.get("total_usd")),
            "on Solana",
            _sparkline(history, "stablecoins_usd", _fmt_usd),
        ),
        _tile(
            "Delinquent validators",
            "{}%".format(_fmt_num(val.get("delinquent_pct"), 2)),
            "{} of {} active".format(
                _fmt_num(val.get("delinquent_count")), _fmt_num(val.get("active_count"))
            ),
            _sparkline(history, "delinquent_pct", lambda v: "{:.2f}%".format(v)),
        ),
        _tile(
            "Nakamoto coefficient",
            str(val.get("nakamoto_coefficient") or "n/a"),
            "validators to halt consensus",
            _sparkline(history, "nakamoto_coefficient", lambda v: "{:.0f}".format(v)),
        ),
        _tile(
            "Median priority fee",
            _fmt_num(tf.get("median_priority_fee_microlamports")),
            "micro-lamports/CU · {}% of slots need none".format(tf.get("zero_fee_slot_share_pct")),
        ),
        _tile(
            "Measured slot time",
            "{} s".format(_fmt_num(st.get("measured_slot_time_secs"), 4)),
            "via getBlockTime · {}% vs 0.4s target".format(st.get("deviation_from_target_pct")),
        ),
        _tile(
            "Avg slot time",
            "{} s".format(_fmt_num(perf.get("avg_slot_time_secs"), 4)),
            "target 0.4 s",
            _sparkline(history, "avg_slot_time_secs", lambda v: "{:.4f} s".format(v)),
        ),
        _tile(
            "DEX volume 24h",
            _fmt_usd(dex.get("volume_24h_usd")),
            "{} protocols tracked".format(dex.get("protocol_count") or "n/a"),
        ),
        _tile(
            "REV 24h",
            _fmt_usd(fees.get("rev_24h_usd")),
            "network fees + MEV tips",
            _sparkline(history, "rev_24h_usd", _fmt_usd),
        ),
        _tile(
            "App fees 24h",
            _fmt_usd(fees.get("app_fees_24h_usd")),
            _delta(fees.get("app_fees_change_24h_pct")) or "earned by apps, not the network",
        ),
        _tile(
            "Tokenized RWA",
            _fmt_usd(rwa.get("total_rwa_usd")),
            "{} protocols".format(rwa.get("protocol_count") or "n/a"),
            _sparkline(history, "rwa_total_usd", _fmt_usd),
        ),
        _tile(
            "Tokenized equities",
            _fmt_usd(rwa.get("equities_usd")),
            "{}% of tokenized RWA".format(rwa.get("equities_share_pct") or "n/a"),
            _sparkline(history, "equities_usd", _fmt_usd),
        ),
        _tile(
            "Live signers (sampled)",
            _fmt_num(act.get("unique_signers_sampled")),
            "right now, across {} sampled blocks".format(act.get("blocks_sampled") or "?"),
            _sparkline(history, "unique_signers_sampled", lambda v: "{:,.0f} signers".format(v)),
        ),
    ]

    # Daily active addresses come with 90 days of real provider history, so the
    # sparkline is drawn from that rather than from this instance's own runs.
    daa = eco_metrics.get("active_addresses")
    if daa:
        tiles.insert(
            0,
            _tile(
                "Daily active addresses",
                _fmt_num(daa.get("value")),
                "{} · {}".format(_esc(daa.get("date")), _esc(daa.get("provider"))),
                _sparkline_from_series(daa.get("history") or [], lambda v: "{:,.0f}".format(v)),
            ),
        )
    fee_payers = eco_metrics.get("fee_payers")
    if fee_payers:
        tiles.append(
            _tile(
                "Daily fee payers",
                _fmt_num(fee_payers.get("value")),
                "{} · {}".format(_esc(fee_payers.get("date")), _esc(fee_payers.get("provider"))),
                _sparkline_from_series(fee_payers.get("history") or [], lambda v: "{:,.0f}".format(v)),
            )
        )

    # --- Epoch ------------------------------------------------------------
    if "error" in ep:
        epoch_block = '<p class="err">Epoch data unavailable: {}</p>'.format(_esc(ep["error"]))
    else:
        pct = ep.get("progress_pct") or 0
        epoch_block = (
            '<div class="tile"><div class="label">Epoch {n}</div>'
            '<div class="value">{pct}%</div>'
            '<div class="sub">slot {i} of {t} &middot; ~{eta} h remaining</div>'
            '<svg class="spark" viewBox="0 0 240 12" preserveAspectRatio="none" role="img" '
            'aria-label="Epoch {n} is {pct} percent complete">'
            '<rect x="0" y="3" width="240" height="6" rx="3" fill="var(--grid)"/>'
            '<rect x="0" y="3" width="{w}" height="6" rx="3" fill="var(--series)"/>'
            "</svg></div>"
        ).format(
            n=_esc(ep.get("epoch")), pct=_esc(pct),
            i=_fmt_num(ep.get("slot_index")), t=_fmt_num(ep.get("slots_in_epoch")),
            eta=_esc(ep.get("eta_hours")), w=round(240 * float(pct or 0) / 100, 1),
        )

    # --- Validator table --------------------------------------------------
    rows = "".join(
        "<tr><td>{i}</td><td class='mono'>{acct}</td><td class='num'>{stake}</td>"
        "<td class='num'>{pct}%</td><td class='num'>{comm}%</td></tr>".format(
            i=i, acct=_esc(v.get("vote_account")), stake=_fmt_num(v.get("stake_sol")),
            pct=_esc(v.get("stake_pct")), comm=_esc(v.get("commission")),
        )
        for i, v in enumerate(val.get("top_validators", []), 1)
    )
    validator_table = (
        '<div class="scroll"><table><thead><tr><th>#</th><th>Vote account</th>'
        '<th class="num">Stake (SOL)</th><th class="num">Share</th>'
        '<th class="num">Commission</th></tr></thead><tbody>{}</tbody></table></div>'
    ).format(rows) if rows else '<p class="err">Validator data unavailable.</p>'

    # --- DEX table --------------------------------------------------------
    dex_rows = "".join(
        "<tr><td>{}</td><td class='num'>{}</td></tr>".format(
            _esc(d.get("name")), _fmt_usd(d.get("volume_24h_usd"))
        )
        for d in (dex.get("top_dexes") or [])
    )
    dex_table = (
        '<div class="scroll"><table><thead><tr><th>DEX</th>'
        '<th class="num">Volume 24h</th></tr></thead><tbody>{}</tbody></table></div>'
    ).format(dex_rows) if dex_rows else ""

    # --- Tokenized assets table -------------------------------------------
    rwa_rows = "".join(
        "<tr><td>{}{}</td><td class='num'>{}</td><td>{}</td></tr>".format(
            _esc(p.get("name")),
            ' <span class="tag">equity</span>' if p.get("is_equity") else "",
            _fmt_usd(p.get("tvl_usd")),
            _esc(p.get("category")),
        )
        for p in (rwa.get("top_protocols") or [])
    )
    rwa_table = (
        '<div class="scroll"><table><thead><tr><th>Protocol</th>'
        '<th class="num">Value</th><th>Category</th></tr></thead>'
        "<tbody>{}</tbody></table></div>"
    ).format(rwa_rows) if rwa_rows else "<p class='note'>No tokenized-asset data this run.</p>"

    # --- Degraded sections -------------------------------------------------
    # The docs promise a failed section reports why. Tiles fall back to "n/a",
    # which shows that something is missing but not what -- so failures are
    # collected and explained in one place.
    degraded = []
    for group in ("chain", "market"):
        for name, section in (snapshot.get(group) or {}).items():
            if isinstance(section, dict) and "error" in section:
                degraded.append((name, section["error"]))
    for group in ("ecosystem", "news", "upgrades", "social"):
        section = snapshot.get(group) or {}
        if "error" in section:
            degraded.append((group, section["error"]))

    degraded_block = (
        '<div class="alerts">{}</div>'.format(
            "".join(
                '<div class="alert warning"><span class="icon">UNAVAILABLE</span>'
                '<span class="body"><span class="metric">{}</span> '
                '<span class="detail">{}</span></span></div>'.format(_esc(n), _esc(e))
                for n, e in degraded
            )
        )
        if degraded
        else ""
    )

    # --- Provider divergence ----------------------------------------------
    div_rows = "".join(
        "<tr><td>{}</td><td>{}</td><td class='num'>{}%</td><td>{}</td></tr>".format(
            _esc(d["metric"]), _esc(d["date"]), d["spread_pct"],
            _esc(", ".join("{}: {:,.0f}".format(p, v) for p, v in d["by_provider"].items())),
        )
        for d in (eco.get("provider_divergence") or [])
    )
    divergence_block = (
        '<div class="scroll"><table><thead><tr><th>Metric</th><th>Date</th>'
        '<th class="num">Spread</th><th>Provider readings</th></tr></thead>'
        "<tbody>{}</tbody></table></div>"
        '<p class="note">The same metric is published by several providers with different '
        "methodologies. Where they disagree by more than 15% on the same day it is flagged "
        "here rather than hidden behind a single chosen number.</p>"
    ).format(div_rows) if div_rows else ""

    # --- News -------------------------------------------------------------
    news_items = "".join(
        '<li><a href="{}" target="_blank" rel="noopener">{}</a>'
        '<div class="news-sub">{}</div></li>'.format(
            _esc(_safe_url(i.get("link"))), _esc(i.get("title")), _esc(i.get("summary") or "")
        )
        for i in (news.get("items") or [])
    )
    news_block = (
        '<ul class="news">{}</ul>'
        '<p class="note">Source: official Solana news feed.</p>'
    ).format(news_items) if news_items else ""

    # --- Upcoming upgrades -------------------------------------------------
    upgrade_block = ""
    if "error" not in up and up.get("proposal_count"):
        versions = up.get("cluster_versions") or {}
        distinct = {v for v in versions.values() if v}
        version_line = " · ".join(
            "{} <strong>{}</strong>".format(_esc(c), _esc(v or "unknown")) for c, v in versions.items()
        )
        drift = (
            '<p class="note">Clusters are running different versions — a rollout in progress.</p>'
            if len(distinct) > 1 else ""
        )
        stat_tiles = "".join([
            _tile("Proposals tracked", _fmt_num(up.get("proposal_count")), "SIMD repository"),
            _tile("With a feature gate", _fmt_num(up.get("gated_count")), "switchable on-chain"),
            _tile("Live on mainnet", _fmt_num(up.get("active_on_mainnet")), "gates activated"),
            _tile("Awaiting mainnet", _fmt_num(up.get("pending_on_mainnet")), "gates pending"),
        ])
        highlight_rows = "".join(
            "<tr><td>SIMD-{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                _esc(h.get("simd")), _esc(h.get("title")), _esc(h.get("status")),
                _esc(", ".join("{}: {}".format(c, s) for c, s in (h.get("clusters") or {}).items())
                     or "no gate assigned yet"),
            )
            for h in (up.get("highlights") or [])
        )
        pending_rows = "".join(
            "<tr><td>SIMD-{}</td><td class='mono'>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                _esc(t.get("simd")), _esc(t.get("feature_name")),
                _esc((t.get("clusters") or {}).get("mainnet", "?")),
                _esc((t.get("clusters") or {}).get("testnet", "?")),
                _esc((t.get("clusters") or {}).get("devnet", "?")),
            )
            for t in (up.get("recently_pending") or [])
        )
        upgrade_block = (
            '<div class="grid">{tiles}</div>'
            '<p class="note" style="margin-top:14px">Cluster versions: {versions}</p>{drift}'
            '{hl_head}{hl}'
            '{pd_head}{pd}'
        ).format(
            tiles=stat_tiles, versions=version_line, drift=drift,
            hl_head="<h3>Named proposals</h3>" if highlight_rows else "",
            hl=('<div class="scroll"><table><thead><tr><th>SIMD</th><th>Title</th>'
                '<th>Status</th><th>Feature gate</th></tr></thead><tbody>{}</tbody></table></div>'
                '<p class="note">A proposal with no feature gate has not reached the point of '
                'being switchable on any cluster. Alpenglow is at that stage today.</p>'
                ).format(highlight_rows) if highlight_rows else "",
            pd_head="<h3>Gated features not yet live on mainnet</h3>" if pending_rows else "",
            pd=('<div class="scroll"><table><thead><tr><th>SIMD</th><th>Feature</th>'
                '<th>Mainnet</th><th>Testnet</th><th>Devnet</th></tr></thead>'
                '<tbody>{}</tbody></table></div>').format(pending_rows) if pending_rows else "",
        )

    # --- Announcements -----------------------------------------------------
    social_items = "".join(
        '<li><a href="{}" target="_blank" rel="noopener">@{}</a>'
        '<div class="news-sub">{}</div></li>'.format(
            _esc(_safe_url(p.get("url"))), _esc(p.get("handle")), _esc(p.get("text"))
        )
        for p in (soc.get("posts") or [])
    )
    social_block = (
        '<ul class="news">{}</ul>'
        '<p class="note">Announcements only — replies and retweets filtered. '
        "Source rate-limits intermittently; a failed account degrades this section alone.</p>"
    ).format(social_items) if social_items else ""

    # --- Full metric table (the accessible view of every tile) ------------
    supply_pct = sup.get("circulating_pct")
    table_rows = [
        ("Non-vote TPS", _fmt_num(perf.get("tps_non_vote"), 2)),
        ("Total TPS (incl. votes)", _fmt_num(perf.get("tps_total"), 2)),
        ("Vote share of transactions", "{}%".format(_fmt_num(perf.get("vote_share_pct"), 2))),
        ("Average slot time (perf samples)", "{} s".format(_fmt_num(perf.get("avg_slot_time_secs"), 4))),
        ("Measured slot time (getBlockTime)", "{} s".format(_fmt_num(st.get("measured_slot_time_secs"), 4))),
        ("Median priority fee (micro-lamports/CU)", _fmt_num(tf.get("median_priority_fee_microlamports"))),
        ("Slots needing no priority fee", "{}%".format(tf.get("zero_fee_slot_share_pct")) if tf.get("zero_fee_slot_share_pct") is not None else "n/a"),
        ("Current slot", _fmt_num(perf.get("current_slot"))),
        ("Block height", _fmt_num(perf.get("block_height"))),
        ("Active validators", _fmt_num(val.get("active_count"))),
        ("Delinquent validators", _fmt_num(val.get("delinquent_count"))),
        ("Total active stake", "{} SOL".format(_fmt_num(val.get("total_active_stake_sol")))),
        ("Nakamoto coefficient", str(val.get("nakamoto_coefficient") or "n/a")),
        ("Median commission", "{}%".format(val.get("median_commission")) if val.get("median_commission") is not None else "n/a"),
        ("SOL price", _fmt_usd(price.get("usd"), 2)),
        ("Market cap", _fmt_usd(price.get("market_cap_usd"))),
        ("DeFi TVL", _fmt_usd(tvl.get("tvl_usd"))),
        ("DEX volume 24h", _fmt_usd(dex.get("volume_24h_usd"))),
        ("Stablecoin supply", _fmt_usd(stables.get("total_usd"))),
        ("REV 24h (network fees + MEV tips)", _fmt_usd(fees.get("rev_24h_usd"))),
        ("  of which network fees", _fmt_usd(fees.get("network_fees_24h_usd"))),
        ("  of which MEV tips", _fmt_usd(fees.get("mev_tips_24h_usd"))),
        ("Annualised REV run-rate", _fmt_usd(fees.get("rev_annualised_usd"))),
        ("Application fees 24h (not network revenue)", _fmt_usd(fees.get("app_fees_24h_usd"))),
        ("Tokenized RWA total", _fmt_usd(rwa.get("total_rwa_usd"))),
        ("Tokenized equities", _fmt_usd(rwa.get("equities_usd"))),
        ("Daily active addresses", _fmt_num((eco_metrics.get("active_addresses") or {}).get("value"))),
        ("Daily fee payers", _fmt_num((eco_metrics.get("fee_payers") or {}).get("value"))),
        ("Live signers (sampled, not daily)", _fmt_num(act.get("unique_signers_sampled"))),
        ("Non-vote share of sampled txs", "{}%".format(act.get("non_vote_share_pct")) if act.get("non_vote_share_pct") is not None else "n/a"),
        ("Circulating supply", "{} SOL{}".format(
            _fmt_num(sup.get("circulating_sol")),
            " ({}%)".format(supply_pct) if supply_pct else "")),
    ]
    metric_table = (
        '<div class="scroll"><table><thead><tr><th>Metric</th>'
        '<th class="num">Value</th></tr></thead><tbody>{}</tbody></table></div>'
    ).format(
        "".join(
            "<tr><td>{}</td><td class='num'>{}</td></tr>".format(_esc(k), _esc(v))
            for k, v in table_rows
        )
    )

    return """<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Solana Ecosystem Dashboard — SolVitals</title>
<meta name="description" content="Auto-updating report on the state of the Solana ecosystem: network health, validators, REV, tokenized assets, and live feature-gate activation across mainnet, testnet and devnet.">
<meta property="og:title" content="SolVitals — Solana Ecosystem Dashboard">
<meta property="og:description" content="Network health, validators, REV, tokenized assets, and live feature-gate activation. Refreshes every 15 minutes. Python stdlib only.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://techbronick.github.io/solvitals/">
<meta name="twitter:card" content="summary">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%231a1a19'/%3E%3Cpath d='M4 20l5-6 5 4 5-9 5 7 4-3' fill='none' stroke='%233987e5' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
<style>{css}</style>
</head>
<body>
<div class="wrap">
  <header>
    <div>
      <h1>Solana Ecosystem Dashboard</h1>
      <div class="stamp">Updated {stamp} UTC &middot; {runs} readings recorded</div>
    </div>
    <button class="toggle" id="themeBtn" type="button">Toggle theme</button>
  </header>

  <h2>Alerts</h2>
  {alerts}

  {degraded_heading}
  {degraded}

  <h2>Key metrics</h2>
  <div class="grid">{tiles}</div>

  <h2>Epoch progress</h2>
  <div class="grid">{epoch}</div>

  {upgrade_heading}
  {upgrades}

  <h2>Top validators by stake</h2>
  {validators}
  <p class="note">The Nakamoto coefficient is the number of validators that would need to
  collude to control 33% of stake and halt consensus. Higher is more decentralised.</p>

  <h2>Top DEXes by 24h volume</h2>
  {dex}

  <h2>Tokenized real-world assets</h2>
  {rwa}
  <p class="note">Tokenized equities are broken out from treasuries, credit and
  commodities, which dominate the RWA category overall.</p>

  {divergence_heading}
  {divergence}

  {news_heading}
  {news}

  {social_heading}
  {social}


  <h2>All metrics</h2>
  {metrics}

  <footer>
    <p><strong>Other output formats:</strong>
      <a href="report.md">Markdown report</a> ·
      <a href="report.json">JSON</a> ·
      <a href="history.jsonl">metric history</a> ·
      <a href="https://github.com/techbronick/solvitals">source on GitHub</a>
    </p>
    <p>Sources: Solana JSON-RPC (mainnet-beta), solana.com/data, solana.com/news,
    CoinGecko, DeFiLlama. No API keys required, Python standard library only.
    Tiles sourced from this instance's own history show {runs} readings; tiles
    sourced from solana.com carry the provider's own daily series.</p>
  </footer>
</div>
<div id="tip"></div>
<script>{js}</script>
</body>
</html>""".format(
        css=CSS, js=JS, stamp=_esc(snapshot.get("captured_at")), runs=len(history),
        alerts=alerts, tiles="".join(tiles), epoch=epoch_block,
        degraded=degraded_block,
        degraded_heading="<h2>Unavailable this run</h2>" if degraded_block else "",
        validators=validator_table, dex=dex_table or "<p class='note'>No DEX data this run.</p>",
        rwa=rwa_table, metrics=metric_table,
        divergence=divergence_block,
        divergence_heading="<h2>Where data providers disagree</h2>" if divergence_block else "",
        news=news_block,
        news_heading="<h2>Ecosystem and community news</h2>" if news_block else "",
        social=social_block,
        social_heading="<h2>Announcements from key accounts</h2>" if social_block else "",
        upgrades=upgrade_block,
        upgrade_heading="<h2>Upcoming upgrades and protocol changes</h2>" if upgrade_block else "",
    )
