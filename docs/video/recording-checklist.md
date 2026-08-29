# JANSAHAY — Video Recording Checklist & Verification Matrix

## 1. Master Recording Verification Checklist

- [ ] **Application starts correctly**: Fast boot on `http://localhost:8000/` with zero backend exceptions.
- [ ] **Demo account works**: Seamless login/switch for citizen `Rahul Sharma` and officer `Sunil Verma`.
- [ ] **Synthetic data confirmed**: All records use synthetic IDs, mock Aadhaar (`****4321`), and sample PDFs.
- [ ] **Citizen journey works**: End-to-end user path functions without breaks or dead ends.
- [ ] **Service discovery works**: "Tell us what you need" query resolves instantly to Income Certificate recommendation.
- [ ] **Checklist works**: 3 eligibility questions dynamically generate the 3-document requirement list.
- [ ] **Document upload works**: Sandboxed mock document verification passes and updates declaration state.
- [ ] **Case Passport works**: Generates Case ID (`JS-2026-INC-48192`), 5-stage progression, and 4-question plain status card.
- [ ] **Officer workflow works**: Verification officer can inspect attached files and advance state to Department Review.
- [ ] **Security behavior works**: Contextual RBAC badges visible; invalid actions and out-of-scope desks blocked.
- [ ] **Audit view works**: Tamper-evident SHA-256 event timeline renders with active `Chain Intact ✓` status.
- [ ] **AI view works if implemented**: Bounded assistant drawer responds with helpful service explanation.
- [ ] **Synthetic disclaimer visible**: Prominent amber header banner clearly visible throughout the entire recording.
- [ ] **No personal data visible**: Zero real names, real phone numbers, or genuine PII.
- [ ] **No real government credentials visible**: No official government passwords, OTPs, or production tokens.
- [ ] **No government endorsement implied**: Clear disclosure as an independent hackathon prototype.
- [ ] **Recording is under 2 minutes**: Video length strictly between **1:50 and 1:55** (Hard cap: 2:00).
- [ ] **Voice is understandable**: Calm, natural human narration in clear English (~175 words, ~90–100 wpm).
- [ ] **Cursor movement is clean**: Deliberate mouse clicks, smooth movement, and 1–2 second pauses after UI changes.
- [ ] **Final video reviewed completely**: Full start-to-finish playback review completed before submission.

---

## 2. Scene-by-Scene Timing & Visual Cues

| Scene | Target Timestamp | Max Duration | Primary Action | Screen Cue |
|:---|:---|:---|:---|:---|
| **Scene 1: Problem + JANSAHAY** | `00:00 – 00:08` | 8s | Load citizen portal with Rahul Sharma persona | Hero title & *Citizen-First Engine* |
| **Scene 2: Service Discovery** | `00:08 – 00:18` | 10s | Enter "I need an income certificate for college" | Instant card *"We think you may need"* |
| **Scene 3: Checklist + Application** | `00:18 – 00:30` | 12s | Check 3 eligibility boxes $\to$ load checklist | 3-item required proof cards |
| **Scene 4: Submit & Case Passport** | `00:30 – 00:52` | 22s | Upload mock files $\to$ check declaration $\to$ submit $\to$ view Case Passport | 5-stage stepper + 4 plain questions |
| **Scene 5: Officer Workflow** | `00:52 – 01:00` | 8s | Switch to `Sunil Verma (Verification Officer)` $\to$ click `VERIFY` | Stage moves to Dept Review |
| **Scene 6: Universal Case Engine** | `01:00 – 01:15` | 15s | Filter Certificates, EPFO, and Grievance tabs | Multi-domain engine parity |
| **Scene 7: Security & Audit** | `01:15 – 01:40` | 25s | Show role badges, optimistic concurrency, and SHA-256 chain | `Chain Intact ✓` cryptographic proof |
| **Scene 8: AI & Safety Disclosure** | `01:40 – 01:55` | 15s | Open AI Assistant drawer $\to$ pan to top amber disclaimer banner | Assistive boundary & synthetic disclaimer |
| **Scene 9: Closing** | `01:55 – 02:00` | 5s | Hold on Case Passport resolution view | Ends at **01:55** (5s buffer) |

---

## 3. Post-Recording 6-Point Hackathon Judging Review

| Judging Area | Review Question | Verification Status |
|:---|:---|:---:|
| **1. Problem** | Can the reviewer immediately understand citizen pain across bureaucratic departmental silos? | **PASS** |
| **2. Working Build** | Does the video prove that the prototype is a live, functional, interactive application? | **PASS** |
| **3. Usability** | Does the interface visibly look simpler, cleaner, and more reassuring than traditional portals? | **PASS** |
| **4. Product Thinking** | Is there a clear product rationale for the Case Passport, unified workflow, and tailored checklist? | **PASS** |
| **5. End-to-End Thinking** | Does the video show the full chain: Citizen $\to$ Case $\to$ Officer $\to$ Workflow $\to$ Security $\to$ Audit? | **PASS** |
| **6. Honesty** | Does the video honestly disclose synthetic data, mock integrations, and assistive AI guardrails? | **PASS** |
