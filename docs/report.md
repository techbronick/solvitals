# Solana Ecosystem Report

Generated 2026-08-19 17:16:04 UTC by SolVitals.

## Alerts

- [CRITICAL] **price_usd** — price_usd is 5.5 sigma above its 287-point mean
- [CRITICAL] **tvl_usd** — tvl_usd is 6.0 sigma above its 288-point mean
- [WARNING] **tps_non_vote** — tps_non_vote is 3.0 sigma above its 288-point mean

## Network Performance

| Metric | Value |
| --- | --- |
| Non-vote TPS | 3,785.25 |
| Total TPS (incl. votes) | 5,413.10 |
| Vote share of transactions | 30.07% |
| Average slot time | 0.4196 s |
| Current slot | 440,306,729 |
| Block height | 418,356,754 |

_Non-vote TPS is the figure that reflects user activity; consensus votes are transactions on Solana and inflate the raw count._

## Epoch

Epoch **1019** — 22.85% complete (`#####...............`), ~38.5 hours remaining.

Slot 98,730 of 432,000. Lifetime transaction count: 539,682,662,623.

## Transaction costs and slot timing

| Metric | Value |
| --- | --- |
| Median priority fee | 0 micro-lamports/CU |
| 75th percentile | 0 |
| 95th percentile | 0 |
| Slots needing no priority fee | 100.0% |
| Median total fee (200k CU, 1 sig) | 5e-06 SOL |
| Measured slot time (`getBlockTime`) | 0.4154 s |
| Deviation from 0.4s target | 3.85% |

_Priority fees are per compute unit in micro-lamports. Median total assumes a 200k CU transaction with one signature._

### Watched account

`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` (SPL Token program) — balance 0.1928 SOL, 10 recent signatures, 6 with errors.

## Validators

| Metric | Value |
| --- | --- |
| Active validators | 686 |
| Delinquent validators | 9 (1.29%) |
| Stake held by delinquents | 429,073 SOL (0.099%) |
| Total active stake | 434,812,195 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Zero-commission validators | 255 |

_The Nakamoto coefficient is the number of validators that would need to collude to control 33% of stake and halt consensus. Higher is more decentralised._

### Top validators by stake

| # | Vote account | Stake (SOL) | Share | Commission |
| --- | --- | --- | --- | --- |
| 1 | `CcaHc2L43ZWjwCHART3oZoJvHLAe9hzT2DJNUpBzoTN1` | 17,101,527 | 3.933% | 7% |
| 2 | `he1iusunGwqrNtafDtLdhsUQDFvo13z9sUa36PauBtk` | 16,011,570 | 3.682% | 0% |
| 3 | `CatzoSMUkTRidT5DwBxAC2pEtnwMBTpkCepHkFgZDiqb` | 12,410,378 | 2.854% | 5% |
| 4 | `3N7s9zXMZ4QqvHQR15t5GNHyqc89KduzMP7423eWiD5g` | 12,198,972 | 2.806% | 0% |
| 5 | `26pV97Ce83ZQ6Kz9XT4td8tdoUFPTng8Fb8gPyc53dJx` | 9,188,631 | 2.113% | 7% |
| 6 | `51JBzSTU5rAM8gLAVQKgp4WoZerQcSqWC7BitBzgUNAm` | 8,991,290 | 2.068% | 10% |
| 7 | `8GbwASqdpw4dVcwbWUxbHXMrjyQx2aKkoBR5H1GJF8iD` | 8,308,413 | 1.911% | 0% |
| 8 | `9QU2QSxhb24FUX3Tu2FpczXjpK3VYrvRudywSZaM29mF` | 7,991,430 | 1.838% | 7% |
| 9 | `CvSb7wdQAFpHuSpTYTJnX5SYH4hCfQ9VuGnqrKaKwycB` | 7,344,654 | 1.689% | 5% |
| 10 | `DumiCKHVqoCQKD8roLApzR5Fit8qGV5fVQsJV9sTZk4a` | 6,546,146 | 1.506% | 0% |

## Economics

| Metric | Value |
| --- | --- |
| SOL price | $81.37 (up 5.79%) |
| Market cap | $47.46B |
| DeFi TVL | $5.05B |
| TVL rank across chains | 2 |
| DEX volume (24h) | $1.84B (up 24.62%) |
| Stablecoin supply | $15.45B |

### Real Economic Value (REV)

| Component | 24h |
| --- | --- |
| **REV (total)** | **$789.17K** |
| Network fees | $649.17K |
| MEV tips (out-of-protocol) | $140.00K (17.74% of REV) |
| Annualised REV run-rate | $288.05M |

_REV is what the **network** captures. It is a different and much smaller figure than fees earned by applications built on Solana, which follow separately -- conflating the two overstates REV by more than 10x._

| MEV source | Tips (24h) |
| --- | --- |
| Jito MEV Tips | $119.86K |
| Harmonic | $12.81K |
| bloXroute | $7.32K |
| Pyth Express Relay | $0 |

### Application fees (distinct from REV)

Fees earned by the 295 applications built on Solana -- DEXes, launchpads, wallets and bots. Economically interesting, but not network revenue.

| Window | Application fees |
| --- | --- |
| 24 hours | $8.77M (down 22.25%) |
| 7 days | $62.89M |
| 30 days | $250.65M |

| Top fee-earning app | Fees (24h) |
| --- | --- |
| PumpSwap | $2.61M |
| pump.fun | $1.51M |
| Axiom | $1.31M |
| Solana | $649.17K |
| Phantom Wallet | $544.74K |

## Tokenized assets

| Metric | Value |
| --- | --- |
| Total tokenized RWA | $1.88B |
| Tokenized equities | $412.47M (21.92% of RWA) |
| RWA protocols on Solana | 25 |

### Tokenized equity issuers

| Protocol | Value | 24h |
| --- | --- | --- |
| xStocks | $383.12M | -0.345% |
| Ondo Global Markets | $29.35M | 0.543% |

### Largest tokenized-asset protocols

| Protocol | Value | Category |
| --- | --- | --- |
| BlackRock BUIDL | $741.42M | RWA |
| xStocks | $383.12M | RWA |
| OnRe | $270.31M | RWA |
| Ondo Yield Assets | $179.07M | RWA |
| Hastra | $171.99M | RWA |
| Ondo Global Markets | $29.35M | RWA |
| Theo Network thBill | $26.37M | RWA |
| Nest Credit | $22.46M | RWA |
| Apollo Diversified Credit Securitize Fund | $18.32M | RWA |
| VanEck Treasury Fund | $13.93M | RWA |

## Address activity

| Metric | Value |
| --- | --- |
| Unique fee payers (sampled) | 1,726 |
| Blocks sampled | 3 |
| Transactions in sample | 6,219 |
| Non-vote share of sample | 67.34% |
| Signers per block | 575.3 |

_Unique fee payers across sampled blocks -- an activity indicator, not a 24h unique-address count._

### Top DEXes by 24h volume

| DEX | Volume (24h) |
| --- | --- |
| PumpSwap | $698.60M |
| BisonFi | $241.78M |
| HumidiFi | $160.54M |
| Orca DEX | $109.96M |
| Raydium AMM | $97.92M |

## Supply

Circulating 583,007,094 SOL of 632,514,347 total (92.17%).

## Ecosystem growth (solana.com/data)

| Metric | Value | As of | Provider |
| --- | --- | --- | --- |
| Active Addresses | 651,869 | 2026-08-18 | Dune |
| Fee Payers | 2,508,175 | 2026-08-18 | Dune |
| Transaction Count (Total) | 317,794,113 | 2026-08-18 | Dune |
| Non Vote Transaction Count (Success) | 100,016,033 | 2026-08-18 | Dune |
| Non Vote Transaction Count (Failed) | 75,593,485 | 2026-08-18 | Dune |
| DEX Volume | $1.25B | 2026-08-18 | Dune |
| DEX Traders | 623,352 | 2026-08-18 | Dune |
| Transfer Volume | $12.02B | 2026-08-18 | Dune |
| Total Stake | 434,953,370 | 2026-08-19 | Stakewiz |
| Validator Count | 680 | 2026-08-19 | Stakewiz |
| Top 3 ASN Share | 35.79 | 2026-08-19 | Stakewiz |

_Daily active addresses are deduplicated across the full day by the provider — distinct from the live block sample below, which measures current activity._

## Announcements from key accounts

- **@solana** — MoneyGram CEO Anthony Soohoo on connecting cash to Solana: "The biggest announcement we've made with Solana is about access, providing all their developers the ability to build on our MoneyGram network." "Anyone building on Solana can use … [(link)](https://x.com/solana/status/2090033619792523378)
- **@solana** — We’ve crossed 30% of @Solana’s daily DEX aggregator volume for the first time, reflecting growing demand for competitive routing, reliable execution, and broader market access onchain. [(link)](https://x.com/solana/status/2089941783874773230)
- **@solana** — Looking for companies doing the following + building on @solana: - Using AI to underwrite lower-cost personal + small business loans - Securitizing compute - KYA (KYC for agents) - Markets for GPU inference - Data center tokenization or fi… [(link)](https://x.com/solana/status/2089938286282526971)
- **@solana** — BREAKING: @MoneyGram Ramps is live on Solana. 60M+ customers, nearly 500,000 retail locations, 170+ countries. One of the world's largest payments networks is now a single API away for every builder on Solana. https://t.co/TSOhIpBjvz [(link)](https://x.com/solana/status/2087163225393750405)
- **@solanalabs** — Shipped Live episode 3 is coming 🔜 Tomorrow August 11 at 11am EST The latest on the Solana Mobile ecosystem, featuring: - @beeman_nl - @web4O - @inno_sol Sign up now 👇 https://t.co/dVQgaOulNi [(link)](https://x.com/solanalabs/status/2086893782742757446)
- **@solanalabs** — Crack open the map with @lootgo_official 🏴‍☠️ Hunt down loot boxes, drop SKR Boosters, and stack rewards while you do it. New Seeker Summer R3 Quests: ↳ Loot Goblin: Open up 5 loot boxes ↳ Boost Seeker: Buy + deploy 1 SKR Booster on the ma… [(link)](https://x.com/solanalabs/status/2084686710630400035)
- **@solanalabs** — Three months in the Incubator > three years figuring it out alone – 3 months of hands-on mentorship from Solana OGs IRL in NYC – Weekly workshops, office hours, and 1:1s – Demo day in front of the ecosystem's top VCs and builders Apply now… [(link)](https://x.com/solanalabs/status/2046985139029479873)
- **@solanalabs** — 1/ Grow your company alongside the Solana Labs team! Applications for Cohort 5 of the Solana Incubator are now open — join us in NYC for 3 months starting September 2026. 📅 Deadline: June 5. ✅ Rolling review — early applicants prioritized.… [(link)](https://x.com/solanalabs/status/2046973323620577341)

_Announcements only; replies and retweets filtered. The endpoint rate-limits intermittently, so a failed account degrades this section alone and the cached copy is reused._

## Upcoming upgrades and protocol changes

| Metric | Value |
| --- | --- |
| Improvement proposals tracked | 123 |
| With an assigned feature gate | 33 |
| Gates live on mainnet | 22 |
| Gates awaiting mainnet | 11 |

### Proposals by status

| Status | Count |
| --- | --- |
| Review | 51 |
| Activated | 25 |
| Implemented | 14 |
| Idea | 13 |
| Accepted | 9 |
| Withdrawn | 5 |
| Draft | 3 |
| Living | 2 |
| Stagnant | 1 |

**Cluster versions:** mainnet `4.2.0` · testnet `4.2.0` · devnet `4.2.0`

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

## Ecosystem and community news

- **[Lowering Slot Time and Validators Economic](https://solana.com/news/lowering-slot-time-and-validators-economic)**
  Solana will reduce its slot times from 400ms to 200ms. This change will make the protocol more competitive in terms of latency. Here we explore some possible implication on validators economic.
- **[Transaction v1 and the ALT Trade-off](https://solana.com/news/transaction-v1-and-the-alt-trade-off)**
- **[Solana Changelog: August 13, 2026](https://solana.com/news/solana-changelog-august-13-2026)**
  Slot times to 250ms on testnet and releases from Agave and Firedancer.
- **[How Meow Built Agentic Banking and Agent Payment Rails, with Brandon Arvanaghi](https://solana.com/news/how-meow-built-agentic-banking-and-agent-payment-rails-with-brandon-arvanaghi)**
  Meow lets AI agents form a company and apply for a business bank account in one prompt, with payment rails spanning ACH, USDC, SOL, and more.
- **[Why Asia Is Ahead on Stablecoins, According to Reap's Daren Guo](https://solana.com/news/bits-to-bricks-asia-ahead-stablecoins-daren-guo-reap)**
  Reap moves roughly $6B a year in stablecoin card volume after building cross-border payments infrastructure from Asia.
- **[MoneyGram Ramps launches on Solana](https://solana.com/news/moneygram-ramps)**
  MoneyGram Ramps gives Solana builders one API for cash deposits in 25+ countries and withdrawals in 170+ countries and territories.
- **[Solana Changelog: August 6, 2026](https://solana.com/news/solana-changelog-august-6-2026)**
  Agave, Firedancer, Frankendancer, SDK, and testing-tool releases shipped as 350ms slot-time gates reached Devnet and Testnet.
- **[Webinar Recap: Giving AI agents a native way to pay with x402](https://solana.com/news/webinar-recap-agentic-payments)**
  X402 has processed roughly 200M transactions and $50B in volume, giving AI agents a stablecoin-native way to pay for web resources.

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
