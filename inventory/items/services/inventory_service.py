from __future__ import annotations

from items.domain.errors import DuplicateNameError, InvariantError
from items.domain.invariants import ensure_unique_name, validate_name, validate_qty
from items.domain.models import ItemModel
from items.repo.item_repo import Repo
from items.shared.result import Err, Ok, Result


class InventoryService:
    def __init__(self, repo: Repo) -> None:
        self._repo = repo

    def create_item(self, name: str, qty: int) -> Result[ItemModel]:
        try:
            normalized_name = validate_name(name)
            validated_qty = validate_qty(qty)

            existing_normalized_names = {
                item.name for item in self._repo.list().values()
            }
            ensure_unique_name(normalized_name, existing_normalized_names)

        except (InvariantError, DuplicateNameError) as e:
            return Err(e)

        item = self._repo.create(name=normalized_name, qty=validated_qty)

        return Ok(item)

    def delete_item(self, item_id: str) -> None:
        self._repo.delete(item_id)
