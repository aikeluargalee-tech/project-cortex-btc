"""Tests for static GitHub Pages read-only market viewer exporter."""

from __future__ import annotations

import json
from pathlib import Path

from cortex_core.constants import UNVALIDATED
from export_github_pages import export_pages


def test_export_pages_generates_read_only_market_view_without_balances(tmp_path: Path) -> None:
    metrics_path = tmp_path / "metrics.json"
    verdict_path = tmp_path / "verdict.json"
    out_dir = tmp_path / "docs"

    metrics_path.write_text(
        json.dumps(
            {
                "as_of_utc": "2026-11-17T02:00:00Z",
                "spot_price": 64900.0,
                "venues": {"binance": {"price": 64900.0, "timestamp_utc": "2026-11-17T01:59:55Z"}},
                "price": {
                    "spot": 64900.0,
                    "sma50": 79000.0,
                    "sma200": 72900.0,
                    "rsi14": 24.0,
                    "range_high_45d": 87000.0,
                    "range_low_45d": 62000.0,
                },
            }
        ),
        encoding="utf-8",
    )
    verdict_path.write_text(
        json.dumps(
            {
                "compiled_at_myt": "2026-11-17 10:00:00 MYT",
                "summary": {
                    "verdict_action": "LOCKED_HALT",
                    "regime_id": "R5_CAPITULATION_CRISIS",
                    "icdm_score": 45.0,
                    "net_r": 2.8,
                },
                "canonical_telemetry": {"price_change_pct_24h": 0.34},
            }
        ),
        encoding="utf-8",
    )

    html_path, json_path = export_pages(
        metrics_path=metrics_path,
        verdict_path=verdict_path,
        output_dir=out_dir,
    )
    assert html_path.exists() and json_path.exists()

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["banner"]["validation_status"] == UNVALIDATED
    assert payload["banner"]["instrument"] == "BTC/USDT SPOT ONLY"
    assert payload["banner"]["market_ts_myt"].endswith("MYT (UTC+8)")
    assert payload["legacy_matrix_summary"]["verdict_action"] == "LOCKED_HALT"
    assert "btc_core_protected" not in payload
    assert "usdt_tactical" not in payload

    html = html_path.read_text(encoding="utf-8")
    assert "CORTEX-BTC // Public Market Viewer" in html
    assert "./market_state.json" in html
