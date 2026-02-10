from django.test import TestCase
from items.services.inventory_service import create_item, delete_item, update_qty
from items.domain.models import Item


class CreateItemServiceTests(TestCase):

    def test_create_valid_item_commits(self):
        create_item("apple", 5)

        self.assertEqual(Item.objects.count(), 1)

        item = Item.objects.first()
        self.assertEqual(item.name, "apple")
        self.assertEqual(item.qty, 5)

    def test_name_is_stripped(self):
        create_item("  apple  ", 5)

        item = Item.objects.first()
        self.assertEqual(item.name, "apple")

    def test_empty_name_rejected(self):
        with self.assertRaises(ValueError):
            create_item("", 5)

        self.assertEqual(Item.objects.count(), 0)

    def test_negative_qty_rejected(self):
        with self.assertRaises(ValueError):
            create_item("apple", -1)

        self.assertEqual(Item.objects.count(), 0)

    def test_duplicate_name_rejected(self):
        create_item("apple", 5)

        with self.assertRaises(ValueError):
            create_item("apple", 3)

        self.assertEqual(Item.objects.count(), 1)

    def test_delete_idempotent(self):
        item = create_item("apple", 2)
        item_id = item.id

        self.assertTrue(Item.objects.filter(id=item_id).exists())
        delete_item(item_id)
        self.assertFalse(Item.objects.filter(id=item_id).exists())

    def test_update_qty_increment_commits(self):
        item = create_item("apple", 3)
        update_qty(item.id, 5)

        item.refresh_from_db()
        self.assertEqual(item.qty, 8)

    def test_update_qty_decrement_commits(self):
        item = create_item("apple", 3)
        update_qty(item.id, -1)

        item.refresh_from_db()
        self.assertEqual(item.qty, 2)

    def test_update_qty_allows_decrement_to_zero(self):
        item = create_item("apple", 1)
        update_qty(item.id, -1)

        item.refresh_from_db()
        self.assertEqual(item.qty, 0)

    def test_update_qty_rejects_when_would_go_negative(self):
        item = create_item("apple", 0)

        with self.assertRaises(ValueError):
            update_qty(item.id, -1)

        item.refresh_from_db()
        self.assertEqual(item.qty, 0)

    def test_update_qty_rejects_non_int_delta(self):
        item = create_item("apple", 3)

        with self.assertRaises(ValueError):
            update_qty(item.id, "1")  # type: ignore[arg-type]

        item.refresh_from_db()
        self.assertEqual(item.qty, 3)

    def test_update_qty_not_found(self):
        with self.assertRaises(ValueError):
            update_qty(999999, -1)

        self.assertEqual(Item.objects.count(), 0) 