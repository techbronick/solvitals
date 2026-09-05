# Solana Ecosystem Report

Generated 2026-09-05 05:54:58 UTC by SolVitals.

## Alerts

- [CRITICAL] **stablecoins_usd** — stablecoins_usd is 3.7 sigma above its 288-point mean
- [CRITICAL] **rwa_total_usd** — rwa_total_usd is 5.5 sigma above its 288-point mean
- [WARNING] **tps_non_vote** — tps_non_vote is 2.1 sigma below its 288-point mean
- [WARNING] **rev_24h_usd** — rev_24h_usd is 2.8 sigma below its 287-point mean
- [WARNING] **equities_usd** — equities_usd is 2.7 sigma above its 288-point mean

## Network Performance

| Metric | Value |
| --- | --- |
| Non-vote TPS | 936.62 |
| Total TPS (incl. votes) | 3,089.33 |
| Vote share of transactions | 69.68% |
| Average slot time | 0.3132 s |
| Current slot | 444,444,318 |
| Block height | 422,489,171 |

_Non-vote TPS is the figure that reflects user activity; consensus votes are transactions on Solana and inflate the raw count._

## Epoch

Epoch **1028** — 80.63% complete (`################....`), ~7.3 hours remaining.

Slot 348,318 of 432,000. Lifetime transaction count: 545,305,791,846.

## Transaction costs and slot timing

| Metric | Value |
| --- | --- |
| Median priority fee | 0 micro-lamports/CU |
| 75th percentile | 0 |
| 95th percentile | 0 |
| Slots needing no priority fee | 100.0% |
| Median total fee (200k CU, 1 sig) | 5e-06 SOL |
| Measured slot time (`getBlockTime`) | 0.3146 s |
| Deviation from 0.4s target | -21.35% |

_Priority fees are per compute unit in micro-lamports. Median total assumes a 200k CU transaction with one signature._

### Watched account

`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` (SPL Token program) — balance 0.1988 SOL, 10 recent signatures, 2 with errors.

## Validators

| Metric | Value |
| --- | --- |
| Active validators | 677 |
| Delinquent validators | 18 (2.59%) |
| Stake held by delinquents | 141,013 SOL (0.032%) |
| Total active stake | 436,757,852 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Zero-commission validators | 244 |

_The Nakamoto coefficient is the number of validators that would need to collude to control 33% of stake and halt consensus. Higher is more decentralised._

### Top validators by stake

| # | Vote account | Stake (SOL) | Share | Commission |
| --- | --- | --- | --- | --- |
| 1 | `CcaHc2L43ZWjwCHART3oZoJvHLAe9hzT2DJNUpBzoTN1` | 17,393,318 | 3.982% | 7% |
| 2 | `he1iusunGwqrNtafDtLdhsUQDFvo13z9sUa36PauBtk` | 16,324,259 | 3.738% | 0% |
| 3 | `3N7s9zXMZ4QqvHQR15t5GNHyqc89KduzMP7423eWiD5g` | 12,459,602 | 2.853% | 0% |
| 4 | `CatzoSMUkTRidT5DwBxAC2pEtnwMBTpkCepHkFgZDiqb` | 11,379,843 | 2.606% | 5% |
| 5 | `8GbwASqdpw4dVcwbWUxbHXMrjyQx2aKkoBR5H1GJF8iD` | 9,567,623 | 2.191% | 0% |
| 6 | `26pV97Ce83ZQ6Kz9XT4td8tdoUFPTng8Fb8gPyc53dJx` | 9,278,151 | 2.124% | 7% |
| 7 | `51JBzSTU5rAM8gLAVQKgp4WoZerQcSqWC7BitBzgUNAm` | 9,042,760 | 2.07% | 10% |
| 8 | `9QU2QSxhb24FUX3Tu2FpczXjpK3VYrvRudywSZaM29mF` | 7,376,879 | 1.689% | 7% |
| 9 | `CvSb7wdQAFpHuSpTYTJnX5SYH4hCfQ9VuGnqrKaKwycB` | 7,127,366 | 1.632% | 5% |
| 10 | `DumiCKHVqoCQKD8roLApzR5Fit8qGV5fVQsJV9sTZk4a` | 6,593,517 | 1.51% | 0% |

## Economics

| Metric | Value |
| --- | --- |
| SOL price | $101.82 (down 1.59%) |
| Market cap | $59.61B |
| DeFi TVL | $5.86B |
| TVL rank across chains | 2 |
| DEX volume (24h) | $1.85B (down 24.89%) |
| Stablecoin supply | $16.32B |

### Real Economic Value (REV)

| Component | 24h |
| --- | --- |
| **REV (total)** | **$651.59K** |
| Network fees | $531.25K |
| MEV tips (out-of-protocol) | $120.35K (18.47% of REV) |
| Annualised REV run-rate | $237.83M |

_REV is what the **network** captures. It is a different and much smaller figure than fees earned by applications built on Solana, which follow separately -- conflating the two overstates REV by more than 10x._

| MEV source | Tips (24h) |
| --- | --- |
| Jito MEV Tips | $105.88K |
| Harmonic | $10.57K |
| bloXroute | $3.89K |

### Application fees (distinct from REV)

Fees earned by the 310 applications built on Solana -- DEXes, launchpads, wallets and bots. Economically interesting, but not network revenue.

| Window | Application fees |
| --- | --- |
| 24 hours | $9.54M (down 19.33%) |
| 7 days | $80.71M |
| 30 days | $338.06M |

| Top fee-earning app | Fees (24h) |
| --- | --- |
| PumpSwap | $2.84M |
| fomo Wallet | $1.33M |
| pump.fun | $928.13K |
| Axiom | $554.79K |
| Solana | $531.25K |

## Tokenized assets

| Metric | Value |
| --- | --- |
| Total tokenized RWA | $2.36B |
| Tokenized equities | $473.40M (20.07% of RWA) |
| RWA protocols on Solana | 26 |

### Tokenized equity issuers

| Protocol | Value | 24h |
| --- | --- | --- |
| xStocks | $447.08M | -2.518% |
| Ondo Global Markets | $25.84M | -1.035% |
| Remora Markets | $481.80K | -0.351% |

### Largest tokenized-asset protocols

| Protocol | Value | Category |
| --- | --- | --- |
| BlackRock BUIDL | $977.90M | RWA |
| xStocks | $447.08M | RWA |
| OnRe | $298.55M | RWA |
| Huma Finance V2 | $192.14M | RWA |
| Ondo Yield Assets | $179.98M | RWA |
| Hastra | $150.48M | RWA |
| Ondo Global Markets | $25.84M | RWA |
| Plume Vaults | $23.99M | RWA |
| Apollo Diversified Credit Securitize Fund | $18.39M | RWA |
| VanEck Treasury Fund | $13.95M | RWA |

## Address activity

| Metric | Value |
| --- | --- |
| Unique fee payers (sampled) | 1,439 |
| Blocks sampled | 3 |
| Transactions in sample | 3,613 |
| Non-vote share of sample | 41.02% |
| Signers per block | 479.7 |

_Unique fee payers across sampled blocks -- an activity indicator, not a 24h unique-address count._

### Top DEXes by 24h volume

| DEX | Volume (24h) |
| --- | --- |
| PumpSwap | $310.67M |
| BisonFi | $232.51M |
| Orca DEX | $228.55M |
| Meteora DLMM | $180.66M |
| Manifest Trade | $156.93M |

## Supply

Circulating 585,359,743 SOL of 633,454,768 total (92.41%).

## Ecosystem growth (solana.com/data)

| Metric | Value | As of | Provider |
| --- | --- | --- | --- |
| Active Addresses | 885,022 | 2026-09-03 | Dune |
| Fee Payers | 2,437,125 | 2026-09-03 | Dune |
| Transaction Count (Total) | 322,525,919 | 2026-09-03 | Dune |
| Non Vote Transaction Count (Success) | 89,693,427 | 2026-09-03 | Dune |
| Non Vote Transaction Count (Failed) | 48,604,841 | 2026-09-03 | Dune |
| DEX Volume | $2.00B | 2026-09-03 | Dune |
| DEX Traders | 836,551 | 2026-09-03 | Dune |
| Transfer Volume | $21.36B | 2026-09-03 | Dune |
| Total Stake | 438,416,978 | 2026-09-03 | Solscan |
| Validator Count | 675 | 2026-09-04 | Stakewiz |
| Top 3 ASN Share | 46.44 | 2026-09-04 | Stakewiz |

_Daily active addresses are deduplicated across the full day by the provider — distinct from the live block sample below, which measures current activity._

### Where providers disagree

The same metric is published by multiple providers with different methodologies. Divergences above threshold on the same day:

| Metric | Date | Spread | Provider readings |
| --- | --- | --- | --- |
| Active Addresses | 2026-09-03 | 89.7% | Allium: 894,816, Blockworks: 471,798, Dune: 885,022, Goldsky: 885,778, RWA: 886,281 |

## Announcements from key accounts

- **@solana** — JUST IN: @SuperteamAU has helped launch the Buy Australian AI Partnership as a founding partner, alongside the National AI Centre, Stone & Chalk and four of Australia's major banks. [(link)](https://x.com/solana/status/2095738924177973409)
- **@solana** — https://t.co/MwACdPIoC3 [(link)](https://x.com/solana/status/2095698458686652891)
- **@solanalabs** — CLOCK IN - a Solana Mobile Hackathon by @RadiantsDAO is coming 🔜 September 8 - October 8 It’s almost time to clock-in. https://t.co/bTj0T14Ib8 https://t.co/yw2x79n83C [(link)](https://x.com/solanalabs/status/2095546195229716737)
- **@solana** — $607M traded on Jupiter Mobile in August! Month after month, the story's the same, people trade on the fastest, cheapest choice. Just Use Jupiter (Mobile). 📲 https://t.co/L7dRNFz9fa [(link)](https://x.com/solana/status/2095542334956179524)
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
- **[Solana Changelog: August 20, 2026](https://solana.com/news/solana-changelog-august-20-2026)**
  Feature gates reduced mainnet slot times from 400ms to 350ms, while Agave, Firedancer, and Solana Kit shipped updates.
- **[Resource and Inclusion Fee: Digging into Data](https://solana.com/news/resource-and-inclusion-fee-digging-into-data)**
  Here we dive into implications related to the SGP-0003 (namely resource and inclusion fee).

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
