from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def json_404(request, exception):
    return JsonResponse({"error": "not_found"}, status=404)


urlpatterns = [
    path("", include("items.urls")),
    path("admin/", admin.site.urls),
]

handler404 = "inventory.urls.json_404"
