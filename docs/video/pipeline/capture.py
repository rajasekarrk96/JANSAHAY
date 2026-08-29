"""Drive the live JANSAHAY app and capture real UI stills for the 2-minute demo video."""
import os, time, json
from playwright.sync_api import sync_playwright

SP = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(SP, "shots")
DOCS = os.path.join(SP, "mockdocs")
BASE = "http://127.0.0.1:8011"
os.makedirs(SHOTS, exist_ok=True)

manifest = []

FETCH_CASE = """
async (id) => {
  const resp = await fetch('/api/v1/cases/' + id, {headers:{'Authorization':'Bearer ' + app.token}});
  if (!resp.ok) return {ok:false, http: resp.status};
  app.currentCaseDetail = await resp.json();
  const c = app.currentCaseDetail;
  return {ok:true, state: c.current_state, version: c.version_id,
          audits: (c.audit_events||[]).length,
          actions: (c.available_actions||[]).map(a => a.action)};
}
"""

DO_ACTION = """
async (args) => {
  const c = app.currentCaseDetail;
  const docVerifs = (c.documents || []).map(d => ({document_id: d.id, status: 'VERIFIED', notes: args.remarks}));
  const resp = await fetch('/api/v1/cases/' + args.id + '/actions/' + args.action, {
    method: 'POST',
    headers: {'Content-Type':'application/json', 'Authorization':'Bearer ' + app.token},
    body: JSON.stringify({version_id: c.version_id, remarks: args.remarks,
                          document_verifications: docVerifs.length ? docVerifs : null})
  });
  if (!resp.ok) { const e = await resp.json(); return {ok:false, http: resp.status, detail: e.detail}; }
  app.currentCaseDetail = await resp.json();
  return {ok:true, state: app.currentCaseDetail.current_state, version: app.currentCaseDetail.version_id};
}
"""

SCROLL_MODAL = """
px => {
  const m = document.querySelector('#case-detail-modal');
  const sc = m.querySelector('.overflow-y-auto') || m;
  sc.scrollTop = px;
  return sc.scrollTop;
}
"""


def shot(page, name, settle=0.35):
    time.sleep(settle)
    page.screenshot(path=os.path.join(SHOTS, name + ".png"))
    manifest.append(name)
    print("shot:", name)


def set_persona(page, username, wait_view=None):
    page.evaluate("u => localStorage.setItem('jansahay_persona', u)", username)
    page.goto(BASE, wait_until="networkidle")
    page.wait_for_function("() => typeof app !== 'undefined' && app.currentUser", timeout=20000)
    if wait_view:
        page.wait_for_selector(wait_view, timeout=20000)
    page.wait_for_timeout(1200)


def open_case(page, cid):
    info = page.evaluate(FETCH_CASE, cid)
    assert info.get("ok"), f"case fetch failed: {info}"
    page.evaluate("() => app.renderCaseModal()")
    page.wait_for_selector("#case-detail-modal:not(.hidden)", timeout=10000)
    page.wait_for_timeout(800)
    return info


def do_action(page, cid, action, remarks):
    res = page.evaluate(DO_ACTION, {"id": cid, "action": action, "remarks": remarks})
    print("   action", action, "->", res)
    if res.get("ok"):
        page.evaluate("() => app.renderCaseModal()")
        page.wait_for_timeout(900)
    return res


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--force-device-scale-factor=1", "--hide-scrollbars"])
    ctx = browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept(d.default_value or ""))
    page.on("pageerror", lambda e: print("PAGEERROR:", str(e)[:200]))

    page.goto(BASE, wait_until="networkidle")
    page.wait_for_function("() => typeof app !== 'undefined' && app.services && app.services.length > 0", timeout=30000)
    page.wait_for_timeout(1200)

    # ---------------- SCENE 1: home / hero ----------------
    shot(page, "s1_home_hero", 1.0)

    # ---------------- SCENE 2: natural-language service discovery ----------------
    q = "I need an income certificate for college"
    box = page.locator("#service-search-input")
    box.click()
    typed = ""
    marks = {12: "a", 21: "b", 33: "c", len(q): "d"}
    for i, ch in enumerate(q, 1):
        typed += ch
        box.fill(typed)
        page.wait_for_timeout(15)
        if i in marks:
            shot(page, f"s2_typing_{marks[i]}", 0.12)
    page.evaluate("() => app.discoverService()")
    page.wait_for_selector("#service-recommendation-card:not(.hidden)", timeout=10000)
    shot(page, "s2_recommendation", 0.9)

    # ---------------- SCENE 3: eligibility + tailored checklist ----------------
    page.evaluate("() => app.startRecommendedService()")
    page.wait_for_selector("#wizard-step-1:not(.hidden)", timeout=10000)
    shot(page, "s3_eligibility", 0.9)

    page.evaluate("() => app.wizardNext(2)")
    page.wait_for_selector("#wizard-step-2:not(.hidden)", timeout=10000)
    shot(page, "s3_checklist", 0.9)

    # ---------------- SCENE 4: sandboxed upload, declaration, submit ----------------
    page.evaluate("() => app.wizardNext(3)")
    page.wait_for_selector("#wizard-step-3:not(.hidden)", timeout=10000)
    shot(page, "s4_upload_empty", 0.7)

    files = sorted(os.listdir(DOCS))
    inputs = page.locator("#upload-dropzones-container input[type=file]")
    n = inputs.count()
    print("file inputs:", n)
    for i in range(n):
        inputs.nth(i).set_input_files(os.path.join(DOCS, files[i % len(files)]))
        page.wait_for_timeout(700)
        if i == 0:
            shot(page, "s4_upload_scanning", 0.15)
    page.wait_for_timeout(900)
    shot(page, "s4_upload_passed", 0.5)

    page.evaluate("() => app.wizardNext(4)")
    page.wait_for_selector("#wizard-step-4:not(.hidden)", timeout=10000)
    shot(page, "s4_declaration", 0.7)
    page.check("#decl-checkbox")
    shot(page, "s4_declaration_checked", 0.5)

    page.evaluate("() => app.submitApplication()")
    page.wait_for_timeout(2500)
    page.evaluate("() => app.navigate('my-cases')")
    page.wait_for_timeout(1500)
    shot(page, "s4_my_cases", 0.8)

    cid = page.evaluate("""async () => {
        const r = await fetch('/api/v1/cases', {headers:{'Authorization':'Bearer ' + app.token}});
        const cs = await r.json();
        cs.sort((a,b) => new Date(b.submitted_at) - new Date(a.submitted_at));
        return cs[0].id;
    }""")
    print("case id:", cid)

    info = open_case(page, cid)
    print("citizen view:", info)
    public_id = page.locator("#modal-public-id").inner_text()
    print("public case id:", public_id)
    shot(page, "s4_case_passport", 0.6)

    page.evaluate(SCROLL_MODAL, 300)
    shot(page, "s4_case_status_detail", 0.7)
    page.evaluate(SCROLL_MODAL, 0)
    page.evaluate("() => app.closeCaseModal()")

    # ---------------- SCENE 6: universal catalog, one engine ----------------
    page.evaluate("() => app.navigate('home')")
    page.wait_for_timeout(600)
    for cat, label in [("ALL", "all"), ("CERTIFICATES", "certificates"),
                       ("SOCIAL_SECURITY", "epfo"), ("GRIEVANCES", "grievances")]:
        page.evaluate("c => app.setCategoryFilter(c)", cat)
        page.wait_for_timeout(500)
        page.evaluate("() => window.scrollTo(0, 330)")
        shot(page, f"s6_catalog_{label}", 0.45)
    page.evaluate("() => window.scrollTo(0, 0)")
    page.evaluate("() => app.setCategoryFilter('ALL')")

    # ---------------- SCENE 8: bounded assistive AI ----------------
    page.evaluate("() => app.openAIChat()")
    page.wait_for_timeout(500)
    shot(page, "s8_ai_drawer_open", 0.5)
    ai_input = page.locator("#ai-input")
    typed = ""
    for ch in "What does the verification stage mean for my case?":
        typed += ch
        ai_input.fill(typed)
        page.wait_for_timeout(10)
    shot(page, "s8_ai_question", 0.4)
    page.evaluate("() => app.sendAIMessage()")
    page.wait_for_timeout(1800)
    shot(page, "s8_ai_answer", 0.6)
    page.evaluate("() => app.closeAIChat()")

    # ---------------- SCENE 5 + 7: officer workflow, RBAC, audit ----------------
    set_persona(page, "vo_delhi_rev", "#view-officer-queue:not(.hidden)")
    shot(page, "s5_officer_queue", 0.8)
    shot(page, "s7_rbac_context", 0.2)

    info = open_case(page, cid)
    print("VO view:", info)
    shot(page, "s5_officer_case_open", 0.6)

    page.evaluate(SCROLL_MODAL, 1500)
    shot(page, "s7_audit_chain", 0.8)
    page.evaluate(SCROLL_MODAL, 0)

    # RBAC probe: verification officer attempting a final approval outside desk authority
    denied = page.evaluate(DO_ACTION, {"id": cid, "action": "APPROVE",
                                       "remarks": "Attempting approval outside desk authority."})
    print("RBAC denial probe:", denied)
    open_case(page, cid)

    if "VERIFY" in info["actions"]:
        do_action(page, cid, "VERIFY", "Documents verified against statutory guidelines.")
        shot(page, "s5_after_verify", 0.7)
        page.evaluate(SCROLL_MODAL, 1500)
        shot(page, "s7_audit_chain_grown", 0.8)
        page.evaluate(SCROLL_MODAL, 0)
    page.evaluate("() => app.closeCaseModal()")

    # advance through remaining desks to RESOLVED
    for persona, action in [("do_delhi_rev", "FORWARD"), ("ao_delhi_rev", "APPROVE")]:
        set_persona(page, persona, "#view-officer-queue:not(.hidden)")
        info = open_case(page, cid)
        print(persona, info)
        if persona == "do_delhi_rev":
            shot(page, "s7_dept_officer_view", 0.5)
        target = action if action in info["actions"] else (info["actions"][0] if info["actions"] else None)
        if target:
            do_action(page, cid, target, "Scrutiny complete; recommended for next stage.")
        page.evaluate("() => app.closeCaseModal()")

    # ---------------- SCENE 9: resolved Case Passport + digital seal ----------------
    set_persona(page, "citizen_rahul", "#view-home:not(.hidden)")
    page.evaluate("() => app.navigate('my-cases')")
    page.wait_for_timeout(1400)
    shot(page, "s9_my_cases_resolved", 0.6)

    info = open_case(page, cid)
    print("final:", info)
    shot(page, "s9_case_resolved", 0.8)
    page.evaluate(SCROLL_MODAL, 1150)
    shot(page, "s9_certificate_seal", 0.8)
    page.evaluate(SCROLL_MODAL, 1700)
    shot(page, "s7_audit_chain_final", 0.8)

    meta = {"public_case_id": public_id, "final_state": info["state"],
            "audit_events": info["audits"], "rbac_denial": denied, "shots": manifest}
    with open(os.path.join(SP, "capture_manifest.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(json.dumps(meta, indent=2)[:900])

    ctx.close(); browser.close()
