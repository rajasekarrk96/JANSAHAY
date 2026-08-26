# 09 — JANSAHAY Case Management

## 1. Universal Case Concept

In JANSAHAY, both **Applications** (e.g. Income Certificate, Domicile, EPFO Transfer) and **Complaints/Grievances** (e.g. Municipal issues, Pension delay) are represented by the unified **Case** entity.

### 1.1 Identifiers
- **Internal UUID**: Primary key for foreign keys and internal indices (`case_id`).
- **Public Case Identifier**: Human-readable tracking number formatted as:
  `JS-<YEAR>-<SERVICE_SHORT_CODE>-<5_DIGIT_RANDOM>`
  *(e.g., `JS-2026-INC-78124`, `JS-2026-EPF-19042`, `JS-2026-GRV-33108`)*

---

## 2. Case Projection & Timeline

A case payload returned to the citizen or officer contains:
1. **Header**: Public ID, Service Title, Category, Submitted Timestamp, SLA Due Date.
2. **Current State Projection**: Raw state code, Citizen-Friendly Progress Label, Next Stage Name, Action-Required Flag.
3. **Citizen Form Data**: Form fields, income declarations, answers to eligibility questionnaires.
4. **Documents**: List of attached documents with validation status (`VERIFIED`, `REPLACEMENT_REQUIRED`, etc.).
5. **Timeline / Event Ledger**: Complete chronological audit list with actor roles and timestamps.
6. **Available Actions**: Dynamically computed array of actions the current authenticated user can perform on this case right now.
