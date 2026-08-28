# 24 — JANSAHAY SLA & Escalation Engine Specification

**Document Version**: 1.0.0  
**Status**: APPROVED & ACTIVE  
**Last Updated**: 2026-08-28  

---

## 1. Objective & Philosophy

The JANSAHAY SLA & Escalation Engine guarantees accountability in public service delivery. Under statutory citizen charters (such as Delhi e-SLA / Right to Public Services Acts), government departments must process citizen applications within statutory deadlines.

JANSAHAY provides:
1. **Deterministic SLA Tracking**: Computed relative to submission timestamp and service SLA days.
2. **Citizen-Facing Transparency**: Plain-language SLA countdown and status indicators.
3. **Internal Escalation Triggers**: Multi-level escalation paths for delayed applications.

---

## 2. SLA Classification Logic

For any case $C$ of service $S$ submitted at timestamp $T_{sub}$:
- **Target Resolution Time**: $T_{target} = T_{sub} + \text{SLA\_Days}(S)$
- **Elapsed Percentage**: $P = \frac{\text{Now} - T_{sub}}{T_{target} - T_{sub}} \times 100\%$

| Classification | Threshold | Citizen Badge | Officer Queue Styling | Notification Trigger |
| :--- | :--- | :--- | :--- | :--- |
| **ON_TRACK** | $P < 75\%$ | 🟢 *Within SLA* (e.g. "4 days remaining") | Normal priority | Routine stage transition updates |
| **APPROACHING_SLA** | $75\% \le P < 100\%$ | 🟡 *Approaching Deadline* (e.g. "1 day remaining") | Amber highlighted priority | Officer nudge alert |
| **ESCALATED / OVERDUE** | $P \ge 100\%$ | 🔴 *Escalated for Senior Review* | Red flash badge with immediate escalation sort | Urgent notification to Sub-Divisional Magistrate & Admin |

---

## 3. Workflow Escalation State Machine

When an application exceeds statutory limits or is flagged for supervisory intervention:
1. **Action**: `ESCALATE`
2. **Authorized Actors**: `DEPARTMENT_OFFICER`, `APPROVING_OFFICER`, `SYSTEM_ADMIN`
3. **State Shift**: `VERIFICATION` / `DEPARTMENT_REVIEW` $\to$ `APPROVAL` (Fast-tracked to senior magistrate queue).
4. **Citizen Status Update**: *"Your application is taking longer than expected. It has been escalated for senior review."*
5. **Audit Trail**: Generates a cryptographic SHA-256 audit entry recording officer ID, reason, and timestamp.

---

## 4. Architectural Implementation

### Backend Schema Integration
- `Service.sla_days` (e.g. 7 days for Income Certificate, 5 days for Grievances).
- `CaseListOut.sla_days` and `CaseDetailOut.sla_days` exposed to clients.
- `WorkflowEngine.execute_action("ESCALATE")` atomic transition.

### Citizen UI Rendering
- Visible in **Case Passport** header with countdown pill and stage reassurance.
