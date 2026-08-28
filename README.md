# JANSAHAY — Citizen-First Public-Service Journey & Secure Government Workflow Engine

![JANSAHAY Architecture & Demo](https://img.shields.io/badge/Platform-JANSAHAY-0f172a?style=for-the-badge)
![Security Matrix](https://img.shields.io/badge/Security-Contextual%20RBAC%20%7C%20SHA--256%20Ledger-059669?style=for-the-badge)
![Compliance](https://img.shields.io/badge/Compliance-100%25%20Synthetic%20Mock%20Sandbox-d97706?style=for-the-badge)
![Tests](https://img.shields.io/badge/Automated%20Tests-12%2F12%20PASSING-blue?style=for-the-badge)

> **"Government services are organized around departments. JANSAHAY organizes them around the citizen's goal."**  
> **"The case moves through the government workflow. The citizen should not have to chase individual officers."**

---

## 🏛️ Executive Summary & Product Vision

In the traditional administrative apparatus, citizens navigate fragmented departmental portals, opaque file numbers, and physical office queues with no clarity on who holds their application or what action is needed.

**JANSAHAY** replaces this friction with an end-to-end citizen-to-resolution layer:
1. **To the Citizen**: One clean, unified platform offering natural-language service discovery, a personalized document checklist, a transparent **Case Passport**, a plain-language milestone timeline (*What happened? What does it mean? Do I need to do anything? What happens next?*), and a single-file deficiency correction loop.
2. **To the Government**: A multi-departmental, declarative workflow engine powered by centralized contextual authorization (`can(actor, action, resource)`), optimistic concurrency control, quarantined document processing, and a tamper-evident SHA-256 cryptographic audit ledger.

---

## 🛡️ Hackathon Safety & Compliance Boundary (Absolute)

JANSAHAY is an **independent prototype** built strictly for evaluation and innovation benchmarks:
- **100% Synthetic Data**: Citizen profiles, mock Aadhaar last-4 digits, employee codes, UANs, and mock document scans.
- **Zero Live Connections**: No integration with real UIDAI, DigiLocker, NSDL, EPFO, or live payment/SMS gateways.
- **Quarantined Sandbox**: All document uploads are scanned in an isolated sandbox.
- **Bounded Assistive AI**: Natural language assistant helps with service discovery and eligibility without any autonomous decision-making or state-mutation authority.

---

## 🏗️ System Architecture

```mermaid
graph TD
    subgraph Client Layer
        CP[Citizen Portal: Natural Language Entry & Case Passport]
        OP[Officer Scrutiny & Approval Desk]
        AP[Admin & Audit Ledger Verification Console]
    end

    subgraph API Gateway & Security Layer
        API[FastAPI Gateway / OpenAPI Router]
        AUTH[Contextual RBAC Guard: can(actor, action, resource)]
    end

    subgraph Core Business Engines
        CE[Universal Case Engine]
        WE[Declarative Workflow State Machine]
        DE[Quarantined Document Engine]
        AE[Tamper-Evident SHA-256 Audit Ledger]
        NE[Transactional Outbox Notifications]
        AIE[Assistive Bounded AI Intent Layer]
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

## 🚀 Key Architectural Capabilities

1. **Universal Case Engine (`Case` Model)**: A single database entity and state machine powering Statutory Certificates (Income, Domicile), Social Security (EPFO Transfers), and Civic Grievances.
2. **Contextual RBAC (`can(actor, action, resource)`)**: Enforces department scope, jurisdiction boundaries, role capabilities, and citizen case ownership with a strict **Default-Deny** policy.
3. **Tamper-Evident SHA-256 Audit Ledger**: Every state transition cryptographically chains to prior event hashes ($H_N = \text{SHA256}(H_{N-1} + \dots)$) with automated verification endpoints.
4. **Action-Required Correction Loop**: Officers flag defective documents with clear notes without rejecting the entire application; citizens upload single replacement files to resume verification.
5. **Optimistic Concurrency Control**: All state transitions enforce `version_id` checks to prevent race conditions (`409 Conflict`).
6. **Assistive Bounded AI**: Deterministic service intent discovery with zero cloud API dependencies and zero hallucination risk.

---

## 🔒 Automated Security Test Matrix (12/12 Passing)

The platform is continuously validated against a comprehensive 12-vector security test suite (`backend/tests/test_platform.py`):

| # | Test Vector | Security Assertion | Result |
| :---: | :--- | :--- | :---: |
| **1** | JWT Authentication & Me | Generates valid claims & retrieves user context | ✅ PASS |
| **2** | Citizen IDOR Isolation | Citizen A cannot access Citizen B's cases (`403`) | ✅ PASS |
| **3** | Cross-Department Isolation | EPFO Verifier cannot access Revenue cases (`403`) | ✅ PASS |
| **4** | Cross-Jurisdiction Isolation | South Delhi officer cannot access Central Delhi cases (`403`) | ✅ PASS |
| **5** | Role Action Enforcement | Verification Officer cannot execute `APPROVE` (`403`) | ✅ PASS |
| **6** | State Injection Prevention | Arbitrary/unregistered action payloads rejected (`400/422`) | ✅ PASS |
| **7** | Optimistic Concurrency | Stale `version_id` writes return conflict (`409`) | ✅ PASS |
| **8** | Quarantined Document Security | Unauthorized direct download of case docs rejected (`403`) | ✅ PASS |
| **9** | E2E 4-Stage Workflow Journey | Citizen $\to$ VO $\to$ Inspector $\to$ Tehsildar Approval | ✅ PASS |
| **10** | Document Deficiency Loop | Defective doc flag $\to$ citizen replacement upload $\to$ auto-resume | ✅ PASS |
| **11** | Multi-Service Parity | EPFO claims & Civic Grievances run on universal engine | ✅ PASS |
| **12** | Bounded AI Intent Discovery | Natural language prompt resolves to catalog service | ✅ PASS |

---

## 👥 Pre-Seeded Demo Personas (1-Click Switcher)

| Username | Role | Full Name | Department / Desk / Jurisdiction |
|---|---|---|---|
| `citizen_rahul` | `CITIZEN` | Rahul Sharma | Central Delhi Resident (Applicant) |
| `citizen_anita` | `CITIZEN` | Anita Patel | South Delhi Resident |
| `vo_delhi_rev` | `VERIFICATION_OFFICER` | Sunil Verma | Desk `REV-VO-401` (Central Delhi Revenue) |
| `do_delhi_rev` | `DEPARTMENT_OFFICER` | Priya Nair | Desk `REV-DO-204` (Central Delhi Revenue) |
| `ao_delhi_rev` | `APPROVING_OFFICER` | Rajesh Kumar | Tehsildar Desk `REV-AO-101` (Central Delhi) |
| `vo_south_delhi_rev` | `VERIFICATION_OFFICER` | Vikram Sethi | Desk `REV-VO-402` (South Delhi Revenue) |
| `vo_epfo_delhi` | `VERIFICATION_OFFICER` | Amit Roy | EPFO Desk `EPF-VO-882` (Central Delhi) |
| `do_grievance_delhi` | `DEPARTMENT_OFFICER` | Sanjay Gupta | Grievance Cell `GRV-DO-512` (Central Delhi) |
| `admin` | `SYSTEM_ADMIN` | Platform Administrator | Central IT Operations & Audit Verification |

*Password for all personas*: `Password123!`

---

## ⚡ Quickstart Guide

### Option A: Docker Compose (Recommended Zero-Setup)
Run the complete backend, database, synthetic seed data, and embedded web application in an isolated container:
```bash
docker compose up --build
```
- **Web App & Citizen Portal**: [http://localhost:8000](http://localhost:8000)
- **Interactive OpenAPI Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc API Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Option B: Local Python Development
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python -m app.db.init_db
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your web browser.

### Run Automated Security Test Suite
```bash
pytest backend/tests/test_platform.py -v
```

---

## 📚 Complete Engineering Documentation (`docs/`)

- [00 — Project Overview](docs/00-project-overview.md)
- [01 — Product Requirements](docs/01-product-requirements.md)
- [02 — System Architecture](docs/02-architecture.md)
- [03 — System Design & Lifecycles](docs/03-system-design.md)
- [04 — Database Schema](docs/04-database-schema.md)
- [05 — REST API Specification](docs/05-api-specification.md)
- [06 — Authentication & Authorization](docs/06-authentication-authorization.md)
- [07 — Security & Threat Model](docs/07-security.md)
- [08 — Versioned Workflow Engine](docs/08-workflow-engine.md)
- [09 — Case Management](docs/09-case-management.md)
- [10 — Quarantined Document Management](docs/10-document-management.md)
- [11 — Assistive AI Architecture](docs/11-ai-architecture.md)
- [12 — Transactional Outbox Notifications](docs/12-notifications.md)
- [13 — UI/UX Design System](docs/13-ui-ux.md)
- [14 — Accessibility (WCAG 2.1 AA)](docs/14-accessibility.md)
- [15 — Automated Testing Strategy](docs/15-testing.md)
- [16 — Deployment & Run Guide](docs/16-deployment.md)
- [17 — Demo Walkthrough Script](docs/17-demo.md)
- [18 — Synthetic Mock Data Dictionary](docs/18-mock-data.md)
- [19 — Phased Development Plan](docs/19-development-plan.md)
- [20 — Architectural Decision Log (ADR)](docs/20-decision-log.md)
- [21 — Hackathon & Safety Compliance](docs/21-hackathon-compliance.md)
- [22 — Implementation & Codebase Audit](docs/22-implementation-audit.md)
- [23 — Service Catalog & Journey Specs](docs/23-service-catalog.md)
- [24 — SLA & Escalation Engine](docs/24-sla-escalation.md)
- [25 — Case Passport & Citizen Transparency](docs/25-case-passport.md)
- [26 — Assistive AI Safety & Guardrails](docs/26-ai-safety-evaluation.md)
- [27 — Automated Security Test Matrix](docs/27-security-test-matrix.md)
- [28 — Implementation Hardening Plan](docs/28-implementation-hardening-plan.md)
- [Prompts & Requirements Log](docs/prompts-log.md)
