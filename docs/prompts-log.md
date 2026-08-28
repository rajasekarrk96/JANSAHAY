# JANSAHAY — Prompts & Requirements Log

This document records the user prompts and instructions provided for the JANSAHAY project upgrade and hardening.

---

## Prompt 1: Hackathon Upgrade, Hardening & Finalization Charter

**Timestamp**: 2026-08-28T11:20:20+05:30  
**Full Text**:
```text
# JANSAHAY — UPGRADE, HARDENING & HACKATHON FINALIZATION PROMPT

You are now the Lead Product Engineer, Principal Architect, Security Engineer, UX Engineer, AI Engineer, and QA Lead for the JANSAHAY project.
The repository already contains a JANSAHAY implementation, documentation, backend, frontend, tests, and mock data.
Your job is to upgrade the existing project into a polished, secure, demonstrably working hackathon submission.
Do not throw away working functionality.
Do not rebuild everything blindly.
First inspect what exists, understand it, identify gaps, then upgrade it systematically.

1. PRODUCT VISION
JANSAHAY is: "A citizen-to-resolution layer for Indian public services."
"Government services are organized around departments. JANSAHAY organizes them around the citizen's goal."
"The case moves through the government workflow. The citizen should not have to chase individual officers."
JANSAHAY should feel like one simple citizen platform, while internally providing a secure reusable government workflow engine.

2. HACKATHON BOUNDARY — ABSOLUTE
- Independent prototype.
- NEVER connect to live government systems, live Aadhaar, live PAN, live EPFO, real OTPs, real payment systems.
- Use 100% synthetic users, synthetic officers, synthetic UANs, mock documents.
- Clearly identify simulated functionality.

3. EXECUTION RULE: INSPECT -> AUDIT -> PLAN -> IMPLEMENT -> TEST -> FIX -> VERIFY -> DOCUMENT.

4. PRESERVE GOOD WORK.

5. TARGET ARCHITECTURE: Modular monolith with Universal Case Engine, Declarative State Machine, Central Authorization can(actor, action, case), Quarantined Documents Pipeline, SHA-256 Audit Ledger, Notification Outbox.

6. PRIORITY ORDER:
- P0: Certificate end-to-end journey, Secure workflow engine, Citizen timeline, Officer routing, Server-side authorization, Case isolation, Workflow transition security, Audit integrity, Document security, Production/demo build.
- P1: Service Catalog, Personalized document checklist, Correction loop, EPFO configuration, Grievance configuration, Case Passport, SLA/escalation engine, Notification outbox, Security test matrix.
- P2: AI service discovery, AI complaint structuring, AI status explanation, Accessibility improvements, Mobile/low-bandwidth optimization, Visual polish, Demo experience.

7. KEY UX/PRODUCT FEATURES:
- "Tell us what you need" primary entry point
- Service Catalog
- Personalized checklist
- Case Passport
- One Case — One Timeline
- Status explanation ("What happened?", "What does it mean?", "Do I need to do anything?", "What happens next?")
- Action Required & Correction loop
- Universal Case Engine
- Workflow Engine (versioned, declarative, guarded, no arbitrary state acceptance)
- Secure Officer routing
- Central Authorization can(actor, action, resource) with Default Deny
- Security Test Matrix (IDOR, cross-dept, cross-jurisdiction, invalid action, stale conflict 409, doc security)
- Concurrency (Optimistic locking 409)
- Transactional Workflow
- Tamper-evident Audit (SHA-256 chaining)
- Document Security & Versioning
- SLA / Escalation engine
- Notification Outbox
- Assistive Bounded AI with deterministic fallbacks
- Grievance & EPFO Journeys
- Accessibility & Low-Bandwidth UI
- Demo personas & Demo reset
- Documentation updates
```

---

## Prompt 2: Save Implementation & Prompts in docs/ and Proceed

**Timestamp**: 2026-08-28T11:22:55+05:30  
**Full Text**:
```text
save the implementation in .md in doc and save every prompts we give then proceed
```

---

## Prompt 3: Continue Hardening Plan Execution

**Timestamp**: 2026-08-28T11:32:11+05:30  
**Full Text**:
```text
conti with 28-implementation-hardening-plan.md
```

**Actions Executed & Verified**:
1. Completed Phase 1 & Phase 4: Extended `backend/tests/test_platform.py` and `backend/app/db/init_db.py` to cover all 12 security test vectors (cross-jurisdiction isolation, invalid role action rejection, state injection prevention, unauthorized document download protection).
2. Ran `pytest backend/tests/` with 12/12 passing tests (100% success).
3. Created specialized architecture documents:
   - `docs/23-service-catalog.md` (Unified catalog, eligibility schemas, requirements)
   - `docs/24-sla-escalation.md` (Deterministic SLA tracking & escalation state machine)
   - `docs/25-case-passport.md` (4-question citizen transparency UX & correction loop)
   - `docs/26-ai-safety-evaluation.md` (Assistive AI guardrails, intent matching, offline safety)
   - `docs/27-security-test-matrix.md` (Automated 12-vector test suite matrix & SHA-256 ledger integrity)
4. Synchronized `README.md` and updated `docs/28-implementation-hardening-plan.md` to `COMPLETED & VERIFIED`.

---

## Prompt 4: Comprehensive Documentation & README Upgrade

**Timestamp**: 2026-08-28T11:36:00+05:30  
**Full Text**:
```text
update docs and readme.md
```

**Actions Executed & Verified**:
1. Conducted an exhaustive audit and alignment pass across all 28 architecture and operational documents.
2. Synchronized `README.md` with complete architectural diagram, persona reference, test suite execution results, API endpoint directory, and full document table of contents.
3. Updated core specifications (`docs/02-architecture.md`, `docs/04-database-schema.md`, `docs/05-api-specification.md`, `docs/06-authentication-authorization.md`, `docs/07-security.md`, `docs/08-workflow-engine.md`, `docs/17-demo.md`, `docs/20-decision-log.md`).

---

## Prompt 5: Git Commit and Remote Push

**Timestamp**: 2026-08-28T11:43:53+05:30  
**Full Text**:
```text
push
```

**Actions Executed & Verified**:
1. Staged all modified backend, test, frontend, documentation, and prompt log files.
2. Created a structured git commit reflecting the hardened engine, 12-vector security test matrix, and comprehensive documentation suite.
3. Executed `git push origin main` (or tracked branch).

---

## Prompt 6: Docker Compose Build & Bcrypt Compatibility Debugging

**Timestamp**: 2026-08-28T18:53:56+05:30  
**Full Text**:
```text
ValueError: password cannot be longer than 72 bytes, truncate manually if necessary (e.g. my_password[:72])
------
failed to solve: process "/bin/sh -c python -m app.db.init_db" did not complete successfully: exit code: 1
```

**Actions Executed & Verified**:
1. Investigated root cause: `passlib` initialization probe `detect_wrap_bug` conflicting with unpinned `bcrypt>=4.1.0` strict length validation in Python 3.11 container.
2. Updated `backend/requirements.txt` to pin `bcrypt<4.1.0`.
3. Executed `docker compose build backend`, verifying that `init_db` completed cleanly with synthetic seed data and the container image built with exit code `0`.

---

## Prompt 7: Git Commit & Remote Push

**Timestamp**: 2026-08-28T18:54:45+05:30  
**Full Text**:
```text
push to git
```

**Actions Executed & Verified**:
1. Staged `backend/requirements.txt`.
2. Committed with `fix(backend): pin bcrypt<4.1.0 to resolve passlib initialization bug in Docker build` (`6829538`).
3. Successfully pushed to GitHub repository `origin/main`.

---

## Prompt 8: Comprehensive Documentation & README Update

**Timestamp**: 2026-08-28T18:58:59+05:30  
**Full Text**:
```text
update readme.md and other docs
```

**Actions Executed & Verified**:
1. Updated `README.md` to highlight 1-command Docker Compose execution (`docker compose up --build`), live endpoint catalog, architecture diagrams, and testing results.
2. Updated `docs/16-deployment.md` with complete Docker Compose quickstart, volume management, service endpoints, and troubleshooting guides.
3. Added ADR 04 (Bcrypt Pinning) and ADR 05 (Single-Port Embedded Full-Stack Delivery) to `docs/20-decision-log.md`.
4. Synchronized `docs/prompts-log.md` with all development and debugging cycles.
