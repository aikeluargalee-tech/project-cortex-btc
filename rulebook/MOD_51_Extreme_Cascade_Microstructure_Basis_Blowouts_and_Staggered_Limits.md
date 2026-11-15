# PROJECT CORETEX BTC BRAIN — MODULE 51: EXTREME CASCADE MICROSTRUCTURE, BASIS BLOWOUTS & STAGGERED LIMIT EXECUTION
**Waterfall Tier:** Pillar 3 (Derivatives & Basis Stress) & Pillar 4 (Post-Cascade Execution & Slippage Control) — operates directly alongside `MOD 01` (Negative Basis), `MOD 03` (Deleveraging Flushes & OI Resets), `MOD 06` (Passive Absorption), `MOD 34` (AEGIS-3 Impulse Defense), `MOD 35` (Liquidation Heatmap Pull Score), and `MOD 37` (Executable L2 Liquidity & `Net R >= 3.0`).
**Empirical Benchmark Anchor:**
1. **November 13–15, 2026 Liquidation Cascade Benchmark:** On November 13, 2026, CoinGlass recorded **`~$1.47B`** in 24-hour crypto liquidations (followed by another **`$819.6M`** wave with `92%` long liquidations and a `-9.10%` 24H Open Interest drop as BTC swept into the `$59,500–$62,600` liquidation cluster, hitting `$62,199` on Nov 15).
2. **Cascade Microstructure Dynamics:** During `$750M+` liquidation cascades, forced market-sell orders sweep through thin L2 bids, driving annualized perpetual basis sharply negative (`-8%` to `-20%+`), widening bid-ask spreads `3x–8x`, and creating multi-leg "aftershock" wicks before spot-led absorption stabilizes price.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / GitHub Index)

```yaml
module_id: "MOD_51"
entry_type: "CASCADE_EXECUTION_AND_BASIS_ENGINE"
waterfall_pillar: "PILLAR_3_AND_4_CASCADE_EXECUTION"
title: "Extreme Cascade Microstructure, Basis Blowouts & Staggered Limit Execution"

# CASCADE SEVERITY & BASIS THRESHOLDS
cascade_parameters:
  major_liquidation_24h_usd: 750000000 # >= $750M 24H total liquidations (longs >= 80%)
  extreme_cascade_24h_usd: 1250000000 # >= $1.25B 24H liquidations (e.g., Nov 13, 2026 $1.47B flush)
  oi_flush_threshold_pct: -8.0 # 24H Open Interest drop <= -8.0% (Nov 15 benchmark: -9.10%)
  perp_basis_discount_annualized_pct: -10.0 # Annualized perp-spot basis <= -10.0% (extreme backwardation)
  post_cascade_cooldown_hours: 4 # Mandatory 4-hour cooling window after peak 1H liquidation print
  staggered_limit_tranches: 3 # Split authorized post-cascade spot entry into 3 passive limit rungs (40% / 35% / 25%)

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_NO_FIRST_WICK_MARKET_BUYING: "NEVER place market buy orders during an active 1H liquidation spike or within the first 4 hours after peak liquidation velocity; cascades routinely print a second lower liquidity sweep."
  CB_02_CALENDAR_AND_ETF_OVERRIDE: "Even after a $1B+ OI flush and negative basis blowout, if MOD 44 Mega-IPO/Index drain is active OR US Spot ETFs are still bleeding > -$150M/day, maintain 100% Cash Lock (0.00% risk)."
  CB_03_STAGGERED_PASSIVE_LADDER_ONLY: "When L2 depth is recovering post-cascade, execute entries strictly via a 3-rung passive limit ladder anchored to MOD 11 VAL/POC and MOD 43 Fib levels—never a single market fill."
  CB_04_HARD_CAP_0_75_PCT_TOTAL_RISK: "Total combined risk across all 3 staggered limit rungs MUST NOT exceed 0.75% (or 0.375% under GATE_AMBER), with one unified hard invalidation stop beneath the cascade low."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  active_cascade_risk_pct: 0.00 # 100% Cash Lock during live cascade & 4H cooldown
  post_cascade_amber_risk_pct: 0.375 # Initial post-cascade reclaim sizing while Pillar 1 is AMBER
  post_cascade_green_risk_pct: 0.75 # Full 0.75% sizing when Pillar 1 & ETF flows confirm
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Cascade Invariants)

* **Circuit Breaker 1 — The 4-Hour Aftershock Cooldown (`CB-01`):** Forced liquidations clear in multi-wave clusters (`MOD 34` AEGIS-3). Entering during the initial cascade candle exposes capital to secondary forced-margin waves; enforce a strict **4-hour cooldown** after peak 1H liquidation velocity before arming limit bids.
* **Circuit Breaker 2 — Structural Flow Veto Over Derivatives Reset (`CB-02`):** A `-9%` OI flush and `-12%` annualized basis blowout clear *offshore leverage*, **not** institutional spot redemptions. If `MOD 44` (Anthropic IPO / MSCI rebalance) or multi-day US Spot ETF outflows (`MOD 07`) remain active, keep tactical capital in **`100% Cash Lock` (`0.00%` risk)**.
* **Circuit Breaker 3 — 3-Rung Passive Limit Ladder (`CB-03`):** Post-cascade L2 order books remain patchy (`MOD 37`). Split any authorized entry into **3 staggered passive limit orders (`40%` at `1H POC/VAH` reclaim, `35%` at `0.50` Fib / `4H VAL`, `25%` at `0.618–0.786` retest)** to capture maker fills and minimize slippage.
* **Circuit Breaker 4 — Unified `0.75%` Equity Risk Cap (`CB-04`):** Calculate total position size from the blended average entry of the 3 rungs to a single structural stop below the cascade wick low so maximum portfolio loss never exceeds **`0.75%`** (`0.375%` in `GATE_AMBER`).

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-51A: Live Liquidation Cascade & Basis Blowout (`$750M+` Liqs + `OI <= -8%`)
* **Trigger Condition A:** 24H liquidations exceed **`$750M`** (`>= 80%` longs), 24H Open Interest drops **`<= -8.0%`**, annualized perp basis drops **`<= -10.0%`**, and `1H` price volatility exceeds `3.0x` ATR.
* **Observed Outcome B:** Cascading forced deleveraging is actively sweeping L2 bids (`MOD 03` / `MOD 35`).
* **Execution Rule C:** **ENFORCE `100% CASH LOCK` (`0.00%` risk) & START `4-HOUR` COOLDOWN CLOCK (`CB-01`).** Log exact liquidation cluster lows (`MOD 35`) without placing market orders.

### CSU-51B: Post-Cascade Secondary Sweep & Passive Absorption (`T+4H` to `T+24H`)
* **Trigger Condition A:** At least `4 hours` have elapsed since peak 1H liquidations; price sweeps the initial cascade low by `-0.5%` to `-2.0%` on **declining liquidation volume (`< 25%` of peak 1H)** while `Coinbase USD Spot CVD` prints a higher low (`MOD 03 M8` / `MOD 06A` passive absorption) and `Perp Basis` begins curling upward from `<= -10%`.
* **Observed Outcome B:** Weak hands are exhausted and institutional spot buyers are absorbing remaining forced supply at a discount.
* **Execution Rule C:** Verify `MOD 44` and `MOD 07` ETF outflow gates (`CB-02`); if clear, **ARM 3-RUNG PASSIVE LIMIT LADDER (`0.375%` `GATE_AMBER` risk)** with `Net R >= 3.0` (`MOD 37`).

### CSU-51C: Basis Normalization & `4H VAH` Structural Reclaim
* **Trigger Condition A:** Annualized perp basis recovers from `<= -10%` back toward `-2% to +4%`, `1H/4H VAH` is reclaimed for `4+` consecutive `1H` bars, and US Spot ETFs print `>= $0M` net flow (`MOD 07`).
* **Observed Outcome B:** Market structure has transitioned from forced liquidation recovery back into organic spot-led accumulation (`REGIME_5 -> REGIME_2/1`).
* **Execution Rule C:** **UNLOCK FULL `0.75%` SPOT RISK** on pullback retest of `4H VAH / POC`; manage exit via `MOD 18` Two-Stage Protocol (`50%` Stage 1 / `50%` Stage 2 runner).

### CSU-51D: Dead-Cat Basis Snapback Without Spot Demand (Trap Filter)
* **Trigger Condition A:** After a cascade, price bounces `+3%` to `+5%` and perp basis snaps from `-12%` to `+2%` solely via short-covering and fresh offshore perp longs (`Perp OI` rebounding `> +4%`), **while `Coinbase USD Spot CVD` continues falling (`MOD 05C` Quad 3)**.
* **Observed Outcome B:** Fragile leverage reload built on zero spot foundation—high risk of a second cascading leg lower.
* **Execution Rule C:** **REJECT ENTRY & MAINTAIN `100% CASH LOCK`;** wait for the newly reloaded perp longs to flush (`MOD 02` / `MOD 03`).

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed | Mandatory Execution Override |
| :--- | :--- | :--- | :--- |
| **M1: Multi-Day Contagion Cascade (`$1.25B+` Back-to-Back)** | `CSU-51A` | Two consecutive days print `> $1.0B` liquidations alongside `VIX > 28` (`MOD 29`) or exchange solvency stress (`MOD 32`). | **Extend Cooldown to `24–48 Hours` (`100% Cash Lock`)** until cross-asset credit/equity volatility peaks. |
| **M2: `MOD 44` Calendar Vacuum Active During Flush** | `CSU-51B` | OI resets `-9%` and basis hits `-14%`, **but** a `$25B+` Mega-IPO (`Nov 19 ANT`) or MSCI rebalance (`Nov 30`) is still `1–15 days` away. | **Enforce `CB-02` Override:** Stay in `100% Cash Lock` until the calendar deadline clears. |
| **M3: Partial 1-Rung Fill Followed by Immediate Surge** | `CSU-51B` (Ladder Armed) | Rung 1 (`40%` at `1H VAH`) fills, and price immediately rallies `> +1.5R` without dipping to Rungs 2 & 3. | **Cancel Unfilled Lower Rungs Once Price Reaches `+1.5R`;** trail stop to breakeven on filled `40%` tranche (`MOD 18`). |
| **M4: All 3 Rungs Fill + Stop-Out (`-0.75%` Max Loss)** | `CSU-51B` (Ladder Filled) | Price slices through all 3 passive rungs and closes `1H` below the unified structural invalidation stop. | **Execute Hard Stop Immediately (`-0.75%` cap);** trigger `MOD 28 BS-04` audit if 2nd consecutive stop-out. |
| **M5: Extreme Negative Funding (`<= -0.05% / 8H`) Squeeze** | `CSU-51B` / `51C` | After spot absorption confirms, offshore perp funding stays deeply negative (`<= -0.05% / 8H`) as late shorters pile in at resistance (`MOD 01`). | **Hold Stage 2 (`50%`) Runner** to ride forced short-squeeze fuel into HTF `1D POC/VAH`. |
| **M6: L2 Book Depth Remains `< 40%` Median Post-Cooldown** | `T+4H` Post-Cascade | Market makers fail to return after 4 hours, leaving `1%` L2 depth `< 40%` of 30D median (`MOD 37`). | **Halve Maximum Position Size (`0.375%` cap)** to prevent exit slippage (`MOD 37`). |
| **M7: Stablecoin De-Peg Triggered Cascade (`MOD 48 M6`)** | `CSU-51A` | Cascade was triggered by `USDT` or `USDC` de-pegging `<= $0.992`. | **Lock `100% Cash` & Audit Venue Solvency (`MOD 32`);** ban trading until peg restores `>= $0.997` for `6H`. |
| **M8: CoinGlass / Exchange Liquidation API Lag (`MOD 36`)** | Live Volatility | Liquidation aggregator lags during extreme API rate-limiting. | Infer cascade severity directly from **3-venue 1H price drop (`<= -5%`) + exchange OI delta (`<= -8%`)** (`MOD 36`). |
