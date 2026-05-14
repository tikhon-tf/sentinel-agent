---
sop_id: "SOP-CLIN-007"
title: "Adverse Event Detection and Reporting"
business_unit: "Clinical AI Products"
version: "3.6"
effective_date: "2025-02-06"
last_reviewed: "2026-07-12"
next_review: "2027-01-22"
owner: "Dr. Aisha Okafor, VP of Clinical AI Products"
approver: "Dr. Priya Patel, Chief Medical Officer"
classification: "Internal"
regulations:
  - "EU AI Act"
  - "HIPAA"
status: "Active"
---

# Standard Operating Procedure: Adverse Event Detection and Reporting

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes a harmonized, enterprise-wide framework for the detection, assessment, classification, reporting, and root cause analysis of Adverse Events (AEs) arising from or potentially related to the use of Meridian Health Technologies’ Clinical AI Platform. The purpose of this document is to ensure patient safety, maintain regulatory compliance—with particular emphasis on the high-risk AI system obligations under the European Union Artificial Intelligence Act (EU AI Act)—and drive continuous improvement in our AI model lifecycle.

This SOP defines the operational rhythm and governance structures necessary to translate raw safety signals into actionable intelligence, ensuring that Meridian meets its serious incident reporting obligations, mitigates immediate patient harm, and prevents recurrence through systematic corrective and preventive actions (CAPA).

### 1.2 Scope

This SOP applies to all employees, contractors, Business Associates, and authorized third parties involved in the development, deployment, monitoring, clinical validation, and customer support of the Clinical AI Business Unit. The scope encompasses:

- **Products Covered:** All current and future clinical AI/ML models deployed under the Clinical AI Platform, including but not limited to diagnostic imaging analysis algorithms, patient risk scoring engines, adverse event prediction systems, and clinical decision support (CDS) tools. This includes models that have received FDA 510(k) clearance and CE marking under EU MDR, as well as those operating under quality system exemptions.
- **Geographic Applicability:** Global. Specific heightened controls apply to deployments within the European Union (governed by the EU AI Act) and deployments involving Protected Health Information (PHI) for covered entities.
- **Event Types:** Any actual or potential harm, injury, erroneous clinical output, malfunction, or deterioration in performance of an AI/ML model that could lead to patient safety risks, incorrect clinical decisions, or non-compliance with regulatory thresholds.

This SOP explicitly excludes adverse events related to medication therapy management (within the scope of SOP-PHARM-002) and workplace safety incidents (covered by SOP-HR-009).

### 1.3 Effective Date and Compliance

This version (3.6) supersedes all prior versions. Non-compliance with this SOP may result in disciplinary action up to and including termination and regulatory notification where legally mandated.

---

## 2. Definitions and Acronyms

### 2.1 Definitions

| Term | Definition |
| :--- | :--- |
| **Adverse Event (AE)** | Any untoward medical occurrence, unintended disease or injury, or untoward clinical signs in patients, users, or other persons, which may be associated with the use of a Meridian Clinical AI product. |
| **Serious Adverse Event (SAE)** | An AE that results in death, is life-threatening, requires inpatient hospitalization or prolongation of existing hospitalization, results in persistent or significant disability/incapacity, or necessitates medical or surgical intervention to prevent permanent impairment. |
| **Algorithmic Drift** | A statistically significant degradation in the performance metrics of a deployed AI model relative to its validated baseline, potentially leading to incorrect predictions or classifications. |
| **Near Miss** | An error or malfunction in the AI system that was detected and intercepted before causing patient harm. All Near Misses involving high-risk AI systems are treated as non-serious incidents for root cause analysis purposes. |
| **Serious Incident (EU AI Act)** | An incident or malfunction of a high-risk AI system that directly or indirectly leads to the death of a person or serious harm to a person’s health, property, or the environment. |
| **EU AI Act** | Regulation (EU) 2024/1689 of the European Parliament and of the Council laying down harmonised rules on artificial intelligence. |

### 2.2 Acronyms

| Acronym | Definition |
| :--- | :--- |
| AE | Adverse Event |
| CAPA | Corrective and Preventive Action |
| CDS | Clinical Decision Support |
| CMO | Chief Medical Officer |
| EU MDR | European Union Medical Device Regulation |
| FMEA | Failure Mode and Effects Analysis |
| RCA | Root Cause Analysis |
| SAE | Serious Adverse Event |
| SLA | Service Level Agreement |
| VP CAP | Vice President, Clinical AI Products |

---

## 3. Roles and Responsibilities

The following RACI matrix delineates responsibility for the lifecycle of an adverse event.

| Activity / Task | Clinical User / Reporter (I) | Tier 1 Support (R) | Clinical Safety Officer (C) | AI/ML Engineering (C) | VP of Clin. AI Prod. (A) | Chief Medical Officer (A) | Legal & Compliance (C) | Quality Assurance (I) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Initial AE Detection & Triage** | I | R/A | C | | I | | | I |
| **Severity Classification (SAE vs. AE)** | | I | R/A | C | I | C | C | I |
| **EU AI Act Serious Incident Determination** | | | R | C | C | A | C | |
| **Immediate Mitigation (Kill Switch)** | | R | C | R/A | | | | |
| **Mandatory Regulatory Reporting** | | I | R | C | A | C | R/A | I |
| **Root Cause Analysis (RCA)** | | | C | R | A | I | I | C |
| **CAPA Implementation & Closure** | | | I | R | A | I | I | R/A |
| **R = Responsible (Doer), A = Accountable (Approver), C = Consulted, I = Informed** | | | | | | | | |

---

## 5. Detailed Procedures

This section is divided into the operational phases of the Adverse Event lifecycle.

### 5.1 Phase 1: Detection and Intake

The AE process initiates when a potential safety signal is detected. Meridian utilizes three primary detection channels, monitored 24/7 by the Clinical Operations Command Center.

**5.1.1 Automated Model Monitoring (Primary)**
All production Clinical AI models are instrumented using the Meridian AI Guardrails platform (powered by Arize AI backend). An automated ticket is created in ServiceNow (category: `Clinical_AI_Adverse_Event`) if any of the following thresholds are breached:
- **Input Drift:** Population Stability Index (PSI) > 0.25 for any top-ten model feature over a rolling 24-hour window.
- **Output Drift:** The rate of "high-risk" clinical predictions changes by > 30% day-over-day without a corresponding environmental change ticket.
- **Concept Drift:** Accuracy against a delayed gold-standard label set drops > 5% from the validated baseline.
- **Hallucination Detector Alert:** For Large Language Model (LLM)-based CDS tools, the "Meridian Hallucination Guard" detects a Generation Disagreement Ratio (GDR) > 0.4, indicating inconsistent factual clinical guidance.

**5.1.2 User-Reported Complaints (Secondary)**
Clinicians or administrators can report an observed AE via the "Report a Safety Concern" button located in the clinical workflow header of the Meridian application. Upon submission, the form captures the session ID, patient context identifier (tokenized), the model output displayed, and the user’s free-text concern. A critical P1 ticket is auto-generated in ServiceNow.

**5.1.3 Proactive Clinical Review (Tertiary)**
Meridian’s Clinical Review Board (CRB) performs random quarterly audits of 100 anonymized patient encounters per deployed model. Any determination of a clinically significant erroneous output triggers a manual AE intake.

### 5.2 Phase 2: Triage and Severity Classification

Upon ticket creation, the Tier 1 Clinical Support Engineer has a **15-minute SLA** to acknowledge the event and begin triage. The purpose of triage is to assign a Severity Level to direct the urgency of the investigation and escalation.

**5.2.1 Severity Level Definitions**
The classification matrix is based on the Anderson & Sweeney clinical risk taxonomy adapted for algorithmic harm.

| Severity | Classification Criteria | Clinical Impact | Regulatory Trigger |
| :--- | :--- | :--- | :--- |
| **S1 (Critical)** | Death or serious injury; EU AI Act Serious Incident; permanent harm requiring major intervention. | Irreversible patient harm | Immediate notification to authorities required (see Phase 5). |
| **S2 (Major)** | Temporary major incapacitation; incorrect surgical/pharmacological intervention triggered; hospitalization extended > 24h. | Significant reversible harm | Mandatory reporting via Post-Market Surveillance (PMS) update. |
| **S3 (Moderate)** | Erroneous output necessitated additional unnecessary diagnostic testing (labs, imaging); minor medical intervention. | Mitigated harm | Internal CAPA required. |
| **S4 (Minor)** | Inconvenience or transient alarm; output error resulted in no clinical interaction or was ignored/overridden safely. | No clinical impact | Monitored for trend analysis. |
| **S0 (Near Miss)** | Error that would have led to harm if not intercepted. | No actual harm | Trended; high-recurrence Near Misses escalate to RCA. |

The classification must be reviewed and countersigned by the on-call Clinical Safety Officer (CSO) within **60 minutes** for S1/S2 events. It is the responsibility of the CSO to formally declare an EU AI Act "Serious Incident."

### 5.3 Phase 3: Containment and Immediate Mitigation

Containment actions are non-negotiable for any S1 or S2 event to prevent further potential harm.

**5.3.1 Model Circuit Breaker (Kill Switch)**
The VP of Clinical AI Products (or designated delegate) holds the sole authorization to execute the "Model Circuit Breaker" protocol.
1.  **Assessment:** The VP collaborates with the CSO to assess if the harm is model-specific or systemic.
2.  **Execution:** Using the Meridian "ModelOps Hub," the authorized individual executes the "Suspend Inference" command for the specific Model GUID. This reroutes all API calls to a "Graceful Degradation" state, displaying a message that the AI consultation is temporarily unavailable and escalating the case to a manual review by a human specialist.
3.  **Notification:** Broadcast an emergency bulletin via PagerDuty and Slack (`#clinical-ops-critical`) containing the suspended Model GUID, the reason for suspension, and the estimated time for next update.

**5.3.2 Patient Safety Protocol**
For any S1 event potentially impacting patient health, the Clinical Safety Officer must—**within 15 minutes of classification**—draft and send a "Clinical Safety Advisory" to all potentially impacted clinical site administrators, providing de-identified findings and recommended clinical actions (e.g., review all AI-assisted interpretations from a specific shift).

### 5.4 Phase 4: Root Cause Analysis (RCA)

An RCA is mandatory for all S1, S2, and recurring S3 events. The VP of Clinical AI Products convenes a cross-functional RCA team within **1 business day** of an S1/S2 event.

**5.4.1 RCA Procedure**
The team utilizes the Ishikawa (Fishbone) method combined with a Failure Mode and Effects Analysis (FMEA) to identify the point of failure within the AI lifecycle. The analysis must cover the "Meridian 4 Pillars":
1.  **Data Error:** Lookback at data pipelines (Apache Airflow). Was there a bad batch, schema change, or upstream data corruption in Snowflake? Verify data lineage using Monte Carlo log entries.
2.  **Model Drift:** Quantify the difference between the expected model behavior (baseline stored in MLflow Registry) and the observed behavior at the time of the event. Utilize the "AI Guardrails" drift logs.
3.  **Clinical Workflow:** Analyze the human-computer interaction (IHCI). Did the user ignore a valid CDS alert due to alert fatigue? Was the UX ambiguous in communicating confidence scores?
4.  **Infrastructure Failure:** Review Datadog traces. Was there a container crash, network failure, or latency spike in the model serving layer (Seldon Core / Triton Inference Server) that caused a timeout or partial output?

**5.4.2 RCA Report**
A formal RCA Report must be completed within **5 business days** for S1 events and **10 business days** for S2 events. The report must conclude with a specific, actionable Corrective and Preventive Action (CAPA) plan, documented in MasterControl.

### 5.5 Phase 5: Regulatory and External Reporting

Timely regulatory notification is a core Meridian obligation, with specific rigor applied under the EU AI Act.

**5.5.1 EU AI Act Serious Incident Reporting (Article 73)**
For deployments of high-risk AI systems in the European Union, Meridian strictly adheres to the serious incident reporting obligations.
- **Timeline:** A report shall be filed with the relevant National Supervisory Authority (NSA) and the appointed notified body **immediately, and no later than 15 calendar days** after Meridian becomes aware of a serious incident. Where a delay is unavoidable, an initial summary report must be filed within 15 days, explaining the reason for the delay.
- **Method:** Filing shall be completed using the harmonized EU Serious Incident Report Form, submitted via the EU Database for High-Risk AI Systems (as referenced in Article 71).
- **Content:** The report shall include a detailed timeline of the incident, an assessment of the malfunction or nature of the harm, the corrective actions taken (including model suspension), root cause analysis (preliminary), and the measures to prevent recurrence.

**5.5.2 Post-Market Surveillance (PMS) Updates**
Per Meridian’s CE marking obligations under EU MDR, all AEs classified as S2 (Major) and above shall trigger a prompt update to the Post-Market Surveillance Report for the relevant device. Trend reports of S3 and S4 events shall be consolidated in Periodic Safety Update Reports (PSURs).

---

## 6. Controls and Safeguards

Meridian implements the following administrative and technical controls to ensure the integrity of the AE Lifecycle.

### 6.1 Technical Controls

| Control ID | Control Description | Tool/Configuration |
| :--- | :--- | :--- |
| **CT-101** | **Automated Drift Detection:** Real-time monitoring compares live inference distributions against the champion model stored in the Feature Store (Tecton/Tecton.ai). | Arize AI backend, custom Python scripts polling MLflow. |
| **CT-102** | **Immutable Audit Trail:** All AE tickets, severity classifications, and containment actions are logged with non-repudiable signatures. | ServiceNow (Change Management Module), Coralogix for raw log shipping. |
| **CT-103** | **Synthetic Data Injection:** The Quality team randomly injects known faulty synthetic patient scenarios into the production pipeline (via a dedicated "QA Patient" facility) to verify that detection mechanisms fire correctly. | Automated testing suite (Selenium), Jenkins pipeline triggering ServiceNow API. |
| **CT-104** | **PHI Tokenization Gateway:** User-reported safety forms do not transmit raw PHI into the ticketing system. The Meridian API Gateway intercepts patient names/MRNs and replaces them with a token. Only internal re-identification is performed strictly on a need-to-know basis for investigation. | Kong API Gateway, custom Tokenization microservice. |

### 6.2 Administrative Controls

| Control ID | Control Description | Implementation |
| :--- | :--- | :--- |
| **CA-201** | **Segregation of Duties:** The Tier 1 support engineer who creates the initial ticket cannot approve the severity classification. The CSO who classifies the severity cannot authorize the final CAPA closure. | Enforced via ServiceNow workflows and role-based groups. |
| **CA-202** | **CAPA Verification:** All CAPA actions require objective evidence of completion before closure request. Evidence must be validated by an independent Quality Assurance representative. | MasterControl CAPA module. |
| **CA-203** | **Mandatory Model Retraining Gate:** The RCA for any S1 or S2 event must include a formal justification if the model is retrained and re-deployed without an additional human-in-the-loop evaluation stage. | Standard is forced human-prospective evaluation; waivers require CMO signature. |

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs)

To measure the effectiveness of this SOP, the Clinical Operations team tracks the following quantitative thresholds:

| Metric ID | KPI | Target Threshold | Measurement Tool |
| :--- | :--- | :--- | :--- |
| **KPI-AE-01** | Mean Time to Acknowledge (MTTA) P1 Events | < 15 minutes | ServiceNow Dashboard |
| **KPI-AE-02** | Mean Time to Classify (MTTC) | < 45 minutes | Custom PowerBI Report |
| **KPI-AE-03** | Mean Time to Contain (MTTCo) for S1/S2 | < 2 hours | ModelOps Hub Audit Logs |
| **KPI-AE-04** | RCA Report On-Time Delivery | > 95% for 5/10-day deadlines | MasterControl CAPA Workflow |
| **KPI-AE-05** | EU AI Act Serious Incident Reporting On-Time | 100% within 15 calendar days | Legal & Compliance Tracker |
| **KPI-AE-06** | Near Miss to Adverse Event Ratio | Monitor trend; ratio should not degrade > 10% QoQ | Safety Event Database |

### 7.2 Reporting Cadence

- **Daily:** A "System Safety Dashboard" report is pushed to the VP of Clinical AI Products and Chief Medical Director summarizing open S1/S2 tickets and containment statuses.
- **Monthly:** A "Closed AE & RCA Effectiveness Review" is conducted with Legal, Quality, and Engineering to review closed CAPAs and identify any recurrent failure patterns.
- **Quarterly:** A comprehensive "Clinical AI Safety Analysis" report is presented to the C-Suite, including trend analysis of PSI drift, Near Miss rates, and compliance with EU AI Act PMS requirements.

---

## 8. Exception Handling and Escalation

### 8.1 Exception Process

Strict adherence to mandated timelines is required. Any anticipated deviation from reporting or RCA deadlines requires a formally documented Exception Request (ER). The ER must be raised **before** the deadline breach.

### 8.2 Exception Workflow

1.  **Requestor:** The individual unable to meet the SOP timeline submits an ER in ServiceNow, citing the specific SOP section, the reason for the delay, the impact on the investigation, and a proposed new "committed date."
2.  **Initial Review:** The immediate Manager reviews the ER for technical validity and resource justification.
3.  **Final Approval Matrix:**
    - For extensions up to 24 hours: Approval by the Clinical Safety Officer.
    - For extensions up to 5 business days: Approval by the VP of Clinical AI Products.
    - For any extension to a regulatory reporting deadline (e.g., EU AI Act 15-day window): Approval by the **Chief Medical Officer and Chief Legal Counsel** is mandatory. No exception is valid if it contravenes explicit statutory deadlines.

### 8.3 Escalation Path

If a containment action (e.g., model circuit breaker) is contested or delayed, the CSO has the hierarchical escalation path:
1.  VP of Clinical AI Products.
2.  Chief Medical Officer.
3.  Meridian Emergency Incident Management Team (EIMT) — activated for any event S1 in severity.

---

## 9. Training Requirements

### 9.1 Initial Role-Based Training

All personnel involved in the Clinical AI lifecycle must complete mandatory training prior to being granted access to production systems, ServiceNow queues, or clinical dashboards.

| Training Module Code | Module Description | Target Audience | Passing Score |
| :--- | :--- | :--- | :--- |
| **T-CLIN-SAF-101** | Adverse Event Detection & the Human-in-the-Loop | All Clinical Staff, Tier 1 Support | 90% |
| **T-CLIN-SAF-102** | SAE Classification & EU AI Act Obligations | Clinical Safety Officers, Legal, QA | 100% |
| **T-CLIN-SAF-103** | Model Containment (Kill Switch) Technical Drill | AI/ML Engineering, DevOps | 95% |
| **T-CLIN-SAF-104** | Conducting Blameless AI RCAs | Engineering Managers, Senior Staff | 85% |

### 9.2 Recurring Cadence

- **Annual Refresh:** The `T-CLIN-SAF` curriculum is updated annually to incorporate new product features and regulatory updates. Completion is mandatory and tracked via Workday Learning.
- **Semiannual Drills:** The emergency kill switch procedure is drilled semiannually in a staging environment. A drill report, including time-to-kill metric, is published to the C-Suite.

---

## 10. Related Policies and References

This SOP is not a standalone document. It must be read in conjunction with:

### 10.1 Internal Meridian SOPs
- **SOP-QS-001:** CAPA Management (MasterControl Workflow)
- **SOP-CLIN-004:** Clinical Risk Scoring Model Lifecycle
- **SOP-GOV-002:** AI Model Governance and Algorithmic Auditing
- **SOP-INF-009:** Change Management for Production Infrastructure
- **SOP-GRC-001:** Global Regulatory Intelligence Management

### 10.2 External Standards and Regulatory References
- **EU AI Act (Regulation 2024/1689):** Particularly Articles 9 (Risk Management System), 61 (Post-market monitoring), 62 (Reporting of serious incidents), 71 (EU database), and 73 (Reporting obligations).
- **ISO 13485:2016:** Medical devices — Quality management systems.
- **IMDRF/NCAR:** International Medical Device Regulators Forum / National Competent Authority Report exchange criteria.
- **AAMI/ISO TIR34971:** Guidance on the application of ISO 14971 to machine learning.

---

## 11. Revision History

| Version | Effective Date | Author | Summary of Changes |
| :--- | :--- | :--- | :--- |
| 1.0 | 2023-04-15 | Dr. J. Miller (former VP) | Initial creation of AE Detection SOP. Manual reporting only. |
| 2.1 | 2023-11-01 | S. Lee (QA Manager) | Added automated detection channel (AI Guardrails v1). Updated triage SLA to 30 min. |
| 2.3 | 2024-01-20 | L. Chen (Legal) | Minor revisions to align with early drafts of EU AI Act. Introduced "Serious Incident" concept. |
| 3.1 | 2024-05-30 | Dr. A. Okafor | Major revision. Updated classification matrix to S0-S4. Integrated Model Circuit Breaker protocol. Aligned fully with finalized EU AI Act Article 73 reporting timelines. |
| 3.4 | 2024-10-18 | M. Gupta (Compliance) | Clarified roles for RCA approval. Updated RACI matrix for Legal involvement. |
| **3.6** | **2025-02-06** | **Dr. A. Okafor** | **Strengthened EU AI Act 15-day timeline for serious incident reports. Updated technical controls to reflect new Arize AI monitoring backend. Added quarterly CRB proactive review. Mandatory training modules updated.** |