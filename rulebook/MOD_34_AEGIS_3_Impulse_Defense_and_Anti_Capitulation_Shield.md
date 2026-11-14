# PROJECT CORTEX-BTC — MODULE 34: AEGIS-3 (ASYMMETRIC EXPOSURE & GEOPOLITICAL/IMPULSE SHIELD)
**Waterfall Tier:** Pillar 2 & Pillar 4 Real-Time Impulse Defense & Anti-Capitulation Execution Engine (Upstream 1m–5m/1H–4H Shield).
**Provenance & Empirical Benchmark Anchor:** Codified from the November 4–13, 2026 Structural Cascade Log (`$81,000 -> $68,300` liquidity-starved geopolitical headline cascade) and contrasted against the October 29, 2026 Binance `$6.3B` shock (`-6%` absorbed by `$40.9B` surge volume) — decoupling slow pre-event Structural Fragility (`SFI`) from fast 1m/5m Liquidity Vacuum Execution (`ILVD`) while enforcing a hard `CIRCUIT_LOCK` against panic-selling at exhaustion troughs.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_34"
entry_type: "REALTIME_IMPULSE_SHIELD_AND_SELL_FREEZE"
waterfall_pillar: "PILLAR_2_4_AEGIS3_IMPULSE_SHIELD"
title: "AEGIS-3: 3-Stage Impulse Defense & Anti-Capitulation Sell-Freeze"

# THREE-STAGE EXECUTION CLOCKS
evaluation_clocks:
  stage_1_sfi_pre_event: "1H / 4H cycle + mandatory check 60 min before low-liquidity transitions (23:00 UTC / 07:00 MYT)"
  stage_2_ilvd_streaming: "1m / 5m velocity + Rough Path Levy signed area + asynchronous wire NLP"
  stage_3_exhaustion_lock: "5m / 15m post-impulse liquidation decay & bid replenishment gate"

# STAGE 1: STRUCTURAL FRAGILITY INDEX (SFI in [0, 1])
sfi_thresholds:
  NORMAL_RESILIENT: "SFI < 0.45 -> 100% of strategy target permitted; baseline Stage 2 sensitivity"
  ELEVATED_FRAGILITY: "0.45 <= SFI < 0.70 -> Tighten trailing stops; cap new entries; tighten Stage 2 velocity threshold by 25%"
  CRITICAL_FRAGILITY_PRE_TRIM: "SFI >= 0.70 -> Proactively pre-trim 25%-40% of active spot exposure via TWAP slices during liquid hours"

# STAGE 2: IMPULSE & LIQUIDITY VACUUM DETECTOR (ILVD)
ilvd_triggers:
  session_normalized_velocity_zr: "Z_r = (r_dt - mu_TOD) / sigma_TOD <= -2.2 (relaxed to -1.7 when SFI >= 0.70)"
  nlp_wire_multiplier: "Asynchronous geopolitical/regulatory/halt wire velocity lowers Z_r threshold by 0.3 sigma"
  execution_mechanics: "Slippage-bounded chase slices: 3-5 child limit orders pegged 2-5 bps inside best bid over 5-10 min, re-pegging every 15s (zero blind market dumps)"

# STAGE 3: HARD SELL-FREEZE (CIRCUIT_LOCK = TRUE)
circuit_lock_conditions_any_two:
  - "Rolling 4H cross-exchange long liquidations > 95th historical percentile"
  - "Intraday drawdown from UTC open > -3.8% within < 4 hours alongside > 3.5 sigma 15m volatility spike"
  - "Spot order-book bid replenishment ratio > 1.2x ask replenishment after psychological level sweep"

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
  exit_protocol: "AEGIS3_BOUNDED_LIMIT_SLICING"
```

---

## 2. Protective Circuit Breakers (AEGIS-3 Operational Invariants)

* **Circuit Breaker 1 — State-Before-Catalyst Asymmetry (`CB-01`):** Exogenous headlines (even unverified geopolitical claims, such as the Nov 13 IRGC Bahrain radar report) do not cause vertical crashes on their own; they detonate pre-existing liquidity-starved books. Defensive pre-trimming (`Stage 1 SFI >= 0.70`) must execute *before* low-liquidity session transitions (`23:00 UTC / 07:00 MYT`) when ETF outflows and thin depth converge.
* **Circuit Breaker 2 — No Blind Market Dumps in Thin Books (`CB-02`):** During active liquidity vacuums, raw market sell orders cross empty order-book ticks and suffer severe slippage. All `Stage 2` exits must execute via **bounded limit-chase slices** (`3–5` child slices pegged `2–5 bps` inside best bid, re-pegging every `15 seconds`).
* **Circuit Breaker 3 — Anti-Capitulation Sell-Freeze (`CB-03 / CIRCUIT_LOCK`):** Once forced long liquidations blow off (`~3 to 4 hours` after initial wire trigger), expected value flips violently from selling to waiting. `CIRCUIT_LOCK` physically blocks automated or discretionary spot selling at the exhaustion trough.
* **Circuit Breaker 4 — Staged Post-Flush Re-Entry (`CB-04 / RECOVERY_GATE`):** Preserved cash remains locked until 1H liquidation velocity drops below `25%` of cascade peak for 2 consecutive hours and 1H Domestic USD Spot CVD turns net positive.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-34A: Pre-Event Critical Fragility (`SFI >= 0.70` — `PRE_TRIM` State)
* **Trigger Condition A (The Telemetry Scan):**
  1. Normalized **Structural Fragility Index ($\text{SFI} \ge 0.70$)** across four components: multi-day US Spot ETF net outflows + contracting stablecoin supply ($x_1$), top-of-book `1%–2%` bid depth well below 30D session median ($x_2$), rising perp OI/funding against negative Spot CVD ($x_3$), and defensive 25D put skew near dense long liquidation shelves ($x_4$).
  2. Approaching low-liquidity session handoff (`23:00 UTC / 07:00 MYT` or weekend close).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Microstructure Lens:** Bid-side cushion is hollow; any unverified wire or macro surprise can trigger an 85-minute vertical cascade.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **PROACTIVELY PRE-TRIM `25%–40%` OF OPEN SPOT EXPOSURE** via passive/TWAP slices during liquid NY/overlap hours before volatility spikes; block all new swing entries.

### CSU-34B: Impulse & Liquidity Vacuum Breakdown (`ILVD` Fires — `IMPULSE_EXIT` State)
* **Trigger Condition A (The Telemetry Scan):**
  1. **Session-Normalized Return Velocity ($Z_r \le -2.2$, or $\le -1.7$ when $\text{SFI} \ge 0.70$)** on 15m/30m log returns (`further relaxed by 0.3 sigma` if asynchronous wire NLP detects geopolitical escalation, exchange halt, or regulatory shock).
  2. **Order-Flow Confirmation:** Aggressive market-sell delta accelerates on Spot CVD while Order $N \le 2$ **Rough Path Lévy Signed Area ($\mathcal{A}_{p,v}$)** turns sharply negative (`MOD 08`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Microstructure Lens:** Normal two-way chop has mutated into a one-sided liquidity vacuum ahead of major psychological stop clusters (`e.g., $70,000`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **EXECUTE BOUNDED LIMIT-CHASE EXIT (`0%–25%` target exposure remaining)** using `3–5` sliced limit orders pegged `2–5 bps` inside best bid over `5–10 minutes` (re-pegging every `15s`).

### CSU-34C: Capitulation Blow-Off & Hard Sell-Freeze (`CIRCUIT_LOCK = TRUE`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Any **two of three** exhaustion conditions trigger simultaneously during a sharp drop:
     * Rolling 4H long liquidations exceed the **95th historical percentile**.
     * Intraday drawdown from UTC open exceeds **`-3.8%` within `< 4 hours`** alongside a **`> 3.5 sigma`** 15m volatility spike.
     * Spot order-book **bid replenishment ratio exceeds `1.2x` ask replenishment** after sweeping a psychological level.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Microstructure Lens:** Forced margin selling has reached peak climax (`typically ~3.5 hours after initial headline wire`). Selling here locks in the exact bottom tick.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENGAGE HARD SELL-FREEZE (`CIRCUIT_LOCK = TRUE`).** Zero market or limit selling permitted; transition immediately to `RECOVERY_GATE` monitoring.

### CSU-34D: Post-Cascade Stabilization & Tranched Redeployment (`RECOVERY_GATE`)
* **Trigger Condition A (The Telemetry Scan):**
  1. 1H liquidation rate decays below **`25%` of cascade peak** for **2 consecutive hours**.
  2. 1H **Domestic USD Spot CVD** flattens and turns net positive while price holds above the cascade trough.
  3. Core `MOD 18 / MOD 33` waterfall confirms valid entry confluence (`R >= 3.0`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Microstructure Lens:** Passive limit buyers have absorbed the cascade; clean post-flush base is forming (`MOD 30 CONFIG_F`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **REDEPLOY PRESERVED CASH IN 2–3 TRANCHES** capped strictly within the `0.75%` (`or 0.375% Amber`) Sovereign Risk Shield.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Unverified Wire Detonation** | `PRE_TRIM` (`SFI >= 0.70`) | Unverified geopolitical/regulatory wire triggers `-0.75% -> -1.5%` drift (`Z_r <= -1.7`) before mainstream confirmation. | Thin book cascades on headline velocity regardless of factual verification. | **Trigger `CSU-34B` Bounded Limit-Chase Exit immediately** before psychological floor breaks. |
| **M2: Deep-Book Shock Absorption** | `NORMAL` (`SFI < 0.45`) | Major negative headline hits, **but spot volume surges `+50%+`, bid replenishment `> 1.3x`, and `SFI < 0.45`** (benchmark: Oct 29 Binance `$6.3B` shock). | Deep diversified liquidity is absorbing the shock without cascading. | **Suppress Panic Trim;** wait for `MOD 32` Solvency Ratio & `0.618` reclaim check. |
| **M3: Trough Capitulation Lock** | `IMPULSE_EXIT` (Mid-Drop) | While slicing out, 4H liquidations cross 95th pct and drawdown hits `-4.0%` in `< 3.5h` with surging bid replenishment. | Cascade reached terminal exhaustion while slices were still working. | **Cancel Remaining Unfilled Sell Slices (`CIRCUIT_LOCK = TRUE`)**—never sell the trough. |
| **M4: False Velocity Fakeout** | `IMPULSE_EXIT` (Whipsaw) | `Z_r` briefly touches `-2.2` on a 5m wick, but immediately reclaims 15m VWAP with positive USD Spot CVD. | Isolated stop-hunt wick rather than sustained liquidity vacuum. | **Hold Preserved Cash until `RECOVERY_GATE` confirms**; accept minor whipsaw tax as insurance. |
| **M5: Secondary Aftershock Leg** | `CIRCUIT_LOCK` (1–2h Post-Low) | 1H liquidations fail to stay `< 25%` of peak; price loses the cascade trough on fresh expanding sell volume (`Z_r <= -2.2`). | Initial pause was a bear flag; a second waterfall leg is starting. | **Temporarily Lift `CIRCUIT_LOCK` for Remaining Tactical Exposure** if `SFI` remains `>= 0.70`. |
| **M6: Session Handoff Vulnerability** | `0.55 <= SFI < 0.70` | Approaching `23:00 UTC (07:00 MYT)` Asian thin-liquidity window with dense long liquidations `< 2%` below spot. | Overnight Asian desks have thin bid depth to defend psychological shelves. | **Treat as `SFI >= 0.70` (`PRE_TRIM`)** ahead of the `23:00 UTC` session handoff. |
| **M7: NLP Wire False Alarm** | `PRE_TRIM` Watch | Wire NLP flags escalation keywords, **but `Z_r > -1.2` and Spot CVD remains flat/positive** for 30 minutes. | Market ignored the headline; order flow refuses to break down. | **Do Not Fire `Stage 2` Exit;** require dual confirmation (`Velocity + Flow`). |
| **M8: Post-Cascade Re-Entry Abort** | `RECOVERY_GATE` | Liquidations decay `< 25%`, **but rebound lacks USD Spot CVD** (perp-only dead-cat bounce with rising OI). | Leverage is reloading prematurely without real spot accumulation (`MOD 03 M3`). | **Block Re-Entry Tranches;** remain in cash until genuine spot CVD steps in. |
