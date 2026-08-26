# 08 — JANSAHAY Versioned Workflow Engine

## 1. Declarative Workflow Architecture

The core premise of JANSAHAY is **ONE workflow engine** that executes arbitrary public-service journeys defined by versioned, declarative JSON schemas.

### 1.1 State Machine Schema Specification
A workflow definition contains:
```json
{
  "service_code": "INCOME_CERTIFICATE",
  "version": 1,
  "initial_state": "SUBMITTED",
  "states": [
    "DRAFT", "SUBMITTED", "VERIFICATION", "DEPARTMENT_REVIEW", 
    "ACTION_REQUIRED", "APPROVAL", "RESOLVED", "REJECTED"
  ],
  "transitions": [
    {
      "action": "SUBMIT",
      "from_state": "DRAFT",
      "to_state": "SUBMITTED",
      "allowed_roles": ["CITIZEN"],
      "citizen_status": "Application Submitted. Queued for Verification.",
      "citizen_action_required": false
    },
    {
      "action": "ASSIGN_TO_VERIFIER",
      "from_state": "SUBMITTED",
      "to_state": "VERIFICATION",
      "allowed_roles": ["SYSTEM", "VERIFICATION_OFFICER"],
      "citizen_status": "Under Initial Verification with Front-Desk Officer",
      "citizen_action_required": false
    },
    {
      "action": "VERIFY",
      "from_state": "VERIFICATION",
      "to_state": "DEPARTMENT_REVIEW",
      "allowed_roles": ["VERIFICATION_OFFICER"],
      "guards": ["ALL_MANDATORY_DOCS_VERIFIED"],
      "citizen_status": "Under Departmental Scrutiny with Revenue Officer",
      "citizen_action_required": false
    },
    {
      "action": "REQUEST_CORRECTION",
      "from_state": "VERIFICATION",
      "to_state": "ACTION_REQUIRED",
      "allowed_roles": ["VERIFICATION_OFFICER", "DEPARTMENT_OFFICER"],
      "citizen_status": "Action Required: Please replace defective document(s)",
      "citizen_action_required": true
    },
    {
      "action": "RESUBMIT_DOCUMENTS",
      "from_state": "ACTION_REQUIRED",
      "to_state": "VERIFICATION",
      "allowed_roles": ["CITIZEN"],
      "guards": ["ALL_DEFICIENT_DOCS_REPLACED"],
      "citizen_status": "Replacement Documents Received. Resuming Verification.",
      "citizen_action_required": false
    },
    {
      "action": "FORWARD",
      "from_state": "DEPARTMENT_REVIEW",
      "to_state": "APPROVAL",
      "allowed_roles": ["DEPARTMENT_OFFICER"],
      "citizen_status": "Awaiting Final Approval from Competent Authority (Tahsildar)",
      "citizen_action_required": false
    },
    {
      "action": "APPROVE",
      "from_state": "APPROVAL",
      "to_state": "RESOLVED",
      "allowed_roles": ["APPROVING_OFFICER"],
      "citizen_status": "Approved! Certificate is ready for download.",
      "citizen_action_required": false
    },
    {
      "action": "REJECT",
      "from_state": ["VERIFICATION", "DEPARTMENT_REVIEW", "APPROVAL"],
      "to_state": "REJECTED",
      "allowed_roles": ["VERIFICATION_OFFICER", "DEPARTMENT_OFFICER", "APPROVING_OFFICER"],
      "citizen_status": "Application Rejected. See detailed statutory remarks.",
      "citizen_action_required": false
    }
  ]
}
```

---

## 2. Universal Applicability Across Services

1. **EPFO Claim Journey**: Follows `SUBMITTED` $\to$ `VERIFICATION` (Establishment check) $\to$ `DEPARTMENT_REVIEW` (Accounts reconciliation) $\to$ `APPROVAL` $\to$ `RESOLVED` (Disbursed).
2. **Citizen Grievance Journey**: Follows `SUBMITTED` $\to$ `INITIAL_REVIEW` (Triage) $\to$ `DEPARTMENT_ASSIGNMENT` $\to$ `DEPARTMENT_REVIEW` $\to$ `SENIOR_REVIEW` $\to$ `RESOLUTION`.

The workflow engine executes all 3 workflows through identical runtime code paths.
