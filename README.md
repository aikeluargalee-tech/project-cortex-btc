# Project CoreTex BTC Brain (v4.0) — The Sovereign Bitcoin Brain Matrix

> **Build in Peace. Scan in War. Never re-learn a market lesson at a financial loss.**

Deterministic, zero-dependency Python 3 decision engine and **51-source quantitative rulebook vault** (`00`–`00D` + `MOD 01`–`MOD 46`) for **1.0x unleveraged Bitcoin (BTC) spot swing trading** and **secular cycle wealth preservation**, anchored to **Malaysia Time (`MYT / UTC+8`)**.

---

## Core Architecture & Non-Negotiable Guardrails

1. **Zero Hallucination / Zero Synthetic Data:** Missing or failed API feeds stay `null` (`None`), triggering `MOD 31`'s mandatory `50%` missing-field fragility penalty and `MOD 36` quorum checks.
2. **Firewall Between Reasoning & Execution:** `cortex_matrix_engine.py` deterministically compiles telemetry with a verifiable `determinism_sha256` hash. Rules live in `rulebook/`; manual overrides are prohibited.
3. **The 0.75% Sovereign Shield (1.0x Spot Only):** Maximum portfolio equity risk per trade is **`<= 0.75%`** (`0.375%` under `GATE_AMBER`, `0.00%` under `GATE_RED` / `ICDM >= 60`). Direct leverage (`> 1.0x`) is permanently excluded.
4. **Hard Execution Filters:** Spot longs require **`Net R >= 3.0`**, venue quorum **`>= 3/5`**, telemetry age **`<= 90 minutes`**, and clear equity loss locks (**`-1.50%` daily / `-3.00%` weekly**).
5. **No VPIN:** Uses **Rough Path Signatures (`MOD 08`–`MOD 10`)** and **Domestic USD vs. Offshore USDT Spot CVD (`MOD 05`, `MOD 07`, `MOD 19`)**.

---

## Repository Map

| Component | Path | Purpose |
| :--- | :--- | :--- |
| **Telemetry Fetcher** | [`btc_data_fetcher.py`](btc_data_fetcher.py) | Python stdlib-only fetcher pulling spot/depth (`Binance`, `Coinbase`, `CoinGecko`, `Kraken`, `OKX`), derivatives (`OKX`), mempool (`mempool.space`), and macro (`FRED`) telemetry. |
| **Schema Adapter** | [`cortex_schema_adapter.py`](cortex_schema_adapter.py) | Normalizes raw telemetry into canonical CORTEX-BTC fields without inventing missing values. |
| **Decision Compiler** | [`cortex_matrix_engine.py`](cortex_matrix_engine.py) | 6-step compiler (`MOD 36` -> `MOD 31` -> `MOD 33` -> `MOD 30` -> `MOD 37` -> `MOD 18`) emitting `cortex_verdict_latest.json` + SHA-256 attestation. |
| **Telegram HUD** | [`telegram_cortex_alert.py`](telegram_cortex_alert.py) | Formats HTML-safe `MYT (UTC+8)` mobile HUD cards with `Active Drivers` and sends via Telegram Bot API. |
| **Live Snapshots** | [`btc_metrics_latest.json`](btc_metrics_latest.json), [`cortex_verdict_latest.json`](cortex_verdict_latest.json) | Latest hourly market telemetry and deterministic verdict written by GitHub Actions. |
| **Hourly Cron** | [`.github/workflows/btc_fetcher_cron.yml`](.github/workflows/btc_fetcher_cron.yml) | Runs hourly at `:05` UTC (`workflow_dispatch` also enabled) using `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` secrets. |
| **Agent Skills** | [`SKILL.md`](SKILL.md), [`.hermes/skills/project-cortex-btc/SKILL.md`](.hermes/skills/project-cortex-btc/SKILL.md) | Standardized `agentskills.io` / Hermes Agent operator skill definitions. |
| **Knowledge Vault** | [`rulebook/`](rulebook/) | Complete 51-source Markdown rulebook (`00`–`00D`, `MOD 01`–`MOD 46`) + compiled [`PROJECT_CORTEX-BTC_Master_System-v4.md`](rulebook/PROJECT_CORTEX-BTC_Master_System-v4.md). |

---

## Quick Commands

### Run Pipeline Locally (Zero External Dependencies)
```bash
python btc_data_fetcher.py
python cortex_matrix_engine.py
python telegram_cortex_alert.py --dry-run
```

### Trigger Live GitHub Actions Run & Telegram Alert
```bash
gh workflow run btc_fetcher_cron.yml
```

---

## Rulebook Vault (`rulebook/`) — 51 Sources + Master System v4

- **Compiled Unified Rulebook (V4.0):** [`PROJECT_CORTEX-BTC_Master_System-v4.md`](rulebook/PROJECT_CORTEX-BTC_Master_System-v4.md)

### Core Architecture, Indices & Historical Invariants (`00`–`00D`)
- [`00`](rulebook/00_Charter_5_Pillar_Waterfall_and_Master_Architecture.md) — Charter, 5-Pillar Waterfall & Master Architecture
- [`00B`](rulebook/00B_Full_Stack_Master_Index.md) — V2.0 Full-Stack Master Index
- [`00C`](rulebook/00C_Historical_Intelligence_Registry_and_Cycle_Laws.md) — Historical Intelligence Registry & 9-Year Cycle Laws
- [`00D`](rulebook/00D_Complete_Source_Master_Directory.md) — Core Directory Reference

### Quantitative Execution Modules (`MOD 01`–`MOD 46`)
<details>
<summary>Expand all 47 module files (MOD 01 – MOD 46)</summary>

- [`MOD 01`](rulebook/MOD_01_Rising_Open_Interest_Extreme_Negative_Perpetual_Basis.md) — Rising Open Interest + Extreme Negative Perpetual Basis
- [`MOD 02`](rulebook/MOD_02_Rising_Open_Interest_High_Positive_Perpetual_Basis.md) — Rising Open Interest + High Positive Perpetual Basis
- [`MOD 03`](rulebook/MOD_03_Deleveraging_Flushes_And_Open_Interest_Reset_Mechanics.md) — Deleveraging Flushes & Open Interest Reset Mechanics
- [`MOD 04`](rulebook/MOD_04_Funding_Rate_Velocity_And_Price_Divergence_Matrix.md) — Funding Rate Velocity & Price Divergence Matrix
- [`MOD 05`](rulebook/MOD_05_The_4_Quadrant_Spot_CVD_vs_Perpetual_CVD_Matrix.md) — The 4-Quadrant Spot CVD vs. Perpetual CVD Matrix
- [`MOD 06`](rulebook/MOD_06_Passive_Limit_Absorption_vs_Market_Taker_Exhaustion.md) — Passive Limit Absorption vs. Market Taker Exhaustion
- [`MOD 07`](rulebook/MOD_07_Domestic_Fiat_Gateways_and_Spot_ETFs_vs_Offshore_Perp_USDT_Flows.md) — Domestic Fiat Gateways & Spot ETFs vs. Offshore Perp/USDT Flows
- [`MOD 08`](rulebook/MOD_08_Rough_Path_Signatures_I_Price_Volume_Levy_Signed_Area.md) — Rough Path Signatures I: Price-Volume Lévy Signed Area
- [`MOD 09`](rulebook/MOD_09_Rough_Path_Signatures_II_Spot_CVD_Open_Interest_Levy_Signed_Area.md) — Rough Path Signatures II: Spot CVD–Open Interest Lévy Signed Area
- [`MOD 10`](rulebook/MOD_10_Rough_Path_Signatures_III_Multi_Horizon_Alignment.md) — Rough Path Signatures III: Multi-Horizon Alignment
- [`MOD 11`](rulebook/MOD_11_Volume_Profile_Structural_Topology.md) — Volume Profile Structural Topology (VAH, VAL, POC & LVN)
- [`MOD 12`](rulebook/MOD_12_Garman_Klass_Volatility_Squeeze_And_Fan_Expansion.md) — Garman-Klass (OHLC) Volatility Squeeze & Fan Expansion
- [`MOD 13`](rulebook/MOD_13_Short_Term_Holder_Realized_Price_And_MVRV_Bands.md) — Short-Term Holder (STH) Realized Price & MVRV Bands
- [`MOD 14`](rulebook/MOD_14_SOPR_Profit_Loss_Reset_Cycles.md) — SOPR Profit/Loss Reset Cycles
- [`MOD 15`](rulebook/MOD_15_Realized_Cap_Impulse_And_LTH_To_STH_Wealth_Transfer.md) — Realized Cap Impulse & LTH-to-STH Wealth Transfer
- [`MOD 16`](rulebook/MOD_16_Macro_Liquidity_Sovereign_Yields_DXY_And_Stablecoin_Dry_Powder.md) — Macro Liquidity, Sovereign Yields, DXY & Stablecoin Dry Powder
- [`MOD 17`](rulebook/MOD_17_200D_MA_Secular_Gates_Index_Rebalancings_and_Session_Handoffs.md) — 200D MA Secular Gates, Index Rebalancings & Session Handoffs
- [`MOD 18`](rulebook/MOD_18_Master_5_Pillar_Confluence_0.75_Risk_Sizing_Engine_And_Two_Stage_Exit_Protocol.md) — Master 5-Pillar Confluence, 0.75% Risk Sizing & Exit Protocol
- [`MOD 19`](rulebook/MOD_19_Coinbase_Premium_Index_Z_Scores_And_Domestic_Offshore_Spreads.md) — Coinbase Premium Index Z-Scores & Domestic-Offshore Spreads
- [`MOD 20`](rulebook/MOD_20_CME_Futures_Basis_And_Weekend_Gap_Fill_Topology.md) — CME Futures Basis & Weekend Gap Fill Topology
- [`MOD 21`](rulebook/MOD_21_Algorithmic_TWAP_VWAP_Accumulation_Footprints_vs_Spoofed_Liquidity.md) — Algorithmic TWAP/VWAP Accumulation vs. Spoofed Liquidity
- [`MOD 22`](rulebook/MOD_22_Net_Fed_Liquidity_Impulse.md) — Net Fed Liquidity Impulse (`Fed Balance Sheet - TGA - RRP`)
- [`MOD 23`](rulebook/MOD_23_MOVE_Index_And_High_Yield_Credit_Spread_Breakers.md) — MOVE Index & High-Yield Credit Spread Breakers
- [`MOD 24`](rulebook/MOD_24_USD_JPY_Sovereign_Carry_Trade_Unwind_And_BOJ_Intervention_Alerts.md) — USD/JPY Sovereign Carry-Trade Unwind & BOJ Intervention Alerts
- [`MOD 25`](rulebook/MOD_25_Dealer_Gamma_Exposure_And_Zero_Gamma_Flip_Mechanics.md) — Dealer Gamma Exposure (GEX) & Zero-Gamma Flip Mechanics
- [`MOD 26`](rulebook/MOD_26_Deribit_And_CME_Monthly_Quarterly_OPEX_Max_Pain_Gravity.md) — Deribit & CME Monthly/Quarterly OpEx Max Pain Gravity
- [`MOD 27`](rulebook/MOD_27_25_Delta_Implied_Volatility_Skew_And_DVOL_Term_Structure_Extremes.md) — 25-Delta Implied Volatility Skew & DVOL Term Structure Extremes
- [`MOD 28`](rulebook/MOD_28_Live_Autopsy_And_Black_Swan_Circuit_Breaker_Engine.md) — Live Autopsy & Black Swan Circuit Breaker Engine
- [`MOD 29`](rulebook/MOD_29_Equity_Multiple_Compression_Energy_Shocks_And_High_Beta_Contagion.md) — Equity Multiple Compression, Energy Shocks & High-Beta Contagion
- [`MOD 30`](rulebook/MOD_30_PCF3_Order_Flow_Engine_And_10_Deterministic_Configurations.md) — PCF3 Order Flow Engine & 10 Deterministic Configurations
- [`MOD 31`](rulebook/MOD_31_Institutional_Capital_Defense_Matrix.md) — Institutional Capital Defense Matrix (ICDM 100-Pt Fragility Scale)
- [`MOD 32`](rulebook/MOD_32_Exchange_Solvency_Multiplier_And_Sovereign_Multi_Sig_Custody_Architecture.md) — Exchange Solvency Multiplier & Sovereign Multi-Sig Custody
- [`MOD 33`](rulebook/MOD_33_Unified_5_Regime_Master_Radar_And_State_Transition_Engine.md) — Unified 5-Regime Master Radar & State-Transition Engine
- [`MOD 34`](rulebook/MOD_34_AEGIS_3_Impulse_Defense_and_Anti_Capitulation_Shield.md) — AEGIS-3: 3-Stage Impulse Defense & Anti-Capitulation Shield
- [`MOD 35`](rulebook/MOD_35_Liquidation_Heatmap_Distance_Rule_And_Pull_Score_Engine.md) — Liquidation Heatmap Distance Rule & Pull Score Engine
- [`MOD 36`](rulebook/MOD_36_Telemetry_Trust_Staleness_SLA_And_Determinism_Attestation.md) — Telemetry Trust, Staleness SLA & Determinism Attestation
- [`MOD 37`](rulebook/MOD_37_Executable_Liquidity_Net_3.0R_Slippage_and_Equity_Curve_Governor.md) — Executable Liquidity, Net-3.0R Slippage & Equity-Curve Governor
- [`MOD 38`](rulebook/MOD_38_ETF_Primary_Market_Settlement_And_BRRNY_Fix_Window_Engine.md) — ETF Primary-Market Settlement & BRRNY Fix-Window Engine
- [`MOD 39`](rulebook/MOD_39_Exchange_Supply_Activation_And_Aged_UTXO_Dormancy_Engine.md) — Exchange Supply Activation & Aged-UTXO Dormancy Engine
- [`MOD 40`](rulebook/MOD_40_Miner_Treasury_Stress_And_Hashprice_Economics_Engine.md) — Miner Treasury Stress & Hashprice Economics Engine
- [`MOD 41`](rulebook/MOD_41_Secular_Cycle_ATH_Cluster_and_Double_Top_Exit_Engine.md) — Secular Cycle ATH Cluster, First-Week Flush & Flat Double-Top (`+4%`) Exit Engine
- [`MOD 41.1`](rulebook/MOD_41.1_Secular_ATH_Operational_Field_Runbook_and_Countdown_Checklist.md) — Secular ATH Operational Field Runbook & 10-Day Countdown Checklist
- [`MOD 42`](rulebook/MOD_42_Classical_Structural_Shapes_and_Liquidity_Pool_Authentication.md) — Classical Structural Shapes & Liquidity-Pool Authentication Engine
- [`MOD 43`](rulebook/MOD_43_Algorithmic_Fibonacci_Confluence_and_Harmonic_Impulse_Measurement.md) — Algorithmic Fibonacci Confluence & Harmonic Impulse Measurement
- [`MOD 44`](rulebook/MOD_44_Mega_IPO_Capital_Vacuums_and_Index_Rebalance_Liquidity_Drains.md) — Mega-IPO Capital Vacuums & Index Rebalance Liquidity Drains
- [`MOD 45`](rulebook/MOD_45_Executive_Bottom_Line_HUD_and_Mobile_Presentation_Protocol.md) — Executive Bottom-Line HUD & Mobile Presentation Protocol
- [`MOD 46`](rulebook/MOD_46_Block_1050000_April_2028_Secular_Horizon_and_Sovereign_Barbell_Anchor.md) — Block 1,050,000 (April 2028) Secular Horizon & Sovereign Barbell Anchor

</details>
