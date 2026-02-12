from typing import Optional

def extract_bearer_token(request) -> Optional[str]:
    auth = request.META.get("HTTP_AUTHORIZATION")
    if not auth:
        return None

    prefix = "Bearer "
    if not auth.startswith(prefix):
        return None

    token = auth[len(prefix):].strip()
    if token == "":
        return None

    return token
