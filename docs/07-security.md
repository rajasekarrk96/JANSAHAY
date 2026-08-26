# 07 — JANSAHAY Security & Threat Model

## 1. Threat Model & Mitigations

| Threat Vector | Severity | Attack Scenario | JANSAHAY Architectural Mitigation |
|---|---|---|---|
| **Insecure Direct Object References (IDOR)** | Critical | Citizen changes URL `case_id` to view another citizen's tax/income certificate. | Enforced in `can()` authorization guard. All case lookups filter by authenticated `citizen_id` or matching officer jurisdiction/department. |
| **State Machine Skipping** | High | Officer sends API request to jump directly from `SUBMITTED` to `RESOLVED` bypassing verification. | Backend workflow engine strictly executes declared state transition graphs. The API does not accept target states, only explicit verified actions. |
| **Race Conditions & Double Approval** | High | Two officers concurrently approve or reject the same case. | Optimistic concurrency locking via `version_id`. Stale updates fail immediately with `409 Conflict`. |
| **Malicious File Upload** | High | Attacker uploads executable or script disguised as PDF/PNG. | Quarantined multi-stage upload sandbox. Validates magic bytes, enforces strict file extensions, limits file size ($\le 5\text{MB}$), and serves only through authenticated binary endpoints with strict headers (`X-Content-Type-Options: nosniff`). |
| **Audit Log Tampering** | Critical | Rogue admin or compromised DB account edits past officer remarks to cover malfeasance. | Cryptographic SHA-256 hash chaining of audit events ($H_N = \text{SHA256}(H_{N-1} + \dots)$). Any modification invalidates downstream hashes. |
| **Prompt Injection in Assistive AI** | Medium | User enters malicious prompt instructing AI to "Approve Case JS-12345". | Assistive AI has read-only discovery context and zero execution pathways into the database or state machine. Pydantic schemas enforce rigid JSON parsing. |

---

## 2. Document Access Controls
1. No raw file paths or unauthenticated URLs are exposed to the client.
2. File retrieval requires authenticated session verifying `can(actor, VIEW_DOCUMENT, document.case)`.
3. Files are stored outside the public web root directory in a local isolated storage volume.
