"""Shared timeline: scenes, shot segments, and narration cues for the 2-minute demo."""

W, H, FPS = 1920, 1080, 30
TOTAL = 119.0          # 1:59 - inside the 2:00 hard cap
FADE_IN, FADE_OUT = 0.8, 0.9
XFADE = 0.45           # crossfade between shots

# ---------------------------------------------------------------- scenes
# (number, title chip, start, end)
SCENES = [
    (1, "Public Services Organized Around Your Goal",      0.0,   8.0),
    (2, "Tell us what you need",                            8.0,  18.0),
    (3, "Your personalized checklist",                     18.0,  30.0),
    (4, "Your Case Passport",                              30.0,  52.0),
    (5, "Authorized workflow",                             52.0,  60.0),
    (6, "Universal Case Engine",                           60.0,  75.0),
    (7, "Authorized access · Audit history",               75.0, 100.0),
    (8, "Assistive AI · Synthetic Prototype",             100.0, 115.0),
    (9, "One citizen journey. One case. One timeline.",   115.0, 119.0),
]

# ---------------------------------------------------------------- shots
# (shot_name, start, end, focus_rect_or_None)
# focus rect = (x0, y0, x1, y1) in 1920x1080 source coords; the renderer
# expands it to 16:9 and eases from the full frame toward it.
SHOTS = [
    # Scene 1 - the problem, and JANSAHAY's answer
    ("s1_home_hero",            0.0,   8.0,  (352, 220, 1568, 730)),

    # Scene 2 - natural-language service discovery
    ("s2_typing_a",             8.0,   9.3,  (380, 330, 1560, 560)),
    ("s2_typing_b",             9.3,  10.6,  (380, 330, 1560, 560)),
    ("s2_typing_c",            10.6,  11.9,  (380, 330, 1560, 560)),
    ("s2_typing_d",            11.9,  13.2,  (380, 330, 1560, 560)),
    ("s2_recommendation",      13.2,  18.0,  (380, 400, 1170, 700)),

    # Scene 3 - guided eligibility, tailored checklist
    ("s3_eligibility",         18.0,  24.0,  (400, 230, 1520, 720)),
    ("s3_checklist",           24.0,  30.0,  (400, 230, 1520, 720)),

    # Scene 4 - sandboxed upload, declaration, submission, Case Passport
    ("s4_upload_empty",        30.0,  33.0,  (400, 230, 1520, 730)),
    ("s4_upload_scanning",     33.0,  35.4,  (400, 300, 1520, 700)),
    ("s4_upload_passed",       35.4,  38.4,  (400, 300, 1520, 700)),
    ("s4_declaration",         38.4,  40.6,  (400, 250, 1520, 720)),
    ("s4_declaration_checked", 40.6,  42.8,  (400, 400, 1520, 720)),
    ("s4_my_cases",            42.8,  45.0,  (340, 120, 1580, 560)),
    ("s4_case_passport",       45.0,  48.8,  (520,  60, 1400, 360)),
    ("s4_case_status_detail",  48.8,  52.0,  (520, 130, 1400, 470)),

    # Scene 5 - the case moves through the right officers
    ("s5_officer_queue",       52.0,  55.4,  (340, 100, 1580, 460)),
    ("s5_officer_case_open",   55.4,  57.6,  (520,  60, 1400, 400)),
    ("s5_after_verify",        57.6,  60.0,  (520,  60, 1400, 400)),

    # Scene 6 - one engine, many services
    ("s6_catalog_all",         60.0,  63.7,  None),
    ("s6_catalog_certificates",63.7,  67.4,  None),
    ("s6_catalog_epfo",        67.4,  71.2,  None),
    ("s6_catalog_grievances",  71.2,  75.0,  None),

    # Scene 7 - server-side RBAC, rejected actions, tamper-evident audit
    ("s7_rbac_context",        75.0,  81.0,  (352, 110, 1580, 300)),
    ("s7_dept_officer_view",   81.0,  84.0,  (352, 110, 1580, 300)),
    ("s5_officer_case_open",   84.0,  91.6,  (520, 380, 1400, 900)),   # + denial callout
    ("s7_ledger_full",         91.6,  96.2,  (520, 540, 1400, 960)),
    ("s7_ledger_full",         96.2, 100.0,  (520, 540, 1400, 760)),

    # Scene 8 - bounded assistive AI, synthetic-data disclosure
    ("s8_ai_drawer_open",     100.0, 103.2,  (1480, 660, 1910, 1070)),
    ("s8_ai_question",        103.2, 106.4,  (1480, 660, 1910, 1070)),
    ("s8_ai_answer",          106.4, 111.0,  (1480, 660, 1910, 1070)),
    ("s8_ai_answer",          111.0, 115.0,  (300,    0, 1620,  120)),  # amber disclosure banner

    # Scene 9 - one case, one timeline, digitally sealed
    ("s9_certificate_seal",   115.0, 119.0,  (520, 470, 1400, 730)),
]

# ---------------------------------------------------------------- narration
# Sentence-level cues; time is split across each scene by word count.
NARRATION = {
    1: ["Government services can be difficult to navigate.",
        "JANSAHAY makes the journey simpler, starting with what the citizen actually needs."],
    2: ["Instead of searching through departments, the citizen simply describes their goal."],
    3: ["JANSAHAY asks a few simple questions and shows exactly what documents are needed."],
    4: ["The citizen uploads the required documents and submits the application.",
        "A Case Passport is created immediately.",
        "The citizen can see where the case is and what happens next."],
    5: ["Behind the scenes, the case moves through the right officers."],
    6: ["Technically, JANSAHAY uses one case engine and one workflow engine.",
        "The same system can support certificates, EPFO claims, and grievances."],
    7: ["Security is enforced on the server.",
        "Officers only see cases and actions allowed for their role, department, and jurisdiction.",
        "Invalid actions are rejected.",
        "Every important workflow action is recorded in a tamper-evident audit history."],
    8: ["AI helps with service discovery and simple explanations.",
        "It cannot approve, reject, or change a case.",
        "This prototype uses synthetic data and mocked government integrations."],
    9: ["JANSAHAY puts the citizen's journey first."],
}

# The server's real 403 response, captured during the recorded run.
DENIAL_CALLOUT = {
    "start": 85.2, "end": 91.6,
    "request": "POST /api/v1/cases/{id}/actions/APPROVE",
    "status": "403 Forbidden",
    "detail": "Actor role VERIFICATION_OFFICER is not authorized "
              "to execute APPROVE on this case.",
}


def build_cues():
    """Expand NARRATION into timed cues (start, end, text)."""
    cues = []
    for num, chip, s, e in SCENES:
        lines = NARRATION[num]
        span = e - s
        weights = [max(1, len(l.split())) for l in lines]
        total_w = sum(weights)
        # leave a small tail of silence in each scene so lines don't run together
        usable = span - min(0.6, span * 0.08)
        t = s
        for line, w in zip(lines, weights):
            d = usable * (w / total_w)
            cues.append((round(t, 3), round(t + d, 3), line))
            t += d
    return cues


if __name__ == "__main__":
    words = sum(len(l.split()) for ls in NARRATION.values() for l in ls)
    print(f"total {TOTAL}s  words={words}  wpm={words / (TOTAL / 60):.1f}")
    for s, e, txt in build_cues():
        print(f"  {s:6.2f} -> {e:6.2f}  ({e-s:4.2f}s) {txt}")
