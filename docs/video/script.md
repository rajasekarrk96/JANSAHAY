# JANSAHAY — 2-Minute Hackathon Demo Script & Storyboard

## Video Objective
Demonstrate JANSAHAY as a working, citizen-first public service platform and secure government workflow engine within a strict 2-minute duration limit:
- **00:00–01:00 (Citizen Experience)**: Problem context, natural language service discovery, tailored checklist, sandboxed upload, submission, Case Passport, 4-question plain-language status explanation, and officer verification.
- **01:00–02:00 (Architecture, Security & Engineering)**: Universal Case Engine, declarative workflow state machine, contextual RBAC authorization (`can(actor, action, resource)`), tamper-evident SHA-256 audit ledger, bounded assistive AI, and synthetic prototype disclosure.

---

## Recording Rules & Constraints
- **Target Duration**: Exactly 01:56 (Leaving a 4-second safety buffer under the 2:00 ceiling).
- **Data Integrity**: 100% Synthetic mock data (Rahul Sharma, synthetic Aadhaar `****4321`, mock PDF scans). Zero live government connections.
- **Tone**: Professional, clear, concise, evidence-based demonstration.
- **Spoken Word Count**: 242 words (~130 words/minute delivery).

---

## Scene Timeline & Storyboard

| Timestamp | Scene / Section | Screen / View | Primary Action | Narration & Focus |
|:---|:---|:---|:---|:---|
| **00:00–00:08** | **1. Opening & Problem** | Citizen Portal Homepage | Display JANSAHAY hero banner and synthetic persona badge | Establish friction of departmental silos vs citizen goals |
| **00:08–00:18** | **2. Service Discovery** | "Tell us what you need" | Type/click query: *"I need income proof for college fee concession"* $\to$ Card pops up | Natural language intent matching to Income Certificate |
| **00:18–00:28** | **3. Eligibility & Checklist** | 4-Step Application Wizard | Answer 3 eligibility questions $\to$ Step 2 displays personalized 3-doc checklist | Dynamic scoping to required proof without bloat |
| **00:28–00:38** | **4. Upload & Submit** | Quarantined Sandbox | Step 3 displays scanned mock documents $\to$ Step 4 accepts declaration $\to$ Submit | Sandboxed document validation and instant case creation |
| **00:38–00:50** | **5. Case Passport & Timeline** | Case Passport & 4-Question Milestone Card | Open Case `JS-2026-INC-48192` $\to$ Highlight 5-step stepper & 4 questions | Total transparency: *What happened? What does it mean?* |
| **00:50–01:00** | **6. Officer Scrutiny Desk** | Officer Queue (`vo_delhi_rev`) | Switch to Verification Officer $\to$ Review attached documents $\to$ Click `VERIFY` | Stage progression to Department Review with RBAC guards |
| **01:00–01:15** | **7. Universal Case Engine** | Multi-Service View / Architecture | Display Service Catalog (Certificates, EPFO, Civic Grievances) | One universal case entity powering all state machines |
| **01:15–01:30** | **8. Contextual RBAC & Concurrency** | Officer Queue / Security Modal | Highlight role, department, jurisdiction guards & `version_id` locking | Strict default-deny authorization & conflict prevention |
| **01:30–01:42** | **9. SHA-256 Audit & Document Pipeline** | Audit Ledger & Document Matrix | Scroll cryptographic event chain with `Chain Intact ✓` status | Tamper-evident mathematical proof & versioned documents |
| **01:42–01:50** | **10. Assistive Bounded AI** | JANSAHAY AI Assistant Drawer | Open Assistant $\to$ Show intent classification & status explanation | Bounded assistive AI with zero state-mutation authority |
| **01:50–01:58** | **11. Safety & Prototype Disclosure** | Top Disclaimer Banner | Highlight amber synthetic boundary banner | Clear disclosure: 100% synthetic sandbox prototype |
| **01:58–02:00** | **12. Final Closing Screen** | Case Passport / Resolution Center | Focus on Case Passport & Digital Grant Seal | *"One citizen journey. One case. One clear timeline."* |

---

## Complete Voice-Over Script (242 Words)

### [00:00 – 00:08] The Problem & Vision
> *"Government services are organized around departments. Citizens shouldn't have to understand bureaucracy just to get something done. JANSAHAY gives citizens one simple place to discover services, complete their journey, and track what happens next."*

### [00:08 – 00:18] Citizen Discovery
> *"Instead of searching confusing portals, citizens simply describe their goal. JANSAHAY instantly identifies the statutory Income Certificate service and explains why."*

### [00:18 – 00:28] Tailored Checklist
> *"A quick 3-question eligibility check personalizes the application, generating an exact document checklist so citizens never submit unnecessary paperwork."*

### [00:28 – 00:38] Sandboxed Submission
> *"Supporting documents are uploaded into a quarantined sandbox, validated, and submitted with one digital declaration."*

### [00:38 – 00:50] The Case Passport
> *"Immediately, JANSAHAY generates a Case Passport. With a single timeline answering what happened, what it means, and what happens next, citizens never have to guess."*

### [00:50 – 01:00] Controlled Officer Scrutiny
> *"Behind the scenes, the case routes to authorized officers. The verification officer inspects the documents and forwards the case to departmental review."*

### [01:00 – 01:15] Universal Case Architecture
> *"Technically, JANSAHAY is built on one Universal Case Engine. Certificates, EPFO claims, and civic grievances all run on the same declarative state machine."*

### [01:15 – 01:30] Contextual RBAC & Concurrency
> *"Security is enforced server-side using contextual authorization. An officer must have the exact role, department, and jurisdiction to act. Invalid actions and stale concurrent writes are strictly rejected."*

### [01:30 – 01:42] Tamper-Evident Audit Ledger
> *"Every state transition is cryptographically chained using SHA-256 hashes, creating an immutable audit history."*

### [01:42 – 01:50] Bounded Assistive AI
> *"Our AI is strictly assistive: it guides discovery and simplifies statuses, but holds zero decision-making power."*

### [01:50 – 02:00] Synthetic Sandbox & Conclusion
> *"Built with 100% synthetic data in a secure sandbox, JANSAHAY proves how public services can be organized around citizens."*

---

## Screen Actions & Recording Cues

### Scene 1 (00:00–00:08): Homepage
- **Screen**: `http://localhost:8000/`
- **Action**: View loads with active user `Rahul Sharma (Citizen)`.
- **On-Screen Text**: *"Public Services Organized Around Your Goal"*

### Scene 2 (00:08–00:18): Natural Language Discovery
- **Screen**: Search Input
- **Action**: Click *"🎓 Income Certificate"* quick chip or type query.
- **On-Screen Text**: *"We think you may need: Income Certificate"* $\to$ Click *"Continue to Application"*.

### Scene 3 (00:18–00:28): Eligibility & Checklist
- **Screen**: Application Wizard (Step 1 & Step 2)
- **Action**: Confirm checkboxes for income, residence, ID $\to$ Click *"Next: Personalized Checklist"* $\to$ View 3 required items.

### Scene 4 (00:28–00:38): Upload & Submit
- **Screen**: Application Wizard (Step 3 & Step 4)
- **Action**: Advance through pre-loaded mock files $\to$ Check declaration $\to$ Click *"Submit & Generate Case ID"*.

### Scene 5 (00:38–00:50): Case Passport
- **Screen**: Case Detail Modal (`JS-2026-INC-48192`)
- **Action**: Highlight the 5-step milestone stepper, SLA badge, and the 4-question status explanation card (*"What happened?", "What does it mean?", "Do I need to do anything?", "What happens next?"*).

### Scene 6 (00:50–01:00): Officer Workflow
- **Screen**: Persona Switcher $\to$ `Sunil Verma (Verification Officer)`
- **Action**: Open Officer Queue $\to$ Select Case $\to$ Click *"Verify & Forward to Department Scrutiny"*.

### Scene 7 (01:00–01:15): Universal Case Engine
- **Screen**: Services Catalog / Architecture
- **Action**: Filter by Statutory Certificates, EPFO Social Security, and Civic Grievances to demonstrate unified multi-service engine.

### Scene 8 (01:15–01:30): Security & RBAC
- **Screen**: Case Details & Officer Actions
- **Action**: Highlight contextual authorization badges (Role, Department, Jurisdiction) and optimistic concurrency lock (`version_id`).

### Scene 9 (01:30–01:42): Cryptographic Audit Ledger
- **Screen**: Case Modal Audit Section
- **Action**: Scroll the SHA-256 audit event timeline with the green `Chain Intact ✓` badge.

### Scene 10 (01:42–01:50): Assistive AI Assistant
- **Screen**: AI Assistant Drawer
- **Action**: Open Assistant drawer showing intent matching and plain-language explanation with bounded execution guardrails.

### Scene 11 (01:50–01:58): Compliance Disclosure
- **Screen**: Top Amber Banner & Footer
- **Action**: Frame the disclaimer: *"100% Synthetic Citizen & Officer Profiles. No live government APIs."*

### Scene 12 (01:58–02:00): Closing
- **Screen**: Case Passport Overview
- **Action**: Hold on Case Passport resolution view.

---

## Safety & Compliance Disclosure
- **Independent Demonstration**: JANSAHAY is an academic and hackathon prototype.
- **Zero Real Data**: All Aadhaar numbers (`****4321`), employee codes, and case records are synthetic mock representations.
- **No Government Endorsement**: This prototype is not affiliated with or endorsed by any government entity.
