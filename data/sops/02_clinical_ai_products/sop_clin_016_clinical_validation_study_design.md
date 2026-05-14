---
sop_id: "SOP-CLIN-016"
title: "Clinical Validation Study Design"
business_unit: "Clinical AI Products"
version: "3.1"
effective_date: "2024-11-19"
last_reviewed: "2025-11-25"
next_review: "2026-05-19"
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

This Standard Operating Procedure (SOP) establishes the mandatory methodology for the design, execution, and reporting of clinical validation studies for all Artificial Intelligence and Machine Learning (AI/ML) systems developed or deployed by Meridian Health Technologies, Inc. (“Meridian”) within the Clinical AI Platform business unit. The purpose is to ensure that clinical performance claims are supported by robust, statistically sound, and ethically conducted evidence that demonstrates safety, efficacy, and fairness, thereby ensuring patient safety, maintaining regulatory compliance, and upholding Meridian’s market reputation as a trusted provider of high-risk AI systems.

### 1.2 Scope

This SOP applies to all personnel, contractors, and third-party partners involved in the lifecycle of Meridian’s Clinical AI products, from initial proof-of-concept through post-market surveillance.

**In-Scope Activities:**
- Prospective and retrospective clinical validation studies.
- In-silico validation using synthetic or benchmark datasets.
- Algorithm change validation requiring re-submission to regulatory bodies.
- Model performance monitoring studies conducted as part of post-market surveillance (as defined in SOP-PMS-004).
- Studies intended for submission to the U.S. Food and Drug Administration (FDA), European Notified Bodies under the EU Medical Device Regulation (MDR), or as part of EU AI Act conformity assessments.

**Out-of-Scope Activities:**
- Internal engineering unit tests and model smoke tests (covered in SOP-ENG-042).
- Financial models governed by SR 11-7 within HealthPay Financial Services (covered in SOP-FIN-008).
- Pure business analytics devoid of clinical decision support.

### 1.3 Applicability

This SOP is binding upon:
- **Clinical AI Products** (Dr. Aisha Okafor)
- **Clinical Affairs** (Dr. Priya Patel’s office)
- **Data Science & Biostatistics**
- **Regulatory Affairs** (General Counsel Maria Gonzalez)
- **Quality Management System (QMS) Team**

---

## 2. Definitions and Acronyms

| Term | Definition |
| :--- | :--- |
| **4A’s Framework** | Meridian’s internal AI governance model: Assess, Align, Acquire, Audit. |
| **Area Under the Curve (AUC)** | A performance measurement for classification models at various threshold settings. |
| **Bias-Variance Frontier** | The theoretical optimization limit between generalization error and training error. |
| **Clinically Meaningful Outcome (CMO)** | An endpoint directly related to patient symptoms, function, or survival. |
| **Concordance Index (C-index)** | A measure of rank-based predictive accuracy for time-to-event models. |
| **Equivalence Margin (δ)** | The pre-specified maximum clinically acceptable difference between AI and standard of care. |
| **Grouper Algorithm** | Meridian’s proprietary patient stratification logic deployed in AWS SageMaker Async Inference. |
| **High-Risk AI System** | As defined in EU AI Act Annex III, including AI intended to be used to detect, diagnose, or predict clinical deterioration. |
| **Net Reclassification Improvement (NRI)** | A metric quantifying the correctness of upward/downward movement in risk categories. |
| **Positive Predictive Value (PPV)** | The probability that subjects with a positive screening test truly have the condition. |
| **Snowflake SecureView** | Meridian’s governed data access layer used for cohort definition. |

---

## 3. Roles and Responsibilities

The following RACI (Responsible, Accountable, Consulted, Informed) matrix defines the governance structure for clinical validation studies.

| Activity | Principal Investigator (PI) | Biostatistics Lead | VP Clinical AI (Okafor) | Chief Medical Officer (Patel) | Data Governance (CISO) | Regulatory Affairs |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Study Protocol Authoring** | R | C | A | I | C | C |
| **Sample Size Justification** | C | R | C | A | I | I |
| **Anchoring Bias Review** | C | R | A | I | I | C |
| **Data Freeze & Extraction** | C | C | R | A | C | I |
| **Statistical Analysis Plan (SAP)** | I | R | A | C | I | C |
| **Final Report Sign-off** | I | C | R | A | I | C |
| **EU AI Act Conformity Alignment** | C | C | R | C | C | A |

**Specific Role Definitions:**
- **Biostatistics Lead (Dr. Elena Torres):** Sole authority to sign off on the Statistical Analysis Plan (SAP) prior to data freeze. Dr. Torres must validate the “Bias-Variance Frontier” stability metrics before unmasking comparative groups.
- **Clinical Interpretability Panel:** A sub-group of Dr. Patel’s Clinical Affairs team, responsible for verifying the clinical plausibility of every statistically significant endpoint prior to public disclosure.

---

## 4. Policy Statements

Meridian Health Technologies commits to the following policy principles in alignment with NIST AI RMF and internal quality standards for all covered clinical validation activities:

1.  **Pre-Registration Mandate:** Every prospective validation study must be registered on ClinicalTrials.gov or an equivalent public registry (e.g., ISRCTN) *before* the first patient is enrolled. The registration record must include a link to the unblinded SAP (per Policy-TRS-003).

2.  **NIST RMF Alignment (GOVERN 3.2):** Validation protocols must explicitly map risk controls to NIST AI RMF Subcategories **MAP 1.4 (Lifecycle Mapping)** and **MEASURE 2.3 (Independent Review)**. The protocol’s “Risk Mitigation” section shall itemize how each AI-specific bias (including automation complacency and anchoring bias) is proactively addressed through the 4A’s Framework.

3.  **EU AI Act Compliance (Article 17 & Annex IV Alignment):**
    - *Technical Documentation*: The Clinical Validation Report (CVR) serves as a core input to the Technical Documentation required by Annex IV. The Biostatistics Lead is responsible for including a dedicated section summarizing how the study design validates the stated Intended Purpose.
    - *Quality Management System*: Study design procedures shall reference the Meridian Quality Manual. Any deviation from protocol must be logged in the MasterQMS CAPA module (See Section 8).

4.  **Ethical Guardrails:** No validation study may intentionally deny a standard of care to a control arm if the standard is known to be life-sustaining. Studies utilizing retrospective data must obtain a waiver of consent from the Institutional Review Board (IRB) via the Advarra CIRBI Platform.

---

## 5. Detailed Procedures

### 5.1 Study Protocol Design

#### 5.1.1 Intended Purpose Definition (NIST MAP 1.1)
Before statistical design commences, the PI must lock the “Intended Purpose Statement” in Meridian’s QMS (Veeva Vault). The statement must explicitly detail:
- Disease/phenotype to be predicted or stratified.
- Patient population (age, sex, comorbidity profile).
- Clinical decision the model is intended to influence (Diagnostic, Prognostic, or Screening).

#### 5.1.2 Protocol Template Assembly
The Clinical Affairs Associate retrieves the Master Template (TMPL-CLIN-016a) from the Veeva Vault controlled-document library. **No local copies are permitted.**

**Mandatory Protocol Sections:**
1.  **Synopsis**: Structured table mapped to WHO Trial Registration Data Set.
2.  **Rationale and Background**: Literature review and prior internal pilot data.
3.  **Study Objectives**: Primary and secondary objectives mapped to AI performance metrics.
4.  **Study Design**: Parallel, cross-over, or stepped-wedge design justification.
5.  **Population**: Detailed inclusion/exclusion criteria. Data freeze logic (Snowflake timestamp).
6.  **Statistical Analysis Plan (SAP)**: (See Section 5.4).

### 5.2 Sample Size and Power Analysis

Biostatistics must execute a formal power analysis using the `pwr` and `caretEnsemble` packages in the Meridian Stats-Titan R environment (Version 4.2.3).

#### 5.2.1 Sample Size Inputs
- **Primary Endpoint Type:** Continuous (Mean Error), Binary (Sensitivity/Specificity), or Time-to-event (C-index).
- **Significance Level (α):** Fixed at 0.05 unless multiple comparison correction (Bonferroni-Holm) is applied.
- **Target Power (1-β):** Minimum 0.80 for FDA submissions; 0.90 for CE-mark Class III devices.
- **Equivalence Margin (δ):** Defined by the Clinical Interpretability Panel. Must not exceed 5% absolute difference in diagnostic accuracy for safety-critical endpoints.
- **Attrition Rate:** A 15% dropout buffer is mandatory for 12-week longitudinal studies.

#### 5.2.2 Minority Class Stratification (MEASURE 2.11)
To satisfy NIST AI RMF MAP 2.5 (Fairness), sample size calculations must include an explicit stratification plan ensuring sufficient statistical power for the model’s primary function *within* each demographic subgroup (Race, Ethnicity, Sex, Age-group). If population incidence is too low to achieve subgroup power, the protocol must document a synthetic augmentation strategy (Meridian’s SMOTE-GAN pipeline).

### 5.3 Endpoint Selection

#### 5.3.1 Hierarchy of Endpoints
Endpoints must follow a pre-defined hierarchy to prevent “cherry-picking”:
1.  **Clinically Meaningful Outcomes (CMOs):** e.g., 30-day re-admission rate, ICU transfer within 6 hours.
2.  **Clinical Surrogates:** e.g., Sepsis-3 criteria vs. clinician documentation timestamp.
3.  **Model Performance Metrics:**
    - **Discrimination:** AUC-ROC, C-index.
    - **Calibration:** Brier Score, Hosmer-Lemeshow goodness-of-fit test (p > 0.05 required per subgroup).
    - **Net Reclassification:** NRI > 0.10 with a 95% CI not crossing zero.
4.  **User-Centric Metrics:** Time-to-action, alert dismissal rate (measured via the Meridian *ClinOps Dashboard*).

### 5.4 Statistical Analysis Plan (SAP)

The SAP must be approved and frozen *prior to* the execution of the data extraction script. It must contain:

#### 5.4.1 Interim Analysis Rules
- **Lan-DeMets Alpha Spending Function:** O’Brien-Fleming boundaries for efficacy; Pocock boundaries for futility.
- AI-specific stop criteria: If the Grouper Algorithm produces calibration slope < 0.70 on a blinded interim sample, the study automatically triggers a CAPA investigation.

#### 5.4.2 Multiplicity Control
- Bonferroni correction for secondary endpoints.
- Gatekeeping protocol: Primary endpoint must meet superiority (p < 0.05) before sequential testing of secondary endpoints is considered valid.

### 5.5 Data Management and Lock (NIST MAP 3.2)

1.  **Cohort Definition:** Data engineers execute the “Grouper Algorithm” on `Snowflake SecureView`.
2.  **Pseudonymization:** All records are stripped of 18 PHI identifiers and assigned a Meridian *Internal Research Identifier (IRI)*.
3.  **Data Quality Check:** Biostatistics runs the `DataIntegrityCheck.R` script:
    - Completeness > 98% on primary covariates.
    - Heterogeneity check (clustering flags if Gini Impurity < 0.1).
4.  **Soft Lock:** Data is frozen for primary analysis (Read-only mode on Snowflake schema `CLIN_VAL_v311`).
5.  **Hard Lock:** Executed after final adverse event reconciliation for PMA studies. Only the Chief Medical Officer can authorize a database unlock after a Soft Lock.

### 5.6 Unblinding and Results Interpretation

Unblinding sequence:
1.  Biostatistics generates Group Labels (A vs. B).
2.  Clinical Interpretability Panel maps labels to AI-Expert vs. Standard-of-Care.
3.  Biostatistics executes the SAP.
4.  **NIST MEASURE 2.6 (Validity Check):** PI evaluates whether the AI’s performance aligns with the intended clinical context, checking for “laboratory bias” (overfitting to idealized retrospective environments).

---

## 6. Controls and Safeguards

### 6.1 Technical Controls

| Control ID | Control Description | Implementation Tool |
| :--- | :--- | :--- |
| **CLIN-016-C1** | Immutable audit trail for all modifications to the Post-Freeze analytical code repository. | AWS CodeCommit (Git) |
| **CLIN-016-C2** | Automated detection of distributional drift in validation data relative to training data. | Amazon SageMaker Model Monitor (Drift Threshold: Hellinger Distance > 0.15). |
| **CLIN-016-C3** | Cryptographic signing of final model weight hashes to prevent tampering between validation and deployment. | AWS Key Management Service (KMS) |
| **CLIN-016-C4** | Logical air-gap for statistical computing environments. | Stats-Titan RStudio Docker Container |

### 6.2 Administrative Controls

| Control ID | Control Description | NIST AI RMF Alignment |
| :--- | :--- | :--- |
| **CLIN-016-A1** | Segregation of duties: The Principal Investigator cannot approve their own protocol’s SAP. | GOVERN 2.2 |
| **CLIN-016-A2** | Annual mandatory “Fairness in AI Validation” refresher training for all Biostatistics staff. | GOVERN 1.6 |
| **CLIN-016-A3** | Pre-submission peer review of validation reports by an independent biostatistician external to the study team. | MEASURE 2.3 |

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs)

| Metric | Target | Measurement Frequency | Responsible Owner |
| :--- | :--- | :--- | :--- |
| **Protocol Deviation Rate** | < 2% of enrolled subjects | Monthly during active enrollment | Dr. Aisha Okafor |
| **SAP Deviations** | No unapproved SAP changes post-Data Freeze | Per-study audit | Biostatistics Lead (Torres) |
| **Calibration Drift (PSI)** | Population Stability Index (PSI) < 0.10 during Post-Market validation | Quarterly (SOP-PMS-004) | Dr. Priya Patel |
| **Subgroup Performance Equity** | AUC disparity ratio (Best/Worst demographic group) < 1.1 | Pre- and Post-Market | Clinical Affairs |

### 7.2 Reporting Cadence

- **Study Status Dashboard:** Real-time display on Meridian’s internal Confluence (accessible to Clinical AI Products, QA, and Executive Leadership). Includes enrollment curve, protocol deviation count, and NIST Govern Tracker status.
- **Monthly Clinical Affairs Review:** Dr. Okafor presents active validation study key figures to Dr. Patel.
- **Quarterly Management Review (QMR):** Aggregated KPI data is fed into the corporate QMR deck for EU AI Act conformity assessment artifact generation.

---

## 8. Exception Handling and Escalation

### 8.1 Minor Protocol Deviations

A deviation is classified as “Minor” if it does not affect the statistical power, participant rights, or primary endpoint integrity.
- **Examples:** Missed non-critical entry visit window (+/- 3 days), administrative transcription error corrected within 24 hours.
- **Handling:** Logged directly in Veeva Vault QMS by the Clinical Research Associate (CRA). Auto-approved by the system if the deviation logic matches the pre-defined “minor” matrix.

### 8.2 Major Protocol Deviations & Exceptions

A “Major” exception includes unblinding prior to Hard Lock, altering the primary endpoint, or adding N>10 subjects without a revised power analysis.
- **Process:**
    1.  PI files an Exception Request Form (ERF) in Veeva Vault (Form `FRM-016-EXC`).
    2.  Biostatistics Lead provides a Risk Impact Assessment within 48 hours.
    3.  Review by VP of Clinical AI (Dr. Okafor).
    4.  **Final Approval Authority:** Dr. Priya Patel (Chief Medical Officer). Any exception impacting EU safety endpoints must be forwarded to General Counsel, Maria Gonzalez, for Notified Body notification assessment.

### 8.3 NIST AI RMF Escalation (MANAGE 4.3)

If a model demonstrates clinically significant negative performance on a specific demographic subgroup during validation (Disparity Ratio > 1.2), an automatic “Hold for Clinical Review” tag is applied in the Model Registry.
- **Escalation Tier 1:** Biostatistics Lead + PI.
- **Escalation Tier 2:** VP Clinical AI + Chief Medical Officer.
- **Escalation Tier 3:** Chief Regulatory Counsel (Gonzalez) + CEO.
Timeline: Tier 1 must be engaged within 24 hours of algorithmic detection.

---

## 9. Training Requirements

| Role Profile | Training Module | Frequency | Tracking System |
| :--- | :--- | :--- | :--- |
| **Principal Investigator** | Clinical Validation SOP (016), GCP Refresher, EU AI Act Annex IV Authoring. | Bi-annual | Veeva Vault Vault Training |
| **Biostatistician** | Stats-Titan Environment Management, Imbalanced Data Handling, NIST MEASURE 2.3 Workshop. | Annual | Veeva Vault Vault Training |
| **Data Engineer** | Grouper Algorithm Logic, PHI Pseudonymization Pipeline (SOP-DATA-022). | Annual (with quarterly Q&A) | Absorb LMS |
| **Regulatory Affairs** | AI Lifecycle Document Mapping (Annex IV to QMS), FDA Pre-sub meeting training. | Ad-hoc (per device filing) | Veeva Vault Vault Training |

**Training Compliance Metric:** 100% assignment completion rate required for access to Snowflake `CLIN_VAL` schema. Access is provisioned via an automated IAM sync from the Veeva Vault training transcript.

---

## 10. Related Policies and References

| Internal Reference ID | Document Title |
| :--- | :--- |
| **SOP-PMS-004** | Post-Market Surveillance and Clinical Follow-up |
| **SOP-ENG-042** | Software Development Lifecycle for AI/ML Applications |
| **SOP-DATA-022** | Clinical Data Management and Pseudonymization |
| **Policy-TRS-003** | Clinical Trial Registration and Results Disclosure |
| **SOP-FIN-008** | Financial Model Validation (SR 11-7) |
| **QM-001** | Meridian Quality Manual |

| External Reference | Title / Version |
| :--- | :--- |
| **NIST AI 100-1** | Artificial Intelligence Risk Management Framework (AI RMF 1.0) - *Govern 3.2, Map 1.4, Measure 2.3, Manage 4.3* |
| **EU 2024/1689** | EU Artificial Intelligence Act - Article 17, Annex IV |
| **ICH E9 (R1)** | Statistical Principles for Clinical Trials: Addendum on Estimands |
| **FDA Guidance** | Clinical Decision Support Software (Final Guidance, Sept 2022) |

---

## 11. Revision History

| Version | Date | Author | Approver | Change Summary |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2022-03-15 | Dr. Aisha Okafor | Dr. Priya Patel | Initial release. Focused on retrospective validation study designs. |
| **2.0** | 2023-07-22 | Dr. Elena Torres (Biostatistics) | Dr. Aisha Okafor | Added mandatory prospective pre-registration clause. Introduced NIST AI RMF references for fairness and governance (MAP 2.5). Updated SAP templates. |
| **2.1** | 2024-01-10 | Dr. Rachel Smith (Clinical Affairs) | Dr. Aisha Okafor | Minor revision: Updated Data Freeze procedure to include Snowflake SecureView reference. Added “Grouper Algorithm” definition. |
| **3.0** | 2024-09-05 | Dr. Elena Torres | Dr. Priya Patel | Major revision for EU AI Act readiness. Restructured Section 5 to include explicit QMS linkage for Article 17 conformity. Expanded Annex IV technical documentation guidelines in Section 5.1. |
| **3.1** | 2024-11-19 | Dr. Aisha Okafor | Dr. Priya Patel | Post-CE marking amendment. Clarified Equivalence Margin definitions for MDR submissions. Updated roles for Regulatory Affairs regarding Notified Body communication. |