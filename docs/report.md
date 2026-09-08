# Solana Ecosystem Report

Generated 2026-09-08 00:20:21 UTC by SolVitals.

## Alerts

- [WARNING] **stablecoins_usd** — stablecoins_usd is 2.7 sigma above its 288-point mean
- [WARNING] **rwa_total_usd** — rwa_total_usd is 2.9 sigma above its 288-point mean
- [WARNING] **equities_usd** — equities_usd is 2.0 sigma above its 288-point mean
- [WARNING] **unique_signers_sampled** — unique_signers_sampled is 2.8 sigma above its 288-point mean

## Network Performance

| Metric | Value |
| --- | --- |
| Non-vote TPS | 1,905.06 |
| Total TPS (incl. votes) | 4,020.43 |
| Vote share of transactions | 52.62% |
| Average slot time | 0.3178 s |
| Current slot | 445,200,199 |
| Block height | 423,244,363 |

_Non-vote TPS is the figure that reflects user activity; consensus votes are transactions on Solana and inflate the raw count._

## Epoch

Epoch **1030** — 55.6% complete (`###########.........`), ~16.8 hours remaining.

Slot 240,199 of 432,000. Lifetime transaction count: 546,170,890,114.

## Transaction costs and slot timing

| Metric | Value |
| --- | --- |
| Median priority fee | 0 micro-lamports/CU |
| 75th percentile | 0 |
| 95th percentile | 0 |
| Slots needing no priority fee | 100.0% |
| Median total fee (200k CU, 1 sig) | 5e-06 SOL |
| Measured slot time (`getBlockTime`) | 0.316 s |
| Deviation from 0.4s target | -21.0% |

_Priority fees are per compute unit in micro-lamports. Median total assumes a 200k CU transaction with one signature._

### Watched account

`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` (SPL Token program) — balance 0.1988 SOL, 10 recent signatures, 3 with errors.

## Validators

| Metric | Value |
| --- | --- |
| Active validators | 676 |
| Delinquent validators | 12 (1.74%) |
| Stake held by delinquents | 49,529 SOL (0.011%) |
| Total active stake | 439,428,459 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Zero-commission validators | 243 |

_The Nakamoto coefficient is the number of validators that would need to collude to control 33% of stake and halt consensus. Higher is more decentralised._

### Top validators by stake

| # | Vote account | Stake (SOL) | Share | Commission |
| --- | --- | --- | --- | --- |
| 1 | `CcaHc2L43ZWjwCHART3oZoJvHLAe9hzT2DJNUpBzoTN1` | 17,438,541 | 3.968% | 7% |
| 2 | `he1iusunGwqrNtafDtLdhsUQDFvo13z9sUa36PauBtk` | 16,336,964 | 3.718% | 0% |
| 3 | `3N7s9zXMZ4QqvHQR15t5GNHyqc89KduzMP7423eWiD5g` | 12,517,399 | 2.849% | 0% |
| 4 | `CatzoSMUkTRidT5DwBxAC2pEtnwMBTpkCepHkFgZDiqb` | 11,397,824 | 2.594% | 5% |
| 5 | `8GbwASqdpw4dVcwbWUxbHXMrjyQx2aKkoBR5H1GJF8iD` | 9,564,412 | 2.177% | 0% |
| 6 | `26pV97Ce83ZQ6Kz9XT4td8tdoUFPTng8Fb8gPyc53dJx` | 9,181,909 | 2.09% | 7% |
| 7 | `51JBzSTU5rAM8gLAVQKgp4WoZerQcSqWC7BitBzgUNAm` | 9,038,443 | 2.057% | 10% |
| 8 | `9QU2QSxhb24FUX3Tu2FpczXjpK3VYrvRudywSZaM29mF` | 7,384,461 | 1.68% | 7% |
| 9 | `CvSb7wdQAFpHuSpTYTJnX5SYH4hCfQ9VuGnqrKaKwycB` | 6,858,929 | 1.561% | 5% |
| 10 | `DumiCKHVqoCQKD8roLApzR5Fit8qGV5fVQsJV9sTZk4a` | 6,595,421 | 1.501% | 0% |

## Economics

| Metric | Value |
| --- | --- |
| SOL price | $103.78 (down 2.25%) |
| Market cap | $60.83B |
| DeFi TVL | $5.91B |
| TVL rank across chains | 2 |
| DEX volume (24h) | $2.90B (up 55.76%) |
| Stablecoin supply | $16.39B |

### Real Economic Value (REV)

| Component | 24h |
| --- | --- |
| **REV (total)** | **$792.18K** |
| Network fees | $653.15K |
| MEV tips (out-of-protocol) | $139.04K (17.55% of REV) |
| Annualised REV run-rate | $289.15M |

_REV is what the **network** captures. It is a different and much smaller figure than fees earned by applications built on Solana, which follow separately -- conflating the two overstates REV by more than 10x._

| MEV source | Tips (24h) |
| --- | --- |
| Jito MEV Tips | $121.43K |
| Harmonic | $12.30K |
| bloXroute | $5.30K |

### Application fees (distinct from REV)

Fees earned by the 310 applications built on Solana -- DEXes, launchpads, wallets and bots. Economically interesting, but not network revenue.

| Window | Application fees |
| --- | --- |
| 24 hours | $14.66M (up 44.97%) |
| 7 days | $84.28M |
| 30 days | $348.01M |

| Top fee-earning app | Fees (24h) |
| --- | --- |
| PumpSwap | $3.14M |
| fomo Wallet | $2.00M |
| Raydium AMM | $1.61M |
| Meteora DLMM | $1.15M |
| Axiom | $959.52K |

## Tokenized assets

| Metric | Value |
| --- | --- |
| Total tokenized RWA | $2.36B |
| Tokenized equities | $474.15M (20.07% of RWA) |
| RWA protocols on Solana | 25 |

### Tokenized equity issuers

| Protocol | Value | 24h |
| --- | --- | --- |
| xStocks | $448.00M | -0.79% |
| Ondo Global Markets | $26.15M | -0.18% |

### Largest tokenized-asset protocols

| Protocol | Value | Category |
| --- | --- | --- |
| BlackRock BUIDL | $977.90M | RWA |
| xStocks | $448.00M | RWA |
| OnRe | $302.49M | RWA |
| Huma Finance V2 | $186.52M | RWA |
| Ondo Yield Assets | $179.70M | RWA |
| Hastra | $154.84M | RWA |
| Ondo Global Markets | $26.15M | RWA |
| Plume Vaults | $24.03M | RWA |
| Apollo Diversified Credit Securitize Fund | $18.38M | RWA |
| VanEck Treasury Fund | $13.95M | RWA |

## Address activity

| Metric | Value |
| --- | --- |
| Unique fee payers (sampled) | 2,044 |
| Blocks sampled | 3 |
| Transactions in sample | 4,340 |
| Non-vote share of sample | 53.04% |
| Signers per block | 681.3 |

_Unique fee payers across sampled blocks -- an activity indicator, not a 24h unique-address count._

### Top DEXes by 24h volume

| DEX | Volume (24h) |
| --- | --- |
| PumpSwap | $677.89M |
| Raydium AMM | $307.82M |
| BisonFi | $241.45M |
| Orca DEX | $236.61M |
| Meteora DLMM | $223.09M |

## Supply

Circulating 586,165,658 SOL of 633,642,937 total (92.51%).

## Ecosystem growth (solana.com/data)

| Metric | Value | As of | Provider |
| --- | --- | --- | --- |
| Active Addresses | 853,180 | 2026-09-06 | Dune |
| Fee Payers | 2,102,185 | 2026-09-06 | Dune |
| Transaction Count (Total) | 316,700,650 | 2026-09-06 | Dune |
| Non Vote Transaction Count (Success) | 96,026,748 | 2026-09-06 | Dune |
| Non Vote Transaction Count (Failed) | 37,253,729 | 2026-09-06 | Dune |
| DEX Volume | $2.27B | 2026-09-06 | Dune |
| DEX Traders | 795,658 | 2026-09-06 | Dune |
| Transfer Volume | $10.13B | 2026-09-06 | Dune |
| Total Stake | 439,250,223 | 2026-09-06 | Solscan |
| Validator Count | 674 | 2026-09-07 | Stakewiz |
| Top 3 ASN Share | 43.87 | 2026-09-07 | Stakewiz |

_Daily active addresses are deduplicated across the full day by the provider — distinct from the live block sample below, which measures current activity._

### Where providers disagree

The same metric is published by multiple providers with different methodologies. Divergences above threshold on the same day:

| Metric | Date | Spread | Provider readings |
| --- | --- | --- | --- |
| Active Addresses | 2026-09-06 | 92.3% | Allium: 858,456, Artemis: 772,633, Blockworks: 482,520, Dune: 853,180, Goldsky: 853,777, RWA: 928,010 |
| Fee Payers | 2026-09-06 | 103.3% | Allium: 2,102,218, Artemis: 4,252,585, Blockworks: 2,092,204, Dune: 2,102,185, Token Terminal: 2,122,213 |

## Announcements from key accounts

- **@solana** — Start the week with @WSOP poker https://t.co/sAXVEGov7T [(link)](https://x.com/solana/status/2097063901279997970)
- **@solana** — https://t.co/5oeNnYguvf [(link)](https://x.com/solana/status/2097037299435585682)
- **@solana** — make a confidential transfer. on Solana. Right now. live on https://t.co/vhoQ701uCC https://t.co/G8ULcG7kEc [(link)](https://x.com/solana/status/2097015389448183872)
- **@solanalabs** — CLOCK IN - a Solana Mobile Hackathon by @RadiantsDAO is coming 🔜 September 8 - October 8 It’s almost time to clock-in. https://t.co/bTj0T14Ib8 https://t.co/yw2x79n83C [(link)](https://x.com/solanalabs/status/2095546195229716737)
- **@solana** — $166,946.50 raised for Nepal flood relief. Thank you to everyone that took part. Your logos will be up on our pfp and pinned post for the next week. https://t.co/YssiVQk9eH [(link)](https://x.com/solana/status/2095173372158394780)
- **@solanalabs** — Welcome and a big congrats to the incredible teams in Cohort 5 🥳 Follow @incubator for updates on their progress and to stay in the loop on all things Solana Incubator. [(link)](https://x.com/solanalabs/status/2094856511587860600)
- **@solanalabs** — Introducing Cohort 5 of the Solana Incubator. Our most competitive pool yet — founders building across AI, robotics, and trading on @solana. Day one of working with these teams: 🟣@clawpumptech 🟣@crowdbrainai 🟣@Lavaragexyz 🟣@morfimarkets 🟣@… [(link)](https://x.com/solanalabs/status/2094842504025694668)
- **@solanalabs** — Introducing Cohort 5 of the Solana Incubator. Our most competitive pool yet — founders building across AI, robotics, and trading on @solana. Day one of working with these teams: 🟣@clawpumptech 🟣@crowdbrainai 🟣@Lavaragexyz 🟣@morfimarkets 🟣@… [(link)](https://x.com/solanalabs/status/2094842504025694668)

_Announcements only; replies and retweets filtered. The endpoint rate-limits intermittently, so a failed account degrades this section alone and the cached copy is reused._

## Upcoming upgrades and protocol changes

| Metric | Value |
| --- | --- |
| Improvement proposals tracked | 125 |
| With an assigned feature gate | 34 |
| Gates live on mainnet | 22 |
| Gates awaiting mainnet | 12 |

### Proposals by status

| Status | Count |
| --- | --- |
| Review | 51 |
| Activated | 25 |
| Implemented | 14 |
| Idea | 14 |
| Accepted | 9 |
| Withdrawn | 5 |
| Draft | 4 |
| Living | 2 |
| Stagnant | 1 |

**Cluster versions:** mainnet `4.2.2` · testnet `4.3.0-beta.3` · devnet `4.3.0-beta.3`

_Clusters are running different versions, which is itself a rollout-in-progress signal._

### Named proposals

| SIMD | Title | Status | Feature gate |
| --- | --- | --- | --- |
| SIMD-0326 | Alpenglow | Review | no gate assigned yet |
| SIMD-0337 | Markers for Alpenglow Fast Leader Handover | Review | no gate assigned yet |
| SIMD-0357 | Alpenglow Validator Admission Ticket | Review | no gate assigned yet |
| SIMD-0384 | Alpenglow migration | Review | mainnet: not created, testnet: not created, devnet: not created |
| SIMD-0525 | Reduce Slot Times | Draft | no gate assigned yet |

_A proposal with no feature gate has not reached the point of being switchable on any cluster. Alpenglow is at that stage today._

### Gated features not yet live on mainnet

| SIMD | Feature | Mainnet | Testnet | Devnet |
| --- | --- | --- | --- | --- |
| SIMD-0163 | `None` | not created | not created | not created |
| SIMD-0178 | `None` | not created | not created | not created |
| SIMD-0189 | `None` | not created | not created | not created |
| SIMD-0219 | `None` | not created | not created | not created |
| SIMD-0268 | `raise_cpi_nesting_limit_to_8` | not created | not created | not created |
| SIMD-0290 | `relax_fee_payer_constraint` | not created | not created | not created |
| SIMD-0384 | `None` | not created | not created | not created |
| SIMD-0387 | `None` | not created | not created | not created |
| SIMD-0406 | `None` | not created | not created | not created |
| SIMD-0430 | `None` | not created | not created | not created |
| SIMD-0529 | `enable_big_mod_exp_syscall` | not created | not created | not created |
| SIMD-0599 | `None` | not created | not created | not created |

## Ecosystem and community news

- **[# How BitRobot Crowdsources Real-World Data for Embodied AI, with Jonathan Victor](https://solana.com/news/bits-to-bricks-bitrobot-jonathan-victor)**
  BitRobot open-sourced 2,000 hours of robot navigation data and uses Solana to track and reward embodied AI data contributors.
- **[Solana Ecosystem Roundup: August 2026](https://solana.com/news/solana-ecosystem-roundup-august-2026)**
  Solana’s August 2026 roundup: record transactions, $4B in RWAs, growing stablecoin payments, tokenized stocks, DeFi innovation, ETFs, and governance.
- **[Payment Channels: 1 Million Payments Per Second](https://solana.com/news/payment-channels-1-million-payments-per-second)**
  Payment channels support 1 million payments per second by authorizing agent spending once.
- **[How to Reclaim Excess SOL After Rent Reduction](https://solana.com/news/how-to-reclaim-excess-sol-after-rent-reduction)**
  Rent on Solana has been Reduced. Every Account Is Now Over-Funded. Here's How to Reclaim Excess SOL.
- **[The Token Supercycle: Everything of Value is Becoming Programmable](https://solana.com/news/the-token-supercycle-oped)**
  More than $4.7 trillion in stablecoins moved across Solana in the past year as tokenized markets expand access to ownership and finance.
- **[Webinar Recap: Cross-Border Payments in Latin America](https://solana.com/news/webinar-recap-cross-border-payments-in-latin-america)**
  Jorge Borges, Head of Latin America at Fireblocks, and Antonio Neto of the Solana Foundation discussed how firms across LATAM are putting stablecoin payments into production.
- **[Solana Changelog: August 27, 2026](https://solana.com/news/solana-changelog-august-27-2026)**
  V1 Transactions are approaching, while a 300ms slot-time feature gate reached Mainnet and new releases shipped across Solana tooling.
- **[The Token Supercycle Is Here: Solana Brings Breakpoint 2026 to London](https://solana.com/news/breakpoint-2026-london-speakers)**
  Breakpoint comes to London November 15–17, bringing 8,000+ attendees and leaders from capital markets, payments, technology and policy.

_Source: official Solana news feed (solana.com/news)._

## Sources

| Section | Source | Key required |
| --- | --- | --- |
| Performance, epoch, validators, supply, address sample | Solana JSON-RPC (mainnet-beta) | No |
| SOL price and market cap | CoinGecko public API | No |
| TVL, DEX volume, stablecoins, fees, tokenized assets | DeFiLlama public API | No |
| Daily active addresses, ecosystem growth (incl. Dune-computed) | solana.com/data | No |
| Ecosystem and community news | solana.com/news RSS | No |
| Upcoming upgrades | SIMD repo + Agave feature-set + live RPC | No |
| Announcements from key accounts | x.com syndication timeline | No |
