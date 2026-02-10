from django.db.models import F
from django.db import transaction, IntegrityError
from items.domain.models import Item

def create_item(name: str, qty: int) -> Item:
    try:
        with transaction.atomic():
            item = Item(name=name, qty=qty)
            item.save()
            return item

    except IntegrityError:
        raise ValueError("item with that name already exists")


def delete_item(item_id: str) -> None:
    with transaction.atomic():
        item = Item.objects.filter(id=item_id)
        item.delete() 


# state = S' = S - {item_id -> Item} 
# invariant = idempotent 
# transition = delete(item_id) -> None:
                # 

def update_qty(item_id: int, delta: int) -> None:
    if not isinstance(delta, int):
        raise ValueError("delta must be an int")
    

    updated = (
        Item.objects
        .filter(id=item_id, qty__gte= - delta)
        .update(qty=F("qty") + delta)
    )
   
    if updated:
        return
    
    if not Item.objects.filter(id=item_id).exists():
        raise ValueError("No item found")

    raise ValueError("qty must not be below 0")