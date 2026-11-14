# PROJECT CORTEX-BTC — MODULE 25: DEALER GAMMA EXPOSURE (GEX) & ZERO-GAMMA FLIP MECHANICS
**Waterfall Tier:** Pillar 2 & Pillar 3 Bridge (Options Market-Maker Delta-Hedging Flows & Volatility Amplification) cross-verified with Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 10–13, 2026 Deribit & Multi-Venue Options Telemetry — Aggregate BTC options Open Interest standing at **434,345 BTC ($32.85B)** across Deribit (`78.9%`), OKX (`10.2%`), Binance (`5.0%`), Bybit (`4.4%`), and Delta (`1.4%`), with the **Zero-Gamma Flip Level anchored at $75,000**, **Call Wall at $90,000**, and **Put Wall at $70,000**—so once spot broke below **$75,000**, dealers flipped into **Negative Gamma** and were mechanically forced to sell into the drop toward **$68,450**.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_25"
entry_type: "CONDITIONAL_SIGNAL_UNIT"
waterfall_pillar: "PILLAR_2_3_OPTIONS_GAMMA_MECHANICS"
title: "Dealer Gamma Exposure (GEX) & Zero-Gamma Flip Mechanics"

# PILLAR 1 MASTER PERMISSION PRE-CHECK
pillar_1_permission_required: true
cash_lock_override: "If Pillar 1 Macro Regime == RISK_OFF_100_CASH and Spot < Zero_Gamma_Flip, negative gamma accelerates downside—enforce 100% Cash Lock."

# PRIMARY TELEMETRY TRIGGERS (DEALER DELTA-HEDGING REGIMES)
base_regime_triggers:
  zero_gamma_flip_level: "Strike price where aggregate Net Dealer GEX crosses 0.0 (benchmark $75,000 in Nov 2026)"
  positive_gamma_regime: "Spot_Price > Zero_Gamma_Flip AND Net_GEX > 0 (Dealers buy dips, sell rallies -> volatility suppression)"
  negative_gamma_regime: "Spot_Price < Zero_Gamma_Flip AND Net_GEX < 0 (Dealers sell dips, buy rallies -> momentum amplification)"
  major_gamma_walls: "Call Wall (largest positive GEX overhead strike; benchmark $90K) and Put Wall (largest negative GEX support strike; benchmark $70K)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy a falling knife in a Negative Gamma regime (Spot < Zero-Gamma Flip) until a major Put Wall is swept and reclaimed with Domestic USD Spot CVD."
  CB_02_VENUE_CONTAMINATION: "Compute Net GEX across Deribit (core ~80% liquidity) + OKX/Binance/Bybit composite option chains."
  CB_03_FORCED_FLOW_STANDDOWN: "When Spot breaks cleanly below the major Put Wall (e.g., losing $70K Put Wall), dealers must aggressively short futures to hedge—stand down 100% in Cash."
  CB_04_SIGNAL_HALF_LIFE: "GEX walls reset sharply after weekly/monthly Friday 08:00 UTC expiries; always recompute the Zero-Gamma Flip immediately post-expiry."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  negative_gamma_stop_multiplier: 1.5 # Widen stops by 1.5x in Negative Gamma to avoid dealer-hedging whip-wicks
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "TWO_STAGE_STRUCTURAL"
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Why **Dealer Gamma Exposure (GEX)** governs whether breakouts stick or mean-revert:
* Options market makers (dealers) remain delta-neutral by dynamically hedging their book in spot and perpetual futures:
  * **Above the Zero-Gamma Flip (`Positive Gamma`):** Dealers are net long gamma—when price rises, they **sell** futures; when price drops, they **buy** futures. This dampens volatility and pins price inside ranges.
  * **Below the Zero-Gamma Flip (`Negative Gamma`):** Dealers are net short gamma—when price drops, they are mechanically forced to **sell** futures into the hole; when price rises, they are forced to **buy** into the rally. This creates violent trend acceleration and wide ranges.
* **Circuit Breaker 1 — Put-Wall Breach Stand-Down (`CB-03`):** The **Put Wall** (strike with largest put OI/negative gamma, e.g., `$70,000`) acts as support *only* while spot stays above it. Once price breaks decisively *below* the Put Wall, dealer delta-hedging flips into forced selling, accelerating the drop toward the next lower strike cluster.
* **Circuit Breaker 2 — Negative Gamma Stop Calibration (`CB-04`):** In a Negative Gamma regime, intraday swings expand by `1.5x–2.0x`. Always widen your structural stop distance accordingly and shrink BTC position size so your dollar loss never exceeds `0.75%`.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-25A: Zero-Gamma Flip Reclaim ("Transition From Acceleration to Institutional Pinning")
* **Trigger Condition A (The Telemetry Scan):**
  1. Bitcoin reclaims the **Zero-Gamma Flip Level** from below (benchmark: reclaiming **$75,000**) with a confirmed 1H/4H Volume Profile **VAH** close.
  2. **Order-Flow Confirmation:** **Domestic Fiat (USD) Spot CVD** (`MOD 05/19`) is positive, and dealer short-gamma covering forces market makers to buy futures as price crosses the flip point.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Market structure transitions from unstable downward acceleration into dealer-stabilized upward drift toward the overhead **Call Wall** (`$80K–$90K`).
  * **Probable Trajectory:** Sharp initial squeeze through the Zero-Gamma Flip followed by orderly, supported trend progression.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** on a 15m/1H pullback retest of the reclaimed **Zero-Gamma Flip Level** with positive Domestic USD Spot CVD.
  * **Position Sizing Formula (0.75% Risk Ceiling):**
    `Spot Position (BTC) = (0.0075 * Total Portfolio Equity) / (Entry Price - Invalidation Stop Price)`
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (50% of Position):** Close 50% halfway to or at the first major **Positive Gamma Peak / Call Wall** (where dealer selling dampens upside); move stop to breakeven.
    * **Stage 2 Exit (Remaining 50%):** Trail behind 4H VAL or close fully at the primary **Call Wall**.

### CSU-25B: Put-Wall Sweep & Reclaim in Negative Gamma ("Dealer Short-Cover Reversal")
* **Trigger Condition A (The Telemetry Scan):**
  1. In a Negative Gamma regime (`Spot < Zero-Gamma Flip`), price sweeps downward through the major **Put Wall** (e.g., sweeping below `$70,000` toward `$68,000`), triggering peak dealer hedging sales and perp liquidations (`MOD 03A`).
  2. **Reclaim Confirmation:** Price snaps back **above the Put Wall** on the 15m/1H chart, **Domestic USD Spot CVD** surges positive (`absorbing the dealer hedge flow`), and 1H VAL is reclaimed.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Because dealers are short gamma below the flip, once spot reclaims the Put Wall, those exact same dealers are mechanically forced to **buy back** the futures they just sold—fueling a rapid squeeze back toward the Zero-Gamma Flip.
  * **Probable Trajectory:** Fast V-shaped mean-reversion rally from the Put Wall back toward the Zero-Gamma Flip level.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Entry Trigger:** Execute **Unleveraged Spot Long** upon confirmed **15m/1H close back above the Put Wall + VAL** backed by positive USD Spot CVD, sized strictly to `0.75%` (`0.375%` if Pillar 1 is `GATE_AMBER`).
  * **Two-Stage Profit Exit Protocol:**
    * **Stage 1 Exit (60% of Position):** Close 60% just below the **Zero-Gamma Flip Level** (where dealer buying pressure neutralizes); move stop to breakeven.
    * **Stage 2 Exit (Remaining 40%):** Hold only if price breaks cleanly through the Zero-Gamma Flip (`CSU-25A`).

### CSU-25C: Negative Gamma Breakdown Below Put Wall ("Dealer Hedging Waterfall")
* **Trigger Condition A (The Telemetry Scan):**
  1. Spot trades below the **Zero-Gamma Flip** (`Net GEX < 0`) AND breaks cleanly **below the major Put Wall** (`1H close below Put Wall`) with **Domestic USD Spot CVD negative**.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Market makers are forced to sell progressively larger amounts of spot/futures as price falls further into negative gamma territory, creating an air-pocket cascade toward the next lower open-interest strike.
  * **Probable Trajectory:** Rapid downward acceleration with failed minor bounces.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE STRICT 100% CASH LOCK.** Stand down completely until price reaches the next major lower strike cluster and satisfies `CSU-25B` reclaim rules.

### CSU-25D: Positive Gamma Call-Wall Pinning ("Low-Volatility Mean-Reversion Chop")
* **Trigger Condition A (The Telemetry Scan):**
  1. Spot trades cleanly above the **Zero-Gamma Flip (`Net GEX >> 0`)** and approaches a massive overhead **Call Wall** (e.g., `$90,000` with `$20M+` gamma density), while Garman-Klass volatility compresses (`MOD 12`).
* **Observed Outcome B (The Mechanical Trajectory):**
  Dealers sell into every uptick near the Call Wall and buy every dip toward the Zero-Gamma Flip, pinning price in a tight range.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **BANK STAGE 2 PROFITS AT THE CALL WALL.** Do not chase breakouts directly into a massive Call Wall until after OpEx expiry clears the gamma concentration (`MOD 26`).

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Put-Wall Collapse Cascade** | `CSU-25B` (At Put Wall) | Price touches the Put Wall (`$70K`), bounces briefly, then **closes 1H below Put Wall on expanding volume and negative USD Spot CVD**. | Put Wall breached; dealers forced into aggressive downside delta-hedging (`CSU-25C`). | **Immediate Hard Stop / Lock 100% Cash.** |
| **M2: Zero-Gamma Flip Rejection** | `CSU-25B` (Rallying) | Price rallies from Put Wall right up to the **Zero-Gamma Flip (`$75K`)**, fails to break above, and USD Spot CVD turns negative. | Dealer short-cover tailwind ended at the flip point; overhead call resistance held. | **Stage 1 (60%) already banked**; close remaining 40% immediately at the Zero-Gamma Flip rejection. |
| **M3: Post-OpEx Gamma Unclench** | Friday `08:00 UTC` Expiry | Major monthly/quarterly Deribit expiry settles at `08:00 UTC`, wiping out `> 30%` of total GEX and removing the Call/Put Wall pin. | Dealer hedging constraints vanish; price is released for a directional trend move (`MOD 26`). | Watch the first post-expiry NY session (`13:30 UTC`) for `MOD 11B` VAH breakout with USD Spot CVD. |
| **M4: Zero-Gamma Flip Migration Downward** | `CSU-25C` (Bear Trend) | Options traders roll puts lower and sell calls at lower strikes, dragging the **Zero-Gamma Flip level down** closer to spot price. | Makes it easier for a modest spot rally to flip dealers back into Positive Gamma support. | Update daily Zero-Gamma Flip coordinate in Python/HUD (`re-arm CSU-25A at new lower flip level`). |
| **M5: Call-Wall Roll-Up Squeeze** | `CSU-25D` (At Call Wall) | Spot pushes into the Call Wall with strong **USD Spot CVD**, and options traders aggressively buy higher-strike calls (`Call Wall rolls up +$5K`). | Dealer short-gamma exposure above the old wall forces market makers to chase spot higher. | Hold `Stage 2` runner; trail stop directly beneath the old Call Wall (now support). |
| **M6: 0DTE / Front-Expiry Gamma Spike** | `< 24h` to Expiry | Front-expiry gamma concentration surges (`gamma spikes as time-to-expiry -> 0`), causing violent intraday ping-pong around a single strike. | Extreme short-dated gamma pinning (`MOD 26`). | **Avoid Intraday Breakout Trades** within 12 hours of major Friday `08:00 UTC` expiry. |
| **M7: Multi-Venue Flip Divergence** | Any State | Deribit-only Zero-Gamma Flip sits at `$75,000`, while 5-exchange composite flip sits at `$76,500` due to offshore retail call/put skew. | Zone between `$75,000` and `$76,500` is a transitional neutral-gamma buffer. | Require full clearance above the **higher composite flip** before assuming full Positive Gamma stability. |
| **M8: Negative Gamma + Negative Basis Sync** | `MOD 25C` + `MOD 01` | Spot is in Negative Gamma (`< Flip`) AND perpetual basis is deeply negative (`< -0.04%`) with surging OI. | Maximum two-way explosive fragility: breakdown triggers cascading flushes, while VAL reclaim triggers violent squeeze. | Strictly obey `MOD 03A` + `CSU-25B` reclaim trigger—zero guessing before reclaim confirms. |
