import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import AsyncSessionLocal
from app.db.init_db import init_db_data

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/admin/reset-demo")

@pytest.mark.asyncio
async def test_auth_login_and_me():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Citizen login
        res = await client.post("/api/v1/auth/login", json={"username": "citizen_rahul", "password": "Password123!"})
        assert res.status_code == 200
        data = res.json()
        assert data["user"]["role"] == "CITIZEN"
        token = data["access_token"]

        # 2. Get me
        me_res = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_res.status_code == 200
        assert me_res.json()["username"] == "citizen_rahul"

@pytest.mark.asyncio
async def test_citizen_cross_tenant_isolation():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Login Anita (Citizen 2)
        res_anita = await client.post("/api/v1/auth/login", json={"username": "citizen_anita", "password": "Password123!"})
        token_anita = res_anita.json()["access_token"]

        # Attempt to access Rahul's case (JS-2026-INC-48192)
        res = await client.get("/api/v1/cases/JS-2026-INC-48192", headers={"Authorization": f"Bearer {token_anita}"})
        assert res.status_code == 403 # DENY cross-tenant access

@pytest.mark.asyncio
async def test_officer_cross_department_isolation():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Login EPFO Verifier
        res_epfo = await client.post("/api/v1/auth/login", json={"username": "vo_epfo_delhi", "password": "Password123!"})
        token_epfo = res_epfo.json()["access_token"]

        # Attempt to view/action Revenue Department's Income Certificate Case
        res = await client.get("/api/v1/cases/JS-2026-INC-48192", headers={"Authorization": f"Bearer {token_epfo}"})
        assert res.status_code == 403 # DENY cross-department access

@pytest.mark.asyncio
async def test_full_certificate_workflow_journey():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Step 1: Verification Officer (Sunil Verma) verifies documents and forwards
        res_vo = await client.post("/api/v1/auth/login", json={"username": "vo_delhi_rev", "password": "Password123!"})
        token_vo = res_vo.json()["access_token"]

        # Fetch case
        case_res = await client.get("/api/v1/cases/JS-2026-INC-48192", headers={"Authorization": f"Bearer {token_vo}"})
        case_data = case_res.json()
        assert case_data["current_state"] == "VERIFICATION"
        doc_ids = [d["id"] for d in case_data["documents"]]

        # Action: VERIFY
        verify_payload = {
            "version_id": case_data["version_id"],
            "remarks": "All proofs verified against Delhi Revenue Land guidelines.",
            "document_verifications": [
                {"document_id": doc_ids[0], "status": "VERIFIED"},
                {"document_id": doc_ids[1], "status": "VERIFIED"},
                {"document_id": doc_ids[2], "status": "VERIFIED"}
            ]
        }
        action_res = await client.post(
            "/api/v1/cases/JS-2026-INC-48192/actions/VERIFY",
            json=verify_payload,
            headers={"Authorization": f"Bearer {token_vo}"}
        )
        assert action_res.status_code == 200
        assert action_res.json()["current_state"] == "DEPARTMENT_REVIEW"

        # Step 2: Department Officer (Priya Nair) scrutinizes and forwards
        res_do = await client.post("/api/v1/auth/login", json={"username": "do_delhi_rev", "password": "Password123!"})
        token_do = res_do.json()["access_token"]

        forward_payload = {
            "version_id": action_res.json()["version_id"],
            "remarks": "Scrutiny complete. Recommending grant of Income Certificate."
        }
        fwd_res = await client.post(
            "/api/v1/cases/JS-2026-INC-48192/actions/FORWARD",
            json=forward_payload,
            headers={"Authorization": f"Bearer {token_do}"}
        )
        assert fwd_res.status_code == 200
        assert fwd_res.json()["current_state"] == "APPROVAL"

        # Step 3: Approving Officer (Rajesh Kumar, Tahsildar) grants approval
        res_ao = await client.post("/api/v1/auth/login", json={"username": "ao_delhi_rev", "password": "Password123!"})
        token_ao = res_ao.json()["access_token"]

        approve_payload = {
            "version_id": fwd_res.json()["version_id"],
            "remarks": "Approved. Certificate issued under Delhi Executive Magisterial seal."
        }
        app_res = await client.post(
            "/api/v1/cases/JS-2026-INC-48192/actions/APPROVE",
            json=approve_payload,
            headers={"Authorization": f"Bearer {token_ao}"}
        )
        assert app_res.status_code == 200
        assert app_res.json()["current_state"] == "RESOLVED"

        # Step 4: Verify Cryptographic Audit Trail is unbroken
        audit_res = await client.get("/api/v1/admin/verify-audit-chain/JS-2026-INC-48192")
        assert audit_res.status_code == 200
        assert audit_res.json()["is_chain_unbroken"] is True
        assert audit_res.json()["event_count"] >= 5

@pytest.mark.asyncio
async def test_stale_write_optimistic_locking():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res_vo = await client.post("/api/v1/auth/login", json={"username": "vo_delhi_rev", "password": "Password123!"})
        token_vo = res_vo.json()["access_token"]

        # Intentionally provide outdated version_id (e.g. 99)
        payload = {
            "version_id": 99,
            "remarks": "Trying to update with stale version."
        }
        res = await client.post(
            "/api/v1/cases/JS-2026-INC-48192/actions/VERIFY",
            json=payload,
            headers={"Authorization": f"Bearer {token_vo}"}
        )
        assert res.status_code == 409 # Stale write returns 409 Conflict

@pytest.mark.asyncio
async def test_deficiency_and_correction_loop():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Step 1: Officer requests correction
        res_vo = await client.post("/api/v1/auth/login", json={"username": "vo_delhi_rev", "password": "Password123!"})
        token_vo = res_vo.json()["access_token"]

        case_res = await client.get("/api/v1/cases/JS-2026-INC-48192", headers={"Authorization": f"Bearer {token_vo}"})
        case_data = case_res.json()
        doc_to_reject = case_data["documents"][1]["id"] # Salary Slip

        req_payload = {
            "version_id": case_data["version_id"],
            "remarks": "Salary slip scan is blurred. Please upload legible scan.",
            "document_verifications": [
                {"document_id": doc_to_reject, "status": "REPLACEMENT_REQUIRED", "notes": "Scan blurred."}
            ]
        }
        req_res = await client.post(
            "/api/v1/cases/JS-2026-INC-48192/actions/REQUEST_CORRECTION",
            json=req_payload,
            headers={"Authorization": f"Bearer {token_vo}"}
        )
        assert req_res.status_code == 200
        assert req_res.json()["current_state"] == "ACTION_REQUIRED"

        # Step 2: Citizen uploads replacement file and resubmits
        res_cit = await client.post("/api/v1/auth/login", json={"username": "citizen_rahul", "password": "Password123!"})
        token_cit = res_cit.json()["access_token"]

        # Upload replacement
        upload_res = await client.post(
            "/api/v1/documents/upload",
            data={"requirement_id": case_data["documents"][1]["requirement_id"], "case_id": case_data["id"]},
            files={"file": ("salary_slip_clear.pdf", b"%PDF-1.4 Legible clear replacement scan", "application/pdf")},
            headers={"Authorization": f"Bearer {token_cit}"}
        )
        assert upload_res.status_code == 201
        new_doc_id = upload_res.json()["id"]

        # Resubmit document
        resub_payload = {
            "version_id": req_res.json()["version_id"],
            "replacement_document_id": new_doc_id,
            "target_document_id": doc_to_reject,
            "remarks": "Uploaded high-resolution scanned salary certificate."
        }
        resub_res = await client.post(
            f"/api/v1/cases/{case_data['id']}/resubmit-document",
            json=resub_payload,
            headers={"Authorization": f"Bearer {token_cit}"}
        )
        assert resub_res.status_code == 200
        assert resub_res.json()["current_state"] == "VERIFICATION"

@pytest.mark.asyncio
async def test_epfo_and_grievance_parity():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Citizen creates EPFO claim
        res_cit = await client.post("/api/v1/auth/login", json={"username": "citizen_rahul", "password": "Password123!"})
        token_cit = res_cit.json()["access_token"]

        srvs = await client.get("/api/v1/services")
        epfo_srv = next(s for s in srvs.json() if s["code"] == "EPFO_CLAIM_TRANSFER")
        grv_srv = next(s for s in srvs.json() if s["code"] == "STREET_LIGHT_GRIEVANCE")

        # Submit EPFO Case
        epfo_case_res = await client.post(
            "/api/v1/cases",
            json={
                "service_id": epfo_srv["id"],
                "jurisdiction_id": "",
                "form_data": {"uan": "100982718291", "prev_member_id": "DLCPM001928300001"}
            },
            headers={"Authorization": f"Bearer {token_cit}"}
        )
        assert epfo_case_res.status_code == 201
        assert "EPF" in epfo_case_res.json()["public_case_id"]

        # Submit Grievance Case
        grv_case_res = await client.post(
            "/api/v1/cases",
            json={
                "service_id": grv_srv["id"],
                "jurisdiction_id": "",
                "form_data": {"landmark": "Karol Bagh Metro Pillar 140", "description": "Streetlight defunct for 2 weeks."}
            },
            headers={"Authorization": f"Bearer {token_cit}"}
        )
        assert grv_case_res.status_code == 201
        assert "STR" in grv_case_res.json()["public_case_id"] or "STREET" in grv_case_res.json()["public_case_id"] or "JS-2026" in grv_case_res.json()["public_case_id"]

@pytest.mark.asyncio
async def test_ai_assist_bounded_recommendations():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        ai_res = await client.post("/api/v1/ai/assist", json={"prompt": "I need help with my pension and PF transfer to my new job."})
        assert ai_res.status_code == 200
        data = ai_res.json()
        assert data["recommended_service_id"] == "EPFO_CLAIM_TRANSFER"
        assert "EPFO" in data["service_title"] or "Provident" in data["explanation"]
