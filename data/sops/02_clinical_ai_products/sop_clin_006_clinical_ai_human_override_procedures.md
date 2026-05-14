---
sop_id: "SOP-CLIN-006"
title: "Clinical AI Human Override Procedures"
business_unit: "Clinical AI Products"
version: "5.8"
effective_date: "2025-05-21"
last_reviewed: "2026-08-04"
next_review: "2027-02-05"
owner: "Dr. Aisha Okafor, VP of Clinical AI Products"
approver: "Dr. Priya Patel, Chief Medical Officer"
classification: "Internal"
regulations:
  - "EU AI Act"
  - "HIPAA"
  - "NIST AI RMF"
status: "Active"
---

# Standard Operating Procedure: Clinical AI Human Override Procedures

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the governing framework for clinician-initiated overrides of Clinical AI Platform outputs across all Meridian Health Technologies deployments. The document codifies the processes, controls, and accountability mechanisms that enable qualified clinical professionals to exercise independent medical judgment when interacting with AI-driven clinical decision support tools, diagnostic imaging analysis, patient risk scoring, and adverse event prediction systems.

The fundamental principle underlying this SOP is that Meridian's Clinical AI Platform serves as an augmentation to—not a replacement for—clinical expertise. The override mechanism constitutes the formal recognition that artificial intelligence systems, regardless of their sophistication, operate within constraints of training data, algorithmic limitations, and contextual boundaries that necessitate human oversight.

### 1.2 Scope

This SOP applies to the following systems, products, and personnel:

**Systems and Products in Scope:**
| System | Product Code | Deployment Count | Regulatory Classification |
|--------|--------------|------------------|---------------------------|
| Clinical Decision Support Engine | CDS-2023-A | 312 hospitals | EU AI Act High-Risk; FDA Class II |
| Diagnostic Imaging Analysis Suite | DIA-2024-B | 287 hospitals | EU AI Act High-Risk; FDA 510(k) Cleared |
| Patient Risk Stratification Module | PRS-2023-C | 340 clinics | EU AI Act High-Risk |
| Adverse Event Prediction System | AEP-2024-D | 198 hospitals | EU AI Act High-Risk |
| Medication Interaction Analyzer | MIA-2025-A | 256 hospitals | EU AI Act High-Risk |

**Personnel in Scope:**
- All licensed physicians, nurse practitioners, and physician assistants with active clinical privileges at Meridian-deployed facilities
- Clinical pharmacists authorized to review AI-generated medication recommendations
- Radiologists and pathologists interpreting AI-annotated diagnostic images
- Clinical department chairs and medical directors with supervisory authority
- Meridian Clinical Support Specialists (tier 2 and tier 3 support)
- Meridian Clinical AI Safety Monitoring team

**Geographic Scope:** All deployments across North America and European Union member states.

**Out of Scope:**
- Administrative overrides of non-clinical system configurations
- Emergency system shutdowns (covered under SOP-IT-042 "Emergency System Decommissioning")
- Patient-initiated data corrections (covered under SOP-PRIV-018 "Patient Data Amendment Requests")
- Research and development environments operating under IRB-approved protocols

---

## 2. Definitions and Acronyms

### 2.1 Definitions

| Term | Definition |
|------|------------|
| **Clinical Override** | The deliberate action by a qualified clinician to reject, modify, or disregard one or more AI-generated outputs in favor of an alternative clinical assessment, decision, or course of action. |
| **Override Event** | A discrete instance of clinical override, encompassing the triggering conditions, the clinician's alternative determination, and the associated metadata captured at the point of override. |
| **Override Audit Trail** | The complete, immutable record of an override event, including timestamp, clinician identity, patient context, AI output rejected, alternative clinical decision, and clinical rationale. |
| **Qualified Clinician** | A licensed medical professional holding active, unrestricted credentials at the deploying institution and having completed Meridian Clinical AI Platform training per SOP-TRN-024. |
| **Concurrent Override** | An override executed at the time of AI output delivery, prior to clinical action being taken. |
| **Retrospective Override** | An override identified after clinical action based on AI output has been initiated, requiring corrective intervention. |
| **Override Rate** | The percentage of AI-generated recommendations that are overridden by clinicians, calculated per module, per facility, and per clinician. |
| **Override Justification** | The structured clinical rationale provided by the overriding clinician, selected from a standardized taxonomy with optional free-text elaboration. |
| **Silent Override** | An override executed without proper documentation in the Meridian platform, identified through retrospective reconciliation with EHR systems. Silent overrides constitute a compliance violation. |
| **Override Threshold** | The pre-defined statistical boundary at which an override rate triggers automatic review under the escalation procedures defined in Section 8. |

### 2.2 Acronyms

| Acronym | Definition |
|---------|------------|
| AI | Artificial Intelligence |
| CDS | Clinical Decision Support |
| CMO | Chief Medical Officer |
| DIA | Diagnostic Imaging Analysis |
| EHR | Electronic Health Record |
| EU AI Act | European Union Artificial Intelligence Act (Regulation 2024/1689) |
| FMEA | Failure Mode and Effects Analysis |
| GDPR | General Data Protection Regulation (EU 2016/679) |
| HIPAA | Health Insurance Portability and Accountability Act |
| MDR | Medical Device Regulation (EU 2017/745) |
| ML | Machine Learning |
| NIST AI RMF | National Institute of Standards and Technology Artificial Intelligence Risk Management Framework |
| PHI | Protected Health Information |
| SAQ | Structured Assessment Questionnaire |
| SLA | Service Level Agreement |
| SOP | Standard Operating Procedure |

---

## 3. Roles and Responsibilities

### 3.1 Responsibility Assignment Matrix

The following RACI matrix delineates accountability for all override-related activities:

| Activity | Clinician | Clinical Dept Chair | Meridian Clinical Support | Clinical AI Safety Team | Chief Medical Officer | VP Clinical AI Products | Compliance Officer |
|----------|-----------|---------------------|--------------------------|------------------------|----------------------|------------------------|-------------------|
| Executing Clinical Override | R, A | I | I | I | I | I | I |
| Documenting Override Justification | R, A | C | I | I | I | I | I |
| Reviewing Departmental Override Patterns | I | R, A | C | C | I | I | C |
| Investigating High Override Rates (>15%) | I | C | C | R, A | I | C | I |
| Approving Override Taxonomy Updates | I | C | I | R | A | R | I |
| Executing Model Retraining Decisions | I | I | I | C | A | R | I |
| Reporting to Regulatory Bodies | I | I | I | C | R | C | A |
| Performing Silent Override Audits | I | I | C | R | I | I | A |
| Escalating Patient Safety Concerns | R | R | C | C | A | I | I |
| Maintaining Override System Functionality | I | I | R, A | C | I | C | I |

**Legend:** R = Responsible (executes); A = Accountable (approves); C = Consulted; I = Informed

### 3.2 Role Descriptions

**3.2.1 Clinician (Override Executor)**
The licensed medical professional who directly interacts with Clinical AI Platform outputs and exercises override authority. Clinicians bear primary responsibility for the clinical appropriateness of their override decisions and must document justification contemporaneously with the override action. Clinicians must complete mandatory override procedure training per Section 9 prior to being granted override privileges.

**3.2.2 Clinical Department Chair**
The supervising physician or administrator responsible for monitoring override patterns within their department. Department chairs receive monthly override reports and must conduct quarterly reviews of override trends. Chairs have authority to require peer review of override decisions exceeding established thresholds.

**3.2.3 Meridian Clinical Support Team (Tiers 2 and 3)**
Technical and clinical specialists responsible for maintaining override system functionality, investigating override-related system anomalies, and providing frontline support for override documentation workflows. Tier 3 specialists include board-certified physicians who can adjudicate override-related disputes.

**3.2.4 Clinical AI Safety Monitoring Team**
A dedicated cross-functional team reporting to the Chief Medical Officer with responsibility for continuous monitoring of override patterns, identification of potential model degradation signals, and initiation of model performance investigations. This team includes biostatisticians, clinical informaticists, and patient safety specialists.

**3.2.5 Chief Medical Officer (Dr. Priya Patel)**
The executive accountable for clinical safety of all Meridian AI products. The CMO approves override policy changes, reviews escalated patient safety override events, and serves as the clinical authority for regulatory communications regarding override governance.

**3.2.6 VP of Clinical AI Products (Dr. Aisha Okafor)**
The executive responsible for product-level override mechanisms, override taxonomy maintenance, and coordination between clinical safety findings and product engineering responses.

**3.2.7 Compliance Officer**
Responsible for ensuring override documentation meets regulatory requirements, conducting periodic silent override audits, and managing regulatory reporting related to override governance.

---

## 4. Policy Statements

### 4.1 Foundational Policies

**POL-CLIN-006-01: Primacy of Clinical Judgment**
Meridian Health Technologies affirms that qualified clinicians retain ultimate authority over all patient care decisions. No AI-generated output shall constrain, limit, or predetermine a clinician's professional judgment. The override mechanism is an inherent feature—not an exception—of the Clinical AI Platform architecture.

**POL-CLIN-006-02: Mandatory Override Documentation**
Every clinical override event, regardless of materiality or clinical context, shall be documented in the Meridian Override Registry contemporaneously with the override action. Undocumented overrides ("silent overrides") constitute a violation of this SOP and shall be subject to the escalation procedures defined in Section 8.

**POL-CLIN-006-03: Override Transparency**
All override events shall generate an auditable record accessible to the overriding clinician, their departmental supervisory chain, Meridian Clinical AI Safety Monitoring team, and authorized compliance personnel. Patients shall be informed of substantive AI output modifications through existing informed consent frameworks, consistent with institutional policies. Meridian's platform provides generic transparency notifications to EHR systems regarding the use of AI-assisted clinical decision support.

**POL-CLIN-006-04: Non-Retaliation**
Meridian strictly prohibits any adverse employment action, privileging consequence, or professional sanction against any clinician solely on the basis of override frequency, provided such overrides are properly documented and executed in good faith clinical judgment. Override patterns triggering investigation shall be evaluated for clinical appropriateness, not as presumptive evidence of improper conduct.

**POL-CLIN-006-05: Continuous Safety Monitoring**
Override events constitute critical safety signals. Meridian shall maintain continuous automated surveillance of override patterns across all deployments to detect potential model degradation, training data drift, or systematic clinical disagreement requiring model retraining or deployment modification.

**POL-CLIN-006-06: Regulatory Compliance**
All override procedures, documentation, and retention practices shall comply with applicable regulations including but not limited to the EU AI Act, HIPAA, GDPR, FDA requirements for AI/ML-based Software as a Medical Device (SaMD), and EU MDR requirements for CE-marked clinical AI products.

**POL-CLIN-006-07: Human Oversight Commitment**
Meridian maintains human oversight capability across all Clinical AI Platform deployments. Clinical personnel are stationed at each deployment site and are accessible during operational hours to review override decisions. The platform includes mechanisms for human review of override patterns at aggregate and individual levels.

---

## 5. Detailed Procedures

### 5.1 Concurrent Override Procedure (Real-Time Clinical Decision Support)

This procedure applies when a clinician reviews AI-generated recommendations at the point of care and elects to override prior to initiating clinical action.

#### 5.1.1 Step-by-Step Process

**Step 1: AI Output Review**
The clinician accesses AI-generated outputs through the Meridian Clinical Workbench interface (MCW-2024.2 or later). The platform displays:
- Primary AI recommendation with confidence score
- Top three alternative recommendations (if applicable) with confidence scores
- Reference evidence citations supporting the recommendation
- Patient-specific factors considered by the model
- Model version and last validation date

**Step 2: Override Decision**
Upon determining that the AI output requires modification or rejection, the clinician selects the "Initiate Override" button adjacent to the specific output being overridden. The system captures:
- The specific AI output identifier (Output-ID)
- The module generating the output
- Timestamp (UTC, with local time displayed)
- Patient encounter context
- Clinician identity (from SSO/EHR integration)
- Clinical context (diagnosis codes, medications, lab values active at time of recommendation)

**Step 3: Override Justification Selection**
The clinician must select a primary override justification from the Standardized Override Taxonomy (see Section 5.1.2). Selection of the primary justification is mandatory; the system will not accept an override without this selection. The clinician may optionally select up to three contributing justifications and provide free-text elaboration (limited to 500 characters).

**Step 4: Alternative Clinical Assessment Entry**
The clinician enters the alternative clinical decision, selected from a context-sensitive dropdown populated based on the clinical domain (e.g., alternative medication, alternative diagnosis, alternative risk score). The system requires:
- Primary alternative determination (mandatory)
- Clinical basis for alternative (free-text, minimum 50 characters, maximum 1000 characters)
- Expected patient outcome differential (optional but encouraged)

**Step 5: Clinical Verification**
The platform displays a summary screen showing:
- Original AI output
- Clinician's override determination
- Selected justification(s)
- Free-text rationale
- Warning: "You are overriding an AI-generated clinical recommendation. Your override will be permanently recorded in the patient's clinical record and the Meridian Override Registry. You are confirming that this override reflects your independent professional clinical judgment."

The clinician must acknowledge this warning by selecting "Confirm Override — I Accept Clinical Responsibility."

**Step 6: Documentation and Integration**
Upon confirmation:
- The override record is written immutably to the Meridian Override Registry (AuroraDB cluster, multi-region replication)
- The override is transmitted to the facility's EHR system via HL7 FHIR R4 Override resource
- The patient's clinical record reflects the clinician's alternative determination as the active order/recommendation
- The AI output remains visible as an overridden historical entry with clear visual demarcation (strikethrough display with timestamp of override)

**Step 7: Post-Override Monitoring Trigger**
For overrides classified under Justification Codes J-01 through J-04 (patient safety concern categories; see Section 5.1.2), the system automatically generates a Clinical Safety Monitoring ticket in the Meridian Safety Event Tracking System (SETS) for review within 24 hours.

#### 5.1.2 Standardized Override Justification Taxonomy

The following taxonomy shall be used for all override documentation. The taxonomy is maintained by the Clinical AI Safety Monitoring Team with annual review and approval by the Chief Medical Officer.

| Code | Category | Justification | Auto-Review Trigger |
|------|----------|---------------|---------------------|
| **Clinical Disagreement** ||||
| CD-01 | Clinical Disagreement | Clinician disagrees with AI risk stratification level | No |
| CD-02 | Clinical Disagreement | Clinician identifies alternative diagnosis with higher clinical suspicion | No |
| CD-03 | Clinical Disagreement | Clinician selects alternative medication based on patient-specific factors | No |
| CD-04 | Clinical Disagreement | Clinician determines AI recommendation is contraindicated per clinical guidelines | Yes |
| CD-05 | Clinical Disagreement | Clinician identifies drug-drug interaction not flagged by AI | Yes |
| **Incomplete Patient Context** ||||
| PC-01 | Patient Context | AI recommendation does not account for documented patient allergy | Yes |
| PC-02 | Patient Context | AI recommendation does not account for patient social determinants of health | No |
| PC-03 | Patient Context | AI recommendation does not account for patient treatment preferences | No |
| PC-04 | Patient Context | AI recommendation does not account for recent clinical changes not yet in EHR | No |
| PC-05 | Patient Context | AI recommendation does not account for comorbidities documented in problem list | No |
| **Model Limitation** ||||
| ML-01 | Model Limitation | AI confidence score below acceptable clinical threshold (<60%) | Yes |
| ML-02 | Model Limitation | Clinician has observed pattern of similar AI errors in this domain | Yes |
| ML-03 | Model Limitation | AI recommendation contradicted by recent high-quality evidence | No |
| ML-04 | Model Limitation | AI recommendation outside locally accepted standard of care | No |
| **Safety Concern** ||||
| J-01 | Patient Safety | AI recommendation would cause immediate patient harm if followed | Yes |
| J-02 | Patient Safety | AI recommendation would cause probable patient harm if followed | Yes |
| J-03 | Patient Safety | AI recommendation involves contraindicated medication for this patient | Yes |
| J-04 | Patient Safety | AI recommendation exceeds safe dosing parameters | Yes |
| **Technical Issue** ||||
| TI-01 | Technical | System performance degradation affecting output timeliness | No |
| TI-02 | Technical | AI output display error (truncation, formatting corruption) | No |

### 5.2 Retrospective Override Procedure (Post-Action Correction)

This procedure applies when a clinician or supervisory physician identifies that clinical action was taken based on an AI recommendation that should have been overridden, but the override was not performed concurrently.

#### 5.2.1 Step-by-Step Process

**Step 1: Detection and Notification**
Upon identification (via clinical rounds, case review, adverse event investigation, or automated monitoring), the identifying clinician shall immediately:
- Assess for patient harm or potential harm
- Initiate appropriate clinical corrective actions
- Document the identification event in the facility's incident reporting system per institutional policy
- Notify the Meridian Clinical Support Team via the Priority Safety Hotline (available 24/7/365 at +1-833-MER-SAFE or EU +49-30-MER-SAFE)

**Step 2: Retrospective Override Documentation**
Within 4 hours of detection, the responsible clinician or supervising physician shall complete the retrospective override documentation:
- Access the Meridian Clinical Workbench
- Navigate to Patient Encounter → AI Recommendations → "Record Retrospective Override"
- The system will display all AI recommendations active at the time of the original clinical action
- Select the AI recommendation(s) that should have been overridden
- Complete override justification per the Standardized Taxonomy (Section 5.1.2)
- Indicate whether patient harm occurred or was averted:
  - Category A: No harm, no potential harm (override disagreement only)
  - Category B: Potential harm averted (override action taken before patient impact)
  - Category C: Actual harm — minor (temporary, reversible)
  - Category D: Actual harm — moderate (requiring intervention)
  - Category E: Actual harm — severe (permanent impairment or death)

**Step 3: Clinical Corrective Action Documentation**
For Categories B through E, the clinician shall additionally document:
- The clinical corrective actions taken
- Current patient status
- Whether the AI recommendation contributed causally to the adverse outcome
- Recommendations for system-level corrective action

**Step 4: Mandatory Reporting Escalation**
The Clinical AI Safety Monitoring Team shall review all retrospective overrides within 24 hours. For Category D and E events, the CMO and Compliance Officer shall be immediately notified (within 2 hours), and regulatory reporting assessments shall commence per SOP-COMP-031 "Adverse Event Regulatory Reporting."

### 5.3 Override Reconciliation and Silent Override Detection

Meridian conducts systematic reconciliation between Clinical AI Platform outputs and EHR clinical actions to detect undocumented overrides.

#### 5.3.1 Reconciliation Process

**Frequency:** Weekly, automated; Monthly, manual verification

**Data Sources:**
- Meridian Clinical AI Platform Override Registry
- Facility EHR data feed (HL7 FHIR Order, MedicationRequest, and ClinicalImpression resources)
- Facility billing/claims data (ICD-10, CPT, HCPCS codes)

**Reconciliation Algorithm:**
1. Identify all AI-generated recommendations logged in the Meridian platform
2. Trace each recommendation to EHR clinical orders placed within 60 minutes of AI output display
3. Classify congruence:
   - **Fully Congruent:** EHR order matches AI recommendation exactly
   - **Partially Congruent with Documented Override:** EHR order differs from AI recommendation; documented override record exists matching the alternative determination
   - **Partially Congruent without Documented Override:** EHR order differs from AI recommendation; no override record found → **FLAG for Silent Override Investigation**
   - **Unrelated Action:** No EHR order corresponds temporally to the AI recommendation (clinician did not act on the recommendation; no override required)
4. For flagged potential silent overrides, the Compliance Officer initiates investigation within 5 business days per SOP-COMP-015 "Compliance Investigation Procedures."

### 5.4 Multi-Clinician Override Scenarios

In situations where multiple clinicians interact with the same AI output (e.g., care team huddles, multidisciplinary rounds), the following procedures apply:

**5.4.1 Attending Physician Primacy**
The attending physician of record holds override authority. If the attending overrides an AI recommendation, the override is documented under their identity regardless of team input.

**5.4.2 Disagreement with Override**
If another licensed clinician on the care team disagrees with an override decision:
- The disagreeing clinician may document their disagreement via the "Add Clinical Annotation" function (not an override)
- The annotation is visible to the attending but does not modify the override record
- In emergency patient safety situations, the disagreeing clinician may escalate per Section 8.2

---

## 6. Controls and Safeguards

### 6.1 Technical Controls

| Control ID | Control Description | Implementation | Verification Method |
|------------|---------------------|----------------|---------------------|
| TEC-CLIN-006-01 | Immutable Override Registry | AuroraDB with append-only transaction log and cryptographic hashing (SHA-256) of each override record | Quarterly audit by Information Security; continuous integrity verification |
| TEC-CLIN-006-02 | Clinician Identity Verification | Multi-factor authentication required for override initiation; biometric (fingerprint or facial recognition) option for high-acuity settings | Monthly MFA compliance report; annual penetration testing |
| TEC-CLIN-006-03 | Timeout and Session Management | Override sessions automatically timeout after 5 minutes of inactivity; override documentation in progress is NOT saved as draft (security measure) | Quarterly session management review |
| TEC-CLIN-006-04 | Override Rate Threshold Alerting | Automated alert generation when facility-level override rate exceeds 15% or clinician-level override rate exceeds 25% (per module) | Monthly threshold tuning review |
| TEC-CLIN-006-05 | Silent Override Detection | Weekly reconciliation batch process comparing AI outputs to EHR clinical decisions | Monthly reconciliation accuracy audit |
| TEC-CLIN-006-06 | FHIR AuditEvent Integration | All override events transmitted to facility audit repositories using HL7 FHIR AuditEvent resource per IHE ATNA profile | Quarterly interface validation |
| TEC-CLIN-006-07 | Geographic Data Residency | EU clinician override data stored exclusively in Frankfurt region (AWS eu-central-1); North American data in us-east-1 and us-west-2 | Continuous monitoring via AWS Config rules |

### 6.2 Administrative Controls

| Control ID | Control Description | Frequency | Responsible Role |
|------------|---------------------|-----------|------------------|
| ADM-CLIN-006-01 | Override Privilege Verification | Monthly | Credentialing Office (facility) |
| ADM-CLIN-006-02 | Justification Taxonomy Review | Annually (or ad-hoc upon regulatory change) | VP Clinical AI Products + CMO |
| ADM-CLIN-006-03 | Override Pattern Peer Review | Quarterly (departments with >15% aggregate override rate) | Clinical Department Chair |
| ADM-CLIN-006-04 | Regulatory Compliance Audit | Semi-annually | Compliance Officer + External Auditor |
| ADM-CLIN-006-05 | Model Retraining Trigger Review | Monthly (review of override patterns correlated with model performance) | Clinical AI Safety Team |
| ADM-CLIN-006-06 | Override Registry Access Audit | Quarterly | Information Security + Privacy Officer |
| ADM-CLIN-006-07 | Clinician Override Competency Assessment | Annually | Clinical Education Department |

### 6.3 Override System Access Controls

Access to the Override Registry is strictly governed by role-based access control:

| Role | Read Access | Write Access | Export Access | Bulk Query |
|------|-------------|--------------|---------------|------------|
| Clinician (Own Overrides) | Full | Full | Yes | No |
| Clinician (Peer Overrides within Department) | Anonymized only | No | No | No |
| Department Chair | Full (dept) | No | Yes | Yes (dept only) |
| Clinical AI Safety Team | Full | No (read-only) | Yes | Yes |
| CMO | Full | Yes (corrections only) | Yes | Yes |
| Compliance Officer | Full | No | Yes | Yes |
| Information Security | Metadata only | No | No | Yes |
| Product Engineering | De-identified only | No | No | Yes (de-identified) |

All access is logged with user identity, timestamp, records accessed, and action performed. Access logs are retained for a minimum of 7 years per HIPAA and GDPR requirements.

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs)

| KPI ID | Metric | Target | Measurement Method | Reporting Cadence |
|--------|--------|--------|-------------------|-------------------|
| KPI-OVR-01 | **Global Override Rate** — percentage of AI recommendations overridden across all deployments | ≤12% (acceptable); >15% (investigation trigger) | Automated dashboard (Grafana) querying Override Registry vs. total recommendations served | Weekly to Clinical AI Safety Team; Monthly to CMO |
| KPI-OVR-02 | **Per-Module Override Rate** — override rate disaggregated by AI module | ≤15% per module | Same as above, filtered by Output-Module-ID | Weekly |
| KPI-OVR-03 | **Per-Facility Override Rate** — facility-level override comparison | ≤20% per facility; >20% triggers site visit | Override Registry grouped by Facility-ID | Monthly |
| KPI-OVR-04 | **Per-Clinician Override Rate** — individual clinician override frequency | ≤25% per clinician; >25% triggers peer review | Override Registry grouped by Clinician-ID (pseudonymized for routine reporting) | Monthly to Department Chairs |
| KPI-OVR-05 | **Safety-Category Override Rate** — rate of J-01 through J-04 overrides | ≤2% of all overrides; any J-01 triggers immediate review | Justification code filtering | Daily automated alert for J-codes |
| KPI-OVR-06 | **Silent Override Detection Rate** — percentage of EHR-congruent actions lacking override documentation | ≤1% of total actions | Weekly reconciliation batch | Monthly to Compliance Officer |
| KPI-OVR-07 | **Override Documentation Completeness** — override records with all mandatory fields completed | ≥99.5% | Automated validation on override record creation | Weekly |
| KPI-OVR-08 | **Mean Time to Retrospective Override Documentation** — time from detection to documentation completion | ≤4 hours for Categories A-B; ≤2 hours for Categories C-E | SETS ticket timestamp delta | Monthly |
| KPI-OVR-09 | **Override Justification Distribution** — frequency of each justification code | Monitoring for distribution shifts >2 standard deviations from baseline | Automated anomaly detection (Isolation Forest model) | Weekly anomaly alert |
| KPI-OVR-10 | **Clinician Override Training Compliance** — percentage of active override-privileged clinicians with current training | ≥99% | LMS (Cornerstone) report | Monthly |

### 7.2 Dashboards

**7.2.1 Clinical AI Safety Dashboard (Real-Time)**
Accessible to: Clinical AI Safety Team, CMO, VP Clinical AI Products
- Live global override rate with 24-hour rolling window
- Per-facility override rate heat map
- J-code override alert feed (all J-01/J-02 overrides displayed within 5 minutes)
- Top 10 clinicians by override rate (rolling 30-day)
- Model confidence score distribution for overridden vs. accepted recommendations

**7.2.2 Department Chair Dashboard (Monthly Refresh)**
Accessible to: Clinical Department Chairs, Facility Medical Directors
- Department-level override rate trend (12-month view)
- Per-clinician override rates within department (named, not pseudonymized)
- Override justification distribution for department
- Peer comparison (de-identified) against similar departments
- Silent override audit results

**7.2.3 Compliance Dashboard (Quarterly Refresh)**
Accessible to: Compliance Officer, Legal, C-Suite
- Regulatory compliance metrics mapped to EU AI Act obligations
- HIPAA-compliant override audit trail integrity scores
- Access audit summary (Override Registry access patterns)
- Incident trend analysis (Category C/D/E retrospective overrides)

### 7.3 Reporting Cadence

| Report | Recipients | Frequency | Delivery Method |
|--------|------------|-----------|-----------------|
| Override Safety Signal Report | Clinical AI Safety Team | Daily (automated) | Email digest + Slack channel #override-safety |
| Clinical Override Weekly Summary | CMO, VP Clinical AI Products | Weekly (Monday 09:00 UTC) | Secure PDF to executive inbox |
| Department Override Analysis | Clinical Department Chairs | Monthly (1st business day) | Secure portal download |
| Facility Override Benchmark Report | Facility CMOs, CQOs | Monthly | Secure portal download |
| Regulatory Compliance Attestation | Compliance Officer | Quarterly | Docusign workflow with executive approval |
| Annual Override Governance Review | Board Quality Committee, External Auditors | Annually | Formal report with findings, trends, and recommendations |

---

## 8. Exception Handling and Escalation

### 8.1 Exception Types and Handling

| Exception Type | Definition | Handling Procedure | Approval Authority |
|----------------|------------|-------------------|-------------------|
| **EXC-CLIN-006-01: System Unavailability** | Override documentation system unavailable during clinical override event | Clinician documents override in EHR free-text note; Meridian Clinical Support retroactively enters override within 24 hours of system restoration. EHR free-text note serves as interim documentation of record. | No pre-approval required; retroactive entry validated by Clinical Support Team Lead |
| **EXC-CLIN-006-02: Technical Override Recording Failure** | System accepts override documentation but fails to write to Override Registry | Automated alert generated to Meridian Clinical Support; investigation initiated within 4 hours; override re-documented if confirmed as not recorded | Clinical Support Team Lead |
| **EXC-CLIN-006-03: Emergency Clinical Override** | Life-threatening situation requiring immediate clinical action without time for standard override documentation | Clinician acts on clinical judgment; documentation completed within 1 hour of patient stabilization using "Emergency Override" workflow (abbreviated justification; mandatory retrospective elaboration within 24 hours) | Clinical Department Chair (retrospective review within 48 hours) |
| **EXC-CLIN-006-04: Offline Deployment Override** | Facility operating with intermittent connectivity | Override queued locally on Meridian Edge Node (MEN-2024); synchronized to Override Registry upon connectivity restoration. Local queue persists for maximum 14 days. | Automatic synchronization upon reconnection; no approval required |
| **EXC-CLIN-006-05: Research Protocol Override** | Override occurring within IRB-approved research protocol using modified AI parameters | Research-specific override taxonomy and documentation workflow pre-approved by IRB; override data segregated from production registry; not included in standard override rate calculations | IRB + CMO (dual approval) |

### 8.2 Escalation Pathway

Override-related escalations follow a tiered pathway based on severity and complexity:

**Level 1: Routine Override Pattern Concern**
*Trigger:* Department chair identifies clinician override rate exceeding 25% or unusual justification code distribution.
*Action:* Department chair schedules peer review discussion with clinician within 14 calendar days.
*Resolution:* Peer review documented; clinician feedback incorporated; override privileges unaffected unless patient safety concern identified.

**Level 2: Elevated Override Pattern with Potential Safety Implications**
*Trigger:* Clinical AI Safety Team identifies facility-level override rate exceeding 20% OR J-code override cluster (>5 J-codes within 7 days for same module at same facility).
*Action:* CMO notified within 24 hours; site assessment initiated within 7 calendar days (virtual or on-site); module may be temporarily suspended at affected facility pending assessment per SOP-IT-043 "Clinical AI Service Suspension."
*Resolution:* Written assessment report with findings and recommendations; module reinstatement or continued suspension determined by CMO.

**Level 3: Patient Harm Associated with Override Failure**
*Trigger:* Category C, D, or E retrospective override event (patient harm occurred because override was not performed when clinically indicated).
*Action:*
1. Immediate notification to CMO and Compliance Officer (within 2 hours)
2. Root cause analysis initiated within 24 hours per SOP-QUAL-012 "Adverse Event Investigation"
3. Regulatory reporting assessment completed within 72 hours
4. Affected module reviewed for potential systemic issues
5. Affected facility clinical leadership briefed within 5 business days
*Resolution:* Formal investigation report; corrective and preventive actions (CAPA) plan; regulatory filings as required; potential model retraining or deployment modification.

**Level 4: Systematic Override Mechanism Failure**
*Trigger:* Override recording system failure affecting multiple facilities or persisting >4 hours at any single facility.
*Action:*
1. Incident declared by VP Clinical AI Products within 1 hour
2. IT incident response team activated per SOP-IT-044 "Major Incident Management"
3. Affected facilities notified to utilize manual override documentation procedures
4. Regulatory notification assessment per applicable medical device vigilance requirements
*Resolution:* System restoration; root cause analysis; full override data reconciliation; regulatory reporting as applicable.

### 8.3 Override Privilege Modification

Override privileges may be modified under the following circumstances:

| Condition | Modification | Duration | Approval Authority |
|-----------|-------------|----------|-------------------|
| Clinician override rate >40% for two consecutive months | Mandatory peer review; override privileges maintained but subject to monthly prospective review | Until rate drops below 30% for two consecutive months | Department Chair + CMO |
| Clinician found to have executed >5 silent overrides within 12 months | Override privileges temporarily restricted to "Override with Co-Signature" (second clinician must co-sign override) | 90 calendar days minimum | CMO + Compliance Officer |
| Clinician override determined to have contributed to patient harm (Category E) | Immediate suspension of override privileges pending full investigation | Duration of investigation (maximum 60 calendar days) | CMO |

All override privilege modifications are documented in the clinician's Meridian platform profile and communicated to the facility credentialing office.

---

## 9. Training Requirements

### 9.1 Required Training Modules

All clinicians eligible for override privileges must complete the following training:

| Training Module | Code | Duration | Delivery Method | Frequency |
|-----------------|------|----------|-----------------|-----------|
| Clinical AI Platform Fundamentals | TRN-CLIN-024-A | 2.0 hours | Asynchronous e-learning (Cornerstone LMS) | Once at onboarding; refresher upon major version update |
| Override Procedures and Documentation | TRN-CLIN-024-B | 1.5 hours | Asynchronous e-learning + 30-minute virtual instructor-led practicum | Once at onboarding; annual refresher (1 hour) |
| Justification Taxonomy and Application | TRN-CLIN-024-C | 1.0 hour | Case-based e-learning (12 clinical scenarios with override decision points) | Once at onboarding; updated annually with taxonomy updates |
| Patient Safety and AI Limitations | TRN-CLIN-024-D | 1.5 hours | Instructor-led (virtual or in-person) | Once at onboarding; biennial refresher |
| Regulatory Compliance for AI Overrides | TRN-CLIN-024-E | 1.0 hour | Asynchronous e-learning | Annual (all override-privileged clinicians) |

**Total Initial Training: 7.0 hours** (including practicum)
**Annual Refresher Training: 3.0 hours**

### 9.2 Training Competency Assessment

**Initial Competency Assessment:**
- Written examination (80% passing threshold): 50 multiple-choice questions covering override procedures, taxonomy application, and safety escalation
- Practical assessment: 8 simulated override scenarios (minimum 7 of 8 correct override justification selections)
- Instructor evaluation: Virtual practicum includes direct observation of override workflow execution

**Annual Competency Reassessment:**
- Written examination (80% passing threshold): 30 questions
- Practical assessment: 5 simulated override scenarios (minimum 4 of 5 correct)

**Remediation:**
Clinicians failing initial or annual competency assessment:
- 30-day remediation window
- Assigned peer mentor (experienced override-privileged clinician)
- Retake assessment (maximum 2 retake attempts)
- Override privileges suspended pending successful remediation (exception: clinicians may continue to override but require Department Chair co-signature on all overrides during suspension period)

### 9.3 Training Compliance Tracking

- All training completions recorded in Cornerstone LMS with clinician identifier linked to EHR NPI number
- Monthly training compliance reports to Clinical Department Chairs
- Dashboard (KPI-OVR-10) tracks real-time override training compliance percentage
- Non-compliance >90 days: automatic override privilege restriction to "Override with Co-Signature" until training completed
- Annual attestation by CMO confirming training program adequacy and compliance

---

## 10. Related Policies and References

### 10.1 Internal Meridian SOPs

| SOP ID | Title | Relationship to SOP-CLIN-006 |
|--------|-------|------------------------------|
| SOP-CLIN-001 | Clinical AI Platform Governance Framework | Establishes overarching governance under which override procedures operate |
| SOP-CLIN-003 | Clinical AI Model Version Control and Deployment | Defines model version tracking referenced in override documentation requirements |
| SOP-CLIN-005 | Adverse Event Prediction System Validation | Validation procedures for AEP module; override data used as validation input |
| SOP-CLIN-008 | Clinical Decision Support Alert Fatigue Management | Addresses override rate thresholds in context of clinician alert burden |
| SOP-TRN-024 | Clinical AI Platform Clinician Training Program | Detailed training curriculum and certification requirements |
| SOP-COMP-015 | Compliance Investigation Procedures | Silent override investigation procedures referenced in Section 5.3 |
| SOP-COMP-031 | Adverse Event Regulatory Reporting | Mandatory reporting for Category D/E retrospective overrides |
| SOP-PRIV-018 | Patient Data Amendment Requests | Patient-initiated data corrections (out of scope for this SOP) |
| SOP-IT-042 | Emergency System Decommissioning | System-wide shutdown procedures |
| SOP-IT-043 | Clinical AI Service Suspension | Module or facility-level suspension procedures invoked in Level 2 escalation |
| SOP-IT-044 | Major Incident Management | IT incident response for systematic override mechanism failures |
| SOP-QUAL-012 | Adverse Event Investigation | Root cause analysis procedures for patient harm events |

### 10.2 External Standards and Regulations

| Standard/Regulation | Reference | Applicability |
|---------------------|-----------|---------------|
| EU AI Act (Regulation 2024/1689) | Article 14 (Human Oversight) | High-risk AI systems must be designed to allow effective human oversight; Meridian maintains human oversight capability at all deployments |
| EU Medical Device Regulation (2017/745) | Annex I (General Safety and Performance Requirements); Annex VIII (Classification) | CE-marked DIA-2024-B classified as Class IIb medical device |
| HIPAA | 45 CFR §164.312 (Technical Safeguards); §164.308 (Administrative Safeguards); §164.310 (Physical Safeguards) | PHI protection within Override Registry; access controls; audit controls |
| HIPAA Security Rule | 45 CFR §164.312(b) — Audit Controls | Hardware, software, and procedural mechanisms to record and examine activity in information systems containing ePHI |
| HIPAA Privacy Rule | 45 CFR §164.508 — Uses and Disclosures | Override data use for treatment, payment, and healthcare operations |
| NIST AI RMF 1.0 | Govern 1.2: Organizational policies and procedures address AI risks; Govern 2.3: Accountability structures for AI system outcomes; Map 3.1: Context established for AI risk assessment; Measure 4.3: Monitoring for impacts on individuals and groups | Comprehensive governance, accountability, and monitoring framework applied to override mechanisms |
| NIST AI RMF 1.0 | Manage 1.2: Risk treatment options including risk avoidance; Manage 2.4: Mechanisms for stakeholder feedback regarding AI system performance | Override mechanism as documented risk treatment; override patterns as continuous stakeholder feedback channel |
| NIST AI RMF 1.0 | Map 2.1: System benefits and potential harms identified; Measure 3.2: Testing for accuracy, robustness, and reliability | FMEA-informed identification of override necessity; override rates as proxy metric for AI reliability |
| NIST SP 800-53 Rev. 5 | AU-2 (Event Logging); AU-3 (Content of Audit Records); AU-6 (Audit Record Review, Analysis, and Reporting); AU-11 (Audit Record Retention) | Immutable override audit trail; 7-year retention; monthly access audits |
| FDA AI/ML SaMD Action Plan | Total Product Lifecycle regulatory approach | Override monitoring as post-market surveillance input |
| IHE ATNA Profile | Audit Trail and Node Authentication | FHIR AuditEvent integration for override records |

### 10.3 Reference Documents

| Document | Description | Location |
|----------|-------------|----------|
| Clinical AI Platform FMEA Report (2026) | Failure Mode and Effects Analysis identifying override-critical failure modes | Meridian Quality Management System (QMS-CLIN-FMEA-2026-001) |
| Standardized Override Justification Taxonomy Codebook | Detailed definitions, examples, and coding guidance for all justification codes | Clinical AI Safety SharePoint (internal) |
| Clinical AI Platform System Architecture | Technical architecture diagrams including Override Registry AuroraDB cluster configuration | Engineering Technical Documentation Repository |
| EU AI Act Conformity Assessment Documentation | Technical documentation supporting high-risk classification and conformity | Legal/Regulatory SharePoint |

---

## 11. Revision History

| Version | Date | Author | Description of Changes | Approved By |
|---------|------|--------|------------------------|-------------|
| 5.0 | 2024-09-12 | Dr. James Morrison (former VP Clinical AI) | Major restructure: Separated override procedures for CDS, DIA, and PRS modules; introduced Standardized Override Justification Taxonomy; added retrospective override procedure. | Dr. Priya Patel, CMO |
| 5.2 | 2024-12-03 | Dr. Aisha Okafor, VP Clinical AI Products | Added silent override detection reconciliation process (Section 5.3); updated escalation pathway to include 4-tier structure; revised override rate KPI thresholds based on 2024 Q3 operational data analysis. | Dr. Priya Patel, CMO |
| 5.5 | 2025-03-18 | Dr. Aisha Okafor, VP Clinical AI Products; Sarah Chen, Compliance Officer | EU AI Act compliance alignment: added specific controls for high-risk AI system human oversight; expanded training requirements to include regulatory module; updated override registry access controls for GDPR compliance. Incorporated NIST AI RMF mapping to all control sections. HIPAA technical safeguard controls detailed in Section 6.1. | Dr. Priya Patel, CMO |
| 5.7 | 2025-09-30 | Dr. Aisha Okafor, VP Clinical AI Products | Added Adverse Event Prediction System (AEP-2024-D) and Medication Interaction Analyzer (MIA-2025-A) to scope. Updated justification taxonomy to include MIA-specific codes. Revised department chair override monitoring responsibilities. Added annual competency reassessment requirement. | Dr. Priya Patel, CMO |
| 5.8 | 2026-08-04 | Dr. Aisha Okafor, VP Clinical AI Products; Dr. Marcus Rivera, Clinical AI Safety Lead | Comprehensive annual review. Updated KPIs with 2026 operational targets. Added Section 6.3 override registry access control matrix. Revised escalation pathway timeframes based on post-market surveillance data (2025-2026). Updated related policies cross-references. No substantive procedural changes. | Dr. Priya Patel, CMO |

---

*End of Document — SOP-CLIN-006 v5.8*
*Next Scheduled Review: 2027-02-05*
*Document Owner: Dr. Aisha Okafor, VP of Clinical AI Products*
*Classification: Internal — Do Not Distribute Externally Without Legal Review*