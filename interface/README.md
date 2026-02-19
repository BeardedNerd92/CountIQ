# CountIQ CLI Interface

This script is a lightweight Python interface used to interact with the CountIQ API.
It simulates a real external client and is intended for testing, learning, and deployment validation.

The interface allows a user to perform basic operations against the API through a terminal menu.

---

## Purpose

This client exists to:

* test API endpoints outside the backend
* simulate real user interaction
* validate authentication and request flow
* provide a simple development tool during deployment
* reinforce system invariants at the client boundary

This script does **not** replace backend validation.
All invariants are still enforced server-side.

---

## Architecture

The interface follows strict separation of concerns:

```
main → state → transitions → api methods → curl/http client
                ↓
             invariants
```

### Key components

**main.py**

* entry point
* displays menu
* routes user input

**state.py**

* holds in-memory state
* maintains counter → method mapping
* ensures state invariants

**invariants.py**

* central validation class
* validates user input
* validates state integrity
* enforces authentication presence

**transitions.py**

* orchestrates allowed mutations
* ensures only authenticated users perform writes

**items/api_methods.py**

* contains API interaction methods
* READ, POST, DELETE, PATCH

**items/curl_client.py**

* single HTTP/curl wrapper
* prevents duplicated request logic
* enforces DRY

**user.py**

* represents authenticated user
* new instance created per action

---

## State Model

The client maintains an in-memory state:

```
state = {
    counter: int,
    menu: dict[int → method]
}
```

The counter increments for each registered command.
The menu dictionary maps user selections to callable actions.

State exists only for the lifetime of the program.

---

## Invariants

The following invariants are enforced at the interface level:

```
counter must be int ≥ 0
state must remain a dict during runtime
user must be authenticated before mutations
name must be non-empty string
qty must be non-negative integer
delta must be non-negative integer
```

These invariants prevent invalid requests from being sent to the API.

Server-side invariants remain the source of truth.

---

## Transitions

Allowed transitions:

```
READ   → fetch items
POST   → create item
DELETE → remove item
PATCH  → update name or quantity
```

Rules:

* Only authenticated users may perform mutations
* Read operations require authentication but do not mutate state
* State is not persisted locally

---

## Usage

Run the script:

```
python main.py
```

You will see:

```
1 → read
2 → create
3 → delete
4 → patch
```

Follow prompts to provide input.

---

## Environment Variables

The interface expects:

```
COUNTIQ_BASE_URL
COUNTIQ_TOKEN
COUNTIQ_USER_ID
```

Example:

```
export COUNTIQ_BASE_URL=http://localhost:8000
export COUNTIQ_TOKEN=dev-token
```

---

## Design Principles

This interface follows the same discipline as the backend:

* separation of concerns
* centralized invariants
* stateless requests
* explicit transitions
* no hidden mutation
* DRY request layer

The client mirrors the system architecture to reinforce understanding.

---

## Future Improvements

Possible extensions:

* structured logging
* response formatting
* retry logic
* config file support
* SDK-style packaging
* test harness integration

---

## Notes

This interface is intentionally minimal.
Its goal is clarity and correctness, not convenience.

The backend remains the authority on data integrity.