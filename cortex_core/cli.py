"""Phase 1 CLI status reporter for CORTEX-BTC Foundation & Portfolio Ledger."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from btc_config_loader import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_CONFIG_HISTORY_PATH,
    initialize_default_config,
    load_config,
)
from cortex_core.constants import DATA_UNAVAILABLE
from cortex_core.ledger import PortfolioLedger
from cortex_core.market_data import build_market_snapshot
from cortex_core.time_utils import format_myt


def build_phase1_status_report(
    *,
    metrics_path: Path = Path("btc_metrics_latest.json"),
    config_path: Path = DEFAULT_CONFIG_PATH,
    history_path: Path = DEFAULT_CONFIG_HISTORY_PATH,
    ledger_path: Path = Path("data/portfolio_ledger.json"),
) -> dict[str, Any]:
    """Assemble a non-destructive Phase 1 status report without inventing missing inputs."""
    cfg = (
        load_config(config_path)
        if config_path.exists()
        else initialize_default_config(config_path, history_path)
    )
    raw_metrics: dict[str, Any] = {}
    if metrics_path.exists():
        raw_metrics = json.loads(metrics_path.read_text(encoding="utf-8"))

    mkt = build_market_snapshot(raw_metrics, config=cfg)
    ledger = PortfolioLedger(state_path=ledger_path)
    prt = ledger.snapshot(spot_price=mkt.spot_price, config_version=cfg.config_version)

    return {
        "operating_mode": cfg.operating_mode.value,
        "validation_status": cfg.validation_status,
        "instrument": cfg.instrument,
        "spot_only": cfg.spot_only,
        "autonomous_execution": cfg.autonomous_execution,
        "config_version": cfg.config_version,
        "market_snapshot": {
            "snapshot_id": mkt.snapshot_id,
            "spot_price_usdt": mkt.spot_price if mkt.spot_price is not None else DATA_UNAVAILABLE,
            "source_event_ts_utc": mkt.source_event_ts_utc,
            "source_event_ts_myt": format_myt(mkt.source_event_ts_utc),
            "retrieved_ts_utc": mkt.retrieved_ts_utc,
            "retrieved_ts_myt": format_myt(mkt.retrieved_ts_utc),
            "overall_integrity_status": mkt.overall_integrity_status.value,
            "missing_or_unavailable_fields": mkt.missing_or_unavailable_fields,
            "proxy_fields": mkt.proxy_fields,
            "stale_fields": mkt.stale_fields,
        },
        "portfolio_snapshot": {
            "portfolio_snapshot_id": prt.portfolio_snapshot_id,
            "configured": prt.configured,
            "reconciliation_status": prt.reconciliation_status.value,
            "btc_total": prt.display_field("btc_total"),
            "btc_core_protected": prt.display_field("btc_core_protected"),
            "btc_tactical": prt.display_field("btc_tactical"),
            "btc_reserved": prt.display_field("btc_reserved"),
            "usdt_total": prt.display_field("usdt_total"),
            "usdt_tactical": prt.display_field("usdt_tactical"),
            "usdt_reserved": prt.display_field("usdt_reserved"),
        },
    }


def main() -> int:
    report = build_phase1_status_report()
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
