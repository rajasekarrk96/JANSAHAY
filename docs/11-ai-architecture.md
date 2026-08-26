# 11 — JANSAHAY AI Architecture & Safety Boundaries

## 1. Assistive AI Role & Boundaries

The AI subsystem in JANSAHAY acts strictly in an **advisory and assistive capacity**.

### 1.1 What AI CAN Do:
1. **Service Recommendation**: Ingest natural language queries from citizens and map them to appropriate public service IDs.
2. **Document & Prerequisite Explanation**: Explain why specific documents (e.g. Income proof, Ration card) are mandatory in clear conversational vernacular.
3. **Grievance Structuring**: Help citizens draft clear, objective grievance descriptions with relevant departmental categorization.
4. **Status Summarization**: Translate technical bureaucratic notes into simplified plain-language explanations.

### 1.2 What AI CANNOT Do:
1. **Cannot Transition Cases**: AI has no tool invocation to call state transition endpoints.
2. **Cannot Approve or Reject**: Decisions remain exclusively with authenticated officers.
3. **Cannot Alter Audit Logs**: Audit ledgers are strictly append-only by the workflow engine.
4. **Cannot Bypass Guards or Permissions**: AI has zero direct database write permissions.

---

## 2. Guardrails & Validation
- Output schemas are strictly validated via Pydantic models.
- If no OpenAI API key is configured in the environment, the platform automatically falls back to an intelligent rule-based discovery matcher, ensuring 100% offline demo determinism.
