import uuid
from django.db import models
from .invariants import normalize_and_validate_item


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)

    qty = models.IntegerField()

    owner_id = models.CharField(max_length=64, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner_id", "name"],
                name="uniq_item_name_per_user",
            )
        ]

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
