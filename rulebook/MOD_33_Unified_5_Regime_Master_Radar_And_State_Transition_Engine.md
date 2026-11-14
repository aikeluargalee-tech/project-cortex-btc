# PROJECT CORTEX-BTC — MODULE 33: UNIFIED 5-REGIME MASTER RADAR & STATE-TRANSITION ENGINE
**Waterfall Tier:** Supreme Macro-Structural Regime Classifier (Sitting above Pillars 1–5 to govern active execution protocols and route tactical Configs A–J).
**Empirical Benchmark Anchor:** November 13, 2026 Live Synthesis — Governing the transition between structural liquidity expansion, multiple-compression chop, and liquidation/capitulation resets across the master architecture.

---

## 1. Machine-Readable State & Routing Block (Python / Hermes / NotebookLM Index)

```yaml
module_id: "MOD_33"
entry_type: "MASTER_REGIME_RADAR_CLASSIFIER"
waterfall_pillar: "SUPREME_MACRO_STRUCTURAL_REGIME_RADAR"
title: "Unified 5-Regime Master Radar and State-Transition Engine"

# MASTER REGIME GOVERNANCE & CONFIG ROUTING
master_regimes:
  REGIME_1_SECULAR_LIQUIDITY_EXPANSION:
    description: "Macro GREEN, Positive GEX, Spot-Led Trend"
    permitted_configs: ["CONFIG_A", "CONFIG_G"]
    risk_cap_pct: 0.75
  REGIME_2_EQUILIBRIUM_RANGE_COMPRESSION:
    description: "Neutral Liquidity, GK Squeeze <= 15th pct, Positive GEX Pinning"
    permitted_configs: ["CONFIG_A", "CONFIG_F", "CONFIG_J"]
    risk_cap_pct: 0.75
  REGIME_3_RESTRICTIVE_MULTIPLE_COMPRESSION:
    description: "High Real Rates / MOVE 90-115, STH-MVRV ~1.0 Battle"
    permitted_configs: ["CONFIG_C", "CONFIG_H"]
    risk_cap_pct: 0.375
  REGIME_4_LIQUIDITY_DRAIN_NEGATIVE_GAMMA:
    description: "Macro RED, ICDM >= 60, Negative GEX Acceleration, Negative Coinbase Premium"
    permitted_configs: ["CONFIG_E", "CONFIG_I"]
    risk_cap_pct: 0.00
  REGIME_5_CAPITULATION_EXHAUSTION_RESET:
    description: "Post-Flush OI Reset (-8% to -17%), STH-SOPR <= 0.96, Shark Accumulation + USD Spot CVD Reclaim"
    permitted_configs: ["CONFIG_F", "CONFIG_J"]
    risk_cap_pct: 0.375

# RISK & SIZING CONSTANTS (PILLAR 4)
risk_parameters:
  max_portfolio_risk_pct: 0.75
  amber_reduced_risk_pct: 0.375
  red_lock_risk_pct: 0.00
  leverage_permitted: 1.0 # Strict Unleveraged Spot Only
```

---

## 2. Master Regime Classification & Permitted Execution Matrix

| Master Regime | Supreme Macro-Structural Trigger (`Condition A`) | Structural Diagnosis (`Outcome B`) | Legally Permitted `MOD 30` Configs | Maximum Risk Ceiling (`Rule C`) |
| :--- | :--- | :--- | :--- | :--- |
| **`REGIME_1`**<br>**Secular Liquidity Expansion** | • Pillar 1 `GATE_GREEN` (`MOD 16/22`)<br>• Spot > rising `200D MA` (`MOD 17`)<br>• Positive Dealer Gamma (`Spot > Zero-Gamma Flip`, `MOD 25`)<br>• `ICDM Score <= 35` (`MOD 31`) | Full-stack macro, institutional ETF, and positive-gamma tailwind. | • **`CONFIG_A`** (Healthy Bull)<br>• **`CONFIG_G`** (Short Squeeze harvest) | **Full `0.75%` Portfolio Risk Ceiling** (`1.0x` unleveraged spot + Stage 2 runners). |
| **`REGIME_2`**<br>**Equilibrium Range & Compression** | • Pillar 1 neutral (`MOVE < 85`, stablecoins flat)<br>• Garman-Klass Volatility `<= 15th pct` (`MOD 12`)<br>• Positive Gamma pinning between Put & Call Walls | Coiled equilibrium balance; breakouts fail unless backed by USD Spot CVD. | • **`CONFIG_A`** (VWAP/VAH pullback retest)<br>• **`CONFIG_F`** (Re-Accumulation)<br>• **`CONFIG_J`** (Bear Trap Spring) | **Full `0.75%` Portfolio Risk Ceiling** strictly at Value Area boundaries (`R >= 3.0`). |
| **`REGIME_3`**<br>**Restrictive Multiple Compression** | • Restrictive real yields (`10Y TIPS > 2.0%`) / `MOVE 90–115` (`MOD 23/29`)<br>• Equity P/E contraction capping high-beta assets<br>• `ICDM Score = 36–59` | Valuation denominator drag; upside breakouts stall at overhead supply. | • **`CONFIG_C`** (Bullish Absorption at range low)<br>• **`CONFIG_H`** (Distribution Top exit) | **Half-Risk Cap (`0.375%` Maximum Risk)**; zero breakout chasing. |
| **`REGIME_4`**<br>**Liquidity Drain & Negative Gamma** | • Pillar 1 `GATE_RED` (`10Y > 5.0%`, `DXY > 103`, stablecoins draining, `TGA > $850B`)<br>• `ICDM Score >= 60`<br>• Negative Gamma (`Spot < Zero-Gamma Flip` & Put Wall)<br>• Negative Coinbase Premium (`MOD 19C`) | Active dollar liquidity drain compounded by dealer downside delta-hedging. | • **`CONFIG_E`** (Liquidation Cascade stand-down)<br>• **`CONFIG_I`** (Bear Trend cash preservation) | **Strict `100% Cash Lock` (`0.00%` Risk)** — all long entries blocked until `REGIME_5` triggers. |
| **`REGIME_5`**<br>**Capitulation Exhaustion & Reset** | • Post-flush OI wipeout (`-8% to -17%`, `MOD 03A`)<br>• `STH-SOPR <= 0.96` (`MOD 14D`)<br>• 5m liquidations `< $2M` + OI flat<br>• `100–10K BTC` shark accumulation + **Domestic USD Spot CVD reclaim** | Forced sellers exhausted; smart-money absorption establishing a structural floor. | • **`CONFIG_F`** (Post-Cascade Clean Base)<br>• **`CONFIG_J`** (Bear Trap / Wyckoff Spring) | **`0.375%` Half-Risk** (if Pillar 1 still `RED/AMBER`) up to **`0.75%` Full Risk** (`R >= 3.0`). |

---

## 3. State-Transition Rules (`M1` through `M6`)

| Transition ID | Path | Mandatory Telemetry Required to Trigger Transition | Governance Override |
| :--- | :--- | :--- | :--- |
| **`TR-01`** | `REGIME_4` $\rightarrow$ `REGIME_5` | Hourly OI drop halts (`< -0.3%/hr`), 5m liquidations drop `< $2M`, `15m/1H` hammer wick prints at HTF support, and **Domestic USD Spot CVD turns positive**. | Unlocks `CONFIG_F` / `CONFIG_J` reversal watch (capped at `0.375%` risk until Pillar 1 improves). |
| **`TR-02`** | `REGIME_5` $\rightarrow$ `REGIME_2` | Price reclaims 4H **VAH** and **Zero-Gamma Flip Level** (`MOD 25A`), `STH-SOPR` crosses back above `1.00`, and `ICDM Score` drops below `55`. | Upgrades risk ceiling from `0.375%` to full `0.75%` at confirmed Value Area boundaries. |
| **`TR-03`** | `REGIME_2` $\rightarrow$ `REGIME_1` | Net Fed Liquidity (`MOD 22`) expands `>= +$75B/4W`, 30D stablecoins grow `>= +1.5%`, price holds `>= 3` daily closes above `200D MA`, and `Coinbase Premium > +0.05%`. | Activates full trend-following mode (`CONFIG_A` + Stage 2 trailing runners). |
| **`TR-04`** | `REGIME_1` $\rightarrow$ `REGIME_3` | Real 10Y yields spike `> +15 bps`, `MOVE` crosses above `90`, or `ICDM Score` rises above `36` while Spot holds near `STH Realized Price`. | Immediately cuts max risk per trade in half (`0.75% -> 0.375%`) and disables breakout entries. |
| **`TR-05`** | `REGIME_1/2/3` $\rightarrow$ `REGIME_4` | `ICDM Score >= 60`, `Spot` loses `200D MA` + `Zero-Gamma Flip`, or `USD/JPY` / `MOVE` triggers an emergency Pillar 1 macro shock. | **Immediate Kill-Switch:** Exit open swings at market and lock **100% Cash**. |
| **`TR-06`** | `REGIME_5` $\rightarrow$ `REGIME_4` *(Failed Bottom)* | Reclaim fails: price closes `4+` consecutive 1H bars below sweep support (`00C`) and `USD Spot CVD` rolls back negative. | Hard stop triggered (`-0.375%` max loss); re-lock **100% Cash** immediately. |
