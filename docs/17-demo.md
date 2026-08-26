# 17 — JANSAHAY Demo & Evaluation Script

## 1. Reviewer Journey 1: The Certificate Application Journey (Deep Dive)

```text
1. Citizen Login
   - Login as synthetic citizen "citizen_rahul" (Rahul Sharma, Central Delhi).
   
2. Service Discovery & Eligibility
   - Explore "Income Certificate" under Revenue Department.
   - Run Eligibility Check: Family Income ₹1,80,000 (< ₹2,50,000 threshold) -> ELIGIBLE.
   
3. Tailored Checklist & Upload
   - View personalized document requirements: Identity Proof, Income Proof, Residence Proof.
   - Upload mock files into the Quarantined Sandbox. Watch instant virus & format checks pass.
   
4. Case Submission & ID Generation
   - Submit case -> Receive instant Public Case ID: `JS-2026-INC-XXXXX`.
   - View initial status: "Application Submitted. Awaiting Initial Verification."

5. Verification Officer Action
   - Switch role to "Verification Officer" (Sunil Verma, Revenue, Delhi Central).
   - Review pending queue -> Open case -> Inspect documents.
   - Execute Action: `VERIFY` (Docs Validated).

6. Department Officer Scrutiny
   - Switch role to "Department Officer" (Priya Nair, Revenue, Delhi Central).
   - Scrutinize revenue records -> Execute Action: `FORWARD`.

7. Approving Officer Grant
   - Switch role to "Approving Officer" (Tahsildar Rajesh Kumar, Delhi Central).
   - Review case history and audit trail -> Execute Action: `APPROVE` with remarks.

8. Citizen Resolution
   - Switch back to Citizen view.
   - Status is now `RESOLVED` ("Approved! Certificate is ready").
   - View generated official digital certificate preview and audit chain.
```

---

## 2. Reviewer Journey 2: Deficiency & Correction Loop
- Verification officer marks Income Proof as `REPLACEMENT_REQUIRED` with note: "Salary slip unreadable".
- Case shifts to `ACTION_REQUIRED`.
- Citizen receives alert, uploads replacement salary certificate in Citizen Action Center.
- Case automatically returns to `VERIFICATION` queue without requiring a new application.

---

## 3. Reviewer Journey 3: EPFO & Grievance Multi-Service Parity
- Submit an EPFO Claim and a Public Grievance.
- Demonstrate that both execute seamlessly through the **same universal workflow state engine**.
