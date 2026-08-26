# 03 — JANSAHAY System Design & Lifecycles

## 1. Request Lifecycle & Transaction Boundary

All state-modifying requests execute within a strict transactional boundary:

```mermaid
sequenceDiagram
    autonumber
    actor User as Citizen / Officer
    participant API as FastAPI Router
    participant Auth as can() RBAC Guard
    participant Engine as Workflow Engine
    participant DB as Relational Database
    participant Audit as Audit Ledger
    participant Outbox as Notification Outbox

    User->>API: POST /api/cases/{id}/actions/{action_name} (Payload + Version)
    API->>Auth: Evaluate can(actor, action, case)
    alt Unauthorized
        Auth-->>API: 403 Forbidden / 401 Unauthorized
        API-->>User: Error Response
    else Authorized
        API->>Engine: execute_transition(case_id, action, actor, payload, expected_version)
        Note over Engine,DB: BEGIN TRANSACTION
        Engine->>DB: SELECT case FOR UPDATE (or check version_id)
        alt Version Mismatch (Stale Write)
            Engine-->>API: 409 Conflict Error
            API-->>User: Return 409
        else Valid Version & State
            Engine->>Engine: Validate Transition Guards
            Engine->>DB: UPDATE case SET state = new_state, version_id = version_id + 1
            Engine->>Audit: INSERT INTO audit_events (hash_chain_entry)
            Engine->>Outbox: INSERT INTO notification_outbox (citizen_alert)
            Note over Engine,DB: COMMIT TRANSACTION
            Engine-->>API: TransitionSuccess(case_projection)
            API-->>User: 200 OK + Updated Case & Next Legal Actions
        end
    end
```

---

## 2. Core Case State Machine Lifecycle (Certificate Journey)

```mermaid
stateDiagram-v2
    [*] --> DRAFT : Citizen Starts Journey
    DRAFT --> SUBMITTED : Citizen Submits with Uploaded Docs
    
    SUBMITTED --> VERIFICATION : Auto-assigned to Verification Officer
    
    VERIFICATION --> DEPARTMENT_REVIEW : Action: VERIFY (Docs Validated)
    VERIFICATION --> ACTION_REQUIRED : Action: REQUEST_CORRECTION (Doc Deficient)
    VERIFICATION --> REJECTED : Action: REJECT (Ineligible / Fraud)
    
    ACTION_REQUIRED --> VERIFICATION : Citizen Action: RESUBMIT_DOCUMENTS
    
    DEPARTMENT_REVIEW --> APPROVAL : Action: FORWARD (Scrutiny Cleared)
    DEPARTMENT_REVIEW --> ACTION_REQUIRED : Action: REQUEST_CORRECTION (Field Defect)
    DEPARTMENT_REVIEW --> REJECTED : Action: REJECT (Statutory Ineligibility)
    
    APPROVAL --> RESOLVED : Action: APPROVE (Certificate Issued)
    APPROVAL --> REJECTED : Action: REJECT (Final Denial)
    
    RESOLVED --> [*]
    REJECTED --> [*]
```

---

## 3. Document Processing Lifecycle

```mermaid
stateDiagram-v2
    [*] --> UPLOAD_REQUESTED : Presigned/Local Ticket Created
    UPLOAD_REQUESTED --> QUARANTINED : File Streamed to Disk
    QUARANTINED --> VALIDATING : MIME & Size Checker
    VALIDATING --> SCAN_FAILED : Malformed or Disallowed Format
    VALIDATING --> SCAN_PASSED : Magic Bytes & Antivirus OK
    SCAN_PASSED --> AVAILABLE : Linked to Case
    AVAILABLE --> VERIFIED : Officer Action: ACCEPT_DOCUMENT
    AVAILABLE --> REPLACEMENT_REQUIRED : Officer Action: REJECT_DOCUMENT
    REPLACEMENT_REQUIRED --> REPLACED : Citizen Uploads New Version
    REPLACED --> AVAILABLE : Scan Passed
```

---

## 4. Assistive AI Interaction Architecture

```mermaid
graph LR
    Citizen[Citizen Query] --> Guardrail[AI Gateway & Input Sanitizer]
    Guardrail --> PromptTemplate[System Prompt: Bounded Public Assistant]
    PromptTemplate --> ServiceSchema[JSON Schema of Services & Rules]
    PromptTemplate --> LLM[Language Model / Synthetic Mock]
    LLM --> Validator[Pydantic Output Validation]
    Validator --> SafeOutput[Structured Response: Recommendation / Clarification]
    SafeOutput --> Citizen
```
The AI has **no direct database write access** and is strictly isolated from changing state machines.
