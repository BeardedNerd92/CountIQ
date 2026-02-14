# 📦 CountIQ — Systems-First Inventory Engine

## Project Scope

See [docs/mvp.md](docs/MVP.md) for MVP scope, deliverables, and roadmap.

**CountIQ** is a backend systems project focused on enforcing **correct state transitions** rather than just building CRUD endpoints.

This project explores how real services handle:

* authentication
* ownership
* invariants
* state mutation
* correctness under failure

Originally built as an inventory API, it was renamed to **CountIQ** to reflect its purpose:

> Count state correctly.
> Control who can change it.
> Prove the system behaves correctly.

There is **no UI**.
All interaction happens through HTTP using `curl`.

---

# 🧭 System Philosophy

Most apps focus on endpoints.

CountIQ focuses on guarantees:

* Who can mutate state?
* When must state remain unchanged?
* How do we prove correctness?

Core rule:

```
Unauthorized request ⇒ state does not change
```

---

# 🏗 Architecture

```
transport → service → model → database
```

### Transport

* Parses HTTP
* Resolves user from token
* Returns HTTP responses

### Service

* Enforces ownership
* Validates invariants
* Controls state transitions

### Database

* Stores source of truth
* Enforces schema rules

---

# 🔄 Request Flow Diagram

```
Client (curl)
   ↓
Transport layer
   ↓
Auth check (token → user)
   ↓
Service layer
   ↓
Ownership + invariant checks
   ↓
Database mutation (if allowed)
```

If any step fails:

```
request rejected
state unchanged
```

---

# 🧮 The Math (explained simply)

You’ll see math-like notation in this repo.
Here’s what it means in plain English.

### System state

```
S = everything stored in the database
```

Each item:

```
item = { id, name, qty, owner_id }
```

---

### Requests change state

```
S' = f(S, request)
```

Translation:

> The new state is the result of applying a request to the current state.

Example:

```
POST → adds item
DELETE → removes item
```

---

### Most important rule

If request is unauthorized:

```
S' = S
```

Translation:

> Nothing changes.

We test this explicitly.

---

# 🔐 Authentication Model (v2-auth)

Development auth uses simple tokens:

```
Authorization: Bearer token-a
```

Token maps to user:

```
token-a → user-a
token-b → user-b
```

All write routes require authentication.

---

# 📡 Endpoints

## Create Item

```
POST /items
```

Create an item owned by the authenticated user.

### Example

```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Authorization: Bearer token-a" \
  -H "Content-Type: application/json" \
  -d '{"name":"milk","qty":2}'
```

Response:

```json
{
  "id": "uuid",
  "name": "milk",
  "qty": 2,
  "owner_id": "user-a"
}
```

### What happens internally

```
token → user_id
user_id → owner_id
item saved
```

If no auth token:

```
401 unauthorized
```

---

## Delete Item

```
DELETE /items/<id>
```

Only the owner can delete.

### Non-owner attempt

```bash
curl -X DELETE http://127.0.0.1:8000/items/<id> \
  -H "Authorization: Bearer token-b"
```

Response:

```
403 forbidden
```

State does not change.

---

### Owner delete

```bash
curl -X DELETE http://127.0.0.1:8000/items/<id> \
  -H "Authorization: Bearer token-a"
```

Response:

```
204
```

Item removed.

---

# 🔒 Invariants

These must always be true:

```
name cannot be empty
qty ≥ 0
owner_id must exist
```

Ownership rule:

```
item.owner_id == request.user.id
```

If violated:

```
reject request
state unchanged
```

---

# 🧪 Testing Strategy

The system is verified using:

* unit tests
* integration tests
* manual curl testing

Key properties tested:

```
unauthenticated → 401
non-owner delete → 403
owner delete → 204
forbidden mutation → state unchanged
```

---

# 🏷 Version Roadmap

```
v1-foundations   core architecture + invariants
v2-auth          authentication + ownership
v2-deploy        deployment + logging
v3-performance   indexing + scaling
v4-concurrency   queues + contention
v5-ml            analytics layer
```

Each milestone is tagged in Git.

---

# 🚀 Running Locally

```
python manage.py runserver
```

Then use the curl commands above.

To test auth locally, seed tokens in the session store:

```python
SESSIONS["token-a"] = "user-a"
SESSIONS["token-b"] = "user-b"
```

---

# 🧠 Why CountIQ Exists

This project is designed to think like a systems engineer:

* enforce invariants
* model state transitions
* prove correctness
* build versioned systems

Not just CRUD.

---

# 🔭 Next Steps

* PATCH ownership enforcement
* deployment milestone
* observability
* performance tuning

---

# 📘 Mental Model

CountIQ is a guarded state machine:

```
Authorized action → state changes
Unauthorized action → state stays the same
```

That’s the core of the system.

---

## Concurrency Notes

CountIQ is designed around a strict transition model:

```
S' = f(S, input)
if invariant fails → S' = S
```

In **v2-deploy**, the service logic is correct for single-request execution, but **not yet hardened for concurrent writers**. Specifically, any flow that effectively does:

```
read → validate → write
```

can suffer from classic race conditions (TOCTOU / lost update) when two requests operate on the same record at the same time. ([Wikipedia][1])

### What this means today

* **DELETE** remains *API-idempotent*, but can still race with other operations unless enforced atomically at the DB boundary.
* **PATCH/UPDATE** can experience “lost update” style anomalies if two updates interleave between read and write.

### Planned hardening (Concurrency Version)

A future concurrency-focused version will make writes concurrency-safe by enforcing **atomic transitions** at the database boundary, using one (or more) of these standard approaches:

1. **Pessimistic row locking**
   Lock the target row during the read/validate/write window (e.g., `SELECT … FOR UPDATE`) so concurrent writers must wait until the transaction completes. ([PostgreSQL][2])

2. **Atomic conditional updates**
   Encode the invariant directly into the update statement (e.g., update only if the invariant still holds) so the DB applies the transition as a single atomic action. ([PostgreSQL][3])

These changes are intentionally deferred to the concurrency version to avoid scope creep during v2-deploy hardening.

---

[1]: https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use?utm_source=chatgpt.com "Time-of-check to time-of-use"
[2]: https://www.postgresql.org/docs/current/explicit-locking.html?utm_source=chatgpt.com "Documentation: 18: 13.3. Explicit Locking"
[3]: https://www.postgresql.org/docs/current/sql-update.html?utm_source=chatgpt.com "PostgreSQL: Documentation: 18: UPDATE"

---

# 👋 Author

Built as a systems learning project focused on backend correctness, architecture, and production-minded design.
