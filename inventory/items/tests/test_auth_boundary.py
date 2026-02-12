import uuid
from django.test import TestCase

from items.domain.models import Item
from items.services.inventory_service import create_item, delete_item, update_qty


class TestInventoryService(TestCase):
    # ----------------------------
    # create_item (service layer)
    # ----------------------------

    def test_create_item_sets_owner_id_and_persists(self):
        # Arrange
        user_id = "user-a"

        # Act
        item = create_item(name="milk", qty=2, user_id=user_id)

        # Assert
        self.assertEqual(item.name, "milk")
        self.assertEqual(item.qty, 2)
        self.assertEqual(item.owner_id, user_id)
        self.assertTrue(Item.objects.filter(id=item.id).exists())

    def test_create_item_duplicate_name_same_user_raises_value_error(self):
        # Arrange
        user_id = "user-a"
        create_item(name="milk", qty=1, user_id=user_id)

        # Act + Assert
        with self.assertRaises(ValueError) as ctx:
            create_item(name="milk", qty=2, user_id=user_id)

        self.assertEqual(str(ctx.exception), "item with that name already exists")

        # State unchanged: still only one "milk" for that user
        self.assertEqual(Item.objects.filter(owner_id=user_id, name="milk").count(), 1)

    def test_create_item_same_name_different_users_allowed(self):
        # This assumes the DB constraint is UNIQUE(owner_id, name) (per-user uniqueness)
        user_a = "user-a"
        user_b = "user-b"

        a = create_item(name="milk", qty=1, user_id=user_a)
        b = create_item(name="milk", qty=2, user_id=user_b)

        self.assertNotEqual(a.owner_id, b.owner_id)
        self.assertEqual(Item.objects.filter(name="milk").count(), 2)

    # ----------------------------
    # delete_item (service layer)
    # ----------------------------

    def test_delete_item_owner_can_delete(self):
        # Arrange
        user_id = "user-a"
        item = create_item(name="milk", qty=2, user_id=user_id)

        # Act
        delete_item(str(item.id), user_id)

        # Assert
        self.assertFalse(Item.objects.filter(id=item.id).exists())

    def test_delete_item_non_owner_forbidden_and_state_unchanged(self):
        # Arrange
        owner_id = "user-a"
        other_id = "user-b"
        item = create_item(name="milk", qty=2, user_id=owner_id)

        # Act + Assert
        with self.assertRaises(PermissionError) as ctx:
            delete_item(str(item.id), other_id)

        self.assertEqual(str(ctx.exception), "forbidden")
        self.assertTrue(Item.objects.filter(id=item.id).exists())

    def test_delete_item_missing_raises_value_error(self):
        # Arrange
        user_id = "user-a"
        missing_id = str(uuid.uuid4())

        # Act + Assert
        with self.assertRaises(ValueError) as ctx:
            delete_item(missing_id, user_id)

        self.assertEqual(str(ctx.exception), "item not found")

    # ----------------------------
    # update_qty (service layer)
    # ----------------------------

    def test_update_qty_owner_can_increment(self):
        # Arrange
        user_id = "user-a"
        item = create_item(name="milk", qty=2, user_id=user_id)

        # Act
        updated = update_qty(str(item.id), 3, user_id)

        # Assert
        self.assertIsNotNone(updated)
        self.assertEqual(updated.qty, 5)

        item.refresh_from_db()
        self.assertEqual(item.qty, 5)

    def test_update_qty_owner_can_decrement_to_zero(self):
        # Arrange
        user_id = "user-a"
        item = create_item(name="milk", qty=2, user_id=user_id)

        # Act
        updated = update_qty(str(item.id), -2, user_id)

        # Assert
        self.assertIsNotNone(updated)
        self.assertEqual(updated.qty, 0)

        item.refresh_from_db()
        self.assertEqual(item.qty, 0)

    def test_update_qty_non_owner_forbidden_and_state_unchanged(self):
        # Arrange
        owner_id = "user-a"
        other_id = "user-b"
        item = create_item(name="milk", qty=2, user_id=owner_id)
        before_qty = item.qty

        # Act + Assert
        with self.assertRaises(PermissionError) as ctx:
            update_qty(str(item.id), 1, other_id)

        self.assertEqual(str(ctx.exception), "forbidden")

        item.refresh_from_db()
        self.assertEqual(item.qty, before_qty)

    def test_update_qty_missing_item_returns_none(self):
        # Arrange
        user_id = "user-a"
        missing_id = str(uuid.uuid4())

        # Act
        result = update_qty(missing_id, 1, user_id)

        # Assert
        self.assertIsNone(result)

    def test_update_qty_cannot_go_below_zero_raises_value_error_and_state_unchanged(self):
        # Arrange
        user_id = "user-a"
        item = create_item(name="milk", qty=2, user_id=user_id)
        before_qty = item.qty

        # Act + Assert
        with self.assertRaises(ValueError) as ctx:
            update_qty(str(item.id), -3, user_id)  # 2 + (-3) => -1

        self.assertEqual(str(ctx.exception), "qty cannot go below 0")

        item.refresh_from_db()
        self.assertEqual(item.qty, before_qty)

    def test_update_qty_delta_must_be_int_raises_value_error_and_state_unchanged(self):
        # Arrange
        user_id = "user-a"
        item = create_item(name="milk", qty=2, user_id=user_id)
        before_qty = item.qty

        # Act + Assert
        with self.assertRaises(ValueError) as ctx:
            update_qty(str(item.id), "nope", user_id)  # type: ignore[arg-type]

        self.assertEqual(str(ctx.exception), "delta must be an int")

        item.refresh_from_db()
        self.assertEqual(item.qty, before_qty)

    def test_update_qty_delta_bool_rejected_raises_value_error_and_state_unchanged(self):
        # Arrange
        user_id = "user-a"
        item = create_item(name="milk", qty=2, user_id=user_id)
        before_qty = item.qty

        # Act + Assert (bool is a subclass of int in Python)
        with self.assertRaises(ValueError) as ctx:
            update_qty(str(item.id), True, user_id)  # type: ignore[arg-type]

        self.assertEqual(str(ctx.exception), "delta must be an int")

        item.refresh_from_db()
        self.assertEqual(item.qty, before_qty)
