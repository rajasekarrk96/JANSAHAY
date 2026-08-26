# 06 — JANSAHAY Authentication & Authorization

## 1. Authentication Strategy

JANSAHAY uses JSON Web Tokens (JWT) signed with HMAC-SHA256 (`HS256`).

- **Token Payload**:
  - `sub`: User ID
  - `username`: Login handle
  - `role`: `CITIZEN` | `VERIFICATION_OFFICER` | `DEPARTMENT_OFFICER` | `APPROVING_OFFICER` | `SYSTEM_ADMIN`
  - `department_id`: Scoped department (if officer)
  - `jurisdiction_id`: Scoped administrative jurisdiction (if officer)
  - `exp`: Expiration timestamp (default: 8 hours for demo sessions)

---

## 2. Authorization Engine: `can(actor, action, resource)`

Authorization decisions are centralized in a dedicated module (`backend/app/core/authz.py`) rather than dispersed across endpoint handlers.

```python
def can(actor: UserContext, action: ActionEnum, resource: Case | Document | None) -> bool:
    # 1. System Admin has global inspect privileges (excluding state tampering)
    if actor.role == RoleEnum.SYSTEM_ADMIN:
        return action in ADMIN_ALLOWED_ACTIONS

    # 2. Citizen checks
    if actor.role == RoleEnum.CITIZEN:
        if action == ActionEnum.CREATE_CASE:
            return True
        if resource and isinstance(resource, Case):
            if action in [ActionEnum.VIEW_CASE, ActionEnum.RESUBMIT_DOCUMENTS]:
                return resource.citizen_id == actor.citizen_id
        return False

    # 3. Officer Scope Checks
    if actor.role in [RoleEnum.VERIFICATION_OFFICER, RoleEnum.DEPARTMENT_OFFICER, RoleEnum.APPROVING_OFFICER]:
        if resource and isinstance(resource, Case):
            # Check Department Isolation
            if resource.department_id != actor.department_id:
                return False
            # Check Jurisdiction Isolation
            if resource.jurisdiction_id != actor.jurisdiction_id:
                return False
            # Check Role Action Capabilities
            allowed_actions_for_role = ROLE_ACTION_PERMISSIONS.get(actor.role, [])
            return action in allowed_actions_for_role

    return False
```

---

## 3. Role-to-Action Permission Matrix

| Role | `VIEW_CASE` | `CREATE_CASE` | `VERIFY` | `REQUEST_CORRECTION` | `FORWARD` | `APPROVE` | `REJECT` | `RESUBMIT_DOCUMENTS` |
|---|---|---|---|---|---|---|---|---|
| **`CITIZEN`** | Owned Only | Yes | No | No | No | No | No | Owned Only |
| **`VERIFICATION_OFFICER`** | Dept + Jur Scope | No | Yes | Yes | No | No | Yes | No |
| **`DEPARTMENT_OFFICER`** | Dept + Jur Scope | No | No | Yes | Yes | No | Yes | No |
| **`APPROVING_OFFICER`** | Dept + Jur Scope | No | No | No | No | Yes | Yes | No |
| **`SYSTEM_ADMIN`** | Read Only | No | No | No | No | No | No | No |

---

## 4. Default Deny Principle
Any request missing an explicit affirmative evaluation in `can()` is rejected with `HTTP 403 Forbidden`.
