# Inventory System v2

A state-driven inventory management system focused on **domain truth, invariants, and clean system boundaries**.

This project is being built deliberately from the inside out:

1. Define truth
2. Enforce invariants
3. Establish service authority
4. Then expose via API and UI

The goal is not just to build an app, but to build it **correctly**.

---

## Architecture Principles

### Source of Truth

The **domain layer** defines what is true about the system.
Persistence (Postgres) stores that truth but does not define it.

### Authority

All state mutation flows through the **service layer**, which enforces invariants before persistence.

### Persistence

Postgres will serve as the durable data store.
A repository layer isolates persistence from domain logic.

### Invariants

System invariants enforced centrally:

* Product name is trimmed and required
* Quantity must be a non-negative integer
* Product name is unique
* Delete operations are idempotent

These invariants define the system’s correctness and are enforced independent of UI or transport layer.

---

## Tech Stack (Planned)

* React (UI)
* Django (transport + integration layer)
* Postgres (persistence)

---

## Current Status

* Django scaffold complete
* Environment-based configuration in place
* Preparing domain + service layer implementation
* No endpoints or UI yet (intentional)

---

## Project Structure (in progress)

```
inventory-system-v2/
  items/
    domain/
    services/
    repo/
  README.md
```

---

## Future Work

* Implement domain model + invariants
* Add service layer
* Introduce Postgres persistence
* Add API endpoints
* Build React UI

---

## Author

Nick — Software engineer in training, focused on systems design and long-term mastery.
