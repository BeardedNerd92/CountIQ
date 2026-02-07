from __future__ import annotations

from items.domain.errors import DuplicateNameError, InvariantError


def normalize_name(name: str) -> str:
    if not isinstance(name, str):
        raise InvariantError("name must be a string")
    return name.strip().casefold()


def validate_name(name: str) -> str:
    normalized = normalize_name(name)
    if normalized == "":
        raise InvariantError("name must be a non-empty string")
    return normalized


def validate_qty(qty: int) -> int:
    if not isinstance(qty, int):
        raise InvariantError("qty must be an integer")
    if qty < 0:
        raise InvariantError("qty must be a non-negative integer")
    return qty


def ensure_unique_name(normalized_name: str, existing_normalized_names: set[str]) -> None:
    if normalized_name in existing_normalized_names:
        raise DuplicateNameError(f"name already exists: {normalized_name}")
