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
