from django.urls import path
from items.views import create_item_view, delete_item_view, update_qty_view

app_name = "items"

urlpatterns = [
    path("items", create_item_view, name="create"),
    path("items/<uuid:item_id>", delete_item_view, name="delete"),
    path("items/<uuid:item_id>/qty", update_qty_view, name="update_qty"),
]
