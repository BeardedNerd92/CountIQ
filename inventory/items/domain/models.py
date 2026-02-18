import uuid
from django.db import models
from django.conf import settings
from items.domain.invariants import normalize_and_validate_item, normailize_and_validate_user




class User(models.Model):
    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )

    username = models.CharField(
        max_length=255
        )

    is_active = models.BooleanField(
        editable=False, 
        null=False
        )

    created_at = models.DateTimeField(
        editable=False, 
        null=False
        )

    updated_at = models.DateTimeField(
        editable=False, 
        null=False
        )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username'], 
                name='unique_username',
                )
        ]


    def clean_user(self):
        canonical = normailize_and_validate_user({
            ...
        })
        ...
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
    ...




class Token(models.Model):
    token_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
        )

    token_hash = models.CharField(
        max_length=255, 
        editable=False, 
        null=False
        )

    expires_at = models.DateTimeField(
        editable=False, 
        null=False
        )

    revoked_at = models.DateTimeField(
        editable=True, 
        null=True
        )

    created_at = models.DateTimeField(
        editable=False, 
        null=False
        )

    last_used = models.DateTimeField(
        editable=True, 
        null=True
        )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'token_hash'], 
                name='unique_user_id_token_hash',
                )
        ]



    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
    ...




class Item(models.Model):
    item_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )

    name = models.CharField(
        max_length=255
        )

    qty = models.IntegerField()

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        editable=False, 
        null=False
        )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'name'], 
                name='unique_owner_name',
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