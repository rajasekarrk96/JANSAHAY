# 05 — JANSAHAY REST API Specification

## 1. Global API Standards
- **Base URL**: `/api/v1`
- **Format**: JSON (`Content-Type: application/json`)
- **Authentication**: Bearer JWT (`Authorization: Bearer <token>`)
- **Error Format**:
```json
{
  "error": {
    "code": "CONFLICT_STALE_VERSION",
    "message": "The case has been modified by another officer. Please refresh your view.",
    "details": { "expected_version": 2, "provided_version": 1 }
  }
}
```

---

## 2. Authentication & Identity (`/auth`)

### `POST /auth/login`
- **Description**: Authenticate citizen, officer, or admin.
- **Request Body**:
```json
{
  "username": "citizen_rahul",
  "password": "Password123!"
}
```
- **Response `200 OK`**:
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user": {
    "id": "u-101",
    "username": "citizen_rahul",
    "role": "CITIZEN",
    "full_name": "Rahul Sharma",
    "profile_id": "c-501",
    "department": null,
    "jurisdiction": "DELHI_CENTRAL"
  }
}
```

### `GET /auth/me`
- **Description**: Return authenticated user context and accessible scope.

---

## 3. Public Services & Discovery (`/services`)

### `GET /services`
- **Query Params**: `category` (optional: `CERTIFICATES`, `SOCIAL_SECURITY`, `GRIEVANCES`)
- **Response `200 OK`**: List of available services with SLA days, department, and requirement schemas.

### `GET /services/{service_id}/eligibility`
- **Description**: Fetch dynamic eligibility questions and checklist generator rules.

---

## 4. Case Management & Workflow Execution (`/cases`)

### `POST /cases`
- **Authorization**: `CITIZEN` only.
- **Description**: Create and submit a new case (Application or Grievance).
- **Request Body**:
```json
{
  "service_id": "srv-income-cert",
  "jurisdiction_id": "jur-delhi-central",
  "form_data": {
    "applicant_name": "Rahul Sharma",
    "annual_family_income": 180000,
    "income_source": "Agriculture and Private Employment",
    "reason_for_certificate": "Higher Education Fee Concession"
  },
  "document_ids": ["doc-uuid-1", "doc-uuid-2"]
}
```
- **Response `201 Created`**:
```json
{
  "id": "case-uuid-99",
  "public_case_id": "JS-2026-INC-48192",
  "current_state": "SUBMITTED",
  "citizen_status": "Application Submitted. Awaiting Initial Verification.",
  "version_id": 1,
  "submitted_at": "2026-08-26T12:00:00Z"
}
```

### `GET /cases`
- **Authorization**: Authenticated Users.
- **Scoping**:
  - Citizens only receive their own cases.
  - Officers receive cases filtered by their assigned `department_id` and `jurisdiction_id`.
- **Query Params**: `status`, `page`, `limit`.

### `GET /cases/{id}`
- **Description**: Retrieve detailed case view, attached documents, audit trail, and allowed contextual actions.

### `POST /cases/{id}/actions/{action_name}`
- **Description**: **CRITICAL CONTRACT**: Explicit workflow action trigger (e.g., `VERIFY`, `FORWARD`, `REQUEST_CORRECTION`, `APPROVE`, `REJECT`, `RESUBMIT_DOCUMENTS`). The client does NOT set `new_state`.
- **Request Body**:
```json
{
  "version_id": 1,
  "remarks": "Income proof verified against Tahsil revenue guidelines. All criteria met.",
  "document_verifications": [
    { "document_id": "doc-uuid-1", "status": "VERIFIED" },
    { "document_id": "doc-uuid-2", "status": "VERIFIED" }
  ]
}
```
- **Response `200 OK`**:
```json
{
  "case_id": "case-uuid-99",
  "previous_state": "VERIFICATION",
  "new_state": "DEPARTMENT_REVIEW",
  "citizen_status": "Under Departmental Scrutiny with Revenue Officer",
  "version_id": 2,
  "event_hash": "a8f3b29c91...",
  "updated_at": "2026-08-26T12:15:00Z"
}
```
- **Error Codes**:
  - `403 Forbidden`: Officer lacks scope or role permissions.
  - `409 Conflict`: `version_id` does not match active DB version (optimistic lock failure).
  - `422 Unprocessable Entity`: Action guards not satisfied (e.g. attempting `APPROVE` with deficient docs).

---

## 5. Document Management (`/documents`)

### `POST /documents/upload`
- **Format**: `multipart/form-data`
- **Description**: Upload file into quarantined sandbox. Performs MIME validation, size bounds, and virus checks before linking.
- **Response `201 Created`**:
```json
{
  "document_id": "doc-uuid-1",
  "file_name": "salary_certificate.pdf",
  "status": "AVAILABLE",
  "file_size_bytes": 482910
}
```

### `GET /documents/{id}/download`
- **Authorization**: Scoped check `can(actor, VIEW_DOCUMENT, document.case)`. Returns binary stream or short-lived authenticated stream. Public static access is strictly prohibited.

---

## 6. Assistive AI & Notifications (`/ai`, `/notifications`)

### `POST /ai/assist`
- **Description**: Natural language assistant for service discovery and grievance drafting.
- **Request Body**:
```json
{
  "prompt": "I need a certificate for my daughter's college scholarship claiming our family income is under 2 lakhs. What documents do I need?",
  "session_context": { "jurisdiction": "DELHI_CENTRAL" }
}
```
- **Response `200 OK`**:
```json
{
  "recommended_service_id": "srv-income-cert",
  "service_title": "Income Certificate",
  "explanation": "To apply for an Income Certificate in Central Delhi with annual income under ₹2,00,000, you will need: 1. Aadhaar/Identity Proof, 2. Salary Slip/Self-Declaration Form, and 3. Central Delhi Residence Proof.",
  "confidence_score": 0.98
}
```

### `GET /notifications`
- **Description**: Fetch pending and delivered notification timeline for authenticated user.

---

## 7. Demo & Administration (`/admin`)

### `POST /admin/reset-demo`
- **Description**: Restores all database tables to pristine seeded demo states with synthetic citizens, officers, and test cases.
