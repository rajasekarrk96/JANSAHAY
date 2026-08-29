# JANSAHAY — Final 2-Minute Hackathon Demo Script

## Video Overview & Timing Structure
- **Target Duration**: **1:50 – 1:55** (Hard maximum: 2:00)
- **Word Count**: **175 words** (Within strict 170–190 word target)
- **Structure**:
  - **First ~1 Minute (00:00–01:00)**: Citizen Experience (Problem, Discovery, Checklist, Submission, Case Passport, Officer Scrutiny).
  - **Second ~1 Minute (01:00–02:00)**: Engineering, Security & Architecture (Universal Engine, Contextual RBAC, Audit History, Bounded AI, Safety Disclosure).
- **Tone**: Calm, natural, clear Indian English. Spoken like a real person explaining a project with natural pauses for clicks, page transitions, and visual emphasis.

---

## Story Flow
```text
Citizen has a problem
        ↓
JANSAHAY understands the goal
        ↓
JANSAHAY guides the citizen
        ↓
Citizen submits
        ↓
Citizen gets one case
        ↓
Citizen can track it
        ↓
Government workflow moves the case
        ↓
Access is controlled
        ↓
AI only assists
        ↓
Everything is synthetic for the prototype
```

---

## 9-Scene Storyboard & Timeline

| Scene | Time | Screen & Action | On-Screen Label | Narration | Words |
|:---|:---|:---|:---|:---|:---:|
| **1. Problem + JANSAHAY** | `00:00–00:08` | Citizen homepage (`Rahul Sharma`). Hero banner in view. | *Public Services Organized Around Your Goal* | *"Government services can be difficult to navigate. JANSAHAY makes the journey simpler, starting with what the citizen actually needs."* | 18 |
| **2. Service Discovery** | `00:08–00:18` | "Tell us what you need" search. Type: *"I need an income certificate for college."* Click chip $\to$ recommendation card pops up. | *Tell us what you need* | *"Instead of searching through departments, the citizen simply describes their goal."* | 11 |
| **3. Checklist + Application** | `00:18–00:30` | 3 eligibility questions answered $\to$ Dynamic 3-document checklist displayed. | *Your personalized checklist* | *"JANSAHAY asks a few simple questions and shows exactly what documents are needed."* | 13 |
| **4. Submit & Case Passport** | `00:30–00:52` | Upload mock scans $\to$ check declaration $\to$ submit $\to$ Case Passport opens (`JS-2026-INC-48192`) showing 5-step stepper & 4-question status card. | *Your Case Passport*<br>*Current stage*<br>*What's next?* | *"The citizen uploads the required documents and submits the application. A Case Passport is created immediately. The citizen can see where the case is and what happens next."* | 28 |
| **5. Officer Workflow** | `00:52–01:00` | Switch persona to `Sunil Verma (Verification Officer)` $\to$ Open scrutiny desk $\to$ Click `VERIFY`. | *Authorized workflow* | *"Behind the scenes, the case moves through the right officers."* | 10 |
| **6. Universal Case Engine** | `01:00–01:15` | Services catalog showing Certificates, EPFO Social Security, and Civic Grievances on one platform. | *Universal Case Engine* | *"Technically, JANSAHAY uses one case engine and one workflow engine. The same system can support certificates, EPFO claims, and grievances."* | 21 |
| **7. Security & Audit** | `01:15–01:40` | Highlight role/department/jurisdiction badges, `version_id` lock, and SHA-256 event timeline with `Chain Intact ✓`. | *Authorized access*<br>*Invalid actions blocked*<br>*Audit history* | *"Security is enforced on the server. Officers only see cases and actions allowed for their role, department, and jurisdiction. Invalid actions are rejected. Every important workflow action is recorded in a tamper-evident audit history."* | 34 |
| **8. AI & Safety Disclosure** | `01:40–01:55` | AI Assistant drawer open $\to$ highlight top amber compliance banner (`100% Synthetic Prototype`). | *Assistive AI*<br>*Synthetic Prototype* | *"AI helps with service discovery and simple explanations. It cannot approve, reject, or change a case. This prototype uses synthetic data and mocked government integrations."* | 25 |
| **9. Closing** | `01:55–02:00` | Case Passport overview with digital seal. Clean fade. | *One citizen journey. One case. One clear timeline.* | *"JANSAHAY puts the citizen's journey first."* | 6 |
| **TOTALS** | **1:55** | | | **Complete Voice-Over** | **176** |

---

## Full Narration Script (176 Words)

### [00:00 – 00:08] SCENE 1: Problem + JANSAHAY
> *"Government services can be difficult to navigate. JANSAHAY makes the journey simpler, starting with what the citizen actually needs."*

### [00:08 – 00:18] SCENE 2: Service Discovery
> *"Instead of searching through departments, the citizen simply describes their goal."*

### [00:18 – 00:30] SCENE 3: Checklist + Application
> *"JANSAHAY asks a few simple questions and shows exactly what documents are needed."*

### [00:30 – 00:52] SCENE 4: Submit & Case Passport
> *"The citizen uploads the required documents and submits the application. A Case Passport is created immediately. The citizen can see where the case is and what happens next."*

### [00:52 – 01:00] SCENE 5: Officer Workflow
> *"Behind the scenes, the case moves through the right officers."*

### [01:00 – 01:15] SCENE 6: Universal Case Engine
> *"Technically, JANSAHAY uses one case engine and one workflow engine. The same system can support certificates, EPFO claims, and grievances."*

### [01:15 – 01:40] SCENE 7: Security & Audit
> *"Security is enforced on the server. Officers only see cases and actions allowed for their role, department, and jurisdiction. Invalid actions are rejected. Every important workflow action is recorded in a tamper-evident audit history."*

### [01:40 – 01:55] SCENE 8: AI & Safety Disclosure
> *"AI helps with service discovery and simple explanations. It cannot approve, reject, or change a case. This prototype uses synthetic data and mocked government integrations."*

### [01:55 – 02:00] SCENE 9: Closing
> *"JANSAHAY puts the citizen's journey first."*

---

## Screen Direction & What the Screen Communicates Visually

The narrator explains the **idea and value** in everyday human terms, while the screen visually proves the engineering rigor:

| Element | Handled Verbally | Communicated Visually on Screen |
|:---|:---|:---|
| **Intent Matching** | "citizen simply describes their goal" | Query input $\to$ Instant card *"We think you may need: Income Certificate"* |
| **Checklist** | "shows exactly what documents are needed" | 3 concise badges: Identity Proof, Income Proof, Residence Proof |
| **Transparency** | "see where the case is and what happens next" | 5-stage stepper + 4 plain-language questions card |
| **Architecture** | "one case engine and one workflow engine" | Multi-category tabs: Certificates, EPFO claims, Civic Grievances |
| **Security & RBAC** | "Security is enforced on the server" | Role badges (`REV-VO-401`), Jurisdiction tags, `version_id` lock |
| **Audit Ledger** | "recorded in a tamper-evident audit history" | Cryptographic SHA-256 timeline with green `Chain Intact ✓` pill |
| **AI Boundaries** | "cannot approve, reject, or change a case" | AI assistant side drawer scoped to guidance |
| **Safety & Sandbox** | "synthetic data and mocked government integrations" | Prominent top amber disclaimer banner across all views |

---

## Delivery & Narration Guidelines
1. **Pacing**: Steady, unhurried 90–100 words per minute.
2. **Pauses**: Leave 1–2 second visual breathing room between scene transitions.
3. **Cursor Control**: Move smoothly, click deliberately, and never swirl or wiggle the mouse.
4. **Volume**: Clean, balanced vocal track with zero overpowering background music.
