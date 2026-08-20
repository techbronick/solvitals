# Solana Ecosystem Report

Generated 2026-08-20 15:22:31 UTC by SolVitals.

## Alerts

- [CRITICAL] **tvl_usd** — tvl_usd is 3.3 sigma above its 288-point mean
- [CRITICAL] **rev_24h_usd** — rev_24h_usd is 3.0 sigma above its 288-point mean
- [WARNING] **price_usd** — price_usd is 3.0 sigma above its 287-point mean
- [WARNING] **equities_usd** — equities_usd is 2.8 sigma above its 288-point mean

## Network Performance

| Metric | Value |
| --- | --- |
| Non-vote TPS | 3,114.92 |
| Total TPS (incl. votes) | 4,724.64 |
| Vote share of transactions | 34.07% |
| Average slot time | 0.4255 s |
| Current slot | 440,498,043 |
| Block height | 418,547,865 |

_Non-vote TPS is the figure that reflects user activity; consensus votes are transactions on Solana and inflate the raw count._

## Epoch

Epoch **1019** — 67.14% complete (`#############.......`), ~16.5 hours remaining.

Slot 290,044 of 432,000. Lifetime transaction count: 540,005,586,637.

## Transaction costs and slot timing

| Metric | Value |
| --- | --- |
| Median priority fee | 0 micro-lamports/CU |
| 75th percentile | 0 |
| 95th percentile | 0 |
| Slots needing no priority fee | 100.0% |
| Median total fee (200k CU, 1 sig) | 5e-06 SOL |
| Measured slot time (`getBlockTime`) | 0.4184 s |
| Deviation from 0.4s target | 4.6% |

_Priority fees are per compute unit in micro-lamports. Median total assumes a 200k CU transaction with one signature._

### Watched account

`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` (SPL Token program) — balance 0.1928 SOL, 10 recent signatures, 7 with errors.

## Validators

| Metric | Value |
| --- | --- |
| Active validators | 689 |
| Delinquent validators | 7 (1.01%) |
| Stake held by delinquents | 5,555 SOL (0.001%) |
| Total active stake | 435,235,713 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Zero-commission validators | 256 |

_The Nakamoto coefficient is the number of validators that would need to collude to control 33% of stake and halt consensus. Higher is more decentralised._

### Top validators by stake

| # | Vote account | Stake (SOL) | Share | Commission |
| --- | --- | --- | --- | --- |
| 1 | `CcaHc2L43ZWjwCHART3oZoJvHLAe9hzT2DJNUpBzoTN1` | 17,101,527 | 3.929% | 7% |
| 2 | `he1iusunGwqrNtafDtLdhsUQDFvo13z9sUa36PauBtk` | 16,011,570 | 3.679% | 0% |
| 3 | `CatzoSMUkTRidT5DwBxAC2pEtnwMBTpkCepHkFgZDiqb` | 12,410,378 | 2.851% | 5% |
| 4 | `3N7s9zXMZ4QqvHQR15t5GNHyqc89KduzMP7423eWiD5g` | 12,198,972 | 2.803% | 0% |
| 5 | `26pV97Ce83ZQ6Kz9XT4td8tdoUFPTng8Fb8gPyc53dJx` | 9,188,631 | 2.111% | 7% |
| 6 | `51JBzSTU5rAM8gLAVQKgp4WoZerQcSqWC7BitBzgUNAm` | 8,991,290 | 2.066% | 10% |
| 7 | `8GbwASqdpw4dVcwbWUxbHXMrjyQx2aKkoBR5H1GJF8iD` | 8,308,413 | 1.909% | 0% |
| 8 | `9QU2QSxhb24FUX3Tu2FpczXjpK3VYrvRudywSZaM29mF` | 7,991,430 | 1.836% | 7% |
| 9 | `CvSb7wdQAFpHuSpTYTJnX5SYH4hCfQ9VuGnqrKaKwycB` | 7,344,654 | 1.688% | 5% |
| 10 | `DumiCKHVqoCQKD8roLApzR5Fit8qGV5fVQsJV9sTZk4a` | 6,546,146 | 1.504% | 0% |

## Economics

| Metric | Value |
| --- | --- |
| SOL price | $86.96 (up 7.52%) |
| Market cap | $50.69B |
| DeFi TVL | $5.29B |
| TVL rank across chains | 3 |
| DEX volume (24h) | $3.01B (up 63.74%) |
| Stablecoin supply | $15.64B |

### Real Economic Value (REV)

| Component | 24h |
| --- | --- |
| **REV (total)** | **$1.15M** |
| Network fees | $925.81K |
| MEV tips (out-of-protocol) | $228.72K (19.81% of REV) |
| Annualised REV run-rate | $421.40M |

_REV is what the **network** captures. It is a different and much smaller figure than fees earned by applications built on Solana, which follow separately -- conflating the two overstates REV by more than 10x._

| MEV source | Tips (24h) |
| --- | --- |
| Jito MEV Tips | $194.00K |
| Harmonic | $21.77K |
| bloXroute | $12.92K |
| Pyth Express Relay | $25 |

### Application fees (distinct from REV)

Fees earned by the 295 applications built on Solana -- DEXes, launchpads, wallets and bots. Economically interesting, but not network revenue.

| Window | Application fees |
| --- | --- |
| 24 hours | $13.68M (up 55.88%) |
| 7 days | $66.89M |
| 30 days | $256.96M |

| Top fee-earning app | Fees (24h) |
| --- | --- |
| PumpSwap | $2.85M |
| pump.fun | $1.99M |
| Axiom | $1.81M |
| Jupiter Perpetual Exchange | $1.02M |
| Solana | $925.81K |

## Tokenized assets

| Metric | Value |
| --- | --- |
| Total tokenized RWA | $1.90B |
| Tokenized equities | $430.15M (22.64% of RWA) |
| RWA protocols on Solana | 25 |

### Tokenized equity issuers

| Protocol | Value | 24h |
| --- | --- | --- |
| xStocks | $404.48M | 5.683% |
| Ondo Global Markets | $25.66M | 2.9% |

### Largest tokenized-asset protocols

| Protocol | Value | Category |
| --- | --- | --- |
| BlackRock BUIDL | $740.49M | RWA |
| xStocks | $404.48M | RWA |
| OnRe | $272.25M | RWA |
| Ondo Yield Assets | $179.22M | RWA |
| Hastra | $170.97M | RWA |
| Theo Network thBill | $26.38M | RWA |
| Ondo Global Markets | $25.66M | RWA |
| Nest Credit | $22.46M | RWA |
| Apollo Diversified Credit Securitize Fund | $18.35M | RWA |
| VanEck Treasury Fund | $13.93M | RWA |

## Address activity

| Metric | Value |
| --- | --- |
| Unique fee payers (sampled) | 1,785 |
| Blocks sampled | 3 |
| Transactions in sample | 6,079 |
| Non-vote share of sample | 66.79% |
| Signers per block | 595.0 |

_Unique fee payers across sampled blocks -- an activity indicator, not a 24h unique-address count._

### Top DEXes by 24h volume

| DEX | Volume (24h) |
| --- | --- |
| PumpSwap | $753.62M |
| BisonFi | $440.28M |
| Orca DEX | $335.42M |
| HumidiFi | $331.84M |
| Manifest Trade | $200.02M |

## Supply

Circulating 583,005,961 SOL of 632,513,505 total (92.17%).

## Ecosystem growth (solana.com/data)

| Metric | Value | As of | Provider |
| --- | --- | --- | --- |
| Active Addresses | 617,475 | 2026-08-19 | Dune |
| Fee Payers | 2,675,872 | 2026-08-19 | Dune |
| Transaction Count (Total) | 357,868,974 | 2026-08-19 | Dune |
| Non Vote Transaction Count (Success) | 112,664,546 | 2026-08-19 | Dune |
| Non Vote Transaction Count (Failed) | 103,976,655 | 2026-08-19 | Dune |
| DEX Volume | $869.63M | 2026-08-19 | Dune |
| DEX Traders | 471,166 | 2026-08-19 | Dune |
| Transfer Volume | $12.02B | 2026-08-18 | Dune |
| Total Stake | 435,024,271 | 2026-08-20 | Stakewiz |
| Validator Count | 686 | 2026-08-20 | Stakewiz |
| Top 3 ASN Share | 46.13 | 2026-08-20 | Stakewiz |

_Daily active addresses are deduplicated across the full day by the provider — distinct from the live block sample below, which measures current activity._

### Where providers disagree

The same metric is published by multiple providers with different methodologies. Divergences above threshold on the same day:

| Metric | Date | Spread | Provider readings |
| --- | --- | --- | --- |
| Active Addresses | 2026-08-19 | 31.5% | Allium: 811,969, Dune: 617,475 |

## Announcements from key accounts

- **@solana** — https://t.co/GS74mG15b1 [(link)](https://x.com/solana/status/2090283987017269679)
- **@solana** — Solana sustained 5-6k real transactions per second today and is still processing about 4k This is 3x more than NASDAQ on an average day The future is now [(link)](https://x.com/solana/status/2090227975576756285)
- **@solanalabs** — Your stablecoins were never meant to sit still. Now you can earn yield on your USDC on the go. Introducing the USDC Earn Vault powered by @Kamino, now live on Seeker in Seed Vault Wallet 🧵 https://t.co/HpF12YO1ak [(link)](https://x.com/solanalabs/status/2090185322986668285)
- **@solana** — BREAKING: $MRNA from Moderna is live on Solana via @sunrise, issued by @Backpack Securities Moderna announced the first ever positive Phase 3 results for a personalized cancer vaccine https://t.co/vkyVEQeuYp [(link)](https://x.com/solana/status/2090177416375259541)
- **@solana** — Sunrise has listed $MRNA on @Solana. Today, Moderna and Merck reported the first positive Phase 3 results for an mRNA cancer therapy. Issued by @Backpack Securities, a tokenized Moderna share now trades on Solana, 24/7. https://t.co/uqGE6y… [(link)](https://x.com/solana/status/2090176270885925087)
- **@solanalabs** — Shipped Live episode 3 is coming 🔜 Tomorrow August 11 at 11am EST The latest on the Solana Mobile ecosystem, featuring: - @beeman_nl - @web4O - @inno_sol Sign up now 👇 https://t.co/dVQgaOulNi [(link)](https://x.com/solanalabs/status/2086893782742757446)
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
  Solana is introducing a new transaction format (v1) alongside an increase of the maximum transaction size from 1232 bytes to 4096 bytes. The v1 format aims to unlock new possibilities on-chain. This is done trading-off …
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
