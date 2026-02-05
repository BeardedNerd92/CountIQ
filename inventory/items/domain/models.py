from dataclasses import dataclass

@dataclass(frozen=True)
class ItemModel:
    id: int
    name: str
    qty: int