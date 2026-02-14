# CountIQ's — App Architecture

## Overview

CountIQ is a Django backend with a frozen Interface layer (currently exercised via CLI/curl for transport testing).

**Architecture (backend):**

transport → service → domain → database

**State model:**
S = Map[id → item], where item = { id, name, qty, owner_id }

**Transition rule:**
S' = f(S, input)
if invariant fails → S' = S

---

## End-to-end system diagram

```mermaid
flowchart TD
  %% ===== Interface =====
  A[Interface (frozen)\nCurrently: CLI/curl for transport testing]
    -->|HTTP| B[Django App]

  %% ===== Django request stack =====
  B --> C[ASGI/WSGI Server\n(gunicorn/uvicorn later)]
  C --> D[Django Middleware Chain\n(request_id, logging, auth helpers)]
  D --> E[URL Router]
  E --> F[Transport Layer (Views)]

  %% ===== Layered backend =====
  F --> G[Service Layer (Authority Boundary)]
  G --> H[Domain Layer (Invariants + Models)]
  H --> I[Repository / ORM]
  I --> J[(Database)]

  %% ===== Response =====
  J --> I --> H --> G --> F --> K[HTTP Response]
  K --> A

  %% ===== Observability (cross-cutting) =====
  D -. emits events .-> L[Python logging\n(JSON formatter)]
  G -. emits mutation events .-> L
  F -. emits request/response events .-> L
  L --> M[stdout/stderr]
  M --> N[Docker log capture (tomorrow)]
  N --> O[AWS logs aggregation (CloudWatch)]
````

---

## Internal backend flow (detail)

```mermaid
flowchart TD
  R[HTTP Request] --> M1[Middleware: assign request_id]
  M1 --> T1[Transport: parse route + method]
  T1 --> A1{Auth/Ownership}
  A1 -->|Denied| X1[Log auth.denied] --> RESP1[401/403 Response]
  A1 -->|Allowed| S1[Service: orchestrate operation]
  S1 --> P1{Mutation?}

  P1 -->|No| Q1[Repo query] --> OK1[Log http.completed] --> RESP2[2xx Response]

  P1 -->|Yes| L1[Log mutation.intent]
  L1 --> D1[Domain validate invariants]
  D1 -->|Fail| E1[Log error.domain_invariant] --> RESP3[4xx Error Response]
  D1 -->|Pass| DB1[DB transaction / persist]
  DB1 -->|Fail| E2[Log error.db_exception] --> RESP4[5xx Response]
  DB1 -->|Success| L2[Log mutation.success] --> OK2[Log http.completed] --> RESP5[2xx Response]
```

---

## Django-standard logging placement

### Settings responsibilities (configuration only)

* `settings.py` defines:

  * `LOGGING` dict (formatters/handlers/loggers)
  * `MIDDLEWARE` entries (order matters)
  * environment toggles (DEBUG, LOG_LEVEL, etc.)

### Code responsibilities (logic)

* `middleware.py` contains:

  * Request ID assignment
  * request start/completion logs
  * latency timing

* `service` emits:

  * mutation intent/outcome events
  * auth outcomes (deny/allow)

* `domain` returns typed invariant errors:

  * service logs invariant failures consistently

---

## Modules and boundaries

```mermaid
flowchart LR
  subgraph Interface
    I1[Interface (frozen)\nCLI/curl currently]
  end

  subgraph Django
    D1[Transport (Views)] --> S1[Service (Authority)]
    S1 --> G1[Domain (Invariants/Models)]
    G1 --> R1[Repo/ORM]
    R1 --> DB[(DB)]
  end

  subgraph Observability
    O1[Middleware RequestId + Req/Resp logs]
    O2[Service mutation logs]
    O3[Exception logging]
    O4[JSON logging config in settings.py]
  end

  I1 --> D1
  O1 -.observes .-> D1
  O2 -.observes .-> S1
  O3 -.observes .-> Django
  O4 -.configures .-> Observability
```

---

## Logging event envelope (stable)

All log lines are JSON objects with a stable base:

* timestamp
* level
* event
* request_id
* method
* path
* status_code
* latency_ms
* actor_id (optional)
* item_id (optional)
* error_code (optional)
* service
* env


flowchart TD
  R[HTTP Request] --> M1[Middleware: assign request_id]
  M1 --> T1[Transport: parse route + method]
  T1 --> A1{Auth/Ownership}
  A1 -->|Denied| X1[Log auth.denied] --> RESP1[401/403 Response]
  A1 -->|Allowed| S1[Service: orchestrate operation]
  S1 --> P1{Mutation?}

  P1 -->|No| Q1[Repo query] --> OK1[Log http.completed] --> RESP2[2xx Response]

  P1 -->|Yes| L1[Log mutation.intent]
  L1 --> D1[Domain validate invariants]
  D1 -->|Fail| E1[Log error.domain_invariant] --> RESP3[4xx Error Response]
  D1 -->|Pass| DB1[DB transaction / persist]
  DB1 -->|Fail| E2[Log error.db_exception] --> RESP4[5xx Response]
  DB1 -->|Success| L2[Log mutation.success] --> OK2[Log http.completed] --> RESP5[2xx Response]
