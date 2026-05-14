---
sop_id: "SOP-CLIN-005"
title: "Diagnostic AI Accuracy and Calibration"
business_unit: "Clinical AI Products"
version: "3.8"
effective_date: "2024-06-03"
last_reviewed: "2025-02-11"
next_review: "2025-08-19"
owner: "Dr. Aisha Okafor, VP of Clinical AI Products"
approver: "Dr. Priya Patel, Chief Medical Officer"
classification: "Internal"
regulations:
  - "EU AI Act"
  - "NIST AI RMF"
status: "Active"
---

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the framework, methodologies, and operational cadence for ensuring the analytical accuracy, clinical validity, and statistical calibration of all diagnostic artificial intelligence (AI) models deployed within the Clinical AI Platform at Meridian Health Technologies, Inc. The primary objective of this document is to mandate a continuous evidence-generation lifecycle that ensures model outputs are not only statistically robust but also clinically safe and generalizable across diverse patient populations. This SOP defines the mechanisms by which Meridian ensures that sensitivity, specificity, positive predictive value (PPV), negative predictive value (NPV), and expected calibration error (ECE) remain within pre-specified clinical acceptance criteria throughout the model’s operational lifecycle.

### 1.2 Scope

This SOP applies to all personnel involved in the design, development, validation, deployment, and post-market surveillance of machine learning algorithms classified as "Diagnostic AI" or "Patient Risk Scoring" within the **Clinical AI Products** business unit, under the leadership of Dr. Marcus Rivera, Chief AI Officer, and Dr. Aisha Okafor, VP of Clinical AI Products. This includes:

- **Product Coverage:** All AI/ML models holding FDA 510(k) clearance (e.g., Pneumothorax Detection v4.2, Chest X-ray Triage v2.1) and CE-marked models under EU MDR (e.g., CT Stroke Volume Quantification v3.0). This SOP also extends to "Software as a Medical Device" (SaMD) algorithms in pre-submission phases.
- **Platform Coverage:** Models deployed on the `Meridian-AI-Engine` inference platform, including real-time, batch, and on-premise containerized deployments at customer sites.
- **Data Scope:** Calibration and accuracy monitoring apply to ground-truth comparison against radiologist-adjudicated labels in the Meridian Clinical Data Lake (MCDL) and silent trial emulations.
- **Exclusions:** This SOP does not cover the credit risk scoring models within HealthPay Financial Services, nor the population health risk stratification algorithms in MedInsight Analytics that are explicitly non-diagnostic and not regulated as medical devices.

---

## 3. Roles and Responsibilities

The following matrix delineates the responsibilities for the execution and oversight of this SOP.

| Role | Designation | Responsibility |
|---|---|---|
| **Executive Sponsor** | Dr. Priya Patel, Chief Medical Officer | Ultimate authority on clinical safety and off-label use risks; approves high-risk calibration exceptions. |
| **SOP Owner** | Dr. Aisha Okafor, VP of Clinical AI Products | Maintains SOP relevance; authorizes deviations; oversees the Strategic AI Accuracy Review (SAAR). |
| **Algorithm Owners** | Lead MLEs (Machine Learning Engineers) | Responsible for the technical calibration of specific model fingerprints; executing retraining runs; maintaining the `Model Fingerprint Registry`. |
| **Clinical Validation Lead** | Director of Biostatistics & Clinical Evidence | Designs and executes silent prospective trials; authorizes the statistical analysis plan (SAP); signs off on subgroup calibration analyses. |
| **MLOps Engineering** | MLOps Team Lead | Maintains the `Meridian-AI-Engine` monitoring infrastructure; manages the automated drift detection pipelines; ensures data logging integrity. |
| **Data Curation** | Clinical Data Operations Lead | Ensures the quality, diversity, and integrity of ground-truth labels in the Meridian Clinical Data Lake (MCDL); manages adjudication queues. |
| **Quality Assurance (QA)** | Regulatory QA Manager | Independent review of calibration documentation prior to regulatory submissions (e.g., 510(k) Specials, MDR Technical File updates). |

### 2.2 Acronyms

| Acronym | Definition |
|---|---|
| **AUROC** | Area Under the Receiver Operating Characteristic curve |
| **AUPRC** | Area Under the Precision-Recall Curve |
| **ECE** | Expected Calibration Error |
| **FN / FP** | False Negative / False Positive |
| **HITL** | Human-in-the-Loop |
| **MCDL** | Meridian Clinical Data Lake |
| **NPV** | Negative Predictive Value |
| **PPV** | Positive Predictive Value |
| **PSI** | Population Stability Index |
| **SAAR** | Strategic AI Accuracy Review |
| **SAP** | Statistical Analysis Plan |
| **TN / TP** | True Negative / True Positive |

---

## 4. Policy Statements

Meridian Health Technologies maintains the following high-level policy commitments to govern the accuracy and calibration of diagnostic AI:

- **POL-005.1: Calibration-as-Safety.** A well-calibrated model is a prerequisite for clinical safety. Probabilistic outputs must reflect the true empirical likelihood of the predicted condition. An overconfident misdiagnosis constitutes a significant patient safety hazard.
- **POL-005.2: Performance Guarantee.** All actively marketed Clinical AI models must maintain a per-subgroup sensitivity and specificity within 5% absolute margin of their FDA-cleared or CE-marked labeling claims.
- **POL-005.3: Lifecycle Monitoring.** Accuracy and calibration are not static properties. Continuous, automated monitoring shall be active for every deployed model instance to detect silent performance decay.
- **POL-005.4: Silent Trial Integrity.** Prospective silent trials provide the highest tier of evidence for post-market performance. Tampering with silent trial configurations, unblinding, or premature analysis without Clinical Validation Lead authorization is strictly prohibited.
- **POL-005.5: Data Integrity.** No calibration analysis shall be performed on data that has not passed the `MCDL-Data-Quality-Gate` (refer to SOP-DATA-019 for data pipeline validation).
- **POL-005.6: Risk Stratification.** All diagnostic AI models shall be assigned a criticality tier (Tier 1: Acute/Triage, Tier 2: Diagnostic Aid, Tier 3: Workflow Optimization). Accuracy monitoring SLAs are tier-dependent.
- **POL-005.7: Subgroup Transparency.** Performance metrics must be transparently reported not just globally, but for key demographic and clinical subgroups as defined in the model-specific Statistical Analysis Plan (SAP).

---

## 5. Detailed Procedures

### 5.1 Model Fingerprinting and Baseline Registration

Upon completion of internal clinical validation but prior to any regulatory submission or customer deployment, every PRSA must undergo a formal fingerprinting process to establish the performance baseline.

**Procedure Steps:**
1.  **Hold-out Locking:** The Algorithm Owner, in conjunction with the Clinical Data Operations Lead, permanently locks the hold-out test dataset. This dataset must be temporally and geographically distinct from the training and validation sets.
2.  **Baseline Metric Calculation:** Execute the `baseline-metrics-runner` pipeline against the locked hold-out set to calculate the following:
    - AUROC, AUPRC
    - Sensitivity, Specificity, PPV, NPV at the operating threshold
    - Calibration curve (reliability diagram) binned by decile
    - Expected Calibration Error (ECE)
3.  **Fingerprint Record:** Log the SHA-256 hash of the model weights, the environment configuration, the dataset version hash, and the full metric output into the `Model Fingerprint Registry` (Snowflake table: `CLINICAL_AI.MODEL_REGISTRY.FINGERPRINT_BASELINES`).
4.  **Threshold Lock:** The clinical operating threshold (e.g., the specificity target corresponding to 95% sensitivity) is locked and tagged as the `clinical-op-point` in the MLflow model registry.

### 5.2 Prospective Validation: Silent Trial

Prior to obtaining a CE marking or initial launch at a new clinical site, or upon any major model version upgrade, a silent trial must be executed.

**Procedure Steps:**
1.  **Trial Design & SAP:** The Clinical Validation Lead drafts a Silent Trial Protocol and Statistical Analysis Plan (SAP) using the template `CLIN-FORM-005-A`. This SAP must pre-specify primary and secondary endpoints, subgroup analysis plans (e.g., by sex, age bands [18-40, 41-65, 65+], and relevant co-morbidities), and stopping rules for safety.
2.  **Integration:** MLOps deploys the "shadow mode" container to the target clinical site's PACS/DICOM router. The model ingests live clinical data, generates predictions, and stores them in an encrypted local log, but **no results are displayed to clinicians**.
3.  **Ground Truth Adjudication:** Concurrently, the patient cases are routed to the adjudication queue. Two independent radiologists from the Meridian Clinical Network provide blinded reads. In cases of discordance, a third senior subspecialty radiologist provides the tie-breaking ground-truth label.
4.  **Lock & Analyze:** Upon reaching the pre-specified sample size, the Clinical Validation Lead locks the dataset. The Algorithm Owner runs the `validation-report-generator` to compare silent trial performance against the baseline fingerprint.
5.  **Pass/Fail Gate:** If the lower bound of the 95% Confidence Interval for sensitivity and specificity falls below the acceptance criteria defined in the SAP, the model is blocked from go-live. The Executive Sponsor must be notified within 24 hours via the `SAAR-Alert` channel.

### 5.3 Post-Market Continuous Monitoring (Live Environment)

All active diagnostic models undergo continuous, automated metric computation.

1.  **Real-time Data Ingestion:** The `Meridian-Observability-Bus` streams live inference payloads (input features) and model outputs (logits, probabilities, final class labels) to a dedicated, HIPAA-compliant Kafka topic.
2.  **Opportunistic Labeling:** The `MCDL-Label-Connector` attempts to link every inference event to a subsequent confirmed clinical outcome (e.g., pathology report, procedure code, subsequent imaging study confirming or ruling out the finding) within a 30-day lookback window.
3.  **Windowed Metric Calculation:** Every 24 hours, a scheduled Spark job calculates a 7-day and 30-day rolling window of key metrics (Sensitivity, Specificity, ECE, PSI) on the "opportunistically labeled" cohort. This is considered a Tier-2 monitoring signal.
4.  **Threshold Breach Alerts:** If the 7-day rolling sensitivity or specificity drops by >5% absolute percentage points compared to the registered baseline, a `P2 - Degraded Accuracy` incident is automatically created in PagerDuty and routed to the MLOps and Algorithm Owner teams.
5.  **Quarterly Deep Dive (Silent Re-Emulation):** Every calendar quarter, the Clinical Validation Lead selects a stratified random sample of 5,000 cases from the previous quarter's opportunistic log. These are pushed to the adjudication queue for formal dual-reader ground truth assignment. This constitutes the gold-standard "re-emulation" analysis. The formal Quarterly Calibration Report is generated from this process using the template `CLIN-FORM-005-B`.

### 5.4 Calibration and Reliability Curve Analysis

Probability calibration shall be assessed using reliability diagrams.

**Procedure Steps:**
1.  **Prediction Bucketing:** Predictions from the re-emulation cohort are split into deciles (0.0-0.1, 0.1-0.2, ..., 0.9-1.0).
2.  **Fraction of Positives:** For each bin, compute the true fraction of positive cases.
3.  **ECE Calculation:** Calculate ECE as the weighted average of the absolute difference between the mean predicted probability and the true fraction of positives for each bin. The weight is the proportion of samples in the bin.
4.  **Mitigation Trigger:** If ECE exceeds 0.05 (5%), the Algorithm Owner must initiate a recalibration protocol. This typically involves applying Platt Scaling or Isotonic Regression on a recent validation cohort, followed by a regression test suite against the locked hold-out set to ensure discrimination (AUROC) has not been harmed.

### 5.5 Subgroup Performance Analysis

Global metrics can obscure material, clinically significant performance degradation in patient subgroups.

**Procedure Steps:**
1.  **Mandatory Subgroups:** The `validation-report-generator` and Quarterly Calibration Report (Form `CLIN-FORM-005-B`) must always break down performance for the following subgroups, provided the subgroup sample size n > 50 to satisfy statistical power minimums:
    - **Biological Sex:** Male, Female.
    - **Age Bands:** 18-44, 45-64, 65-80, 80+.
    - **Imaging Device Vendor:** Siemens, GE, Philips, Canon.
    - **Key Co-morbidity:** Diabetic vs. Non-diabetic (for applicable models).
2.  **Disparity Threshold:** If the absolute difference in Sensitivity or Specificity between any two subgroups within a protected characteristic category (e.g., Male vs. Female) exceeds 3%, the Algorithm Owner must log a `PERF-DISPARITY-1` finding.
3.  **Root Cause Analysis (RCA):** An RCA must be completed within 14 calendar days of the finding. The RCA must determine if the cause is pre-analytical (data shift), analytical (model bias), or post-analytical (labeling bias in ground truth).
4.  **Remediation:** If identified as model bias, a targeted re-training or fine-tuning intervention using a re-balanced dataset must be scoped and executed within 45 days.

---

## 6. Controls and Safeguards

### 6.1 Technical Controls

| Control ID | Control Description | Implementation |
|---|---|---|
| **TEC-005.01** | **Immutable Audit Logging:** Every model prediction payload, including the `model_version`, `fingerprint_hash`, `input_hash`, `prediction_score`, and `threshold_result`, must be immutably logged to a blockchain-backed ledger. | Applied via the `Meridian-Audit-Sidecar` container injected into every inference pod. |
| **TEC-005.02** | **A/B Canary Deployment:** No new model version shall receive 100% of inference traffic immediately. Traffic must be split 5%/95% (New/Old) for a minimum of 72 hours to validate operational stability and preliminary metric parity. | Configured in `Istio` virtual service routing rules. |
| **TEC-005.03** | **Input Data Validation:** Incoming DICOM headers and pixel data must pass the `CLIN-DATA-SCHEMA-V2` validator. Non-conformant studies are rejected before inference and logged as `SOP-DATA-PROTOCOL-019` exceptions. | Performed by the `Meridian-Input-Validator` sidecar. |
| **TEC-005.04** | **Operating Point Safeguard:** The clinical operating point threshold in the model serving layer is immutable. A change to this threshold requires a security-incident-level change control ticket. | Enforced via HashiCorp Vault secret management for threshold parameters. |

### 6.2 Administrative and Procedural Controls

| Control ID | Control Description | Cadence |
|---|---|---|
| **ADM-005.01** | **Strategic AI Accuracy Review (SAAR):** A formal governance meeting to review the Quarterly Calibration Reports, open RCA findings, subgroup disparity logs, and decommissioning timelines. | Quarterly |
| **ADM-005.02** | **Labeling Reconciliation:** Adjudication discordance rates between primary readers must be tracked. If discordance exceeds 15%, the Clinical Data Operations Lead must reassess the adjudication protocol. | Monthly |
| **ADM-005.03** | **SOP Deviation Logging:** Any departure from the procedures in Section 5 must be logged as an exception. | Per Instance |

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs)

The health of the Clinical AI Platform regarding accuracy and calibration is measured against these core metrics:

| KPI | Metric | Target | Monitoring Window |
|---|---|---|---|
| **Clinical Discrimination** | AUROC Regression | < 3% absolute drop from baseline | 30-day rolling & Quarterly Re-emulation |
| **Clinical Sensitivity** | Sensitivity (Recall) | ≥ FDA-cleared label - 5% | 30-day rolling & Quarterly Re-emulation |
| **Clinical Specificity** | Specificity | ≥ FDA-cleared label - 5% | 30-day rolling & Quarterly Re-emulation |
| **Model Calibration** | Expected Calibration Error (ECE) | < 0.08 | Quarterly Re-emulation |
| **Data Stability** | Population Stability Index (PSI) | < 0.2 | 7-day rolling |
| **Subgroup Equity** | Max pairwise subgroup Δ in F1-score | < 5% | Quarterly Re-emulation |

### 7.2 Dashboards and Reporting

- **Live AI Operations Dashboard (Grafana):** Displays real-time request volume, latency p99, error rates, and the 30-day rolling opportunistic sensitivity/specificity trends. Accessible to MLOps and Clinical Engineering.
- **Quarterly Accuracy & Calibration Report (PDF):** Generated semi-automatically via the `CLIN-FORM-005-B` template, stored in the `QualityDocs` Veeva Vault system. This is the record of truth for regulatory audits. Distribution includes the SAAR committee, Clinical Risk Management, and the VP of QA.
- **Model Health Scorecard (Tableau):** A high-level aggregated view of all active models, showing RAG (Red/Amber/Green) status against KPIs. Reviewed by the Clinical AI Leadership team weekly.

---

## 8. Exception Handling and Escalation

### 8.1 Model Accuracy Deviation

Any event where automated monitoring or a silent re-emulation reveals a statistically significant breach of a KPI target triggers the Accuracy Deviation Protocol.

**Procedure:**
1.  **Automated Quarantine:** The MLOps lead immediately isolates the "amber" or "red" model version. New deployments to additional customer sites are halted. A client communication is drafted by the VP of Clinical AI Products.
2.  **Severity Classification:**
    - **SEV-3 (Minor Drift):** ECE or PSI targets breached, but clinical sensitivity/specificity remain within bounds. Action: Scheduled recalibration at next maintenance window.
    - **SEV-2 (Moderate Performance Dip):** Specificity or Sensitivity drop >5% but <10% absolute. Action: Immediate RCA; silent trial initiated; rollback to previous stable fingerprint prepared.
    - **SEV-1 (Critical Failure):** Drop >10% or evidence of a clinically dangerous systematic error (e.g., specific mass being systematically missed). Action: Emergency shutdown of the model `model-rollback-or-kill`; direct notification to Dr. Priya Patel; preliminary adverse event filing to regulatory bodies via the Quality Assurance team.
3.  **RCA Documentation:** All SEV-2 and SEV-1 events require a formal Root Cause Analysis document (`CLIN-FORM-005-RCA`) filed within 72 hours of incident resolution.

### 8.2 Exception Handling

Requests to temporarily deviate from monitoring cadences (e.g., during a planned PACS upgrade at a major customer site) must be approved by the SOP Owner (Dr. Aisha Okafor). An exception request must include the specific procedure being waived, a technical justification, a client impact assessment, and a defined expiration date. Unauthorized deviations discovered during internal audits will be treated as a non-conformance event per corporate QA policy.

---

## 9. Training Requirements

All personnel assigned to roles in Section 3 must complete the following training curricula. Successful completion is tracked via the `Meridian-LMS` (Litmos).

### 9.1 Training Curriculum

| Training Module Code | Module Title | Target Audience | Frequency | Assessment |
|---|---|---|---|---|
| **CLIN-TRN-005.1** | SOP-CLIN-005 Core Awareness & Workflow Integration | All Section 3 Roles | Annually | Multiple-choice quiz (Pass Mark: 90%) |
| **CLIN-TRN-005.2** | Advanced Calibration Techniques & Silent Trial Design | Algorithm Owners, Clinical Validation Lead | Annually | Case-study based assignment |
| **CLIN-TRN-005.3** | Fairness and Subgroup Clinical Validity | Algorithm Owners, Clinical Validation Lead, Data Curation | Annually | Completion certificate required |
| **CLIN-TRN-005.4** | Practical MLOps for Clinical Observability | MLOps Engineering, Algorithm Owners | Bi-annually | Hands-on lab via Katacoda |

### 9.2 Compliance

Access to production model registries and customer deployment tooling is automatically suspended for any user whose assigned training modules exceed their renewal due date, enforced via an LDAP group policy integration with the `Meridian-LMS`.

---

## 10. Related Policies and References

### 10.1 Internal Meridian SOPs

| SOP ID | Title | Relationship |
|---|---|---|
| SOP-DATA-019 | Data Pipeline Validation and Quality Gates | Defines the data integrity checks prerequisite to accuracy monitoring. |
| SOP-SEC-009 | Incident Response and Breach Notification for Connected Devices | Governs the emergency security response that may preempt standard calibration cycles. |
| SOP-CLIN-001 | Clinical Algorithm Development Lifecycle Model | Governs the Phases 1-4 of model development from ideation to go-live. |
| SOP-CLIN-008 | Post-Market Surveillance and Vigilance Reporting | Governs the handling of adverse clinical events potentially linked to AI failure. |
| SOP-VM-022 | Vendor Offboarding and Contract Termination | Governs the decommissioning of third-party ground truth labeling services. |

### 10.2 External Standards and Templates

- **CLIN-FORM-005-A:** Silent Trial Protocol and SAP Template
- **CLIN-FORM-005-B:** Quarterly Calibration Report Template
- **CLIN-FORM-005-RCA:** Root Cause Analysis for Algorithmic Variance
- **ISO 13485:2016** — Quality Management Systems for Medical Devices
- **ISO 14971:2019** — Application of Risk Management to Medical Devices
- **Good Machine Learning Practice (GMLP) Guiding Principles** — Guiding Principles 7, 8, and 10

---

## 11. Revision History

| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 3.8 | 2025-02-11 | Dr. Aisha Okafor | Clarified subgroup sample size minimums (n>50) in Section 5.5; Updated severity classification thresholds in Section 8.1 to align with revised clinical risk matrix; Updated Section 3 roles to reflect new MLOps reporting structure. |
| 3.7 | 2024-12-18 | Dr. Aisha Okafor | Added ECE threshold to KPI table in Section 7.1 per post-audit corrective action; Refined the definition of A/B Canary Splits from 10% to 5% traffic in Section 6.1. |
| 3.6 | 2024-08-30 | Dr. Marcus Rivera | Introduced formal Subgroup Performance Analysis procedure (Section 5.5) as part of regulatory harmonization; Updated SOP references from deprecated version SOP-DEV-014 to SOP-CLIN-001. |
| 3.5 | 2024-06-03 | Dr. Aisha Okafor | Major revision upon obtaining CE marking; Expanded calibration procedures to include ECE as primary metric alongside reliability diagrams; Formalized silent trial template; Updated training curriculum codes. |
| 3.4 | 2024-02-15 | Dr. Sarah Chen | Minor revision; Updated opportunistic labeling lookback window from 14 days to 30 days in Section 5.3; Updated MCDL URL endpoints. |