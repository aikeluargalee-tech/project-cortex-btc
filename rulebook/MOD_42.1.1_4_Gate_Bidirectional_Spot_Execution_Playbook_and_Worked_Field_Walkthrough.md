### PROJECT CORTEX-BTC — MODULE 42.1.1: 4-GATE BIDIRECTIONAL SPOT EXECUTION PLAYBOOK & WORKED FIELD WALKTHROUGH
**Waterfall Tier:** Pillar 2 & Pillar 4 Operational Field Runbook (Step-by-Step `USDT <-> BTC` Execution Workflow & Worked Examples) — child operational reference of **MOD 42.1 (The Symmetrical 11-Pattern Price Action & Microstructure Playbook)** and **MOD 42 (Classical Structural Shapes & Liquidity-Pool Authentication Engine)**, integrated with **MOD 05** (Spot vs. Perp CVD), **MOD 11** (Volume Profile Topology), **MOD 18** (`0.75%` Spot Risk Sizing & Two-Stage Exit), **MOD 31** (`ICDM` Fragility Gate), **MOD 37** (`Net R >= 3.0`), **MOD 54** (MTF Kline Lock), **MOD 60** (Veto Precedence), **MOD 62** (`DIBSE v2.0`), and **MOD 65** (`CB-02` Multi-Step Sequence).
**Document Provenance:** Codified from the live November 2026 operational walkthrough of `MOD 42.1` inside `DIBSE v2.0` (`MOD 62`).
**Governance Posture:** Quick-Reference Execution Runbook & Worked Sizing Calibration (`1.0x` Unleveraged Spot BTC/USDT Only). Every pattern runs sequentially through **Gate 1 (Location & Macro Permission) → Gate 2 (Pattern Match) → Gate 3 (Microstructure Confirmation) → Gate 4 (Sizing & Hard Invalidation)**—never trade a pattern in isolation.

---

#### 0. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)
```yaml
module_id: "MOD_42.1.1"
parent_module: "MOD_42.1"
root_module: "MOD_42"
entry_type: "OPERATIONAL_FIELD_WALKTHROUGH_AND_QUICK_REFERENCE"
waterfall_pillar: "PILLAR_2_AND_4_4GATE_BIDIRECTIONAL_SPOT_RUNBOOK"
title: "4-Gate Bidirectional Spot Execution Playbook & Worked Field Walkthrough"

execution_sequence:
  gate_1: "HTF Location (POI) & Pillar 1 Macro Permission Check"
  gate_2: "Structural Pattern Match (#1-#11 Symmetrical Registry)"
  gate_3: "Microstructure & Momentum Confirmation (Rulebooks 3.1-3.4 / Footprint / RSI+AO)"
  gate_4: "1.0x Spot Sizing Formula, Net R >= 3.0 & Hard Invalidation"

loop_routing:
  loop_a_accumulation: "USDT -> BTC (Patterns #1, #3, #5, #7, #10 — Blocked when Pillar 1 == GATE_RED)"
  loop_b_distribution: "BTC -> USDT (Patterns #2, #4, #6, #8, #9, #11 — Authorized under GATE_RED to protect Sleeve A BTC)"

sizing_invariants:
  leverage_permitted: 1.0
  gate_amber_risk_pct: 0.375
  gate_green_risk_pct: 0.75
  gate_red_long_risk_pct: 0.00
  min_net_reward_to_risk: 3.0
```

---

#### I. Part 1 — Defensive Distribution (`Loop B: BTC → USDT`) at Resistance
*Operational Scenario: Holding active `Sleeve A` spot BTC while price rallies into overhead resistance (`$64,000–$66,000`), mirroring the Nov 18–19, 2026 relief rally prior to breakdown.*

1. **Gate 1 — HTF Location & `Pillar 1` Check:**
   * **Location:** Identify an established `4H/1D` `Supply Cluster` or flipped `HVN` resistance (`$64,000–$66,000`). Never execute a distribution rotation in mid-range air.
   * **Macro Permission:** When `Pillar 1` is `GATE_RED` (e.g., `ICDM 77.0`, `-$3.47B` November ETF outflows), `MOD 42.1` (`pillar_1_upstream_override`) blocks new `USDT → BTC` buys but **authorizes** `BTC → USDT` distribution patterns (`#2, #4, #6, #8, #9, #11`) to protect existing `Sleeve A` BTC inventory.
2. **Gate 2 — Structural Pattern Match:**
   * Drop to `15m/1H` inside the `$64,000–$65,500` supply zone and classify the price interaction:
     * **Pattern #9 (`The Mouse Trap`):** Price surges into `$64k` with speed, stalls at flat `Poor Highs`, sweeps above them to trap breakout buyers, and snaps back inside.
     * **Pattern #2 (`Double Top Sweep`)** or **Pattern #6 (`Rounded Retest Short`):** Price pierces a prior swing high (`SFP`) inside supply and closes back below it.
3. **Gate 3 — Bearish Microstructure Confirmation (Rulebooks `3.1`–`3.4`):**
   * Require at least **two** of the four deterministic `MOD 42.1` confirmations before rotating `BTC → USDT`:
     * **Rulebook `3.1` (Spot vs. Perp CVD Divergence):** Price and `Perp CVD` print higher highs on the sweep, while **Domestic USD `Spot CVD` prints a lower high or stays flat** (spot holders distributing into leveraged perp chasing).
     * **Rulebook `3.2` (`OI` Spike + Positive Funding Snap):** `BTC`-denominated Open Interest jumps and funding turns positive *during* the sweep wick, followed by a candle close back **below** the swept high (trapping late longs).
     * **Rulebook `3.3` (`"P"`-Shaped Profile Breakdown):** Pull a Fixed-Range Volume Profile (`FRVP`) from the rally origin to the sweep peak; wait for a candle close **below the upper bulb's `VAL`** to confirm breakdown into the thin lower `LVN` tail.
     * **Rulebook `3.4` (`AVWAP` Kiss-of-Death Retest):** Anchor VWAP to the swing low that started the bounce; wait for an impulsive close below `AVWAP` and a failed retest rejection from underneath.
4. **Gate 4 — Spot Rotation & Hard Invalidation:**
   * **Trigger:** Rotate `Sleeve A` `BTC → USDT` on the reclaim close below the swept high or upper-bulb `VAL`.
   * **Hard Invalidation:** A clean `4H` close above the sweep wick peak (or if `Spot CVD` surges to new highs alongside `Perp CVD`).

---

#### II. Part 2 — Tactical Accumulation (`Loop A: USDT → BTC`) at Demand
*Operational Scenario: Bitcoin sweeps a major secular floor (`$57,800–$58,566` June 2026 range low, printing `$57,970–$58,081`) and `Sleeve A` USDT is staged on watchlist.*

1. **Gate 1 — HTF Location & `Pillar 1` Check:**
   * **Location (`PASS`):** Price tests a multi-month `Demand Cluster` (`$57,800–$58,566`, `-54%` off the `$126,198` Oct 2025 ATH).
   * **Macro Permission (`WAIT FOR UNLOCK`):** While `GATE_RED` is active, `MOD 42.1` enforces `0.00%` `USDT → BTC` deployment. Arm the watchlist now, and execute **only** once `Pillar 1` upgrades to `GATE_AMBER` (`0.375%` max risk) or `GATE_GREEN` (`0.75%` max risk) via `ICDM < 55` and ETF outflow stabilization (`MOD 31 M2`).
2. **Gate 2 — Structural Pattern Match:**
   * **Pattern #1 (`Double Bottom Sweep`):** Price undercuts the June secular close (`$58,566`) to `$57,970` to flush sell stops, disqualifying **Pattern #3 (`No Sweep`)**, and prepares to reclaim `$58,566`.
   * **Pattern #10 (`Bullish Divergence: RSI 14 & AO`):** Pair the sweep with simultaneous higher lows on both `RSI (14)` and the `Awesome Oscillator (AO)` inside the demand zone. *(Note: If price bounces weakly below `$61.5k` and makes one final sweep into `$55,000–$56,500`, the setup upgrades to **Pattern #7 `Three Drives Long`**).*
3. **Gate 3 — Microstructure & Momentum Confirmation:**
   * Verify **volume + negative delta spike** on the `$57,970` sweep wick, followed by a `1D` reclaim close above `$58,566` (or `4H` reclaim above `$60,000`), back-to-back green closes (`MOD 65 CB-02`), simultaneous `RSI + AO` higher lows, and rising **Domestic USD Spot CVD** (`MOD 05`).
4. **Gate 4 — Deterministic Sizing Formula, `Net R >= 3.0`, & Two-Stage Exit (Worked Example):**
   * **Assumptions:** `Pillar 1` unlocks to **`GATE_AMBER` (`0.375%` risk)** on a `$100,000` portfolio (`$375` max dollar risk) after a confirmed reclaim:
     * **Entry Trigger (`USDT → BTC`):** `$59,200` (confirmed `4H` displacement reclaim above `$58,566` with positive USD Spot CVD).
     * **Hard Invalidation Stop:** `$57,450` (placed cleanly below the `$57,970` sweep wick extreme; risk = `$1,750` per BTC).
     * **Position Size (`1.0x` Unleveraged Spot):**
       $$\text{Spot Position} = \frac{\$375}{\$59,200 - \$57,450} = 0.2143\text{ BTC} \quad (\approx \$12,686\text{ spot allocation})$$
     * **Two-Stage Profit Scaling (`MOD 18` / `MOD 37`):**
       * **Stage 1 (`50%` exit at `$64,000` LTF `CHoCH` / flipped `POC`):** `+$4,800/BTC` = **`2.74R`**; move stop on remaining `50%` to breakeven (`$59,200`).
       * **Stage 2 (`50%` runner to `$68,000` `200W MA`):** `+$8,800/BTC` = **`5.03R`**.
       * **Blended Reward-to-Risk:** **`3.89R`** gross (`>= 3.0R` net after `MOD 37` slippage).

---

#### III. Quick-Reference Pattern Selector Matrix (`#1`–`#11`)

| Tape Behavior at HTF Level | Long Setup (`USDT → BTC`) | Short Setup (`BTC → USDT`) | Primary Confirmation Filter |
| :--- | :--- | :--- | :--- |
| **Stop-Hunt Wick Beyond Level** | **#1** Double Bottom (Sweep) | **#2** Double Top (Sweep) / **#9** Mouse Trap | Wick delta/volume spike + reclaim close + `OI`/`Spot CVD` flip |
| **Limit Wall Stops Price Early** | **#3** Double Bottom (No Sweep) | **#4** Double Top (No Sweep) | Footprint bid/ask absorption prints before swing extreme |
| **Curved Multi-Bar Bowl / Cap** | **#5** Rounded Retest (Long) | **#6** Rounded Retest (Short) | Drying volume through curve + internal `SFP` (`#6`) + `AVWAP` |
| **Three Exhaustion Pushes** | **#7** Three Drives (Long) | **#8** Three Drives (Short) | Simultaneous **#10 / #11** `RSI (14) + AO` divergence on Drive 3 |

---

##### FINAL DIRECTIVE
**MOD 42.1.1 operationalizes MOD 42.1 inside DIBSE v2.0: never execute a chart shape on sight—enforce Gate 1 Location & Pillar 1 Permission, Gate 2 Pattern Classification, Gate 3 Order-Flow/Momentum Confirmation, and Gate 4 `Net R >= 3.0` Spot Sizing.**
