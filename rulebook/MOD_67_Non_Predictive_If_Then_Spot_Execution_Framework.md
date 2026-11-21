### PROJECT CORTEX-BTC — MODULE 67: NON-PREDICTIVE IF-THEN SPOT EXECUTION FRAMEWORK
**Waterfall Tier:** Tier D Behavioral Governance & Pillar 4 Spot Execution Rulebook (Replacing Directional Forecasting with Binary Candle-Close If-Then Decision Matrices & Cash-Firewall Discipline) — harmonized with **00 Charter**, **MOD 18 / 18.1 / 18.2** (`0.75%` Risk Sizing, Pre-Flight Go/No-Go & Reading a Falling Market Without a Forecast), **MOD 31** (`ICDM` Fragility Gate), **MOD 42.1 / 42.1.1** (Symmetrical 11-Pattern Playbook), **MOD 54** (MTF Candle-Close Lookback Contract), **MOD 60** (Veto Precedence Ladder), **MOD 62** (`DIBSE v2.0`), **MOD 65** (Media Hygiene), and **MOD 66** (4-Layer Timeframe Synthesis).
**Module Type:** Educational / Behavioral Governance Rulebook Entry (NotebookLM Reference Library)
**Desk Scope:** Unleveraged Spot-Only BTC/USDT Swing Trading (`1.0x` Spot Only — Zero Margin, Zero Futures/Perpetuals)
**Reference Context:** Mid-November 2026 sub-`$60,000` test (`$57,970–$58,566` June 2026 secular range low) with `50%` deployed across **Tranche 1 (`$72,850`)** and **Tranche 2 (`$70,450`)** (`~$71,650` blended basis) and **`50%` defensive cash** firewall.

---

#### 0. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)
```yaml
module_id: "MOD_67"
entry_type: "BEHAVIORAL_GOVERNANCE_AND_IF_THEN_EXECUTION_RULEBOOK"
waterfall_pillar: "TIER_D_AND_PILLAR_4_NON_PREDICTIVE_SPOT_EXECUTION"
title: "Non-Predictive If-Then Spot Execution Framework"

governance_registration:
  mod_60_precedence_rank: "BEHAVIORAL_EXECUTION_GUARDRAIL_FOR_PILLAR_4"
  spot_only_constraint: true # Strict 1.0x unleveraged BTC/USDT spot only (zero margin/perps)
  reference_anchor:
    regime: "Mid-November 2026 sub-$60,000 secular support test"
    deployed_tranche_1_usd: 72850
    deployed_tranche_2_usd: 70450
    blended_cost_basis_usd: 71650
    cash_firewall_split: "50% deployed / 50% defensive cash (or 100% Sleeve A USDT cash lock under GATE_RED)"

execution_invariants:
  default_bounce_presumption: "GUILTY_UNTIL_PROVEN_INNOCENT"
  candle_close_authority: "Completed 1D / 1W candle closes govern structural state; open intraday candles are non-actionable noise."
  four_pillars:
    pillar_1: "Weigh Probabilities, Not Certainties"
    pillar_2: "Separate Intraday Noise from Candle-Close Truth"
    pillar_3: "Pre-Write a Binary If-Then Decision Matrix"
    pillar_4: "Protect the Cash Firewall"
```

---

#### 1. Core Thesis: Stop Predicting, Start Reacting
Most discretionary traders lose capital not from a lack of charts or market data, but by asking *"Where is price going next?"* Forecasting direction in high-volatility regimes forces traders into guesswork when valid arguments exist on both sides simultaneously.

An institutional desk replaces prediction with a mechanical **"If-Then" Execution Framework**:
* **Guilty Until Proven Innocent:** Treat every unconfirmed bounce during a breakdown as *guilty until proven innocent*.
* **Candle-Close & Flow Authority:** Let completed candle closes (`MOD 54`) and verified spot flow/demand shifts (`MOD 05` / `MOD 07`) govern action—never intraday emotion, open-candle wicks, or hope.

---

#### 2. The Two-Sided Trap (Why Forecasting Fails Around Key Floors)
At major psychological and structural boundaries (such as **`$60,000`**), opposing forces collide at the exact same time, making directional forecasting statistically futile:
* **Downside Pressure Vectors:** Breakdowns below prior support, net US Spot ETF outflows (`MOD 07`), macro/rate headwinds (`MOD 16` / `MOD 64`), and contracted stablecoin demand (`MOD 48`) open structural air pockets toward lower support shelves (such as the June 2026 low reference near **`$58,566`** and lower macro zones in the **`$51,000–$58,000`** band).
* **Upside Snap-Back Vectors:** Deeply oversold momentum readings (such as daily `RSI < 30`), Extreme Fear sentiment (`Fear & Greed ~10–11`), and trapped short/liquidity pockets (`MOD 01` / `MOD 35`) can trigger sharp, sudden short-covering rallies.

---

#### 3. Four Pillars of Non-Predictive Execution & Binary "If-Then" Matrix

1. **Pillar 1 — Weigh Probabilities, Not Certainties:** Treat intraday green candles as relief/reclaim tests when downward pressure dominates (`MOD 18.2`).
2. **Pillar 2 — Separate Intraday Noise from Candle-Close Truth:** Anchor major portfolio decisions to confirmed **daily (`1D`) or weekly (`1W`) candle closes** around a clear line in the sand (e.g., **`$60,000`** or **`$58,566`**).
3. **Pillar 3 — Pre-Write a Binary "If-Then" Decision Matrix:** Commit to exact conditional branches *before* the candle closes so no judgment is made under live volatility stress.
4. **Pillar 4 — Protect the Cash Firewall:** Maintain a split allocation (**`50%` deployed / `50%` defensive cash** in the reference allocation, or `100%` `Sleeve A` USDT cash lock under `Pillar 1 GATE_RED`) to cap portfolio drawdown and preserve dry powder for verified lower bases.

##### Binary "If-Then" Execution Matrix (Line-in-the-Sand Protocol)
| Candle-Close Condition (`IF`) | Structural Interpretation | Mandatory Spot Action (`THEN`) | Cash Firewall Posture |
| :--- | :--- | :--- | :--- |
| **Confirmed `1D` / `1W` Close ABOVE Threshold** *(with supporting spot demand)* | Breakdown rejected; support reclaimed and defended by real spot buyers (`MOD 05` / `MOD 42.1`). | **Hold / Stay Aligned** with existing spot position; authorize next staged tranche only if `Pillar 1` (`MOD 31`) permits. | **Intact** — Keep defensive cash reserve protected; never go all-in on a single bounce. |
| **Confirmed `1D` / `1W` Close BELOW Threshold** | Support breached; sellers maintain control and lower air pockets (`$58,566` → `$51,000–$58,000`) remain open. | **Step Aside to Cash** (`BTC → USDT` rotation per `DIBSE Loop B`) to cap loss and wait for a verified lower base (`MOD 42.1` Gate 3/4). | **Expanded** — Preserve dry powder for confirmed bottoming structure (`MOD 33 REGIME_5`). |

---

#### 4. Protective Circuit Breakers (Behavioral Anti-Guesswork Guardrails)
* **Circuit Breaker 1 — Open-Candle Freeze (`CB-01`):** Never execute a structural trim or accumulation tranche based on an unclosed intraday candle poking above or below the line in the sand (`MOD 54`).
* **Circuit Breaker 2 — No Averaging Down in Freefall (`CB-02`):** When existing tranches sit underwater (e.g., `~$71,650` blended basis across `$72,850` and `$70,450` while spot tests sub-`$60,000`), never deploy the `50%` defensive cash reserve solely because price looks "cheap" or `RSI < 30` (`MOD 18.1` Anti-Knife Protocol).
* **Circuit Breaker 3 — Spot-Only Invariant (`CB-03`):** All execution under `MOD 67` is strictly `1.0x` unleveraged `BTC/USDT` spot—never use margin, perpetuals, or futures to "make back" unrealized spot drawdown.

---

#### 5. 60-Second Anti-Guesswork Pre-Action Checklist
Before clicking Buy (`USDT → BTC`) or Sell (`BTC → USDT`), verify all four questions in under 60 seconds:
1. **Reacting or Guessing?** Is this action triggered by a *completed candle close* and pre-written rule, or by open-candle emotion?
2. **Line in the Sand Defined?** Is the exact invalidation level clear *before* capital is risked?
3. **Reclaim Proven?** Has price closed back above broken resistance with supporting spot demand (`MOD 05` USD Spot CVD / `MOD 07` ETF stabilization)?
4. **Worst-Case Contained?** Is total portfolio drawdown bounded by position sizing (`<= 0.75%` risk per trade) and defensive cash reserves?

---

##### FINAL DIRECTIVE
**MOD 67 eliminates emotional forecasting: treat every unconfirmed bounce as guilty until proven innocent, anchor all portfolio shifts to completed daily/weekly candle closes around a pre-defined line in the sand, and guard the cash firewall at 1.0x unleveraged spot.**
