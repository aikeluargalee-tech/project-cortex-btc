"""
Phase 5 Verification Suite — Unified Command Centre Service & HTTP Server.
"""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from cortex_core.constants import NOT_CONFIGURED, UNVALIDATED, PortfolioState, Verdict
from cortex_core.dashboard_service import DashboardService
from cortex_dashboard import create_server


def _http_get(url: str) -> tuple[int, bytes]:
    with urllib.request.urlopen(url, timeout=5) as resp:
        return resp.status, resp.read()


def _http_post(url: str, payload: dict) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


def test_dashboard_service_initial_unconfigured_state_and_exports(tmp_path: Path) -> None:
    metrics_path = tmp_path / "metrics.json"
    metrics_path.write_text(
        json.dumps(
            {
                "as_of_utc": "2026-11-17T02:00:00Z",
                "spot_price": 65000.0,
                "venues": {"binance": {"price": 65000.0, "timestamp_utc": "2026-11-17T01:59:55Z"}},
                "price": {
                    "spot": 65000.0,
                    "sma50": 64000.0,
                    "sma200": 62000.0,
                    "rsi14": 48.0,
                    "range_high_45d": 70000.0,
                    "range_low_45d": 60000.0,
                },
            }
        ),
        encoding="utf-8",
    )
    svc = DashboardService(metrics_path=metrics_path, data_dir=tmp_path / "data")
    state = svc.get_command_centre_state(now_utc="2026-11-17T02:01:00Z")

    assert state["banner"]["validation_status"] == UNVALIDATED
    assert state["banner"]["instrument"] == "BTC/USDT SPOT ONLY"
    assert state["banner"]["market_ts_myt"].endswith("MYT (UTC+8)")
    assert state["portfolio_display"]["btc_total"] == NOT_CONFIGURED
    assert state["decision"]["final_verdict"] == Verdict.ABSTAIN.value
    assert state["decision"]["new_operating_state"] == PortfolioState.HUMAN_REVIEW.value

    csv_bytes, ctype_csv, _ = svc.export_audit_bytes("csv")
    json_bytes, ctype_json, _ = svc.export_audit_bytes("json")
    assert "text/csv" in ctype_csv and b"DECISION_RECORDED" in csv_bytes
    assert "application/json" in ctype_json and len(json.loads(json_bytes.decode("utf-8"))) >= 1


def test_dashboard_http_server_end_to_end(tmp_path: Path) -> None:
    metrics_path = tmp_path / "metrics.json"
    metrics_path.write_text(
        json.dumps(
            {
                "as_of_utc": "2026-11-17T02:00:00Z",
                "spot_price": 65000.0,
                "venues": {"binance": {"price": 65000.0, "timestamp_utc": "2026-11-17T01:59:55Z"}},
                "price": {
                    "spot": 65000.0,
                    "sma50": 64000.0,
                    "sma200": 62000.0,
                    "rsi14": 48.0,
                    "range_high_45d": 70000.0,
                    "range_low_45d": 60000.0,
                },
                "liquidity": {"spread_bps": 0.5, "depth_1pct_usd": 10000000.0},
                "order_flow": {"spot_cvd_binance": {"24h": {"cvd_btc": 250.0}}},
            }
        ),
        encoding="utf-8",
    )

    server = create_server(host="127.0.0.1", port=0, metrics_path=metrics_path, data_dir=tmp_path / "data")
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"

    try:
        # 1. HTML Command Centre loads
        st, html_bytes = _http_get(f"{base}/")
        assert st == 200
        html = html_bytes.decode("utf-8")
        assert "CORTEX-BTC" in html
        assert "1. Command Centre" in html

        # 2. Configure balances via HTTP
        st, bal = _http_post(
            f"{base}/api/portfolio/configure",
            {
                "btc_core_protected": 0.80,
                "btc_tactical": 0.10,
                "usdt_tactical": 5000.0,
                "operator_id": "op_http",
                "reason": "Manual HTTP balance verification",
            },
        )
        assert st == 200
        assert bal["btc_total"] == 0.90
        assert bal["btc_core_protected"] == 0.80

        # 3. Forbidden invariant update returns HTTP 400
        st, err = _http_post(
            f"{base}/api/config/update",
            {
                "updates": {"invariants": {"leverage_allowed": True}},
                "operator_id": "op_http",
                "change_reason": "Forbidden",
                "operator_acknowledged": True,
            },
        )
        assert st == 400
        assert "non-negotiable invariant" in err["error"]

        # 4. Valid config update succeeds
        st, cfg_res = _http_post(
            f"{base}/api/config/update",
            {
                "updates": {
                    "portfolio_policy": {"active_tactical_sleeve_pct": 20.0, "portfolio_risk_budget_pct": 0.75},
                    "execution_assumptions": {"maker_fee_bps": 10.0, "expected_slippage_bps": 5.0},
                },
                "operator_id": "op_http",
                "change_reason": "Configure fees & sleeve",
                "operator_acknowledged": True,
            },
        )
        assert st == 200
        assert cfg_res["config_version"] == 2

        # 5. Open a Loop A cycle and export CSV/JSON
        st, cyc = _http_post(
            f"{base}/api/cycles/open",
            {"loop": "LOOP_A", "starting_qty": 2500.0, "original_setup_ref": "HTTP_TEST"},
        )
        assert st == 200
        assert cyc["loop"] == "LOOP_A"

        st_csv, csv_data = _http_get(f"{base}/api/export/csv")
        st_json, json_data = _http_get(f"{base}/api/export/json")
        assert st_csv == 200 and b"CONVERSION_CYCLE_OPENED" in csv_data
        assert st_json == 200 and len(json.loads(json_data.decode("utf-8"))) >= 2
    finally:
        server.shutdown()
        server.server_close()
