# CountIQ's Logging Architecture

System flow (Interface → backend → logs)

flowchart TD
  %% ===== Interface =====
  A[Interface (frozen)\nCurrently implemented via CLI/curl for transport testing]
    -->|HTTP Request| B[Django Transport / URL Router]

  %% ===== Middleware =====
  B --> C[Middleware: request_id + start log]
  C --> D[Auth Boundary]

  %% ===== Auth branch =====
  D -->|Denied| E[Log: auth.denied] --> F[HTTP 401/403 Response]
  D -->|Allowed| G[Service Layer]

  %% ===== Service branch =====
  G --> H{Mutation?}

  %% ===== Read path =====
  H -->|No| I[Repo/Query] --> J[Log: http.completed] --> K[HTTP Response]

  %% ===== Mutation path =====
  H -->|Yes| L[Log: mutation.intent]
  L --> M[Domain Validation]
  M -->|Fail| N[Log: error.domain_invariant] --> O[Error Response]
  M -->|Pass| P[DB Transaction]
  P -->|DB Error| Q[Log: error.db_exception] --> R[HTTP 5xx]
  P -->|Success| S[Log: mutation.success] --> T[Log: http.completed] --> U[HTTP 2xx]

  %% ===== Exception fallback =====
  B -. unhandled exception .-> X[Log: error.unhandled_exception] --> R
