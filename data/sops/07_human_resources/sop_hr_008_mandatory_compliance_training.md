---
sop_id: "SOP-HR-008"
title: "Mandatory Compliance Training"
business_unit: "Human Resources"
version: "5.8"
effective_date: "2024-05-01"
last_reviewed: "2025-05-03"
next_review: "2025-11-19"
owner: "Jennifer Walsh, Chief Human Resources Officer"
approver: "Dr. Sarah Chen, CEO"
classification: "Internal"
regulations:
  - "HIPAA"
  - "SOC 2"
  - "GDPR"
  - "EU AI Act"
status: "Active"
---

# Standard Operating Procedure: Mandatory Compliance Training

**SOP ID:** SOP-HR-008
**Version:** 5.8
**Effective Date:** 2024-05-01
**Owner:** Jennifer Walsh, Chief Human Resources Officer
**Approver:** Dr. Sarah Chen, CEO

---

## 1. Purpose and Scope

### 1.1 Purpose
This Standard Operating Procedure (SOP) establishes the enterprise-wide framework for the design, assignment, delivery, tracking, and enforcement of mandatory compliance training at Meridian Health Technologies, Inc. The program is designed to ensure that all personnel understand their legal, regulatory, and ethical obligations, thereby mitigating organizational risk and fostering a culture of compliance. This SOP operationalizes the Board-level commitment to maintain a workforce that is demonstrably proficient in handling Protected Health Information (PHI), personal data subject to global privacy regulations, and high-risk Artificial Intelligence (AI) systems.

### 1.2 Scope
This SOP applies to all Meridian Health Technologies, Inc. entities globally, including subsidiaries in London, Berlin, Singapore, and Toronto. The scope encompasses:

- **All Personnel:** Full-time employees, part-time employees, independent contractors, temporary workers, interns, and consultants who access Meridian systems, networks, or data.
- **All Business Units:** Clinical AI Platform, HealthPay Financial Services, MedInsight Analytics, Meridian SaaS Platform, and all corporate functions (Human Resources, Finance, Legal, IT, etc.).
- **All Regulatory Domains:** Mandatory training requirements related to HIPAA, SOC 2, GDPR, the EU AI Act, NIST AI RMF, SR 11-7, and other relevant frameworks as defined in the Meridian Regulatory Obligations Register.

This SOP does **not** cover technical product-specific training or general professional development, which are managed by respective business unit leads, except where such training is explicitly mandated by a compliance control or regulation referenced herein.

---

## 2. Definitions and Acronyms

| Term / Acronym        | Definition                                                                                                                                                              |
| :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AI Literacy**       | The skills, knowledge, and understanding that allow personnel to make informed use of AI systems, as mandated by Article 4 of the EU AI Act.                            |
| **Annual Training Period** | The defined window, from June 1 to September 30, during which all annual mandatory compliance training must be completed.                                           |
| **CCO**               | Chief Compliance Officer, Thomas Anderson.                                                                                                                              |
| **CHRO**              | Chief Human Resources Officer, Jennifer Walsh.                                                                                                                          |
| **CMS**               | Compliance Management System, the platform provided by LogicGate, used for hosting, assigning, and tracking all compliance training modules.                            |
| **CPO/DPO**           | Chief Privacy Officer / Data Protection Officer, Dr. Klaus Weber.                                                                                                      |
| **EU AI Act**         | Regulation (EU) 2024/1689 laying down harmonized rules on artificial intelligence.                                                                                      |
| **HIPAA**             | Health Insurance Portability and Accountability Act of 1996.                                                                                                           |
| **HRIS**              | Human Resources Information System, Workday. This remains the system of record for employment data and drives role-based training assignments.                          |
| **LMS**               | Learning Management System, a sub-module within the CMS (LogicGate) used for content delivery, SCORM package hosting, and quiz administration.                         |
| **NIST AI RMF**       | National Institute of Standards and Technology Artificial Intelligence Risk Management Framework 1.0, adopted voluntarily on 2024-02-15.                               |
| **PHI**               | Protected Health Information, as defined by HIPAA.                                                                                                                      |
| **Role-Based Training** | Specific training curricula automatically assigned based on an individual's job function and access privileges, as mapped in the HRIS.                               |
| **SOC 2**             | Service Organization Control 2, governed by the Trust Services Criteria (TSC) established by the AICPA.                                                                 |
| **SR 11-7**           | Federal Reserve SR Letter 11-7 / OCC Bulletin 2011-12, "Model Risk Management," applicable to HealthPay Financial Services' model development.                         |
| **Triggering Event**  | An event, such as a security incident, identified process gap, or a new hire's start date, that creates a non-standard training demand.                                |

---

## 3. Roles and Responsibilities

| Role                                 | Responsibility                                                                                                                                                                                                                                  | Assigned Person / System       |
| :----------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------- |
| **Executive Sponsor (CEO)**          | Provide executive-level support; approve significant policy changes and resource allocation for the compliance training program.                                                                                                                | Dr. Sarah Chen                 |
| **Process Owner (CHRO)**             | Own the performance of the overall training program; approve curriculum architecture, SLA modifications, and escalation procedures. Ensure the HRIS feeds accurate personnel data to the CMS.                                                   | Jennifer Walsh                 |
| **Program Manager (Head of LMS)**   | Design, maintain, and publish the Annual Training Catalog; manage the CMS configuration; generate monthly compliance dashboards; escalate non-compliance to business unit directors.                                                              | Head of LMS, HR Operations     |
| **Content Approvers**                | Review and approve the technical and regulatory accuracy of all training content within their domain prior to publication.                                                                                                                      | CCO (HIPAA/SOC 2), CPO/DPO (GDPR), Chief AI Officer (EU AI Act) |
| **Business Unit Directors**          | Accountable for ensuring 100% of their personnel complete assigned training by the deadlines; receive and act on non-compliance notifications from the Program Manager; approve exception requests and remedial training plans.                | Respective VPs and Directors   |
| **Personnel (All)**                  | Complete all assigned mandatory training by the specified deadlines; attest to understanding the content; apply the knowledge to daily job functions.                                                                                           | All Meridian Personnel         |
| **Systems (HRIS & CMS)**            | **HRIS (Workday):** System of record for employment status, job codes, department, and management hierarchy. **CMS (LogicGate):** System for training assignment, delivery, assessment, and record-keeping; stores completion records and attestations. | Automated Systems              |

---

## 4. Policy Statements

Meridian Health Technologies is committed to the following mandatory compliance training policies:

- **Zero-Tolerance for Non-Compliance:** All Personnel are required to complete assigned compliance training by the specified due dates. Failure to comply will result in progressive disciplinary action, up to and including termination of employment or contract, as detailed in Section 7.4.
- **Role-Based Assignment:** No "one-size-fits-all" approach is permitted. Training is assigned based on a comprehensive matrix mapping job roles to regulatory obligations and system access levels.
- **Annual Re-Certification:** A foundational set of mandatory training must be completed by all Personnel annually. Additional role-based modules must also be completed annually.
- **Triggering Event Training:** New hires must complete foundational and role-based training prior to being provisioned with production system credentials. Personnel transferring to new roles that trigger new training requirements must complete that training within 14 calendar days of the transfer date.
- **Content Integrity and Currency:** All training modules are reviewed at least semi-annually by the Program Manager and designated Content Approvers to ensure continued regulatory accuracy and alignment with Meridian’s evolving products, controls, and threat landscape. The CPO/DPO is responsible for ensuring GDPR training content accurately reflects our data handling procedures, including the existence of privacy notices. The Chief AI Officer is responsible for ensuring EU AI Act content reflects the current risk classification and conformity assessments for our High-Risk AI Systems.

---

## 5. Detailed Procedures

### 5.1 Annual Training Catalog Management and Publishing

The Head of LMS shall maintain the "Meridian Mandatory Compliance Training Catalog" within the CMS. This catalog is the single source of truth for all available compliance training modules, their descriptions, target audiences, and regulatory mappings.

**Procedure:**
1.  **Inventory Review (Bi-Annually):** On the first Monday of March and the first Monday of September, the Head of LMS shall convene a meeting with all Content Approvers (CCO, CPO/DPO, Chief AI Officer, CISO) to review the current catalog. The agenda must cover:
    - Any new or materially changed regulatory requirements (e.g., new EU AI Act delegated acts, updated SOC 2 TSC points of focus, GDPR procedural changes).
    - Feedback from monitoring activities (Section 7.3) on module effectiveness.
    - Requests from Business Unit Directors for new or modified training.
2.  **Catalog Update:** Based on the review, the Head of LMS updates module descriptions, creates new course shells in the CMS, and retires obsolete training.
3.  **Content Development/Revision:** For each required update, the Head of LMS commissions the respective Content Approver or an authorized designee to author or revise the SCORM-compliant content package.
4.  **Quality Assurance (QA):** The revised content package is deployed to a sandbox environment in the CMS. A designated test group comprising one representative from each relevant business unit must complete the module and provide explicit sign-off on technical accuracy and usability. The QA sign-off form must be completed and archived in LogicGate.
5.  **Content Approval:** The finalized content package is presented to the Content Approvers for formal sign-off within the CMS workflow. This approval locks the content and generates an auditable digital signature.
6.  **Catalog Publication:** The Head of LMS activates the new/revised modules in the live CMS, updating the "Published Version" date in the catalog. A notification is sent to all Business Unit Directors, signaling the start of the 90-day Annual Training Period for existing personnel.

### 5.2 Role-Based Training Curriculum Assignment

Personnel are assigned training based on their "Compliance Role," a calculated attribute generated daily in Workday and pushed to LogicGate via API. The Compliance Role algorithm considers 15 distinct factors including job family, department code, AWS IAM permission sets, and Finance-System access flags.

**Curriculum Mapping Matrix (Excerpt):**

| Compliance Role Code | Role Description                                        | Foundational Modules (All)       | Domain-Specific Modules                                                                 |
| :------------------- | :------------------------------------------------------ | :------------------------------- | :-------------------------------------------------------------------------------------- |
| **ALL-001**          | All Personnel                                           | HIP-101, GDPR-AWARE, SOC2-AWARE, AI-AWARE | *None*                                                                                  |
| **CLINICIAN-010**    | Clinical personnel accessing PHI directly via MedInsight Analytics | *All from ALL-001*               | **PHI-201** (Handling PHI), **CLIN-ETHICS-501** (Patient Data Ethics)                   |
| **AI-ENG-020**       | Engineers developing/deploying Clinical AI Platform models        | *All from ALL-001*               | **EU-AI-301** (Art. 9 & 61), **NIST-AI-RMF-401** (Risk Frameworks), **AI-BIAS-502**     |
| **FINANCE-030**      | Personnel processing HealthPay Financial Services transactions    | *All from ALL-001*               | **SR-11-7-601** (Model Risk for Operators), **PCI-DSS-701**                             |
| **DATA-ENG-040**     | Data Engineers managing MedInsight or SaaS Platform data pipelines | *All from ALL-001*               | **HIP-301**, **EU-DATA-302** (Data Minimization & Purpose Limitation), **SOC2-CM-801** (Change Management) |
| **EXEC-050**         | VP and above                                             | *All from ALL-001*               | **EXEC-COMPLIANCE-901** (Oversight & Liability)                                         |

**Assignment Procedure:**
1.  **Nightly Sync:** Each night, Workday calculates the `ComplianceRoleCode` for all active personnel. The HRIS integration agent pushes a flat file containing `PersonnelID`, `ComplianceRoleCode`, `ManagerID`, and `DepartmentCode` to the CMS via a secure SFTP drop.
2.  **Rule Engine Trigger:** Upon file ingestion, the CMS (LogicGate) rule engine executes the `TrainingRuleSet_v5.8`. For each `PersonnelID`, the engine evaluates the `ComplianceRoleCode` against the published Curriculum Mapping Matrix. If the required module set for the current year does not match the assigned module set, the CMS automatically creates new training assignments or revokes obsolete ones.
3.  **Exception Queue:** If a `ComplianceRoleCode` cannot be mapped or is missing, the record is moved to a "Role Error" queue. The Head of LMS reviews this queue daily and works with the HRIS team to resolve data source issues.

### 5.3 New Hire and Triggering Event Procedure
1.  **New Hires:** On the date of hire, as recorded in Workday, the HRIS triggers a "New Hire" event to the CMS. The foundational training (`ALL-001`) is assigned immediately. Access to any system containing PHI, sensitive financial data, or administrative AI interfaces (provisioned via SOP-SEC-002) remains gated. The IAM provisioning system queries the CMS API; unless a "Compliant" status for `ALL-001` and all assigned role-based modules is returned, credentials are not created.
2.  **Role Transfers:** When a personnel's profile changes in Workday (e.g., promotion to a Director role, transfer to the AI Platform team), the nightly sync (Step 5.2.1) triggers the rule engine. If the new role requires training beyond what was previously completed, the new assignments are created with a due date of 14 calendar days from the event date. Access tied to the *new* role is automatically gated until training is complete, but existing access for the *former* role is not altered during the transition period.

### 5.4 Training Completion and Attestation
1.  **Module Launch:** Personnel access modules directly via an SSO portal in Okta that directs them to LogicGate.
2.  **SCORM Interaction:** The CMS tracks progress via the SCORM 2004 (3rd Edition) standard. Module completion is defined as viewing 100% of the slides and passing the embedded knowledge check quiz with a score of ≥ 80%. Personnel have unlimited attempts to pass the quiz.
3.  **Attestation:** Upon successful quiz completion, the CMS presents a mandatory, standalone attestation statement:
    > *"I, [Name], acknowledge that I have completed the [Module Name] training. I comprehend my obligations as presented in this training and commit to applying these policies and procedures in my daily work at Meridian Health Technologies. I understand that my failure to uphold these standards may result in disciplinary action, up to and including termination."*
4.  **Audit Record:** The attestation is digitally signed, capturing the user's unique session ID, a timestamp, and the content version. This record is immutable and immutably stored in the CMS audit trail log. A "Completed" status and digital badge are posted to the personnel's CMS profile immediately.

### 6.5 Remedial Training Procedure
Remedial training is enforced when a personnel is found to be the root cause or a contributing factor in a validated incident, as determined by a post-incident review (see SOP-SEC-004, Security Incident Response).
1.  **Incident Post-Mortem:** The incident review board determines that a compliance-policy violation occurred due to an apparent gap in the individual's understanding.
2.  **Remedial Assignment Request:** The CCO or CISO formally submits a "Remedial Training Request" in LogicGate, linking to the open incident ticket in Jira Service Management. The request details the specific policy violated and the module(s) to be retaken, plus any new, supplemental micro-training.
3.  **Assignment:** The CCO approves the request. The Head of LMS assigns the module(s) through the CMS, setting a deadline of 7 calendar days from assignment.
4.  **Completion and Post-Training Interview:** The personnel must complete the module(s). Upon completion, their direct manager is mandated to conduct a 30-minute, documented interview using the Meridian "Compliance Interview Guide" to verify understanding of the remediation. The signed guide is uploaded to the CMS record.
5.  **Failure to Remediate:** Failure to complete remedial training by the deadline immediately escalates per Section 8.

### 6.2 EU AI Act Specific Controls
Per the requirements for providers of High-Risk AI Systems, the following specific training controls are enforced:
- **AI Literacy (Art. 4):** Module **EU-AI-AWARE** is mandatory for all Personnel, per curriculum `ALL-001`. The training content, designed and approved by the Chief AI Officer, covers: (1) the technical principles of how our Clinical AI Platform models work (layperson's terms); (2) the concepts of input data bias and output interpretation; and (3) the specific use cases in a clinical workflow context.
- **Human Oversight (Art. 14):** Personnel assigned to `CLINICIAN-010` and `AI-OPS-022` roles must complete module **EU-AI-HUMAN-302**. This module provides scenario-based training on interpreting the user-in-the-loop interface outputs, correctly identifying anomalies, and understanding the authority to override algorithmic decisions. Competency is measured via a simulated clinical decision exercise with a mandatory 100% pass mark on the override safety procedure.
- **Automatic Logging (Art. 12):** The CMS, as a supporting tool, automatically logs all training assignments and completions for personnel directly involved in the development and operation of the High-Risk AI System. These logs are retained for a period of ten years, in accordance with the monitoring plan specified in our EU AI Act Technical Documentation (SOP-AI-DOC-001).

### 6.3 SOC 2 Specific Controls
In alignment with our SOC 2 Type II examination scope, this SOP implements specific controls mapped to the 2023 Trust Services Criteria:
- **Control CC2.1 — Communication of Commitments:** The zero-tolerance policy, role-based matrix, and annual cycle detailed in Section 4 are the primary mechanisms for communicating Meridian’s commitment to security, availability, and confidentiality to all internal personnel. The attestation in Step 5.4.3 serves as an auditable check on the receipt and acknowledgment of these commitments.
- **Control CC2.2 — Communication of Roles and Responsibilities:** Section 3 of this SOP delineates responsibilities. The automated nightly feed from Workday to LogicGate (Step 5.2.1) ensures that a current, authoritative system of record dictates personnel roles, directly driving the specific communication of risk-mitigation responsibilities.
- **Control PI1.4 — Processing of Personal Information:** The role-based training defined in this SOP, specifically for `DATA-ENG-040` and `PRIVACY-045` roles, provides explicit instruction on how personal information must be processed in accordance with our privacy commitments to our employees and clients. Compliance with this training is monitored via a monthly KPI dashboard (KP-MCT-01-REV) reviewed by the CCO.
- **Control CC4.2 — Monitoring Activities:** The KPI structure and reporting cadence defined in Section 7.3 constitutes our primary management-level monitoring activity for the training compliance control. Management of the "Exception Queue" in Step 5.2.3 is the associated operational-level monitoring activity.

---

## 6. Controls and Safeguards

### 6.1 Preventative Controls
- **Access Gating via API:** A zero-trust middleware agent (Okta Access Gateway) intercepts all requests for production system credentials. The agent makes a real-time API call to LogicGate to verify that the requesting user's `PersonnelID` has a status of `Compliant` for all mandatory modules associated with the privileges being requested. This safeguard ensures no untrained user can access sensitive systems, databases (AWS RDS), or administrative consoles.
- **Data Segregation:** Training records, which may contain performance data on quizzes, are logically separated from core HR records within LogicGate by a strict access control policy. Only members of the LMS Administration Group can view granular quiz results.

### 6.2 Detective Controls
- **Monthly Configuration Audit:** On the first business day of each month, the Head of LMS shall execute a pre-built audit report (`TR-AUDIT-001`) within LogicGate. This report compares the "currently assigned" curriculum for a randomized, 10% sample of active Personnel against the approved "expected" curriculum from the master catalog for their specific `ComplianceRoleCode`. All mismatches are logged and resolved as Priority 2 tickets.
- **Ghost User Check:** A quarterly detective check executed by the CISO’s team to identify completed training records in LogicGate associated with a `PersonnelID` that has been subsequently disabled in Workday, indicating a potential access de-provisioning failure. Any discrepancy triggers a P1 ticket per the Incident Response SOP.

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs)
| KPI ID                | Metric Description                                                     | Target                               | Calculation                                                                                  |
| :-------------------- | :--------------------------------------------------------------------- | :----------------------------------- | :------------------------------------------------------------------------------------------- |
| **KP-TRN-001**        | **Overall Completion Rate (Annual)**                                   | **100%** completion by Sep 30       | `(Total Personnel Assigned Training — Total Personnel *Not* Compliant) / Total Personnel`      |
| **KP-TRN-002**        | **New Hire On-Time Completion**                                        | **≥ 98%** completion within 30 days  | `(New Hires in Month completing all modules within 30 days) / (Total Active New Hires)`        |
| **KP-TRN-003**        | **Remedial Training Efficacy**                                         | **≥ 95%** no repeat incident in 6mo | `(Remedial Assignments from Incidents — Repeat Incidents from Same Person in 6mo) / Remedial Assignments` |
| **KP-TRN-004-EU-AI**  | **AI Operations Staff Competency (Art. 14)**                           | **100%** pass first attempt          | `(Total AI-OPS Personnel passing *all* EU AI modules on first try) / (Total AI-OPS Personnel)`  |

### 7.2 Compliance Dashboards
The Head of LMS shall publish a real-time, read-only "Compliance Training Dashboard" (built in Tableau, sourcing data from the LogicGate CMS) to all VP-level stakeholders. This dashboard will display:
- Overall company compliance percentage against target (KP-TRN-001).
- Compliance rate, broken down by Business Unit and by Department.
- A red-highlighted "Non-Compliance List" showing all personnel past due on any module.
- Completion rate trend line over the fiscal year, with annotations for key triggering events (e.g., release of revised EU AI Act module).

### 7.3 Reporting Cadence
- **Monthly Reporting:** On the 5th business day of each month, the Head of LMS generates a "Monthly Training Compliance Report." This report includes the dashboard snapshot, a summary of all exception approvals, and a detailed, granular KPI analysis. The report is reviewed in the monthly Compliance Steering Committee meeting chaired by the CCO.
- **Audit Reporting:** For the SOC 2 Type II examination, the control matrix and corresponding evidence (KPI dashboards, exception logs, system configuration reports) are provided to external auditors as part of the evidence request process managed by the CISO and CCO.

### 7.4 Escalation for Non-Compliance
A graduated escalation process is strictly enforced. All actions, including formal warnings, will be documented in Workday by the CHRO’s delegate.
1.  **5 Business Days Past Due:** The CMS sends an automated final reminder to the Personnel, with a visible cc: to their direct manager.
2.  **10 Business Days Past Due:** The CMS escalates the non-compliance record to the Business Unit Director, who is required to submit a written plan for achieving compliance within 48 hours.
3.  **15 Business Days Past Due & No Remediation Plan:** The CCO, in coordination with the CHRO, will issue a formal written warning to the Personnel, and all access to Meridian systems will be temporarily suspended until training is complete. The suspension period is unpaid for hourly contractors.
4.  **30 Business Days Past Due:** The Personnel’s non-compliance is considered a material breach of employment terms and a voluntary resignation, subject to termination proceedings managed by HR.

---

## 8. Exception Handling and Escalation

### 8.1 Exception Request Policy
Meridian recognizes that in rare, legitimate circumstances, a Personnel may be unable to complete training by the deadline (e.g., approved extended medical leave, active military deployment). Failure to complete training is not an exception; only the *deadline for completion* can be excepted. No exceptions are granted for the content itself.

### 8.2 Exception Request Procedure
1.  **Request Submission:** The Personnel’s direct manager must submit a formal "Compliance Training Exception Request" form in LogicGate **no less than 14 calendar days prior to the training deadline**. The form must clearly state:
    - The specific business justification for the extended deadline.
    - The proposed new completion date (not to exceed the original due date + 30 days).
    - A risk acknowledgment affirming the manager accepts the operational risk of the Personnel performing duties without up-to-date training for the exception period.
2.  **Risk Assessment:** The CCO reviews the request and appends a formal "Risk Acceptance Memo" evaluating the regulatory and operational risk impact of the exception based on the Personnel's role. For any roles mapping to `AI-ENG-020` or `CLINICIAN-010`, the Chief AI Officer must co-approve.
3.  **Approval/Denial:** The CCO or CHRO approves or denies the request. An approval is logged in the CMS and attached to the Personnel’s record, and the due date is temporarily adjusted. All approvals are reported as a material risk metric to the Board’s Risk and Compliance Committee on a quarterly basis. A denial follows the standard non-compliance escalation in Section 7.4.

---

## 9. Training Requirements

All Personnel responsible for the administration of this SOP (i.e., members of the HR Operations, LMS Administration, and Compliance teams) must undergo "Train-the-Trainer" certification on this specific procedure, SOP-HR-008. This certification is conducted annually by the CHRO, using the current version of this document itself as the primary training material. A competency quiz requiring a score of 100% must be passed. Failure to maintain this internal certification disqualifies the individual from operating the CMS or approving exception requests, constituting a triggering event for the purposes of their own compliance.

---

## 10. Related Policies and References

| Reference ID       | Document Name                                               | Relationship to SOP-HR-008                                                                 |
| :----------------- | :---------------------------------------------------------- | :--------------------------------------------------------------------------------------- |
| **SOP-HR-001**     | Code of Conduct and Ethics Training                         | Foundational module delivered through this SOP's CMS framework.                          |
| **SOP-SEC-002**    | User Access Management                                      | Details the technical provisioning gating controlled by training status in Section 5.3.   |
| **SOP-SEC-004**    | Security Incident Response                                  | Procedure for post-incident review that may trigger remedial training as in Section 5.5. |
| **SOP-AI-DOC-001** | EU AI Act Technical Documentation                           | Contains the monitoring log retention policies referenced in Section 6.2.               |
| **SOP-DP-005**     | Data Subject Rights and Privacy Request Handling            | GDPR-specific operational procedure informed by the training herein.                     |
| **POL-RISK-001**   | Enterprise Risk Management Policy                           | Defines the risk acceptance hierarchy used for exception handling in Section 8.2.         |

---

## 11. Revision History

| Version | Revision Date | Author / Owner           | Summary of Changes                                                                                                    |
| :------ | :------------ | :----------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| 3.2     | 2022-01-15    | J. Miller, Dir. HR Ops   | Initial integration of SOC 2 controls into curriculum; added gated access procedure for new hires.                   |
| 4.0     | 2022-11-01    | A. Thompson, Legal       | Major rewrite to incorporate GDPR principles post-acquisition. Added Role "ALL-001" for all-staff foundational module. |
| 4.5     | 2023-06-10    | J. Walsh, CHRO           | Transitioned LMS from Saba to LogicGate; updated all procedures to new CMS tooling; added quarterly audit report.     |
| 5.1     | 2024-01-18    | K. Ito, DPO              | Added EU AI Act modules and controls; created specific roles for AI operations staff; updated escalation flow.       |
| 5.7     | 2024-03-22    | J. Walsh, CHRO           | Refined exception handling procedure; introduced formal workday integration for escalation warnings.                 |
| **5.8** | **2024-05-01**| **J. Walsh, CHRO**       | **Annual review. Updated KPI dashboards and SOC 2 mapping for 2023 TSC alignment. Minor curriculum mapping updates.** |