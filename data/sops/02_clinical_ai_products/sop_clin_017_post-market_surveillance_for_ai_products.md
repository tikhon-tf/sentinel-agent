---
sop_id: "SOP-CLIN-017"
title: "Post-Market Surveillance for AI Products"
business_unit: "Clinical AI Products"
version: "5.1"
effective_date: "2024-12-04"
last_reviewed: "2025-03-17"
next_review: "2025-09-09"
owner: "Dr. Aisha Okafor, VP of Clinical AI Products"
approver: "Dr. Priya Patel, Chief Medical Officer"
classification: "Internal"
regulations:
  - "EU AI Act"
  - "HIPAA"
status: "Active"
---

# Standard Operating Procedure: Post-Market Surveillance for AI Products

**SOP ID:** SOP-CLIN-017
**Version:** 5.1
**Effective Date:** 2024-12-04
**Owner:** Dr. Aisha Okafor, VP of Clinical AI Products
**Approver:** Dr. Priya Patel, Chief Medical Officer

---

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the framework, responsibilities, and operational procedures for the continuous post-market surveillance (PMS) of all artificial intelligence and machine learning (AI/ML) products developed and deployed by the Clinical AI Products business unit of Meridian Health Technologies, Inc. The purpose of this surveillance system is to proactively collect, monitor, analyze, and act upon real-world performance data to ensure the continued safety, effectiveness, and compliance of our AI products throughout their lifecycle. This SOP ensures a systematic process for identifying, escalating, and resolving product safety issues, performance degradation, and unintended outcomes that may emerge after clinical deployment.

### 1.2 Scope

This SOP applies to all AI/ML-based software products classified under the Clinical AI Platform business line that have been released for clinical use. This includes, but is not limited to:

| Product Category | Examples | Deployment Context |
|---|---|---|
| Diagnostic Imaging Analysis | Chest X-ray AI, Retinal Scan Classifier, CT Anomaly Detection | Radiology departments, PACS integration |
| Clinical Decision Support | Sepsis Early Warning System, Readmission Risk Scorer | EHR-embedded workflows, nursing dashboards |
| Patient Risk Scoring | Deterioration Index, Comorbidity Burden Calculator | Population health, inpatient monitoring |
| Adverse Event Prediction | Drug-Drug Interaction Predictor, Fall Risk AI | Pharmacy systems, care planning |

This SOP encompasses the following post-market activities:
- Continuous real-world performance monitoring and drift detection.
- Structured collection and analysis of complaints, adverse events, and near-misses.
- Proactive field safety communication and corrective action management.
- Periodic safety update reporting to internal governance bodies.
- Integration with Meridian’s quality management system (QMS).

This SOP applies to all employees, contractors, and third-party partners involved in the development, deployment, monitoring, support, and oversight of Clinical AI products. Adherence is mandatory for personnel in Engineering, Data Science, Clinical Operations, Customer Operations, Quality Assurance, Regulatory Affairs, Legal, and Compliance teams.

### 1.3 Out of Scope

This SOP does not cover the pre-market validation, clinical trial processes, or initial FDA 510(k) clearance submission activities. Refer to SOP-RD-004 (Design Control and Pre-Market Validation for AI/ML Devices). This SOP also does not cover general IT infrastructure monitoring of the Meridian SaaS Platform, which is addressed in SOP-IT-022 (Cloud Platform Operational Monitoring).

---

## 2. Definitions and Acronyms

### 2.1 Definitions

| Term | Definition |
|---|---|
| **Adverse Event** | Any untoward medical occurrence in a patient or clinical user that is temporally associated with the use of a Meridian AI product, whether or not considered product-related. |
| **Complaint** | Any written, electronic, or oral communication that alleges deficiencies related to the identity, quality, durability, reliability, safety, effectiveness, or performance of a Meridian AI product. |
| **Concept Drift** | A change in the underlying statistical properties of the relationship between model inputs (features) and the target output (prediction) over time. |
| **Data Drift** | A change in the distribution of input data features fed to the model compared to the training or baseline distribution. |
| **Field Safety Corrective Action (FSCA)** | Any action taken by Meridian to reduce a risk of death or serious deterioration in health associated with a released AI product. May include product recall, software patch, configuration change, or advisory notice. |
| **Model Decay** | The gradual degradation of a model's predictive performance over time, typically measured by key performance indicators. |
| **Post-Market Surveillance (PMS)** | The systematic, proactive process of collecting and analyzing experience from AI products in clinical use to identify safety or performance issues and ensure continuous product safety. |
| **Prediction Shift** | A statistically significant change in the distribution of model output scores in a live environment relative to a validated baseline. |
| **Real-World Performance** | The measured accuracy, safety, and effectiveness of an AI product in actual clinical settings, distinct from controlled pre-market validation. |
| **Serious Incident** | An adverse event that resulted in, or could have resulted in, death, life-threatening illness or injury, hospitalization, disability, or a congenital anomaly. |

### 2.2 Acronyms

| Acronym | Definition |
|---|---|
| AIRC | AI Incident Response Committee |
| CMO | Chief Medical Officer |
| CPO | Chief Privacy Officer / DPO |
| CPR | Clinical Performance Report |
| CSM | Customer Success Manager |
| DPA | Data Protection Authority |
| FSCA | Field Safety Corrective Action |
| GC | General Counsel |
| KPI | Key Performance Indicator |
| MDR | Medical Device Regulation (EU) |
| MLflow | Machine Learning Lifecycle Management Platform |
| OCR | Office for Civil Rights (HHS) |
| PHI | Protected Health Information |
| PMS | Post-Market Surveillance |
| PSM | Post-Market Surveillance Manager |
| QMS | Quality Management System |
| SDE | Safety Data Event |
| SLA | Service Level Agreement |

---

## 3. Roles and Responsibilities

The following RACI matrix defines the responsible, accountable, consulted, and informed parties for post-market surveillance activities.

| Activity / Decision | VP Clinical AI | PSM | Clinical Ops Lead | CISO / DPO | CMO | AI Ethics Board | GC |
|---|---|---|---|---|---|---|---|
| **PMS Plan Ownership & Maintenance** | A | R | C | C | I | C | C |
| **Continuous Performance Monitoring** | I | R | C | I | I | I | I |
| **Complaint Intake & Classification** | I | A | R | C | C | I | I |
| **Adverse Event Investigation** | I | R | C | C | A | C | C |
| **Initiation of Field Safety Corrective Action** | C | R | I | C | A | C | C |
| **Regulatory Notification Decision** | C | R | I | C | A | C | A |
| **Periodic Safety Report Approval** | A | R | C | C | C | C | I |
| **Customer Communication** | I | C | A | I | I | I | C |

**R = Responsible, A = Accountable, C = Consulted, I = Informed**

### 3.1 Key Role Descriptions

**VP of Clinical AI Products (Dr. Aisha Okafor)**
Accountable for the overall effectiveness of the PMS system. Authorizes major Field Safety Corrective Actions and holds final sign-off authority for product retirement decisions based on safety trends.

**Post-Market Surveillance Manager (PSM)**
A dedicated role within the Clinical AI Products business unit, reporting to the VP of Clinical AI. Responsible for the day-to-day execution of this SOP, including maintaining the surveillance plan, managing complaint investigations, overseeing monitoring dashboards, and authoring the aggregate Clinical Performance Report.

**Clinical Operations Lead**
Manages the frontline intake of complaints and adverse event reports submitted by clinicians and customer site administrators. Owns the relationship with customer sites for incident investigation and data collection.

**Chief Medical Officer (Dr. Priya Patel)**
Provides clinical expertise for safety signal evaluation and adverse event severity classification. Accountable for clinical safety determinations and serves as the final medical safety escalation point.

**Chief Information Security Officer (Rachel Kim) & Chief Privacy Officer (Dr. Klaus Weber)**
Consulted on any PMS activity involving a potential breach of PHI or system security incident. The CPO evaluates data protection impact and leads any required breach notifications.

**AI Ethics Board**
A cross-functional governance committee co-chaired by the Chief AI Officer and General Counsel, including clinical, legal, and technical leadership. Provides consultation on AI-specific fairness and bias issues identified during monitoring.

---

## 4. Policy Statements

Meridian Health Technologies is committed to maintaining the highest standards of safety and performance for its clinical AI products throughout their entire operational lifecycle. The following policy commitments govern our post-market surveillance activities:

4.1 **Continuous Monitoring Mandate:** All production Clinical AI models shall undergo automated, continuous performance monitoring against established clinical and technical benchmarks. No model shall operate without active surveillance instrumentation.

4.2 **Proactive Safety Culture:** Meridian proactively solicits and analyzes real-world performance data and user feedback. We do not rely solely on passive complaint intake. All personnel have a duty to report any suspected safety issue or performance anomaly.

4.3 **Structured Complaint Management:** All complaints, regardless of perceived severity, shall be formally logged, assigned a unique identifier, and investigated in accordance with a defined, risk-based timeline. No complaint shall be closed without a documented root-cause analysis or a justified rationale for closure.

4.4 **Timely Corrective Action:** Upon identification of a validated safety signal that presents an unacceptable risk, Meridian commits to initiating a Field Safety Corrective Action (FSCA) and communicating with affected sites within a risk-proportionate timeframe.

4.5 **Periodic Safety Reporting:** A comprehensive Clinical Performance Report (CPR) shall be compiled and presented to senior leadership at least quarterly, aggregating all surveillance data, complaint trends, and corrective actions.

4.6 **Customer Transparency:** Customers shall be informed of product-specific PMS activities during onboarding and shall be provided a clear mechanism for reporting issues. Significant safety advisories shall be communicated to all impacted customers.

4.7 **HIPAA Breach Notification:** In the event a surveillance activity or complaint investigation uncovers a potential breach of Protected Health Information (PHI), the incident shall be immediately escalated to the Chief Privacy Officer. If qualifying as a reportable breach, Meridian will notify affected individuals and relevant authorities without unreasonable delay, consistent with legal obligations.

4.8 **Training:** All Clinical AI personnel and customer-facing support staff shall complete annual post-market surveillance and complaint-handling training.

---

## 5. Detailed Procedures

### 5.1 Post-Market Surveillance Plan Management

The PSM maintains a modular Post-Market Surveillance Plan document for each product family. The plan is the living specification for how a product is monitored.

**5.1.1 Plan Content Requirements**
Each product’s PMS Plan must contain:
- **Product Description:** Version, intended use, intended patient population.
- **Safety Profile:** A summary of residual risks identified from pre-market risk analysis (refer to SOP-RM-003).
- **Performance Metrics:** The Key Performance Indicators (KPIs) relevant to the product’s clinical function, their acceptable limits, and drift thresholds.
- **Data Sources:** A specification of the data pipelines and monitoring infrastructure used (see Section 6).
- **Surveillance Methods:** The specific methods used (e.g., automatic drift detection, periodic user surveys, site audits).
- **Surveillance Schedule:** Frequency of automated metric checks, manual reviews, and report generation.

**5.1.2 Plan Review Cadence**
The plan shall be reviewed with the product team during the normal sprint cycle and formally updated:
- Upon any significant product update or version release (major or minor).
- At least annually, timed with the product’s initial deployment anniversary.
- As an output of any major incident review (see Section 8).

### 5.2 Real-World Performance Monitoring

The core of the PMS system is the continuous monitoring of model performance in live clinical environments.

**5.2.1 Automated Performance Metrics Collection**
For each Clinical AI model, the following metrics shall be calculated on a **daily rolling 7-day window** and compared against the validated baseline from pre-market assessment:

| Metric Category | Metric Name | Typical Drift Threshold | Monitoring Tool |
|---|---|---|---|
| **Data Quality** | % Missing Features | > 5% absolute increase | Datadog + Custom |
| **Data Quality** | Feature Out-of-Range Rate | Per-feature spec | Datadog + Custom |
| **Input Drift** | PSI (Population Stability Index) | > 0.25 | Evidently AI |
| **Input Drift** | Chi-squared Distribution Test | p < 0.01 | Evidently AI |
| **Output Drift** | Mean Prediction Score | > 1.5 Std Dev shift | Evidently AI |
| **Output Drift** | Prediction Category Shift | > 10% in a category | Custom Looker Dashboard |
| **Performance** | Gini / AUROC (if labels available) | < 0.05 absolute drop | Custom, MLflow |
| **Fairness** | Demographic Parity Difference | > 0.1 | Custom Monitoring |

**5.2.2 Manual Performance Review via Clinical Audits**
In addition to automated monitoring, Clinical Operations shall coordinate structured clinical audits for each product line. An audit involves a retrospective chart review of a random sample of at least **200 patient encounters per product per quarter**. Results are reviewed by the CMO and PSM.

**Procedure:**
1. **Sample Pull (Week 1):** Clinical Data Team pulls a random sample of 200 encounters where the AI product's primary prediction was generated, stratified by site and clinical outcome to ensure a representative mix.
2. **Blinded Review (Weeks 2-3):** A panel of three independent clinicians reviews the cases. They are provided with the AI’s score and the patient’s actual outcome. They grade the AI’s performance as: **Clinically Appropriate**, **Clinically Ambiguous**, or **Clinically Inappropriate**.
3. **Concordance Scoring (Week 4):** The PSM calculates inter-rater reliability and overall concordance. A Clinically Inappropriate rate exceeding **5%** triggers an immediate deep-dive investigation per Section 8.

### 5.3 Complaint Handling and Adverse Event Reporting

This procedure covers the lifecycle of a report from intake to closure.

**5.3.1 Intake and Logging**
All complaints and adverse event reports are received via one of the following channels:
- **Customer Portal:** "Report a Concern" form in the Meridian Support Hub (primary intake).
- **Direct Communication:** Email to clinical-support@meridian.com or a call to the Customer Success Manager (CSM).
- **Internal Reporting:** Any Meridian employee identifying a potential issue during an audit or internal test.

The Clinical Operations Lead (or designated triage specialist) is responsible for monitoring all intake channels. Upon receipt, within **1 business day**, a unique SDE (Safety Data Event) ticket must be created in the QMS (Quality Management System) system (ServiceNow QMS Module).

**SDE Ticket Creation Procedure:**
1. Log in to ServiceNow QMS Module.
2. Select "Create New" -> "SDE Record".
3. Populate the **SDE Intake Form** with the following mandatory fields:
   - **Reporter Information:** Name, Role, Site, Contact Details.
   - **Product:** Specific AI Product Name and deployed Version Number.
   - **Date of Incident:** Date the event occurred.
   - **Description:** Verbatim description from the reporter.
   - **Initial Severity Classification:** (See 5.3.2).

**5.3.2 Triage and Severity Classification**
Each SDE ticket is triaged by the Clinical Operations Lead within **1 business day** of creation. Severity is classified using the **Meridian AI Severity Scale (3-Level)** .

| Severity Level | Definition | Response SLA |
|---|---|---|
| **Level 1: Critical** | A confirmed serious adverse event with a probable causal link to the AI product, potential for imminent patient harm, or system-wide outage. | Investigation initiated within 4 hours. CMO and VP Clinical AI notified immediately. |
| **Level 2: Major** | A significant performance deviation, a near-miss, or a complaint involving a non-serious but clinically relevant error. | Investigation initiated within 2 business days. PSM notified immediately. |
| **Level 3: Minor** | A cosmetic defect, user interface annoyance, or a single user's subjective dissatisfaction without clinical impact. | Logged for trend analysis. Acknowledged to reporter within 5 business days. No formal investigation required unless trend emerges. |

**5.3.3 Investigation**
The PSM is responsible for leading the investigation for all Level 1 and Level 2 events. The investigation follows a structured root-cause analysis process.

**Procedure:**
1. **Assemble File:** PSM compiles all relevant data: full model inputs and outputs for the incident encounter, user logs, site configuration, a snapshot of the model version and feature store at the time of the event, similar cases from the reporting site for the last 30 days.
2. **Form Investigation Team:** PSM convenes a team including a Data Scientist (model owner), a Clinical Specialist (relevant to the product), and the site’s CSM. For safety investigations, the CMO is a mandatory team member.
3. **Clinical Analysis:** The clinical specialist reviews the case in detail to determine if the AI output was clinically reasonable given the inputs, regardless of outcome.
4. **Technical Analysis:** The data scientist analyzes the model inputs for an outlier or anomalous features, runs a counterfactual analysis, and checks for any underlying data pipeline errors.
5. **Root Cause Categorization:** The team must categorize the root cause as one of the following:
   - **Input Data Error:** Incorrect, missing, or corrupted data fed to the model from the EHR.
   - **Model Error:** The model correctly processed valid inputs but produced an incorrect prediction.
   - **Clinical Workflow Error:** The model output was correct but was misinterpreted, ignored, or misapplied by the clinical user.
   - **System/IT Failure:** A downstream system integration failure (e.g., score not displayed in EHR).
   - **No Issue Found:** Investigation confirms product functioned as intended.
6. **Investigation Report:** The PSM documents findings in the "SDE Investigation Template" within ServiceNow and submits for approval. The CMO must approve all Level 1 and Level 2 investigation reports.

### 5.4 Field Safety Corrective Actions (FSCA)

An FSCA is initiated when a validated safety issue requires an action to prevent or reduce a risk.

**5.4.1 Criteria for Initiating an FSCA**
An FSCA is mandatory in any of the following circumstances:
- A confirmed Level 1 Severity Event with a root cause of "Model Error" or "Input Data Error" that could be systemic.
- Identification of a systematic defect through trend analysis (e.g., cluster of Level 2 events with common root cause) that presents an unacceptable clinical risk.
- A regulatory authority mandate.

**5.4.2 FSCA Decision Procedure**
1. **Safety Alert Review Meeting:** The PSM convenes an urgent meeting with the VP of Clinical AI, CMO, GC, and the AI Product Lead. The PSM presents the incident report and trend data.
2. **Risk Assessment:** The committee reviews the severity and probability of harm.
3. **Corrective Action Decision:** The committee determines the most appropriate action. Options include:
   - **Technical Correction:** A targeted software "hotfix" or patch.
   - **System Controls:** Implementation of a hard-stop or clinical guardrail in the software workflow.
   - **Customer Advisory Notice:** A communication to customer site administrators warning of the issue and providing recommended mitigation steps (e.g., specific patient cohorts, workflow changes).
   - **Product Recall:** For extreme circumstances, removing an AI model from commercial clinical use at all or targeted sites.
4. **Approval:** The CMO and VP of Clinical AI jointly approve the FSCA plan.

**5.4.3 FSCA Execution and Follow-up**
1. **Customer Notification:** The VP of Customer Operations, working with the GC, drafts and sends the advisory or recall notice to all impacted sites. The notice includes a clear description of the issue, the patient risk, the required corrective action, and contact information for questions.
2. **Verification of Effectiveness:** For corrective actions requiring a software update, the PSM must monitor the specific performance metric related to the failure for a defined, pre-specified period (minimum **30 days** post-deployment) to confirm the issue is resolved.
3. **Closure:** An FSCA is formally closed only when the verification of effectiveness is positive and all customer sites have acknowledged the advisory.

### 5.5 Periodic Reporting

Aggregate PMS data is reviewed and reported to provide a holistic view of product safety.

**5.5.1 Clinical Performance Report (CPR)**
The PSM authors a quarterly Clinical Performance Report for each major product family. This report aggregates:
- A summary of all SDE tickets, by severity and root cause category.
- Trending of KPI data and drift metrics.
- Summary of clinical audit findings.
- Status of any open FSCAs.
- A cumulative safety profile update.

The report is submitted by the PSM to the AI Ethics Board for review within **30 days** of the quarter end.

---

## 6. Controls and Safeguards

### 6.1 Technical Controls

The following technical controls are implemented to support and enforce PMS procedures.

| Control ID | Control Description | Implementation |
|---|---|---|
| **CTRL-PMS-01** | **Automated Drift Detection** | Evidently AI monitors are deployed on all production model prediction pipelines. A daily batch job calculates PSI and other drift metrics against a stored baseline profile in the MLflow Model Registry. |
| **CTRL-PMS-02** | **Immutable Inference Logs** | Every model prediction and the input feature vector are hashed (SHA-256) and logged to a tamper-proof, append-only data store (AWS CloudWatch Logs with MFA-protected data integrity). This ensures a trusted audit trail for investigation. |
| **CTRL-PMS-03** | **Model Version Gating** | The MLflow Model Registry enforces a staging-to-production workflow. Only models with a validated "baseline" tag and approved surveillance plan can be deployed to production. |
| **CTRL-PMS-04** | **Proactive Alerting** | Critical drift thresholds (PSI > 0.25, Model Error rate > 2% in clinical audit) trigger automated, high-priority PagerDuty alerts to the PSM, Clinical Ops Lead, and the on-call Clinical AI SRE team. |

### 6.2 Administrative Controls

| Control ID | Control Description |
|---|---|
| **CTRL-ADM-01** | **PMS Procedure Training** | Annual training on this SOP for all roles in the RACI matrix, including complaint handling and severity classification. Training is tracked via Workday. |
| **CTRL-ADM-02** | **Access Control** | Access to the ServiceNow QMS module and raw complaint data is restricted via Role-Based Access Control (RBAC) to the PSM, Clinical Ops Team, and relevant Quality personnel. |
| **CTRL-ADM-03** | **PHI Minimization for Monitoring** | Where feasible, technical monitoring dashboards (Datadog, Evidently) are configured to aggregate data and surface metadata (drift scores, error rates) without displaying raw Protected Health Information (PHI). Full PHI access is limited for investigation purposes only. |

### 6.3 PHI Handling Procedures

Access to raw PHI for the purpose of a PMS investigation must follow these procedures:
1. **Justification:** The PSM must document the specific justification for accessing PHI in the SDE ticket.
2. **Minimal Access:** Access shall be granted to the minimum necessary PHI, for the minimum number of investigators.
3. **Audit Trail:** All access to and export of PHI from the PMS system is logged and auditable. The CPO conducts a quarterly review of PHI access logs. Any unauthorized access or suspected breach must be reported to the CISO within **24 hours** of discovery.
4. **Workforce Training:** All personnel with potential access to PHI must complete PHI handling and HIPAA compliance training annually.

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs) for the PMS Process

The performance of the surveillance system itself is tracked to ensure its effectiveness.

| PMS Process KPI | Target | Owner | Measurement Tool |
|---|---|---|---|
| **Mean Time to SDE Ticket Creation** | < 1 business day | Clinical Ops Lead | ServiceNow QMS |
| **Mean Time to Level 1 Investigation Initiation** | < 4 hours | PSM | ServiceNow QMS |
| **Mean Time to Level 1 Investigation Closure** | < 45 calendar days | PSM | ServiceNow QMS |
| **Mean Time to Level 2 Investigation Closure** | < 60 calendar days | PSM | ServiceNow QMS |
| **FSCA Effectiveness Verification Completion** | 100% within defined period | PSM | ServiceNow QMS |
| **PMS Plan Review & Update Cycle** | 100% compliant with schedule | PSM | MLflow Registry |

### 7.2 Reporting Cadence

| Report | Audience | Frequency | Author | Delivery Mechanism |
|---|---|---|---|---|
| **Product Health Dashboard** | Product Managers, Engineering Leads | Real-time, Live | PSM / MLOps | Shared Looker Dashboard |
| **Monthly Complaint Trend Report** | VP of Clinical AI, CMO | Monthly, by 10th | PSM | PDF to email, PowerPoint for review |
| **Quarterly Clinical Performance Report** | AI Ethics Board, Executive Leadership | Quarterly, by end of following month | PSM | Formal written report for QMS record |

---

## 8. Exception Handling and Escalation

### 8.1 Deviation from SOP Procedures

Any deviation from a mandated SLA or procedure defined in this SOP must be handled via a formal Exception Request. This includes, but is not limited to, pausing monitoring for a non-active model, exceeding an investigation timeline, or using a non-standard FSCA communication method.

**Procedure:**
1. **Initiation:** The Responsible party documents the deviation in an "SOP Exception Request" form in the QMS. The request includes the specific procedure deviated from, the justification, the risk assessment of the deviation, and the proposed timeline.
2. **Approval Path:**
   - Level 1 Investigation-related exceptions: Approval by CMO.
   - Level 2 Investigation or Reporting-related exceptions: Approval by VP of Clinical AI.
   - FSCA-related exceptions: Joint approval by CMO and GC.

### 8.2 Escalation of Disagreements

If a safety-related disagreement cannot be resolved at the operational level (e.g., disagreement on root cause between engineering and clinical teams, or on the need for an FSCA), the PSM shall escalate the issue.

**Escalation Path:**
1. **Step 1 (Technical):** Escalate to VP of Engineering and VP of Clinical AI to attempt resolution.
2. **Step 2 (Clinical Safety):** If unresolved, escalate to the Chief Medical Officer. The CMO’s decision on clinical safety matters is final and binding.
3. **Step 3 (Regulatory/Compliance):** If the CMO and VP of Clinical AI agree that an unresolved risk may have regulatory or compliance implications, they notify the General Counsel (GC).
4. **Step 4 (Ethical):** For issues with a significant AI ethics or fairness dimension, any member of the AI Ethics Board may escalate the issue directly to the full Board for deliberation and a non-binding recommendation to the executive leadership.

---

## 9. Training Requirements

### 9.1 Role-Based Training Curriculum

All personnel assigned roles in the RACI matrix (Section 3) shall complete the following training before being granted access to PMS systems and data.

| Required Training Module | Target Audience | Frequency | Tracking System |
|---|---|---|---|
| **PMS-101: Principles of Post-Market Surveillance** | All personnel in scope | Annually | Workday |
| **PMS-201: SDE Intake, Triage, and the Severity Scale** | Clinical Ops Lead, CSMs, Tier 1 Support | Annually | Workday |
| **PMS-301: Advanced Root-Cause Investigation for AI/ML** | PSM, Data Science Leads, SREs | Annually | Workday |
| **HIPAA-101: Protected Health Information Handling & PHI Minimization** | All personnel in scope | Annually | Workday |

### 9.2 Training Compliance and Tracking

The VP of Clinical AI is responsible for ensuring 100% training compliance for their team. The QMS team will generate a monthly non-compliance report from Workday. Any personnel non-compliant for more than 30 days shall have their access to PMS systems (ServiceNow, monitoring dashboards) temporarily suspended until training is completed.

---

## 10. Related Policies and References

### 10.1 Internal Meridian Policies

| SOP / Policy ID | Document Name | Business Unit |
|---|---|---|
| SOP-CLIN-012 | Clinical AI Model Lifecycle Management | Clinical AI Products |
| SOP-RD-004 | Design Control and Pre-Market Validation for AI/ML Devices | R&D |
| SOP-RM-003 | Risk Management for Software as a Medical Device | Quality & Regulatory |
| SOP-IT-022 | Cloud Platform Operational Monitoring | IT Operations |
| SOP-SEC-009 | Security Incident Response and PHI Breach Notification | Information Security |
| POL-LEG-001 | HIPAA Privacy and Security Rule Compliance Policy | Legal & Compliance |
| SOP-QLT-001 | Quality Management System (QMS) – Core Processes | Quality |

### 10.2 External Standards and Regulations

- EU Medical Device Regulation (MDR) 2017/745
- EU Artificial Intelligence Act
- HIPAA Privacy Rule (45 CFR Part 160 and Subparts A and E of Part 164)
- ISO 13485:2016 – Medical devices – Quality management systems
- ISO 14971:2019 – Medical devices – Application of risk management to medical devices

---

## 11. Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | 2021-05-15 | J. Millar (Former VP, QA) | Initial release. Established framework for PMS following first FDA clearance. |
| 2.3 | 2022-02-22 | K. Chen (Former PSM) | Major update. Added real-world performance monitoring section with automated drift detection; introduced Meridian AI Severity Scale replacing generic scale. |
| 3.5 | 2022-11-30 | Dr. A. Okafor | Minor revision. Updated roles and responsibilities to align with Clinical AI BU organizational change. Added clinical audit procedure with 200-encounter sample size. |
| 4.2 | 2023-08-14 | Dr. A. Okafor | Significant revision. Integrated Evidently AI monitoring tools. Updated FSCA procedure with post-fix verification period. Added KPI targets for process timeliness. |
| 5.0 | 2024-10-01 | M. Dubois (Clinical Ops Lead) & Dr. A. Okafor | Major QMS upgrade revision. Migrated to ServiceNow QMS Module for ticket tracking. Updated SDE forms, investigation templates, and reporting cadences to be quarterly. |
| 5.1 | 2024-12-04 | Dr. A. Okafor | Revised PHI breach notification procedure after consultation with CPO. Clarified that CPO evaluation and notification will proceed per standard legal review with the GC, without specifying fixed hourly timelines. Updated related document references. |