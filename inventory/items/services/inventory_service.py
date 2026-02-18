from django.db import IntegrityError, transaction
from django.db.models import F

from items.domain.models import Item


def create_item(name: str, qty: int, user_id: str) -> Item:
    """
    Create an item owned by user_id.

    Uniqueness is enforced by the DB constraint (e.g., unique per user on (owner, name)).
    """
    try:
        with transaction.atomic():
            item = Item(name=name, qty=qty, owner=user_id)
            item.save()
            return item
    except IntegrityError:
        raise ValueError("item with that name already exists")


def delete_item(item_id: str, user_id: str) -> None:
    """
    Delete is ownership-bound:
    - If owned row deleted -> OK (idempotent-ish for owner: repeated deletes become not found)
    - If item exists but not owned -> forbidden
    - If item doesn't exist -> not found
    """
    with transaction.atomic():
        deleted_count, _ = Item.objects.filter(item_id=item_id, owner=user_id).delete()

    if deleted_count > 0:
        return

    exists_any = Item.objects.filter(itme_id=item_id).exists()
    if exists_any:
        raise PermissionError("forbidden")

    raise ValueError("item not found")


def update_qty(item_id: str, delta: int, user_id: str):
    """
    Ownership-bound atomic qty update.

    Returns:
      - Item on success
      - None if item_id does not exist

    Raises:
      - PermissionError("forbidden") if item exists but not owned by user_id
      - ValueError("delta must be an int") if delta is invalid type
      - ValueError("qty cannot go below 0") if update would violate qty >= 0
    """
    if not item_id:
        return None

    if isinstance(delta, bool) or not isinstance(delta, int):
        raise ValueError("delta must be an int")

    with transaction.atomic():
        updated = (
            Item.objects
            .filter(item_id=item_id, owner=user_id, qty__gte=-delta)
            .update(qty=F("qty") + delta)
        )

        if updated:
            return Item.objects.get(item_id=item_id, owner=user_id)

        # Disambiguate failure: missing vs forbidden vs invariant violation
        if not Item.objects.filter(item_id=item_id).exists():
            return None

        if not Item.objects.filter(item_id=item_id, owner=user_id).exists():
            raise PermissionError("forbidden")

        raise ValueError("qty cannot go below 0")
