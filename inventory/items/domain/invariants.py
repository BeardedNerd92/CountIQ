def normalize_and_validate_item(data: dict) -> dict:
    name = data.get("name")
    qty = data.get("qty")

    if not isinstance(name, str):
        raise ValueError("name must be a string")

    name = name.strip()
    if name == "":
        raise ValueError("name must be non-empty")

    if not isinstance(qty, int):
        raise ValueError("qty must be an integer")

    if qty < 0:
        raise ValueError("qty must be >= 0")

    return {
        "name": name,
        "qty": qty,
    }
