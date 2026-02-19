from __future__ import annotations


class Invariants:
    """
    Central validation authority for the client script.
    Pure validation only. No I/O. No side effects.
    """

    # ---------- generic ----------

    def require_non_empty_str(self, value: object, *, field: str) -> str:
        ...

    def require_non_negative_int(self, value: object, *, field: str) -> int:
        ...


    # ---------- auth ----------

    def require_authenticated(self, is_authenticated: bool) -> None:
        ...


    # ---------- state ----------

    def validate_state(self, counter: int, menu: dict) -> None:
        ...


    # ---------- patch-specific ----------

    def require_valid_delta(self, value: object, *, field: str = "delta") -> int:
        ...

    def require_valid_name(self, value: object, *, field: str = "name") -> str:
        ...
