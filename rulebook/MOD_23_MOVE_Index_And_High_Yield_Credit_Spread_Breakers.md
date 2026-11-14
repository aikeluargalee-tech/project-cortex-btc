# PROJECT CORTEX-BTC — MODULE 23: MOVE INDEX (BOND VOLATILITY) & HIGH-YIELD CREDIT SPREAD BREAKERS
**Waterfall Tier:** Pillar 1 (Fixed-Income Systemic Stress & Cross-Asset Margin Risk Early-Warning Radar) cross-verified with Pillar 4 (Portfolio Engineering).
**Empirical Benchmark Anchor:** November 2026 Fixed-Income Telemetry — ICE BofA **MOVE Index** (US Treasury Implied Volatility) jumping to **92.44** alongside the US 10-Year Yield surging to **5.129%** following hot October CPI, triggering cross-asset duration repricing and draining liquidity from high-beta assets including Bitcoin.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_23"
entry_type: "MASTER_PERMISSION_GATE"
waterfall_pillar: "PILLAR_1_FIXED_INCOME_STRESS_BREAKER"
title: "MOVE Index (Bond Volatility) & High-Yield Credit Spread Breakers"

# MASTER WATERFALL AUTHORITY (SYSTEMIC RISK CIRCUIT BREAKER)
waterfall_authority: "SYSTEMIC_CREDIT_CIRCUIT_BREAKER"

# PRIMARY TELEMETRY TRIGGERS (RATES VOLATILITY & CREDIT SPREADS)
base_regime_triggers:
  move_index_levels:
    CALM_RISK_ON: "MOVE Index < 85 and trending downward (smooth collateral pricing)"
    ELEVATED_CAUTION: "MOVE Index between 90 and 115 (benchmark 92.44 in Nov 2026; rising rate uncertainty)"
    SYSTEMIC_STRESS_LOCK: "MOVE Index >= 120 to 130+ OR 5-day MOVE surge >= +20% (collateral haircut shock)"
  hy_credit_spreads:
    oas_spread_trigger: "ICE BofA US High Yield OAS widening >= +40 bps in 10 sessions (or HYG ETF breaking 200D MA on volume)"

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_PREMATURE_CLOSE: "NEVER buy a Bitcoin technical support bounce while the MOVE Index is surging >= +15% in a week or HY credit spreads are blowing out."
  CB_02_VENUE_CONTAMINATION: "Verify MOVE Index and HY OAS using official end-of-day ICE BofA / FRED data alongside intraday US Treasury futures (ZN/ZB) volatility."
  CB_03_FORCED_FLOW_STANDDOWN: "When MOVE >= 120, prime brokers raise haircuts on Treasury collateral—forcing hedge funds to sell liquid 24/7 assets (BTC) for cash. Lock 100% Cash."
  CB_04_SIGNAL_HALF_LIFE: "Bond volatility shocks govern 3-day to 4-week cross-asset risk-off regimes; wait for MOVE to peak and roll over before re-entering BTC."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  calm_regime_max_risk_pct: 0.75
  elevated_move_max_risk_pct: 0.375
  systemic_stress_max_risk_pct: 0.00 # Emergency 100% Cash Lock
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Pre-Execution Filters)

Why **MOVE Index** and **High-Yield (Junk) Credit Spreads** act as Bitcoin's systemic early-warning system:
* US Treasuries are the foundational collateral of the entire global financial system. When **MOVE** (bond volatility) spikes, prime brokers and clearinghouses mechanically increase margin haircuts on Treasury collateral—forcing multi-strategy hedge funds to raise cash immediately by selling their most liquid, 24/7-traded asset: **Bitcoin**.
* **Circuit Breaker 1 — The Collateral Haircut Rule (`CB-03`):** Whenever `MOVE >= 120` (or surges `>= +20%` in 5 days), Bitcoin ceases trading on crypto fundamentals and trades strictly as an institutional ATM for cash raising. **100% Cash Lock is mandatory.**
* **Circuit Breaker 2 — Credit Spread Confirmation (`CB-01`):** Rising 10Y yields driven by *healthy economic growth* (`HY credit spreads tight/falling`) are manageable for Bitcoin; rising yields or falling yields driven by *credit stress* (`HY OAS widening >= +40 bps`) trigger systemic deleveraging.
* **Circuit Breaker 3 — Volatility Peak Inflection:** The exact bottom of a cross-asset liquidation wave almost always coincides with the **intraday peak of the MOVE Index**—not before.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-23A: Calm Bond Volatility & Tight Credit Spreads ("Clean Collateral Tailwind")
* **Trigger Condition A (The Telemetry Scan):**
  1. **ICE BofA MOVE Index** sits below **`85`** (or trends steadily lower from elevated levels).
  2. **US High-Yield Credit Spreads (HY OAS)** are stable or compressing (`HYG` trading above its 50D/200D MA).
  3. Supported by `MOD 16` (`DXY stable/falling`, `Stablecoins expanding`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Predictable bond pricing lowers collateral haircuts across prime brokers, encouraging institutional risk-taking and steady inflows into Bitcoin spot and ETFs.
  * **Probable Trajectory:** Low cross-asset correlation shocks; Bitcoin trades cleanly according to its internal Pillar 2, 3, and 5 supply/demand mechanics.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`PERMIT FULL 0.75% RISK CEILING`** across validated Pillar 2/3 setups.

### CSU-23B: Elevated Rate Volatility Regime ("MOVE 90–115 Caution Zone")
* **Trigger Condition A (The Telemetry Scan):**
  1. **MOVE Index** rises into the **`90 to 115` zone** (benchmark: **92.44** on Nov 12–13, 2026) as Treasury yields reprice rapidly around inflation/Fed uncertainty, while HY credit spreads remain contained (`< +30 bps` widening).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional desks reduce gross leverage and widen stop buffers ahead of rate volatility, thinning out Bitcoin order-book depth (`$72M depth`).
  * **Probable Trajectory:** Choppy, headline-sensitive price action with sharp intraday wicks around US bond market hours (`12:00–20:00 UTC`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`CAP PILLAR 1 AT GATE_AMBER (Max 0.375% Risk)`** (or `GATE_RED` if combined with `MOD 16C` stablecoin drain). Require wider Garman-Klass stop calibration (`MOD 12`).

### CSU-23C: Systemic Bond & Credit Stress Shock ("MOVE >= 120 / Credit Blowout Cash Lock")
* **Trigger Condition A (The Telemetry Scan):**
  1. **MOVE Index spikes above `120–130+`** (or jumps `>= +20%` within 5 sessions), **OR** **High-Yield Credit Spreads (HY OAS)** widen by `>= +40 to +75 bps` in 10 sessions (`HYG` breaking down sharply).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Active systemic liquidity crunch—institutions are facing margin calls across bond and credit books and liquidating Bitcoin spot/ETFs indiscriminately for USD cash.
  * **Probable Trajectory:** Violent multi-day correlation-1.0 sell-off across equities, credit, and crypto.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Gate Output:** **`EMERGENCY PILLAR 1 = GATE_RED_100_CASH_LOCK`.**
  * **Action:** Close 100% of active swing positions immediately; block all dip-buying until `Mutation M1` confirms MOVE and credit spreads have peaked.

### CSU-23D: Post-Crisis Bond Volatility Crush ("MOVE Peak Reversal Entry")
* **Trigger Condition A (The Telemetry Scan):**
  1. After spiking above `120+`, the **MOVE Index prints a sharp reversal downward (`dropping >= -15% off peak` over 3–5 sessions)** as Fed intervention or dovish policy calms Treasury markets.
  2. Bitcoin holds a higher-timeframe support floor (`MOD 03A / 13D`) and **Domestic USD Spot CVD** turns positive.
* **Observed Outcome B (The Mechanical Trajectory):**
  Collateral haircuts relax and forced institutional liquidation stops abruptly—releasing pent-up spot demand into an oversold Bitcoin market.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** Upgrade Pillar 1 from `GATE_RED` to `GATE_AMBER` (`0.375% Risk`), authorizing Spot Long entry upon 15m/1H **VAH/VAL reclaim** confirmed by USD Spot CVD.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: MOVE Peak & Roll-Over** | `CSU-23C` (Stress Lock) | MOVE spikes to `125+`, then drops for **3 consecutive sessions (`< 105`)** while HY credit spreads stop widening. | Acute fixed-income liquidation phase has passed its climax. | Lift emergency stress freeze; move to `CSU-23D` watch for Pillar 2 VAL reclaim. |
| **M2: Credit Contagion Escalation** | `CSU-23B` (MOVE 90–115) | MOVE stays near `95`, **but High-Yield OAS suddenly widens `> +50 bps`** and regional bank/credit equities plunge. | Rate volatility just mutated into corporate credit default stress. | **Immediate Downgrade to `GATE_RED_100_CASH_LOCK`.** |
| **M3: Benign Yield Rise (Growth Reflation)** | `CSU-23A` (Calm) | 10Y Yield ticks up `+15 bps`, **but MOVE stays `< 82` and HY credit spreads tighten** (equities making new highs). | Yield rise reflects healthy nominal growth rather than liquidity stress. | **Do Not Trip Cash Lock:** Maintain `GATE_GREEN` if stablecoins (`MOD 16`) are expanding. |
| **M4: Treasury Auction Tail Shock** | `17:00 UTC` Auction Window | Weak 10Y or 30Y US Treasury auction triggers an immediate `+10 bps` yield spike and MOVE jump intraday. | Dealer balance sheets choked on Treasury supply, draining intraday risk appetite. | **Suspend Intraday Long Entries for 24 Hours** until bond market digests auction supply. |
| **M5: Corporate Spread Compression Wave** | `CSU-23D` (Recovery) | HY OAS compresses `-40 bps` over 2 weeks while MOVE drops back below `85` and Bitcoin reclaims 200D MA. | Full cross-asset risk-on normalization. | **Promote Pillar 1 to `GATE_GREEN_FULL_RISK` (`0.75%`)**. |
| **M6: Sovereign Debt Ceiling / Shutdown Standoff** | Any State | T-Bill yields at specific maturity dates spike (`kink in T-bill curve`) alongside MOVE surge. | Technical default/plumbing anxiety creating acute cash hoarding. | **Enforce 100% Cash Lock** until legislative resolution clears the T-bill kink. |
| **M7: BTC-Gold Safe-Haven Decoupling** | `CSU-23B` / `23C` | MOVE spikes above `115` due to fiscal deficit fears, **yet Bitcoin rises alongside Gold** with positive Domestic USD Spot CVD (`> +0.10%` Coinbase Premium). | Rare sovereign-debt-flight regime where BTC trades as digital gold rather than tech beta. | **Allow Half-Size (`0.375%`) Spot Long** *only* if 4H VAH holds AND Coinbase Premium is strongly positive. |
| **M8: Friday Bond Close Stabilization** | Friday `20:00 UTC` | After a volatile week, 10Y yields settle lower and MOVE closes near weekly lows on Friday afternoon. | Removes weekend macro overhang heading into Asian/crypto weekend sessions. | Clear `CB-01` weekend macro caution; evaluate Sunday/Monday `MOD 20` gap setups normally. |
