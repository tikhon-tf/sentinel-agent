---
sop_id: "SOP-COPS-013"
title: "Customer Data Breach Communication"
business_unit: "Customer Operations"
version: "4.8"
effective_date: "2025-05-03"
last_reviewed: "2026-12-06"
next_review: "2027-06-27"
owner: "Michael Chang, VP of Customer Operations"
approver: "Robert Liu, VP of Financial Services"
classification: "Internal"
regulations:
  - "GDPR"
  - "HIPAA"
status: "Active"
---

# Standard Operating Procedure: Customer Data Breach Communication

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the framework, operational workflows, and communication protocols for Meridian Health Technologies, Inc. in the event of a Customer Data Breach. The document is designed to ensure a unified, auditable, and legally defensible response that preserves customer trust, meets stringent regulatory obligations under the General Data Protection Regulation (GDPR), and aligns with contractual commitments across all four business lines: Clinical AI Platform, HealthPay Financial Services, MedInsight Analytics, and the Meridian SaaS Platform.

The primary objectives of this SOP are to:
1.  Define a standardized cross-functional incident communication methodology.
2.  Establish clear quantitative timelines for customer-facing notifications based on regulatory severity and data sensitivity classifications.
3.  Provide reusable, legally vetted notification templates to accelerate response times.
4.  Delineate explicit roles and responsibilities to eliminate ambiguity during crisis management.
5.  Ensure demonstrable compliance with Articles 33 and 34 of the GDPR, as enforced by the Data Protection Officer (DPO) and monitored by the Chief Compliance Officer.

### 1.2 Scope

This SOP applies globally to all employees, contractors, temporary staff, and third-party vendors of Meridian Health Technologies, Inc. who access, process, or manage data classified as "Customer Content" or "Personal Data" within any Meridian system. The scope encompasses:

- **In-Scope Data Types:** Protected Health Information (PHI), Personally Identifiable Information (PII), payment card information handled by HealthPay Financial Services, clinical diagnostic data processed by the Clinical AI Platform, and population health datasets stored within MedInsight Analytics.
- **In-Scope Systems:** All production environments on AWS (us-east-1, eu-west-1), Azure DR environments, Snowflake data warehouses, HealthPay transaction engines, and the Meridian SaaS Platform, regardless of physical location.
- **Geographical Applicability:** All global offices in Boston, London, Berlin, Singapore, and Toronto, with specific emphasis on processing activities involving EU Data Subjects.
- **Out of Scope:** Internal corporate data not containing customer or patient information, non-production sandbox environments utilizing synthetic data, and intellectual property breaches that do not involve regulated personal data (these follow Meridian SOP-IS-045, *Intellectual Property Incident Response*).

---

## 2. Definitions and Acronyms

For the purposes of this SOP, the following definitions apply:

| Term | Definition |
| :--- | :--- |
| **Customer Data Breach** | A security incident leading to the accidental or unlawful destruction, loss, alteration, unauthorized disclosure of, or access to, personal data transmitted, stored, or otherwise processed. This specifically excludes unsuccessful login attempts or benign anomalies that do not compromise confidentiality, integrity, or availability. |
| **Breach Notification Coordinator (BNC)** | A dedicated role within Customer Operations responsible for drafting, coordinating approvals, and transmitting all external customer communications during a validated breach event. |
| **High-Risk AI System** | Systems classified under Annex III of the EU AI Act, specifically Meridian’s Clinical AI Platform diagnostic engines. Breaches involving adversarial manipulation of these models fall under this SOP due to potential patient safety impact. |
| **Data Subject** | An identified or identifiable natural person. Under this SOP, includes patients, healthcare provider users, and insurance plan members. |
| **Trigger Condition** | The moment the Meridian Security Incident Response Team (SIRT) validates a confirmed breach, initiating the communication timeline clock. |
| **Criticality Tier** | A classification matrix (Tiers 0-3) that determines notification timelines and channel selection, based on data volume, sensitivity, and regulatory exposure. |
| **CIRT** | Cyber Incident Response Team. |
| **DPO** | Data Protection Officer. |
| **MDR** | Medical Device Regulation (EU) 2017/745. Relevant for clinical communication breaches involving CE-marked medical devices. |

---

## 3. Roles and Responsibilities

Coordination between Customer Operations, Legal, Compliance, Security, and specific Business Units is required. The following Responsibility Assignment Matrix (RACI) clarifies functional ownership.

- **Responsible (R):** The individual(s) who execute the task.
- **Accountable (A):** The single point of ultimate ownership (the "buck stops here").
- **Consulted (C):** Subject matter experts whose input is mandatory before finalization.
- **Informed (I):** Stakeholders updated on progress status.

| Activity/Task | VP Customer Ops (M. Chang) | Breach Notification Coordinator | Data Protection Officer (DPO) | VP of InfoSec | VP of HealthPay (R. Liu) | General Counsel | CIRT Lead |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Breach Validation** | I | I | C | A | I | C | R |
| **Criticality Tier Assignment** | A | R | C | C | C | I | C |
| **Drafting Customer Notification** | C | R | A | C | C | C | I |
| **GDPR Art. 33 Supervisory Notification (72hr)** | I | I | R | C | I | A | C |
| **GDPR Art. 34 Data Subject Communication** | C | R | A | C | C | C | I |
| **Channel Selection & Transmission** | A | R | I | I | C | I | I |
| **Press/Media Query Handling** | C | R | I | I | I | A | I |
| **Post-Incident Review** | A | R | C | C | R | C | C |

---

## 4. Policy Statements

Meridian Health Technologies is committed to transparent and timely communication with customers during adverse data events. The following high-level policies govern this commitment.

**4.1 Transparency and Timeliness Policy**
Meridian shall notify affected Customers without undue delay, and specifically within the timelines defined by the Criticality Tier matrix (Section 5.4). No contractual limitation shall restrict Meridian’s ability to communicate directly with Data Controllers or affected Data Subjects when legally mandated.

**4.2 Centralized Communication Policy**
To prevent fragmented or contradictory messaging, the Breach Notification Coordinator (BNC) serves as the sole authorized drafter and distributor for all mass-customer breach communications. No Business Unit, including Clinical Engineering or HealthPay Operations, may distribute independent "shadow" breach notifications to customers without BNC approval.

**4.3 Regulatory Supervisory Notification Policy**
Where a breach involves risks to the rights and freedoms of natural persons, notification to the competent supervisory authority shall take precedence over customer notification, but shall never delay direct customer notification beyond mandated statutory maximums. Under the EU MDR, any breach impacting the safety performance of AI clinical decision support tools constitutes a reportable event. The BNC shall align with the Clinical Regulatory team regarding CE-marked device communication.

**4.4 No-Fault Interim Communication Policy**
In ambiguous early-stage investigations (between "Trigger Condition" and "Root Cause Confirmation"), the BNC is authorized to distribute "No-Fault" early-warning advisories to high-risk customers, clearly stating that an investigation is underway and providing guidance on immediate precautionary measures. This communication does not constitute a legal admission of liability.

---

## 5. Detailed Procedures

The procedures are organized into four sequential phases: Initial Detection and Validation, Analysis and Tiering, Communication Execution, and Follow-Up & Closure.

### 5.1 Phase I: Detection and Validation

1.  **Initial Alert:** The Meridian Security Information and Event Management (SIEM) system, operated by the CIRT, generates an alert of a potential data exfiltration event, ransomware execution, or unauthorized privilege escalation.
2.  **Preliminary Triage:** The CIRT Lead assesses the alert within 30 minutes. If the incident vector involves "Customer Content" (PHI, PII, Payment Data), the CIRT Lead immediately declares a "Code Yellow" — suspending all non-critical change windows and initiating the digital forensics preservation protocol via AWS GuardDuty and Splunk.
3.  **Validation Confirmation:** The CIRT Lead conducts a manual forensic analysis to rule out false positives.
    - **If False Positive:** The incident log is closed in ServiceNow within 4 hours. No external communication is triggered.
    - **If Validated Breach:** The CIRT Lead immediately marks the ServiceNow incident as `Confirmed Breach`, which triggers the SOP-COPS-013 workflow. This marking action is the **Trigger Condition** and starts the official Timeline Clock (T0).

### 5.2 Phase II: Analysis and Tiering (T0 + 2 Hours)

The VP of InfoSec and CIRT Lead conduct a rapid scoping assessment and assign a Criticality Tier, as defined in Section 5.4.

1.  **Data Volume Estimation:** CIRT determines a bounding estimate of the records exfiltrated (e.g., "less than 1,000 records" vs. "massive unstructured dump > 1 TB").
2.  **Data Sensitivity Assessment:** CIRT identifies data classification by consulting the Meridian Data Catalog:
    - `Class A (Critical)`: Clinical AI diagnostic records, PHI, EU PII, payment account numbers, biometric data.
    - `Class B (Confidential)`: Non-health PII, provider financial data, business emails.
    - `Class C (Internal)`: System logs, metadata (generally does not trigger customer communication unless combined with Class A/B in a specific attack narrative).
3.  **Customer Attribution:** The HealthPay Customer Account Master (CAM) system or MedInsight Tenant Registry is queried to map compromised tenant IDs to valid customer contact information. The BNC verifies the accuracy of the distribution list by cross-referencing the most recent 30-day CRM snapshot.

### 5.3 Phase III: Communication Execution

This phase is owned entirely by the BNC, with legal review required for Tiers 0, 1, and Regulatory-Triggered notifications.

#### 5.3.1 Template Selection and Customization

The BNC selects the correct template from the Meridian Template Repository (Jira Service Management, Confluence Space: `COPS-BREACH-TEMPLATES`):

| Template ID | Use Case | Tone |
| :--- | :--- | :--- |
| **TEMPLATE-T0-URGENT** | Active adversarial threat, ransomware, ongoing data exfiltration. | Urgent, Directive, Action-Oriented. |
| **TEMPLATE-T1-STANDARD** | Confirmed high-sensitivity data loss by an external party or rogue insider. | Formal, Empathetic, High-Assurance. |
| **TEMPLATE-T2-INFORMATIONAL** | Low-sensitivity, contained misconfiguration (e.g., unsecured S3 bucket for < 1h). | Informational, Professional, Reassuring. |
| **TEMPLATE-REG-REGULATOR** | Breach requiring EU or MDR supervisory authority pre-notification. | Legal-Mandated, Formal. |

Customization fields include `[CUSTOMER-NAME]`, `[BRIEF-VECTOR-DESCRIPTION]`, `[DATA-ELEMENTS-IMPACTED]`, and `[REMEDIATION-TAKEN]`.

> **Critical Rule:** For GDPR Article 34 communications, the BNC must include the specific nature of the breach, the name and contact details of the DPO, a clear description of the likely consequences of the data breach, and the measures taken or proposed to be taken to address the breach.

#### 5.3.2 Channel Selection Matrix

| Tier | Primary Channel | Secondary Channel (24h) | Fallback |
| :--- | :--- | :--- | :--- |
| **Tier 0** | PagerDuty Incident Notification, SMS, Email (Salesforce). | Phone calls to Technical Executives. | In-application Admin Banner. |
| **Tier 1** | Email (Salesforce Marketing Cloud). | In-Platform Dashboard Alert. | U.S. Certified Mail. |
| **Tier 2** | Email (Salesforce Marketing Cloud). | Monthly Business Review mention. | None required. |
| **Regulatory Trigger** | Secure Portal Message (GDPR Art. 34 direct channel). | Email to Data Protection Officer contacts. | Registered Letter. |

### 5.4 Phase IV: Follow-Up & Closure

1.  **Root Cause Analysis Publication:** 30 days post-incident, the CIRT Lead publishes a redacted Root Cause Analysis (RCA) document. The BNC distributes this to Tier 0 and Tier 1 impacted customers, and makes it available to Tier 2 customers upon request via a secure portal.
2.  **ServiceNow Ticket Closure:** The BNC moves the master communication ticket to `Resolved` only after confirming 100% delivery or documented delivery failure (bounced) handling for all recipients.
3.  **Process Improvement:** The VP of Customer Operations schedules a formal SOP-COPS-013 review with the DPO and CISO within 10 business days of closure to identify template or workflow improvements.

#### 5.4.1 Criticality Tier Definition and SLA Table

| Tier | Criteria | Customer Notification SLA | Template | Approval Chain |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 0: Critical** | Active ransomware, PHI/PII > 10K records, adversarial manipulation of Clinical AI (MDR Trigger), HealthPay system integrity compromise. | **4 Hours** from T0 via PagerDuty + Phone. | TEMPLATE-T0-URGENT | CISO, General Counsel, DPO, VP HealthPay (R. Liu). |
| **Tier 1: High** | Confirmed exfiltration of Class A/B data < 10K records, insider threat, misconfigured database for > 24h. | **24 Hours** from T0 via primary channel (Email). | TEMPLATE-T1-STANDARD | DPO, General Counsel. |
| **Tier 2: Medium** | Unintentional public exposure of non-sensitive Class C data, minor policy violation without data exfiltration. | **7 Calendar Days** from T0. | TEMPLATE-T2-INFORMATIONAL | BNC Manager. |
| **Regulatory-Only** | Data includes specific EU Special Categories (Art. 9) requiring supervisory notice but not meeting Tier 0 volume. | Coordinated with DPO, not to exceed 72 hours for Regulator, 24 hours for Customer. | TEMPLATE-REG-REGULATOR | DPO, General Counsel. |

---

## 6. Controls and Safeguards

Meridian implements a layered model of technical and administrative controls that specifically govern the communication workflow to prevent unauthorized or malformed notifications.

### 6.1 Access Control for Communication Tools
- **Salesforce Marketing Cloud:** Multi-Factor Authentication (MFA) enforced via Google Workspace SSO. The BNC role is assigned via dedicated Permission Sets, audited monthly by the IAM team. Production list imports require approval from a second BNC Analyst (Four-Eyes Principle).
- **PagerDuty:** Tier 0 broadcasts require verification of the API key by the current on-call Site Reliability Engineer (SRE) before the BNC can inject a "Customer Notification" event.
- **SMS Gateways (Twilio):** Tier 0 SMS capabilities are locked behind a "Break Glass" authentication procedure valid for 120 seconds, accessible only to the VP of Customer Operations and the CIRT Lead.

### 6.2 Communication Integrity Controls
- **Hash Verification:** Every outbound mass email template and accompanying CSV recipient list is sha256-hashed. The BNC validates the delivered hash against the Jira `COPS-BREACH` ticket artifact to ensure tampering did not occur between extraction and transmission.
- **URL Rewriting and Tracking:** All links are proxied through Proofpoint URL Defense. Click-tracking is enabled to create an auditable log of customer engagement, which is later used for non-responder follow-up logic.

### 6.3 GDPR-Specific Data Subject Access Control
- **Encrypted Self-Service Portal:** In compliance with the need for confidential communication, a temporary, tokenized Secure Breach Portal instance is spun up on an isolated AWS subnet (eu-west-1). Customers are given an expiring token (24-hour TTL) to view the full breach disclosure, download affected data logs (if identifiable), and communicate directly with the DPO.

### 6.4 Administrative Safeguards
- **Mandatory Approval Gates:** No communication for Tier 0 or Tier 1 can leave the Meridian network unless the ticket in Jira Service Management has status `Ready to Send`, which requires digital sign-offs from the specific approvers listed in the Tier Definition Table (Section 5.4.1).
- **Audit Trail Immutability:** A write-once log entry is recorded in the Compliance Vault (AWS S3 Object Lock — Governance Mode) for every communication sent, capturing the sending user, timestamp, recipient list hash, template used, and approval chain.

---

## 7. Monitoring, Metrics, and Reporting

The effectiveness of SOP-COPS-013 is continuously measured against quantitative KPIs to identify delays, bottlenecks, or training deficiencies.

### 7.1 Real-Time Monitoring Dashboards
A dedicated Kibana dashboard (`COPS-013-Breach-Comms`) pulls data from ServiceNow, Salesforce, and Twilio logs to provide executive visibility:

- **Current Breach Widget:** Visual countdown timer ("Time Since T0: HH:MM"), current Tier, and notification status (Draft / Sent / Delivered).
- **Delivery Queue Depth:** Number of pending emails, SMS, and PagerDuty alerts in buffer.
- **Bounce & Non-Delivery Tracker:** Real-time visualization of hard bounces, enabling the BNC to trigger manual phone calls for Tier 0 incidents.

### 7.2 Key Performance Indicators (KPIs)

| Metric | Threshold (Target) | Measurement Tool | Reporting Owner |
| :--- | :--- | :--- | :--- |
| **Mean Time to Notify (MTTN)** | T0: < 4h, T1: < 24h, T2: < 7 days. | ServiceNow SLA Timer | Michael Chang |
| **Template Selection Accuracy** | 100% (Zero mismatch between Tier and Template chosen). | BNC Manager Audit | BNC Manager |
| **Recipient List Accuracy** | 100% (Zero reports of "Not Our Tenant" from valid customers). | CRM Snapshot Comparison | Robert Liu (HealthPay) |
| **Regulator Notification Timeliness (GDPR Art. 33)** | 72 hours from Trigger Condition. | DPO Case Log | DPO |
| **Post-Breach Customer Attrition** | < 5% Tier-specific churn within 90 days. | CRM Retention Dashboard | Michael Chang |

### 7.3 Reporting Cadence
- **Real-Time:** The `COPS-013-Breach-Comms` dashboard is the single pane of glass during active incidents.
- **Weekly:** The BNC Manager submits a "Zero Breach Report" or summarizes open incidents to the VP of Customer Operations.
- **Monthly:** A consolidated breach communication metrics package is reviewed by the Data Governance Steering Committee, chaired by the DPO and the Chief Compliance Officer.
- **Quarterly:** KPI trends and process improvement recommendations are presented to the Meridian Executive Risk Committee.

---

## 8. Exception Handling and Escalation

All deviations from the standard SLA timelines or template requirements must follow a highly governed exception process to ensure accountability.

### 8.1 Exception Criteria
Exceptions to the SLA timelines defined in Section 5.4.1 may be granted only under the following limited circumstances:
1.  **Active Hostage/Life-Safety Event:** A credible physical threat related to the cyber incident that requires coordinated law enforcement intervention before customer alerting.
2.  **Forensic Freeze:** An explicit, documented directive by the VP of InfoSec that sending a notification would prematurely alert the adversary, destroying critical forensic evidence needed to determine the full scope of the breach. This "freeze" cannot exceed **24 hours** for Tier 0, or **72 hours** for Tier 1, without escalation to the CEO.
3.  **Legal Seal:** An official protective order, court seal, or law enforcement directive prohibiting disclosure for a defined period.

### 8.2 Escalation Path
If a CIRT or Legal "freeze" is demanded, the Business Owner (VP, Customer Operations) must execute the following escalation immediately:

1.  **Initial Dispute:** VP Customer Operations logs a "COPS-013 Exception Request" in ServiceNow, linking the incident and stating the reason for the delay.
2.  **Executive Trigger:** If the requested delay exceeds the thresholds in Section 8.1, the ServiceNow ticket automatically triggers an emergency email to:
    - **Decider:** General Counsel.
    - **Inform:** Chief Medical Officer (for Clinical AI Tier 0), Chief Financial Officer (for HealthPay), VP Customer Operations.
3.  **Compensating Controls:** During the delay, compensating controls must be activated. For a HealthPay Tier 0 "Forensic Freeze," the VP of Financial Services (Robert Liu) must authorize a manual transaction-monitoring "Circuit Breaker" for the impacted tenant, effectively freezing monetary movement while the forensic investigation concludes.

---

## 9. Training Requirements

All personnel mapped to a "Responsible" or "Accountable" role in the RACI matrix (Section 3) must undergo mandatory training to ensure technical and procedural readiness.

### 9.1 Training Curriculum

| Module Code | Training Content | Target Audience | Duration |
| :--- | :--- | :--- | :--- |
| **COPS-013-MOD1** | *SOP-COPS-013 Process Walkthrough:* Trigger, Triage, Tiering, and Templates. | Breach Notification Coordinator, CIRT Analysts, Customer Ops Managers. | 2 Hours |
| **COPS-013-MOD2** | *Template Customization & Communication Tone:* Handling Tier 0 empathy vs. Tier 1 formality, avoiding liability-creating language. | BNC Analysts. | 1.5 Hours |
| **COPS-013-MOD3** | *GDPR & Clinical Data Nuance:* Specific Art. 33/34 requirements, MDR clinical risk communication, DPO coordination. | DPO Office, Legal Team, Clinical Engineering Leads. | 3 Hours |
| **COPS-013-MOD4** | *Tabletop Simulation (Tabletop Ex):* A 4-hour live simulation where a Meridian "Red Team" simulates a Tier 0 Clinical AI data injection breach, forcing the team through all 4 Phases in real-time. | Entire CIRT, Customer Ops, HealthPay Leadership. | 4 Hours (Quarterly) |

### 9.2 Frequency and Tracking
- **Initial Onboarding:** Must be completed within 5 business days of role assignment.
- **Annual Refresh:** Modules COPS-013-MOD1 through MOD3 must be retaken annually.
- **Quarterly Tabletop:** The simulation (MOD4) is mandatory for VP-level approvers and the BNC Team on a quarterly calendar. Attendance is tracked via Jira Service Management.
- **LMS Tracking:** All training completions, simulation results, and failure-to-complete escalations are logged in Workday Learning (LMS). The BNC Manager’s quarterly performance objective includes a `100% Team Training Compliance` KPI.

---

## 10. Related Policies and References

This SOP must be executed in conjunction with the following internal policies and external regulatory standards:

### 10.1 Internal Meridian SOPs
| SOP ID | Document Title | Relationship to SOP-COPS-013 |
| :--- | :--- | :--- |
| SOP-IS-045 | *Intellectual Property Incident Response* | Out-of-scope; referenced for non-personal-data breaches. |
| SOP-SEC-002 | *Identity and Access Management (IAM)* | Governs access to the communication systems described in Section 6. |
| SOP-CLIN-077 | *Clinical Decision Support System Integrity Protocol* | Co-executed for Tier 0 Clinical AI breaches under MDR guidelines. |
| SOP-ENG-019 | *AWS Account and S3 Bucket Security* | Referenced when the root cause is a cloud misconfiguration. |
| SOP-LEG-001 | *Regulatory Notification Framework* | Governs the internal DPO legal review process prior to Art. 33 notifications. |

### 10.2 External Regulatory Standards
- **EU General Data Protection Regulation (GDPR) 2016/679:**
    - **Article 33:** Notification of a personal data breach to the supervisory authority.
    - **Article 34:** Communication of a personal data breach to the data subject.
- **EU Medical Device Regulation (MDR) 2017/745:** Concerning post-market surveillance (PMS) reporting for CE-marked clinical AI products, specifically incident reporting timelines overlapping with this SOP.

---

## 11. Revision History

| Version | Date | Author(s) | Description of Changes |
| :--- | :--- | :--- | :--- |
| **1.0** | 2023-01-10 | J. Miller (COPS) | Initial draft; basic email notification template. |
| **2.1** | 2023-06-15 | M. Chang (VP COPS) | Added Tier definitions and first PagerDuty integration. |
| **3.0** | 2024-02-01 | L. Strauss (Legal) | Major revision; added GDPR Art. 33/34 procedures, approval gates. |
| **4.0** | 2024-11-20 | S. Chen (DPO Office) | Integrated MDR reporting requirements for Clinical AI Tier 0. |
| **4.5** | 2025-03-01 | M. Chang (VP COPS) | Updated RACI matrix, integrated HealthPay VP (R. Liu) as approver for financial data breaches. Added Twilio "Break Glass" SMS protocol. |
| **4.8** | 2025-05-03 | M. Chang (VP COPS) | Refinement of Tier 0 SLA from "Best Effort" to "4 Hours Firm". Updated Template REPO Links. Pre-review for EU AI Act alignment. |