# PROJECT CORTEX-BTC — MODULE 65: MEDIA DE-NOISING, NARRATIVE TRIAGE & SIGNAL HYGIENE PROTOCOL

**Waterfall Tier:** Tier D (Meta-Governance, Pre-Ingestion Filter & Signal Hygiene Gateway) — cross-verified with MOD 36 (Telemetry Trust & Staleness SLA), MOD 60 (Precedence Ladder), and MOD 61 (Data Hub Ingestion & Hygiene Gate).
**Provenance & Empirical Benchmark Anchor:** Codified from market cycle down-trend field studies (*"Bitcoin in a Downtrend: How to Read Liquidity, ETF Flows, and Sentiment Without Getting Fooled"*).
**Governance Posture:** Mandatory Pre-Ingestion Firewall. Audits external media, influencer commentary, and vendor models. Has zero standalone trade authorization authority (cannot buy or sell); prevents unvetted narratives from triggering premature capital deployment or panic selling.

---

## 0. Machine-Readable State & Routing Block

```yaml
module_id: "MOD_65"
entry_type: "SIGNAL_HYGIENE_GATEWAY"
waterfall_tier: "TIER_D_META_GOVERNANCE"
title: "Media De-Noising, Narrative Triage & Signal Hygiene Protocol"

mod_60_registration:
  precedence_rank: "PRE_INGESTION_FILTER_TO_MOD_61"
  subordination: "Yields unconditionally to all MOD 60 Rank 0-4 vetoes. Cannot authorize standalone trade execution."

audit_criteria:
  timeframe_isolation: true
  closed_candle_confirmation: true
  primary_source_traceability: true
  falsifiability_defined: true
  risk_and_sizing_bounded: true

quarantine_threshold: ">= 2 FAILED_QUESTIONS -> ASSIGN 0.00% EXECUTION WEIGHT"
```

---

### PART I — THE 5-QUESTION MEDIA AUDIT GATE

Before any external analysis, YouTube/X narrative, or vendor model is ingested into operational planning, it must answer:

1. **Timeframe Separation:** Are higher-timeframe trends (1D/1W), tactical swings (4H/1H), and multi-year DCA horizons strictly isolated, or is the author shifting goalposts?
2. **Deterministic Trigger:** Does the analysis specify an exact candle-close confirmation and a hard invalidation price, or is it relying on unclosed intraday wicks?
3. **Primary-Source Verification:** Are ETF flows, derivatives, and sentiment numbers traceable to primary feeds (Farside, CoinGlass, Glassnode, FRED), or are they unverified estimates?
4. **Falsifiability Condition:** Does the analyst state an explicit *"I am wrong if..."* invalidation level alongside an alternative scenario?
5. **Risk & Sizing Completeness:** Does the thesis account for position sizing (capped at ≤ 0.75% portfolio risk), execution friction, and liquidity depth, or is it merely entertainment?

*Rule:* If an external thesis fails **two or more** questions, it is classified as entertainment, assigned **0.00% execution weight**, and quarantined.

---

### PART II — ANTI-TRAP CIRCUIT BREAKERS

* **CB-01 (Model-vs.-Order-Book Translation Filter):** Forbids treating liquidation heatmaps as actual resting limit orders. Long-lookback heatmaps (1Y–2Y) contain ghost bands from closed positions rather than active liquidity. True liquidity must be verified via Volume Profile (MOD 11) and Limit Order Book depth (MOD 06).
* **CB-02 (Single-Candle CHoCH & Moving-Goalpost Ban):** Prohibits declaring a trend reversal off a single candle close above a lower high. A valid trend reversal mandates a strict two-step sequence: **CHoCH close → Higher Low → Higher High close** on the governing timeframe.
* **CB-03 (Oversold RSI Extension vs. Timing Filter):** Treats daily RSI < 30 as a measure of downside momentum and extension, **never as a calendar bottom date or a standalone buy trigger**.
* **CB-04 (Backward-Looking Sentiment & Reflexive ETF Filter):** Treats Extreme Fear readings (≤ 15) and single-day ETF inflow pauses as historical lag and T+1 feedback loops rather than forward capital turnarounds.
* **CB-05 (Multi-Horizon Frame Separation Lock):** Strictly decouples long-term sovereign accumulation (Sleeve B) from intraday tactical execution (Sleeve A). Long-term "generational value" narratives are never permitted to override active daily cash locks.

---

### FINAL DIRECTIVE
**MOD 65 separates market mechanics from market theater. Models estimate, oscillators measure extension, sentiment reflects the past, and only multi-step candle-close structure backed by verified spot flow authorizes capital.**
