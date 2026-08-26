# 15 — JANSAHAY Testing Strategy & Verification Matrix

## 1. Automated Test Matrix

The test suite validates both standard business flows and mandatory security negative tests:

### 1.1 Mandatory Security & Isolation Test Cases
1. `test_citizen_cross_tenant_isolation`: Citizen A attempting to view Citizen B's case is rejected with `403 Forbidden`.
2. `test_officer_cross_department_isolation`: Revenue Officer attempting to action an EPFO case is rejected with `403 Forbidden`.
3. `test_officer_cross_jurisdiction_isolation`: Delhi Central Officer attempting to action a Bangalore Urban case is rejected with `403 Forbidden`.
4. `test_invalid_state_transition`: Attempting an unpermitted transition (e.g., jumping from `SUBMITTED` directly to `RESOLVED`) is rejected with `422/400`.
5. `test_stale_write_optimistic_locking`: Submitting an action with an outdated `version_id` is rejected with `409 Conflict`.
6. `test_unauthorized_document_access`: Unauthenticated or cross-tenant document download returns `403/401`.
7. `test_tamper_evident_audit_chain`: Verifies that event SHA-256 hashes form a continuous, unbroken chain.

### 1.2 End-to-End Workflow Verification
- **Income Certificate Full Pipeline**: Citizen submit $\to$ Verifier check $\to$ Department scrutiny $\to$ Approving Officer grant $\to$ Certificate issued.
- **Deficiency & Correction Loop**: Verifier requests correction on defective doc $\to$ Case moves to `ACTION_REQUIRED` $\to$ Citizen resubmits replacement doc $\to$ Workflow resumes at `VERIFICATION`.
- **EPFO & Grievance Multi-Service Parity**: Verifies that EPFO claims and public grievances execute through identical engine code paths.
