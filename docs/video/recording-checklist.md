# JANSAHAY — Video Recording Checklist & Verification Matrix

## 1. Pre-Recording Environment Checklist

- [x] **Backend Server Active**: Running at `http://localhost:8000/` with static SPA mounted.
- [x] **OpenAPI Swagger Route**: Accessible at `http://localhost:8000/docs`.
- [x] **Database Seed Status**: Pre-seeded with 2 Citizens, 6 Officers, 1 Demo Income Certificate case (`JS-2026-INC-48192`), and 3 mock document attachments.
- [x] **Synthetic Compliance Banner**: Prominently displayed across all pages (`100% Synthetic Citizen & Officer Profiles. No live government APIs`).
- [x] **Clean Browser Session**: No bookmarks bar, no devtools panel, clean 16:9 viewport ratio.
- [x] **Zero Console Errors**: All static scripts, Tailwind styles, and Lucide icons load cleanly.

---

## 2. Scene-by-Scene Quality & Timing Verification

| Scene | Target Timestamp | Max Duration | Screen Action | Quality Check |
|:---|:---|:---|:---|:---|
| **Scene 1: Problem & Hero** | `00:00 – 00:08` | 8s | Load citizen portal with Rahul Sharma context | Persona banner & hero tagline readable |
| **Scene 2: Service Discovery** | `00:08 – 00:18` | 10s | Enter query into "Tell us what you need" $\to$ Recommendation card | Immediate response without lag |
| **Scene 3: Eligibility & Checklist** | `00:18 – 00:28` | 10s | Step 1 checkboxes $\to$ Step 2 dynamic checklist | 3 personalized items shown |
| **Scene 4: Sandboxed Upload** | `00:28 – 00:38` | 10s | Step 3 mock files scanned $\to$ Step 4 declaration submit | Clean progress to Case ID generation |
| **Scene 5: Case Passport & Timeline** | `00:38 – 00:50` | 12s | Open Case Passport with 5-stage stepper & 4 questions | 4 status questions clearly visible |
| **Scene 6: Officer Workflow** | `00:50 – 01:00` | 10s | Switch persona to `vo_delhi_rev` $\to$ Execute `VERIFY` action | Live stage transition to Dept Review |
| **Scene 7: Universal Engine** | `01:00 – 01:15` | 15s | Filter Certificates, EPFO claims, Civic Grievances | Multi-service parity demonstrated |
| **Scene 8: Contextual RBAC** | `01:15 – 01:30` | 15s | Show role, department, jurisdiction guards & `version_id` | Server-side default-deny explained |
| **Scene 9: Audit & Documents** | `01:30 – 01:42` | 12s | Cryptographic SHA-256 timeline & `Chain Intact ✓` | Mathematical chain verification |
| **Scene 10: Assistive AI** | `01:42 – 01:50` | 8s | Open AI Assistant chat drawer | Guardrails and offline bounded model |
| **Scene 11: Safety & Disclosure** | `01:50 – 01:58` | 8s | Highlight synthetic banner & mock disclosure | Unambiguous non-government declaration |
| **Scene 12: Final Outro** | `01:58 – 02:00` | 2s | Hold on Case Passport resolution view | Ends within exact 2:00 limit |

---

## 3. Post-Recording Verification Rules

- **Total Length**: Must not exceed `02:00` (Target: `01:56`).
- **Pacing**: Steady, clear narration (~130 words/minute).
- **Legibility**: All text, status badges, and IDs legible at 1080p.
- **Integrity**: No real government credentials or PII shown.
