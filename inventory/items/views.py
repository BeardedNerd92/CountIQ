import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from items.services.inventory_service import create_item, delete_item, update_qty


@csrf_exempt
def create_item_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        raw = request.body.decode("utf-8") if request.body else "{}"
        data = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({"error": "invalid JSON"}, status=400)

    name = data.get("name")
    qty = data.get("qty")

    try:
        item = create_item(name, qty)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse(
        {"id": str(item.id), "name": item.name, "qty": item.qty},
        status=201,
    )


@csrf_exempt
def delete_item_view(request, item_id: str):
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE only"}, status=405)

    delete_item(item_id)
    return HttpResponse(status=204)


@csrf_exempt
def update_qty_view(request, item_id):
    if request.method != "PATCH":
        return JsonResponse({"error": "PATCH only"}, status=405)

    if not item_id:
        return JsonResponse({"error": "item_id required"}, status=400)


    try:
        raw = request.body.decode("utf-8") if request.body else "{}"
        data = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({"error": "invalid JSON"}, status=400)


    if "delta" not in data:
        return JsonResponse({"error": "missing delta"}, status=400)

    delta = data["delta"]

    if isinstance(delta, bool) or not isinstance(delta, int):
        return JsonResponse({"error": "delta must be integer"}, status=400)


    try:
        item = update_qty(item_id, delta)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    if item is None:
        return JsonResponse({"error": "item not found"}, status=404)

    return JsonResponse(
        {"id": str(item.id), "name": item.name, "qty": item.qty},
        status=200,
    )
