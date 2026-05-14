---
sop_id: "SOP-HR-007"
title: "Employee Data Privacy"
business_unit: "Human Resources"
version: "3.8"
effective_date: "2025-02-26"
last_reviewed: "2026-06-05"
next_review: "2026-12-24"
owner: "Jennifer Walsh, Chief Human Resources Officer"
approver: "Dr. Sarah Chen, CEO"
classification: "Internal"
regulations:
  - "GDPR"
  - "HIPAA"
status: "Active"
---

# Standard Operating Procedure: Employee Data Privacy
## SOP-HR-007 | Version 3.8

---

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the framework for the collection, processing, storage, transfer, and disposal of Employee Personal Data at Meridian Health Technologies, Inc. and its wholly-owned subsidiaries. Given Meridian's dual role as a healthcare technology provider processing protected health information (PHI) and as an employer managing sensitive workforce data across multiple jurisdictions, adherence to the highest standards of data privacy is not merely a regulatory obligation but a foundational element of our corporate integrity.

The purpose of this document is to operationalize the principles of data minimization, purpose limitation, storage limitation, integrity, confidentiality, and accountability as they pertain to our workforce. It ensures that Meridian respects the privacy rights of its employees, contractors, and applicants while enabling the business to meet its operational, legal, and financial objectives.

### 1.2 Scope

This SOP applies to the following categories of individuals ("Data Subjects"):

- **Current Employees:** All full-time, part-time, and fixed-term employees of Meridian Health Technologies, Inc. across all global offices (Boston HQ, London, Berlin, Singapore, Toronto).
- **Former Employees:** Individuals whose employment has been terminated, until the expiration of applicable statutory retention periods.
- **Applicants and Candidates:** Individuals who have applied for a position at Meridian, submitted through the Workday Recruiting module.
- **Contractors and Contingent Workers:** Independent contractors, consultants, temporary staff, and interns whose personal data is processed by Meridian HR systems.
- **Dependents and Beneficiaries:** To the extent that Meridian processes personal data of employee dependents for benefits administration (e.g., health insurance enrollment through Meridian's HealthPay benefits portal).

This SOP covers all Employee Personal Data regardless of format—digital data residing in Workday, ADP Workforce Now, the Meridian Okta identity platform, Snowflake HR analytics, and physical records stored in locked HR file rooms.

### 1.3 Out-of-Scope

This SOP does not govern the processing of patient data, provider data, or consumer financial data. Those activities are governed by the Clinical AI Platform data governance framework, HealthPay SOC 2 controls, and the MedInsight Data Processing Agreement. Refer to SOP-COMP-001 (Clinical AI Data Governance) and SOP-FIN-014 (HealthPay Consumer Privacy) for those domains. However, if an employee is also a patient of Meridian's occupational health services, the patient-employee data segregation wall described in Section 6.9 applies.

---

## 2. Definitions and Acronyms

| Term / Acronym | Definition |
| :--- | :--- |
| **Employee Personal Data** | Any information relating to an identified or identifiable Employee Data Subject. This includes identifiers such as name, employee ID, government ID numbers, location data, online identifiers (Okta user ID, IP address), and factors specific to the individual's physical, physiological, genetic, mental, economic, cultural, or social identity. |
| **Sensitive Employee Data** | Special categories of personal data requiring enhanced protections, including: racial or ethnic origin data (collected for EEO/Affirmative Action), political opinions (if disclosed for accommodation requests), religious beliefs (for accommodation requests), trade union membership (if applicable), genetic data, biometric data (fingerprints used in Boston HQ biometric access systems), health information (occupational health records, disability status, sick leave records), and sexual orientation data (collected via voluntary DEI surveys). |
| **Processing** | Any operation performed on personal data, whether automated or manual, including collection, recording, organization, structuring, storage in Workday, transmission via Slack or Meridian email, consultation, use, disclosure by transmission, alignment with other data, restriction, erasure, or destruction. |
| **Data Subject Request (DSR)** | A formal request from an employee exercising rights under GDPR (Chapter III, Articles 12-23) or equivalent state laws, including the right of access, rectification, erasure, restriction of processing, data portability, and objection. |
| **Data Protection Impact Assessment (DPIA)** | A mandatory assessment required under GDPR Article 35 for processing operations that are likely to result in high risk to the rights and freedoms of natural persons, such as the use of new technologies for employee monitoring. |
| **Privacy by Design and Default** | The principle enshrined in GDPR Article 25, requiring that data protection measures are integrated into the processing activity design and that only data necessary for each specific purpose is processed by default. |
| **Joint Controllership** | Where two or more controllers (e.g., Meridian and ADP) jointly determine the purposes and means of processing. The arrangement is governed by a transparent agreement per GDPR Article 26. |
| **HRIS** | Human Resources Information System (Workday). |
| **PII** | Personally Identifiable Information. |
| **PIIA** | Proprietary Information and Inventions Agreement. |
| **LCA** | Public Access Files for Labor Condition Applications. |

---

## 3. Roles and Responsibilities

The following RACI matrix delineates responsibility for employee data privacy operations at Meridian. Specific responsibilities are detailed below the matrix.

| Activity / Process | CHRO (Owner) | Chief Privacy Officer | HR Operations Director | IT Security (CISO) | Legal (GC) | Payroll Director | Employee |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Policy Maintenance & Approval** | **A** | R | C | I | C | I | I |
| **Data Inventory & Mapping** | I | **A** | R | C | C | C | I |
| **Privacy Notice Delivery** | I | I | **A / R** | I | C | I | I |
| **Consent Management (Art. 7)** | I | **A** | R | C | C | I | I |
| **Data Subject Request Processing** | I | **A** | R | C | C | I | R |
| **Access Control Provisioning** | I | I | C | **A / R** | I | C | I |
| **Breach Detection & Notification** | I | R | C | **A** | R | I | I |
| **Retention & Deletion Execution** | I | I | **A / R** | R | C | I | I |
| **Third-Party Due Diligence** | I | **A** | R | C | R | I | I |
| **Annual Privacy Training Development** | I | **A** | R | C | R | I | I |

**Key:** R = Responsible (executes), A = Accountable (approver, ultimately answerable), C = Consulted (prior to action), I = Informed (after action).

### 3.1 Chief Human Resources Officer (CHRO), Jennifer Walsh
- Serves as the executive owner of this SOP.
- Approves all HR data privacy exceptions and escalations.
- Approves new processing activities involving Sensitive Employee Data.
- Reviews and signs off on HR Data Protection Impact Assessments.

### 3.2 Chief Privacy Officer (CPO), Marcus Okonkwo
- Provides authoritative interpretation of GDPR, HIPAA, and applicable state privacy laws.
- Leads the investigation and regulatory notification for all actual or suspected personal data breaches.
- Maintains the Meridian Record of Processing Activities (ROPA) per GDPR Article 30, including all HR processing activities.
- Coordinates the Data Subject Request portal and ensures timely responses within statutory deadlines.

### 3.3 Director of HR Operations, Priya Singh
- Operationalizes this policy within the Workday HRIS.
- Manages the lifecycle of employee data, including onboarding collection, in-service changes, and off-boarding archival.
- Executes the annual data minimization clean-up sprints.
- Serves as the primary point-of-contact for third-party HR vendors (ADP, HireRight, Workday) regarding data processing agreements.

### 3.4 Chief Information Security Officer (CISO), David Chen
- Implements and maintains technical and organizational measures (TOMs) to ensure appropriate security of employee data, including encryption, pseudonymization, and access logs.
- Leads technical forensics during a data incident investigation.
- Manages the SIEM (Splunk) rules that alert on anomalous access to HR data lakes (Snowflake).

### 3.5 General Counsel, Priya Kapoor
- Advises on legal bases for processing in high-risk jurisdictions.
- Reviews and approves cross-border data transfer mechanisms (EU SCCs, UK Addendum).
- Manages litigation holds that override standard retention policies.

### 3.6 Employees (All Data Subjects)
- Review and acknowledge this SOP and the Employee Privacy Notice during onboarding and annually thereafter.
- Submit Data Subject Requests through the designated Jira Service Management portal ("Privacy Rights" project).
- Immediately report any suspected privacy incident or unauthorized access via the `#sec-incident` Slack channel or by emailing `privacy@meridianhealth.com`.

---

## 4. Policy Statements

Meridian Health Technologies adheres to the following foundational policy commitments, which are derived directly from the GDPR Article 5 principles and extended to all global operations:

- **Lawfulness, Fairness, and Transparency (Art. 5.1.a):** Employee personal data shall be processed lawfully, fairly, and in a transparent manner. Meridian provides a detailed Privacy Notice accessible via the Workday Help Portal, updated on a rolling 12-month cycle or within 30 days of a material processing change. No hidden or covert monitoring will occur.

- **Purpose Limitation (Art. 5.1.b):** Data collected for specific, explicit, and legitimate purposes (e.g., payroll) shall not be further processed in a manner incompatible with those purposes. Employee engagement surveys conducted on Culture Amp will not be co-mingled with performance management data in Workday without explicit, documented justification approved by the CHRO and CPO.

- **Data Minimization (Art. 5.1.c):** Processing of employee data shall be adequate, relevant, and limited to what is necessary. This principle is enforced at the system-configuration level in Workday. Recruiters are blocked from viewing candidate health data or Social Security Numbers. Manager dashboards redact the underlying reasons for leave-of-absence, displaying only "LOA – Status Code."

- **Accuracy (Art. 5.1.d):** Meridian will take every reasonable step to ensure inaccurate personal data is rectified or deleted without delay. Employees are encouraged and technically empowered to update their personal contact details, banking information, and emergency contacts via the "Employee Self-Service" portal in Workday. Annual "Data Accuracy" campaigns are run every January.

- **Storage Limitation (Art. 5.1.e):** Data shall be kept in a form which permits identification of data subjects for no longer than is necessary. Strict retention schedules are enforced (see Table 4.1) via automated archival and purging scripts.

- **Integrity and Confidentiality (Art. 5.1.f):** Data shall be processed in a manner that ensures appropriate security, including protection against unauthorized or unlawful processing and against accidental loss, destruction or damage. Encryption at rest (AES-256) and in transit (TLS 1.3) is mandatory.

- **Accountability (Art. 5.2):** The CHRO and CPO are jointly responsible for demonstrating compliance with these principles. This is achieved through meticulous Record of Processing Activities (ROPA) maintenance, regular internal audits conducted by the Internal Audit team (see SOP-IA-011), and adherence to approved Codes of Conduct.

### 4.1 Legal Basis for Processing

Meridian does not rely primarily on consent for the processing of core employee data. Consent is used only in narrow, non-employment-conditional circumstances (e.g., inclusion on a marketing photo newsletter). The primary legal bases for processing are:

1.  **Contractual Necessity (Art. 6.1.b):** Processing for salary payment, benefits enrollment, performance management, and provision of IT access credentials. If an employee refuses to provide essential payroll data, Meridian cannot fulfill the employment contract.
2.  **Legal Obligation (Art. 6.1.c):** Reporting payroll taxes to the IRS and HMRC, maintaining records for EEO compliance, retaining records for OSHA mandates, and processing garnishment orders.
3.  **Legitimate Interests (Art. 6.1.f):** Processing for enterprise security (access badging, network monitoring), workforce planning analytics (aggregated, non-individualized), and internal directory services. A Legitimate Interests Assessment (LIA) is documented and approved by the CPO for each such processing activity.
4.  **Explicit Consent (Art. 9.2.a):** For processing Sensitive Data (e.g., health information for a wellness portal integration), explicit consent, separate from the employment contract, is obtained using a granular consent form stored in the employee's Workday Worker Profile under "Documents." Consent may be withdrawn via the DSR mechanism.

---

## 5. Detailed Procedures

This section defines the end-to-end operational workflows for managing employee data privacy at Meridian.

### 5.1 Employee Data Collection

#### 5.1.1 Recruitment and Onboarding

**Procedure:**
1.  **Offer Letter Generation:** The Talent Acquisition (TA) Partner generates the offer letter package via Workday Recruiting. This package includes the conditional offer, links to the global Employee Privacy Notice (SOP-HR-007-PN-3.8), and confidentiality agreements (PIIA).
2.  **Background Check Authorization:** Should a role require a background check per Meridian's screening matrix, the candidate receives a standalone disclosure and authorization form, electronically via HireRight. The TA Partner is responsible for ensuring the disclosure is presented separately from the main offer letter. No background check is initiated without a valid electronic signature recorded in HireRight.
3.  **Onboarding Data Entry (Pre-Day-1):** Upon acceptance, the Onboarding Coordinator triggers the "New Hire Data Collection" business process in Workday. The new hire receives a "Onboarding Portal" task to complete the following sections *before* their first day:
    - Personal Identity Data: Full legal name, date of birth, national identifier (SSN/SIN/NIN).
    - Contact Data: Emergency contacts (minimum 2), personal email, personal mobile number.
    - Banking Data: Direct deposit details (routing/account number). This data is masked in Workday UI and API calls.
4.  **Day-1 Identity Verification (I-9/E-Verify):** On their first day, the US-based employee presents original identity and employment authorization documents to the Onboarding Coordinator. The Onboarding Coordinator reviews the physical document in the presence of the employee, enters the data into the E-Verify system within 3 business days, and stores a digital copy in the employee's secure, isolated "Government Compliance" folder in the Workday Document Cloud. Physical copies are returned to the employee immediately after digital archiving. Non-US employees are processed through the right-to-work checks mandated by specific jurisdictions (e.g., UK Home Office online checking service).
5.  **Biometric Enrollment:** Employees at the Boston HQ are invited to enroll their fingerprint template in the Brivo access control system. A separate biometric consent form is administered, explicitly stating that the fingerprint is used solely for physical access and not for time-tracking or any secondary purpose. The template is stored as a one-way hashed token in Brivo's cloud; the raw fingerprint image is discarded.

#### 5.1.2 Collection of Sensitive Employee Data

**Procedure for Voluntary DEI Surveys (Art. 9.2.a GDPR):**
1.  The Office of Inclusion conducts an annual "Meridian Culture Monitor" survey using the Culture Amp platform.
2.  Demographic questions concerning race/ethnicity, veteran status, disability, sexual orientation, and gender identity are strictly optional.
3.  Each question includes a "Prefer not to say" option, which is the default.
4.  The invitation email explicitly states: *"Your participation is voluntary. Data collected is aggregated and anonymized for workforce reporting and is never linked to your individual HR record, performance evaluations, or compensation. In accordance with SOP-HR-007, your explicit consent is required."*
5.  Before the survey launches, a granular consent form is presented. The employee must actively toggle "Yes" for each special category of data they agree to provide.
6.  The Culture Amp integration pipeline to our Snowflake analytics instance applies a strict hashing and aggregation script that prevents re-identification of any individual "raw" responses.

### 5.2 Processing Purposes and Restrictions

Meridian strictly segregates processing purposes to prevent function creep. Data collected for one purpose is not processed for another incompatible purpose without explicit notice, consent (where required), and CPO approval.

#### 5.2.1 Payroll Processing (Joint Controllership with ADP)

The Payroll Director (reporting to the CFO) specifies the purpose for payroll data. The HR Operations Director transmits a secure, encrypted file (SFTP, port 2222, AES-256-GCM encryption) to ADP containing only the Minimum Necessary Data elements (Name, Employee ID, Salary, Tax Withholding Elections, Bank Routing). Performance ratings, medical leave details, or disciplinary records are explicitly excluded from the payroll transmission schema. This is enforced by a Workday Integration Security rule: "Integration_ISU_Payroll_Export."

#### 5.2.2 Workforce Planning Analytics (Legitimate Interest)

The People Analytics team uses de-identified and aggregated HR data to model attrition risk and workforce needs. Queries run on the Snowflake `HR_ANALYTICS` (read-only) schema, which is automatically refreshed daily from Workday. A strict SQL-based masking view has been implemented (`ANALYTICS.VW_EMPLOYEE_MASKED`) that replaces direct identifiers (Name, Email) with pseudonymous tokens. The data scientist cannot access raw tables without explicit approval via a SailPoint temporary elevated access request, which is monitored by the CISO's team.

### 5.3 Data Subject Requests (DSRs)

Meridian empowers employees to exercise their rights under GDPR Chapter III, Articles 15-22. The DSR process is managed centrally by the Privacy Operations team.

#### 5.3.1 Receipt and Validation

1.  **Receipt:** Employees submit requests via the Jira Service Management portal ("Privacy Rights" project), selecting the specific right (e.g., "Right of Access," "Right to Erasure"). Automated acknowledgment is sent immediately.
2.  **Validation:** The Privacy Analyst (first-line responder) validates the requestor's identity within 24 hours. Given the logged-in SSO context, this is typically satisfied by the Okta session token. If a request is submitted from an external channel (e.g., personal Gmail), a multi-factor challenge is initiated: the analyst sends a verification code to the employee's registered personal mobile phone or personal email on file in Workday.
3.  **Logging:** The validated request is logged in the "DSR Register" (a locked, restricted-access SharePoint list) with a unique DSR-ID, timestamp, and status ("Open").

#### 5.3.2 Processing a "Right of Access" Request (Art. 15)

1.  The Privacy Analyst maps the DSR-ID against our processing activities.
2.  An automated, orchestrated data search is triggered across primary HR silos:
    - **Workday:** The `Worker Data Export` integration is invoked via the DSR-ID.
    - **ADP:** A secure e-mail containing the request ID is sent to our designated ADP Privacy Officer (`DPO@adp.com`) via TLS-encrypted mail.
    - **Brivo** (for BOS HQ employees): The privacy officer manually downloads the employee's access-event log.
    - **Slack Enterprise Grid:** A DSR export tool captures public channel messages and metadata.
3.  Within 28 days, the Privacy Analyst compiles the data into a structured, portable, machine-readable JSON and PDF report. The report is delivered through the Jira portal in a password-protected `.zip` archive, with the password delivered via SMS.

#### 5.3.3 Processing a "Right to Erasure" Request (Art. 17)

1.  **Eligibility Check:** The Legal & Privacy team reviews the request based on the established legal bases. For example, a current employee's basic payroll data cannot be erased due to legal obligation. The record is retained, but the primary identifier in the analytics sandbox (Snowflake) is pseudonymized.
2.  **Segmented Deletion:** A script is executed across the HR tech stack:
    - Culture Amp Survey raw responses: Hard delete.
    - Workday: If permissible, non-statutory fields are overwritten with "[REDACTED]". Where statutory retention overrides the right to erasure, the record is placed under an "Archival Lock" with a future deletion date.
    - HireRight: A deletion command is sent via API to the HireRight background screening platform.
3.  **Confirmation:** A "Certificate of Erasure/Archival" is generated and delivered to the requestor within 40 days.

### 5.4 Data Retention and Disposal

Meridian implements a lifecycle approach to all employee records, governed by the Global Retention Schedule (Appendix G of this SOP).

#### 5.4.1 Retention Schedule (Excerpt)

| Record Category | System of Record | Retention Period | Trigger Event | Disposal Method |
| :--- | :--- | :--- | :--- | :--- |
| **Core HR Master File** (Offer letters, PIIA, Performance Reviews) | Workday | Termination + 7 Years | Termination Date | Automated archival to AWS Glacier; Cryptographic shredding at 7yr+1day via Workday purge job. |
| **Payroll Records** (Payslips, Tax forms) | ADP Workforce Now | Termination + 4 Years | End of Tax Year | Secure file deletion via ADP Admin Console; Certificate of Destruction retained. |
| **Recruitment (Unsuccessful Candidates)** | Workday Recruiting | 2 Years | Application Rejection Date | Automated anonymization script (`ANON_CANDIDATE`) runs every Sunday at 03:00 UTC. |
| **I-9 Forms (US)** | Workday Gov Cloud | Termination + 3 Years | Termination Date | Manual purge by HR Ops on the first Monday after the 3-year anniversary. |
| **Background Check Reports** | HireRight | 2 Years | Hire Date | API call to HireRight deletion endpoint; confirmation logged. |

#### 5.4.2 Disposal Procedure

1.  **Trigger:** A nightly batch script (`RETENTION_ENGINE`) runs, comparing `Record_Date + Retention_Period` against `Current_Date`. Records identified for disposal are moved to a "Pending Purge" staging area. A notification is generated to the HR Operations Director.
2.  **Review:** The HR Operations Director has a 10-day "cooling-off" period to place a hold on any record (e.g., pending litigation). If no hold is placed, the system automatically executes the purge on day 11.
3.  **Execution and Verification:** The disposal job executes, overwriting the unencrypted data blocks with cryptographically secure random data before releasing the cloud storage blocks. A Destruction Certificate log is written to an immutable ledger (AWS QLDB) for audit purposes.

### 5.5 Cross-Border Data Transfers (Chapter V, GDPR)

As a global entity with offices in the US, UK, and Singapore, Meridian routinely transfers employee data across jurisdictions.

1.  **Data Flow Mapping:** The `HR_Data_Transfer_Impact_Assessment.xlsx` (maintained by HR Ops) maps all flows, including the hub-to-spoke transfer from London to Boston (colocation-managed Workday private cloud) and Boston to Singapore.
2.  **Safeguards for EU/UK Data:**
    - **Binding Corporate Rules (BCRs):** Meridian implemented HR-specific BCRs, approved by the Irish Data Protection Commission (Lead Supervisory Authority) in Q3 2024. These BCRs govern all intra-group transfers of employee data. A summary of the BCRs is provided in the Employee Privacy Notice.
    - **Standard Contractual Clauses (SCCs):** For transfers to a third-country processor (e.g., a US-based benefits provider not bound by our BCRs), the Meridian 2021 EU SCC Module Two (Controller to Processor) template is utilized, supplemented by a Transfer Impact Assessment (TIA).
3.  **Necessity Derogations (Art. 49):** In the rare, non-repetitive circumstance where BCRs or SCCs do not apply, a transfer may be made only if necessary for the performance of the contract between the data subject and Meridian. This is strictly interpreted and must be approved by the CPO prior to the transfer.

---

## 6. Controls and Safeguards

Meridian implements a multi-layered defense-in-depth strategy encompassing administrative, technical, and physical controls.

### 6.1 Technical Controls

- **Encryption:** AES-256 at rest for all data stores (Workday, Snowflake, AWS S3 buckets). TLS 1.3 for all data in transit.
- **Pseudonymization:** Analytics environments utilize tokenized employee IDs, rendering datasets effectively non-identifiable without a key stored in a separate, hardened vault (HashiCorp Vault).
- **Identity and Access Management (IAM):** Role-Based Access Control (RBAC) enforced via Okta SSO integrated with Workday. Segregation of Duties (SOD) rules prevent a single individual from modifying both payroll and banking data.
- **Audit Logging:** All access, modification, and export events within the HR Data Domain are shipped as immutable JSON logs to Splunk Cloud. Anomaly detection rules flag bulk downloads of HR records performed outside of the `HR_Integrations` service account.

### 6.2 Administrative Controls

- **Access Reviews:** Semi-annual "HR Data Access Certification" campaign conducted in SailPoint. Managers must affirmatively re-certify that their team members require their assigned HR roles.
- **Data Minimization:** Workday fields are configured with mandatory field-level help tags indicating the lawful basis for collection. The HRIS team conducts an annual "Field Harvest" sprint to identify and remove any fields that are not actively used for a documented processing purpose.

### 6.3 Access Controls and the HIPAA Intersection

Given that Meridian administers a self-insured health plan, our Benefits team in HR interfaces with electronic Protected Health Information (ePHI). To meet the HIPAA Security Rule's Access Control standard (45 CFR § 164.312(a)(1)), the following technical policies are enforced:

- **Unique User Identification:** All access to ePHI systems (e.g., the Blue Cross Blue Shield portal, Meridian's internal occupational health system) requires a unique Okta-assigned username.
- **Automatic Logoff:** Workday sessions terminate automatically after 15 minutes of inactivity.
- **Access Authorization:** The Benefits Manager role in Workday is the only role granted access to view dependent health enrollment data. This role is granted via a strict Okta group push.

### 6.4 Breach Notification Procedure

In the event of a confirmed Personal Data Breach (both PII and ePHI), the Meridian Incident Response Team (MIRT) is convened. For breaches involving ePHI, Meridian's HIPAA Breach Notification Rule obligations are triggered, requiring notification to affected individuals and the Secretary of HHS. The MIRT assesses the nature and extent of the PHI involved, the unauthorized person who used the PHI, and whether the PHI was actually acquired or viewed. The notification to individuals is provided without unreasonable delay and in no case later than the statutory timeframe.

### 6.5 Physical Controls

- **Clean Desk Policy:** SOP-HR-002 mandates a clean desk policy in HR suites. File cabinets containing employment records are locked at the end of the business day.
- **Access Badging:** HR suites in Boston, London, and Singapore are "Red Zone" access areas, requiring specific badge access granted only to HR personnel and approved facilities staff. Badge logs are reviewed monthly by Physical Security.

---

## 7. Monitoring, Metrics, and Reporting

Compliance with this SOP is continuously monitored through a series of Key Performance Indicators (KPIs) and Key Risk Indicators (KRIs).

| Metric ID | Metric Description | Target / Threshold | Measurement Tool | Reporting Cadence | Owner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **KPI-007-A** | **DSR Timeliness:** Percentage of Data Subject Requests fulfilled within regulatory deadline (30/60 days). | **Target: 100%**<br>Threshold: < 95% | Jira Service Management Dashboard | Monthly | CPO |
| **KPI-007-B** | **Record Purge Accuracy:** Percentage of records dispositioned on their scheduled destruction date without manual intervention. | **Target: 98%**<br>Threshold: < 95% | Workday Audit Trail / AWS QLDB | Quarterly | Dir, HR Ops |
| **KPI-007-C** | **Access Control Recertification:** Percentage of sensitive HR roles re-certified by managers within the 14-day campaign window. | **Target: 100%**<br>Threshold: 90% | SailPoint IdentityIQ | Semi-Annual | CISO |
| **KRI-007-A** | **Unauthorized Access Attempts:** Count of "Access Denied" (Error 403) events in Workday for sensitive worker profile segments. | **Threshold: > 10 attempts from a single user in 1 hour triggers real-time alert.** | Splunk SIEM Alert | Real-Time Alerting; Monthly Trend Report | CISO |
| **KRI-007-B** | **Bulk Data Exports:** Count of events where a single user exports more than 50 employee records from Workday. | **Alert on Any Occurrence** | Splunk SIEM Alert | Real-Time | Dir, HR Ops |

### 7.1 Reporting Cadence

- **Monthly Operational Report:** The HR Operations Director presents a scorecard of KPI-007-A (DSR Timeliness), minor incident volumes, and exception statuses to the CHRO.
- **Quarterly Governance Review:** The CPO presents a consolidated "Employee Data Privacy Dashboard" to the Data Protection Steering Committee (chaired by the CEO), covering all KPIs, KRIs, DPIA approvals, and regulatory horizon scanning.
- **Annual Privacy Report:** A detailed report on the state of employee data privacy, including ROPA updates and training completion rates, is included in the Chief Compliance Officer's annual board presentation.

---

## 8. Exception Handling and Escalation

Privacy by default requires that any deviation from this SOP is formally managed.

### 8.1 Standard Exception Process

1.  **Request:** The requestor (e.g., a recruiter requesting access to a redacted field for an audit) must submit a ticket in the "HR Privacy Exception" queue in Jira. The ticket must specify the data elements involved, the processing purpose, the technical necessity, and the duration (max 90 days).
2.  **Risk Assessment:** The Privacy Analyst completes a mini-risk assessment attached to the Jira ticket, rating the risk as Low, Medium, or High based on data sensitivity and processing volume.
3.  **Approval Matrix:**

    | Risk Level | Approver Required | Documentation Required |
    | :--- | :--- | :--- |
    | **Low** (e.g., extended retention of an org chart) | Director, HR Operations | Jira ticket approval |
    | **Medium** (e.g., granting temporary PI access to an auditor) | CPO | Approved DPIA Lite / Justification Memo |
    | **High** (e.g., processing new category of sensitive data) | CHRO & CPO | Full DPIA signed by both CHRO and CPO |

4.  **Lifecycle:** All exceptions have a hard-coded expiration date. Jira automatically transitions the issue to a "Decommission" workflow 3 days before expiry, notifying the requestor to remove access or cease processing. If no action is taken, the SOC team is automatically assigned to revoke access/execute a clean-up script.

### 8.2 Escalation Path

- **Potential Data Breach Identified:** Any employee who identifies a potential security incident (including a privacy breach) must immediately telephone the Security Operations Center (SOC) at extension `x-1-777` (Boston HQ) or `+44-20-7946-0958` (London). Do not use email or Slack as the sole initial reporting mechanism.
- **Unresolved DSR Dispute:** If a Privacy Analyst cannot resolve an employee's DSR complaint, the matter is escalated within 3 business days to the CPO. The employee is informed of their right to lodge a complaint with their local supervisory authority (e.g., the UK Information Commissioner's Office, the Irish Data Protection Commission).

---

## 9. Training Requirements

Effective privacy protection demands a competent and aware workforce.

| Training Module | Target Audience | Frequency | Delivery Method | Compliance Target |
| :--- | :--- | :--- | :--- | :--- |
| **SOP-HR-007: Employee Data Privacy (Annual Refresher)** | ALL Employees, Contractors | Annually (by Q1 end) | Litmos LMS (15-min video + quiz) | 100% Completion |
| **GDPR Foundations for HR Professionals** | HR Operations, Recruitment, Total Rewards, TA | Annually | Instructor-Led (CPO) | 100% Attendance |
| **Handling Sensitive Data (ART. 9)** | Benefits Team, DEI Analytics Team | Quarterly | Micro-learning Module (Litmos) | 95% Completion |
| **Phishing & Social Engineering Awareness** | ALL Employees | Monthly | Simulated Phishing via KnowBe4 | < 3% Click-Through Rate for HR Dept. |
| **DSR Triage and Processing** | Privacy Operations Team (Legal) | Bi-Annually | Workshop with GC | 100% Certification |

Training completion records are automatically synced from Litmos to the employee's Workday profile. Non-compliance at 30 days past the deadline results in automated notification to the line manager and, at 60 days, a formal written warning per SOP-HR-003 (Progressive Discipline).

---

## 10. Related Policies and References

### 10.1 Internal Meridian Policies

- **SOP-IS-001:** Information Security Policy
- **SOP-IS-005:** Incident Response and Data Breach Notification
- **SOP-IS-008:** Identity and Access Management (Okta & SailPoint)
- **SOP-IA-011:** Internal Privacy Audit Procedure
- **SOP-LG-002:** Global Employee Privacy Notice (External-Facing)
- **SOP-HR-003:** Progressive Discipline Policy
- **SOP-HR-004:** Personnel Records & Retention
- **SOP-COMP-001:** Clinical AI Data Governance
- **SOP-DE-001:** Data Ethics Framework

### 10.2 External Regulations and Frameworks

- **Regulation (EU) 2016/679** (General Data Protection Regulation), specifically Chapter III (Rights of the Data Subject) and Chapter IV (Controller and Processor).
- **UK GDPR** and Data Protection Act 2018.
- **Health Insurance Portability and Accountability Act of 1996** (HIPAA) Privacy and Security Rules.
- **California Privacy Rights Act (CPRA)**.
- **Singapore Personal Data Protection Act 2012 (PDPA)**.
- **ISO/IEC 27001:2022** Information Security, Control A.7.3.1 (Termination responsibilities) and A.5.34 (Privacy and protection of PII).

---

## 11. Revision History

| Version | Date | Author | Description of Changes |
| :--- | :--- | :--- | :--- |
| 1.0 | 2019-03-15 | J. Walsh | Initial document creation. Aligns with pre-GDPR preparation. |
| 2.2 | 2020-11-01 | P. Singh | Major overhaul: Added detailed DSR procedures, Jira portal integration, cross-border transfer maps. |
| 3.0 | 2023-07-12 | M. Okonkwo | Post-Schrems II update; incorporation of Binding Corporate Rules (BCRs) for EU-UK-US transfers. |
| 3.5 | 2024-09-05 | D. Chen | Technical controls refresh: implemented QLDB for destruction logs, Splunk SIEM rules for bulk export alerting. |
| 3.7 | 2025-01-15 | P. Singh | Updated Third-Party vendor processor list; added Culture Amp to DEI data processing procedures. |
| **3.8** | **2025-02-26** | **J. Walsh** | **Annual review cycle. Minor edits to retention table (I-9 period), updated CHRO approval signature. Matured HIPAA access control descriptions.** |