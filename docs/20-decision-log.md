# 20 — JANSAHAY Architectural Decision Log (ADR)

## ADR 01: Universal State Engine Architecture
- **Date**: 2026-08-26
- **Context**: Government services historically build disjoint portals with custom hardcoded status tables.
- **Decision**: Build ONE universal versioned state machine engine where services (Certificates, EPFO, Grievances) are configurations with declarative transition graphs and guard rules.
- **Tradeoffs**: Requires rigorous schema design and guard validation, but yields zero code duplication and instant extensibility for new government services.

---

## ADR 02: Explicit Action Endpoints over Generic State Transitions
- **Date**: 2026-08-26
- **Context**: Allowing clients to send `POST /cases/{id}` with `{ "new_state": "APPROVED" }` invites state skipping and privilege escalation vulnerabilities.
- **Decision**: Enforce explicit action endpoints (`POST /cases/{id}/actions/{action_name}`) where the backend evaluates RBAC, guards, and calculates the legal next state.
- **Tradeoffs**: Requires well-defined action verbs, but completely prevents illegal workflow leaps.

---

## ADR 03: Tamper-Evident SHA-256 Event Chaining
- **Date**: 2026-08-26
- **Context**: Public administrative decisions require non-repudiation and auditability.
- **Decision**: Hash chain every workflow event ($H_N = \text{SHA256}(H_{N-1} + \dots)$) in the same transaction as state changes.
- **Tradeoffs**: Slight compute overhead per transition, but provides mathematical proof against administrative tampering.

---

## ADR 04: Password Hashing Library Compatibility & Bcrypt Version Pinning
- **Date**: 2026-08-28
- **Context**: `passlib` version 1.7.4 contains a legacy `detect_wrap_bug` test probe that executes during password hashing initialization using a secret longer than 72 bytes. When installed with `bcrypt>=4.1.0`, `bcrypt` strictly raises a `ValueError` for inputs over 72 bytes, crashing database initialization in Python 3.11 Docker environments.
- **Decision**: Pin `bcrypt<4.1.0` in `requirements.txt` while maintaining standard salted `bcrypt` algorithms for user credential hashing.
- **Tradeoffs**: Minor restriction on minor bcrypt releases, but guarantees 100% reproducible zero-error container initialization and authentication operations.

---

## ADR 05: Single-Port Embedded Full-Stack Delivery
- **Date**: 2026-08-28
- **Context**: Hackathon evaluators require instant, frictionless setup without configuring multiple ports, reverse proxies, or separate Node dev servers.
- **Decision**: Bundle the interactive frontend SPA directly into FastAPI's static/HTML delivery layer on port 8000 alongside OpenAPI Swagger docs and backend endpoints, while preserving full separation for standalone Vite development.
- **Tradeoffs**: Simplifies evaluator experience to a single `docker compose up` command.

