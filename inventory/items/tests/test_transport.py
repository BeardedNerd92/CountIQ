import json
from django.test import TestCase, Client
from items.domain.models import Item


class CreateItemViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_post_creates_item(self):
        res = self.client.post(
            "/items",
            data=json.dumps({"name": "apple", "qty": 5}),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Item.objects.count(), 1)

    def test_invalid_name_returns_400(self):
        res = self.client.post(
            "/items",
            data=json.dumps({"name": "", "qty": 5}),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(Item.objects.count(), 0)

    def test_duplicate_name_returns_400(self):
        self.client.post(
            "/items",
            data=json.dumps({"name": "apple", "qty": 5}),
            content_type="application/json",
        )

        res = self.client.post(
            "/items",
            data=json.dumps({"name": "apple", "qty": 3}),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(Item.objects.count(), 1)
