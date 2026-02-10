from django.db.models import F
from django.db import transaction, IntegrityError
from items.domain.models import Item
import uuid


def create_item(name:str, qty:int) -> Item:
    try:
        with transaction.atomic():
            item = Item(name=name, qty=qty)
            item.save()
            return item

    except IntegrityError:
        raise ValueError("item with that name already exists")


def delete_item(item_id:str) -> None:
    with transaction.atomic():
        Item.objects.filter(id=item_id).delete()


def update_qty(item_id:str, delta:int) -> None:
    if item_id is None:
        return
    
    if isinstance(delta, bool) or not isinstance(delta, int):
        raise ValueError("delta must be an int")

    with transaction.atomic():
        updated = (
            Item.objects
            .filter(id=item_id, qty__gte=-delta)
            .update(qty=F("qty") + delta)
        )

        if updated:
            return Item.objects.get(id=item_id)

        exists = Item.objects.filter(id=item_id).exists()

        if not exists:
            return 

        raise ValueError("qty cannot go below 0")
