### PROJECT CORTEX-BTC — MODULE 42.1: THE SYMMETRICAL 11-PATTERN PRICE ACTION & MICROSTRUCTURE PLAYBOOK
**Waterfall Tier:** Pillar 2 & Pillar 4 Sub-Module (Symmetrical Range Extremes, Liquidity Sweeps, Order-Flow Absorption & Bidirectional Spot BTC/USDT Swing Execution) — child operational playbook of **MOD 42 (Classical Structural Shapes & Liquidity-Pool Authentication Engine)**, harmonized with **MOD 05** (Spot vs. Perp CVD), **MOD 06** (Passive Limit Absorption), **MOD 11** (Volume Profile Topology), **MOD 18** (0.75% Spot Risk Sizing), **MOD 35** (Liquidation Sweeps), **MOD 54** (MTF Kline Lock), **MOD 60** (7-Rank Veto Precedence Ladder), and **MOD 62** (Dual-Inventory Bidirectional Swing Engine — DIBSE v2.0).
**Document Provenance:** Codified from `the_symmetrical_11_pattern_price_action_microstructure_playbook.md`.
**Governance Posture:** Symmetrical Bidirectional Spot Swing Playbook (`USDT -> BTC` Accumulation at Range Lows / Demand Clusters vs. `BTC -> USDT` Distribution at Range Highs / Supply Clusters). Subordinate to `MOD 60` Ranks 0–3 upstream vetoes (`MOD 36` Data Halt, `MOD 16`/`MOD 22` Liquidity Lock, `MOD 31` `ICDM >= 60`, `MOD 44`/`MOD 58` Event Lock, `MOD 64` Shadow Credit Stress).

---

#### 0. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)
```yaml
module_id: "MOD_42.1"
parent_module: "MOD_42"
entry_type: "BIDIRECTIONAL_PRICE_ACTION_AND_MICROSTRUCTURE_PLAYBOOK"
waterfall_pillar: "PILLAR_2_AND_4_SYMMETRICAL_SPOT_SWING_EXECUTION"
title: "The Symmetrical 11-Pattern Price Action & Microstructure Playbook"

# MOD 60 & PILLAR 1 PRECEDENCE REGISTRATION
governance_registration:
  mod_60_precedence_rank: "PILLAR_2_EXECUTION_SUBMODULE_TO_MOD_42_AND_MOD_62"
  pillar_1_upstream_override: "If Pillar 1 == GATE_RED (or ICDM >= 60), block all Long accumulation patterns (#1, #3, #5, #7, #10); allow only Short distribution rotations (BTC -> USDT: #2, #4, #6, #8, #9, #11) to de-risk existing Sleeve A BTC inventory."
  spot_only_constraint: true # Strict 1.0x unleveraged BTC/USDT spot inventory rotation (zero margin/perps)

# SYMMETRICAL 11-PATTERN REGISTRY
symmetrical_patterns:
  range_extreme_sweeps:
    long: "Pattern #1: Double Bottom (Sweep)"
    short: "Pattern #2: Double Top (Sweep)"
  range_extreme_front_runs:
    long: "Pattern #3: Double Bottom (No Sweep / Front-Run)"
    short: "Pattern #4: Double Top (No Sweep / Front-Run)"
  rounded_retests:
    long: "Pattern #5: Rounded Retest (Long)"
    short: "Pattern #6: Rounded Retest (Short)"
  multi_drive_campaigns:
    long: "Pattern #7: Three Drives (Long)"
    short: "Pattern #8: Three Drives (Short)"
  ltf_execution_and_momentum:
    short_poi_trap: "Pattern #9: The Mouse Trap"
    long_momentum_filter: "Pattern #10: Bullish Divergence (RSI 14 & AO)"
    short_momentum_filter: "Pattern #11: Bearish Divergence (RSI 14 & AO)"

# BEARISH GATE 3 CONFIRMATION RULEBOOKS
gate_3_bearish_rulebooks:
  - "Rulebook 3.1: Spot vs. Perp CVD Divergence (Price HH + Perp CVD HH + Spot CVD LH/Flat)"
  - "Rulebook 3.2: BTC-Denominated OI Spike + Positive Funding Sweep Snap"
  - "Rulebook 3.3: P-Shaped Fixed-Range Volume Profile & Poor Highs VAL Breakdown"
  - "Rulebook 3.4: Anchored VWAP (AVWAP) Breakdown & Kiss-of-Death Retest"

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  min_reward_to_risk: 3.0 # Net R >= 3.0 after MOD 37 slippage
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only (BTC <-> USDT)
  dibse_loop_mapping:
    long_patterns_1_3_5_7_10: "Loop A (USDT -> BTC -> USDT)"
    short_patterns_2_4_6_8_9_11: "Loop B (BTC -> USDT -> BTC)"
```

---

#### I. Master Playbook Architecture (The 11 Setups)

Classical chart patterns often fail in liquid cryptocurrency markets because they treat diagonal geometry as predictive rather than reading price as a continuous auction for liquidity. When large participants need to fill size without causing immediate slippage, they engineer liquidity events—pushing price through obvious swing highs and lows to trigger resting stop-loss orders and breakout entries before reversing direction.

To build a fully symmetrical decision framework that balances long-side accumulation with short-side distribution, the original 7 patterns are expanded into an **11-Pattern Symmetrical Playbook**. Every accumulation setup at range lows has an exact mirror distribution setup at range highs, backed by deterministic microstructure filters (**Cumulative Volume Delta**, **Footprint Absorption**, **Open Interest**, **Anchored VWAP**, and **Dual RSI/AO Divergences**).

The playbook is organized into four functional tiers: **Range-Extreme Sweeps**, **Range-Extreme Front-Runs & Rounded Retests**, **Multi-Drive Exhaustion Campaigns**, and **LTF Execution & Momentum Filters**.

| # | Pattern Name | Direction | Structural Tier | Core Market Mechanics |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Double Bottom (Sweep)** | Long (`USDT → BTC`) | Range Extreme | Undercuts `Range Low` (`First Low`) to flush sell stops before reclaiming the floor with aggressive buyers. |
| **2** | **Double Top (Sweep)** | Short (`BTC → USDT`) | Range Extreme | Pierces `Range High` (`First High`) to trigger buy stops and breakout longs before snapping back inside the range. |
| **3** | **Double Bottom (No Sweep)** | Long (`USDT → BTC`) | Range Extreme | Passive limit bids step in early (`Front-run`) just above `Range Low`, absorbing market sellers before stops are reached. |
| **4** | **Double Top (No Sweep)** | Short (`BTC → USDT`) | Range Extreme | Passive limit asks step in early (`Front-run`) just below `Range High`, absorbing market buyers before highs are swept. |
| **5** | **Rounded Retest (Long)** | Long (`USDT → BTC`) | Range Extreme | Price dips into an established `Demand Cluster`, carves a curved multi-bar bowl of higher lows, and launches upward. |
| **6** | **Rounded Retest (Short)** | Short (`BTC → USDT`) | Range Extreme | Price curves up into a `Supply Cluster`, rejects on a `1st test`, sweeps that internal high (`SFP`), and rolls over. |
| **7** | **Three Drives (Long)** | Long (`USDT → BTC`) | HTF Reversal | Three descending drives separated by two `LH` bounces systematically exhaust forced sellers into HTF support. |
| **8** | **Three Drives (Short)** | Short (`BTC → USDT`) | HTF Reversal | Three ascending drives separated by two `HL` pullbacks systematically exhaust breakout buyers into HTF resistance. |
| **9** | **The Mouse Trap** | Short (`BTC → USDT`) | LTF Execution | Price surges with `Speed` into a POI, forms flat `Poor Highs`, sweeps them to trap buyers, and breaks down. |
| **10** | **Bullish Divergence (RSI & AO)** | Long (`USDT → BTC`) | Momentum Filter | Marginal lower low into a `Demand Zone` or `SFP` paired with simultaneous higher lows on both RSI and AO. |
| **11** | **Bearish Divergence (RSI & AO)** | Short (`BTC → USDT`) | Momentum Filter | Marginal higher high into a `Supply Zone` or `SFP` paired with simultaneous lower highs on both RSI and AO. |

---

#### II. Detailed Pattern Reference & Execution Mechanics

##### 1. Double Bottom (Sweep) — Long (`USDT → BTC`)
* **Structural Anatomy:** Price establishes a `First Low` at `Range Low`, rotates higher, and later returns to undercut that floor (`Sweep`). That pierce clears resting sell stops and tempts late breakdown shorts before price reclaims `Range Low` with impulsive bullish candles (`Initiation "Buyers"`).
* **Microstructure Confluence:** A sharp spike in **volume** and **negative delta** during the sweep wick, followed immediately by a reclaim of `Range Low` and a flip to positive delta, proves that forced sellers were absorbed rather than initiating a genuine breakdown.
* **Trigger & Invalidation:** Execute on the reclaim close back above `Range Low` (or the first bullish displacement candle). Place structural invalidation beneath the sweep wick extreme.

##### 2. Double Top (Sweep) — Short (`BTC → USDT`)
* **Structural Anatomy:** The exact mirror of Pattern #1 at range resistance. Price prints a `First High` at `Range High`, rotates lower, and returns to poke cleanly above `First High` (`Sweep`), triggering short-covering stops and breakout entries before snapping back beneath `Range High`.
* **Microstructure Confluence:** Look for a surge in **positive delta**, **volume**, and **Open Interest (OI)** during the sweep wick as late leveraged longs open at the highs, followed by immediate acceptance back below `Range High` and `Initiation "Sellers"`.
* **Trigger & Invalidation:** Execute on the close back below `Range High` once sellers step in. Place invalidation cleanly above the sweep wick peak.

##### 3. Double Bottom (No Sweep / Front-Run) — Long (`USDT → BTC`)
* **Structural Anatomy:** Price prints `First Low` at `Range Low` and rallies. On the second leg down, early longs get flushed, but passive limit buyers step up early (`Front-run`) just above `Range Low`, preventing price from reaching the resting stop cluster beneath the first wick.
* **Footprint Tie-Breaker:** Because a front-run looks identical to a pending breakdown on standard candles, use the **footprint chart**. Heavy negative delta and large bid-side prints at the candle lows *without* downward price follow-through confirm passive bid absorption.
* **Trigger & Invalidation:** Execute when buyers lift the offer aggressively (`Initiation "Buyers"`) off the front-run low. Invalidation sits beneath the untouched `Range Low`, as a break there indicates absorption failed.

##### 4. Double Top (No Sweep / Front-Run) — Short (`BTC → USDT`)
* **Structural Anatomy:** Price sets `First High` at `Range High` and pulls back. On the second push upward, passive limit sellers step in early (`Front-run`) just below `Range High`, absorbing incoming market buy orders before the stop pool above `First High` can be triggered.
* **Footprint Tie-Breaker:** On the footprint chart, look for heavy positive delta and large ask-side absorption prints near the second peak while price stalls and fails to tick higher.
* **Trigger & Invalidation:** Execute on downside displacement (`Initiation "Sellers"`) once buyers exhaust against the ask wall. Invalidation sits above the untouched `Range High`.

##### 5. Rounded Retest (Long) — Long (`USDT → BTC`)
* **Structural Anatomy:** After rallying away from an established `Demand Cluster`, price rotates back down into the upper boundary of that shaded zone, prints a brief rejection wick, and carves a smooth, curved bowl of higher lows (`Rounded Retest`) rather than a sharp V-bottom.
* **Microstructure Confluence:** Selling volume dries up through the curve of the base while Cumulative Volume Delta (CVD) stabilizes or trends upward ahead of price, signaling quiet accumulation.
* **Trigger & Invalidation:** Execute on the bullish shift candle (`"Entry"`) as `Initiation "Buyers"` push price out of the curve. Place invalidation cleanly beneath the entire `Demand Cluster` low so shallow wicks inside the zone do not trigger premature exits.

##### 6. Rounded Retest (Short) — Short (`BTC → USDT`)
* **Structural Anatomy:** Price curves upward into the lower boundary of an overhead `Supply Cluster`, rejects on a `1st test` (establishing a horizontal local high), pulls back slightly, and then makes a shallow push above that `1st test` high (`Internal Sweep` / SFP) inside the supply zone before rolling over.
* **Microstructure Confluence:** The `Internal Sweep` clears local stops built above the `1st test` without breaking out of the broader `Supply Cluster`. A Swing Failure Pattern (SFP) closing back beneath the `1st test` high confirms trapped buyers inside supply.
* **Trigger & Invalidation:** Execute on the bearish displacement candle (`"Entry"`) immediately following the SFP close back below the `1st test` line. Invalidation sits above the upper boundary of the `Supply Cluster`.

##### 7. Three Drives (Long) — Long (`USDT → BTC`)
* **Structural Anatomy:** A rare, high-conviction higher-timeframe (4H/Daily) bottoming structure composed of three descending swing lows (`1st Drive`, `2nd Drive`, `3rd Drive`) separated by two corrective lower-high bounces (`LH`). Each drive flushes a fresh wave of stops until forced sellers are completely drained at the `3rd Drive`.
* **Microstructure Confluence:** Higher lows on **RSI** and **AO** across the three descending drives, ideally paired with an **SFP** on the `3rd Drive` into higher-timeframe support.
* **Trigger & Invalidation:** Execute on `Initiation "Buyers"` reclaiming the prior structure off the `3rd Drive`. Invalidation sits directly below the `3rd Drive` extreme, with the two prior `LH` swing highs serving as sequential upside targets.

##### 8. Three Drives (Short) — Short (`BTC → USDT`)
* **Structural Anatomy:** The higher-timeframe distribution counterpart to Pattern #7. Price grinds upward through three ascending pushes (`1st Drive`, `2nd Drive`, `3rd Drive`) separated by two higher-low (`HL`) pullbacks into a major `Supply Cluster`, trapping breakout traders at every new high.
* **Microstructure Confluence:** Lower highs on **RSI**, **AO**, and **Spot CVD** across the three drives, paired with an **SFP** on the `3rd Drive` where price pierces a major HTF high and closes back below it.
* **Trigger & Invalidation:** Execute on `Initiation "Sellers"` breaking local structure beneath the `3rd Drive`. Invalidation sits above the `3rd Drive` high, targeting the prior `HL` liquidity pools on the way down.

##### 9. The Mouse Trap — Short (`BTC → USDT` LTF Execution Model)
* **Structural Anatomy:** Used to execute inside an established higher-timeframe Point of Interest (POI). Price arrives at the POI with `Speed`, stalls to form a tight horizontal ceiling of equal/clustered highs (`Poor Highs`), sweeps cleanly above those highs (`Mouse Trap`) to trigger breakout buyers, and snaps back inside the range.
* **Microstructure Confluence:**
  * **"P"-Shaped Volume Profile:** Heavy volume concentration near the top of the local distribution (trapped longs and short-covering) with a thin low-volume tail below.
  * **Delta Spike + Buyer Absorption:** A burst of positive delta on the sweep wick that gets absorbed by passive limit sellers, forcing price back beneath the `Poor Highs` line.
* **Trigger & Invalidation:** Execute once price closes back below the `Poor Highs` and breaks down from the local consolidation (`Initiation (Sellers)`). Place tight invalidation just above the trap wick.

##### 10. Bullish Divergence (RSI & AO) — Long Filter & Trigger (`USDT → BTC`)
* **Structural Anatomy:** Price presses into an established `Demand Zone` or sweeps a prior swing low (`SFP`) to print a marginal lower low, while both **RSI (14)** and the **Awesome Oscillator (AO)** print clear higher lows.
* **Why Both Indicators Matter:** RSI measures closing-price velocity while AO tracks broader median-price wave momentum (5- vs. 34-period SMAs). Requiring both to diverge simultaneously inside a `Demand Zone` filters out early oscillator signals during strong downtrends.
* **Trigger & Invalidation:** Enter on the first bullish displacement candle that reclaims above the prior swing low inside the zone. Invalidation sits beneath the divergence sweep low.

##### 11. Bearish Divergence (RSI & AO) — Short Filter & Trigger (`BTC → USDT`)
* **Structural Anatomy:** Price pushes into an overhead `Supply Zone` or sweeps a prior swing high (`SFP`) to print a marginal higher high, while both **RSI (14)** and **AO** print lower highs.
* **Why Both Indicators Matter:** Confirms that upward price expansion is losing both closing velocity (RSI) and underlying wave impulse (AO) right as price tests institutional supply.
* **Trigger & Invalidation:** Enter on the bearish displacement candle that closes back below the swept swing high or `1st test` reference level. Invalidation sits above the divergence sweep high.

---

#### III. Bearish Microstructure & Derivatives Confirmation Rulebooks

To prevent premature top-calling during strong uptrends, none of these four tools are standalone trade triggers. Each rulebook operates strictly inside **Gate 3 (Microstructure & Momentum Confirmation)** after **Gate 1 (HTF Supply Cluster / Range High)** and **Gate 2 (Patterns #2, #4, #6, #8, #9, or #11)** are already present.

##### Master Confirmation Matrix

| Tool | Exact Anchor / Setting | Mandatory Confirmation Signal | Execution Trigger (`BTC → USDT`) | Hard Invalidation |
| :--- | :--- | :--- | :--- | :--- |
| **3.1 Spot vs. Perp CVD** | Last 2 swing highs at `Supply Cluster` | Price HH + Perp CVD HH + **Spot CVD LH or flat** | Sweep reclaim close + Perp CVD hook down | Spot CVD surges to new HH above resistance |
| **3.2 OI + Funding Spike** | Sweep candle above `Range High` / `Poor Highs` | **BTC OI spikes** + positive funding on the sweep | Candle closes back **below** swept high | OI drops on breakout (short squeeze) or acceptance above |
| **3.3 "P"-Shape Profile** | FRVP from impulse origin to sweep peak | Upper HVN bulb + `Poor Highs` + thin lower tail | Candle close **below** upper bulb's **VAL** | Price reclaims above the `Mouse Trap` sweep wick |
| **3.4 Anchored VWAP** | Swing low or impulse-base wick of the rally | Bearish pattern + impulsive close below AVWAP | Failed retest rejection from **underside** of AVWAP | Clean candle close back above AVWAP |

##### Rulebook 3.1: Spot vs. Perp CVD Divergence
* **Core Objective:** Detect when an upward push into resistance is driven purely by leveraged futures chasing rather than genuine spot demand, while spot holders quietly distribute into the bid.
* **Step 1 — Configure Clean Telemetry Feeds:** Plot **Spot CVD** (aggregated across major spot venues such as Binance BTC/USDT, Coinbase BTC/USD, and OKX BTC/USDT) alongside **Perpetual Futures CVD**. Match the CVD candle interval to your execution timeframe (15m/1H for LTF execution like **#9 The Mouse Trap**; 4H for HTF structures like **#8 Three Drives**).
* **Step 2 — Define the Anchor Window:** Measure CVD behavior across the **last two swing highs** testing the `Supply Cluster` or `Range High` (for example, `1st Test` vs. `Internal Sweep` in **#6 Rounded Retest**, or `2nd Drive` vs. `3rd Drive` in **#8 Three Drives**).
* **Step 3 — Verify Deterministic Divergence Criteria:**
  * **Price:** Prints a higher high (or sweeps above the prior high).
  * **Perp CVD:** Prints a clear higher high (aggressive market-buy orders lifting perp offers).
  * **Spot CVD (Required):** Fails to make a higher high—either printing a **lower high** (net spot selling into the rally) or remaining completely **flat** while Perp CVD spikes vertically.
* **Step 4 — Execution Trigger & Invalidation:**
  * **Trigger:** Wait for Perp CVD to hook downward and price to close back beneath the swept swing high (`Initiation "Sellers"`), confirming that spot sellers have absorbed the perp breakout. Rotate **BTC → USDT**.
  * **False-Signal Filter / Invalidation:** If **Spot CVD** suddenly surges upward alongside Perp CVD and holds above the prior swing high, genuine spot accumulation is absorbing supply—abort the bearish thesis immediately.

##### Rulebook 3.2: Open Interest (OI) Spike + Positive Funding Timing
* **Core Objective:** Confirm that a liquidity sweep above `Range High` or `Poor Highs` trapped fresh leveraged longs at the peak, turning their stop-losses and liquidation levels into forced market-sell fuel on the way down.
* **Step 1 — Baseline Observation Before the Sweep:** Monitor aggregated **Open Interest (in BTC terms, not USD)**—measuring in BTC removes price-inflation distortion so you see true net contract creation—alongside **8-hour / 1-hour Funding Rates**.
* **Step 2 — Identify the Sweep & Positioning Surge:** As price pierces above `First High` (**#2 Double Top Sweep**), `Poor Highs` (**#9 Mouse Trap**), or the `3rd Drive` (**#8 Three Drives**), verify two simultaneous shifts:
  1. **BTC-Denominated OI Jumps:** Sharp vertical expansion in open contracts during the sweep candle(s), proving the move was fueled by **new leveraged positions opening** rather than existing shorts simply closing (which would cause OI to drop).
  2. **Funding Rate Skews Positive:** Funding climbs noticeably above baseline, confirming the newly opened OI is heavily skewed toward aggressive late longs.
* **Step 3 — Time the Reclaim (The Trap Snap):** **Do not sell while OI is still expanding above the swept high.** Wait for the sweep candle (or the immediate follow-up candle) to **close back below the swept reference level**. Once price closes back inside the range with elevated OI still trapped above the high, any downside displacement forces those underwater longs to market-sell (`Initiation "Sellers"`).
* **Step 4 — Execution Trigger & Invalidation:**
  * **Trigger:** Execute **BTC → USDT** rotation on the close back below the swept high once downward momentum begins unwinding the elevated OI.
  * **False-Signal Filter / Invalidation:** If OI drops sharply *during* the upward breakout (pure short squeeze with no trapped longs) or if price consolidates *above* the swept high for multiple bars while funding normalizes, the breakout is accepted—stand down.

##### Rulebook 3.3: "P"-Shaped Volume Profile & Poor Highs Breakdown
* **Core Objective:** Map trapped upper-range inventory created by short-covering and late breakout buying, and time the breakdown once price exits the high-volume shelf into the thin air pocket below.
* **Step 1 — Construct the Local Session / Swing Profile:** Pull a **Fixed-Range Volume Profile (FRVP)** from the origin of the upward impulse (`Speed` leg in **#9 Mouse Trap** or the start of the final rally leg) up to the sweep peak.
* **Step 2 — Verify the "P"-Shape & Poor Highs Anatomy:**
  * **Upper Bulb (HVN):** Heavy volume concentration clustered tightly near the top of the move, creating a prominent **Point of Control (POC)** and thick **Value Area** right beneath resistance.
  * **Poor Highs:** Two or more candle highs stalling within a few ticks of the exact same price level without clean excess rejection wicks, showing buyers repeatedly tried and failed to clear passive supply.
  * **Lower Tail (LVN):** A thin, low-volume single-print stem beneath the upper bulb where price moved too fast to build structural support.
* **Step 3 — Wait for Value Area Low (VAL) Acceptance Below:** After the `Mouse Trap` sweep above the `Poor Highs` snaps back into the upper bulb, mark the **Value Area Low (VAL)** of that upper "P"-shaped distribution.
  * **Trigger:** Execute **BTC → USDT** rotation when a candle **closes cleanly below the upper bulb's VAL** (and ideally retests that VAL from underneath as resistance). Once price accepts below the VAL, trapped longs inside the heavy upper node liquidate rapidly through the thin lower tail toward the prior range POC/VAL.
* **Step 4 — Invalidation:** Place structural invalidation just above the `Mouse Trap` sweep wick peak (or above the upper bulb's Value Area High if trading a wider 4H profile).

##### Rulebook 3.4: Anchored VWAP (AVWAP) Breakdown & Failed Retest
* **Core Objective:** Identify the exact volume-weighted average cost basis of buyers who drove the upward leg, and use the loss of that level to confirm that buyers are underwater and turning into overhead supply.
* **Step 1 — Select the Exact Anchor Point (Deterministic Rules):** Anchor the VWAP strictly to one of two structural origins—never arbitrarily mid-trend:
  1. **Primary Swing Anchor:** The exact lowest wick candle (`First Low` or range floor) that initiated the entire upward rotation into the `Supply Cluster`.
  2. **Impulse-Leg Anchor (LTF):** For steep parabolic pushes into resistance (such as **#9 Mouse Trap** or the `3rd Drive` in **#8**), anchor to the base candle of the final vertical impulse leg.
* **Step 2 — Wait for the Bearish Pattern & Initial Breakdown:** While price trends higher, the rising **AVWAP** acts as dynamic support. After a bearish structure completes (**#6 Rounded Retest**, **#8 Three Drives**, or **#11 Bearish Divergence**), wait for an impulsive bearish candle (`Initiation "Sellers"`) to **close decisively below the AVWAP**.
* **Step 3 — Execute the "Kiss of Death" Retest:**
  * Aggressive entries can execute on the initial close below AVWAP when paired with an SFP reclaim.
  * **High-Probability Confirmation Entry:** Wait for price to bounce weakly back up to touch the **underside of the flattening/declining AVWAP** and print a bearish rejection wick or lower-timeframe engulfing close. At that touch, trapped buyers who bought the rally are exiting at breakeven, reinforcing supply. Rotate **BTC → USDT** on the rejection close.
* **Step 4 — Invalidation & Target Trail:**
  * **Invalidation:** A clean candle close back *above* the AVWAP and the local swing high of the failed retest.
  * **Downside Target:** Trail **BTC → USDT** allocation down toward the next higher-timeframe `Demand Cluster` or the AVWAP anchored from the prior macro swing low.

---

#### IV. Bidirectional Spot BTC/USDT Execution & Rotation Protocol

In an unleveraged dual-asset spot portfolio (**BTC + USDT**), short-side patterns do not require margin or perpetual contracts. Instead, long patterns govern **USDT → BTC accumulation** (`DIBSE Loop A`), while short patterns govern **BTC → USDT distribution** (`DIBSE Loop B`), continuously harvesting two-way volatility without liquidation risk (`<= 0.75%` max portfolio risk per trade, `Net R >= 3.0`).

##### Gate-by-Gate Execution Checklist

1. **Gate 1 — Higher-Timeframe Location (POI) & Pillar 1 Check:** Verify `Pillar 1` / `MOD 60` permissions (`GATE_RED` blocks all `USDT → BTC` accumulation) and identify `Range Low` / `Demand Cluster` (for `USDT → BTC`) or `Range High` / `Supply Cluster` (for `BTC → USDT`) on 4H/Daily structure. Never trade a pattern in mid-range air.
2. **Gate 2 — Structural Pattern Match:** Classify the interaction into one of the 11 setups (e.g., *Did price sweep the extreme (#1/#2), front-run it (#3/#4), carve a rounded retest (#5/#6), complete three drives (#7/#8), or form a Mouse Trap (#9)?*).
3. **Gate 3 — Microstructure & Momentum Confirmation:** Verify order-flow absorption or momentum exhaustion before committing capital:
   * *For Sweeps (#1, #2, #9):* Delta + volume spike on the wick followed by a reclaim close and OI/CVD confirmation (Rulebooks 3.1, 3.2, 3.3).
   * *For Front-Runs (#3, #4):* Footprint absorption at the candle extreme showing passive limit walls holding.
   * *For Divergences & Multi-Drives (#7, #8, #10, #11):* Simultaneous **RSI + AO** divergence inside the zone plus displacement shift or AVWAP breakdown (Rulebook 3.4).
4. **Gate 4 — Spot Rotation & Structural Invalidation (`MOD 18` / `MOD 37` / `MOD 62`):**
   * **Long Trigger (`USDT → BTC`):** Rotate allocated USDT tranche into spot BTC upon displacement confirmation (`<= 0.75%` risk, `Net R >= 3.0`). If price closes cleanly beyond the structural invalidation level (below the sweep low, `Demand Cluster`, or `3rd Drive`), rotate back to USDT to preserve capital and wait for the next HTF level.
   * **Short Trigger (`BTC → USDT`):** Rotate spot BTC inventory into USDT upon bearish displacement or AVWAP breakdown. Re-accumulate BTC only at lower structural demand zones or if price reclaims and accepts cleanly above the invalidated `Supply Cluster` high.

---

##### FINAL DIRECTIVE
**MOD 42.1 turns classical geometry into an exact bidirectional spot auction playbook: every long accumulation setup at demand has an exact short distribution mirror at supply, authenticated by Spot CVD, footprint absorption, BTC-denominated OI, "P"-shaped profiles, and Anchored VWAP—strictly at 1.0x unleveraged spot.**
