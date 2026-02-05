import pytest

from items.domain.errors import DuplicateNameError, InvariantError
from items.domain.invariants import ensure_unique_name, validate_name, validate_qty


def test_validate_name_trims_and_casefolds():
    assert validate_name(" Milk ") == "milk"


def test_validate_name_rejects_empty():
    with pytest.raises(InvariantError):
        validate_name(" ")


def test_validate_qty_rejects_negative():
    with pytest.raises(InvariantError):
        validate_qty(-1)


def test_ensure_unique_name_raises_on_duplicate():
    with pytest.raises(DuplicateNameError):
        ensure_unique_name("milk", {"milk"})
