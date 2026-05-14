---
sop_id: "SOP-CLIN-001"
title: "Clinical Decision Support System Validation"
business_unit: "Clinical AI Products"
version: "3.3"
effective_date: "2024-05-05"
last_reviewed: "2025-05-23"
next_review: "2025-11-03"
owner: "Dr. Aisha Okafor, VP of Clinical AI Products"
approver: "Dr. Priya Patel, Chief Medical Officer"
classification: "Internal"
regulations:
  - "EU AI Act"
  - "HIPAA"
  - "NIST AI RMF"
status: "Active"
---

# Standard Operating Procedure: Clinical Decision Support System Validation

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the enterprise-wide framework for the rigorous validation of all Clinical Decision Support Systems (CDSS) developed, deployed, or maintained by Meridian Health Technologies, Inc. The purpose of this document is to ensure that every AI-driven clinical tool provides accurate, reliable, clinically meaningful, and equitable outputs that support—rather than supplant—the judgment of licensed healthcare professionals. This SOP operationalizes the principles of Good Machine Learning Practice (GMLP), the NIST AI Risk Management Framework (AI RMF), and applicable international regulations to standardize how Meridian defines, measures, and monitors clinical performance.

This SOP is the authoritative reference for distinguishing between model development completion and clinical readiness. No CDSS model shall be promoted from a development environment to a staging or production environment without documented adherence to the procedures herein.

### 1.2 Scope

This SOP applies to the **Clinical AI Platform** business unit and extends to any component within the Meridian SaaS Platform that generates patient-specific risk scores, diagnostic suggestions, adverse event predictions, or treatment pathway recommendations.

**In-Scope Systems:**
- Radiological diagnostic imaging analysis models (e.g., ChestXray-AI, NeuroQuant-MS)
- Patient deterioration and sepsis risk scoring engines (e.g., Meridian Early Warning System)
- Hospital readmission risk stratification models
- Adverse drug event prediction systems
- Clinical trial matching algorithms that process patient PHI
- Any new CDSS product acquired through merger, acquisition, or partnership

**Out-of-Scope Systems (covered under separate SOPs):**
- Population-level analytics dashboards that do not generate patient-specific outputs (see SOP-ANL-002)
- Revenue cycle management and claims automation algorithms (see SOP-FIN-015)
- Administrative scheduling or staffing prediction tools
- General-purpose large language models before fine-tuning for clinical use (see SOP-AI-009)

**Regulatory Context:**
These procedures are designed to satisfy the validation requirements for:
- **EU AI Act:** High-Risk AI Systems (Annex III, point 2(a) - Medical Devices and In Vitro Diagnostic Medical Devices)
- **HIPAA:** Privacy and Security Rules pertaining to electronic Protected Health Information (ePHI) used in model training and inference
- **NIST AI RMF 1.0:** Functions MAP, MEASURE, and GOVERN as adopted by the Meridian AI Governance Committee
- **FDA:** Quality System Regulation (21 CFR Part 820) and guidance on Clinical Decision Support Software

### 1.3 Applicability

This SOP is binding on all full-time employees, contractors, consultants, and third-party vendors who contribute to the design, development, testing, deployment, or monitoring of CDSS models. Compliance is mandatory and subject to audit by the Quality Assurance and Internal Audit teams. Failure to adhere to this SOP may result in disciplinary action, termination of contract, and regulatory non-compliance exposure for the organization.

---

## 2. Definitions and Acronyms

For the purposes of this SOP, the following definitions and acronyms apply. Terms not defined here shall align with the Meridian Corporate Glossary (GLOS-CORP-001) and ISO 9000:2015.

### 2.1 Definitions

| Term | Definition |
| :--- | :--- |
| **Clinical Decision Support System (CDSS)** | Any AI/ML-enabled software system that analyzes patient-specific data to generate a risk score, classification, recommendation, or prediction intended to inform a clinical decision by a qualified healthcare provider. |
| **Clinical Validation** | The process of demonstrating that a CDSS achieves its intended clinical purpose by producing outputs that are accurate, reliable, and clinically meaningful when compared to an established reference standard in a representative patient population. This is distinct from technical validation (does the code run?) and business validation (does it save money?). |
| **Gold Standard / Reference Standard** | The best available method for establishing the presence or absence of the target condition. This may include histopathological biopsy results, expert consensus panel adjudication, patient outcomes at 30/60/90 days, or FDA-cleared comparator devices. |
| **Silent Trial** | A prospective validation methodology wherein the CDSS runs in real-time on live production data and generates predictions, but those predictions are not displayed to clinicians. System outputs are logged and retrospectively compared against clinical outcomes to measure performance without introducing clinical risk. |
| **Clinical Endpoint** | A precisely defined variable that reflects a clinically meaningful outcome relevant to the CDSS's intended use. Endpoints must be objective, measurable, and verifiable. Examples: 30-day all-cause mortality, ICU transfer within 6 hours, histologically confirmed malignancy. |
| **Alert Fatigue Threshold** | The maximum rate of false-positive alerts, expressed as alerts per clinician per shift or positive predictive value (PPV), above which clinical users demonstrably ignore or override system warnings. |
| **Model Drift** | The degradation of a model's performance over time due to changes in the underlying data distribution (data drift), changes in the relationship between input features and the target variable (concept drift), or changes in clinical practice. |
| **Equitable Performance** | The degree to which a CDSS maintains clinically acceptable performance metrics (e.g., sensitivity, specificity, AUROC) across predefined demographic subpopulations—including but not limited to race, ethnicity, sex, age, primary language, and geographic region—without statistically significant disparity. |
| **Human-in-the-Loop (HITL)** | A design paradigm obligating that every CDSS output is presented to and reviewable by a qualified human operator with the authority to accept, override, or dismiss the machine's recommendation. |
| **Technical Documentation** | The collection of documents describing the design, development, and validation of the AI system, maintained to satisfy Annex IV of the EU AI Act. |

### 2.2 Acronyms

| Acronym | Meaning |
| :--- | :--- |
| AUROC | Area Under the Receiver Operating Characteristic Curve |
| AUPRC | Area Under the Precision-Recall Curve (preferred for imbalanced datasets) |
| CDSS | Clinical Decision Support System |
| CMO | Chief Medical Officer |
| ePHI | Electronic Protected Health Information |
| FMEA | Failure Mode and Effects Analysis |
| FN | False Negative |
| FP | False Positive |
| GMLP | Good Machine Learning Practice |
| HITL | Human-in-the-Loop |
| MLflow | Machine Learning Lifecycle Management Platform (Meridian's tracking server) |
| NIST AI RMF | National Institute of Standards and Technology Artificial Intelligence Risk Management Framework |
| PPV | Positive Predictive Value (Precision) |
| QMS | Quality Management System |
| SOTA | State-of-the-Art |
| TN | True Negative |
| TP | True Positive |

---

## 3. Roles and Responsibilities

The following matrix delineates the roles and accountabilities for CDSS validation activities. All named roles represent functions; a single individual may serve multiple roles if no conflict of interest exists, as determined by General Counsel.

| Role | Accountable (A) | Responsible (R) | Consulted (C) | Informed (I) |
| :--- | :---: | :---: | :---: | :---: |
| **VP of Clinical AI Products (Dr. Aisha Okafor)** | A | | C (Design reviews) | I (Release decisions) |
| **Chief Medical Officer (Dr. Priya Patel)** | | A (Final sign-off) | | |
| **Clinical Data Science Lead** | | R (Validation protocol design, execution, statistical analysis) | C (Endpoint selection) | I |
| **Biostatistician (Medical Affairs)** | | R (Sample size calculation, statistical test plan) | | I |
| **Quality Assurance Manager** | | R (Process adherence audit) | C (Test case verification) | I |
| **Privacy Officer (Dr. Klaus Weber)** | | | C (Data usage / GDPR Art. 9 compliance) | I |
| **Regulatory Affairs Specialist** | | R (Submission prep) | C (Risk classification) | I |
| **Chief AI Officer (Dr. Marcus Rivera)** | | | | I (Quarterly review) |
| **CISO (Rachel Kim)** | | | C (Data security posture) | I |
| **Clinical Subject Matter Expert (e.g., Radiologist, Intensivist)** | | R (Gold standard adjudication, clinical significance assessment) | C (Workflow integration) | I |

### 3.1 Detailed Responsibility Descriptions

- **VP of Clinical AI Products:** Holds ultimate accountability for the technical integrity of the CDSS portfolio. Responsible for securing budget and personnel for validation studies. Authorizes the release of models from Development to Staging.
- **Chief Medical Officer:** Holds final signatory authority on all Clinical Validation Reports. Assesses whether the system poses acceptable clinical risk. Cannot be overridden on matters of patient safety.
- **Clinical Data Science Lead:** Authors the Validation Plan. Coordinates the extraction of test datasets from Snowflake. Ensures that MLflow tracking servers log all validation metrics and that the experiment lineage is immutable.
- **Biostatistician:** Determines the minimum sample size required to achieve 80% statistical power with a significance level of α = 0.05 (unless otherwise pre-specified). Selects appropriate frequentist or Bayesian methods for hypothesis testing.
- **Quality Assurance Manager:** Witnesses validation testing where required by SOP-QA-100. Records and tracks all deviations from this SOP in the Veeva Vault QMS. Approves the closure of validation incidents.

---

## 4. Policy Statements

Meridian Health Technologies, Inc. commits to the following binding policies in the execution of CDSS validation:

### 4.1 Evidence-Based Clinical Performance
Every CDSS must demonstrate a statistically significant improvement in at least one pre-registered clinical endpoint compared to standard-of-care decision-making, OR demonstrate non-inferiority with a pre-specified margin (Δ < 0.1 for AUROC comparisons). Purely technical metrics (e.g., F1 score, log-loss) are necessary but insufficient for production release.

### 4.2 Multi-Dataset Validation
Validation must occur across a minimum of three independent data sources: (1) a retrospective holdout test set from the training data period, (2) a temporally distinct dataset (e.g., data from the 6 months following the training data cutoff), and (3) a geographically distinct dataset (e.g., data from a Meridian customer site not included in training—prioritizing EU sites for CE-marked products).

### 4.3 Human-in-the-Loop Efficacy
Validation testing must explicitly measure the human-machine team performance, not just algorithmic standalone performance. A silent trial phase of no fewer than 30 calendar days is mandatory prior to go-live display.

### 4.4 Technical Documentation
Meridian shall maintain comprehensive Technical Documentation in accordance with Annex IV of the EU AI Act for each high-risk AI system. This documentation shall include a general description of the system, detailed elements of the design, and a description of the system's intended purpose. The documentation shall reference the Quality Management System established under ISO 13485.

### 4.5 Performance Benchmarking
Prior to CE marking or FDA clearance, a formal State-of-the-Art (SOTA) comparison must be conducted, benchmarking Meridian’s model against at least two clinically accepted alternative methods, which may include established clinical scoring rules (e.g., SOFA, APACHE II) or cleared competitor algorithms.

### 4.6 Minimum Necessary Access
Validation teams shall be granted access only to the minimum necessary ePHI datasets required to perform the validation function. De-identified datasets must be prioritized. Where identification is required for gold standard label generation, a Limited Data Set agreement, as defined by HIPAA, must be executed, and the 18 direct identifiers must be stripped before ingestion into any sandbox environment not managed as a Production-PHI enclave.

### 4.7 Breach Notification
In the event of a breach of unsecured ePHI utilized within a validation environment, the incident response lead shall coordinate notification. The incident shall be reported to the CISO and Privacy Officer immediately upon discovery. Notifications to affected individuals, the Secretary of Health and Human Services, and prominent media outlets will be executed in accordance with the Incident Response Plan (SOP-SEC-006) and applicable breach notification laws.

---

## 5. Detailed Procedures

This section is the authoritative operational guide for executing CDSS Validation. The lifecycle is divided into six Gates, each with mandatory entry/exit criteria logged in the Veeva Vault QMS and the MLflow experiment registry.

### 5.1 Gate 1: Validation Strategy and Endpoint Analysis (Duration: ~10 Business Days)

**Trigger:** Model card complete and retrospective testing metrics (AUROC > 0.75) achieved on the Engineering holdout set.

**Procedure Steps:**

1.  **Initiation:** The Clinical Data Science Lead opens a new Validation Initiative record in the QMS (Veeva Vault, Doc Type: "Validation Plan"). The record is linked to the specific model version ID in the MLflow Model Registry.
2.  **Stakeholder Kick-off:** A 60-minute meeting is convened with the Clinical Data Science Lead, Biostatistician, and the designated Clinical Subject Matter Expert (SME). Minutes are recorded in the QMS record.
3.  **Target Condition Definition:** The Clinical SME formally defines the clinical condition being predicted. *Example: For NeuroQuant-MS, the target condition is "Radiologically Isolated Syndrome (RIS) confirmed by McDonald 2017 criteria at 6-month follow-up MRI."* This definition is locked and version-controlled.
4.  **Endpoint Hierarchy Establishment:** The team establishes a Primary Endpoint (weighted 60% in overall assessment) and at least two Secondary Endpoints (weighted 20% each).
    - *Primary Endpoint Example:* Sensitivity > 0.90 with specificity floor of > 0.75.
    - *Secondary Endpoint Example:* Mean time to clinical alert < 45 seconds from PACS data ingestion.
5.  **Reference Standard Selection:** The SME identifies the Gold Standard. If the Gold Standard is invasive (e.g., biopsy), a surrogate standard may be proposed via a formal Exception Request (see Section 8).

**Exit Criteria:** Completed "Validation Strategy Template" (FRM-CLIN-101) signed by the Biostatistician and Clinical SME.

### 5.2 Gate 2: Statistical Test Plan and Data Procurement (Duration: ~15 Business Days)

**Procedure Steps:**

1.  **Sample Size Calculation:** The Biostatistician uses the locked endpoint definitions from Gate 1 to programmatically compute the required sample size in R (using the `pwr` package). Script and output must include:
    - Alpha level: 0.05 (adjusted for multiplicity if secondary endpoints gate primary).
    - Desired Power: 0.80 (or 0.90 depending on risk classification).
    - Expected Effect Size: Based on preliminary research or internal pilot data.
2.  **Diversity Mandate Compliance:** The sample cohort definition must specify stratified sampling based on the Meridian Equity Schema (race, ethnicity, sex, age decile [18-90+]). No single demographic cell shall constitute more than 60% of the test cohort unless clinically justifiable (e.g., prostate cancer model).
3.  **Data Source Identification:** The team identifies candidate datasets in Snowflake using the `CDSS_VALIDATION_CATALOG` view.
    - **Temporal Holdout:** Partition where `inference_date > training_end_date`.
    - **Geographic Holdout:** Partition where `site_id NOT IN (training_site_ids)` – explicitly targets at least one EU member state hospital.
4.  **Data Quality (DQ) Check:** Execute the `DQ-CLIN-101` automated script. Fail the pipeline immediately if:
    - Missingness > 5% in critical features.
    - Duplicate patient records detected.
    - Feature drift (Population Stability Index > 0.25) detected compared to the original training set.
5.  **De-identification and Authorization:** For data leaving the production Snowflake environment (e.g., to an on-prem GPU cluster), apply the HIPAA Safe Harbor method. The Privacy Officer (Dr. Weber) must approve the authorization checklist (FRM-CSEC-005) before data transfer.

**Exit Criteria:** "Statistical Analysis Plan (SAP)" document locked and digitally co-signed by Biostatistician and Clinical Data Science Lead.

### 5.3 Gate 3: Retrospective Clinical Validation

**Procedure Steps:**

1.  **Blinded Inference:** Run inference using the frozen model binary (as stored in the Meridian Model Registry) against the curated cohort. The execution environment must be isolated and tracked in MLflow for audit trail completeness.
2.  **Ground Truth Adjudication:** For cases where the Gold Standard differs from the "soft label" in the EHR, escalate to the Clinical Adjudication Panel (see Section 6.1).
3.  **Confusion Matrix Generation:** Generate the standard confusion matrix (TP, TN, FP, FN). Compute AUROC, AUPRC, PPV, Negative Predictive Value (NPV), and Likelihood Ratios (+LR, -LR).
4.  **Calibration Analysis:** Generate a calibration curve (reliability diagram). If Brier Score > 0.25 for risk prediction models, a Platt Scaling recalibration must be applied to the inference pipeline artifact.
5.  **Subgroup Performance Analysis:** Disaggregate metrics according to the Meridian Equity Schema. A warning flag shall be logged by the system if a disparity ratio (Min AUROC / Max AUROC) < 0.8 for any sensitive attribute.

**Exit Criteria:** "Retrospective Validation Report" (TEMPL-CLIN-105) generated with automated statistical outputs.

### 5.4 Gate 4: Silent Trial Protocol (Prospective Validation)

**Procedure Steps:**

1.  **Engineering Deployment for Silent Mode:** The validated model is deployed to the production Kubernetes cluster (`meridian-prod-us-east`). The `clinical_display_flag` environment variable is explicitly set to `FALSE`.
2.  **Real-Time Data Pipeline Registration:** The model subscribes to the production HL7 FHIR R4 stream. Every patient encounter that meets the inclusion criteria triggers an inference event.
3.  **Shadow Logging:** Inference results (risk score, class label, confidence interval) are written to the `silent_trial_results` Apache Kafka topic with strict message ordering. No data is rendered in the Epic or Cerner EHR interfaces.
4.  **Duration Monitoring:** The silent trial shall run for a minimum of 30 calendar days, collecting a minimum sample size equivalent to 70% of the SAP target. In the event of a significant software release of the Meridian Gateway API, the silent trial duration resets.
5.  **Mid-Point Utility Check:** At Day 15, the team analyzes the distribution of risk scores. If >85% of risk scores fall into the "indeterminate" category, the model is paused, labeling it as having "Low Clinical Utility," and returned to Step 1 (Development).

**Exit Criteria:** Prospective data collection complete, with Kafka topic backlog consumed and validated against EHR structured query language (SQL) audit tables. A data completeness report > 98% must be achieved.

### 5.5 Gate 5: Clinical Utility and Human-in-the-Loop (HITL) Simulation

**Procedure Steps:**

1.  **Clinician Review Panel Assembly:** Recruit a panel of 5 practicing clinicians representative of the intended user base. This panel must be independent of the model development team.
2.  **Retrospective Case Mix Construction:** The Biostatistician constructs a balanced review packet containing 200 cases:
    - 100 cases where the model prediction was correct.
    - 50 cases where the model prediction was incorrect.
    - 50 random negative controls.
3.  **HITL Efficacy Testing:** Clinicians review the cases *without* AI assistance first, documenting their assessment. Then, the AI output is revealed. The changes in clinician diagnostic accuracy are measured.
4.  **Alert Fatigue Assessment:** A Likert-scale survey (1-5) is administered after each of the 200 cases, asking, "I found the AI alert to be clinically helpful." If the inter-rater reliability (Fleiss' Kappa) for helpfulness falls below 0.6, the UX of the alert presentation in the EHR must be revised.
5.  **Harm Analysis:** A Failure Mode and Effects Analysis (FMEA) is executed by the panel to identify top-ten failure modes, focusing specifically on false negatives that could cause patient harm due to omission.

**Exit Criteria:** A mean helpfulness score > 3.5, Fleiss' Kappa > 0.6, and a documented FMEA with no open catastrophic (Severity 5) findings.

### 5.6 Gate 6: Final Release Authorization and Documentation

**Procedure Steps:**

1.  **Collation of the Validation Report:** The Clinical Data Science Lead compiles Gates 1-5 into the "Summary of Safety and Clinical Performance" (SSCP).
2.  **CMO Final Review:** Dr. Priya Patel reviews the complete dossier. The CMO documents the clinical risk-benefit justification in Veeva Vault.
3.  **Artifact Freezing:** All datasets, model binaries, MLflow experiments, scripts, and logs are tagged with the release version (`v3.3.0`) and moved to immutable cloud storage (AWS S3 Glacier Instant Retrieval) for regulatory retention.
4.  **Technical Documentation Update:** The Technical Documentation package is updated to reflect the validation results. The documentation describes the system's intended purpose, its intended users, and the logic of the algorithm.

---

## 6. Controls and Safeguards

### 6.1 Technical Controls

| Control Category | Control ID | Control Description |
| :--- | :--- | :--- |
| **Data Isolation** | TAC-01 | Validation datasets used in Gate 3 shall be logically isolated from the model training lakehouse via Snowflake’s `VALIDATION_SCHEMA` role-based access controls. No service account with write access to the model store shall have write access to the validation raw data. |
| **Immutability** | TAC-02 | All MLflow experiment tracking and artifacts logged during validation runs shall be tagged with `immutable: true`. The `mlflow.admin.delete_experiment` permission is rescinded for all non-CISO personnel in production. |
| **Model Versioning** | TAC-03 | Only models registered in the MLflow Model Registry with a `stage/production` tag and a passed Validation Gate checklist may be deployed. The CI/CD pipeline (GitLab CI) programmatically queries MLflow before building the inference container. |
| **PHI Masking in Logs** | TAC-04 | Patient identifier columns (e.g., MRN, Name, DoB) are programmatically masked to `*****` in all predictive model log streams via a Fluentd filter. Any unmasked PHI in logs triggers an automatic PagerDuty Critical alert. |

### 6.2 Administrative Controls

| Control Category | Control ID | Control Description |
| :--- | :--- | :--- |
| **Adjudication Panel** | ADC-01 | A Clinical Adjudication Panel (CAP), comprising three independently licensed Meridian-employed physicians, shall resolve disagreements in the reference standard. Majority vote determines the final label. |
| **Segregation of Duties** | ADC-02 | The Data Scientist who trained the model is strictly prohibited from executing the Gate 3 validation testing or approving the SAP. The role of "Validation Execution" is assigned only to persons in the Quality Assurance or independent Clinical Data Science sub-team. |
| **Access Controls for ePHI** | ADC-03 | Validation engineers shall access de-identified datasets in the `deid_clinical_research` environment. Access to identifiable data is restricted to the Clinical Adjudication Panel and requires MFA using a FIDO2 hardware token. |

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Production Monitoring (Post-Deployment Surveillance)

Following a successful Go-Live, the CDSS enters ongoing surveillance. The Meridian Observability Platform (Grafana stack) shall provide real-time dashboards for the following Key Performance Indicators (KPIs):

| KPI Category | Specific Metric | Threshold (Critical) | Threshold (Warning) |
| :--- | :--- | :--- | :--- |
| **Operational Health** | Prediction API Latency (p99) | > 2000 ms | > 1000 ms |
| **Data Drift** | Feature PSI (Population Stability Index) | > 0.30 | > 0.15 |
| **Feature Health** | Percentage of null values in a critical feature | > 25% | > 10% |
| **Clinical Efficacy** | Surrogate Model AUROC (measured via silent trial) | Drop > 0.10 from baseline | Drop > 0.05 from baseline |
| **Adoption** | Alert Acceptance Rate (Clinician accepts suggestion) | < 30% | < 50% |
| **System Diversity** | Demographic disparity in inference volume vs. census | χ² p < 0.001 | χ² p < 0.05 |

### 7.2 Reporting Cadence

- **Weekly:** Automated reports on data drift and feature health delivered to the MLOps Team and Clinical Data Science Lead.
- **Monthly:** Model performance reports (PSI, feature drift, alert acceptance) distributed to the VP of Clinical AI Products and Product Managers.
- **Quarterly:** Comprehensive CDSS Portfolio Efficacy Report presented to the Chief Medical Officer and Chief AI Officer. This report shall discuss performance trends across all monitored subpopulations and assess aggregate clinical value.

---

## 8. Exception Handling and Escalation

### 8.1 Exception Request Process

Deviations from any mandatory step in this SOP require a formal Exception Request. The process is as follows:

1.  **Submission:** The requestor must complete the "Validation Exception Form" (FRM-QA-201) in Veeva Vault. The form must detail:
    - The specific Section/Gate from which deviation is sought.
    - A technical or clinical justification for non-compliance.
    - A compensating control or alternative validation methodology proposed.
    - Risk assessment describing the safety impact of the deviation.
2.  **Review:** The Exception Request is reviewed by the Quality Assurance Manager and the Biostatistician. They may request additional data.
3.  **Approval Matrix:**
    - **Low Risk Exception:** (e.g., extension of temporal holdout by 30 days) Approval required: VP of Clinical AI Products.
    - **Medium Risk Exception:** (e.g., waiving a geographic holdout site) Approval required: VP of Clinical AI Products + Chief Medical Officer.
    - **High Risk Exception:** (e.g., deviating from primary endpoint or reducing sample size below power requirements) Approval required: Chief Medical Officer + Chief AI Officer + General Counsel. This exception must be reported to the Board Audit and Compliance Committee.

### 8.2 Escalation Protocol for Live Model Drift

If a production CDSS breaches a Critical Threshold detailed in Section 7.1:

1.  **Automatic Page:** A PagerDuty incident is created and assigned to the Director of Clinical Engineering.
2.  **Immediate Action:** The Director of Clinical Engineering shall, within 4 hours, determine whether to place the model into "Shadow Mode" (prediction disabled in the EHR view) using the global LaunchDarkly kill switch.
3.  **CMO Notification:** The CMO must be notified within 8 hours of a confirmed Critical Threshold breach.
4.  **Remediation Loop:** A Root Cause Analysis (RCA) utilizing a standardized "Five Whys" template must be initiated within the QMS within 48 hours.

---

## 9. Training Requirements

All personnel identified in the roles and responsibilities matrix (Section 3) must complete and document the following training:

| Training Module | Audience | Method | Frequency | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **ISEC-001: HIPAA & Data Privacy in Clinical Research** | All Validation Personnel | LMS (Workday) | Annual | Privacy Officer |
| **CLTR-105: GMLP & Clinical Validation SOP** | Clinical Data Science, Biostatistics, QA | Instructor-Led + LMS Exam | Initial (before first access), then biennial | VP of Clinical AI |
| **HITL-210: Clinical Review Panel Operations** | Adjudication Panel Members | Hands-on Workshop (Veeva Vault) | Initial, then on version change | Clinical Data Science Lead |
| **BIA-101: Algorithmic Bias & Equity Principles** | All Clinical AI Staff | E-Learning | Annual | VP of Diversity & AI Ethics |

Training records shall be maintained in Workday. The Quality Assurance Manager is responsible for auditing training compliance quarterly. Validators who are non-compliant with any mandatory training module shall have their access to the Snowflake `VALIDATION_SCHEMA` temporarily revoked until compliance is achieved.

---

## 10. Related Policies and References

### 10.1 Internal Meridian Policies

| Document ID | Title | Relationship |
| :--- | :--- | :--- |
| SOP-AI-009 | General Purpose AI Model Development | Defines development lifecycle pre-validation. |
| SOP-SEC-006 | Information Security Incident Response | Governs breach notification and escalation processes. |
| SOP-PRV-003 | De-identification and Anonymization of Clinical Data | Defines the technical methodology used in Gate 2. |
| SOP-DQ-022 | Data Quality Assurance for Clinical Data Warehouses | Defines the DQ checks mandated in Gate 2. |
| SOP-FIN-015 | Revenue Cycle Algorithm Validation | Analogous validation SOP for financial (non-clinical) models. |
| SOP-HR-100 | Disciplinary and Corrective Action Policy | Consequences of non-compliance. |
| GLOS-CORP-001 | Meridian Corporate Glossary | Enterprise definition of terms. |

### 10.2 External References

- ISO 13485:2016 - Medical devices — Quality management systems
- ISO 14971:2019 - Medical devices — Application of risk management
- Good Machine Learning Practice for Medical Device Development (GMLP) Guiding Principles
- CONSORT-AI and SPIRIT-AI reporting guidelines
- ITU-T/WHO FG-AI4H deliverables

---

## 11. Revision History

| Version | Date | Author | Description of Change |
| :--- | :--- | :--- | :--- |
| 1.0 | 2021-09-12 | J. Hendricks | Initial SOP creation for ChestXray-AI v1. |
| 2.0 | 2022-11-15 | A. Okafor | Major revision: Introduced Gates 1-6 lifecycle, added RACI matrix, and mandated silent trials. |
| 3.0 | 2023-06-01 | L. Kim (QA) | Integration with Veeva Vault QMS; added mandatory diversity stratification; removed waterfall validation terminology. |
| 3.1 | 2023-10-20 | M. Dubois | Clarified de-identification standards for EU patient data; added CE marking prerequisites per EU MDR transition period. |
| 3.2 | 2024-01-10 | A. Okafor | Updated escalation protocol contact points (replaced retired CSO role); added Kafka topic naming convention for silent trial logs. |
| 3.3 | 2025-05-23 | A. Okafor | Scheduled review cycle update; refined "Monitoring" Section 7.1 thresholds; added explicit SOTA benchmarking clause in Section 4.5; updated Technical Documentation linkage to reflect ISO 13485 integration for EU AI Act readiness; updated training ID references. |