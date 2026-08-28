# 26 — JANSAHAY Assistive AI Safety, Evaluation & Guardrails

**Document Version**: 1.0.0  
**Status**: APPROVED & ACTIVE  
**Last Updated**: 2026-08-28  

---

## 1. Architectural Philosophy: Assistive, Never Autonomous

In administrative governance and legal certitude, AI must **never** make sovereign statutory decisions (e.g. granting certificates, rejecting claims, or assigning rights).

JANSAHAY implements an **Assistive, Bounded AI Layer**:
1. **Citizens**: Natural-language intent matching, schema discovery, and plain-language stage translations.
2. **Officers**: Summary structuring and proof completeness highlighting.
3. **Workflow Engine**: 100% deterministic, state-machine governed, and cryptographically audited.

---

## 2. Guardrails & Zero-Failure Fallbacks

```
                       [Citizen Natural Language Query]
                                      │
                                      ▼
                        [Rule-Based Keyword Fast-Path]
                                      │
                   ┌──────────────────┴──────────────────┐
                   ▼                                     ▼
      [Matches Known Patterns]              [Uncertain / Out-of-Domain]
                   │                                     │
                   ▼                                     ▼
     [Deterministic Match Return]            [Semantic Keyword Fallback]
                   │                                     │
                   └──────────────────┬──────────────────┘
                                      │
                                      ▼
                         [Safe Structured Output]
                   (Recommended Service + "Why" Reasoning)
```

### Deterministic Intent Rules

| Intent Category | Trigger Keywords | Resolved Service | Explanation Provided |
| :--- | :--- | :--- | :--- |
| **Income / Subsidy** | *income, salary, scholarship, fee waiver, ews, earnings* | `INCOME_CERTIFICATE` | Proof of household income for scholarships, fee concessions, and state welfare schemes. |
| **Domicile / Residence** | *domicile, resident, native, address, local, 3 years* | `DOMICILE_CERTIFICATE` | Continuous residency proof required for Delhi university quotas and state recruitment. |
| **Provident Fund / Pension** | *epfo, pf, provident, uan, pension, transfer claim* | `EPFO_CLAIM_TRANSFER` | Direct PF account transfer from previous establishment to active member account. |
| **Civic Grievance** | *streetlight, pothole, road, garbage, water, drainage, sewage* | `STREET_LIGHT_GRIEVANCE` | Direct civic complaint intake for municipal repairs and public infrastructure. |

---

## 3. Security & Privacy Boundaries

1. **No PII Transmission**: Citizen PII (Aadhaar number, phone number, financial figures) is NEVER sent to external LLMs.
2. **Prompt Injection Immunity**: The AI endpoint only returns verified catalog service IDs from a strictly typed enum; it cannot alter state machine transitions or override authorization checks.
3. **Offline Reliability**: The assistive AI engine works completely offline in local air-gapped environments without any third-party cloud API dependencies.
