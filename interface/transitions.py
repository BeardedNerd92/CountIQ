Here’s the **contract (signatures only)** for `transitions.py`, matching your rules:

* **mutations only** (create/delete/patch) live here
* **auth gate** happens here (don’t rely on the API methods class to do it)
* **value-first invariants** are called here (or delegated, but this is the orchestrator)
* **no I/O** (no `input()`, no `print()`)
from __future__ import annotations

from dataclasses import dataclass

from invariants import Invariants
from user import User
from items.api_methods import CountIQApi


@dataclass
class Transitions:
    """
    Orchestrates allowed state transitions (mutations) for the client.
    Enforces auth + invariant checks before delegating to API methods.
    No I/O. No persistence. No business logic beyond gating + validation.
    """

    api: CountIQApi
    inv: Invariants

    def create_item(self, *, user: User, name: str, qty: int) -> None:
        ...

    def delete_item(self, *, user: User, item_id: str) -> None:
        ...

    def patch_qty(self, *, user: User, item_id: str, delta: int) -> None:
        ...

    def patch_name(self, *, user: User, item_id: str, name: str) -> None:
        ...