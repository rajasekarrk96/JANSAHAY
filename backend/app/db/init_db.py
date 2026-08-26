import os
import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.base import Base
from app.db.session import engine, AsyncSessionLocal
from app.db.models import (
    User, Citizen, Department, Jurisdiction, Officer,
    Service, ServiceRequirement, WorkflowDefinition,
    Case, Document, AuditEvent, NotificationOutbox, UserRole
)
from app.core.security import get_password_hash
from app.core.audit import create_audit_event, GENESIS_HASH

async def init_db_data(session: AsyncSession):
    # Ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    default_pwd_hash = get_password_hash("Password123!")

    # 1. Departments
    dept_rev = Department(code="REVENUE", name="Revenue Department", description="Land records, statutory certificates, and executive magisterial services")
    dept_epfo = Department(code="EPFO", name="Employees' Provident Fund Organisation", description="Social security, pension, and provident fund management")
    dept_grv = Department(code="PUBLIC_GRIEVANCE", name="Public Grievance Redressal Cell", description="Civic complaints and municipal service escalation")
    dept_welfare = Department(code="SOCIAL_WELFARE", name="Social Welfare Department", description="Scholarships, social security benefits, and inclusion programs")

    session.add_all([dept_rev, dept_epfo, dept_grv, dept_welfare])
    await session.flush()

    # 2. Jurisdictions
    jur_delhi_c = Jurisdiction(code="DELHI_CENTRAL", name="Central Delhi District", state="Delhi")
    jur_delhi_s = Jurisdiction(code="DELHI_SOUTH", name="South Delhi District", state="Delhi")
    jur_blr_u = Jurisdiction(code="BANGALORE_URBAN", name="Bangalore Urban District", state="Karnataka")
    jur_mum_s = Jurisdiction(code="MUMBAI_SUBURBAN", name="Mumbai Suburban District", state="Maharashtra")

    session.add_all([jur_delhi_c, jur_delhi_s, jur_blr_u, jur_mum_s])
    await session.flush()

    # 3. Services & Requirements
    # 3.1 Income Certificate
    srv_income = Service(
        code="INCOME_CERTIFICATE",
        title="Income Certificate",
        category="CERTIFICATES",
        department_id=dept_rev.id,
        sla_days=7,
        eligibility_criteria_json={
            "description": "Statutory proof of annual household income for educational scholarships, welfare schemes, and subsidies.",
            "questions": [
                {"id": "q1", "text": "Is your total annual household income less than ₹2,50,000?", "type": "boolean", "required": True},
                {"id": "q2", "text": "Do you reside in Central Delhi District?", "type": "boolean", "required": True},
                {"id": "q3", "text": "Do you possess an active identity proof (Aadhaar/Voter ID)?", "type": "boolean", "required": True}
            ]
        }
    )
    session.add(srv_income)
    await session.flush()

    req_inc_id = ServiceRequirement(
        service_id=srv_income.id,
        document_type_code="IDENTITY_PROOF",
        document_name="Proof of Identity (Aadhaar / Voter ID)",
        is_mandatory=True,
        allowed_extensions=".pdf,.jpg,.jpeg,.png",
        max_size_kb=5120
    )
    req_inc_inc = ServiceRequirement(
        service_id=srv_income.id,
        document_type_code="INCOME_PROOF",
        document_name="Proof of Income (Salary Slip / Form 16 / Self Declaration)",
        is_mandatory=True,
        allowed_extensions=".pdf,.jpg,.jpeg,.png",
        max_size_kb=5120
    )
    req_inc_res = ServiceRequirement(
        service_id=srv_income.id,
        document_type_code="RESIDENCE_PROOF",
        document_name="Proof of Residence (Electricity Bill / Rent Agreement)",
        is_mandatory=True,
        allowed_extensions=".pdf,.jpg,.jpeg,.png",
        max_size_kb=5120
    )
    session.add_all([req_inc_id, req_inc_inc, req_inc_res])

    # 3.2 Domicile Certificate
    srv_domicile = Service(
        code="DOMICILE_CERTIFICATE",
        title="Domicile / Residence Certificate",
        category="CERTIFICATES",
        department_id=dept_rev.id,
        sla_days=14,
        eligibility_criteria_json={
            "description": "Certifies permanent residency within Delhi for education admissions and state recruitment.",
            "questions": [
                {"id": "q1", "text": "Have you continuously resided in Delhi for at least 3 years?", "type": "boolean", "required": True}
            ]
        }
    )
    session.add(srv_domicile)
    await session.flush()

    req_dom_id = ServiceRequirement(
        service_id=srv_domicile.id,
        document_type_code="IDENTITY_PROOF",
        document_name="Proof of Identity (Aadhaar Card)",
        is_mandatory=True,
        allowed_extensions=".pdf,.jpg,.jpeg,.png",
        max_size_kb=5120
    )
    req_dom_res = ServiceRequirement(
        service_id=srv_domicile.id,
        document_type_code="CONTINUOUS_RESIDENCE",
        document_name="Proof of 3-Year Continuous Stay in Delhi",
        is_mandatory=True,
        allowed_extensions=".pdf,.jpg,.jpeg,.png",
        max_size_kb=5120
    )
    session.add_all([req_dom_id, req_dom_res])

    # 3.3 EPFO Claim Transfer
    srv_epfo = Service(
        code="EPFO_CLAIM_TRANSFER",
        title="EPFO Online Transfer Claim",
        category="SOCIAL_SECURITY",
        department_id=dept_epfo.id,
        sla_days=10,
        eligibility_criteria_json={
            "description": "Transfer PF balance from previous employer establishment to current active account.",
            "questions": [
                {"id": "q1", "text": "Do you have an active Universal Account Number (UAN)?", "type": "boolean", "required": True},
                {"id": "q2", "text": "Is your Aadhaar seeded with your EPFO member profile?", "type": "boolean", "required": True}
            ]
        }
    )
    session.add(srv_epfo)
    await session.flush()

    req_epf_uan = ServiceRequirement(
        service_id=srv_epfo.id,
        document_type_code="UAN_MEMBER_PROOF",
        document_name="UAN Member Passbook or Service Certificate",
        is_mandatory=True,
        allowed_extensions=".pdf,.jpg,.jpeg,.png",
        max_size_kb=5120
    )
    session.add(req_epf_uan)

    # 3.4 Public Grievance
    srv_grv = Service(
        code="STREET_LIGHT_GRIEVANCE",
        title="Public Civic & Infrastructure Grievance",
        category="GRIEVANCES",
        department_id=dept_grv.id,
        sla_days=5,
        eligibility_criteria_json={
            "description": "Lodge formal complaints for broken streetlights, road damages, drainage, or municipal sanitation.",
            "questions": [
                {"id": "q1", "text": "Is the defect located in a public municipal jurisdiction?", "type": "boolean", "required": True}
            ]
        }
    )
    session.add(srv_grv)
    await session.flush()

    req_grv_photo = ServiceRequirement(
        service_id=srv_grv.id,
        document_type_code="SITE_PHOTO",
        document_name="Site Photo / Location Landmark Proof",
        is_mandatory=False,
        allowed_extensions=".pdf,.jpg,.jpeg,.png",
        max_size_kb=5120
    )
    session.add(req_grv_photo)
    await session.flush()

    # 4. Declarative Workflows
    # 4.1 Certificate Workflow Definition
    cert_wf_json = {
        "service_code": "INCOME_CERTIFICATE",
        "version": 1,
        "initial_state": "SUBMITTED",
        "states": ["SUBMITTED", "VERIFICATION", "DEPARTMENT_REVIEW", "ACTION_REQUIRED", "APPROVAL", "RESOLVED", "REJECTED"],
        "transitions": [
            {
                "action": "VERIFY",
                "from_state": ["SUBMITTED", "VERIFICATION"],
                "to_state": "DEPARTMENT_REVIEW",
                "allowed_roles": ["VERIFICATION_OFFICER"],
                "guards": ["ALL_MANDATORY_DOCS_VERIFIED"],
                "citizen_status": "Under Departmental Scrutiny with Revenue Inspector",
                "requires_remarks": True
            },
            {
                "action": "REQUEST_CORRECTION",
                "from_state": ["SUBMITTED", "VERIFICATION", "DEPARTMENT_REVIEW"],
                "to_state": "ACTION_REQUIRED",
                "allowed_roles": ["VERIFICATION_OFFICER", "DEPARTMENT_OFFICER"],
                "citizen_status": "Action Required: Defective document detected. Please replace.",
                "requires_remarks": True
            },
            {
                "action": "RESUBMIT_DOCUMENTS",
                "from_state": "ACTION_REQUIRED",
                "to_state": "VERIFICATION",
                "allowed_roles": ["CITIZEN"],
                "guards": ["ALL_DEFICIENT_DOCS_REPLACED"],
                "citizen_status": "Replacement Document Received. Resuming Initial Verification.",
                "requires_remarks": False
            },
            {
                "action": "FORWARD",
                "from_state": "DEPARTMENT_REVIEW",
                "to_state": "APPROVAL",
                "allowed_roles": ["DEPARTMENT_OFFICER"],
                "citizen_status": "Awaiting Final Approval from Tahsildar (Executive Magistrate)",
                "requires_remarks": True
            },
            {
                "action": "APPROVE",
                "from_state": "APPROVAL",
                "to_state": "RESOLVED",
                "allowed_roles": ["APPROVING_OFFICER"],
                "citizen_status": "Approved! Official digital certificate is ready for download.",
                "requires_remarks": True
            },
            {
                "action": "REJECT",
                "from_state": ["SUBMITTED", "VERIFICATION", "DEPARTMENT_REVIEW", "APPROVAL"],
                "to_state": "REJECTED",
                "allowed_roles": ["VERIFICATION_OFFICER", "DEPARTMENT_OFFICER", "APPROVING_OFFICER"],
                "citizen_status": "Application Rejected based on statutory revenue verification rules.",
                "requires_remarks": True
            }
        ]
    }

    wf_income = WorkflowDefinition(service_id=srv_income.id, version=1, initial_state="SUBMITTED", definition_json=cert_wf_json)
    wf_domicile = WorkflowDefinition(service_id=srv_domicile.id, version=1, initial_state="SUBMITTED", definition_json=cert_wf_json)
    wf_epfo = WorkflowDefinition(service_id=srv_epfo.id, version=1, initial_state="SUBMITTED", definition_json=cert_wf_json)
    wf_grv = WorkflowDefinition(service_id=srv_grv.id, version=1, initial_state="SUBMITTED", definition_json=cert_wf_json)

    session.add_all([wf_income, wf_domicile, wf_epfo, wf_grv])
    await session.flush()

    # 5. Users & Profiles
    # 5.1 Citizens
    u_rahul = User(username="citizen_rahul", email="rahul.sharma@example.com", phone_number="+91-9876500001", password_hash=default_pwd_hash, role=UserRole.CITIZEN)
    u_anita = User(username="citizen_anita", email="anita.patel@example.com", phone_number="+91-9876500002", password_hash=default_pwd_hash, role=UserRole.CITIZEN)
    session.add_all([u_rahul, u_anita])
    await session.flush()

    c_rahul = Citizen(user_id=u_rahul.id, full_name="Rahul Sharma", synthetic_aadhaar_last4="4321", date_of_birth="1995-04-12", address_line="Plot 14/B Karol Bagh", district="Central Delhi", state="Delhi", pincode="110005")
    c_anita = Citizen(user_id=u_anita.id, full_name="Anita Patel", synthetic_aadhaar_last4="8765", date_of_birth="1992-09-28", address_line="22/A Hauz Khas", district="South Delhi", state="Delhi", pincode="110016")
    session.add_all([c_rahul, c_anita])
    await session.flush()

    # 5.2 Officers
    u_vo_rev = User(username="vo_delhi_rev", email="vo.delhi.rev@jansahay.gov.mock", phone_number="+91-9876510001", password_hash=default_pwd_hash, role=UserRole.VERIFICATION_OFFICER)
    u_do_rev = User(username="do_delhi_rev", email="do.delhi.rev@jansahay.gov.mock", phone_number="+91-9876510002", password_hash=default_pwd_hash, role=UserRole.DEPARTMENT_OFFICER)
    u_ao_rev = User(username="ao_delhi_rev", email="ao.delhi.rev@jansahay.gov.mock", phone_number="+91-9876510003", password_hash=default_pwd_hash, role=UserRole.APPROVING_OFFICER)
    u_vo_epf = User(username="vo_epfo_delhi", email="vo.epfo.delhi@jansahay.gov.mock", phone_number="+91-9876510004", password_hash=default_pwd_hash, role=UserRole.VERIFICATION_OFFICER)
    u_do_grv = User(username="do_grievance_delhi", email="do.grv.delhi@jansahay.gov.mock", phone_number="+91-9876510005", password_hash=default_pwd_hash, role=UserRole.DEPARTMENT_OFFICER)
    u_admin = User(username="admin", email="admin@jansahay.gov.mock", phone_number="+91-9876599999", password_hash=default_pwd_hash, role=UserRole.SYSTEM_ADMIN)

    session.add_all([u_vo_rev, u_do_rev, u_ao_rev, u_vo_epf, u_do_grv, u_admin])
    await session.flush()

    o_vo_rev = Officer(user_id=u_vo_rev.id, employee_code="REV-VO-401", full_name="Sunil Verma", designation="Naib Tehsildar Desk In-Charge", department_id=dept_rev.id, jurisdiction_id=jur_delhi_c.id)
    o_do_rev = Officer(user_id=u_do_rev.id, employee_code="REV-DO-204", full_name="Priya Nair", designation="Revenue Inspector", department_id=dept_rev.id, jurisdiction_id=jur_delhi_c.id)
    o_ao_rev = Officer(user_id=u_ao_rev.id, employee_code="REV-AO-101", full_name="Rajesh Kumar", designation="Tehsildar (Executive Magistrate)", department_id=dept_rev.id, jurisdiction_id=jur_delhi_c.id)
    o_vo_epf = Officer(user_id=u_vo_epf.id, employee_code="EPF-VO-882", full_name="Amit Roy", designation="Section Supervisor", department_id=dept_epfo.id, jurisdiction_id=jur_delhi_c.id)
    o_do_grv = Officer(user_id=u_do_grv.id, employee_code="GRV-DO-512", full_name="Sanjay Gupta", designation="Grievance Redressal Nodal Officer", department_id=dept_grv.id, jurisdiction_id=jur_delhi_c.id)

    session.add_all([o_vo_rev, o_do_rev, o_ao_rev, o_vo_epf, o_do_grv])
    await session.flush()

    # 6. Pre-seed Demo Case for Rahul Sharma
    case1 = Case(
        public_case_id="JS-2026-INC-48192",
        service_id=srv_income.id,
        workflow_version=1,
        citizen_id=c_rahul.id,
        department_id=dept_rev.id,
        jurisdiction_id=jur_delhi_c.id,
        current_state="VERIFICATION",
        version_id=1,
        form_data_json={
            "applicant_name": "Rahul Sharma",
            "father_name": "Satish Sharma",
            "annual_family_income": 180000,
            "occupation": "Private Sector Employee & Small Retail",
            "purpose": "College Tuition Fee Concession for Sister",
            "declaration_accepted": True
        },
        submitted_at=datetime.utcnow()
    )
    session.add(case1)
    await session.flush()

    # Create dummy storage files for case 1
    os.makedirs("./storage/documents/demo", exist_ok=True)
    mock_id_path = "./storage/documents/demo/aadhaar_mock.pdf"
    mock_inc_path = "./storage/documents/demo/salary_slip_mock.pdf"
    mock_res_path = "./storage/documents/demo/electricity_bill_mock.pdf"

    for p in [mock_id_path, mock_inc_path, mock_res_path]:
        if not os.path.exists(p):
            with open(p, "w") as f:
                f.write("%PDF-1.4 Mock Synthetic Government Document for JANSAHAY Demo.")

    doc1 = Document(case_id=case1.id, requirement_id=req_inc_id.id, file_name="Aadhaar_Card_Proof.pdf", file_path=mock_id_path, mime_type="application/pdf", file_size_bytes=1048576, status="AVAILABLE", version=1)
    doc2 = Document(case_id=case1.id, requirement_id=req_inc_inc.id, file_name="Salary_Certificate_2026.pdf", file_path=mock_inc_path, mime_type="application/pdf", file_size_bytes=819200, status="AVAILABLE", version=1)
    doc3 = Document(case_id=case1.id, requirement_id=req_inc_res.id, file_name="Electricity_Bill_Jan2026.pdf", file_path=mock_res_path, mime_type="application/pdf", file_size_bytes=655360, status="AVAILABLE", version=1)

    session.add_all([doc1, doc2, doc3])
    await session.flush()

    # Genesis Audit for Case 1
    audit1 = create_audit_event(
        case_id=case1.id,
        event_sequence=1,
        actor_id=u_rahul.id,
        actor_role=UserRole.CITIZEN,
        action="SUBMIT",
        from_state="DRAFT",
        to_state="SUBMITTED",
        remarks="Citizen submitted Income Certificate application with 3 attached documents.",
        previous_event_hash=GENESIS_HASH
    )
    session.add(audit1)
    await session.flush()

    audit2 = create_audit_event(
        case_id=case1.id,
        event_sequence=2,
        actor_id="SYSTEM",
        actor_role="SYSTEM",
        action="ASSIGN_TO_VERIFIER",
        from_state="SUBMITTED",
        to_state="VERIFICATION",
        remarks="Application auto-assigned to Central Delhi Revenue Verification Queue.",
        previous_event_hash=audit1.event_hash
    )
    session.add(audit2)

    # Initial notification
    notif1 = NotificationOutbox(
        case_id=case1.id,
        recipient_user_id=u_rahul.id,
        channel="IN_APP",
        title="Application Received: JS-2026-INC-48192",
        message="Your Income Certificate application has been assigned to Verification Officer Sunil Verma (Desk REV-VO-401).",
        status="PROCESSED"
    )
    session.add(notif1)

    await session.commit()
    print("Database successfully initialized with synthetic demo data!")

if __name__ == "__main__":
    asyncio.run(init_db_data(AsyncSessionLocal()))
