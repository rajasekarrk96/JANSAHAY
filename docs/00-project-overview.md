# 00 — JANSAHAY Project Overview

## 1. Executive Summary
**JANSAHAY** is a citizen-first public service journey and secure government workflow platform designed for the Indian public administration context. 

Traditional e-governance solutions mirror bureaucratic organizational silos, forcing citizens to navigate fragmented departmental portals, decipher obscure bureaucratic nomenclature, repeatedly submit redundant documentation, and physically pursue individual desk officers.

JANSAHAY inverts this paradigm by establishing a **single universal case engine** and **declarative workflow state machine**. Government services are organized entirely around citizen outcomes, while public officials interact through a unified, role-governed, auditable dispatch and verification workspace.

---

## 2. Problem Statement
1. **Departmental Silos vs Citizen Intent**: Citizens seeking an Income Certificate, Domicile Certificate, Pension transfer, or Grievance Redressal encounter disjointed systems with differing UX standards, authentication hurdles, and disconnected status terminology.
2. **Opaque Case Lifecycles**: Application statuses such as "Under Process" provide zero visibility into which desk or verification phase a case is situated, leaving citizens vulnerable to administrative delays.
3. **Deficiency & Correction Friction**: Minor document inaccuracies or unreadable scans frequently lead to outright case rejections rather than targeted, actionable correction requests.
4. **Dispersed Accountability**: Officers lack unified queue prioritization, jurisdiction-scoped access controls, and tamper-evident audit trails that verify case progression.

---

## 3. Core Product Principles
> **"Government services are organized around departments. JANSAHAY organizes them around the citizen's goal."**

> **"The case moves through the government workflow. The citizen should not have to chase individual officers."**

---

## 4. Product Scope & Personas

### 4.1 Target Personas
- **The Citizen (Aadhaar/Mobile Authenticated)**:
  - Discovers services based on life events and eligibility checks.
  - Receives tailored, step-by-step document checklists before filing.
  - Submits synthetic, validated documents into a secure quarantine pipeline.
  - Tracks real-time public case timelines (`JS-2026-XXXXX`).
  - Corrects deficient documents in a dedicated Citizen Action Center without case forfeiture.
- **Verification Officer (Field / Front-Desk Reviewer)**:
  - Reviews assigned applications, inspects verified document previews, and performs initial statutory checks.
  - Executes explicit atomic actions (`VERIFY`, `REQUEST_CORRECTION`, `REJECT`).
- **Department Officer (Desk / Scrutiny In-Charge)**:
  - Conducts departmental scrutiny, cross-checks revenue/welfare records, and prepares case findings.
  - Executes actions (`FORWARD`, `REQUEST_CORRECTION`, `REJECT`).
- **Approving Officer (Tahsildar / Competent Authority)**:
  - Issues final administrative approval or formal reasoned rejection.
  - Attaches digital resolution notes and triggers certificate dispatch.
- **System Administrator**:
  - Manages jurisdiction boundaries, officer department scopes, service workflow versions, and inspects tamper-evident audit ledgers.

---

## 5. MVP Scope vs Out-of-Scope

### In-Scope (MVP Core)
- **Unified Engine**: ONE universal Case Engine + ONE Workflow State Engine powering:
  1. **Certificate Application Journey** (Deepest end-to-end journey: Eligibility $\to$ Document Checklist $\to$ Quarantined Upload $\to$ Verification $\to$ Department Review $\to$ Approval $\to$ Citizen Certificate Generation).
  2. **EPFO Claim Redressal Journey** (Unified verification and settlement tracking).
  3. **Government Public Grievance Journey** (Triage $\to$ Department Assignment $\to$ Redressal $\to$ Resolution Closure).
- **Contextual RBAC**: `can(actor, action, resource)` enforcing Department, Jurisdiction, and Case Stage authorization.
- **Tamper-Evident Audit Ledger**: SHA-256 hash-chained immutable event ledger recording every state change and actor action.
- **Quarantined Document Management**: Secure multi-state lifecycle (`UPLOAD_REQUESTED` $\to$ `QUARANTINED` $\to$ `VALIDATING` $\to$ `SCAN_PASSED` $\to$ `AVAILABLE` $\to$ `VERIFIED` / `REPLACEMENT_REQUIRED`).
- **Citizen Correction Loop**: Non-destructive document replacement resuming workflow execution at the exact pending stage.
- **Assistive AI Boundary**: Bounded AI assistant for natural language service discovery, eligibility explanations, and grievance drafting with zero decision-making authority.

### Out-of-Scope (Hackathon Safety Boundaries)
- Direct integration with live state or central government APIs (DigiLocker, UIDAI, NSDL, EPFO live portals).
- Live financial transaction gateways or treasury payment processing.
- Storage or processing of real citizen PII, real Aadhaar numbers, or real government credentials.

---

## 6. Synthetic Data & Non-Government Status Policy
JANSAHAY is an independent technology prototype built exclusively for demonstration and evaluation purposes. All citizen records, officer identities, document uploads, scanning pipelines, and departmental decisions operate on synthetic, sandboxed datasets.
