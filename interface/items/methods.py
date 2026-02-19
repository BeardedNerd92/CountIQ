from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from user import User
from .curl import CurlClient


@dataclass
class ItemMethods:
    """
    API interaction layer.

    Responsible only for:
    - calling HTTP endpoints
    - delegating to CurlClient

    Not responsible for:
    - validation
    - authentication enforcement
    - user input
    """

    client: CurlClient

    # ---------- READ ----------

    def read_items(self, *, user: User) -> Any:
        """
        GET /items
        """
        ...

    def read_item(self, *, user: User, item_id: str) -> Any:
        """
        GET /items/{id}
        """
        ...

    # ---------- CREATE ----------

    def create_item(self, *, user: User, name: str, qty: int) -> Any:
        """
        POST /items
        """
        ...

    # ---------- DELETE ----------

    def delete_item(self, *, user: User, item_id: str) -> Any:
        """
        DELETE /items/{id}
        """
        ...

    # ---------- PATCH ----------

    def patch_qty(self, *, user: User, item_id: str, delta: int) -> Any:
        """
        PATCH /items/{id} → qty update
        """
        ...

    def patch_name(self, *, user: User, item_id: str, name: str) -> Any:
        """
        PATCH /items/{id} → name update
        """
        ...
