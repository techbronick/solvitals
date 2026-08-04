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
  --serious:     #ec835a;
  --critical:    #d03b3b;
}
:root[data-theme="light"] {
  color-scheme: light;
  --page: #f9f9f7; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e;
  --muted: #898781; --grid: #e1e0d9; --axis: #c3c2b7;
  --border: rgba(11,11,11,0.10); --series: #2a78d6; --good: #006300;
}
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
    color-scheme: light;
    --page: #f9f9f7; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e;
    --muted: #898781; --grid: #e1e0d9; --axis: #c3c2b7;
    --border: rgba(11,11,11,0.10); --series: #2a78d6; --good: #006300;
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
.scroll { overflow-x: auto; }
.note { color: var(--muted); font-size: 12.5px; margin-top: 9px; }
.err { color: var(--serious); font-size: 13px; }

#tip { position: fixed; pointer-events: none; opacity: 0; transition: opacity .1s;
       background: var(--surface); color: var(--ink); border: 1px solid var(--border);
       border-radius: 7px; padding: 6px 9px; font-size: 12.5px;
       font-variant-numeric: tabular-nums; box-shadow: 0 4px 14px rgba(0,0,0,.4); z-index: 9; }
footer { margin-top: 44px; padding-top: 18px; border-top: 1px solid var(--grid);
         color: var(--muted); font-size: 12.5px; }
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
      tip.innerHTML = '<strong>' + p.v + '</strong><br>' + p.t;
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


def _fmt_usd(value: Any, decimals: int = 0) -> str:
    if value is None:
        return "n/a"
    for unit, size in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(value) >= size:
            return "${:,.2f}{}".format(value / size, unit)
    return "${:,.{}f}".format(value, decimals)


def _fmt_num(value: Any, decimals: int = 0) -> str:
    if value is None:
        return "n/a"
    return "{:,.{}f}".format(value, decimals)


def _sparkline(series: List[Dict[str, Any]], key: str, fmt) -> str:
    """Single-series sparkline. Width 100% via viewBox; 34px tall.

    Fewer than two points is not a trend, so the tile says so rather than
    drawing a misleading flat line.
    """
    points = [(row.get("captured_at"), row.get(key)) for row in series if row.get(key) is not None]
    if len(points) < 2:
        return '<div class="no-history">Trend appears after 2+ runs</div>'

    w, h, pad = 240.0, 34.0, 4.0
    values = [v for _, v in points]
    lo, hi = min(values), max(values)
    span = (hi - lo) or (abs(hi) or 1) * 0.02
    step = w / (len(points) - 1)

    coords = []
    for i, (stamp, value) in enumerate(points):
        x = i * step
        y = pad + (h - 2 * pad) * (1 - (value - lo) / span)
        coords.append({"x": round(x, 2), "y": round(y, 2), "v": fmt(value), "t": stamp or ""})

    path = " ".join("{},{}".format(c["x"], c["y"]) for c in coords)
    last = coords[-1]
    return (
        '<svg class="spark" viewBox="0 0 {w} {h}" preserveAspectRatio="none" '
        'role="img" aria-label="Trend over the last {n} readings" '
        "data-points='{pts}'>"
        '<polyline class="line" points="{path}"/>'
        '<line class="cross" y1="0" y2="{h}" x1="0" x2="0"/>'
        '<circle class="dot" r="3" cx="{cx}" cy="{cy}"/>'
        '<rect class="hit" x="0" y="0" width="{w}" height="{h}"/>'
        "</svg>"
    ).format(
        w=w, h=h, n=len(coords), pts=json.dumps(coords).replace("'", "&#39;"),
        path=path, cx=last["x"], cy=last["y"],
    )


def _tile(label: str, value: str, sub: str = "", spark: str = "") -> str:
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
    ]

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
            n=_esc(ep.get("epoch")), pct=pct,
            i=_fmt_num(ep.get("slot_index")), t=_fmt_num(ep.get("slots_in_epoch")),
            eta=ep.get("eta_hours"), w=round(240 * pct / 100, 1),
        )

    # --- Validator table --------------------------------------------------
    rows = "".join(
        "<tr><td>{i}</td><td class='mono'>{acct}</td><td class='num'>{stake}</td>"
        "<td class='num'>{pct}%</td><td class='num'>{comm}%</td></tr>".format(
            i=i, acct=_esc(v.get("vote_account")), stake=_fmt_num(v.get("stake_sol")),
            pct=v.get("stake_pct"), comm=v.get("commission"),
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

    # --- Full metric table (the accessible view of every tile) ------------
    supply_pct = sup.get("circulating_pct")
    table_rows = [
        ("Non-vote TPS", _fmt_num(perf.get("tps_non_vote"), 2)),
        ("Total TPS (incl. votes)", _fmt_num(perf.get("tps_total"), 2)),
        ("Vote share of transactions", "{}%".format(_fmt_num(perf.get("vote_share_pct"), 2))),
        ("Average slot time", "{} s".format(_fmt_num(perf.get("avg_slot_time_secs"), 4))),
        ("Current slot", _fmt_num(perf.get("current_slot"))),
        ("Block height", _fmt_num(perf.get("block_height"))),
        ("Active validators", _fmt_num(val.get("active_count"))),
        ("Delinquent validators", _fmt_num(val.get("delinquent_count"))),
        ("Total active stake", "{} SOL".format(_fmt_num(val.get("total_active_stake_sol")))),
        ("Nakamoto coefficient", str(val.get("nakamoto_coefficient") or "n/a")),
        ("Median commission", "{}%".format(val.get("median_commission"))),
        ("SOL price", _fmt_usd(price.get("usd"), 2)),
        ("Market cap", _fmt_usd(price.get("market_cap_usd"))),
        ("DeFi TVL", _fmt_usd(tvl.get("tvl_usd"))),
        ("DEX volume 24h", _fmt_usd(dex.get("volume_24h_usd"))),
        ("Stablecoin supply", _fmt_usd(stables.get("total_usd"))),
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
<title>Solana Ecosystem Dashboard</title>
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

  <h2>Key metrics</h2>
  <div class="grid">{tiles}</div>

  <h2>Epoch progress</h2>
  <div class="grid">{epoch}</div>

  <h2>Top validators by stake</h2>
  {validators}
  <p class="note">The Nakamoto coefficient is the number of validators that would need to
  collude to control 33% of stake and halt consensus. Higher is more decentralised.</p>

  <h2>Top DEXes by 24h volume</h2>
  {dex}

  <h2>All metrics</h2>
  {metrics}

  <footer>
    Generated by SolPulse. Sources: Solana JSON-RPC (mainnet-beta), CoinGecko, DeFiLlama.
    No API keys required. Sparklines show the last {runs} readings from this
    instance's own history.
  </footer>
</div>
<div id="tip"></div>
<script>{js}</script>
</body>
</html>""".format(
        css=CSS, js=JS, stamp=_esc(snapshot.get("captured_at")), runs=len(history),
        alerts=alerts, tiles="".join(tiles), epoch=epoch_block,
        validators=validator_table, dex=dex_table or "<p class='note'>No DEX data this run.</p>",
        metrics=metric_table,
    )
