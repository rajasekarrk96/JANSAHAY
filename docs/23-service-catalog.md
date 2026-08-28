# 23 — JANSAHAY Service Catalog & Journey Specifications

**Document Version**: 1.0.0  
**Status**: APPROVED & ACTIVE  
**Last Updated**: 2026-08-28  

---

## 1. Executive Summary

The JANSAHAY Service Catalog unifies diverse public sector citizen journeys under a single schema and declarative execution engine. Government services are categorized by citizen intent rather than bureaucratic silos, with standardized eligibility questionnaires, document requirement profiles, and statutory review chains.

---

## 2. Supported Service Profiles

### 2.1 Statutory Revenue Certificates

#### A. Income Certificate (`INCOME_CERTIFICATE`)
- **Department**: Revenue Department (`REVENUE`)
- **Statutory Authority**: Executive Magistrate / Tehsildar
- **SLA**: 7 Business Days
- **Purpose**: Statutory verification of annual household income for educational fee concessions, scholarships, and state welfare schemes.
- **Eligibility Questionnaire**:
  1. Total annual household income $\le$ ₹2,50,000 (Mandatory Boolean)
  2. Resident of assigned administrative district (Mandatory Boolean)
  3. Active identity proof available (Mandatory Boolean)
- **Document Requirements**:
  - `IDENTITY_PROOF`: Proof of Identity (Aadhaar / Voter ID) — Mandatory (max 5 MB, PDF/JPG/PNG)
  - `INCOME_PROOF`: Proof of Income (Salary Slip / Form 16 / Self-Declaration) — Mandatory (max 5 MB, PDF/JPG/PNG)
  - `RESIDENCE_PROOF`: Proof of Residence (Electricity Bill / Rent Agreement) — Mandatory (max 5 MB, PDF/JPG/PNG)
- **Workflow Path**: `SUBMITTED` $\to$ `VERIFICATION` (Front-Desk) $\to$ `DEPARTMENT_REVIEW` (Inspector) $\to$ `APPROVAL` (Tehsildar) $\to$ `RESOLVED` (Certificate Issued).

#### B. Domicile / Continuous Residence Certificate (`DOMICILE_CERTIFICATE`)
- **Department**: Revenue Department (`REVENUE`)
- **Statutory Authority**: Sub-Divisional Magistrate (SDM)
- **SLA**: 14 Business Days
- **Purpose**: Certifies permanent residency for state university quotas, government recruitment, and local welfare entitlements.
- **Eligibility Questionnaire**:
  1. Continuous residence in the NCT/State for $\ge 3$ consecutive years (Mandatory Boolean)
- **Document Requirements**:
  - `IDENTITY_PROOF`: Aadhaar Card — Mandatory
  - `CONTINUOUS_RESIDENCE`: Proof of 3-Year Continuous Stay (Utility bills, school leaving certificate, or land registry) — Mandatory
- **Workflow Path**: `SUBMITTED` $\to$ `VERIFICATION` $\to$ `DEPARTMENT_REVIEW` $\to$ `APPROVAL` $\to$ `RESOLVED`.

---

### 2.2 Social Security & Provident Fund

#### EPFO Online Transfer Claim (`EPFO_CLAIM_TRANSFER`)
- **Department**: Employees' Provident Fund Organisation (`EPFO`)
- **Authority**: Section Supervisor / Assistant PF Commissioner
- **SLA**: 10 Business Days
- **Purpose**: Online transfer of accumulated provident fund balances and service history from a past employer establishment to the active employment account.
- **Form Data Requirements**:
  - `uan`: 12-digit Universal Account Number (Synthetic test UAN: `100982718291`)
  - `prev_member_id`: Previous Member ID (e.g. `DLCPM001928300001`)
- **Document Requirements**:
  - `UAN_MEMBER_PROOF`: Member Passbook copy or Attested Service Certificate — Mandatory
- **Workflow Path**: `SUBMITTED` $\to$ `VERIFICATION` $\to$ `DEPARTMENT_REVIEW` $\to$ `APPROVAL` $\to$ `RESOLVED`.

---

### 2.3 Civic Grievances & Municipal Redressal

#### Public Infrastructure & Civic Grievance (`STREET_LIGHT_GRIEVANCE`)
- **Department**: Public Grievance Redressal Cell (`PUBLIC_GRIEVANCE`)
- **Authority**: Grievance Redressal Nodal Officer / Municipal Engineer
- **SLA**: 5 Business Days
- **Purpose**: Direct intake and time-bound rectification of public infrastructure defects (broken streetlights, potholes, drainage overflows, public sanitation).
- **Form Data Requirements**:
  - `landmark`: Physical location reference (e.g., *Karol Bagh Metro Pillar 140*)
  - `description`: Defect description and impact details
- **Document Requirements**:
  - `SITE_PHOTO`: Geo-tagged site photo or physical landmark evidence — Optional
- **Workflow Path**: `SUBMITTED` $\to$ `VERIFICATION` $\to$ `DEPARTMENT_REVIEW` $\to$ `RESOLVED`.

---

## 3. Declarative Service Schema (`Service` Model)

```json
{
  "id": "uuid-v4",
  "code": "INCOME_CERTIFICATE",
  "title": "Income Certificate",
  "category": "CERTIFICATES",
  "department_id": "dept-uuid",
  "sla_days": 7,
  "eligibility_criteria_json": {
    "description": "Statutory proof of annual household income...",
    "questions": [
      {"id": "q1", "text": "Is your total annual household income less than ₹2,50,000?", "type": "boolean", "required": true}
    ]
  },
  "is_active": true
}
```

---

## 4. Extension Pattern for New Services

To onboard a new public service to JANSAHAY:
1. Define a `Service` entry with unique `code` and SLA timeline.
2. Define `ServiceRequirement` records for mandatory and optional document proofs.
3. Link or inherit a `WorkflowDefinition` state transition graph.
4. Zero code rewrite is required in the backend API or citizen UI.
