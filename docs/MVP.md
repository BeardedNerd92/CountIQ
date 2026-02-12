# CountIQ — MVP Scope & Release Plan

## 🎯 Purpose

CountIQ is a **multi-tenant inventory API** built with systems-first discipline.

The MVP is designed to be:

- usable by a real company
- portfolio-grade
- extensible to analytics and ML
- documented as part of the CountIQ book

This document defines **scope**, **deliverables**, and **release criteria**  
to prevent scope creep and keep development intentional.

---

# 🧱 MVP Definition

The CountIQ MVP is considered ready when a company can:

- create inventory items
- safely mutate quantities
- query inventory
- support multiple users
- track inventory history
- run the API in production

The MVP is **API-only**.  
No UI is required.

---

# 🔒 In Scope

## Core Inventory
- Create item
- Delete item
- Update qty (atomic)
- Enforce invariants:
  - qty ≥ 0
  - name not empty
  - unique per tenant

## Multi-tenant foundation
- Users table
- Organizations table
- Membership table
- Inventory scoped to organization

## Read layer
- `GET /items`
- Pagination
- Filtering
- Sorting

## Audit logging
Every mutation must produce an immutable event.

Events capture:
- item_id
- actor_user_id
- delta
- qty_after
- timestamp

This enables:
- analytics
- ML later
- debugging
- compliance

## Deployment readiness
- Environment-based settings
- Logging
- Health endpoint
- Persistent DB
- Deployed API

---

# 🚫 Out of Scope (MVP)

To prevent scope creep:

- ML / forecasting
- dashboard UI
- notifications
- billing
- advanced roles
- RapidAPI listing
- web frontend
- analytics dashboards

All are post-MVP.

---

# 🏗️ Database Architecture

## Users
```

id (string or uuid, pk)
email (optional for now)
created_at

```

## Organizations
```

id (uuid, pk)
name
created_at

```

## Memberships
```

id (uuid, pk)
org_id (fk)
user_id (fk)
role (admin | member)

UNIQUE(org_id, user_id)

```

## Items
```

id (uuid, pk)
org_id (fk)
name
qty
created_by_user_id (fk)
created_at

CHECK(qty >= 0)
UNIQUE(org_id, name)

```

## Item Events (audit log)
```

id (uuid, pk)
org_id (fk)
item_id (fk)
actor_user_id (fk)
type
delta
qty_after
created_at

```

Indexes:
```

(org_id, created_at)
(item_id, created_at)

```

---

# 📦 MVP Deliverables

## System
- Deployed API
- Persistent DB
- Logging enabled
- Health endpoint
- Environment config

## Features
- Mutation endpoints
- Read endpoints
- Multi-user support
- Audit log recording

## Documentation
- README
- curl examples
- architecture diagram
- invariants documented

## Book alignment
The MVP corresponds to:

- Part I — Foundations
- Part II — Identity & Authority
- Part III — Deployment

---

# ⏱️ Estimated Timeline

Realistic pace:
**1 feature per session**

### Week 1
Deployment readiness:
- env config
- logging
- health endpoint
- deploy

### Week 2
Read layer:
- GET /items
- pagination
- filtering

### Week 3
Users + orgs:
- user table
- organization table
- membership table

### Week 4
Audit log:
- item_events table
- record events on mutation

### Week 5–6
Stabilization:
- cleanup
- docs
- testing
- polish

---

# 🟢 MVP Release Target

**4–6 weeks**

At release, CountIQ becomes:

- usable internally
- portfolio-grade
- extensible to analytics
- ML-ready foundation

---

# 🧠 Post-MVP Roadmap

After MVP:

```

v1 foundations   ✅
v2 auth          ✅
v2 deploy        in progress
v3 reads
v4 org + audit
MVP release
v5 analytics
v6 dashboard
ML layer
RapidAPI (far future)

```

---

# 🛡️ Core Principles

CountIQ is built with:

- invariants first
- service-layer correctness
- atomic mutations
- multi-tenant safety
- extensibility for analytics and ML

This is a **system that evolves**, not a toy project.

---

# Status

```

main: stable
branch: feat/v2-deploy

```

Next milestone: deployment readiness.