### PROJECT CORTEX-BTC — MODULE 66: MULTI-LAYER TIMEFRAME SYNTHESIS & 4-STEP ENTRY ARCHITECTURE
**Waterfall Tier:** Tier D Master Execution Synthesis & Cross-Timeframe Alignment Engine (Organizing Market Structure, On-Chain Valuation/Behavior, Derivatives/ETF Fuel & Volume Profile Triggers into a Disciplined 4-Step Spot Entry Workflow) — harmonized with 00 Charter (5-Pillar Waterfall), MOD 01–07 (Derivatives, Spot CVD & ETF Flows), MOD 11 (Volume Profile Topology), MOD 13–14 (STH Realized Price, MVRV & SOPR), MOD 16/31/64 (Pillar 1 Macro/Credit Gate), MOD 18/18.1 (0.75% Spot Risk Sizing & Pre-Flight Checklist), MOD 35 (Liquidity Sweeps), MOD 54 (MTF Kline Lock), MOD 60 (7-Rank Veto Precedence Ladder), and MOD 62 (DIBSE v2.0).
**Document Provenance:** Codified from `Decoding Multi-Layer Bitcoin Analysis.md` (*Decoding Multi-Layer Bitcoin Analysis: How to Read Market Metrics and Time Better Entries*).
**Governance Posture:** Master Operational Synthesis & Timeframe-Discipline Blueprint. Prevents timeframe mismatch (using macro on-chain oscillators to time 4H entries or trading mid-POC noise) by enforcing a strict 4-Layer Hierarchy and 4-Step Entry Sequence subordinate to Pillar 1 / MOD 60 upstream vetoes.

---

#### 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)
```yaml
module_id: "MOD_66"
entry_type: "MULTI_LAYER_SYNTHESIS_AND_ENTRY_WORKFLOW"
waterfall_pillar: "TIER_D_4_LAYER_SYNTHESIS_AND_EXECUTION_WORKFLOW"
title: "Multi-Layer Timeframe Synthesis & 4-Step Entry Architecture"

# MOD 60 PRECEDENCE & WATERFALL REGISTRATION
governance_registration:
  mod_60_precedence_rank: "EXECUTION_SYNTHESIS_BRIDGE_TO_MOD_18_AND_MOD_62"
  pillar_1_upstream_override: "Pillar 1 Macro/Liquidity/Credit Gates (MOD 16, MOD 22, MOD 31 ICDM >= 60, MOD 44, MOD 64) govern top-level capital permission; if GATE_RED is active, cap tactical risk at 0.00%."
  spot_only_constraint: true # Strict 1.0x unleveraged BTC/USDT spot execution (max 0.75% portfolio risk per trade)

# THE 4 ANALYTICAL LAYERS (TIMEFRAME & FUNCTION SEPARATION)
analytical_layers:
  layer_1_map:
    domain: "Market Structure & Liquidity (1W / 1D / 4H)"
    role: "Directional bias, 50W/200W MA institutional dividers, BOS/CHoCH transitions & post-sweep invalidation points"
    governing_modules: ["MOD_17", "MOD_35", "MOD_42", "MOD_54"]
  layer_2_compass:
    domain: "On-Chain Valuation & Realized Behavior (Multi-Week / Cycle)"
    role: "Macro asymmetry via Realized Price, STH Cost Basis (<155d), MVRV Z-Score (0-1 value band), NUPL, SOPR/STH-SOPR 1.0 polarity & multi-week exchange flows"
    governing_modules: ["MOD_13", "MOD_14", "MOD_15", "MOD_39", "MOD_59"]
  layer_3_fuel:
    domain: "Derivatives Crowding & Institutional Spot Flows (4H / 1D)"
    role: "Trap detection & conviction via BTC-denominated OI, Perpetual Funding, Options Strike GEX/Max Pain & US Spot ETF net flows"
    governing_modules: ["MOD_01", "MOD_02", "MOD_03", "MOD_04", "MOD_07", "MOD_25", "MOD_26", "MOD_38"]
  layer_4_trigger:
    domain: "Volume Profile & Spot Order Flow (15m / 1H / 4H)"
    role: "Precision entries & stops via POC, VAH/VAL (70% value area), HVN vs. LVN air pockets, Rejection vs. Acceptance & Domestic USD Spot CVD"
    governing_modules: ["MOD_05", "MOD_06", "MOD_11", "MOD_19"]

# 4-STEP ENTRY WORKFLOW GATES
entry_workflow_sequence:
  step_1: "ESTABLISH_BIAS (Pillar 1 Macro Gate + 1W/1D Structure + Sustained Spot ETF Flows)"
  step_2: "CHECK_THE_FUEL (Derivatives Crowding Matrix + On-Chain Asymmetry & 1.0 SOPR Polarity)"
  step_3: "MAP_EXECUTION_ZONES (Structural S/R + Liquidation Shelves + VAH/VAL Edges; Ban Mid-POC Entries)"
  step_4: "TRIGGER_AND_INVALIDATION (1H/4H Sweep + CHoCH or Value-Area Rejection/Acceptance + USD Spot CVD + Hard Stop)"

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  conflict_standdown_risk_pct: 0.00 # When layers conflict, reduce size or enforce 100% Cash Lock
  min_reward_to_risk: 3.0 # Net R >= 3.0 after MOD 37 slippage
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

#### 2. The 4-Layer Analytical Matrix & Layer 3 Derivatives Trap Table
##### A. CoreTex 4-Layer Architecture Mapping
| Analytical Layer | Metaphor & Primary Horizon | Core Metrics & Structural Tools | What It Governs (Authority) | What It Cannot Do (Anti-Trap Limit) |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1: Market Structure & Liquidity** | **The Map** (`1W` / `1D` / `4H`) | HH/HL vs. LH/LL sequences, `50W` & `200W` MAs, `BOS` (continuation) vs. `CHoCH` (early shift), post-sweep reactions | **Directional bias** & **hard invalidation points** (`MOD 17`, `MOD 35`, `MOD 54`). | Does not quantify leverage crowding or pinpoint intraday stop placement alone. |
| **Layer 2: On-Chain Metrics** | **The Cycle Compass** (Multi-Week / Cycle) | Realized Price, STH Cost Basis (`< 155d`), MVRV Z-Score (`0–1` value zone), NUPL, `SOPR` / `STH-SOPR` (`1.0` pivot), multi-week exchange flows | **Macro valuation asymmetry** & **cohort stress** (`MOD 13`, `MOD 14`, `MOD 39`, `MOD 59`). | **Never a timing trigger**—markets can stay undervalued on-chain for months while drifting lower. |
| **Layer 3: Derivatives & Institutional Flows** | **The Fuel** (`4H` / `1D`) | BTC-denominated Open Interest (`OI`), Funding Rates, Options strike concentrations, US Spot ETF multi-day flows | **Trap detection & conviction filter** (`MOD 01–04`, `MOD 07`, `MOD 25–26`, `MOD 38`). | Cannot replace structural support/resistance; sustained ETF outflows suppress bounces post-flush. |
| **Layer 4: Volume Profile & Order Flow** | **The Precision Trigger** (`15m` / `1H` / `4H`) | Point of Control (`POC`), Value Area (`VAH`/`VAL`, 70% vol), `HVN` vs. `LVN` air pockets, Rejection vs. Acceptance + **USD Spot CVD** | **Exact entry execution & stop placement** (`MOD 05`, `MOD 06`, `MOD 11`, `MOD 19`). | Must never be traded against HTF structure (`Layer 1`) or `Pillar 1` `GATE_RED` vetoes. |

##### B. Layer 3 Derivatives Crowding & Positioning Lookup Matrix
| Market Condition | Price Action | BTC-Denominated OI | Perpetual Funding Rate | CoreTex Interpretation & Action (`MOD 01–04`) |
| :--- | :--- | :--- | :--- | :--- |
| **Healthy Trend** | Rising | Rising | Mildly positive | Fresh capital entering with trend; valid if backed by positive USD Spot CVD (`MOD 05`). |
| **Crowded Trap** | Flat or stalling | Spiking sharply | Heavily positive | Leveraged longs piling in without price progress; high flush risk (`MOD 02` — block breakout buys). |
| **Weak Rally (Short Covering)** | Rising | Falling | Negative or neutral | Driven by short closures rather than fresh spot demand; prone to fading (`MOD 04` — require Spot CVD). |
| **Deleveraged / Reset** | Dropping or basing | Falling sharply | Near zero or negative | Excess leverage flushed (`MOD 03`); cascade risk drops, but wait for Spot ETF/CVD stabilization before entry. |

---

#### 3. Protective Circuit Breakers (Timeframe & Layer Hygiene Rules)
* **Circuit Breaker 1 — Timeframe-Metric Alignment Lock (CB-01):** Never use Layer 2 macro on-chain oscillators (`MVRV Z-Score`, `NUPL`, `Realized Price`) to time a 4H intraday trade, and never use a 15m Volume Profile poke to override a bearish Weekly/Daily (`Layer 1`) trend or `Pillar 1` `GATE_RED` macro regime (`MOD 16` / `MOD 31` / `MOD 64`).
* **Circuit Breaker 2 — Diminishing MVRV Ceiling & Value-Only Filter (CB-02):** Because MVRV Z-Score peak thresholds have compressed across successive cycles (`MOD 56`), use `MVRV Z-Score <= 0.0–1.0` strictly to identify macro undervaluation and build a watchlist—**never** as an autonomous buy trigger until `Layer 1` structure (`CHoCH -> HL -> HH`) and `Layer 4` order flow confirm (`MOD 13`).
* **Circuit Breaker 3 — The SOPR 1.0 Polarity Law (CB-03):** Treat `STH-SOPR = 1.0` as dynamic support in confirmed bull markets (holders refuse to sell at a loss), but as **overhead breakeven resistance** in bear markets (trapped `< 155d` buyers dump at breakeven on relief rallies) until `STH-SOPR` reclaims and holds `> 1.0` (`MOD 14`).
* **Circuit Breaker 4 — Mid-POC Auction Chop Ban (CB-04):** Never enter breakout or momentum trades in the middle of a `Point of Control (POC)` / `High-Volume Node (HVN)` range (`MOD 11 CSU-11D`). Set alerts strictly at `VAH` / `VAL` edges overlapping structural levels, and trade only verified **Rejection (Mean Reversion)** or **Acceptance (Breakout Continuation)** backed by Domestic USD Spot CVD (`MOD 05`).
* **Circuit Breaker 5 — Cross-Layer Conflict Stand-Down Rule (CB-05):** Whenever Layer 2 deep-value on-chain readings clash with bearish Layer 1 structure and sustained Layer 3 Spot ETF outflows, **do not force a trade**—enforce `0.00%` tactical risk (`100% USDT Cash Lock` on Sleeve A) until cross-layer confluence aligns (`MOD 18` / `MOD 60`).

---

#### 4. Core Conditional Signal Units (Condition A -> Outcome B -> Rule C)
##### CSU-66A: 4-Layer Bullish Confluence ("Full-Waterfall Spot Long")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Step 1 (Bias):** `Pillar 1` permits risk (`ICDM < 55`, non-`GATE_RED`), `1D/1W` structure holds HH/HL (or confirmed two-step `CHoCH -> HL`), and multi-day US Spot ETF flows are neutral-to-positive (`MOD 07`).
  2. **Step 2 (Fuel):** Derivatives are non-crowded (`OI` reset or healthy trend, funding neutral/mild) and on-chain `STH-SOPR` holds/reclaims `>= 1.0` (`MOD 14`).
  3. **Step 3 (Zone):** Price tests a high-confluence `VAL` or broken resistance turned support overlapping a swept liquidity shelf (`MOD 11` / `MOD 35`).
  4. **Step 4 (Trigger):** `1H/4H` prints a liquidity sweep + `CHoCH` or `VAL` rejection close back inside value with rising **Domestic USD Spot CVD** (`MOD 05`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Multi-Layer Lens:** Macro permission, structural trend, clean leverage positioning, and institutional spot absorption align simultaneously.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **EXECUTE UNLEVERAGED SPOT LONG (`0.75%` Max Portfolio Risk, `Net R >= 3.0`)** via `MOD 18` / `MOD 62` Loop A (`USDT -> BTC`), placing hard stop strictly beyond the post-sweep invalidation wick and scaling 50% at `POC`/Stage 1 and 50% at `VAH`/Stage 2.

##### CSU-66B: Value-Area Acceptance Continuation ("LVN Air-Pocket Breakout")
* **Trigger Condition A (The Telemetry Scan):**
  1. `Layer 1` HTF bias and `Layer 3` Spot ETF flows align with breakout direction.
  2. Price closes beyond `VAH` (or `VAL` in bearish Loop B rotation), holds outside across consecutive `1H/4H` candles (`Acceptance`), builds new volume outside the prior value area, and enters a `Low-Volume Node (LVN)` air pocket backed by positive USD Spot CVD (`MOD 11 CSU-11B`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Auction Lens:** Market has rejected the old fair-value range and travels rapidly through the `LVN` toward the next `HVN`.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENTER ON ACCEPTED RETEST OF BROKEN `VAH` EDGE (`0.375%–0.75%` Risk)** with hard stop tucked strictly inside the broken edge / nearest `LVN` boundary.

##### CSU-66C: Cross-Layer Divergence ("Value-vs.-Flow Stand-Down")
* **Trigger Condition A (The Telemetry Scan):**
  1. `Layer 2` on-chain metrics enter deep-value territory (`MVRV Z-Score` in `0–1` band, compressed `NUPL`), **but** `Layer 1` (`1D/1W` LH/LL below 200D/200W MAs) and `Layer 3` (sustained multi-day Spot ETF outflows) remain bearish.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Structural Lens:** Valuation asymmetry is building for long-term watchlists, but active institutional redemptions and downward structure keep near-term path of least resistance lower.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **HOLD 100% USDT CASH LOCK ON SLEEVE A (`0.00%` Risk).** Log level on `00H` watchlist; prohibit anticipatory dip-buying until `Step 1` and `Step 4` triggers confirm.

---

#### 5. Dynamic Regime Mutation Lookup Matrix (M1 through M6)
| Mutation ID | Initial State | Telemetry Mutation Observed (Condition A') | Mechanical Meaning (Outcome B') | Mandatory Execution Override (Rule C') |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Mid-POC Chop Trap** | Any Active Scan | Price hovers near the center of a multi-day `POC` with flat funding and no `VAH`/`VAL` edge sweep. | Two-sided fair-value equilibrium; high chop probability (`CB-04`). | **Stand Aside (`0.00%` Risk);** set alerts at `VAH`/`VAL` edges only. |
| **M2: Short-Covering Mirage** | Rally Toward Resistance | Price rises +3%–5% into broken support, **but BTC-denominated OI drops sharply, funding stays negative, and USD Spot CVD is flat/falling**. | `Layer 3` Weak Rally (short covering without spot demand). | **Block Breakout Longs;** treat broken support as continuation resistance (`Layer 1`). |
| **M3: Crowded Breakout Trap** | Approaching `VAH` | Price pokes above `VAH`, **but OI spikes aggressively and perp funding surges heavily positive without Spot CVD follow-through**. | `Layer 3` Crowded Trap; late leveraged longs vulnerable to flush (`MOD 02`). | **Cancel Breakout Bid;** wait for post-flush `VAL` spring (`CSU-11A`). |
| **M4: SOPR 1.0 Breakeven Rejection** | `CSU-66C` (Bear Watch) | Price rallies into `STH Realized Price`, pushing `STH-SOPR` up to `0.995–1.005`, **where delta turns negative and price rejects**. | Underwater `< 155d` cohort exiting at breakeven (`CB-03` / `MOD 14`). | **Enforce Cash Lock;** require decisive `STH-SOPR > 1.015` hold before trusting bounce. |
| **M5: Acceptance Failure -> Mean Reversion** | `CSU-66B` (Breakout) | Price breaks `VAH`, fails to build volume above it, and closes a `1H/4H` bar back inside the Value Area. | Breakout mutated into a `VAH` Rejection (Mean Reversion toward `POC`/`VAL`). | **Exit Immediately at Hard Stop;** do not hold hoping for a second push. |
| **M6: Full 4-Step Alignment** | `CSU-66C` (Watchlist) | Spot ETF outflows flip to multi-day inflows (`Step 1`), OI/funding normalize (`Step 2`), `VAL` sweep holds (`Step 3`), and `1H/4H` prints `CHoCH` on USD Spot CVD (`Step 4`). | All 4 analytical layers + `Pillar 1` gates aligned. | **Graduate to `CSU-66A` (`0.75%` Spot Entry)** via `MOD 18` / `MOD 62`. |

---

#### 6. Operational 4-Step Entry Execution Checklist (Pre-Order Gate)
1. **Step 1 — Establish Bias (`Pillar 1` + `Layer 1` + `Layer 3 ETFs`):** Is `Pillar 1` non-`GATE_RED`, and do `1W/1D` structure + multi-day Spot ETF flows agree on direction? *(If conflicting or `GATE_RED` -> `0.00%` Cash Lock).*
2. **Step 2 — Check the Fuel (`Layer 3 Derivatives` + `Layer 2 On-Chain`):** Is my intended direction free of `OI`/funding crowding, and is `STH-SOPR` (`1.0` pivot) / `MVRV` supporting the move?
3. **Step 3 — Map the Execution Zones (`Layer 1 Liquidity` + `Layer 4 Volume Profile`):** Does the setup sit at a `VAH`/`VAL` edge or swept liquidity pool rather than the middle of a `POC`?
4. **Step 4 — Wait for Trigger & Hard Invalidation (`1H/4H` + `USD Spot CVD`):** Did a `1H/4H` candle close confirm `CHoCH` or Value-Area Rejection/Acceptance with Domestic USD Spot CVD, and does the hard stop preserve `Net R >= 3.0` at `<= 0.75%` spot risk?

---

##### FINAL DIRECTIVE
**MOD 66 eliminates timeframe confusion by giving every metric one job: Structure draws the map, On-Chain reads the cycle compass, Derivatives and ETFs measure the fuel, and Volume Profile with Spot CVD pulls the trigger—only when all four layers agree.**
