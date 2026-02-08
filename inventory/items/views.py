import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from items.services.inventory_service import create_item, delete_item


@csrf_exempt
def create_item_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid JSON"}, status=400)

    name = data.get("name")
    qty = data.get("qty")

    try:
        item = create_item(name, qty)

        return JsonResponse(
            {
                "id": str(item.id),
                "name": item.name,
                "qty": item.qty,
            },
            status=201,
        )

    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def delete_item_view(request, item_id: str):
    if request.method != "DELETE":
       return JsonResponse({"error": "DELETE only"}, status=405)
    
    delete_item(item_id)
    return HttpResponse(status=204)