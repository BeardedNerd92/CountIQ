# CountIQ Logging Contract (v2-deploy)

## Goals
- Stable, searchable JSON logs
- Correlate all events by request_id
- No secrets in logs
- Works locally and in Docker/AWS without rewrite

## Event Envelope (base fields)
Every log line MUST be a JSON object containing:

- timestamp (ISO 8601)
- level ("INFO"|"WARNING"|"ERROR")
- event (string)
- request_id (string)
- method (string)
- path (string)
- status_code (int, if response known)
- latency_ms (int, for completed requests)
- service ("countiq-api")
- env ("dev"|"prod")

Optional fields:
- actor_id (string)
- item_id (string)
- mutation ("create"|"delete"|"update_qty")
- outcome ("ok"|"error")
- error_code (string)
- detail (string, sanitized)

## Event Names
### HTTP lifecycle
- http.request.started
- http.request.completed

### Auth
- auth.denied
- auth.unauthorized

### Mutations
- mutation.item.create.intent
- mutation.item.create.success
- mutation.item.delete.intent
- mutation.item.delete.success
- mutation.item.update_qty.intent
- mutation.item.update_qty.success

### Errors
- error.domain_invariant
- error.db_exception
- error.unhandled_exception

## Sanitization Rules (hard rules)
- NEVER log: passwords, tokens, SECRET_KEY, session ids, raw Authorization headers
- Log only IDs (actor_id, item_id), not full payloads
- Errors must be normalized to {error_code, detail} with detail scrubbed

## Correlation
- request_id is generated if missing
- request_id is returned in response header: X-Request-ID