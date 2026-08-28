# 28 — JANSAHAY Implementation & Hardening Plan

**Document Version**: 1.1.0  
**Status**: COMPLETED & VERIFIED (12/12 Automated Security Tests Passing)  
**Role Scope**: Lead Product Engineer, Principal Architect, Security Engineer, UX Engineer, AI Engineer, QA Lead  

---

## 1. Architectural Principles & Hackathon Boundary

1. **Hackathon Boundary (Absolute)**:
   - 100% synthetic citizen profiles, synthetic officers, synthetic UANs, mock document numbers, and quarantined simulated scans.
   - Zero connection to live government systems, real Aadhaar/PAN/EPFO, or live payment/OTP gateways.
   - Clear disclosure banners embedded on all interfaces.

2. **Unified Core Engine**:
   - **ONE Universal Case Engine** (`Case` model) and **ONE Declarative Workflow State Machine** (`WorkflowEngine`) powering all services: Statutory Certificates (Income, Domicile), EPFO Claim Transfer, and Civic Grievances.
   - **Centralized Contextual Authorization** (`can(actor, action, resource)`) with Default Deny.
   - **Tamper-Evident Cryptographic SHA-256 Audit Trail**.
   - **Transactional Outbox Notification Engine**.
   - **Assistive, Bounded AI Layer** with deterministic offline fallbacks.

---

## 2. Implementation & Execution Phases

### Phase 1: Security & Engine Hardening (P0) — ✅ COMPLETED
- **Central Authorization (`can()`) Hardening**: Strictly validates citizen ownership, department isolation, jurisdiction boundaries, and document object security with default-deny enforcement.
- **Admin Endpoint Protection**: `/api/v1/admin/reset-demo` and audit chain verification secured and guarded against production misuse.
- **Optimistic Concurrency & Transactional Updates**: Strict `version_id` checks with `409 Conflict` on race conditions; atomic state shift + SHA-256 audit event + notification outbox commit.

### Phase 2: Core Citizen Features & UX Polish (P0 / P1) — ✅ COMPLETED
- **"Tell Us What You Need" Citizen Entry Point**: Prominent natural language search banner with instant bounded recommendations and rationale.
- **Case Passport Component**: Clear card with public ID (`JS-2026-INC-XXXXX`), status badge, milestone dots, and reassuring copy (*"You don't need to do anything right now."*).
- **One Case — One Timeline**: 4-question plain-language breakdown (*What happened?*, *What does it mean?*, *Do I need to do anything?*, *What happens next?*).
- **Action Required & Correction Loop**: Amber deficiency card with officer notes and single-replacement upload that increments document version (`v2`) and resumes verification.

### Phase 3: Service Catalog & Parity Across Journeys (P1) — ✅ COMPLETED
- **Multi-Service Parity**:
  - Income Certificate (4-stage statutory review).
  - Domicile Certificate (continuous residency verification).
  - EPFO Online Transfer Claim (synthetic UAN & member ID).
  - Civic Infrastructure Grievance (photo attachment & municipal engineering resolution).
- **SLA & Escalation Engine**: Deterministic SLA status computation (On Track, Approaching Deadline, Escalated) with multi-level escalation workflow.

### Phase 4: Automated Security Test Matrix & Verification (P0 / P1) — ✅ COMPLETED (12/12 PASSING)
- All 12 security matrix assertions verified in `backend/tests/test_platform.py`:
  1. `test_auth_login_and_me` (JWT token & profile extraction)
  2. `test_citizen_cross_tenant_isolation` (403 Forbidden on IDOR)
  3. `test_officer_cross_department_isolation` (403 Forbidden on cross-dept)
  4. `test_officer_cross_jurisdiction_isolation` (403 Forbidden on cross-jurisdiction)
  5. `test_officer_invalid_role_action_forbidden` (403 Forbidden on illegal role action)
  6. `test_arbitrary_state_or_invalid_transition_rejected` (400/422 on state injection)
  7. `test_stale_write_optimistic_locking` (409 Conflict on concurrency)
  8. `test_unauthorized_document_download_forbidden` (403 Forbidden on doc access)
  9. `test_full_certificate_workflow_journey` (Complete 4-stage statutory journey)
  10. `test_deficiency_and_correction_loop` (Document deficiency replacement)
  11. `test_epfo_and_grievance_parity` (EPFO & Grievance journey execution)
  12. `test_ai_assist_bounded_recommendations` (Bounded AI intent matching)

### Phase 5: Documentation & Presentation Hardening — ✅ COMPLETED
- Synchronized all architecture documents and created targeted specs:
  - `docs/23-service-catalog.md`
  - `docs/24-sla-escalation.md`
  - `docs/25-case-passport.md`
  - `docs/26-ai-safety-evaluation.md`
  - `docs/27-security-test-matrix.md`
  - `README.md`

