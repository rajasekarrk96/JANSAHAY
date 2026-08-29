"""Supplementary captures: deep scroll of the SHA-256 audit ledger on the resolved case."""
import os, time, json
from playwright.sync_api import sync_playwright

SP = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(SP, "shots")
BASE = "http://127.0.0.1:8011"

meta = json.load(open(os.path.join(SP, "capture_manifest.json")))
PUBLIC_ID = meta["public_case_id"]

FETCH_CASE = """
async (pid) => {
  const resp = await fetch('/api/v1/cases/' + pid, {headers:{'Authorization':'Bearer ' + app.token}});
  if (!resp.ok) return {ok:false, http: resp.status};
  app.currentCaseDetail = await resp.json();
  return {ok:true, state: app.currentCaseDetail.current_state,
          audits: (app.currentCaseDetail.audit_events||[]).length};
}
"""

SCROLL_MODAL = """
px => { const m = document.querySelector('#case-detail-modal');
        const sc = m.querySelector('.overflow-y-auto') || m;
        sc.scrollTop = px; return sc.scrollTop; }
"""

SCROLL_AUDIT = """
px => { const el = document.getElementById('modal-audit-timeline');
        el.scrollTop = px; return [el.scrollTop, el.scrollHeight, el.clientHeight]; }
"""

# Give the audit ledger room to breathe so the whole chain is legible on screen.
EXPAND_AUDIT = """
() => { const el = document.getElementById('modal-audit-timeline');
        el.classList.remove('max-h-48');
        el.style.maxHeight = 'none';
        return el.scrollHeight; }
"""


def shot(page, name, settle=0.5):
    time.sleep(settle)
    page.screenshot(path=os.path.join(SHOTS, name + ".png"))
    print("shot:", name)


with sync_playwright() as p:
    b = p.chromium.launch(args=["--force-device-scale-factor=1", "--hide-scrollbars"])
    ctx = b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    pg = ctx.new_page()
    pg.on("dialog", lambda d: d.accept(d.default_value or ""))

    pg.evaluate  # noqa
    pg.goto(BASE, wait_until="networkidle")
    pg.evaluate("u => localStorage.setItem('jansahay_persona', u)", "citizen_rahul")
    pg.goto(BASE, wait_until="networkidle")
    pg.wait_for_function("() => typeof app !== 'undefined' && app.currentUser", timeout=20000)
    pg.wait_for_timeout(1200)

    info = pg.evaluate(FETCH_CASE, PUBLIC_ID)
    print("case:", PUBLIC_ID, info)
    pg.evaluate("() => app.renderCaseModal()")
    pg.wait_for_selector("#case-detail-modal:not(.hidden)", timeout=10000)
    pg.wait_for_timeout(900)

    # audit ledger, scrolled within its own pane
    pg.evaluate(SCROLL_MODAL, 1700)
    print("audit pane:", pg.evaluate(SCROLL_AUDIT, 0))
    shot(pg, "s7_ledger_top")
    pg.evaluate(SCROLL_AUDIT, 200)
    shot(pg, "s7_ledger_mid")
    pg.evaluate(SCROLL_AUDIT, 9999)
    shot(pg, "s7_ledger_end")

    # full chain expanded so all four events are visible at once
    h = pg.evaluate(EXPAND_AUDIT)
    print("expanded audit height:", h)
    pg.evaluate(SCROLL_MODAL, 9999)
    shot(pg, "s7_ledger_full")
    pg.evaluate(SCROLL_MODAL, 1500)
    shot(pg, "s7_ledger_full_upper")

    ctx.close(); b.close()
