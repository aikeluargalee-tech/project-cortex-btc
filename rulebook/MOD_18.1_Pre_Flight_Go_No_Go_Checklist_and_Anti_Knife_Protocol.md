# PROJECT CORTEX-BTC — MODULE 18.1: PRE-FLIGHT GO/NO-GO CHECKLIST & ANTI-KNIFE PROTOCOL

**Waterfall Tier:** Pillar 2 (Microstructure & Order Flow Execution) & Pillar 3 (Derivatives Microstructure & Positioning) / Operational Execution Runbook
**Parent Framework:** Extension to MOD 18 (Master 5-Pillar Confluence & Risk Sizing) & MOD 62 (DIBSE v2.0 Operational Runbook)
**Governing Principle:** Binary Go/No-Go Gatekeeper before authorizing any Spot Buy order. A single "NO" enforces 100% Cash Lock.

---

## 1. Machine-Readable State & Routing Block

```yaml
module_id: "MOD_18.1"
entry_type: "OPERATIONAL_EXECUTION_RUNBOOK"
waterfall_pillar: "PILLAR_2_MICROSTRUCTURE_AND_PILLAR_3_DERIVATIVES"
title: "Pre-Flight Go/No-Go Checklist & Anti-Knife Protocol"
governing_rule: "BINARY_EXECUTION_GATEKEEPER"
failure_modes: 4
checklist_items: 10
veto_rule: "SINGLE_NO_ENFORCES_100_PERCENT_CASH"
```

---

## 2. Four Falling-Knife Failure Modes to Avoid

1. **Pre-Close Limit Catching**
   - *Rule:* Never rest passive limit buy orders inside a descending liquidation cluster.
   - *Mechanism:* If spot bids pull back or thin out, price slices straight through resting bids without bouncing.
   - *Enforcement:* Always wait for the official 15-minute bar to close before evaluating absorption or entry.

2. **Coordinated Spot Bleed**
   - *Rule:* If Spot CVD drops at the same steep trajectory as Futures CVD, real spot holders (ETFs, treasuries, whales) are actively distributing float.
   - *Mechanism:* Absence of domestic/fiat passive absorption means there is no sovereign bid of last resort.
   - *Enforcement:* Cancel all long setups immediately until Spot CVD flattens or reverses.

3. **Rising Open Interest Breakdowns**
   - *Rule:* If price flushes lower while Open Interest increases ($+\Delta\text{OI}$), aggressive momentum short sellers are opening fresh directional positions rather than exhausted longs liquidating.
   - *Mechanism:* Structural markdown driven by new capital, invalidating capitulation reset assumptions.
   - *Enforcement:* Stand down completely.

4. **Intra-Candle VAH Wick Rejections**
   - *Rule:* Price poking above Value Area High ($\text{VAH}$) mid-candle and closing back below it is overhead supply absorption, not a structural reclaim.
   - *Mechanism:* Classic "look-above-and-fail" auction failure trapping premature breakout buyers.
   - *Enforcement:* Only an official 15-minute candle close strictly above $\text{VAH}$ authorizes structural confirmation and entry.

---

## 3. Pre-Flight Go/No-Go Checklist (10 Checkpoints)

*Before executing any spot buy order, verify all 10 checkpoints. A single "NO" strictly enforces remaining in 100% Cash:*

1. **HTF Confluence:** Is price interacting with a verified 200D MA, 50W SMA, Bull Market Band, or multi-week High Volume Node (HVN)?
2. **Liquidity Sweep:** Did price sweep a visible 24-hour liquidation cluster below structural support?
3. **CVD Decoupling:** Did Futures CVD plunge while Spot CVD remained flat or positive?
4. **Volume Climax:** Did the sweep candle print $\ge 3.0\times$ average 15-minute volume?
5. **Margin Contraction:** Did Open Interest contract ($-\Delta\text{OI}$) during the sweep candle, confirming leverage reset?
6. **Absorption Footprint:** Did the Point of Control (POC) form in the lower 35% of the bar with an explicit lower rejection wick?
7. **Confirmed VAH Reclaim:** Did a subsequent 15-minute candle close strictly above the sweep bar's $\text{VAH}$?
8. **Hard Stop Defined:** Is $P_{\text{stop}}$ anchored cleanly beneath the exact sweep wick low (zero mental stops)?
9. **Risk Shield Sized:** Is maximum dollar loss capped at $\le 0.75\%$ of total portfolio equity with zero leverage ($1.0\times$ spot only)?
10. **Empirical Telemetry:** Are all values verified directly from live exchange feeds rather than unverified estimates (Fail-Closed)?
