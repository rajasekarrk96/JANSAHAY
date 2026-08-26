# 01 — JANSAHAY Product Requirements Document (PRD)

## 1. Product Goals & Personas

### 1.1 Personas
| Persona | Role Identifier | Goals & Responsibilities |
|---|---|---|
| **Citizen** | `CITIZEN` | Discover services, understand prerequisites, submit applications/grievances, track status in plain language, respond to correction notices. |
| **Verification Officer** | `VERIFICATION_OFFICER` | Frontline review of citizen identities, document legibility, baseline criteria compliance within their jurisdiction. |
| **Department Officer** | `DEPARTMENT_OFFICER` | In-depth scrutiny of statutory validity, revenue/record checks, and recommendation formulation. |
| **Senior / Approving Officer** | `APPROVING_OFFICER` | Final statutory authority to grant certificates, approve benefit disbursals, or issue formal rejections with legal rationale. |
| **System Administrator** | `SYSTEM_ADMIN` | Configures services, versions workflow state machines, registers officers into jurisdictions/departments, audits system integrity. |

---

## 2. Functional Requirements (FR)

### 2.1 Citizen Experience
- **FR-CIT-01 (Service Discovery & Eligibility)**: Citizens can search and filter public services by category (Certificates, Social Security, Revenue, Grievance) and complete dynamic eligibility questionnaires before filing.
- **FR-CIT-02 (Dynamic Document Checklist)**: Upon answering eligibility questions, the system must generate an individualized checklist specifying document types, acceptable formats, and maximum sizes.
- **FR-CIT-03 (Quarantined Document Upload)**: Citizens upload documents into a secure sandbox where simulated antivirus, MIME-type verification, and size checks occur before promotion to application attachment.
- **FR-CIT-04 (Atomic Case Submission)**: Upon submission, a unique public tracking ID (`JS-2026-XXXXX`) is generated and an immutable audit event is recorded.
- **FR-CIT-05 (Real-time Timeline & Plain Language Status)**: Citizens see an interactive step-tracker translating internal workflow states into plain-language citizen statuses (e.g., `DEPARTMENT_REVIEW` $\to$ "Under Desk Scrutiny with Revenue Officer").
- **FR-CIT-06 (Action-Required Correction Center)**: When an officer marks a document as defective, the case state updates to `ACTION_REQUIRED`, notifying the citizen with specific officer remarks and enabling targeted document replacement.

### 2.2 Officer Experience
- **FR-OFF-01 (Role & Jurisdiction Queue Filtering)**: Officers only see cases matching their designated department (`REVENUE`, `EPFO`, `PUBLIC_GRIEVANCE`) and jurisdiction (`DISTRICT_DELHI_CENTRAL`, etc.).
- **FR-OFF-02 (Document Inspection & Deficiency Marking)**: Officers can inspect uploaded files, verify validity, or flag specific documents as `REPLACEMENT_REQUIRED` with mandatory notes.
- **FR-OFF-03 (Explicit Action Transitions)**: State transitions cannot be set arbitrarily. Officers can only invoke explicit permitted actions (`VERIFY`, `FORWARD`, `REQUEST_CORRECTION`, `APPROVE`, `REJECT`).
- **FR-OFF-04 (Audit History Visibility)**: Officers can inspect the chronological, tamper-evident timeline of prior reviews, officer notes, and timestamps.

### 2.3 Universal Workflow Engine
- **FR-WF-01 (Single Engine Multi-Service)**: The same state machine engine drives Certificate Issuance, EPFO Redressal, and Public Grievances via declarative versioned schemas.
- **FR-WF-02 (Optimistic Concurrency Control)**: All workflow actions must require a case `version_id`. Stale updates must fail with `409 Conflict`.
- **FR-WF-03 (Transactional Integrity)**: Case updates, workflow transitions, document status shifts, audit ledger entries, and outbox notifications must execute within a single atomic database transaction.

### 2.4 Assistive AI Services
- **FR-AI-01 (Discovery & Eligibility Assistant)**: Natural language conversational assistant answering queries about requirements and guiding users to the correct service.
- **FR-AI-02 (Grievance Drafting Assistant)**: Assists citizens in structuring unstructured complaints into clear, categorizeable departmental grievances.
- **FR-AI-03 (Zero Decision Governance)**: AI cannot modify case states, approve/reject applications, or alter database records.

---

## 3. Non-Functional Requirements (NFR)

### 3.1 Security & Access Control
- **NFR-SEC-01 (Default Deny)**: Contextual RBAC policy `can(actor, action, resource)` must deny all access unless explicitly granted.
- **NFR-SEC-02 (Cross-Tenant Isolation)**: Citizens can NEVER view or modify cases belonging to other citizens (`403 Forbidden`).
- **NFR-SEC-03 (Tamper-Evident Ledger)**: Case events must be hashed with SHA-256 and cryptographically chained to the previous event hash.

### 3.2 Performance & Responsiveness
- **NFR-PERF-01**: API response times for case lookups and workflow transitions must be $< 200\text{ms}$ at p95 under standard loads.
- **NFR-PERF-02**: Frontend initial load $< 1.5\text{s}$ with smooth micro-animations, accessible colors, and WCAG AA contrast compliance.

### 3.3 Reliability & Safety
- **NFR-REL-01**: Seed data and state reset endpoints for demo readiness without requiring database recreation.
- **NFR-REL-02**: Strictly synthetic datasets complying with Indian public safety and hackathon boundaries.
