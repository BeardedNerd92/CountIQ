# Inventory System v2 — Backend Systems Project

This project is a backend-only inventory system built to practice real backend engineering fundamentals:

* state modeling
* invariants
* transactional persistence
* correctness under concurrency

There is **no UI**.
All interaction happens through HTTP endpoints using `curl`.

The goal is not rapid feature building — it is learning how to design systems that preserve correctness under all transitions.

---

## Architecture

```
transport → service → model → database
```

Concrete stack:

* Django (transport + models)
* Service layer (state transitions + transactions)
* SQLite (persistence)

No repository layer is used.
The Django model + database are the source of truth.

---

## System Design Principles

### State Model

```
S = Map[id → item]
item = { id, name, qty }
```

All operations are state transitions:

```
S' = f(S, input)
```

---

### Invariants (truth)

The system guarantees:

* `name.strip() ≠ ""`
* `qty ∈ ℤ`
* `qty ≥ 0`
* `name` is unique

If any invariant fails:

```
S' = S
```

No mutation is allowed.

---

### Invariant Enforcement

Invariants are:

* centralized in `invariants.py`
* pure (no mutation)
* dict in → dict out
* deterministic

They are enforced at the **model boundary** before any database commit.

Mutation happens only at:

```
model.save()
```

---

### Transition Law

All transitions follow:

```
validate → commit → return
```

Never:

```
commit → fix later
```

This guarantees database correctness and rollback safety.

---

### Transactions

All write operations are wrapped in:

```
transaction.atomic()
```

This ensures:

```
valid → commit
invalid → rollback
```

---

## API Endpoints

All interaction is done via `curl`.

---

## Create Item

```
POST /items
```

```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"apple","qty":5}'
```

Success:

```
201 Created
{
  "id": "UUID",
  "name": "apple",
  "qty": 5
}
```

Duplicate names or invalid input return `400`.

---

## Delete Item (idempotent)

```
DELETE /items/<uuid>
```

```bash
curl -X DELETE http://127.0.0.1:8000/items/<UUID>
```

Success:

```
204 No Content
```

Deleting a non-existent item is safe and idempotent.

---

# Update Quantity (atomic transition)

```
PATCH /items/<uuid>/qty
```

Body:

```json
{ "delta": -1 }
```

---

## What `delta` means

`delta` represents the **change** to apply to quantity.

| delta | result         |
| ----- | -------------- |
| -1    | decrement by 1 |
| +5    | increment by 5 |
| 0     | no change      |

This endpoint does **not** set quantity directly.

Instead:

```
qty' = qty + delta
```

This prevents race conditions and ensures atomic transitions.

---

## Service-layer implementation

The transition is implemented using a single guarded atomic update.

```python
updated = (
    Item.objects
    .filter(id=item_id, qty__gte=-delta)
    .update(qty=F("qty") + delta)
)
```

### What this does

**1. Guard**

```
qty__gte=-delta
```

Ensures:

```
current_qty + delta ≥ 0
```

This prevents negative quantity.

---

**2. Atomic update**

```
qty = qty + delta
```

Uses `F("qty")` so the DB handles concurrency safely.

---

**3. Result handling**

```python
if updated:
    return Item.objects.get(id=item_id)

if not Item.objects.filter(id=item_id).exists():
    return None

raise ValueError("qty cannot go below 0")
```

Meaning:

| Outcome                     | Meaning |
| --------------------------- | ------- |
| updated row                 | success |
| no row + not exists         | 404     |
| row exists but guard failed | 400     |

---

## Example Success

```
qty = 5
delta = -1
```

Result:

```
qty = 4
200 OK
```

---

## Example Invariant Violation

```
qty = 0
delta = -2
```

Would produce:

```
qty = -2 → invalid
```

Database blocks update.

Response:

```
400 Bad Request
{
  "error": "qty cannot go below 0"
}
```

State remains unchanged.

---

## Status Code Mapping

| Result               | Status |
| -------------------- | ------ |
| success              | 200    |
| not found            | 404    |
| invalid delta        | 400    |
| qty would go below 0 | 400    |

Service contract:

```
returns Item → success
returns None → not found
raises ValueError → invalid
```

The view maps this to HTTP responses.

---

## Error Handling

All endpoints return JSON.

A custom project-level 404 handler ensures invalid routes also return JSON:

```json
{ "error": "not_found" }
```

instead of Django’s default HTML page.

---

## Running Locally

Install dependencies:

```
pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Start server:

```
python manage.py runserver
```

Run tests:

```
python manage.py test
```

---

## Current Features

* transactional create_item
* idempotent delete_item
* atomic qty updates
* centralized invariant enforcement
* database-enforced uniqueness
* UUID primary keys
* JSON-only responses
* curl-driven interaction
* state-based testing

---

## Recent Stability Fixes

While implementing the PATCH endpoint, several runtime issues were discovered and resolved:

* returned `None` after successful update → false 404
* UUID routing mismatch
* bool treated as int
* inconsistent error responses
* Django HTML error pages for invalid routes

Fixes:

* explicit service return contract
* UUID normalization
* transaction wrapping
* custom JSON 404 handler
* strict type validation

These changes improve runtime correctness and transport reliability.

---

## Upcoming Work

* remove csrf_exempt
* authentication boundary
* request logging
* concurrency tests
* PostgreSQL migration

---

## Why this project exists

Most tutorials focus on frameworks and UI.

This project focuses on:

```
state
invariants
transactions
correctness
```

The goal is to build backend systems that are predictable, testable, and safe under failure.

---

## License

MIT