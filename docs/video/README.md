# JANSAHAY — Video Documentation & Demo Package

## Overview
This directory contains the **rendered 2-minute hackathon demonstration video**, plus the
storyboard, narration script, scene-by-scene timing log, verification checklist, and the
reproducible pipeline that produced the video.

Every frame in the video is a real screenshot of the running JANSAHAY application, captured
by driving the live app end-to-end (Playwright against `uvicorn`) — not a mockup. The case
shown, `JS-2026-INC-68909`, was created, verified, forwarded, approved and resolved through
the real API during the capture run.

---

## Directory Contents

| File | Description |
|:---|:---|
| **[`jansahay_demo_2min_narrated.mp4`](jansahay_demo_2min_narrated.mp4)** | **Submission candidate.** 1920×1080, 30 fps, **1:59**, with machine-generated narration and burned-in captions. |
| **[`jansahay_demo_2min_silent.mp4`](jansahay_demo_2min_silent.mp4)** | Identical picture, **no audio** — the master to dub your own voice-over onto. |
| **[`narration.srt`](narration.srt)** | Timed narration cues; load in any editor as a teleprompter or subtitle track. |
| **[`jansahay_demo_poster.jpg`](jansahay_demo_poster.jpg)** | Poster / thumbnail frame (Case Passport at 00:46). |
| **[`script.md`](script.md)** | 9-scene storyboard, voice-over text, and screen actions. |
| **[`recording-checklist.md`](recording-checklist.md)** | Pre-flight and post-recording verification matrix. |
| **[`final-timestamp-log.md`](final-timestamp-log.md)** | Second-by-second cue log. |
| **[`jansahay_demo_walkthrough.webp`](jansahay_demo_walkthrough.webp)** | Earlier animated walkthrough (11 frames). |
| **[`pipeline/`](pipeline/)** | Scripts that regenerate the video from the live app. |

---

## Which file do I submit?

- Submitting today, no time to record: use **`jansahay_demo_2min_narrated.mp4`** as-is.
- Want a human voice (recommended — the script asks for calm, clear Indian English):
  record over **`jansahay_demo_2min_silent.mp4`** using `narration.srt` as the teleprompter.
  The picture already carries burned-in captions, so the timing is visible while you read.

The synthesised narration uses the only English voices installed on this machine
(`Microsoft Zira Desktop`, US English). It is a placeholder, not a substitute for the
delivery the script describes.

---

## Scene Map (as rendered)

| Scene | Time | On Screen |
|:---|:---|:---|
| 1 | `00:00–00:08` | Citizen home, hero: *Public Services Organized Around Your Goal* |
| 2 | `00:08–00:18` | Typing *"I need an income certificate for college"* → AI recommendation card |
| 3 | `00:18–00:30` | Guided eligibility questionnaire → tailored 3-document checklist |
| 4 | `00:30–00:52` | Quarantined upload sandbox → statutory declaration → Case Passport (`JS-2026-INC-68909`) with live 5-step stepper and the 4-question status card |
| 5 | `00:52–01:00` | Officer Scrutiny Queue (`Sunil Verma`, `REV-VO-401`) → case advanced |
| 6 | `01:00–01:15` | Catalog tabs: Certificates · Social Security & EPFO · Public Grievances |
| 7 | `01:15–01:40` | Role/department/jurisdiction scoping, the real **403** response to an out-of-role `APPROVE`, and the SHA-256 audit ledger (`Chain Intact ✓`) |
| 8 | `01:40–01:55` | Assistive AI drawer, then the amber synthetic-prototype disclosure banner |
| 9 | `01:55–01:59` | Resolved Case Passport with the digital grant seal |

Total runtime **1:59** — inside the 2:00 hard cap.

### Shown on screen, verbatim from the server
The security callout at `01:25` is the actual API response captured during the run, not a
graphic:

```
POST /api/v1/cases/{id}/actions/APPROVE       403 Forbidden
"Actor role VERIFICATION_OFFICER is not authorized to execute APPROVE on this case."
```

---

## Regenerating the Video

Requires `playwright` (+ `playwright install chromium`), `pillow`, `numpy`,
`opencv-python`, `imageio-ffmpeg`.

```bash
# 1. run the app (the capture scripts expect port 8011)
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8011

# 2. drive the live app and capture the stills
python docs/video/pipeline/capture.py        # full citizen -> officer -> resolved journey
python docs/video/pipeline/supplement.py     # deep scroll of the audit ledger

# 3. render picture, then narration, then mux
python docs/video/pipeline/render_video.py   # -> jansahay_demo_2min_silent.mp4
python docs/video/pipeline/gen_audio.py      # -> narration.wav + narration.srt
ffmpeg -i jansahay_demo_2min_silent.mp4 -i narration.wav \
       -c:v copy -c:a aac -b:a 160k -shortest jansahay_demo_2min_narrated.mp4
```

`pipeline/timeline.py` holds every scene boundary, shot, focus rect and narration line —
edit it there and re-run `render_video.py` to retime the cut.

---

## Hackathon Evaluation Alignment

### 1. Structure (50/50 Split)
- **00:00 – 01:00 (Citizen Experience)**: natural language service discovery, tailored
  3-question eligibility, quarantined upload sandbox, submission, Case Passport, the
  4-question plain-language status card, and desk officer scrutiny.
- **01:00 – 02:00 (Technical & Security Deep Dive)**: the Universal Case Engine, declarative
  workflow state machine, contextual RBAC authorization, tamper-evident SHA-256 audit ledger,
  optimistic concurrency (`Case Version`), and bounded assistive AI.

### 2. Safety & Compliance
- **100% Synthetic Personas**: Rahul Sharma (`citizen_rahul`), Sunil Verma (`vo_delhi_rev`),
  Priya Nair (`do_delhi_rev`), Rajesh Kumar (`ao_delhi_rev`), synthetic Aadhaar (`****4321`).
- **Synthetic Attachments**: the three uploaded PDFs are generated placeholders named
  `SYNTHETIC_*.pdf`; their content is a single "NOT A REAL DOCUMENT" line.
- **Zero Live Connections**: no access to UIDAI, DigiLocker, or EPFO production systems.
- **Clear Disclosures**: the amber prototype banner is visible in every frame of the video.

---

## Running the Demo Locally
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
