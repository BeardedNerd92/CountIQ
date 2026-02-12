import json
from typing import Optional

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from items.auth import extract_bearer_token
from items.services.inventory_service import create_item, delete_item, update_qty
from items.session_store import SESSIONS


def resolve_user_id(request) -> Optional[str]:
    token = extract_bearer_token(request)
    if token is None:
        return None
    return SESSIONS.get(token)


@csrf_exempt
def create_item_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    user_id = resolve_user_id(request)
    if user_id is None:
        return JsonResponse({"error": "unauthorized"}, status=401)

    try:
        raw = request.body.decode("utf-8") if request.body else "{}"
        data = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({"error": "invalid JSON"}, status=400)

    name = data.get("name")
    qty = data.get("qty")

    try:
        item = create_item(name, qty, user_id)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse(
        {"id": str(item.id), "name": item.name, "qty": item.qty, "owner_id": user_id},
        status=201,
    )


@csrf_exempt
def delete_item_view(request, item_id: str):
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE only"}, status=405)

    user_id = resolve_user_id(request)
    if user_id is None:
        return JsonResponse({"error": "unauthorized"}, status=401)

    try:
        delete_item(str(item_id), user_id)
    except PermissionError:
        return JsonResponse({"error": "forbidden"}, status=403)
    except ValueError:
        return JsonResponse({"error": "not found"}, status=404)

    return HttpResponse(status=204)


@csrf_exempt
def update_qty_view(request, item_id):
    if request.method != "PATCH":
        return JsonResponse({"error": "PATCH only"}, status=405)

    user_id = resolve_user_id(request)
    if user_id is None:
        return JsonResponse({"error": "unauthorized"}, status=401)

    # (Optional) This will never trigger if URL is <uuid:item_id>, but harmless.
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
        item = update_qty(str(item_id), delta, user_id)
    except PermissionError:
        return JsonResponse({"error": "forbidden"}, status=403)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    if item is None:
        # Keep consistent with DELETE: "not found"
        return JsonResponse({"error": "not found"}, status=404)

    return JsonResponse(
        {"id": str(item.id), "name": item.name, "qty": item.qty, "owner_id": item.owner_id},
        status=200,
    )
