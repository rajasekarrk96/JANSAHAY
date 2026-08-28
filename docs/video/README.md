# JANSAHAY — Video Documentation & Demo Package

## Overview
This directory contains the full storyboard, narration script, scene-by-scene timing log, and verification checklist for the **2-minute JANSAHAY hackathon demonstration video**.

---

## Directory Contents

| File | Description |
|:---|:---|
| **[`jansahay_demo_walkthrough.webp`](jansahay_demo_walkthrough.webp)** | **Recorded visual walkthrough animation** demonstrating full citizen journey, Case Passport, and officer review. |
| **[`script.md`](script.md)** | Complete 2-minute video script, voice-over text (242 words), and screen actions. |
| **[`recording-checklist.md`](recording-checklist.md)** | Pre-flight and post-recording verification matrix and quality checklist. |
| **[`final-timestamp-log.md`](final-timestamp-log.md)** | Exact second-by-second cue log synchronized with screen transitions. |

---

## Hackathon Evaluation Alignment

### 1. Structure (50/50 Split)
- **00:00 – 01:00 (Citizen Experience)**: Demonstrates natural language service discovery, tailored 3-question eligibility, quarantined upload sandbox, submission, Case Passport, 4-question plain-language milestone timeline, and desk officer scrutiny.
- **01:00 – 02:00 (Technical & Security Deep Dive)**: Demonstrates the Universal Case Engine, declarative workflow state machine, contextual RBAC authorization, tamper-evident SHA-256 audit ledger, optimistic concurrency, and bounded assistive AI.

### 2. Safety & Compliance
- **100% Synthetic Personas**: Rahul Sharma (`citizen_rahul`), Sunil Verma (`vo_delhi_rev`), synthetic Aadhaar (`****4321`), mock PDF attachments.
- **Zero Live Connections**: No access to UIDAI, DigiLocker, or EPFO production systems.
- **Clear Disclosures**: Prominently displays prototype status and mock integration boundaries.

---

## Running the Demo Locally
To launch the interactive demo application shown in the video:
```bash
# Using Docker Compose
docker compose up --build

# Or natively with Python
cd backend
pip install -r requirements.txt
python -m app.db.init_db
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.
