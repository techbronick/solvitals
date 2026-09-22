# Solana Ecosystem Report

Generated 2026-09-22 21:43:06 UTC by SolVitals.

## Alerts

- [CRITICAL] **price_usd** — price_usd is 3.2 sigma above its 287-point mean
- [CRITICAL] **tvl_usd** — tvl_usd is 3.3 sigma above its 288-point mean
- [WARNING] **rev_24h_usd** — rev_24h_usd is 2.2 sigma above its 287-point mean
- [WARNING] **rwa_total_usd** — rwa_total_usd is 2.3 sigma below its 288-point mean

## Network Performance

| Metric | Value |
| --- | --- |
| Non-vote TPS | 2,069.65 |
| Total TPS (incl. votes) | 4,576.71 |
| Vote share of transactions | 54.78% |
| Average slot time | 0.2683 s |
| Current slot | 449,503,104 |
| Block height | 427,543,427 |

_Non-vote TPS is the figure that reflects user activity; consensus votes are transactions on Solana and inflate the raw count._

## Epoch

Epoch **1040** — 51.64% complete (`##########..........`), ~15.5 hours remaining.

Slot 223,106 of 432,000. Lifetime transaction count: 551,474,292,458.

## Transaction costs and slot timing

| Metric | Value |
| --- | --- |
| Median priority fee | 0 micro-lamports/CU |
| 75th percentile | 0 |
| 95th percentile | 0 |
| Slots needing no priority fee | 100.0% |
| Median total fee (200k CU, 1 sig) | 5e-06 SOL |
| Measured slot time (`getBlockTime`) | 0.2676 s |
| Deviation from 0.4s target | -33.1% |

_Priority fees are per compute unit in micro-lamports. Median total assumes a 200k CU transaction with one signature._

### Watched account

`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` (SPL Token program) — balance 0.2007 SOL, 10 recent signatures, 3 with errors.

## Validators

| Metric | Value |
| --- | --- |
| Active validators | 677 |
| Delinquent validators | 12 (1.74%) |
| Stake held by delinquents | 199,751 SOL (0.045%) |
| Total active stake | 439,661,998 SOL |
| Nakamoto coefficient | 18 |
| Median commission | 5% |
| Zero-commission validators | 236 |

_The Nakamoto coefficient is the number of validators that would need to collude to control 33% of stake and halt consensus. Higher is more decentralised._

### Top validators by stake

| # | Vote account | Stake (SOL) | Share | Commission |
| --- | --- | --- | --- | --- |
| 1 | `CcaHc2L43ZWjwCHART3oZoJvHLAe9hzT2DJNUpBzoTN1` | 17,826,722 | 4.055% | 7% |
| 2 | `he1iusunGwqrNtafDtLdhsUQDFvo13z9sUa36PauBtk` | 15,840,698 | 3.603% | 0% |
| 3 | `3N7s9zXMZ4QqvHQR15t5GNHyqc89KduzMP7423eWiD5g` | 12,354,353 | 2.81% | 0% |
| 4 | `CatzoSMUkTRidT5DwBxAC2pEtnwMBTpkCepHkFgZDiqb` | 11,265,429 | 2.562% | 5% |
| 5 | `8GbwASqdpw4dVcwbWUxbHXMrjyQx2aKkoBR5H1GJF8iD` | 10,210,832 | 2.322% | 0% |
| 6 | `26pV97Ce83ZQ6Kz9XT4td8tdoUFPTng8Fb8gPyc53dJx` | 9,211,356 | 2.095% | 7% |
| 7 | `51JBzSTU5rAM8gLAVQKgp4WoZerQcSqWC7BitBzgUNAm` | 9,144,102 | 2.08% | 10% |
| 8 | `9QU2QSxhb24FUX3Tu2FpczXjpK3VYrvRudywSZaM29mF` | 7,458,789 | 1.696% | 7% |
| 9 | `CvSb7wdQAFpHuSpTYTJnX5SYH4hCfQ9VuGnqrKaKwycB` | 7,089,342 | 1.612% | 5% |
| 10 | `DumiCKHVqoCQKD8roLApzR5Fit8qGV5fVQsJV9sTZk4a` | 6,555,722 | 1.491% | 0% |

## Economics

| Metric | Value |
| --- | --- |
| SOL price | $118.06 (down 1.30%) |
| Market cap | $69.36B |
| DeFi TVL | $6.50B |
| TVL rank across chains | 2 |
| DEX volume (24h) | $3.43B (up 22.67%) |
| Stablecoin supply | $16.02B |

### Real Economic Value (REV)

| Component | 24h |
| --- | --- |
| **REV (total)** | **$1.39M** |
| Network fees | $1.10M |
| MEV tips (out-of-protocol) | $296.45K (21.29% of REV) |
| Annualised REV run-rate | $508.21M |

_REV is what the **network** captures. It is a different and much smaller figure than fees earned by applications built on Solana, which follow separately -- conflating the two overstates REV by more than 10x._

| MEV source | Tips (24h) |
| --- | --- |
| Jito MEV Tips | $254.49K |
| Harmonic | $29.35K |
| bloXroute | $12.61K |

### Application fees (distinct from REV)

Fees earned by the 316 applications built on Solana -- DEXes, launchpads, wallets and bots. Economically interesting, but not network revenue.

| Window | Application fees |
| --- | --- |
| 24 hours | $18.64M (up 26.21%) |
| 7 days | $110.89M |
| 30 days | $428.70M |

| Top fee-earning app | Fees (24h) |
| --- | --- |
| PumpSwap | $3.36M |
| Axiom | $2.30M |
| StonkFun | $1.81M |
| pump.fun | $1.73M |
| Raydium AMM | $1.69M |

## Tokenized assets

| Metric | Value |
| --- | --- |
| Total tokenized RWA | $536.76M |
| Tokenized equities | $296.07K (0.06% of RWA) |
| RWA protocols on Solana | 15 |

### Tokenized equity issuers

| Protocol | Value | 24h |
| --- | --- | --- |
| Remora Markets | $296.07K | None% |

### Largest tokenized-asset protocols

| Protocol | Value | Category |
| --- | --- | --- |
| OnRe | $302.65M | RWA |
| Huma Finance V2 | $188.67M | RWA |
| Plume Vaults | $28.21M | RWA |
| Invesco USTB | $3.91M | RWA |
| Mansory | $3.01M | RWA |
| VNX | $2.72M | RWA |
| Oro Finance | $2.50M | RWA |
| International Stable Currency | $2.43M | RWA |
| Byzanlink RWA Markets | $890.52K | RWA |
| KAIO | $774.58K | RWA |

### Top DEXes by 24h volume

| DEX | Volume (24h) |
| --- | --- |
| Raydium AMM | $493.51M |
| BisonFi | $446.78M |
| Orca DEX | $398.84M |
| PumpSwap | $390.12M |
| Meteora DLMM | $259.61M |

## Supply

Circulating 587,507,367 SOL of 634,530,995 total (92.59%).

## Ecosystem growth (solana.com/data)

| Metric | Value | As of | Provider |
| --- | --- | --- | --- |
| Active Addresses | 862,448 | 2026-09-21 | Dune |
| Fee Payers | 3,114,991 | 2026-09-21 | Dune |
| Transaction Count (Total) | 394,479,904 | 2026-09-21 | Dune |
| Non Vote Transaction Count (Success) | 116,561,506 | 2026-09-21 | Dune |
| Non Vote Transaction Count (Failed) | 60,140,287 | 2026-09-21 | Dune |
| DEX Volume | $3.25B | 2026-09-21 | Dune |
| DEX Traders | 943,864 | 2026-09-21 | Dune |
| Transfer Volume | $27.82B | 2026-09-21 | Dune |
| Total Stake | 440,061,849 | 2026-09-21 | Solscan |
| Validator Count | 675 | 2026-09-22 | Stakewiz |
| Top 3 ASN Share | 46.10 | 2026-09-22 | Stakewiz |

_Daily active addresses are deduplicated across the full day by the provider — distinct from the live block sample below, which measures current activity._

### Where providers disagree

The same metric is published by multiple providers with different methodologies. Divergences above threshold on the same day:

| Metric | Date | Spread | Provider readings |
| --- | --- | --- | --- |
| Active Addresses | 2026-09-21 | 81.0% | Allium: 871,580, Artemis: 780,606, Blockworks: 492,923, Dune: 862,448, Goldsky: 863,383, RWA: 892,240 |
| Fee Payers | 2026-09-21 | 78.0% | Allium: 3,115,033, Artemis: 5,545,309, Blockworks: 3,128,115, Dune: 3,114,991, Token Terminal: 3,119,854 |

## Announcements from key accounts

- **@solana** — Great technology doesn't get built in isolation. It needs talent, ideas and capital, and something that connects all three. Solana Accelerate China brings them together. Shanghai, Hangzhou, Shenzhen and Beijing, October 16 to 22. https://t… [(link)](https://x.com/solana/status/2102309864085328162)
- **@solana** — Sign up for your city: 16 Oct: Shanghai https://t.co/bQ01yLiZEi 18 Oct: Hangzhou https://t.co/P4jQddS5Mo 20 Oct: Shenzhen https://t.co/4Hhg8xnp0i 22 Oct: Beijing https://t.co/XFPsTaI8Bp [(link)](https://x.com/solana/status/2102309866396373416)
- **@solana** — got a super cool idea you’ve been sitting on? join sid in bangalore (or online) and learn how to make it exist with AI [powered by @SuperteamIN] https://t.co/DE786gbtsM [(link)](https://x.com/solana/status/2102297296562221369)
- **@solana** — JUST IN: Solana handles 76% of all @x402 transactions. 23.2M in four weeks. The next-largest network did 3.39M. https://t.co/OJv35U4kXF [(link)](https://x.com/solana/status/2102285997304148088)
- **@solanalabs** — Seeker Season brings the heat with One Arena @Rosentica ⚔️ Rip packs, collect real graded cards, and put your lineup to the test. Seekers get exclusive perks, and the Seeker Cup Tournament starts today with a $50,000 prize pool. Available … [(link)](https://x.com/solanalabs/status/2099530088614130111)
- **@solanalabs** — Clock In 📱 The Solana Mobile Hackathon by RadiantsDAO is live. - 4 weeks - $135k in prizes - A SKR integration track This is your shot to get distribution and build the next viral mobile crypto app. Submissions due on October 8. Register n… [(link)](https://x.com/solanalabs/status/2097387853990748448)
- **@solanalabs** — Welcome and a big congrats to the incredible teams in Cohort 5 🥳 Follow @incubator for updates on their progress and to stay in the loop on all things Solana Incubator. [(link)](https://x.com/solanalabs/status/2094856511587860600)
- **@solanalabs** — Introducing Cohort 5 of the Solana Incubator. Our most competitive pool yet — founders building across AI, robotics, and trading on @solana. Day one of working with these teams: 🟣@clawpumptech 🟣@crowdbrainai 🟣@Lavaragexyz 🟣@morfimarkets 🟣@… [(link)](https://x.com/solanalabs/status/2094842504025694668)

_Announcements only; replies and retweets filtered. The endpoint rate-limits intermittently, so a failed account degrades this section alone and the cached copy is reused._

## Upcoming upgrades and protocol changes

| Metric | Value |
| --- | --- |
| Improvement proposals tracked | 131 |
| With an assigned feature gate | 34 |
| Gates live on mainnet | 22 |
| Gates awaiting mainnet | 12 |

### Proposals by status

| Status | Count |
| --- | --- |
| Review | 54 |
| Activated | 25 |
| Implemented | 14 |
| Idea | 14 |
| Accepted | 9 |
| Draft | 7 |
| Withdrawn | 5 |
| Living | 2 |
| Stagnant | 1 |

**Cluster versions:** mainnet `4.3.0-rc.0` · testnet `4.3.0-rc.1` · devnet `4.3.0-rc.0`

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
| SIMD-0599 | `remove_inactive_stakes` | not created | not created | not created |

## Ecosystem and community news

- **[Solana Changelog: September 18, 2026](https://solana.com/news/solana-changelog-september-18-2026)**
  Transaction V1 reaches mainnet as Solana targets 250ms slots, lower rent, and program deployments with four times lower fees.
- **[How AI Is Reshaping Crypto Security, with Michael Coates](https://solana.com/news/bits-to-bricks-crypto-security-michael-coates)**
  A ~$116 million Coldcard exploit shows why crypto security must eliminate single points of failure and automate defenses for AI-speed threats.
- **[Project Harmonia Brings Institutional Tokenized Funds to Solana](https://solana.com/news/project-harmonia-brings-institutional-tokenized-funds-to-solana)**
  Project Harmonia connects Allfunds, with about €1.9 trillion under administration, to tokenized funds on Solana; submissions close October 24, 2026.
- **[Solana: Building, Proving and Earning Trust in Public](https://solana.com/news/solana-building-trust-in-public)**
  Solana has maintained 100% uptime since February 2024, including when a routing failure took nearly 29% of network stake offline.
- **[Solana Changelog: September 10, 2026](https://solana.com/news/solana-changelog-september-10-2026)**
  V1 transaction activation is delayed to Epoch 1035, alongside new Agave, Firedancer, Web3.js, Solana Kit, and program releases.
- **[Solana Changelog: September 3, 2026](https://solana.com/news/solana-changelog-september-3-2026)**
  Firedancer adopts three RPC calls and advances ARM support, while three mainnet feature gates and new Agave, Web3.js, and Solana Kit versions land.
- **[Report: Stablecoins Are Reshaping Remittances](https://solana.com/news/report-stablecoins-are-reshaping-remittances)**
  New report on stablecoin remittances covering four implementation paths for money transfer operators, corridor overviews, and case studies.
- **[How BitRobot Crowdsources Real-World Data for Embodied AI, with Jonathan Victor](https://solana.com/news/bits-to-bricks-bitrobot-jonathan-victor)**
  BitRobot open-sourced 2,000 hours of robot navigation data and uses Solana to track and reward embodied AI data contributors.

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
