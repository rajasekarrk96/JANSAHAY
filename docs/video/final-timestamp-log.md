# JANSAHAY — Final Timestamp & Cue Log

This document records the exact cue timestamps for the 2-minute hackathon video recording.

---

## Cue & Timeline Breakdown

```text
00:00 – 00:08  [Scene 1] Problem Statement & Citizen Hero View
00:08 – 00:18  [Scene 2] Natural Language Service Discovery ("Tell us what you need")
00:18 – 00:28  [Scene 3] Guided Eligibility & Tailored Document Checklist
00:28 – 00:38  [Scene 4] Sandboxed Document Upload & Statutory Submission
00:38 – 00:50  [Scene 5] The Case Passport & 4-Question Milestone Timeline
00:50 – 01:00  [Scene 6] Officer Scrutiny Desk & Verified Stage Transition
--------------------------------------------------------------------------------
[01:00 Marker: Transition to Technical & Security Architecture]
--------------------------------------------------------------------------------
01:00 – 01:15  [Scene 7] Universal Case Engine & Multi-Service Parity
01:15 – 01:30  [Scene 8] Contextual Authorization (RBAC) & Concurrency Locking
01:30 – 01:42  [Scene 9] Tamper-Evident SHA-256 Audit Ledger & Quarantined Pipeline
01:42 – 01:50  [Scene 10] Assistive Bounded AI with Strict Guardrails
01:50 – 01:58  [Scene 11] Synthetic Sandbox & Mock Integration Disclosure
01:58 – 02:00  [Scene 12] Final Callout & Case Passport Resolution Center
```

---

## Detailed Section Breakdown

### Part 1: Citizen Experience (00:00 – 01:00)
- **00:00 – 00:08**: Shows `Rahul Sharma (Citizen)` context banner, hero banner, and establishes the core premise: public services organized around citizen goals.
- **00:08 – 00:18**: Citizen types *"I need income proof for college fee concession"*. JANSAHAY resolves query to Statutory Income Certificate with explanation.
- **00:18 – 00:28**: Citizen answers 3 questions. System generates personalized 3-document checklist (Identity, Income, Residence).
- **00:28 – 00:38**: Documents uploaded in quarantined sandbox, validated, and submitted with declaration checkbox. Case ID `JS-2026-INC-48192` generated.
- **00:38 – 00:50**: Case Passport rendered with 5-stage milestone stepper (Submitted $\to$ Verification $\to$ Dept Review $\to$ Approval $\to$ Completed) and 4-question plain-language status card.
- **00:50 – 01:00**: Persona switched to `Sunil Verma (Verification Officer)`. Scrutiny desk verifies documents and executes state transition to `DEPARTMENT_REVIEW`.

### Part 2: How We Built It & Why (01:00 – 02:00)
- **01:00 – 01:15**: Unified multi-service catalog demonstrated across Statutory Certificates, EPFO Claim Transfers, and Civic Grievances on a single `Case` entity.
- **01:15 – 01:30**: Server-side contextual RBAC (`can(actor, action, resource)`) with department, jurisdiction, and role scoping, plus optimistic concurrency (`version_id` conflict protection).
- **01:30 – 01:42**: Tamper-evident cryptographic SHA-256 event chaining ($H_N = \text{SHA256}(H_{N-1} + \dots)$) with `Chain Intact ✓` live verification.
- **01:42 – 01:50**: Assistive bounded AI drawer demonstrated for discovery and plain-language explanation without state-mutation authority.
- **01:50 – 01:58**: Amber prototype disclosure highlighted: 100% synthetic personas, zero live government APIs.
- **01:58 – 02:00**: Concluding hold on the Case Passport resolution screen.
