#!/usr/bin/env python3
"""
CORTEX-BTC Unified Command Centre HTTP Server (Phase 5).

Zero-dependency Python 3 stdlib ThreadingHTTPServer serving the single-screen
CORTEX-BTC Command Centre and manual execution / configuration endpoints.

Usage:
  python cortex_dashboard.py --port 8501
"""

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from cortex_core.dashboard_service import DashboardService
from cortex_core.dashboard_ui import DASHBOARD_HTML


def make_handler(service: DashboardService) -> type[BaseHTTPRequestHandler]:
    """Create HTTP handler bound to a DashboardService instance."""

    class CortexHandler(BaseHTTPRequestHandler):
        def _send_json(self, status: int, payload: Any) -> None:
            body = json.dumps(payload, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_json_body(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0:
                return {}
            raw = self.rfile.read(length).decode("utf-8")
            data = json.loads(raw)
            if not isinstance(data, dict):
                raise ValueError("Request body must be a JSON object.")
            return data

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path in {"/", "/index.html"}:
                body = DASHBOARD_HTML.encode("utf-8")
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            if parsed.path == "/api/state":
                qs = parse_qs(parsed.query)
                propose = qs.get("propose", ["0"])[0] == "1"
                try:
                    state = service.get_command_centre_state(create_proposed_order=propose)
                    self._send_json(HTTPStatus.OK, state)
                except Exception as exc:
                    self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
                return

            if parsed.path in {"/api/export/csv", "/api/export/json"}:
                fmt = "csv" if parsed.path.endswith("csv") else "json"
                try:
                    content, ctype, fname = service.export_audit_bytes(fmt)
                    self.send_response(HTTPStatus.OK)
                    self.send_header("Content-Type", ctype)
                    self.send_header("Content-Disposition", f'attachment; filename="{fname}"')
                    self.send_header("Content-Length", str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                except Exception as exc:
                    self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
                return

            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            try:
                payload = self._read_json_body()
                if parsed.path == "/api/portfolio/configure":
                    res = service.configure_balances(payload)
                elif parsed.path == "/api/portfolio/reconcile":
                    res = service.reconcile_balances(payload)
                elif parsed.path == "/api/portfolio/core-mandate":
                    res = service.update_core_mandate(payload)
                elif parsed.path == "/api/config/update":
                    res = service.update_configuration(payload)
                elif parsed.path == "/api/orders/action":
                    res = service.handle_order_action(payload)
                elif parsed.path == "/api/cycles/open":
                    res = service.open_cycle(payload)
                else:
                    self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
                    return
                self._send_json(HTTPStatus.OK, res)
            except Exception as exc:
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            return

    return CortexHandler


def create_server(
    *,
    host: str = "127.0.0.1",
    port: int = 8501,
    metrics_path: Path = Path("btc_metrics_latest.json"),
    data_dir: Path = Path("data"),
) -> ThreadingHTTPServer:
    service = DashboardService(metrics_path=metrics_path, data_dir=data_dir)
    handler = make_handler(service)
    return ThreadingHTTPServer((host, port), handler)


def main() -> int:
    parser = argparse.ArgumentParser(description="CORTEX-BTC Unified Command Centre Dashboard")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8501)
    parser.add_argument("--metrics", type=Path, default=Path("btc_metrics_latest.json"))
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    args = parser.parse_args()

    server = create_server(
        host=args.host,
        port=args.port,
        metrics_path=args.metrics,
        data_dir=args.data_dir,
    )
    print(f"CORTEX-BTC Command Centre running at http://{args.host}:{args.port} (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
