# JANSAHAY — Citizen-First Public-Service Journey & Secure Government Workflow Engine

![JANSAHAY Architecture & Demo](https://img.shields.io/badge/Platform-JANSAHAY-0f172a?style=for-the-badge)
![Security Matrix](https://img.shields.io/badge/Security-Contextual%20RBAC%20%7C%20SHA--256%20Ledger-059669?style=for-the-badge)
![Compliance](https://img.shields.io/badge/Compliance-100%25%20Synthetic%20Mock%20Sandbox-d97706?style=for-the-badge)

> **"Government services are organized around departments. JANSAHAY organizes them around the citizen's goal."**  
> **"The case moves through the government workflow. The citizen should not have to chase individual officers."**

---

## 🏛️ Executive Summary

**JANSAHAY** is an Indian public service experience platform built from the ground up on **ONE Universal Case Engine** and **ONE Declarative State Machine Engine**. It unifies statutory certificates (Income, Domicile), social security transfers (EPFO), and civic infrastructure grievances into a transparent, citizen-centric journey.

---

## 🛡️ Hackathon Safety & Compliance Boundary

JANSAHAY is an **independent prototype** built solely for evaluation and innovation benchmarks:
- **100% Synthetic Data**: Citizen profiles, Aadhaar last-4 digits, employee codes, UANs, and test documents are synthetic mock data.
- **Zero Live Integrations**: No connection to live UIDAI, DigiLocker, NSDL, EPFO, or payment gateways.
- **Quarantined Sandbox**: All document uploads are scanned in an isolated sandbox.
- **Bounded Assistive AI**: Natural language assistant helps with service discovery and eligibility without any decision-making or state-modification authority.

---

## 🚀 Key Architectural Capabilities

1. **Universal State Machine Engine**: Single runtime engine powering Certificate Issuance, EPFO claim transfers, and Public Grievances via declarative versioned schemas.
2. **Contextual RBAC (`can(actor, action, resource)`)**: Enforces department scope, jurisdiction boundaries, role capabilities, and citizen case isolation with a strict **Default-Deny** policy.
3. **Tamper-Evident SHA-256 Audit Ledger**: Every state transition cryptographically chains to prior event hashes ($H_N = \text{SHA256}(H_{N-1} + \dots)$) with automated verification tools.
4. **Quarantined Document Pipeline**: Multi-stage lifecycle (`UPLOAD_REQUESTED` $\to$ `QUARANTINED` $\to$ `VALIDATING` $\to$ `SCAN_PASSED` $\to$ `AVAILABLE` $\to$ `VERIFIED` / `REPLACEMENT_REQUIRED`).
5. **Action-Required Citizen Correction Loop**: Officers can flag defective documents without rejecting the entire application; citizens upload replacements directly to resume verification.
6. **Optimistic Concurrency Control**: All state transitions enforce `version_id` checks to prevent race conditions (`409 Conflict`).

---

## ⚡ Quickstart Guide

### 1. Backend Setup & Run
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python -m app.db.init_db
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

### 2. Run Automated Pytest Security Matrix
```bash
pytest backend/tests/test_platform.py -v
```

---

## 👥 Pre-Seeded Demo Personas (1-Click Switcher)

| Username | Role | Full Name | Department / Desk |
|---|---|---|---|
| `citizen_rahul` | `CITIZEN` | Rahul Sharma | Central Delhi Resident |
| `vo_delhi_rev` | `VERIFICATION_OFFICER` | Sunil Verma | Desk `REV-VO-401` (Revenue) |
| `do_delhi_rev` | `DEPARTMENT_OFFICER` | Priya Nair | Desk `REV-DO-204` (Revenue) |
| `ao_delhi_rev` | `APPROVING_OFFICER` | Rajesh Kumar | Tehsildar Desk `REV-AO-101` |
| `vo_epfo_delhi` | `VERIFICATION_OFFICER` | Amit Roy | EPFO Desk `EPF-VO-882` |
| `do_grievance_delhi` | `DEPARTMENT_OFFICER` | Sanjay Gupta | Grievance Cell `GRV-DO-512` |

*Password for all personas*: `Password123!`

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
