# PROJECT CORETEX BTC BRAIN — MODULE 48: STABLECOIN SUPPLY RATIO (SSR), USDT.D & NET MINT/BURN VELOCITY
**Waterfall Tier:** Pillar 1 (Macro Liquidity & Crypto-Native Dry Powder) & Pillar 5 (Settlement-Rail Flows & Exchange Buying Power) — operates directly alongside `MOD 05` (Spot vs. Perp CVD), `MOD 07` (Domestic USD Gateways vs. Offshore), `MOD 16` (Macro Liquidity & Stablecoin Dry Powder), `MOD 22` (Net Fed Liquidity), and `MOD 39` (Exchange Supply & Stablecoin Inflows).
**Empirical Benchmark Anchor:**
1. **November 2026 Redemption Drain Benchmark:** Following a May 2026 peak (`~$312.85B–$322.4B`), total USD-pegged stablecoin supply contracted by **`-$14.2B` to `-$14.9B`** over the 30 days through November 9–12, 2026 (down to `~$289.37B`, the fastest 30-day contraction since June 2022). **`USDT` (`-$8.31B` to `$175.64B`)** and **`USDC` (`-$3.20B` to `$69.66B`)** accounted for `77%` of the outflow while maintaining `$1.00` parity (`USDT ~$0.9992`), confirming an active capital redemption drain rather than a solvency de-peg.
2. **SSR Denominator Distortion & Non-Trading Rails (2026 Regime):** During the November 2026 drawdown, stablecoin supply fell `-4.6%` while BTC fell `> -20%`, pushing stablecoins to `~19.5%` of BTC market cap and compressing the **Stablecoin Supply Ratio (`SSR = BTC_Market_Cap / Stablecoin_Market_Cap`)** toward its `-2σ` lower Bollinger band. Simultaneously, post-GENIUS Act / MiCA corporate payment rails (`Stripe`, `PayPal`, `Visa`) and yield-bearing tokens (`sUSDS`, `USDe`) absorb significant non-trading supply, requiring exchange-level inflow confirmation before treating low `SSR` as active spot buying power.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / GitHub Index)

```yaml
module_id: "MOD_48"
entry_type: "CRYPTO_NATIVE_LIQUIDITY_VELOCITY_ENGINE"
waterfall_pillar: "PILLAR_1_AND_5_STABLECOIN_DRY_POWDER"
title: "Stablecoin Supply Ratio (SSR), USDT.D & Net Mint/Burn Velocity"

# STABLECOIN MINT/BURN & DRY POWDER THRESHOLDS
velocity_parameters:
  core_trading_basket: ["USDT", "USDC"] # ~82% of total supply; primary spot/perp collateral rails
  mint_expansion_7d_usd: 1000000000 # >= +$1.0B 7D net USDT+USDC supply growth (fresh dry powder entering)
  mint_expansion_30d_usd: 4000000000 # >= +$4.0B 30D net USDT+USDC supply growth (bullish liquidity wave)
  redemption_drain_7d_usd: -1500000000 # <= -$1.5B 7D net USDT+USDC contraction (capital leaving crypto rails)
  redemption_drain_30d_usd: -5000000000 # <= -$5.0B 30D net contraction (severe liquidity drain; Nov 2026 was -$11.5B)
  ssr_zscore_bands:
    oversold_dry_powder_z: -1.75 # SSR near -2 sigma lower band (high relative buying power IF outflows halt)
    overheated_thin_cash_z: 2.00 # SSR near +2 sigma upper band (BTC stretched relative to sidelined stablecoins)
  depeg_circuit_breaker_usd: 0.992 # Any top-2 stablecoin <= $0.992 for > 2H triggers MOD 16 M7 / MOD 28 BS-02

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_NO_LOW_SSR_BLIND_BUYING: "NEVER buy BTC solely because SSR hits a -2 sigma low during a price crash; SSR falls mechanically when BTC market cap drops faster than stablecoin redemptions (Nov 2026). Require 7D USDT+USDC supply to flatten (>= $0) first."
  CB_02_PAYMENT_RAIL_NOISE_FILTER: "Do NOT treat total stablecoin market cap growth as bullish trading fuel unless spot exchange stablecoin reserves rise alongside Domestic USD Spot CVD (MOD 05) and US Spot ETF flows (MOD 07)."
  CB_03_DOMESTIC_VS_OFFSHORE_SPLIT: "If USDT grows offshore while USDC shrinks and Coinbase Premium is negative, cap Pillar 1 at GATE_AMBER (0.375% risk) per MOD 16 M4."
  CB_04_DEPEG_FLIGHT_REJECTION: "If USDT or USDC trades <= $0.992 for > 2 hours, HALT ALL ENTRIES immediately—never mistake stablecoin panic flight into BTC for organic spot accumulation."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  active_drain_max_risk_pct: 0.00 # Enforce 100% Cash Lock during severe 7D/30D stablecoin contraction
  mint_reclaim_max_risk_pct: 0.75 # Full 0.75% spot risk unlocked when 7D mints flip positive + 4H VAH reclaims
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Stablecoin-Liquidity Invariants)

* **Circuit Breaker 1 — The Denominator Fallacy (`CB-01`):** `SSR` (`BTC Market Cap / Stablecoin Market Cap`) drops automatically whenever Bitcoin sells off `-20%+`, even while billions in `USDT` and `USDC` are being redeemed out of crypto (as seen in November 2026). Never buy a `-2σ` `SSR` reading until **7-day `USDT + USDC` net supply stops shrinking (`>= $0`)**.
* **Circuit Breaker 2 — Non-Trading Payment & Yield Noise (`CB-02`):** Corporate B2B settlement (`Stripe`/`Visa`), AI-agent micropayments, and yield-bearing wrappers (`sUSDS`, `USDe`) inflate total stablecoin supply without adding exchange order-book bids. Track **`USDT + USDC` 7D/30D net change** plus **exchange stablecoin netflows** (`MOD 39 M7`), validated by `Domestic USD Spot CVD` (`MOD 05`).
* **Circuit Breaker 3 — Domestic `USDC` vs. Offshore `USDT` Quality Gate (`CB-03`):** Institutional US spot accumulation flows through `USD` and `USDC` rails (`Coinbase`/`CME`/`ETFs`), whereas `USDT` dominates offshore leverage. When `USDC` contracts while `USDT` expands offshore, cap tactical risk at **`0.375%` (`GATE_AMBER`)**.
* **Circuit Breaker 4 — De-Peg Contagion Lock (`CB-04`):** Any sustained deviation of `USDT` or `USDC` below **`$0.992`** (`> 2 hours`) triggers an immediate **`100% Cash Lock`** (`MOD 16 M7` / `MOD 28 BS-02`).

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-48A: Active Stablecoin Redemption Drain (`7D <= -$1.5B` or `30D <= -$5.0B`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Combined `USDT + USDC` 7-day net supply change is `<= -$1.5B` OR 30-day net change is `<= -$5.0B` (e.g., November 2026 `-$11.51B` combined contraction), while `USDT` and `USDC` maintain `~$1.00` peg (`> $0.995`).
  2. `USDT Dominance (USDT.D)` trends above its `20D/50D` structural resistance while `BTC` trades below `4H VAH`.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Crypto-native dry powder is actively leaving exchanges back into TradFi T-bills, mega-IPOs (`MOD 44`), or fiat bank accounts—removing marginal spot bid depth.
  * **Probable Trajectory:** Weak relief bounces that stall below `4H VAH` / `STH Realized Price` until redemptions exhaust.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE `100% CASH LOCK` (`0.00%` tactical risk)** alongside `MOD 16` / `MOD 44` until the 7-day `USDT + USDC` burn streak flattens (`>= $0`).

### CSU-48B: Redemption Exhaustion & Low-`SSR` Inflection (`SSR <= -1.75 Z` + Burn Halt)
* **Trigger Condition A (The Telemetry Scan):**
  1. `SSR` sits in the oversold dry-powder band (`Z <= -1.75` / `-2σ` lower band) following a multi-week drawdown.
  2. **Flow Turn:** Rolling 7-day `USDT + USDC` supply change flattens from deep negative to **`>= $0`** (or `+0.25%`), `USDT.D` prints a bearish divergence / lower high at resistance, and **spot exchange stablecoin balances turn positive** (`MOD 39 M7`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Capital flight has stopped; the remaining stablecoin pool holds outsized purchasing power relative to discounted BTC market cap.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **UPGRADE DRY-POWDER GATE TO `AMBER/GREEN`:** Authorize `0.375%–0.75%` spot long entry upon confirmed `1H/4H VAH` reclaim + positive `Domestic USD Spot CVD` (`MOD 37 Net R >= 3.0`).

### CSU-48C: Synchronized `USDT + USDC` Mint Expansion (`7D >= +$1.0B` & `30D >= +$4.0B`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Combined `USDT + USDC` supply expands by **`>= +$1.0B` over 7 days** and **`>= +$4.0B` over 30 days**, with **both** `USDT` and `USDC` growing (`USDC` 30D growth `> 0%`).
  2. `Coinbase USD Spot CVD` is positive (`MOD 05A`) and `BTC` holds above `4H/1D POC`.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Fresh fiat capital is minting into both domestic (`USDC`) and global (`USDT`) settlement rails simultaneously, fueling sustained spot-led markup.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **CONFIRM `GATE_GREEN` (`0.75%` max equity risk)** for `MOD 30` pullback/breakout entries; prioritize Stage 2 trailing runners (`MOD 18`).

### CSU-48D: High-`SSR` Thin Dry-Powder Exhaustion (`SSR >= +2.00 Z` + Stalled Mints)
* **Trigger Condition A (The Telemetry Scan):**
  1. `SSR` surges above **`+2.00 Z` (`+2σ` upper band)** after a vertical BTC rally while 14-day `USDT + USDC` mint velocity flattens (`<= 0%`) and `USDT.D` hits multi-month support.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Sidelined stablecoin liquidity has been largely deployed into BTC; marginal spot buying power is thin and vulnerable to a leverage-driven pullback (`MOD 02` / `MOD 13C`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **TIGHTEN TRAILING STOPS & EXECUTE STAGE 1 (`50%`) PROFIT HARVEST (`MOD 18`);** ban late FOMO breakout chasing until `SSR` cools back toward median.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Post-Drain First `$1B+` Mint Reversal** | `CSU-48A` (Drain) | After a `-$10B+` 30D contraction, `USDT + USDC` prints its first **`>= +$1.0B` 7-day net mint** alongside positive US Spot ETF flows (`MOD 07`). | Institutional/global capital rotation has officially flipped from redemption back to deployment. | **Lift `MOD 48` Cash Lock Immediately;** authorize `0.75%` spot entry on `4H VAH` reclaim. |
| **M2: `USDT.D` Rejection + `BTC` Higher Low** | `CSU-48B` (Inflection) | `USDT.D` sweeps above range highs, fails back below its `4H` breakdown level, while `BTC` prints a `MOD 42B` Wyckoff Spring on positive `USD Spot CVD`. | Sidelined stablecoin holders rotated back into spot BTC at the liquidity sweep low. | **Authorize `0.75%` Spot Long (`MOD 30 CONFIG_J`)** with stop beneath the spring wick low. |
| **M3: Offshore `USDT` Mint + Negative `USDC` Split** | `CSU-48B` / `48C` | `USDT` mints `+$1.5B` in 7 days, **but** `USDC` shrinks `-$800M`, `Coinbase Premium` is negative, and `Perp OI` spikes (`MOD 07 M6`). | Offshore derivatives leverage reload without US institutional spot backing. | **Cap Risk at `0.375%` (`GATE_AMBER`) or Hold Cash** until `Coinbase USD Spot CVD` confirms. |
| **M4: Yield-Stablecoin (`sUSDS`/`USDe`) Rotation Drain** | Neutral / Chop | On-chain DeFi/Treasury yields rise, pulling `$2B+` out of spot exchange `USDT/USDC` into locked yield wrappers (`sUSDS`, T-bill tokens) while `BTC` stalls below `200D MA`. | Capital is parking for passive yield rather than bidding spot BTC order books. | **Treat as Neutral/Bearish Liquidity Drag;** require `4H VAH` breakout before deploying risk. |
| **M5: Stablecoin Inflow + Whale BTC Inflow Clash** | `REGIME_2 / 5` | `> $500M` `USDC/USDT` enters exchanges simultaneously with `> 3,000 BTC` whale deposits (`MOD 39 M7`). | Incoming dry powder matches incoming supply—order book equilibrium battle. | **Wait for `1H/4H` Volume Profile Resolution (`VAH` vs `VAL`)** before committing capital. |
| **M6: `USDT` / `USDC` Peg Stress (`<= $0.992`)** | Any Active State | Either `USDT` or `USDC` trades at or below **`$0.992`** for `> 2 hours` on major USD pairs, causing `BTC/USDT` to spike artificially above `BTC/USD`. | Settlement-rail solvency scare creating synthetic `BTC/USDT` premium distortion (`MOD 16 M7`). | **Immediate `100% CASH LOCK` & Venue Audit (`MOD 32`);** ban buying `BTC/USDT` de-peg spikes. |
| **M7: `SSR` Compression Without Exchange Inflows** | `CSU-48B` Watch | `SSR` hits `-2.0 Z`, **but** 7-day `USDT + USDC` supply is still falling (`-$2B/wk`) and exchange stablecoin reserves are shrinking (`CB-01`). | Pure denominator effect from falling BTC price—no real dry powder is stepping in yet. | **Maintain `100% CASH LOCK`;** reject premature bottom-fishing (`MOD 45 CB-02`). |
| **M8: Stablecoin API / DefiLlama Feed Lag (`MOD 36`)** | Routine Scan | Primary stablecoin supply or `SSR` endpoint lags `> 24H` during high volatility. | Stale denominator/numerator data (`UNKNOWN` state). | Tag `MOD_48_STATE = UNKNOWN` (`MOD 36`); rely on live `MOD 05` USD Spot CVD + `MOD 07` ETF flows. |
