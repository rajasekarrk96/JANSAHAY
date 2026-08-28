# 25 — JANSAHAY Case Passport & Citizen Transparency UX

**Document Version**: 1.0.0  
**Status**: APPROVED & ACTIVE  
**Last Updated**: 2026-08-28  

---

## 1. Concept: The Citizen Case Passport

In legacy administrative systems, citizens receive obscure file numbers and are forced to visit municipal offices to ask *"Where is my file?"*.

The **JANSAHAY Case Passport** transforms this experience into a dignified, self-explanatory card that answers all four critical citizen questions at a single glance:
1. **What happened?**
2. **What does it mean?**
3. **Do I need to do anything?**
4. **What happens next?**

---

## 2. Component Structure

```
+-----------------------------------------------------------------------------------+
|  [PASSPORT BADGE]  JS-2026-INC-48192                                              |
|  Income Certificate • Revenue Department (Central Delhi)                          |
|  Status: Under Initial Verification                                               |
|  [Reassurance Pill: "You don't need to do anything right now."]                   |
+-----------------------------------------------------------------------------------+
|  MILESTONES TRACKER                                                               |
|  (x) Submitted  -->  (*) Verification  -->  ( ) Scrutiny  -->  ( ) Approval  -->  ( ) Ready |
+-----------------------------------------------------------------------------------+
|  PLAIN-LANGUAGE STAGE EXPLANATION                                                 |
|  * What happened: Application and documents received at verification desk.        |
|  * What it means: Officer Sunil Verma is checking proof clarity against rules.    |
|  * Action needed: No action required from you at this time.                       |
|  * What happens next: Upon verification, forwarded for Revenue Inspector review.  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Four Plain-Language Questions Mapping

| Stage | What happened? | What does it mean? | Do I need to do anything? | What happens next? |
| :--- | :--- | :--- | :--- | :--- |
| **SUBMITTED** | Application submitted. | Intake queue received application. | You don't need to do anything right now. | Front-desk officer will begin document check. |
| **VERIFICATION** | Under verification. | Officer is checking uploaded scans for clarity. | You don't need to do anything right now. | Forwarded to Department Officer upon completion. |
| **DEPARTMENT_REVIEW** | Under departmental scrutiny. | Revenue Inspector is reviewing municipal records. | You don't need to do anything right now. | Recommendations sent to Tahsildar for final grant. |
| **ACTION_REQUIRED** | Correction required. | Scrutiny noted: *Blurred scan or missing page*. | **Please upload replacement document.** | Once uploaded, verification resumes immediately. |
| **APPROVAL** | Under final review. | Application is with Executive Magistrate / Tahsildar. | You don't need to do anything right now. | Digital certificate will be signed and issued. |
| **RESOLVED** | Certificate issued. | Statutory approval granted. | **Download your official digital certificate.** | Case closed and archived. |
| **REJECTED** | Application rejected. | Statutory criteria not met. | Review rejection grounds. | Fresh application may be submitted if eligible. |

---

## 4. Action Required & Single-File Correction Loop

When an application enters `ACTION_REQUIRED`:
1. The **Case Passport** shifts to high-visibility amber styling.
2. The specific defective document is marked with the officer's exact feedback (e.g. *"Salary slip scan is blurred"*).
3. A single-file dropzone allows the citizen to upload the correction without re-entering the entire application.
4. The system increments the document version (`v2`), creates a chained audit event, and resumes the workflow automatically.
