"""Human-readable Markdown report."""

from typing import Any, Dict, List

SEVERITY_ICON = {"critical": "[CRITICAL]", "warning": "[WARNING]", "info": "[INFO]"}


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


def _fmt_delta(value: Any) -> str:
    if value is None:
        return ""
    arrow = "up" if value >= 0 else "down"
    return " ({} {:.2f}%)".format(arrow, abs(value))


def _section_error(data: Dict[str, Any]) -> str:
    return "> Unavailable this run: {}\n".format(data["error"])


def render(snapshot: Dict[str, Any], findings: List[Dict[str, Any]]) -> str:
    chain = snapshot.get("chain", {})
    market = snapshot.get("market", {})
    lines = [
        "# Solana Ecosystem Report",
        "",
        "Generated {} UTC by SolPulse.".format(snapshot.get("captured_at")),
        "",
    ]

    # Anomalies lead: if something is wrong, it should be the first thing read.
    lines.append("## Alerts")
    lines.append("")
    if findings:
        for f in findings:
            lines.append(
                "- {} **{}** — {}".format(
                    SEVERITY_ICON.get(f["severity"], "[INFO]"), f["metric"], f["message"]
                )
            )
    else:
        lines.append("No anomalies detected against configured thresholds and recent history.")
    lines.append("")

    perf = chain.get("performance", {})
    lines.append("## Network Performance")
    lines.append("")
    if "error" in perf:
        lines.append(_section_error(perf))
    else:
        lines.extend(
            [
                "| Metric | Value |",
                "| --- | --- |",
                "| Non-vote TPS | {} |".format(_fmt_num(perf.get("tps_non_vote"), 2)),
                "| Total TPS (incl. votes) | {} |".format(_fmt_num(perf.get("tps_total"), 2)),
                "| Vote share of transactions | {}% |".format(_fmt_num(perf.get("vote_share_pct"), 2)),
                "| Average slot time | {} s |".format(_fmt_num(perf.get("avg_slot_time_secs"), 4)),
                "| Current slot | {} |".format(_fmt_num(perf.get("current_slot"))),
                "| Block height | {} |".format(_fmt_num(perf.get("block_height"))),
                "",
                "_Non-vote TPS is the figure that reflects user activity; consensus votes are "
                "transactions on Solana and inflate the raw count._",
            ]
        )
    lines.append("")

    ep = chain.get("epoch", {})
    lines.append("## Epoch")
    lines.append("")
    if "error" in ep:
        lines.append(_section_error(ep))
    else:
        filled = int(round(ep.get("progress_pct", 0) / 5))
        lines.extend(
            [
                "Epoch **{}** — {}% complete (`{}{}`), ~{} hours remaining.".format(
                    ep.get("epoch"),
                    ep.get("progress_pct"),
                    "#" * filled,
                    "." * (20 - filled),
                    ep.get("eta_hours"),
                ),
                "",
                "Slot {} of {}. Lifetime transaction count: {}.".format(
                    _fmt_num(ep.get("slot_index")),
                    _fmt_num(ep.get("slots_in_epoch")),
                    _fmt_num(ep.get("transaction_count")),
                ),
            ]
        )
    lines.append("")

    val = chain.get("validators", {})
    lines.append("## Validators")
    lines.append("")
    if "error" in val:
        lines.append(_section_error(val))
    else:
        lines.extend(
            [
                "| Metric | Value |",
                "| --- | --- |",
                "| Active validators | {} |".format(_fmt_num(val.get("active_count"))),
                "| Delinquent validators | {} ({}%) |".format(
                    _fmt_num(val.get("delinquent_count")), _fmt_num(val.get("delinquent_pct"), 2)
                ),
                "| Stake held by delinquents | {} SOL ({}%) |".format(
                    _fmt_num(val.get("delinquent_stake_sol")), _fmt_num(val.get("delinquent_stake_pct"), 3)
                ),
                "| Total active stake | {} SOL |".format(_fmt_num(val.get("total_active_stake_sol"))),
                "| Nakamoto coefficient | {} |".format(val.get("nakamoto_coefficient")),
                "| Median commission | {}% |".format(val.get("median_commission")),
                "| Zero-commission validators | {} |".format(_fmt_num(val.get("zero_commission_count"))),
                "",
                "_The Nakamoto coefficient is the number of validators that would need to collude "
                "to control 33% of stake and halt consensus. Higher is more decentralised._",
                "",
                "### Top validators by stake",
                "",
                "| # | Vote account | Stake (SOL) | Share | Commission |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for i, v in enumerate(val.get("top_validators", []), 1):
            lines.append(
                "| {} | `{}` | {} | {}% | {}% |".format(
                    i,
                    v.get("vote_account"),
                    _fmt_num(v.get("stake_sol")),
                    v.get("stake_pct"),
                    v.get("commission"),
                )
            )
    lines.append("")

    lines.append("## Economics")
    lines.append("")
    price = market.get("price", {})
    tvl = market.get("tvl", {})
    dex = market.get("dex_volume", {})
    stables = market.get("stablecoins", {})
    lines.extend(["| Metric | Value |", "| --- | --- |"])
    lines.append(
        "| SOL price | {}{} |".format(
            _fmt_usd(price.get("usd"), 2) if "error" not in price else "n/a",
            _fmt_delta(price.get("change_24h_pct")),
        )
    )
    lines.append("| Market cap | {} |".format(_fmt_usd(price.get("market_cap_usd"))))
    lines.append("| DeFi TVL | {} |".format(_fmt_usd(tvl.get("tvl_usd"))))
    lines.append(
        "| TVL rank across chains | {} |".format(tvl.get("rank_by_tvl") or "n/a")
    )
    lines.append(
        "| DEX volume (24h) | {}{} |".format(
            _fmt_usd(dex.get("volume_24h_usd")), _fmt_delta(dex.get("change_24h_pct"))
        )
    )
    lines.append("| Stablecoin supply | {} |".format(_fmt_usd(stables.get("total_usd"))))
    lines.append("")

    fees = market.get("fees", {})
    if "error" not in fees:
        lines.extend(
            [
                "### Network fees (REV)",
                "",
                "| Window | Fees |",
                "| --- | --- |",
                "| 24 hours | {}{} |".format(
                    _fmt_usd(fees.get("fees_24h_usd")), _fmt_delta(fees.get("change_24h_pct"))
                ),
                "| 7 days | {} |".format(_fmt_usd(fees.get("fees_7d_usd"))),
                "| 30 days | {} |".format(_fmt_usd(fees.get("fees_30d_usd"))),
                "| Annualised run-rate | {} |".format(_fmt_usd(fees.get("annualised_usd"))),
                "",
                "_{}_".format(fees.get("note", "")),
                "",
            ]
        )
        if fees.get("top_fee_earners"):
            lines.extend(["| Top fee earner | Fees (24h) |", "| --- | --- |"])
            for p in fees["top_fee_earners"]:
                lines.append("| {} | {} |".format(p.get("name"), _fmt_usd(p.get("fees_24h_usd"))))
            lines.append("")

    rwa = market.get("tokenized_assets", {})
    if "error" not in rwa:
        lines.extend(
            [
                "## Tokenized assets",
                "",
                "| Metric | Value |",
                "| --- | --- |",
                "| Total tokenized RWA | {} |".format(_fmt_usd(rwa.get("total_rwa_usd"))),
                "| Tokenized equities | {} ({}% of RWA) |".format(
                    _fmt_usd(rwa.get("equities_usd")), rwa.get("equities_share_pct")
                ),
                "| RWA protocols on Solana | {} |".format(rwa.get("protocol_count")),
                "",
            ]
        )
        if rwa.get("equity_protocols"):
            lines.extend(
                ["### Tokenized equity issuers", "", "| Protocol | Value | 24h |", "| --- | --- | --- |"]
            )
            for p in rwa["equity_protocols"]:
                lines.append(
                    "| {} | {} | {}% |".format(
                        p.get("name"), _fmt_usd(p.get("tvl_usd")), p.get("change_24h_pct")
                    )
                )
            lines.append("")
        if rwa.get("top_protocols"):
            lines.extend(
                ["### Largest tokenized-asset protocols", "", "| Protocol | Value | Category |", "| --- | --- | --- |"]
            )
            for p in rwa["top_protocols"]:
                lines.append(
                    "| {} | {} | {} |".format(
                        p.get("name"), _fmt_usd(p.get("tvl_usd")), p.get("category")
                    )
                )
            lines.append("")

    act = chain.get("activity", {})
    if "error" not in act:
        lines.extend(
            [
                "## Address activity",
                "",
                "| Metric | Value |",
                "| --- | --- |",
                "| Unique fee payers (sampled) | {} |".format(_fmt_num(act.get("unique_signers_sampled"))),
                "| Blocks sampled | {} |".format(act.get("blocks_sampled")),
                "| Transactions in sample | {} |".format(_fmt_num(act.get("transactions_sampled"))),
                "| Non-vote share of sample | {}% |".format(act.get("non_vote_share_pct")),
                "| Signers per block | {} |".format(act.get("signers_per_block")),
                "",
                "_{}_".format(act.get("note", "")),
                "",
            ]
        )

    if dex.get("top_dexes"):
        lines.extend(["### Top DEXes by 24h volume", "", "| DEX | Volume (24h) |", "| --- | --- |"])
        for d in dex["top_dexes"]:
            lines.append("| {} | {} |".format(d.get("name"), _fmt_usd(d.get("volume_24h_usd"))))
        lines.append("")

    sup = chain.get("supply", {})
    if "error" not in sup:
        lines.extend(
            [
                "## Supply",
                "",
                "Circulating {} SOL of {} total ({}%).".format(
                    _fmt_num(sup.get("circulating_sol")),
                    _fmt_num(sup.get("total_sol")),
                    sup.get("circulating_pct"),
                ),
                "",
            ]
        )

    eco = snapshot.get("ecosystem") or {}
    if "error" not in eco and eco.get("metrics"):
        m = eco["metrics"]
        lines.extend(
            [
                "## Ecosystem growth (solana.com/data)",
                "",
                "| Metric | Value | As of | Provider |",
                "| --- | --- | --- | --- |",
            ]
        )
        for key in (
            "active_addresses", "fee_payers", "transactions_total", "non_vote_success",
            "non_vote_failed", "dex_volume", "dex_traders", "transfer_volume",
            "total_stake", "validator_count", "top3_asn_share",
        ):
            if key not in m:
                continue
            row = m[key]
            unit = row.get("unit") or ""
            value = row.get("value")
            shown = _fmt_usd(value) if unit.lower() in ("usd", "dollars") else _fmt_num(value, 2 if unit == "Percent" else 0)
            lines.append(
                "| {} | {} | {} | {} |".format(row.get("label"), shown, row.get("date"), row.get("provider"))
            )
        lines.append("")
        lines.append(
            "_Daily active addresses are deduplicated across the full day by the provider — "
            "distinct from the live block sample below, which measures current activity._"
        )
        lines.append("")

        if eco.get("provider_divergence"):
            lines.extend(
                [
                    "### Where providers disagree",
                    "",
                    "The same metric is published by multiple providers with different "
                    "methodologies. Divergences above threshold on the same day:",
                    "",
                    "| Metric | Date | Spread | Provider readings |",
                    "| --- | --- | --- | --- |",
                ]
            )
            for d in eco["provider_divergence"]:
                readings = ", ".join(
                    "{}: {:,.0f}".format(p, v) for p, v in d["by_provider"].items()
                )
                lines.append(
                    "| {} | {} | {}% | {} |".format(d["metric"], d["date"], d["spread_pct"], readings)
                )
            lines.append("")

    news = snapshot.get("news") or {}
    if "error" not in news and news.get("items"):
        lines.extend(["## Ecosystem and community news", ""])
        for item in news["items"]:
            lines.append("- **[{}]({})**".format(item["title"], item["link"]))
            if item.get("summary"):
                lines.append("  {}".format(item["summary"]))
        lines.append("")
        lines.append("_Source: official Solana news feed (solana.com/news)._")
        lines.append("")

    lines.extend(
        [
            "## Sources",
            "",
            "| Section | Source | Key required |",
            "| --- | --- | --- |",
            "| Performance, epoch, validators, supply, address sample | Solana JSON-RPC (mainnet-beta) | No |",
            "| SOL price and market cap | CoinGecko public API | No |",
            "| TVL, DEX volume, stablecoins, fees, tokenized assets | DeFiLlama public API | No |",
            "| Daily active addresses, ecosystem growth (incl. Dune-computed) | solana.com/data | No |",
            "| Ecosystem and community news | solana.com/news RSS | No |",
            "",
        ]
    )
    return "\n".join(lines)
