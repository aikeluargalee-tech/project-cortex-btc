# PROJECT CORTEX-BTC — MODULE 35: LIQUIDATION HEATMAP DISTANCE RULE & PULL SCORE ENGINE
**Waterfall Tier:** Pillar 2 & Pillar 3 Quantitative Liquidity-Target & Permission Engine (Ranking Competing Upper vs. Lower Liquidation Magnets).
**Provenance & Empirical Benchmark Anchor:** Synthesized from `The Distance Rule` (`CS4`) and `The Liquidity-Hunt Myth` (`CS1` — Nov 13, 2026 BTC worked case study), establishing exact percentage-distance normalization, the **Pull Score** ranking formula, ATR movement feasibility, and the **Permission-Before-Target** law.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_35"
entry_type: "LIQUIDITY_MAGNET_PULL_SCORER"
waterfall_pillar: "PILLAR_2_3_HEATMAP_PULL_SCORE_ENGINE"
title: "Liquidation Heatmap Distance Rule & Pull Score Engine"

# CORE MATHEMATICAL FORMULAS
distance_pct_formula: "Distance_Pct = ((Magnet_Price - Current_Price) / Current_Price) * 100.0"
pull_score_formula: "Pull_Score = Cluster_Size_USD_M / abs(Distance_Pct)"
atr_distance_formula: "ATR_Multiples = abs(Magnet_Price - Current_Price) / Daily_ATR_14"

# THE 5 DISTANCE RULES & SKEW THRESHOLDS
distance_skew_thresholds:
  LOPSIDED_PULL_DOMINANCE: "Nearest_Pull_Score > 1.5 * Opposing_Pull_Score -> Expect visit to cheaper/nearer magnet first"
  BALANCED_CHOP_ZONE: "Upper_Distance_Pct ~= Lower_Distance_Pct (both 2%-3% away, ratio < 1.5x) -> Expect ping-pong chop (Standby)"
  FAR_MAGNET_CATALYST_GATE: "Distance_Pct >= 6.0% OR ATR_Multiples >= 2.0 -> Requires exogenous catalyst + Permission Gate"

# PERMISSION-BEFORE-TARGET GATE (FALSIFYING THE LIQUIDITY-HUNT MYTH)
permission_gate_requirements:
  - "Heatmap intensity is unitless model output (CoinGlass Docs), NEVER resting limit orders or a timetable"
  - "Upside short-liquidation magnet requires Squeeze Fuel (negative funding + OI stacked at lows) OR Spot CVD + Coinbase Premium >= 0"
  - "Downside long-liquidation magnet dominates whenever trend is down, funding >= 0, and OI rises into drops (Cascade Fuel)"

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Heatmap Anti-Myth Governance)

* **Circuit Breaker 1 — The Heatmap Category-Error Filter (`CB-01`):** Liquidation heatmaps (e.g., CoinGlass Models 1/2/3) display *model-estimated* liquidation concentrations, **not** resting order-book limit orders and **not** a schedule. Never treat bright overhead yellow bands as guaranteed upside magnets when spot flow and structure point down (empirical proof: Nov 6–13, 2026, where a bright `~$76.0k–$76.5k` week-old band sat untouched while BTC fell `-7%` to `$70.5k`).
* **Circuit Breaker 2 — Energy Cost & Intervening Friction Filter (`CB-02`):** Every `1%` price move requires net order-flow fuel and must clear intermediate structural shelves. A distant `$200M` cluster `+13%` (`~2.5 ATR`) away is far weaker in the near term than a `$32.5M` cluster `0.5%` (`< 0.3 ATR`) away.
* **Circuit Breaker 3 — Permission Over Magnet (`CB-03`):** Direction is granted exclusively by **Structure + Spot/Perp CVD + Positioning (`Funding / OI`)**. Heatmaps only supply *conditional targets* once flow grants permission to travel in that direction.
* **Circuit Breaker 4 — Never Buy Before the Nearer Downside Flush (`CB-04`):** When lower Pull Score exceeds upper Pull Score by `> 1.5x` and longs are crowded (`funding >= 0`, `top-trader L/S > 1.8`), never front-run an upside hunt; wait for the cheaper downside cluster to flush first.

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-35A: Downside Pull Dominance ("Cheap Downside Trip / Cascade Fuel")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Pull Score Skew:** $\text{Pull Score}_{\text{Lower}} > 1.5 \times \text{Pull Score}_{\text{Upper}}$ (benchmark: Nov 13, 2026 at `$69,223`, where `$68,235` lower magnet had `Pull = 65.0` vs. `$73,635` upper magnet `Pull = 14.4` — a **`4.5x` downside pull advantage**).
  2. **Cascade Fuel Active:** Price in 1D/4H downtrend, `funding >= 0.00%`, `OI` rising or elevated into drops, and `USD Spot CVD` / `Coinbase Premium` negative.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Microstructure Lens:** Downside cluster is `0.3–1.0 ATR` away with zero intervening support, while upside magnets sit `2.0–2.6 ATR` away behind multiple resistance shelves.
  * **Probable Trajectory:** Market takes the "cheap trip" down to sweep nearby long liquidations first; minor `0.2 ATR` bounces (`+0.5%`) are noise, not reversals.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE `100% CASH LOCK` (`0.00%` Risk).** Block all anticipatory dip-buying until the lower cluster sweeps and `MOD 03 / MOD 34` exhaustion confirms.

### CSU-35B: Upside Pull Dominance with Squeeze Permission ("Coiled Short-Squeeze Path")
* **Trigger Condition A (The Telemetry Scan):**
  1. **Pull Score Skew:** $\text{Pull Score}_{\text{Upper}} > 1.5 \times \text{Pull Score}_{\text{Lower}}$ (nearest short-liquidation cluster within `0.5%–2.0%` / `< 0.8 ATR` overhead with clean LVN path).
  2. **Permission Granted (`Squeeze Fuel`):** `Funding <= -0.015%` with `OI` holding/rising at lows (crowded shorts paying), **OR** price reclaims broken 4H support/VAH with rising `USD Spot CVD` and `Coinbase Premium >= 0.00%`.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Microstructure Lens:** Short distance + crowded paying shorts creates self-reinforcing forced buy-to-cover acceleration once the nearest cluster triggers.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **AUTHORIZE `0.375%–0.75% Risk` SPOT LONG** upon confirmed 1H/4H boundary reclaim (`R >= 3.0`), using the upper magnet chain (`T1` nearest cluster, `T2` secondary cluster) for `Stage 1 (50%)` profit harvesting.

### CSU-35C: Balanced Magnet Symmetry ("Ping-Pong Equilibrium Chop")
* **Trigger Condition A (The Telemetry Scan):**
  1. Nearest upper and lower magnets sit at roughly equal distances (`2.0%–3.0%` each way) with $\frac{\max(\text{Pull}_{\text{Upper}}, \text{Pull}_{\text{Lower}})}{\min(\text{Pull}_{\text{Upper}}, \text{Pull}_{\text{Lower}})} < 1.5$.
  2. Neutral funding, flat OI, and Garman-Klass volatility compressed (`MOD 12`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Microstructure Lens:** Neither side offers an asymmetric energy advantage; price oscillates between boundaries while heatmap clusters decay and redraw.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **STANDBY IN CASH (`0.00%` Mid-Range Exposure).** Trade only verified extreme Value Area sweeps (`MOD 11A / 11C`).

### CSU-35D: Far-Magnet Catalyst Ignition ("Multi-ATR Expansion Run")
* **Trigger Condition A (The Telemetry Scan):**
  1. Major dense liquidity band sits `>= 6.0%` (`>= 2.0 ATR`) away behind intermediate resistance shelves, **AND** an exogenous macro/ETF catalyst (cool CPI/PPI, Fed liquidity pivot, `> +$250M` ETF inflow surge) triggers a high-volume 4H close above the nearest intervening shelf (`MOD 11B`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Microstructure Lens:** Exogenous catalyst supplies the multi-ATR energy required to clear intermediate resistance levels and reach the distant cluster.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **HOLD STAGE 2 (`50%`) TRAILING RUNNER** toward the distant magnet once `Stage 1 (50%)` is banked at the first cleared shelf.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: Near Magnet Swept $\rightarrow$ Next Tier** | `CSU-35A` (Lower Sweep) | Price sweeps the first lower magnet (`e.g., $68,235`), **OI keeps rising, and 1H closes below the wick** with no Spot CVD turn. | First sweep failed to exhaust sellers; next lower magnet (`$66,744`, `Pull = 52.0`) is now the active target. | **Keep `100% Cash Lock`**; do not enter until the secondary cluster flushes and reclaims. |
| **M2: Downside Sweep $\rightarrow$ Permission Flip** | `CSU-35A` (Lower Sweep) | Lower magnet sweeps on volume climax, **funding flips negative (`< -0.015%`), OI drops `-8%+`, and 4H reclaims broken support**. | Downside cascade fuel is cleared and flipped into upside squeeze fuel (`Permission Granted`). | **Transition to `CSU-35B`:** Execute `0.375%–0.75% Risk` Spot Long targeting upper magnet chain. |
| **M3: Noise Tag Rejection (`0.2 ATR` Trap)** | `CSU-35A` (Downtrend) | Price bounces `+0.6%` (`0.2 ATR`) to tag a tiny fresh 24h short cluster (`e.g., $71.0k`), then **rejects at 4H resistance with negative Spot CVD**. | Routine downtrend noise squeezing chase-shorts—not a structural reversal. | **Ignore the Bounce;** maintain `100% Cash Lock`. |
| **M4: Heatmap Cluster Decay / Pull** | Any Active Watch | A bright 24h/48h heatmap band fades before price arrives because leveraged traders manually closed or rolled positions. | The fuel pool evaporated; price no longer has forced-liquidation acceleration at that level. | **Remove Target from Active Playbook**; recalculate Pull Scores on remaining live clusters. |
| **M5: Intervening Shelf Rejection** | `CSU-35B` (Upside Run) | Price clears Magnet 1, rallies toward distant Magnet 2 (`+7%`), **but stalls at an intermediate HTF VAH / 200D MA with falling USD Spot CVD**. | Intermediate resistance absorbed the move before reaching the far magnet. | **Execute `Stage 2` Full Exit at the Intermediate Shelf** rather than waiting for the far cluster. |
| **M6: Crowd Flip Mid-Range** | `CSU-35C` (Chop) | While price chops mid-range, **funding plunges to `-0.025%` and OI jumps `+6%`** (aggressive short buildup at range lows). | Positioning skewed heavily short; upside Pull Score + Permission now align. | **Upgrade to `CSU-35B` Watch;** prepare `MOD 11A` VAL reclaim long trigger. |
| **M7: Multi-Model Heatmap Divergence** | Daily Mapping | CoinGlass Model 1 (`high leverage`) shows a nearby cluster, while Model 2/3 (`low leverage`) shows the true heavy shelf `3%` deeper. | High-leverage bucket is decoy fuel; true institutional liquidation wall sits at the Model 2/3 shelf. | **Anchor Invalidation Stop Beneath the Deeper Model 2/3 Shelf** (`minus 0.6%` buffer). |
| **M8: Morning Distance Worksheet Audit** | Daily `08:00 MYT` Scan | Compute `Distance %` and `Pull Score` for nearest 2 upper & 2 lower magnets alongside `MOD 31` ICDM score. | Prevents narrative bias ("inevitable pump") by quantifying exact ATR & percentage energy cost. | **Enforce Distance Rule 1:** Always plan around the higher Pull Score side unless a catalyst fires. |
