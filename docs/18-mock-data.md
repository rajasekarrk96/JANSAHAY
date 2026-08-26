# 18 — JANSAHAY Synthetic Mock Data Dictionary

## 1. Synthetic Citizens

| Username | Full Name | Phone | Aadhaar Last 4 | Address / District |
|---|---|---|---|---|
| `citizen_rahul` | Rahul Sharma | +91-9876500001 | 4321 | 14/B Karol Bagh, Central Delhi |
| `citizen_anita` | Anita Patel | +91-9876500002 | 8765 | 22/A Hauz Khas, South Delhi |
| `citizen_vikram` | Vikram Singh | +91-9876500003 | 1122 | 56 Indiranagar, Bangalore Urban |

*Password for all test users*: `Password123!`

---

## 2. Synthetic Officers & Department Allocations

| Username | Full Name | Role | Department | Jurisdiction | Designation |
|---|---|---|---|---|---|
| `vo_delhi_rev` | Sunil Verma | `VERIFICATION_OFFICER` | `REVENUE` | `DELHI_CENTRAL` | Naib Tehsildar Desk In-Charge |
| `do_delhi_rev` | Priya Nair | `DEPARTMENT_OFFICER` | `REVENUE` | `DELHI_CENTRAL` | Revenue Inspector |
| `ao_delhi_rev` | Rajesh Kumar | `APPROVING_OFFICER` | `REVENUE` | `DELHI_CENTRAL` | Tehsildar (Executive Magistrate) |
| `vo_epfo_delhi` | Amit Roy | `VERIFICATION_OFFICER` | `EPFO` | `DELHI_CENTRAL` | Section Supervisor |
| `ao_epfo_delhi` | Meenakshi Sundaram | `APPROVING_OFFICER` | `EPFO` | `DELHI_CENTRAL` | Assistant Provident Fund Commissioner |
| `do_grievance_delhi`| Sanjay Gupta | `DEPARTMENT_OFFICER` | `PUBLIC_GRIEVANCE` | `DELHI_CENTRAL` | Grievance Nodal Officer |

---

## 3. Public Services Catalog

1. **`INCOME_CERTIFICATE`**: Revenue Department | SLA: 7 Days | Threshold: Annual income verification.
2. **`DOMICILE_CERTIFICATE`**: Revenue Department | SLA: 14 Days | Proof of residence $\ge 3$ years.
3. **`EPFO_CLAIM_TRANSFER`**: EPFO Department | SLA: 10 Days | Previous UAN to current establishment transfer.
4. **`STREET_LIGHT_GRIEVANCE`**: Public Grievance Dept | SLA: 5 Days | Civic infrastructure repair.
