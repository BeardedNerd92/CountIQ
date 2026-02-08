from django.urls import path
from items.views import create_item_view, delete_item_view

urlpatterns = [
    path("items", create_item_view),
    path("items/<str:item_id>/", delete_item_view)
]
