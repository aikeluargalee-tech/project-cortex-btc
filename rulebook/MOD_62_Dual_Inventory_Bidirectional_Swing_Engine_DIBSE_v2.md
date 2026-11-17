# PROJECT CORTEX-BTC — MODULE 62: DUAL-INVENTORY BIDIRECTIONAL SWING ENGINE (DIBSE v2.0)
**Waterfall Tier:** Pillar 4 & Operational Execution Engine (Portfolio Allocation Controller, Dual-Inventory Ledger Accounting & Order Lifecycle Management) — harmonized with `MOD 18` (Master 5-Pillar Compiler & 0.75% Risk Sizing), `MOD 32` (Sovereign Barbell Multi-Sig Custody), `MOD 33` (Unified 5-Regime Master Radar), `MOD 37` (Executable Liquidity & Net-3.0R Slippage Governor), `MOD 46` (Block 1,050,000 Secular Horizon), and `MOD 60` (7-Rank Veto Precedence Ladder).
**Document Provenance:** Integrated from `CORTEX-BTC-IBSR-001` (`DIBSE 1 — Dual-Inventory Bidirectional Swing Engine v2.0`).
**Governance Posture:** Operational Execution & Inventory Accounting Engine (`Rank 4/5` under `MOD 60`). Never overrides `MOD 60` Ranks 0–3 upstream vetoes (`MOD 36` Data Halt, `MOD 44/58` Event/Vacuum Locks, `MOD 16/31/33` Systemic Macro/ICDM Locks, or `MOD 03/34/51` Active Cascade Freezes).

---

## 0. CORTEX-BTC v9 HARMONIZATION & PRECEDENCE BRIDGE (MOD 18 / 33 / 37 / 60)

```yaml
module_id: "MOD_62"
entry_type: "OPERATIONAL_DUAL_INVENTORY_ENGINE"
waterfall_pillar: "PILLAR_4_PORTFOLIO_ALLOCATION_AND_EXECUTION"
title: "Dual-Inventory Bidirectional Swing Engine (DIBSE v2.0 — Integrated Rulebook)"

# MOD 60 VETO PRECEDENCE REGISTRATION (MANDATORY PER MOD 60 M5)
governance_registration:
  mod_60_precedence_rank: "RANK_4_EXECUTION_FEASIBILITY_AND_RANK_5_TACTICAL_ALLOCATION"
  upstream_veto_subordination: "Any MOD 60 Rank 0-3 veto (DATA HALT, GATE_RED, ICDM >= 60, MOD 44/58 Lock, or Active Cascade) immediately forces Portfolio Allocation Controller -> NO TRADE / REMAIN CURRENT INVENTORY."
  autonomous_execution: false # Strictly human operator authorization required

# CAPITAL BARBELL & SLEEVE BOUNDARIES (MOD 32 / MOD 46 ALIGNED)
capital_architecture:
  protected_sovereign_reserve_pct: 80.0 # Sleeve B: 2-of-3 Dual-Jurisdiction Multi-Sig Cold Storage (Untouchable)
  active_tactical_sleeve_pct: 20.0 # Sleeve A: Authorized DIBSE Tactical Operating Envelope
  initial_sleeve_split:
    tactical_btc_pct: 10.0 # Loop B BTC -> USDT -> BTC inventory
    tactical_usdt_pct: 10.0 # Loop A USDT -> BTC -> USDT inventory
  operator_approval_required_for_sleeve_change: true

# DETERMINISTIC REGIME MAPPING (DIBSE 4-REGIME -> MOD 33 5-REGIME & MOD 16 GATES)
regime_harmonization_map:
  CONSTRUCTIVE: "MOD 33 REGIME_1 (Spot-Led Expansion) or REGIME_2 (Short-Squeeze Coil) + MOD 16 GATE_GREEN -> Full 0.75% max portfolio risk ceiling."
  MIXED_CAUTIOUS: "MOD 33 REGIME_3 (High-Funding / Range Chop) or MOD 16 GATE_AMBER -> Reduced 0.375% max portfolio risk ceiling."
  DEFENSIVE: "MOD 33 REGIME_5 (Post-Flush Base) or Below 200D SMA -> Tighten Loop A accumulation; permit Loop B defensive BTC-to-USDT conversion on confirmed distribution."
  DISLOCATION_EXTREME_RISK: "MOD 33 REGIME_4 (Liquidity Drain / Negative Gamma) or ICDM >= 60 -> DATA HALT / 100% CASH LOCK (0.00% new risk; human review mandatory)."

# SIZING, ASYMMETRY & EXECUTION HARMONIZATION (MOD 18 & MOD 37)
execution_harmonization:
  loop_a_sizing_formula: "BTC_Qty = min(Available_Tactical_USDT / Entry_Price, (Max_Risk_Pct * Total_Portfolio_Equity) / (Entry_Price - Hard_Invalidation_Stop))"
  loop_b_conversion_triggers: "Authorized only upon confirmed Pillar 2/3/5 distribution signals (MOD 02B Crowded Basis, MOD 06B Ask-Wall Capping, MOD 13C STH-MVRV >= 1.30, MOD 27B Call-Skew Blow-Off, or MOD 41 Secular ATH Cluster)."
  minimum_asymmetry_filter: "Net R >= 3.0 post-slippage (MOD 37) required for all Loop A entries."
  order_execution_mode: "Limit orders default (Rule 29); marketable limit orders capped by MOD 37 slippage budget permitted when MOD 08A (A_P,V >= +1.5 Z) confirms an LVN fast-traverse breakout."
```

---

# CORTEX-BTC v2.0
## Integrated Bidirectional BTC/USDT Spot Rotation Rulebook

**Document ID:** CORTEX-BTC-IBSR-001
**Version:** 2.0 — Integrated Architecture (Harmonized into Master Rulebook v9 as `MOD_62`)
**Status:** RESEARCH / DECISION-SUPPORT FRAMEWORK — UNVALIDATED
**Strategy:** Bidirectional BTC/USDT Spot Rotation
**Operational Engine:** DIBSE — Dual-Inventory Bidirectional Swing Engine v2.0
**Trading Instruments:** BTC and USDT only
**Execution Preference:** Limit orders (with `MOD 37` slippage-capped marketable limit allowance on `MOD 08A/11B` LVN breakouts)
**Leverage / Margin / Borrowing:** Prohibited (`1.0x` Unleveraged Spot Only)
**Futures / Perpetual Trading:** Prohibited
**Short Selling:** Prohibited
**Autonomous Order Execution:** Prohibited

---

# PART I — SYSTEM IDENTITY AND GOVERNING AUTHORITY

## Rule 1. Core Objective

CORTEX-BTC is a spot-only BTC/USDT portfolio rotation framework.

Its objective is to manage the relative allocation between BTC and USDT through evidence-based accumulation, distribution and re-accumulation decisions.

The system must be capable of:

1. Accumulating BTC using existing USDT when downside conditions become favourable.
2. Holding BTC when market structure remains constructive.
3. Reducing BTC exposure into USDT when credible distribution or downside-risk conditions emerge.
4. Re-accumulating BTC when a subsequent opportunity satisfies the required conditions.
5. Remaining in either asset when evidence is insufficient.

The objective is not to predict every market movement.

The objective is to improve portfolio management through disciplined conversion decisions, risk control and measurable performance.

## Rule 2. Architecture and Authority

CORTEX-BTC is the governing framework (`MOD 01–61`).

DIBSE (`MOD 62`) is its operational trading engine.

The authority hierarchy is:

1. CORTEX-BTC — overall governance (`MOD 36` & `MOD 60` 7-Rank Veto Precedence).
2. Market Regime and Risk Controller — market conditions and risk restrictions (`MOD 16`, `MOD 31`, `MOD 33`).
3. Bullish Accumulation Module — BTC purchase opportunities (`MOD 01–15`, `MOD 19–27`, `MOD 30`, `MOD 42–43`, `MOD 54`, `MOD 59`).
4. Bearish Distribution Module — BTC-to-USDT conversion opportunities (`MOD 02B`, `MOD 06B`, `MOD 13C`, `MOD 15B`, `MOD 27B`, `MOD 41`).
5. Portfolio Allocation Controller — final exposure and trade eligibility (`MOD 18`, `MOD 37`, `MOD 62`).
6. DIBSE — inventory accounting, conversion-cycle tracking and order lifecycle management.
7. Human operator — final execution authorisation.

**Critical rule:** DIBSE must never override CORTEX-BTC governance.

Neither DIBSE trading loop may independently authorise a trade.

The Portfolio Allocation Controller is the single final decision authority.

## Rule 3. Non-Negotiable Trading Restrictions

The system shall never:

- Borrow BTC or USDT.
- Use margin or leverage.
- Open futures or perpetual positions.
- Create synthetic short exposure.
- Sell BTC that is not owned and available.
- Spend USDT that is not available.
- Trade the protected long-term BTC inventory (`Sleeve B`, `MOD 32/46`).
- Execute orders autonomously.

Selling owned BTC for USDT is a spot inventory conversion, not short selling.

---

# PART II — DIBSE OPERATIONAL INTEGRATION

## Rule 4. Dual-Inventory Architecture

DIBSE maintains two strategic inventories:

- BTC inventory.
- USDT inventory.

Both must be monitored independently.

The system must report:

- Available BTC.
- Reserved BTC in open sell orders.
- Available USDT.
- Reserved USDT in open buy orders.
- Protected long-term BTC (`Sleeve B`).
- Tactical BTC inventory (`Sleeve A`).
- Realised trading gains and losses.
- Unrealised portfolio valuation changes.
- Fees and execution costs.

No asset may be allocated to more than one outstanding order.

## Rule 5. Capital Boundary

Only explicitly authorised tactical trading capital may be used by DIBSE.

The DIBSE source rulebook proposes an initial 20% active sleeve (`Sleeve A`):

- 10% of total portfolio capital in USDT.
- 10% of total portfolio capital in BTC.
- Remaining 80% outside the active sleeve (`Sleeve B` Sovereign Multi-Sig Reserve).

This is a proposed allocation parameter, not a proven optimal allocation or an automatic instruction.

CORTEX must require explicit operator approval before activating or changing the sleeve.

The protected reserve must never be appropriated automatically.

## Rule 6. Inventory Floors

Minimum BTC and USDT inventory floors must be configured before deployment.

Every proposed conversion must be checked against:

- Available inventory.
- Reserved inventory.
- Protected holdings.
- Active sleeve boundaries.
- Maximum permitted exposure.
- Existing open orders.

Neither asset may be assumed to be a perfect substitute for the other.

## Rule 7. Two Independent Research Loops

DIBSE operates two opportunity-detection loops.

**Loop A — USDT → BTC → USDT**

Purpose: Increase realised USDT through favourable BTC accumulation and subsequent distribution.

**Loop B — BTC → USDT → BTC**

Purpose: Increase BTC quantity through favourable BTC distribution and subsequent re-accumulation.

Each loop maintains its own setup, conversion-cycle ledger and performance record.

They may monitor opportunities simultaneously.

However, both loops must submit proposed trades to the same Portfolio Allocation Controller.

The controller must reconcile:

- Aggregate BTC exposure.
- Aggregate USDT exposure.
- Available and reserved inventory.
- Conflicting orders.
- Market regime.
- Risk restrictions.
- Portfolio-level trade intent.

Two loops must never become two independent trading authorities.

---

# PART III — MARKET DATA AND EVIDENCE GOVERNANCE

## Rule 8. Evidence Hierarchy

CORTEX prioritises observable market behaviour over indicator-based assumptions.

The principal evidence categories are:

1. Spot CVD and actual spot-market participation (`MOD 05`, `MOD 07`, `MOD 19`).
2. Spot volume and trade delta (`MOD 06`, `MOD 08`).
3. Order-flow imbalance and order-book liquidity (`MOD 21`, `MOD 37`).
4. Footprint and auction behaviour (`MOD 11`).
5. Higher-timeframe market structure (`MOD 17`, `MOD 54`).
6. Open interest and funding as positioning context (`MOD 01–04`).
7. Confirmed liquidation events (`MOD 03`, `MOD 51`).
8. Futures CVD as contextual evidence (`MOD 05`, `MOD 09`).
9. Macro liquidity and broader market conditions (`MOD 16`, `MOD 22–24`, `MOD 29`, `MOD 44`, `MOD 58`).

No single indicator may independently authorise a trade.

## Rule 9. Data Classification

Every material data input must carry a status (aligned with `MOD 36` & `MOD 61`):

- VERIFIED
- PARTIALLY VERIFIED
- PROXY
- STALE
- UNAVAILABLE
- CONFLICTING

The system must distinguish directly observed exchange data from estimated, model-derived or aggregated values.

Source timestamps, collection timestamps and calculation timestamps must be recorded.

## Rule 10. Data Integrity Gate

Before a trade can become eligible, the system must verify:

- Source freshness (`MOD 36` SLA).
- Timestamp consistency.
- Instrument consistency.
- Correct market type.
- Calculation validity.
- Cross-source reconciliation where required (3-venue quorum per `MOD 36` / `MOD 54`).
- No material unresolved data conflicts.

If critical evidence is stale, unavailable or conflicting:

**Decision: DATA HALT / NO NEW TRADE.**

Existing inventory accounting must continue.

Working orders must be reassessed under the order-risk procedure.

---

# PART IV — MARKET REGIME CONTROLLER

## Rule 11. Regime Classification

CORTEX classifies the BTC environment into four operating regimes mapped directly to `MOD 33` (Unified 5-Regime Master Radar) and `MOD 16` (Macro Permission Gates):

**CONSTRUCTIVE** (`MOD 33 REGIME_1 / REGIME_2` + `GATE_GREEN`)

Higher-timeframe structure is supportive, with credible demand and no confirmed major deterioration.

**MIXED / CAUTIOUS** (`MOD 33 REGIME_3` + `GATE_AMBER`)

Evidence is conflicting, structure is unclear or market participation is inconsistent.

**DEFENSIVE** (`MOD 33 REGIME_5` or `< 200D SMA`)

Meaningful structural weakness, distribution or deterioration in market participation is present.

**DISLOCATION / EXTREME RISK** (`MOD 33 REGIME_4` or `ICDM >= 60` / `MOD 60 Rank 0–3 Veto`)

Severe downside displacement, disorderly liquidity, confirmed deleveraging or major market disruption is present.

## Rule 12. Regime Effects

The regime changes the permissions and requirements of both DIBSE loops.

- CONSTRUCTIVE: Accumulation is permitted when its independent conditions pass (up to `0.75%` portfolio risk cap). Distribution requires credible evidence of weakening.
- MIXED / CAUTIOUS: Reduce trade frequency and require stronger confirmation (`0.375%` portfolio risk cap).
- DEFENSIVE: Tighten accumulation requirements and permit defensive BTC-to-USDT conversion when distribution evidence is confirmed.
- DISLOCATION / EXTREME RISK: Suspend new risk-taking until data and market conditions stabilise (`0.00%` new risk / `100% Cash Lock`). Human review is required.

A regime classification alone does not authorise a trade.

---

# PART V — BULLISH ACCUMULATION MODULE

## Rule 13. Accumulation Objective

Identify opportunities to convert available USDT into BTC when downside selling pressure weakens and the market demonstrates credible recovery or acceptance.

## Rule 14. Required Evidence

The module evaluates:

- Higher-timeframe support or structural reference (`MOD 11`, `MOD 13`, `MOD 17`, `MOD 59`).
- Downside liquidity sweep or meaningful support test (`MOD 35`, `MOD 42`).
- Spot CVD and spot participation (`MOD 05`, `MOD 07`, `MOD 19`).
- Selling exhaustion or absorption (`MOD 06`, `MOD 21`).
- Price displacement relative to negative delta (`MOD 06`, `MOD 08`).
- Order-book and bid-replenishment behaviour (`MOD 06`, `MOD 37`).
- Open-interest and liquidation context (`MOD 01`, `MOD 03`, `MOD 51`).
- Volume-profile and auction recovery (`MOD 11`).
- Reclaim of a relevant structural boundary (`MOD 11A/B`, `MOD 54`).

A lower wick, oversold indicator or liquidation heatmap alone cannot authorise accumulation.

## Rule 15. Accumulation Gate

A proposed buy must pass:

1. Data Integrity Gate (`MOD 36` / `MOD 61`).
2. Market Regime Gate (`MOD 16` / `MOD 33` / `MOD 60`).
3. Structural Context Gate (`MOD 17` / `MOD 54`).
4. Selling-Pressure Assessment (`MOD 03` / `MOD 06`).
5. Spot-Market Confirmation (`MOD 05` / `MOD 07` / `MOD 19`).
6. Reversal or Reclaim Confirmation (`MOD 11` / `00C` bar-count rules).
7. Entry Price and Execution Assessment (`MOD 12` / `MOD 37` `Net R >= 3.0`).
8. Inventory and Capital Boundary Check (`DIBSE` Sleeve A USDT floor & reservations).
9. Portfolio Risk Check (`MOD 18` `<= 0.75%` or `0.375%` equity risk cap).
10. Final Portfolio Allocation Controller approval.

If a mandatory gate fails, no BUY authorisation is issued.

---

# PART VI — BEARISH DISTRIBUTION MODULE

## Rule 16. Distribution Objective

Identify opportunities to convert a permitted quantity of existing tactical BTC into USDT when credible evidence indicates weakening upside progress, distribution or increased downside risk.

This module manages BTC exposure. It does not create short exposure.

## Rule 17. Required Evidence

The module evaluates:

- Higher-timeframe resistance or supply (`MOD 11`, `MOD 13C`, `MOD 41`).
- Failed upside auction or rejection (`MOD 11C`).
- Weakening spot participation (`MOD 05C`, `MOD 07B`).
- Deteriorating Spot CVD (`MOD 05`, `MOD 19`).
- Significant buying volume without sustained upside progress (`MOD 06B` Passive Limit Ask-Wall Capping).
- Evidence of supply absorption or distribution (`MOD 15B`, `MOD 39`).
- Failed reclaim or loss of relevant market structure (`MOD 54`).
- Order-book and liquidity changes (`MOD 21`, `MOD 34`).
- Derivative positioning as supporting context (`MOD 02B`, `MOD 04B`, `MOD 27B`).

A resistance touch, high RSI reading or liquidation heatmap target alone cannot authorise distribution.

## Rule 18. Distribution Classification

The module must distinguish:

**PROFIT-TAKING**

A partial conversion at a favourable price without evidence of major structural deterioration (`MOD 18` Stage 1 50% harvest).

**DEFENSIVE REDUCTION**

A reduction in BTC exposure because market structure or participation has weakened (`MOD 34A` `PRE_TRIM` 25%–40% reduction).

**FULL DEFENSIVE EXIT**

A permitted exit of tactical BTC inventory when severe conditions justify it (`MOD 18` Stage 2 / `MOD 60 M2` upstream veto exit).

A full exit must never automatically include protected long-term BTC holdings (`Sleeve B`).

## Rule 19. Distribution Gate

A proposed sell must pass:

1. Data Integrity Gate (`MOD 36` / `MOD 61`).
2. Market Regime Gate (`MOD 16` / `MOD 33` / `MOD 60`).
3. Structural Context Gate (`MOD 11` / `MOD 54`).
4. Upside Weakness Assessment (`MOD 02B` / `MOD 06B` / `MOD 13C`).
5. Spot-Market Confirmation (`MOD 05C` / `MOD 19`).
6. Distribution or Breakdown Confirmation (`MOD 11C` / `MOD 41`).
7. Sell Price and Execution Assessment (`MOD 37` slippage audit).
8. BTC Inventory Floor Check (`DIBSE` Sleeve A tactical BTC floor & protected Sleeve B isolation).
9. Portfolio Risk Check (`MOD 18` / `MOD 34` anti-capitulation sell-freeze check).
10. Final Portfolio Allocation Controller approval.

If a mandatory gate fails, no SELL authorisation is issued.

---

# PART VII — PORTFOLIO ALLOCATION CONTROLLER

## Rule 20. Single Final Decision Authority

The Portfolio Allocation Controller reconciles both trading modules and determines the permitted BTC/USDT exposure within the authorised tactical sleeve (`Sleeve A`).

It must consider:

- Current portfolio allocation.
- Market regime.
- Accumulation evidence.
- Distribution evidence.
- Data integrity.
- Risk restrictions (`MOD 18`, `MOD 31`, `MOD 60`).
- Existing orders.
- Inventory availability.
- Protected capital (`Sleeve B`).
- Expected execution costs (`MOD 37`).

No module may bypass this controller.

## Rule 21. Exposure Research Bands (Tactical Sleeve A Scope)

The following are research allocation bands within the authorised tactical sleeve (`Sleeve A`), subject to `MOD 18` stop-risk sizing (`<= 0.75%` total portfolio equity risk):

| Tactical BTC | Tactical USDT | Classification |
|---:|---:|---|
| 0% | 100% | Fully defensive (`100% Cash Lock` within Sleeve A) |
| 25% | 75% | Defensive |
| 50% | 50% | Balanced (Baseline 10% BTC / 10% USDT split) |
| 75% | 25% | BTC-heavy |
| 100% | 0% | Fully allocated to BTC (within Sleeve A cap) |

The controller may also maintain intermediate allocations when explicitly supported by the approved policy.

These bands apply strictly to the authorised tactical sleeve scope, never automatically to protected holdings (`Sleeve B`).

## Rule 22. Permitted Decisions

The controller may issue:

- ACCUMULATE BTC
- HOLD BTC
- REDUCE BTC
- DEFENSIVE EXIT
- RE-ACCUMULATE BTC
- REMAIN USDT
- NO TRADE
- DATA HALT
- HUMAN REVIEW

A decision must state its permitted size, rationale, evidence, invalidation conditions and expiry.

## Rule 23. Conflict Resolution

If accumulation and distribution modules produce conflicting signals:

1. Reconcile the evidence via `MOD 60` (Global 7-Rank Veto Precedence Ladder & Intra-Pillar Tie-Breakers).
2. Check whether the apparent conflict is caused by different timeframes (`MOD 10` / `MOD 54`).
3. Check data quality and timestamps (`MOD 36` / `MOD 61`).
4. Reassess the market regime (`MOD 33`).
5. Evaluate existing exposure and open orders.

If the conflict remains unresolved:

**Decision: NO TRADE / HOLD CURRENT INVENTORY (`MOD 60 M1 CONFLICT_DEADLOCK`).**

The system must not average contradictory signals into an artificial trade recommendation.

---

# PART VIII — POSITION SIZING AND RISK

## Rule 24. Conversion Limits

Every conversion must have a maximum permitted quantity or notional value.

Sizing must respect:

- Available asset inventory.
- Inventory floors.
- Active sleeve limits (`Sleeve A` 20% portfolio boundary).
- Existing reservations.
- Market regime.
- Portfolio risk policy (`MOD 18` `0.75%` / `0.375%` / `0.00%` stop-loss risk ceiling).
- Expected fees and slippage (`MOD 37`).

Negative inventory and borrowed balances are prohibited.

## Rule 25. Risk Budget

Risk-budget parameters are governed by `MOD 18` and `MOD 37`:

- `GATE_GREEN / CONSTRUCTIVE`: Maximum `0.75%` total portfolio equity risk per trade.
- `GATE_AMBER / MIXED`: Maximum `0.375%` total portfolio equity risk per trade.
- `GATE_RED / DISLOCATION`: `0.00%` new risk (`100% Cash Lock`).

Position size must not be derived from conviction scores alone.

The system must distinguish the amount of capital converted (`notional sleeve allocation`) from the amount of portfolio risk accepted (`stop-distance equity risk`).

## Rule 26. No Automatic Averaging Down

A continuing breakdown is not an accumulation signal.

Every additional buy requires a separately valid setup or a predefined, validated scale-in plan (`MOD 51B` staggered absorption ladder, with combined risk strictly `<= 0.75%`).

## Rule 27. No Automatic Rebuying Higher

After BTC has been converted into USDT, the system must not chase progressively higher BTC prices simply to restore exposure.

USDT may remain unconverted until the next qualified re-accumulation opportunity.

Opportunity cost must be reported.

## Rule 28. Inventory Protection

Long-term core BTC (`Sleeve B`) and tactical trading inventory (`Sleeve A`) must be separately identified.

Only authorised tactical inventory may be used by DIBSE.

No conversion cycle may silently consume protected holdings.

---

# PART IX — DIBSE EXECUTION AND ORDER MANAGEMENT

## Rule 29. Limit-Order Mandate

Limit orders are the preferred execution method (with `MOD 37` slippage-capped marketable limit orders permitted only when `MOD 08A` / `MOD 11B` confirms an LVN fast-traverse breakout).

Every proposed order must specify:

- Instrument (`BTC/USDT` or `BTC/USD`).
- Side (`BUY` or `SELL`).
- Limit price.
- Quantity.
- Notional value.
- Expected fees.
- Inventory impact.
- Setup reference (`MOD` & `CSU` identifier).
- Expiry.
- Cancellation conditions.

Unconstrained market orders are prohibited.

## Rule 30. Order Lifecycle

DIBSE must track:

`PROPOSED → APPROVED → SUBMITTED → WORKING → PARTIALLY FILLED → FILLED`

Alternative terminal states:

`CANCELLED / EXPIRED / REJECTED`.

An order must not be treated as filled or cancelled without confirmed exchange status.

## Rule 31. Partial Fills and Reservations

Only executed quantities are recognised as converted inventory.

Unfilled quantities remain reserved until confirmed cancellation, expiry or other verified terminal status.

The same asset must never be allocated twice.

## Rule 32. Order Reassessment

Working orders must be reassessed when:

- The original setup is invalidated.
- Market structure materially changes.
- The reference price becomes obsolete.
- Data integrity fails (`MOD 36`).
- Inventory constraints change.
- The order expires.

Critical data failure requires immediate order review.

---

# PART X — CONVERSION-CYCLE ACCOUNTING

## Rule 33. Loop A Accounting (`USDT → BTC → USDT`)

For `USDT → BTC → USDT`, record:

- Original USDT committed.
- BTC acquired.
- BTC subsequently sold.
- Gross and net USDT proceeds.
- Fees.
- Net realised USDT gain or loss.
- Cycle duration.

## Rule 34. Loop B Accounting (`BTC → USDT → BTC`)

For `BTC → USDT → BTC`, record:

- Original BTC sold.
- Gross and net USDT proceeds.
- BTC repurchased.
- Fees.
- Net BTC quantity gained or lost.
- Cycle duration.

The principal Loop B metric is:

$$\Delta\text{BTC} = \text{BTC}_{\text{repurchased}} - \text{BTC}_{\text{sold}}$$

A positive result indicates an increase in BTC quantity after accounting for the cycle's costs.

## Rule 35. Whole-Portfolio Performance

A profitable conversion cycle does not automatically mean the overall strategy is successful.

CORTEX must report:

1. Total portfolio value in USDT.
2. Total BTC quantity.
3. Realised and unrealised performance.
4. Trading fees and slippage.
5. Performance of the tactical sleeve (`Sleeve A`).
6. Performance of protected holdings (`Sleeve B`).
7. Opportunity cost.
8. Performance against relevant benchmarks.

---

# PART XI — FAILURE HANDLING AND OPERATIONAL STATES

## Rule 36. Data Failure

When critical data is unavailable, stale or conflicting (`MOD 36` / `MOD 61`):

- Suspend new trade approvals.
- Reassess working orders.
- Preserve inventory accounting.
- Reconcile exchange balances.
- Require verified recovery before resumption (`2 consecutive clean cycles` per `MOD 36`).

## Rule 37. Exchange Failure

Monitor:

- Connectivity.
- Order submission.
- Order status.
- Partial fills.
- Cancellation acknowledgement.
- Balance reconciliation.
- Fee deductions.
- Unexpected rejections.

No unverified execution state may be assumed.

## Rule 38. System States

CORTEX must support:

- `NORMAL`
- `WATCH`
- `SETUP`
- `CONFIRMED`
- `ELIGIBLE`
- `ORDER WORKING`
- `PARTIALLY FILLED`
- `FILLED`
- `RECONVERSION WATCH`
- `CYCLE COMPLETED`
- `INVALIDATED`
- `DATA HALT`
- `HUMAN REVIEW`

Each DIBSE loop may maintain its own operational state, but the Portfolio Allocation Controller governs the final portfolio decision.

---

# PART XII — VALIDATION AND PERFORMANCE REQUIREMENTS

## Rule 39. No Edge Claims Without Evidence

Neither CORTEX nor DIBSE may be described as profitable or possessing a verified trading edge until validated (`MOD 52` Rolling 30-Trade Expectancy Audit).

The integrated architecture is a strategy specification, not proof of profitability.

## Rule 40. Separate Module Testing

Test independently:

1. Bullish Accumulation Module.
2. Bearish Distribution Module.
3. DIBSE Loop A.
4. DIBSE Loop B.
5. Portfolio Allocation Controller.
6. Combined CORTEX-DIBSE strategy.

This identifies which component contributes value and which creates losses or unnecessary turnover.

## Rule 41. Benchmark Requirements

At minimum, compare against:

- 100% BTC buy-and-hold.
- 100% USDT.
- 50% BTC / 50% USDT.
- The proposed integrated rotation strategy.

Include realistic fees, slippage, order non-fills and execution delays.

## Rule 42. Validation Method

Testing must include:

- Historical backtesting.
- Multiple market regimes.
- Out-of-sample testing.
- Walk-forward validation.
- Parameter sensitivity.
- Drawdown analysis.
- Trade-frequency and turnover analysis.
- Missed-upside analysis.
- Avoided-downside analysis.
- BTC-denominated and USDT-denominated performance.

Prevent look-ahead bias, survivorship bias and overfitting.

## Rule 43. Required Performance Metrics

Report:

- Net return.
- CAGR.
- Maximum drawdown.
- Profit factor.
- Expectancy (`MOD 52`).
- Win rate.
- Average gain and loss.
- Trading costs.
- Turnover.
- Time in BTC and USDT.
- BTC quantity gained or lost ($\Delta\text{BTC}$).
- USDT balance gained or lost.
- Benchmark-relative performance.

A strategy must not be declared successful based only on its win rate or the number of completed conversion cycles.

---

# PART XIII — FINAL GOVERNING DOCTRINE

1. CORTEX-BTC is the sole governing framework.
2. DIBSE (`MOD 62`) is the operational dual-inventory engine.
3. BTC and USDT are both strategic inventories.
4. All trading is spot-only (`1.0x`).
5. No leverage, borrowing, margin or short selling.
6. Accumulation and distribution require independent evidence.
7. One Portfolio Allocation Controller governs all trade permissions.
8. Inventory reservations must be reconciled across both loops.
9. Protected BTC holdings (`Sleeve B`) cannot be silently used.
10. Data integrity failures prevent new trade authorisation (`MOD 36`).
11. No trade is compulsory.
12. Limit orders require explicit prices, quantities and expiry rules.
13. Every conversion cycle must be independently accounted for.
14. All portfolio performance must include costs and opportunity costs.
15. No profitability or edge claim without independent validation (`MOD 52`).
16. Human authorisation remains mandatory.

---

# FINAL SYSTEM DIRECTIVE

CORTEX-BTC governs the complete BTC/USDT rotation process.

DIBSE (`MOD 62`) supplies the operational machinery to manage BTC and USDT inventories, identify and track two-way conversion cycles, and control the order lifecycle.

The accumulation and distribution loops may operate independently as research and opportunity-detection modules, but all proposed trades must pass through one central Portfolio Allocation Controller.

The system must be willing to accumulate BTC, reduce BTC, hold either asset or abstain entirely.

Its objective is not maximum trading activity.

Its objective is disciplined portfolio rotation, preservation of capital, measurable improvement in BTC and USDT holdings, and demonstrable performance after all costs.

**CORTEX governs. DIBSE operates. The Portfolio Allocation Controller decides. The human operator authorises execution.**
