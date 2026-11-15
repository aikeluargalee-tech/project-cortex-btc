# PROJECT CORETEX BTC BRAIN — MODULE 49: ROLLING CROSS-ASSET CORRELATION & DECOUPLING MATRIX (BTC VS. NDX / GOLD / DXY)
**Waterfall Tier:** Pillar 1 (Cross-Asset Macro Regime & Contagion Filter) — operates directly alongside `MOD 16` (Macro Liquidity, Yields & DXY), `MOD 17` (Session Handoffs), `MOD 22` (Net Fed Liquidity), `MOD 23` (MOVE Index), `MOD 29` (Equity Multiple Compression & High-Beta Contagion), and `MOD 44` (Mega-IPO Capital Vacuums).
**Empirical Benchmark Anchor:**
1. **September 2026 False-Decoupling Trap:** In late August / early September 2026, Bitcoin's 90-day correlation with Gold hit a near six-year high while its correlation with US equities faded toward `0.00` during a sovereign bond sell-off—a temporary decorrelation that snapped back into extreme equity lockstep within 60 days.
2. **November 2026 Tech/AI & Strong-Dollar Lockstep:** By November 9–11, 2026, BTC's 30-day correlation with the **Nasdaq-100 (`NDX`)** climbed to **`0.72–0.75`** (`99th percentile` since 2020), driven by shared institutional ETF holders, AI/semiconductor volatility (`NVDA`/`AMD`, plus `~33%` of BTC miner revenue tied to AI data-center hosting), and a **US Dollar Index (`DXY`)** surge to **`103.08–103.41`** (`103.50` nine-month resistance) alongside hawkish Fed rate repricing and Gold testing `$3,870/oz`.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / GitHub Index)

```yaml
module_id: "MOD_49"
entry_type: "CROSS_ASSET_REGIME_CLASSIFIER"
waterfall_pillar: "PILLAR_1_CROSS_ASSET_CORRELATION"
title: "Rolling Cross-Asset Correlation & Decoupling Matrix (BTC vs. NDX / Gold / DXY)"

# ROLLING CORRELATION & BETA THRESHOLDS
correlation_parameters:
  lookback_windows_days: [30, 90]
  ndx_high_beta_lock_30d: 0.65 # Corr(BTC, NDX) >= +0.65 -> BTC trades as leveraged AI/Tech liquidity proxy (Nov 2026: 0.72-0.75)
  ndx_moderate_link_30d: [0.25, 0.64] # Normal macro co-movement
  ndx_decoupled_threshold_30d: 0.20 # Corr(BTC, NDX) <= +0.20 -> Independent crypto/sovereign drivers active
  gold_sovereign_alignment_30d: 0.45 # Corr(BTC, XAU) >= +0.45 -> Hard-asset monetary hedge alignment
  dxy_inverse_headwind_30d: -0.50 # Corr(BTC, DXY) <= -0.50 -> Strong dollar directly suppresses BTC spot
  dxy_key_resistance_zone: 103.50 # Nov 2026 9-month / 19-month ceiling watch
  ndx_beta_multiplier_warning: 1.75 # 30D rolling BTC/NDX beta >= 1.75x (amplified equity drawdown sensitivity)

# ANTI-TRAP CIRCUIT BREAKERS
circuit_breakers:
  CB_01_NO_SHORT_WINDOW_DECOUPLING_ILLUSION: "NEVER declare permanent decoupling from Nasdaq based on a 14-to-30 day dip in Corr(BTC, NDX) alone (Sept 2026 trap); require both 30D and 90D Corr(BTC, NDX) <= +0.25 AND positive Domestic USD Spot CVD (MOD 05)."
  CB_02_HIGH_BETA_NDX_BREAKDOWN_VETO: "When Corr(BTC, NDX)_30D >= +0.65 AND Nasdaq-100 / SOX breaks below 20D/50D support on expanding volume, enforce 100% Cash Lock on BTC until US tech indices print a confirmed higher low."
  CB_03_DXY_RESISTANCE_BREAKOUT_GUARD: "When DXY pushes above 103.00 toward 103.50+ with Corr(BTC, DXY)_30D <= -0.50, cap BTC breakout risk at 0.375% (GATE_AMBER) or 0.00% (GATE_RED) until DXY rejects resistance."
  CB_04_PURE_SPOT_BTC_ONLY: "Use NDX, Gold, and DXY strictly as upstream Pillar 1 regime filters—never trade equity, commodity, or FX instruments inside Project CoreTex BTC Brain."

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  high_beta_contagion_max_risk_pct: 0.00 # 100% Cash Lock when Corr_NDX >= 0.65 and NDX is breaking down
  dxy_headwind_cap_risk_pct: 0.375 # GATE_AMBER cap during strong-dollar resistance tests
  decoupled_spot_led_max_risk_pct: 0.75 # Full 0.75% spot risk when cross-asset gates clear + 4H VAH reclaims
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Protective Circuit Breakers (Mandatory Cross-Asset Invariants)

* **Circuit Breaker 1 — The Short-Window Decoupling Illusion (`CB-01`):** Temporary 2–4 week drops in equity correlation (such as August–September 2026) often reflect local positioning exhaustion rather than permanent structural decoupling. Require **both `30D` and `90D` `Corr(BTC, NDX) <= +0.25`** plus sustained `Domestic USD Spot CVD` (`MOD 05`) before treating Bitcoin as immune to Nasdaq sell-offs.
* **Circuit Breaker 2 — High-Beta Tech/AI Veto (`CB-02`):** When `Corr(BTC, NDX)_30D >= +0.65` (`90th–99th` percentile), shared multi-asset ETF desks and AI-hosting miner revenues link BTC directly to semiconductor/Nasdaq liquidity. If `NDX` or `SOX` is actively breaking down during US cash hours (`13:30–20:00 UTC`), block all BTC long entries (`100% Cash Lock`) regardless of intraday crypto oversold oscillators.
* **Circuit Breaker 3 — Strong-Dollar Ceiling Guard (`CB-03`):** Whenever `DXY >= 103.00` (`103.50` breakout zone) with `Corr(BTC, DXY)_30D <= -0.50` and rising US 10Y yields (`MOD 16`), dollar liquidity tightening acts as a direct gravity well on both Gold and Bitcoin. Wait for `DXY` momentum to roll over before deploying full `0.75%` spot risk.
* **Circuit Breaker 4 — Strict Single-Asset Execution (`CB-04`):** Cross-asset telemetry governs **permission and sizing only**—all capital deployment remains `1.0x` unleveraged Spot BTC (`<= 0.75%` max equity risk).

---

## 3. Core Conditional Signal Units (`Condition A -> Outcome B -> Rule C`)

### CSU-49A: High-Beta Tech/AI Liquidity Proxy Lockstep (`Corr_NDX_30D >= +0.65`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Rolling 30-day correlation `Corr(BTC, NDX) >= +0.65` (e.g., November 2026 `0.72–0.75` reading) with rolling beta `>= 1.5x`.
  2. `Nasdaq-100` or `SOX` (semiconductors) is trending below its `20D/50D` moving average with negative US Spot BTC ETF flows (`MOD 07`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Institutional multi-asset portfolios treat BTC as a 24/7 high-beta liquidity release valve during tech/AI de-risking (`MOD 29`).
  * **Probable Trajectory:** BTC cannot sustain an independent bull breakout while `NDX` is making lower lows; weekend crypto bounces risk sharp Monday `13:30 UTC` NY open reversals.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **ENFORCE `100% CASH LOCK` (`0.00%` tactical risk)** while `NDX` is in active breakdown; require `NDX` stabilization + `BTC 4H VAH` reclaim (`MOD 11`) before unlocking entries.

### CSU-49B: Strong-Dollar & Hawkish Rate Squeeze (`DXY >= 103.0` & `Corr_DXY <= -0.50`)
* **Trigger Condition A (The Telemetry Scan):**
  1. `DXY` surges above **`103.00`** toward **`103.50+`** resistance on hawkish Fed rate expectations while `Corr(BTC, DXY)_30D <= -0.50` and Gold breaks below key structural support (`< $3,870/oz`).
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Global dollar shortage / rising real discount rates compress all dollar-denominated store-of-value and risk assets simultaneously (`MOD 16`).
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **DOWNGRADE `Pillar 1` TO `GATE_RED` (`0.00%` risk) OR `GATE_AMBER` (`0.375%` max)** until `DXY` prints a confirmed daily rejection below `103.00` and US 10Y yields peak (`MOD 16 M1`).

### CSU-49C: Sovereign Monetary Decoupling & Gold-Aligned Expansion (`Corr_NDX <= +0.20` & `Corr_Gold >= +0.45`)
* **Trigger Condition A (The Telemetry Scan):**
  1. Both `30D` and `90D` `Corr(BTC, NDX) <= +0.20` while `Corr(BTC, Gold)_30D >= +0.45`.
  2. **Flow Authentication:** US Spot BTC ETFs record multi-day net inflows (`MOD 07`), `Coinbase USD Spot CVD` leads upward (`MOD 05A`), and `BTC` holds above `200D MA` / `4H VAH`.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** Capital is rotating into BTC and Gold as sovereign/monetary debasement hedges independent of equity earnings multiples.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **AUTHORIZE FULL `0.75%` SPOT RISK** (`GATE_GREEN`) on `MOD 30` pullback/breakout triggers with `Net R >= 3.0` (`MOD 37`); prioritize Stage 2 trailing runners (`MOD 18`).

### CSU-49D: High-Correlation `NDX` Bottom & Synchronous Rebound Setup
* **Trigger Condition A (The Telemetry Scan):**
  1. `Corr(BTC, NDX)_30D >= +0.65`, **AND** `Nasdaq-100` prints a confirmed higher low / reclaims its `20D` / `4H` structure on strong US cash breadth.
  2. Simultaneously, `DXY` rejects resistance (`< 103.00`), US Spot BTC ETF outflows halt (`>= $0M`), and `BTC` reclaims `4H VAH` (`4+` 1H bars) with positive `Domestic USD Spot CVD`.
* **Observed Outcome B (The Mechanical Trajectory):**
  * **Sovereign Macro Lens:** The same high-beta linkage that dragged BTC down now acts as synchronized institutional tailwind as risk desks re-gross.
* **Execution Rule C (The Non-Negotiable Action):**
  * **Action:** **UNLOCK `0.75%` SPOT LONG (`MOD 30 CONFIG_A / J`)** with `Net R >= 3.0` (`MOD 37`) and hard stop beneath the `4H VAL` / swing low.

---

## 4. Dynamic Regime Mutation Lookup Matrix (`M1` through `M8`)

| Mutation ID | Initial State | Telemetry Mutation Observed (`Condition A'`) | Mechanical Meaning (`Outcome B'`) | Mandatory Execution Override (`Rule C'`) |
| :--- | :--- | :--- | :--- | :--- |
| **M1: False Decoupling Snapback (Sept -> Nov Trap)** | `CSU-49C` (Low `NDX` Corr) | After 3–6 weeks of low equity correlation, `Corr(BTC, NDX)_30D` spikes from `< +0.15` to **`>= +0.55`** during a `> -2.5%` Nasdaq drop and ETF outflow day. | Macro risk-off shock re-coupled BTC to tech equities overnight. | **Immediately Revoke Decoupled Status (`CB-01`);** tighten stops or lock `100% Cash` if `4H VAL` breaks. |
| **M2: AI / Miner Power-Hosting Contagion** | `CSU-49A` (High `NDX` Corr) | `NVDA` / `SOX` drops `> -5%` on AI data-center capex slowdown headlines while `MOD 40` miner outflows tick up (`~33%` miner AI-hosting revenue link). | Equity AI-infrastructure stress is bleeding directly into Bitcoin miner cash flows and ETF sentiment. | **Hold `100% Cash Lock`** until `SOX`/`NVDA` stabilize and `MOD 40` miner exchange flows cool. |
| **M3: `DXY 103.50` Exhaustion Reversal** | `CSU-49B` (Strong Dollar) | `DXY` pokes above `103.50` on overbought daily RSI, closes back below `103.00`, and Gold + BTC simultaneously reclaim `4H VAH` on `USD Spot CVD`. | Dollar squeeze peaked at nine-month resistance, releasing liquidity across hard assets. | **Upgrade `Pillar 1` from `RED` to `AMBER/GREEN`;** authorize `0.375%–0.75%` spot entry. |
| **M4: Gold Safe-Haven Bid vs. BTC Liquidity Flush** | Cross-Asset Stress | Geopolitical or credit shock sends Gold `+2%` higher while `BTC` drops `-5%` (`Corr(BTC, Gold)_30D` flips sharply negative `< -0.30`). | In acute liquidity panics, institutions sell 24/7 BTC for cash first before rotating into sovereign safe havens. | **Do Not Buy BTC Simply Because Gold Is Up;** wait for `MOD 03` OI flush + `USD Spot CVD` absorption. |
| **M5: `NDX` Bounces While `BTC` Lags (Idiosyncratic Drag)** | `CSU-49A` / `49D` | `Nasdaq-100` rallies `+2%`, **but** `BTC` fails to reclaim `4H VAH` and `US Spot ETFs` keep bleeding (`MOD 44` IPO vacuum or exchange shock). | Crypto-specific liquidity drain (`MOD 44` / `MOD 32`) is overriding broader equity strength. | **Reject "Catch-Up Trade" Entry;** require BTC's own `4H VAH` + ETF flow confirmation. |
| **M6: Weekend Crypto Rally Without `NDX` Confirmation** | Saturday–Sunday Session | `BTC` pumps `+3%` over the weekend on offshore perps while `NDX` futures are closed and `Corr_NDX_30D >= +0.65`. | Unconfirmed weekend move vulnerable to Sunday `22:00 UTC` / Monday `13:30 UTC` equity gap alignment. | **Cap Risk / Wait for Monday NY Open Confirmation (`MOD 17 M3`)** before full sizing. |
| **M7: Sovereign Bond Yield Spike (`10Y > 5.25%`)** | Any Active State | US 10Y Treasury yield surges above `5.25%` (`MOD 16`), pushing `Corr(BTC, 10Y_Yield)_30D <= -0.60` and dragging both `NDX` and `BTC` lower. | Discount-rate shock is the root driver across all risk assets (`MOD 29`). | **Enforce `GATE_RED` (`100% Cash Lock`)** until 10Y yields peak and roll over (`MOD 16 M1`). |
| **M8: Macro Cross-Asset Feed Lag (`MOD 36`)** | Routine Scan | `NDX`, `XAU`, or `DXY` daily close feed lags `> 24H` over holidays/weekends. | Correlation denominator/numerator temporarily static. | Tag `MOD_49_STATE = UNKNOWN` (`MOD 36`); govern entries via live `MOD 05` USD Spot CVD + `MOD 07` ETF flows. |
