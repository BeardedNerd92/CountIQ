from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any


SERVICE_NAME = os.getenv("SERVICE_NAME", "countiq-api")
ENV = os.getenv("ENV", "dev")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # 1) Base envelope (stable keys)
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": SERVICE_NAME,
            "env": ENV,
        }

        # 2) Optional structured extras (safe enrichment)
        # If you pass extra={"event": "...", "request_id": "..."} they appear here.
        for key in ("event", "request_id", "method", "path", "status_code", "latency_ms",
                    "actor_id", "item_id", "mutation", "outcome", "error_code", "detail"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)

        # 3) Exception details (structured, still one JSON line)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
