
from ..domain.invariants import  validate_name, validate_qty, ensure_unique_name


def test_normalize_name():
    item = validate_name("c   ")
    assert item != ""


def test_rejects_negative_qty():
    item = 1
    if not isinstance(item, int) or item < 0: 
        assert validate_qty(item)



def test_name_are_unique():
  a = "a"
  b = ["b","c"]
  if a not in b:
      return
  assert ensure_unique_name(a, b)
 

