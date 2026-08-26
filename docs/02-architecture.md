# 02 — JANSAHAY System Architecture

## 1. High-Level Architectural Model

JANSAHAY is built as a **Modular Monolith** optimized for developer ergonomics, deterministic testing, atomic transactional execution, and zero operational sprawl.

```mermaid
graph TD
    subgraph Client Layer
        CP[Citizen Portal - Next.js/React]
        OP[Officer Workspace - Next.js/React]
        AP[Admin/Demo Console]
    end

    subgraph API Gateway & Auth Layer
        API[FastAPI Gateway / OpenAPI Router]
        AUTH[Contextual RBAC Guard: can(actor, action, resource)]
    end

    subgraph Core Business Engines
        CE[Case Engine]
        WE[Versioned Workflow Engine]
        DE[Quarantined Document Engine]
        AE[Tamper-Evident Audit Ledger]
        NE[Transactional Outbox Notifications]
        AIE[Assistive AI Agent Boundary]
    end

    subgraph Persistence Layer
        DB[(Relational DB: SQLite / PostgreSQL)]
        FS[(Local Sandboxed Document Storage)]
    end

    CP -->|JWT Auth / REST| API
    OP -->|JWT Auth / REST| API
    AP -->|JWT Auth / REST| API

    API --> AUTH
    AUTH --> CE
    AUTH --> WE
    AUTH --> DE
    AUTH --> AIE

    CE --> WE
    WE --> AE
    WE --> NE
    DE --> FS
    CE --> DB
    WE --> DB
    AE --> DB
    NE --> DB
```

---

## 2. Core Architectural Subsystems

### 2.1 Contextual RBAC Layer
The authorization system is centralized around the canonical evaluation pattern:
$$\text{can}(\text{actor}, \text{action}, \text{resource}) \to \{\text{True}, \text{False}\}$$

Evaluation checks:
1. **Role Scope**: Is the actor's role permitted to invoke this action (e.g., `APPROVE` requires `APPROVING_OFFICER`)?
2. **Department Scope**: Does the officer's assigned department match the case department (`REVENUE`, `EPFO`, `GRIEVANCE`)?
3. **Jurisdiction Scope**: Does the officer's administrative jurisdiction cover the case's geographic jurisdiction?
4. **Ownership Scope**: If the actor is a `CITIZEN`, does their `citizen_id` match `case.citizen_id`?
5. **State Guard**: Is the case currently in a state that permits this action?

### 2.2 Versioned Workflow State Engine
Workflows are defined as declarative immutable versioned data structures. Each service maps to a `workflow_version`:
- `INCOME_CERTIFICATE_V1`
- `EPFO_CLAIM_V1`
- `PUBLIC_GRIEVANCE_V1`

Every workflow transition specifies:
- `action`: Name of the triggering action (`VERIFY`, `REQUEST_CORRECTION`, `FORWARD`, `APPROVE`, `REJECT`).
- `from_state` $\to$ `to_state`.
- `allowed_roles`: Explicit list of roles capable of triggering the transition.
- `guards`: Preconditions (e.g., all mandatory documents must be in `VERIFIED` state before `APPROVE` is allowed).
- `citizen_visible_status`: Citizen-friendly milestone string.
- `citizen_action_required`: Boolean flag indicating citizen intervention needed.

### 2.3 Quarantined Document Management Engine
To eliminate file-based vulnerabilities and premature verification:
1. Citizens request an upload ticket for a specific requirement.
2. The file is written to a quarantined private local storage path.
3. A validation worker validates MIME type (e.g., PDF, JPEG, PNG), checks file size limits ($\le 5\text{MB}$), and performs synthetic malware scanning.
4. Clean files transition to `AVAILABLE` and are attached to the case.
5. Verification officers inspect files and mark them `VERIFIED` or `REPLACEMENT_REQUIRED`.
6. Deficient files trigger an action requirement without invalidating unaffected documents.

### 2.4 Tamper-Evident Audit Event Ledger
Every state transition, officer note, or citizen correction appends an immutable audit event:
$$\text{EventHash}_N = \text{SHA256}(\text{EventHash}_{N-1} + \text{CaseID} + \text{ActorID} + \text{Action} + \text{OldState} + \text{NewState} + \text{Timestamp} + \text{PayloadHash})$$

This creates a verifiable cryptographic chain for each case, ensuring no administrative action can be repudiated or silently modified.

### 2.5 Transactional Outbox Notification Pattern
Whenever a workflow event transitions state, a notification record is written to `notification_outbox` in the **exact same database transaction**. An asynchronous processor dispatches in-app, SMS (mock), and email (mock) alerts reliably without two-phase commit risks.
