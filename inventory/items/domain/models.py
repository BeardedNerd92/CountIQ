import uuid
from django.db import models
from .invariants import normalize_and_validate_item


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    qty = models.IntegerField()

    def clean(self):
        canonical = normalize_and_validate_item({
            "name": self.name,
            "qty": self.qty,
        })

        self.name = canonical["name"]
        self.qty = canonical["qty"]

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
