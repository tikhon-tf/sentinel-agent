---
sop_id: "SOP-CLIN-004"
title: "Patient Risk Scoring Algorithms"
business_unit: "Clinical AI Products"
version: "1.4"
effective_date: "2024-07-01"
last_reviewed: "2025-12-11"
next_review: "2026-06-26"
owner: "Dr. Aisha Okafor, VP of Clinical AI Products"
approver: "Dr. Priya Patel, Chief Medical Officer"
classification: "Internal"
regulations:
  - "EU AI Act"
  - "HIPAA"
  - "SR 11-7"
  - "NIST AI RMF"
status: "Active"
---

# Standard Operating Procedure: Patient Risk Scoring Algorithms

## 1. Purpose and Scope

This Standard Operating Procedure (SOP) establishes the governance framework, technical standards, and operational controls for the design, development, deployment, validation, and monitoring of Patient Risk Scoring Algorithms (PRSAs) within Meridian Health Technologies’ Clinical AI Platform. PRSAs are classified as high-risk AI systems under the EU AI Act and directly influence clinical and financial workflows across our provider, payer, and patient user base.

The purpose of this document is to ensure that all risk scores generated, whether predicting hospital readmission, sepsis onset, cardiovascular events, or patient deterioration, are clinically valid, statistically calibrated, free from unlawful bias, transparent, and subject to appropriate human oversight. This SOP operationalizes the principles of fairness, accountability, and transparency as mandated by the NIST AI Risk Management Framework 1.0 and aligns with our voluntary commitments under the White House AI Bill of Rights blueprint.

**Scope:** This SOP applies to the entire lifecycle of all PRSAs deployed or under development by the Clinical AI Products business unit. This includes algorithms hosted on the Meridian SaaS Platform, regardless of whether the end-user is a clinician, a health system administrator, or a payer. The scope covers:

- All predictive models that assign a numerical probability, categorical risk level, or composite score to an individual patient for a future clinical event.
- Models developed in-house, co-developed with academic medical center partners, and licensed third-party algorithms that are integrated into the Clinical AI Platform.
- All stages of the MLOps lifecycle: problem formulation, data acquisition and preprocessing, feature engineering, model training, validation (pre-deployment), deployment, monitoring (post-deployment), and decommissioning.

**Applies to:** All employees, contractors, consultants, and third-party vendors involved in the PRSA lifecycle, specifically including: Data Scientists, Machine Learning Engineers, Clinical Informaticists, Product Managers within Clinical AI Products, Software Engineers on the SaaS Platform team, the Clinical Validation Team staff, the Legal and Compliance Departments, and the AI Governance Committee.

This SOP is operational in all jurisdictions where Meridian Health Technologies operates, with specific accommodations detailed for our EU (EU AI Act, GDPR) and North American (HIPAA, SR 11-7) deployments. For matters related to data privacy, this SOP is subordinate to the GDPR and HIPAA Data Handling Policy [SOP-DATA-001]. For information security, this SOP is subordinate to the Information Security Management System (ISMS) Policy [SOP-SEC-002].

## 2. Definitions and Acronyms

| Term | Definition |
| :--- | :--- |
| **AUC-ROC** | Area Under the Receiver Operating Characteristic Curve. A primary metric for binary classification discrimination performance. |
| **Bias (Statistical)** | A systematic error in a model's prediction, measured as the difference between the average prediction and the true value. |
| **Bias (Fairness)** | Systematic, differential treatment or impact on individuals or groups based on protected characteristics (race, ethnicity, sex, age, etc.) that results in inequitable outcomes. Governed by our Algorithmic Fairness Standard [SOP-CLIN-005]. |
| **Calibration** | The agreement between a predicted risk probability and the observed frequency of the event. Assessed via Brier Score and calibration plots (reliability diagrams). |
| **Champion Model** | The currently active, deployed model in the production environment against which all inference requests are served. |
| **Clinical Risk Category** | A semantic mapping of a numeric risk score into clinically actionable tiers: `LOW`, `MODERATE`, `HIGH`, and `CRITICAL`. The thresholds for these categories are determined and validated per section 5.4 and approved by the Chief Medical Officer. |
| **Concept Drift** | A change in the underlying relationship between model inputs and the target variable, which renders the model's learned decision boundary obsolete. |
| **Data Drift** | A change in the statistical distribution of input features from the training baseline, without a corresponding change in the target variable relationship. |
| **Human-in-the-Loop (HITL)** | A governance design where algorithmic outputs provide a recommendation or score, but a qualified human practitioner retains ultimate decision-making authority. |
| **Net Reclassification Improvement (NRI)** | A metric quantifying how often a new risk model correctly reclassifies patients to a more appropriate risk category compared to a baseline model. |
| **Patient Risk Scoring Algorithm (PRSA)** | A computational process that ingests patient-level structured (e.g., labs, vitals, demographics) and/or unstructured (e.g., clinical notes, imaging reports) data to output a quantitative or qualitative assessment of the probability of a future clinical event for that specific patient. |
| **Protected Characteristics** | Attributes legally protected from discrimination, including but not limited to race, ethnicity, national origin, religion, sex, sexual orientation, gender identity, age, disability, and genetic information. |
| **Shadow/Challenger Model** | A parallel model that operates in the production environment, consuming live data and generating predictions that are logged but not surfaced to end-users. Used for safe evaluation of model updates before promotion. |

### 2.2 Acronyms

| Acronym | Full Text |
| :--- | :--- |
| **AUC** | Area Under the Curve |
| **AUPRC** | Area Under the Precision-Recall Curve |
| **EHR** | Electronic Health Record |
| **FFE** | Fairness, Fairness Evaluation |
| **FHIR** | Fast Healthcare Interoperability Resources |
| **HITL** | Human-in-the-Loop |
| **MLOps** | Machine Learning Operations |
| **NIST AI RMF** | National Institute of Standards and Technology Artificial Intelligence Risk Management Framework 1.0 |
| **NRI** | Net Reclassification Improvement |
| **PRSA** | Patient Risk Scoring Algorithm |
| **SMOTE** | Synthetic Minority Oversampling Technique |

---

## 3. Roles and Responsibilities

A RACI matrix (Responsible, Accountable, Consulted, Informed) defines the roles for the PRSA lifecycle.

| Activity / Decision | Data Science Lead | Clinical Informatics Dir. | VP, Clinical AI (Owner) | Chief Medical Officer | Quality Systems Mgr | AI Governance Comm. |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Problem Formulation & Feasibility** | R | C | A, R | C | I | I |
| **Data Quality Acceptance** | C | R | A | I | R | I |
| **Model Development & Training** | R | C | A | I | I | I |
| **Bias & Fairness Assessment (FFE 1.0)** | R | C | A | C | Consulted | Informed |
| **Pre-Deployment Clinical Validation** | C | R | A | R | R | I |
| **Model Card Approval** | R | R | A | Approver | I | I |
| **Go/No-Go Deployment Decision** | R | R | R | A, R | Informed | Informed |
| **Post-Deployment Monitoring (Ongoing)** | R | I | A | Informed | I | I |
| **Threshold Setting for Risk Categories** | C | R | A | A, R | I | Consulted |
| **Decommissioning Decision** | R | C | A | A, R | I | I |

**Detailed Role Responsibilities:**

- **Data Science Lead:** Responsible for the technical execution of model building, adherence to coding standards, executing bias assessments, authoring the Technical Model Card, and maintaining the production inference pipeline. This role manages the `champion` and `challenger` model artifacts in the Meridian Model Registry.
- **Clinical Informatics Director:** Responsible for the clinical plausibility review, defining clinically meaningful outcome variables, leading the Net Reclassification Improvement analysis, and bridging communication between data science and clinical end-users. This role has veto power over any model whose feature importance contradicts established medical evidence.
- **VP, Clinical AI Products (Dr. Aisha Okafor - SOP Owner):** Accountable for the entire PRSA portfolio, including resource allocation, risk acceptance for low-impact deviations, and ensuring this SOP reflects operational reality. Has final sign-off on the deployment schedule.
- **Chief Medical Officer (Dr. Priya Patel - SOP Approver):** Has ultimate medical accountability for patient safety. Approves all Clinical Risk Category thresholds and has sole decision-making authority for any HITL override process for `CRITICAL` risk scores.
- **Quality Systems Manager:** Manages the formal Design History File (DHF) for PRSAs classified as Software as a Medical Device (SaMD). Ensures quality gates are met per our internal Quality Management System (QMS).
- **AI Governance Committee:** An independent, cross-functional body that provides fiduciary oversight on high-risk AI. Reviews all fairness (FFE) assessment reports, approves all exceptions to this SOP, and serves as the final escalation point for unresolved model risk disagreements.

---

## 4. Policy Statements

Meridian Health Technologies is committed to the safe, equitable, and effective deployment of Patient Risk Scoring Algorithms. The following high-level policy statements are non-negotiable and form the operating principles for the Clinical AI Products business unit.

- **P-001: Clinical Utility and Safety First.** A PRSA shall be deployed only upon demonstration that its use provides a net positive clinical benefit over standard of care, as validated by a Net Reclassification Improvement (NRI) analysis approved by the Clinical Informatics Director. No model shall be deployed if it poses an unacceptable risk of patient harm, as determined by the Chief Medical Officer.
- **P-002: Mandatory Fairness Evaluation.** All PRSAs with a binary classification output must undergo a Fairness Evaluation (FFE 1.0) prior to any clinical pilot, in accordance with the NIST AI RMF MAP 1.0 function and SOP-CLIN-005. A model shall not be promoted to production if it exhibits statistically significant differential performance—defined as an Absolute Difference in True Positive Rate (`TPR_a - TPR_b`) greater than 5% or an Absolute Difference in False Positive Rate greater than 5%—between any two groups segmented by a protected characteristic, without a documented and approved clinical justification.
- **P-003: Human-in-the-Loop (HITL) Governance Mandate.** No `CRITICAL` clinical decision shall be fully automated. All risk scores that map to the `CRITICAL` Clinical Risk Category shall be delivered with a mandatory HITL override in the clinical workflow. The exact HITL mechanism for each model must be reviewed and approved by the Chief Medical Officer as part of the clinical validation package.
- **P-004: Complete Lifecycle Management.** Every PRSA, from conception to decommissioning, shall have a documented lifecycle stored in the Meridian Model Registry. No model shall run in production without an active and approved Model Card, as referenced in Section 5.6.
- **P-005: Data Provenance and Quality.** All datasets used for training, validation, and testing a PRSA must have a documented lineage and a signed Data Quality Acceptance Certificate from the Quality Systems Manager. The use of synthetic data must be explicitly noted, and its distribution validated against the real-world source data.
- **P-006: Right to Appeal.** The output of any PRSA, when used to deny, limit, or significantly affect a patient's access to clinical resources, care pathways, or financial assistance, shall be subject to a clear patient and provider appeal process, as operationalized in our Clinical Decision Support Governance Policy [SOP-CLIN-003].

---

## 5. Detailed Procedures

This section details the step-by-step, end-to-end MLOps lifecycle for PRSAs. Each sub-section represents a gated phase. Progression from one phase to the next requires completion of all specified deliverables and formal approval via the Meridian Model Governance Workflow in Jira (`MOD-` project).

### 5.1 Phase 0: Problem Formulation and Intended Use Definition

This phase is initiated by the creation of a Model Initiation Form (MIF), formally recorded as Jira issue type `MOD-Initiate`.

- **5.1.1 Stakeholder Kick-off:** The Product Manager must convene a kick-off meeting with the Data Science Lead, Clinical Informatics Director, a representative from the Quality Systems team, and a potential clinical end-user champion. The meeting must review the draft MIF.
- **5.1.2 Intended Use Statement:** A clear Intended Use Statement must be drafted and included in the MIF. This statement must specify:
    - The precise, codified clinical outcome to be predicted (e.g., "30-day all-cause unplanned inpatient readmission").
    - The target patient population (inclusion and exclusion criteria, e.g., "Adult patients aged 18-89 discharged from a general medicine service").
    - The intended clinical workflow context (e.g., "Score displayed to the attending hospitalist on the patient’s discharge summary screen to prompt a post-discharge follow-up order.").
    - The **Non-Intended Use** (e.g., "This score is NOT intended to be a sole determinant for denying skilled nursing facility placement.").
- **5.1.3 Feasibility Analysis:** The Data Science Lead must conduct a preliminary feasibility analysis using a retrospective data query from the Meridian Data Lake (platform: Databricks). The output must include:
    - Confirmation of sufficient sample size (>500 positive events) in the target population over the last 36 months.
    - An initial list of candidate features and their data provenance (source system, ETL pipeline).
    - A Data Readiness Score (0-100) as per the Data Quality Standard [SOP-DATA-002].
- **5.1.4 AI Governance Notification:** The Product Manager must formally notify the AI Governance Committee by filing the `MOD-Initiate` Jira issue. This serves as the initial entry into the Algorithmic Risk Register.

**Phase 0 Approval Gate:** VP, Clinical AI Products (Dr. Okafor) approves the MIF.

### 5.2 Phase 1: Data Acquisition, Preprocessing, and Audit Trails

- **5.2.1 Dataset Extraction:** Data Engineers must extract the final training and holdout datasets from the Meridian Data Lake using the approved feature list. The extraction script (`SQL` or `PySpark`) must be version-controlled in GitLab (repo: `clinai/prsa-queries`).
- **5.2.2 Data Split Strategy:** The Data Science Lead must implement a rigorous data splitting strategy to prevent information leakage. Records must be split at the **patient level** (not the encounter level), using a hashed `patient_id`. The standard split ratio is 60/20/20 for Training, Validation (Tuning), and Holdout (Testing) sets, respectively. The holdout set is to be cryptographically hashed and stored in a write-only S3 bucket, and its exact composition shall not be accessible by the development team until the final model evaluation in Phase 3.
- **5.2.3 Audit Logging for Data Access:** All direct, programmatic access to the training and validation datasets must be logged. The system of record for data access logging is the Meridian Data Access Gateway (MDAG). Logs must capture the following granular attributes: `actor_uid`, `resource_id` (dataset), `action` (read), `timestamp`, and `session_id`.
- **5.2.4 Handling Missingness:** A standardized imputation strategy must be defined and persisted as a scikit-learn or PySpark pipeline object. Median imputation is the default for continuous lab values. A novel "Missingness Indicator" binary feature must be created for each clinical feature with >5% missingness. The choice of imputation for any variable with >20% missingness must be clinically reviewed and approved by the Clinical Informatics Director.

**Phase 1 Approval Gate:** Quality Systems Manager signs the Data Quality Acceptance Certificate.

### 5.3 Phase 2: Model Training and Selection

- **5.3.1 Candidate Model Architectures:** The Data Science team is required to train at least three architecturally diverse candidate models to guard against confirmation bias. The standard slate is: (1) L1-Logistic Regression (clinical baseline), (2) XGBoost/Gradient Boosted Trees, and (3) a simple feed-forward Neural Network (MLP).
- **5.3.2 Hyperparameter Tuning:** Tuning must be performed on the dedicated Validation set using Bayesian Optimization (via `Optuna`). The optimization metric must be a multi-objective composite, prioritizing AUC-ROC, Brier Score (Calibration), and the Fairness Equality of Opportunity Difference (EEO_Diff), weighted as per the model's specific FFE plan.
- **5.3.3 Champion Selection:** The selection of the Champion Model cannot be based solely on AUC-ROC. The final model must represent the Pareto-optimal trade-off between discrimination (AUC), calibration (Brier Score 1.0), and fairness. The decision rationale must be documented in the Model Selection Report appended to the `MOD-Select` Jira issue.

**Phase 2 Approval Gate:** Data Science Lead and Clinical Informatics Director jointly approve the Model Selection Report.

### 5.4 Phase 3: Pre-Deployment Clinical Validation and Threshold Setting

This is the critical safety phase, led by the Clinical Informatics Director, independent of the core development team.

- **5.4.1 Holdout Set Evaluation:** The frozen Champion Model is applied by the Clinical Informatics Director to the untouched Holdout set. The results are recorded. No further tuning of the model is permitted after this evaluation.
- **5.4.2 Calibration Assessment:** A reliability diagram must be generated. The Brier Score must be calculated. A calibration-in-the-large (CITL) metric must be reported and must be <0.1. Any visual deviation >5% between the predicted risk and the observed event rate on the calibration curve must be investigated and explained.
- **5.4.3 Fairness Evaluation (FFE 1.0):** The model must be evaluated on the Holdout set, stratified by key groups based on race, sex, and age. The analysis must report True Positive Rate (Sensitivity), False Positive Rate, and Positive Predictive Value per group, along with 95% Confidence Intervals. Any statistically significant (p<0.05) and clinically meaningful (absolute difference >5%) disparity must be escalated to the AI Governance Committee with a Mitigation Plan.
- **5.4.4 Clinical Risk Category Thresholding:** The Clinical Informatics Director leads a structured workshop with at least three independent clinician subject-matter experts. Using the Holdout set predictions, the team must define the numeric cutoffs for `LOW`, `MODERATE`, and `HIGH` categories. The `HIGH`/`CRITICAL` boundary must be set targeting a minimum Positive Predictive Value (PPV) of 60% and a maximum False Positive Rate of 15%, unless otherwise justified. The thresholds are set by consensus. In case of a tie, the Chief Medical Officer holds the deciding vote.
- **5.4.5 Silent (Shadow) Deployment:** Before Go-Live, the full inference pipeline (feature extraction, preprocessing, prediction) is deployed to the production environment in `shadow` mode. Live traffic is ingested, predictions are generated and logged to a Kibana dashboard visible only to the development and validation teams, but no scores are surfaced in the EHR UI. This silent mode period lasts for a minimum of 14 days to monitor operational performance and latency.

**Phase 3 Approval Gate:** The Chief Medical Officer (Dr. Priya Patel) signs the Final Model Validation Report, formally approving the Clinical Risk Category thresholds.

### 5.5 Phase 4: Deployment and Human-in-the-Loop Integration

- **5.5.1 Promotion to Champion:** Upon CMO approval, the `shadow` deployment is promoted to the `champion` model in the Meridian Model Registry. The Kubernetes inference service (`k8s-inference-cluster-prod`) is updated, and traffic is switched to the new endpoint.
- **5.5.2 EHR Integration Workflow:** The risk score and its corresponding Clinical Risk Category must be surfaced to the clinician via our FHIR-compliant API into the EHR user interface.
    - For a `LOW` score: The category is displayed with basic explainability (Top 3 contributing features).
    - For a `MODERATE` score: An interactive "What If?" tool must be available for the clinician to explore the impact of modifying key modifiable features.
    - For a `HIGH` score: An interruptive alert is displayed. The clinician must actively acknowledge the alert by selecting an action (e.g., "Order follow-up", "Dismiss with reason").
    - For a `CRITICAL` score: The workflow is blocked. The UI displays "Clinical Action Required." This hard stop triggers a simultaneous page to the on-call clinical team lead. The clinician must manually override or accept the protocol recommendation. All HITL actions are logged with a `user_id`, `timestamp`, and `action_type` to the Meridian Audit Trail Service.
- **5.5.3 HITL Override Monitoring:** The frequency of overrides for `HIGH` and `CRITICAL` alerts is a critical safety KPI. A weekly report on override rates by user and by unit must be reviewed by the Clinical Informatics Director.

### 5.6 Phase 5: Ongoing Post-Deployment Monitoring

Post-deployment, the model is continuously monitored on a dedicated Observability stack using Evidently AI integrated with Datadog.

- **5.6.1 Model Performance Monitoring (Every Night, 02:00 UTC):** A nightly batch job retrieves the previous day's inference requests and links them to their ground-truth outcomes (from the EHR data warehouse with a 72-hour latency). It computes a rolling 7-day and 30-day AUC, Brier Score, and Precision-Recall. The dashboard refreshes by 06:00 UTC.
- **5.6.2 Drift Monitoring (Real-time):**
    - **Data Drift Detector:** Monitors the Population Stability Index (PSI) for the top 20 features. An alert (P1 SRE ticket) is triggered if the overall multivariate PSI > 0.2.
    - **Concept Drift Detector:** Uses a model-based approach. A lightweight linear classifier is trained hourly to distinguish between training and recent production data. If the classifier achieves an AUC > 0.6, a concept drift alert (P2) is raised.
- **5.6.3 Bias Drift Monitoring (Weekly):** A weekly batch job re-executes the FFE 1.0 analysis on a rolling 90-day production data window. Performance metrics stratified by protected characteristics are plotted on a control chart. An alert is raised if the difference between the highest and lowest TPR by group exceeds the 5% tolerance boundary for three consecutive weeks.

---

## 6. Controls and Safeguards

Meridian implements a defense-in-depth strategy of technical and administrative controls to operationalize NIST AI RMF Function 3 (Manage) and Function 4 (Govern).

### 6.1 Technical Controls

| Control ID | Description | NIST AI RMF Alignment |
| :--- | :--- | :--- |
| **T-CON-01** | **Immutable Model Registry.** All promoted model artifacts are stored in a WORM (Write Once, Read Many) compliant S3 bucket (MLflow Model Registry). Any change to a `champion` model requires a new version and full go/no-go approval. | MAP 3.4 |
| **T-CON-02** | **Adversarial Robustness Checks.** Before deployment, all neural network-based models must pass a basic Carlini-Wagner L2 adversarial attack test. The accuracy under attack must not degrade by more than 15% from the baseline. | MAP 3.1 |
| **T-CON-03** | **Input Schema Validation.** The production inference pipeline strictly enforces a versioned protocol buffer (`protobuf`) schema for all incoming feature tensors. Invalid data types or out-of-range values are rejected with a `4xx` error, logged, and set to a "missing" state which triggers the model's pre-trained imputation logic. | MAP 3.3 |
| **T-CON-04** | **Audit Trail for Inference.** Every single prediction call to the inference endpoint is logged to an immutable JSON ledger in Splunk. The log contains: `trace_id`, `timestamp`, `model_version`, `input_data_hash`, `output_score`, and `output_category`. | MAP 1.5 |

### 6.2 Administrative Controls

| Control ID | Description | NIST AI RMF Alignment |
| :--- | :--- | :--- |
| **A-CON-01** | **AI Governance Committee Review.** The Committee, as defined in Section 3, meets bi-weekly. It reviews all active high-risk registrations, exception approvals, and FFE escalation reports. | GOVERN 4.1 |
| **A-CON-02** | **Third-Party Model Vetting.** Any PRSA from a third-party vendor must undergo an identical technical validation and fairness evaluation as an internally developed model. The vendor's documentation showing training data demographics must map to our target deployment population's demographics (PSI < 0.1). | MAP 2.3 |
| **A-CON-03** | **Mandatory Model Card Documentation.** No model artifact may be registered in the Model Registry without an associated, approved Model Card. The Model Card must detail intended use, non-intended use, ethical considerations, evaluation results, and fairness caveats as per the Meridian Model Card Template [FRM-CLIN-101]. | MAP 1.2 |
| **A-CON-04** | **Transparency Notice.** All clinical notes generated or clinical workflows informed by a PRSA at the `HIGH` or `CRITICAL` level must include a standard transparency boilerplate: *"This clinical decision was significantly aided by an AI-based Patient Risk Score (vX.Y). Review the full model information by clicking here [link to Model Card]."* | GOVERN 5.5 |

---

## 7. Monitoring, Metrics, and Reporting

A robust operational and governance monitoring framework is in place, operationalizing NIST AI RMF MAP 5.1 (Monitor).

### 7.1 Key Model Performance Indicators (KPIs)

The following dashboards are maintained in Datadog and are continuously displayed on the Clinical AI Operations Center monitors.

| KPI | Target / Threshold | Alert Severity | Cadence |
| :--- | :--- | :--- | :--- |
| **Model Discrimination (AUC)** | 30-day rolling AUC > baseline AUC - 5% | P2 | Nightly Refresh |
| **Model Calibration (Brier Score)** | Weekly Brier Score < baseline Brier + 0.05 | P1 | Weekly Refresh |
| **Data Drift (Multivariate PSI)** | PSI < 0.2 | P1 | Real-time (Hourly) |
| **Fairness: TPR Disparity** | Max(Group_TPR) - Min(Group_TPR) < 0.05 | P2 (Soft), P1 (if persists 3 weeks) | Weekly Refresh |
| **HITL Override Rate** | `HIGH` alert override rate < 25% / `CRITICAL` override rate < 10% | P3 | Weekly Refresh |
| **Inference Pipeline Latency (p99)** | < 500ms | P2 | Real-time (5-min avg) |

### 7.2 Reporting Cadence

- **Automated Operational Reports (Weekly, every Monday 08:00 ET):** An auto-generated report from the Datadog dashboards is emailed to the Clinical AI Product Manager, Data Science Lead, and Clinical Informatics Director. It contains the week's KPI values and a trend line.
- **Clinical Performance Review (Monthly):** A dedicated 60-minute meeting chaired by the Clinical Informatics Director. This meeting reviews the prior month's HITL override patterns, adverse event reports linked to a PRSA, and the detailed results of the monthly fairness drift analysis. Minutes are formally recorded in the Meridian Quality Management System (Veeva Vault).
- **AI Governance Committee Quarterly Review:** The VP of Clinical AI Products presents a portfolio health summary to the AI Governance Committee. This review includes a consolidated risk register, all active exceptions, a summary of fairness analyses, and the decommissioning schedule for any legacy models.

---

## 8. Exception Handling and Escalation

Deviations from the standard procedures defined in Section 5 may be approved on a temporary basis to address unforeseen operational needs.

### 8.1 Exceptions

- **Request Initiation:** Any individual may initiate an exception request by filing a `MOD-Exception` issue in Jira. The request must detail the specific SOP section to be deviated from, the technical or business justification, a proposed compensating control, and a sunset date upon which the exception must be remediated.
- **Tiered Approval Model:**
    - **Low-impact exceptions** (e.g., 7-day extension to the silent deployment period) can be approved by the Data Science Lead.
    - **Medium-impact exceptions** (e.g., use of an unapproved feature, a request for emergency deployment) require joint approval from the VP, Clinical AI and the Chief Medical Officer.
    - **High-impact exceptions** (e.g., any deviation that increases the risk of unfair bias or patient harm, such as a waiver of a mandatory fairness assessment for launch) require a full vote by the AI Governance Committee.

### 8.2 Model Risk Escalations

A model risk is defined as any observation where the behavior of a deployed PRSA deviates from its expected and validated operational envelope.

- **Tier 1 (Technical/Operational Risk):** Includes P1/P2 alerts for data drift, pipeline latency, or an accuracy drop. Managed directly by the on-call MLOps engineer via the standard incident management process [SOP-OPS-011].
- **Tier 2 (Safety/Performance Risk):** A sustained deviation in model performance, a clinical override rate exceeding 50% for a `CRITICAL` alert, or a report of potential patient harm attributed to a PRSA. This must be immediately escalated by the Clinical Informatics Director to the VP, Clinical AI and the CMO. A Tiger Team (Data Science Lead, Clinical Informatics Director, Software Lead) is convened within 24 hours to recommend a rollback or emergency suspension.
- **Tier 3 (Governance/Ethical Risk):** A confirmed and sustained fairness violation, a discovery of data leakage, or a subpoena or regulatory inquiry. This is escalated immediately to the CMO, the General Counsel, and the Chair of the AI Governance Committee. The affected model is immediately switched to `shadow` mode, and its output is removed from the clinical UI pending the investigation's outcome.

---

## 9. Training Requirements

Meridian ensures all personnel involved in the PRSA lifecycle are qualified and aware of their responsibilities.

- **9.1 Role-Based Training Matrix:**
    - **Course `CLIN-101: PRSA Lifecycle Awareness`:** Mandatory within 30 days of hire for all employees covered by this SOP. Covers policy statements, HITL governance, and the right to appeal.
    - **Course `CLIN-201: Fairness in Practice`:** Mandatory for all Data Scientists, MLOps engineers, and Clinical Informaticists. An annual, 4-hour workshop using case studies, including hands-on evaluation of a sample model with protected characteristic stratification using the Meridian FFE toolkit.
    - **Course `CLIN-202: EU AI Act for Technical Builders`:** Mandatory for any Product Manager or technical lead working with models deployed in the EU. Covers the quality management system requirements and high-risk classification criteria.
- **9.2 Training Tracking:** All training is assigned and tracked through the Meridian Learning Management System (LMS), powered by Workday Learning. Completion records are linked to the employee’s HR profile. The Quality Systems Manager performs a monthly audit of training compliance for all personnel with active roles in the `MOD-` Jira project.
- **9.3 Clinical End-User Education:** For any new `HIGH` or `CRITICAL` risk score, a Clinical Workflow Education (CWE) module must be completed by all target clinicians on the hospital unit before go-live. The module includes a brief explanation of the model's logic, limitations, and the importance of avoiding automation bias. CWE completion rate must exceed 90% to lift the deployment freeze.

---

## 10. Related Policies and References

This SOP does not exist in isolation. It is an operational node in a wider governance framework.

### 10.1 Internal Meridian Policies

| SOP-ID | Title | Relationship to this SOP |
| :--- | :--- | :--- |
| **SOP-DATA-001** | GDPR and HIPAA Data Handling Policy | Supersedes; defines how PHI is handled, de-identified, and for which purposes. |
| **SOP-SEC-002** | Information Security Management System (ISMS) | Supersedes; defines access controls, endpoint security, and encryption standards. |
| **SOP-CLIN-003** | Clinical Decision Support (CDS) Governance | Defines the broad CDS lifecycle, including the right-to-appeal process referenced in P-006. |
| **SOP-CLIN-005** | Algorithmic Fairness Standard | Sub-procedure; details the FFE 1.0 methodology, stratification criteria, and mitigation strategies. |
| **SOP-CLIN-006** | Decommissioning of Clinical AI Algorithms | Defines the safe retirement of models at end-of-life. |
| **SOP-OPS-011** | Production AI System Incident Management | Defines the P1/P2 incident response process for MLOps alerts. |

### 10.2 External Standards and Frameworks

- **NIST AI RMF 1.0 (AI 100-1):** Primary framework for functions MAP (Map, Measure, Manage, and Govern).
- **EU AI Act:** Regulatory framework governing high-risk AI systems, with specific attention to Articles 9, 10, 15, and 17.
- **HIPAA Security and Privacy Rules (45 CFR 160, 164):** Governing the confidentiality, integrity, and availability of electronic Protected Health Information (ePHI).
- **ISO 13485:2016:** Medical Devices — Quality management systems — Requirements for regulatory purposes.

---

## 11. Revision History

This document undergoes a scheduled full review at a minimum biennially (every two years) or whenever a significant process change, regulatory finding, or post-incident review necessitates an update.

| Version | Date | Author(s) | Description of Changes |
| :--- | :--- | :--- | :--- |
| **1.0** | 2021-09-15 | M. Chen (former VP) | Initial release. Established basic MLOps lifecycle and validation gates for the Readmission Risk Model. |
| **1.1** | 2022-04-11 | K. Johansson (Data Sci Lead), L. Patel (CIO) | Major rewrite: added formal fairness evaluation (FFE 1.0) methodology in response to internal equity audit; introduced Clinical Informatics Director role to the RACI. |
| **1.2** | 2023-01-30 | A. Okafor (VP), K. Johansson | Integrated mandatory HITL workflow for all CRITICAL scores; added detailed data splitting strategy to Phase 1; rebased all MLOps references to the new Databricks/S3 lakehouse architecture. |
| **1.3** | 2023-09-01 | J. Reyes (Compliance), A. Okafor | Aligned entire SOP with NIST AI RMF 1.0 functions; introduced Model Card as a mandatory artifact; added sunset date requirement for all exceptions. |
| **1.4** | 2024-07-01 | A. Okafor, Dr. P. Patel (CMO) | Current release. Operationalized EU-specific controls; refined threshold setting workshop procedure; added Adversarial Robustness control (T-CON-02); expanded post-deployment drift monitoring to include concept drift detection. |