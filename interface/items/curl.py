from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CurlClient:
    """
    Single responsibility:
    Build and execute HTTP/curl requests.

    No invariants.
    No state mutation.
    No business logic.
    """

    base_url: str
    timeout: int = 15

    # ---------- internal helpers ----------

    def _build_url(self, path: str) -> str:
        ...

    def _headers(self, token: str) -> Dict[str, str]:
        ...

    def _run(self, args: list[str]) -> Any:
        ...

    # ---------- public request methods ----------

    def get(self, *, path: str, token: str) -> Any:
        ...

    def post(
        self,
        *,
        path: str,
        token: str,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> Any:
        ...

    def delete(self, *, path: str, token: str) -> Any:
        ...

    def patch(
        self,
        *,
        path: str,
        token: str,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> Any:
        ...
