# JANSAHAY — Project Summary

**JANSAHAY** is a citizen-first public service platform that transforms fragmented, department-siloed government administration into a seamless, goal-oriented journey. Instead of deciphering bureaucratic structures, citizens simply state their objective in everyday language.

### 1. Citizen Experience
* **Intent-Based Discovery**: Citizens express goals naturally (e.g., *"I need income proof for college fee concession"*), and JANSAHAY matches the statutory service with plain-language explanations.
* **Personalized Checklist**: A guided 3-question eligibility screening generates an exact document checklist, eliminating guesswork and application rejection.
* **The Case Passport**: A unified tracking interface answering four fundamental questions: *What happened? What does it mean? Do I need to do anything? What happens next?*

### 2. Universal Engineering & Security
* **Universal Case Engine**: One declarative workflow engine powers diverse domains—Statutory Revenue Certificates, EPFO Claim Transfers, and Civic Grievances—under a unified lifecycle.
* **Contextual RBAC**: Server-side authorization enforces strict role, department, and jurisdiction boundaries (`can(actor, action, resource)`) with optimistic concurrency locks.
* **Tamper-Evident Audit Ledger**: Every workflow action is cryptographically chained via SHA-256 hashes, providing verifiable event integrity.
* **Bounded Assistive AI**: AI provides discovery guidance and simplified explanations with zero decision-making or state-mutation authority.

### 3. Prototype Integrity
JANSAHAY is built as an independent hackathon prototype operating on 100% synthetic citizen profiles, mock attachments, and simulated workflows without live government integration.
