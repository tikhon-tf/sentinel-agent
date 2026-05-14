---
sop_id: "SOP-AIML-013"
title: "Experiment Tracking and Reproducibility"
business_unit: "AI/ML Engineering"
version: "4.0"
effective_date: "2024-01-25"
last_reviewed: "2025-12-12"
next_review: "2026-06-02"
owner: "Dr. Marcus Rivera, Chief AI Officer"
approver: "David Park, VP of Engineering"
classification: "Internal"
regulations:
  - "EU AI Act"
  - "NIST AI RMF"
  - "SR 11-7"
status: "Active"
---

# Standard Operating Procedure: Experiment Tracking and Reproducibility
**SOP-AIML-013 | Version 4.0**

## 1. Purpose and Scope

### 1.1 Purpose
The purpose of this Standard Operating Procedure (SOP) is to establish the mandatory requirements, processes, and controls for experiment tracking, artifact lineage, and computational reproducibility across all AI/ML engineering activities at Meridian Health Technologies, Inc. This policy ensures that every model development experiment—from initial exploratory data analysis through candidate model selection—is systematically logged, versioned, and reproducible by authorized personnel, thereby supporting model validation, regulatory auditability, and intellectual property protection.

### 1.2 Scope
This SOP applies to all Meridian personnel, contractors, and third-party vendors engaged in the design, training, evaluation, or tuning of machine learning models that are intended for deployment in, or in support of, any Meridian business line, specifically:

| Business Line | Products In Scope | Risk Classification |
|---|---|---|
| Clinical AI Platform | Clinical decision support, diagnostic imaging analysis, patient risk scoring, adverse event prediction | High-Risk AI |
| HealthPay Financial Services | Credit scoring models, fraud detection, medical lending underwriting, claims automation | SR 11-7 Covered Model |
| MedInsight Analytics | Population health models, care gap identification, outcomes prediction | Standard Model |
| Meridian SaaS Platform | Infrastructure-level auto-scaling, anomaly detection, cost optimization AI | Operational AI |

This SOP covers the full model development lifecycle up to, but not including, formal model validation for production deployment (see SOP-AIML-015, *Model Validation and Approval*).

### 1.3 Applicability
All Data Scientists, Machine Learning Engineers, ML Research Scientists, and AI Product Managers must comply with this SOP. Compliance is audited monthly by the AI Governance team and is included in the SOC 2 Type II control framework for the Meridian SaaS Platform.

---

## 2. Definitions and Acronyms

| Term/Acronym | Definition |
|---|---|
| **Experiment** | A single, logically bounded unit of model development work, defined by a unique hypothesis, dataset version, model architecture, and hyperparameter configuration. |
| **Run** | A single execution of an experiment with a specific set of parameters, producing a discrete set of metrics and artifacts. |
| **Artifact** | Any file produced during a run, including model weights (`.pt`, `.pb`, `.h5`), serialized tokenizers, feature importance plots, evaluation reports, and serialized model cards. |
| **Lineage** | The complete, auditable chain of data, code, configuration, and environment that produced an artifact. |
| **Reproducibility** | The ability for an independent, authorized party to execute the same code, on the same data, in an equivalent computational environment, and obtain results within a predefined tolerance. |
| **Model Registry** | The centralized MLflow Model Registry instance, designated as the system of record for all Meridian models. |
| **Gold Dataset** | An immutable, versioned dataset approved by the Chief Medical Officer (for clinical data) or VP of Financial Services (for financial data) used as a canonical evaluation baseline. |
| **Seed Standard** | The Meridian-mandated random seed (`42`) and seeding protocol defined in Section 4.4. |
| **HITL** | Human-in-the-Loop. |
| **PHI** | Protected Health Information. |
| **SME** | Subject Matter Expert. |

---

## 3. Roles and Responsibilities

The following responsibility assignment matrix applies to all activities under this SOP.

| Role | Responsibility | Accountable Party |
|---|---|---|
| **Data Scientist / ML Engineer** | Execute experiments, log parameters/metrics/artifacts in real-time, document code in designated repositories, adhere to seed standard. | Individual Contributor |
| **AI Product Manager** | Define experiment objectives and success criteria; ensure alignment with product requirements; approve experiment hypotheses. | Dr. Aisha Okafor (Clinical AI) / Robert Liu (HealthPay) |
| **Lead ML Engineer** | Review experiment logs weekly for completeness and adherence to standard; approve artifact promotion to Model Registry; conduct spot-checks for reproducibility. | AI/ML Engineering Team Leads |
| **Data Quality Steward** | Certify datasets used in experiments; maintain the Gold Dataset registry; ensure PHI is properly de-identified before use in development environments. | VP of IT Operations, Samantha Torres |
| **AI Governance Analyst** | Perform monthly audits of experiment tracking completeness; generate compliance reports; track KPI metrics for the AI Governance Committee. | Chief Compliance Officer, Thomas Anderson |
| **VP of Clinical AI Products** | Approve any deviation from the Gold Dataset; authorize clinical model experiments. | Dr. Aisha Okafor |
| **VP of Financial Services** | Approve any deviation from the Gold Dataset for credit/lending models; authorize financial model experiments. | Robert Liu |
| **Chief AI Officer** | Own this SOP; approve exceptions >30 business days; chair bi-annual AI reproducibility review. | Dr. Marcus Rivera |
| **DevOps / MLOps Engineer** | Maintain the experiment tracking infrastructure (MLflow, Kubeflow); ensure compute environment snapshotting; manage artifact storage immutability in S3. | VP of Engineering, David Park |

---

## 4. Policy Statements

### 4.1 Mandatory Experiment Logging
Every experiment run must be logged to the centralized Meridian Experiment Tracking System (MLflow), hosted at `mlflow.internal.meridian.tech`. Runs are immutable upon completion. Logging must occur via the Meridian-standard MLflow Python client library. Manual CSV or spreadsheet-based tracking is strictly prohibited for any model intended for production or regulatory review.

### 4.2 Artifact Immutability
All artifacts produced by an experiment run and logged to the Model Registry are immutable. Any modification requires creating a new run under a new experiment ID with full lineage traceability.

### 4.3 Reproducibility Baseline
All experiments must be reproducible within 180 calendar days from the run completion date. Reproducibility is demonstrated by re-executing the committed code against the registered dataset hash in an equivalent environment and achieving primary metrics within ±2% absolute tolerance.

### 4.4 Random Seed Standard
The Meridian Seed Standard mandates a fixed global random seed of `42` for all Python-based experiments using libraries including NumPy, PyTorch, TensorFlow, and Python's built-in `random` module. All experiment logs must include a `random_seed` parameter tag set to `42`. Any deviation from this seed requires pre-approval via the exception process in Section 8.

### 4.5 Environment Capture
The full computational environment must be captured and logged with every run. This includes, at minimum: base Docker image SHA digest, pip/conda environment export, and AWS EC2 instance type or SageMaker training job details.

### 4.6 Traceability for Financial Models
All experiments supporting HealthPay Financial Services credit scoring, fraud detection, or lending models are subject to supplementary documentation requirements as described in SOP-FS-102, *Model Risk Management for Financial Products*. Experiment logs for these models must link explicitly to the corresponding model documentation package.

---

## 5. Detailed Procedures

### 5.1 Experiment Pre-Initiation

**5.1.1 Hypothesis Registration**
Prior to initiating any experiment run, the responsible Data Scientist or ML Engineer must create an experiment entry in the MLflow Tracking Server containing:
- **Experiment Name**: Follow the naming convention `[BusinessUnit]_[ProjectCode]_[ModelName]_[YYMMDD]`. Example: `CLINICAL_PRJ-042_DiabeticRetinopathyDetector_250112`.
- **Hypothesis Statement**: A concise, testable statement describing the expected outcome.
- **Success Criteria**: Quantified primary and secondary metrics with target thresholds.
- **Dataset Reference**: The Meridian Data Catalog ID for the dataset version to be used.

This must be reviewed and approved by the AI Product Manager via the MLflow UI comment mechanism before any compute resources are provisioned.

**5.1.2 Dataset Verification**
The Data Scientist must verify that the specified dataset version is the current approved Gold Dataset or has a valid exception approved per Section 8. For any experiment involving PHI, the engineer must confirm that the target environment is within the Meridian PHI-permitted boundary (AWS VPC `phdata-prod` with ID `vpc-0a1b2c3d4e5f6`) and that data is accessed via the tokenized service (HashiCorp Vault path `secret/meridian/database`).

### 5.2 Experiment Execution and Logging

**5.2.1 Run Initialization**
At the start of each run, the training script must call the Meridian-standard initialization function `meridian.mlops.init_run()` (from the internal package `meridian-mlops>=3.1.0`), which automatically:
1. Retrieves the current Git commit SHA and verifies the working tree is clean (no uncommitted changes). If the working tree is dirty, the run will abort unless the `--allow-dirty` flag is set for exploratory work. Runs with `--allow-dirty` are tagged with `production_intent: false` and cannot be promoted to the Model Registry without a full re-run.
2. Sets random seeds globally per the Meridian Seed Standard.
3. Captures environment details and logs them to MLflow as tags.
4. Retrieves the dataset from the Data Catalog using the registered ID, validates its checksum against the catalog, and logs the dataset version to MLflow.

**5.2.2 Parameter Logging**
All tunable parameters must be logged using `mlflow.log_params()`. This includes, and is strictly limited to:
- All hyperparameters (learning rate, batch size, epochs, dropout rate, optimizer, loss function, etc.).
- Feature set version or feature engineering pipeline hash.
- Dataset split ratio.
- Any environment variable that impacts model behavior.

**5.2.3 Metric Logging**
Metrics must be logged after each epoch (or equivalent training interval) using `mlflow.log_metrics()` with the `step` parameter. At minimum, the following must be tracked:
- **Primary Model Metric**: Loss function value (training and validation).
- **Business-Relevant Metrics**: For classification—AUROC, AUPRC, F1-score, sensitivity, specificity. For regression—MSE, MAE, R².
- **Bias and Fairness Metrics**: Demographic Parity Difference and Equalized Odds Difference across the protected attributes identified during the dataset certification process. These must be calculated using the Meridian Fairness Toolkit (`meridian.fairness.metrics`).

**5.2.4 Artifact Logging**
Upon run completion, the following artifacts must be logged to MLflow via `mlflow.log_artifact()`:
1. **Complete Model Card**: A markdown file (`model_card.md`) conforming to the Meridian Model Card Template (TEMPLATE-AIML-005), detailing intended use, out-of-scope use, training dataset summary, evaluation results, ethical considerations, and quantitative fairness analysis.
2. **Serialized Model**: In the format prescribed by the serving infrastructure (e.g., `model.pkl`, `pytorch_model.bin`, `saved_model.pb`).
3. **Evaluation Plots**: Confusion matrices, ROC curves, calibration plots, and SHAP summary plots.
4. **Feature Importance Artifact**: SHAP values or equivalent stored as a CSV artifact.
5. **Environment File**: `environment.yml` or `requirements.txt` with exact pinned versions.

### 5.3 Post-Execution and Peer Review

**5.3.1 Peer Review Submission**
Within 5 business days of the final run in an experiment, the Data Scientist must submit the experiment for peer review. The review is facilitated through the MLflow UI's "Review Request" feature. The reviewer is automatically assigned based on the project's pre-defined code ownership file in the central repository.

**5.3.2 Peer Review Checklist**
The designated Lead ML Engineer reviewer must verify the following within 3 business days:
- [ ] Hypothesis is clearly stated and success criteria are quantified.
- [ ] All parameters are logged; no "magic number" constants are unexplained in code.
- [ ] Metrics include fairness metrics.
- [ ] Model card is complete and accurate.
- [ ] Environment is fully captured.
- [ ] Code is checked in with a tag matching the MLflow `git_commit` tag.
- [ ] Results are reproducible when the reviewer re-executes the code (spot-check frequency: 1 in every 5 experiments reviewed). If a spot-check fails reproducibility criteria, the experiment is rejected.

Upon approval, the reviewer sets the `review_status` tag to `APPROVED` and adds a comment with their Meridian SSO ID.

### 5.4 Artifact Promotion to Model Registry

**5.4.1 Promotion Criteria**
Only runs with `review_status: APPROVED` and `production_intent: true` can be promoted to the Model Registry. Promotion is performed using the `meridian.mlops.promote_run()` function, which:
1. Registers the model in the MLflow Model Registry under the stage `Staging`.
2. Triggers a notification to the MLOps team for automated staging deployment and integration testing.

**5.4.2 Registry Annotations**
Upon registration, the Data Scientist must add the following metadata to the Model Registry entry:
- **Business Unit** tag.
- **Regulatory Classification** tag: `High-Risk AI`, `SR-11-7-Covered`, `Standard`, or `Operational`.
- **Retraining Cadence**: e.g., `Quarterly`, `Triggered-by-Drift`.

---

### 5.5 Procedure: Demonstrating Reproducibility

This procedure is executed during the semi-annual AI reproducibility review, led by the Chief AI Officer, and during any audit triggered by an adverse regulatory finding.

**Step 1: Selection**
The AI Governance Analyst randomly selects 10% of all experiments logged in the preceding 6 months. Selection is stratified by Business Unit. A random seed for selection is publicly posted to the internal audit channel.

**Step 2: Re-execution**
The original author (or a designated engineer if the author has separated from Meridian) clones the exact Git commit SHA logged in the run. They provision a new compute environment using the logged Docker image SHA digest. They execute the training script with the exact parameters logged.

**Step 3: Verification**
The new run produces a new MLflow run ID. The reproducibility evaluation script (`meridian.mlops.verify_reproducibility`) compares the primary metrics of the new run against the original run. If the absolute percentage difference (APD) is ≤2% for all primary metrics, the experiment is deemed "Reproducible." If the APD is >2% and ≤5%, the result is "Partially Reproducible" and requires a written explanation. If the APD is >5%, the result is "Not Reproducible," and a Root Cause Analysis (RCA) must be initiated per Section 8.4.

---

### 5.6 Procedure: Financial Model Documentation Package Assembly

For HealthPay Financial Services models subject to SR 11-7 (per SOP-FS-102), the experiment tracking data in MLflow is the source of truth for assembling the model documentation package.

**Step 1: Documentation Bootstrap**
The Data Scientist executes the `meridian.mlops.generate_doc_package()` function, specifying the winning experiment run ID. This function programmatically extracts all logged parameters, metrics, and the model card from MLflow and populates the Model Documentation Template (TEMPLATE-FS-009).

**Step 2: Component Assembly**
The documentation must include the following sections sourced directly from MLflow:
- **Model Description**: From the MLflow experiment description and model card.
- **Development Data Summary**: Sourced from the Data Catalog reference logged as a run parameter.
- **Performance Metrics**: The final epoch metrics logged in MLflow.
- **Feature Importance**: The SHAP CSV artifact must be included as an appendix.

**Note on SR 11-7 Coverage**: The documentation template will capture the model's overall performance statistics, the training data source, and the feature list. For ongoing monitoring, the experiment documentation should link to the relevant operational dashboards (per SOP-AIML-018). However, specific thresholds for ongoing monitoring performance degradation (e.g., alerting triggers for PSI > X or AUC drop > Y) are not defined within this documentation package, but are presumed to be covered by the separate model risk appetite statement.

---

### 5.7 Template: Model Card (TEMPLATE-AIML-005)

Every experiment run must log a `model_card.md` artifact conforming to this template.

```markdown
# Model Card: [Model Name]

## Model Details
- **Run ID:** [MLflow Run ID]
- **Experiment ID:** [MLflow Experiment ID]
- **Owner:** [Meridian SSO ID]
- **Date:** [YYYY-MM-DD]
- **Version:** [SemVer]
- **Model Type:** [e.g., ResNet-50, XGBoost]
- **Framework:** [PyTorch, TensorFlow, scikit-learn]

## Intended Use
- **Primary Use Case:** [Brief description from Product Manager-approved hypothesis]
- **User Group:** [e.g., Radiologist Assistants, Credit Underwriters]

## Out-of-Scope Use
- [List specific prohibitions, e.g., "Not for pediatric patients under 12," "Not for mortgage origination"]

## Training Data
- **Dataset Name and Version:** [Meridian Data Catalog ID]
- **Data Period:** [Date range of training data]
- **Preprocessing Pipeline Hash:** [DVC pipeline hash or equivalent]

## Evaluation Results
- **Primary Metric:** [Metric Name]: [Value]
- **Secondary Metrics:** [Comma-separated list of Name: Value pairs]
- **Fairness Metrics:**
  - Demographic Parity Difference: [Value]
  - Equalized Odds Difference: [Value]

## Ethical Considerations
- [Summary of any identified biases, fairness trade-offs, and mitigation steps taken]

## Quantitative Analysis
- **Calibration:** [Brier Score or Reliability Diagram reference to artifact]
- **Feature Importance Top-5:** [List]

## Environmental Impact
- **Training Duration (wall clock):** [Hours]
- **Compute Instance Type:** [e.g., p3.2xlarge]
- **Estimated Carbon Footprint (gCO2eq):** [From MLflow-CarbonMeter plugin]
```

### 5.8 Procedure: Gold Dataset Exception Request

**Step 1: Initiation**
The Data Scientist identifies that the Gold Dataset is insufficient for the experiment hypothesis (e.g., requires a different time cohort or additional feature set). They complete FORM-AIML-013-A, *Gold Dataset Deviation Request*, available in the Meridian Document Management System. The form requires:
- Justification for the deviation.
- Details on the alternative dataset source.
- Risk assessment for using non-certified data.

**Step 2: Approval Routing**
The form is digitally routed to:
1. Data Quality Steward (Samantha Torres) for technical data quality review.
2. Relevant Business VP (Dr. Aisha Okafor for Clinical, Robert Liu for HealthPay) for business risk approval.

**Step 3: Experiment Linking**
Upon approval, the form generates a unique Exception ID (`EXC-[YYYY]-[NNNN]`). The Initiator must log this Exception ID as a parameter tag in MLflow (`exception_id: EXC-2025-0123`). Without this tag, any model trained on non-Gold data is blocked from promotion to the Model Registry.

### 5.9 Procedure: Post-Mortem for Failed Reproducibility

When a reproducibility verification fails (APD >5% or run cannot be executed), this procedure is initiated by the Lead ML Engineer.

**Step 1: Immediate Quarantine**
Any model that fails a reproducibility audit and is currently in `Staging` or `Production` in the Model Registry is immediately tagged `quarantine: true`. The MLOps team is automatically notified to halt any active deployments of this model version.

**Step 2: Root Cause Analysis (RCA)**
The original author and Lead ML Engineer have 10 business days to produce an RCA document categorizing the root cause into one of:
- **Code Non-Determinism:** Unseeded random operations, non-deterministic CUDA operations, iterator dependency.
- **Environment Drift:** Original base Docker image retired or corrupted, dependency resolution conflict.
- **Data Drift:** Original dataset partition no longer logically reproducible (e.g., time-based split with a shuffled partition seed not tracked).
- **Procedure Violation:** Experiment was executed without adherence to the Meridian Seed Standard, or parameters were not fully logged.

The RCA is attached to the original MLflow run as an artifact.

**Step 3: Remediation Plan**
The Lead ML Engineer proposes a remediation plan to the Chief AI Officer. For code or environment issues, the plan includes a priority bug fix to the `meridian-mlops` package or training scripts. A retrospective experiment re-run is scheduled.

---

## 6. Controls and Safeguards

### 6.1 Technical Controls

| Control ID | Control Description | System/Tool | Enforcement |
|---|---|---|---|
| **TC-013-01** | **Committed Code Enforcement:** Training jobs on non-development SageMaker/Kubeflow contexts will abort if the Git working tree is dirty and the `--allow-dirty` flag is not present. | `meridian-mlops` pre-execution hook | Automated, Blocking |
| **TC-013-02** | **Artifact Immutability:** The S3 bucket backing the MLflow artifact store (`s3://meridian-ml-artifacts-prod`) has Object Lock enabled in Governance mode with a retention period of 365 days. Overwrites are denied. | AWS S3 Object Lock | Automated, Blocking |
| **TC-013-03** | **Environment Snapshot Mandate:** The `meridian-mlops.init_run()` function will fail with a `FatalEnvironmentError` if it cannot retrieve a valid Docker image SHA digest. | `meridian-mlops` | Automated, Blocking |
| **TC-013-04** | **Seed Deviation Detection:** A post-execution script scans MLflow tags. Any run with a `random_seed` tag not equal to `42` and lacking an approved exception ID tag is flagged to the AI Governance team weekly. | Custom AWS Lambda | Automated, Detective |
| **TC-013-05** | **Dataset Checkum Verification:** The `meridian-mlops.init_run()` function computes a SHA-256 hash of the retrieved dataset partition and compares it against the hash stored in the Data Catalog. A mismatch aborts the run. | `meridian-mlops`, Data Catalog Service | Automated, Blocking |
| **TC-013-06** | **PHI Boundary Enforcement:** ML training jobs launched outside the approved `phdata-prod` VPC (`vpc-0a1b2c3d4e5f6`) cannot resolve the production data warehouse connection string for PHI data. | AWS IAM and VPC Routing | Automated, Blocking |

### 6.2 Administrative Controls

| Control ID | Control Description | Cadence | Responsible Party |
|---|---|---|---|
| **AC-013-01** | **Monthly Experiment Log Completeness Audit:** AI Governance team pulls a report from MLflow of all runs in the past month. Any run missing >10% of defined required tags (see Section 5.2.2) is escalated to the Lead ML Engineer for remediation. | Monthly | AI Governance Analyst |
| **AC-013-02** | **Bi-Annual Reproducibility Audit:** Formal review of a stratified random sample of experiments per Section 5.5. Results presented to the Chief AI Officer. | Semi-Annually | Chief AI Officer |
| **AC-013-03** | **Quarterly Gold Dataset Review:** Data Quality Steward reviews the suitability of all Gold Datasets, retiring outdated versions and certifying new ones. | Quarterly | VP of IT Operations |
| **AC-013-04** | **Annual Access Certification:** Review of all user and service accounts with write access to the MLflow Tracking Server and S3 artifact bucket. | Annually | VP of Engineering |

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs)

The AI Governance team tracks the following quantitative metrics, sourced from a dedicated Kibana dashboard (Dashboard ID: `ML-Ops-Governance-Overview`) fed by MLflow API polling and AWS CloudTrail logs.

| KPI ID | Metric Description | Target Threshold | Measurement Cadence |
|---|---|---|---|
| **KPI-013-01** | **Experiment Run Logging Compliance (%):** Percentage of active compute instances (SageMaker Training Jobs, Kubeflow Pipelines) that successfully log to the central MLflow instance. | 100% | Real-time alerting |
| **KPI-013-02** | **Peer Review Cycle Time (Mean):** Mean time in business days from experiment submission to peer review `APPROVED` status. | ≤3 business days | Weekly |
| **KPI-013-03** | **Model Card Completeness (%):** Percentage of runs promoted to Model Registry in the last quarter with a model card artifact present. | 100% | Monthly |
| **KPI-013-04** | **Seed Deviation Rate (%):** Percentage of runs in a month with a `random_seed` tag value other than `42`. | <1% | Monthly |
| **KPI-013-05** | **Reproducibility Success Rate (%):** Percentage of experiments in the bi-annual audit achieving "Reproducible" status. | ≥90% | Semi-Annually |
| **KPI-013-06** | **Artifact Drift Detection (%):** Percentage of re-executed runs in the audit whose original logged dataset hash differs from the currently available dataset hash in the catalog. This metric informs proactive data pipeline health. | Metric tracked; no target threshold set | Semi-Annually |

### 7.2 Incident Thresholds
When a metric breaches its target threshold, the following occurs:
- **KPI-013-01 Breach:** Automated PagerDuty alert to MLOps on-call. Priority: `P1`.
- **KPI-013-03 Breach (<95%):** Notification sent to the Chief AI Officer and VP of Engineering. All model promotions are temporarily gated until compliance is restored.

### 7.3 Reporting
A monthly "AI Governance Compliance Report" is generated by the AI Governance Analyst, summarizing all KPIs, outstanding exceptions, and audit findings. The report is distributed to all AI/ML Engineering Lead Engineers, the Chief AI Officer, and the Chief Compliance Officer.

---

## 8. Exception Handling and Escalation

### 8.1 Exception Types and Approval Authority

| Exception Type | Definition | Approval Authority | Max Validity |
|---|---|---|---|
| **Seed Deviation** | Use of a random seed other than `42`. | Lead ML Engineer | 1 Experiment |
| **Gold Dataset Waiver** | Use of a non-certified dataset. | Business Unit VP (Okafor or Liu) + Data Quality Steward (Torres) | 1 Model Version |
| **Dirty Working Tree** | Use of `--allow-dirty` flag for prototype work. | Lead ML Engineer | 1 Run (non-promotable) |
| **Reproducibility Timeline Extension** | Request to extend the 180-day reproducibility window. | Chief AI Officer (Rivera) | +30 business days |
| **Logging System Bypass** | Circumventing MLflow for an experiment run. | Prohibited. No exceptions. | N/A |

### 8.2 Exception Request Process
1. The Initiator creates a Jira issue of type "Governance Exception" in the project `AIGOV`.
2. The issue includes: Specific SOP section reference, detailed justification, alternative controls, and a remediation plan with a deadline.
3. The issue is routed to the designated Approval Authority.
4. Upon approval, Jira generates a ticket ID (`AIGOV-NNNN`). This ID must be used as the `exception_id` tag in MLflow. Without the tag, automated controls will treat the run as non-compliant.

### 8.3 Periodic Exception Review
The AI Governance Committee reviews all open exceptions quarterly. Any exception granted a validity extension for more than two consecutive quarters is escalated to the Chief Risk Officer for an opinion on process adequacy.

### 8.4 Escalation for Repeated Non-Compliance
If an individual contributor accumulates three (3) or more substantiated violations of this SOP within a 12-month period, the AI Governance team formally escalates the matter to the individual's manager and the Chief AI Officer, recommending the revocation of access to production-eligible ML development environments until mandated retraining is completed.

---

## 9. Training Requirements

### 9.1 Mandatory Training Module
All personnel within the scope of Section 1.3 must complete the Learning Management System (LMS) course `LMS-ML-013: Experiment Tracking and Reproducibility Standards` with a score ≥90% on the final assessment.

### 9.2 Frequency
- **Initial Onboarding:** Must be completed within the first 5 business days of employment or assignment.
- **Refresher:** Annual retraining is required, coinciding with the employee's annual compliance training schedule. Refresher content will incorporate anonymized findings from the bi-annual reproducibility audits.

### 9.3 Roles-Based Supplemental Training
- **Clinical AI Data Scientists (Boston, Berlin):** Must complete `LMS-ML-013-CLIN` module on PHI-aware logging and de-identification verification before accessing `phdata-prod` VPC.
- **HealthPay Data Scientists:** Must complete `LMS-FS-102` module on model risk documentation standards, which includes a deep-dive on linking experiment logs to SR 11-7 documentation packages.

### 9.4 Training Compliance Tracking
Training completion is tracked automatically in the Meridian HRIS (Workday). Non-completion by the due date results in an automatic, temporary suspension of access privileges to the Meridian AWS Development and Production accounts (`dev` and `prod` OUs) until the training is completed.

---

## 10. Related Policies and References

### 10.1 Internal Meridian Documents
| SOP-ID / Document ID | Title |
|---|---|
| SOP-AIML-015 | Model Validation and Approval |
| SOP-DATA-001 | Data Classification and Handling Standard |
| SOP-DATA-003 | Data Catalog and Gold Dataset Management |
| SOP-FS-102 | Model Risk Management for Financial Products (SR 11-7) |
| SOP-AIML-018 | Model Monitoring and Drift Detection |
| SOP-INFRA-007 | MLOps Environment Provisioning and Container Management |
| POL-HR-042 | Employee Access and Privilege Control |
| TEMPLATE-AIML-005 | Meridian Model Card Template |
| TEMPLATE-FS-009 | Financial Model Documentation Package Template |
| TEMPLATE-AIML-013-A | Gold Dataset Deviation Request Form |

### 10.2 External References
- MLflow Documentation (Version 2.10+)
- Kubeflow Pipelines SDK Documentation
- AWS SageMaker Documentation: Security and Compliance
- Python Packaging Authority (PyPA): Pinning dependencies guide
- ISO/IEC 25010:2011 - Systems and software Quality Requirements and Evaluation (SQuaRE)

---

## 11. Revision History

| Version | Date | Author | Description of Changes |
|---|---|---|---|
| 1.0 | 2021-04-15 | J. Chen (MLOps Lead) | Initial release. Mandated MLflow for all Clinical AI experiments. |
| 2.0 | 2022-11-30 | M. Gupta (Sr. ML Engineer) | Major revision. Expanded scope to include HealthPay Financial Services. Added procedures for SR 11-7 documentation bootstrapping. Introduced Meridian Seed Standard. |
| 3.0 | 2023-08-17 | L. Patel (AI Governance Lead) | Incorporated mandatory fairness metrics logging. Defined Gold Dataset exception process. Added Model Card template. Transitioned from CSV artifact to standardized MLflow Model Registry. |
| 3.1 | 2023-10-05 | M. Gupta (Sr. ML Engineer) | Minor revision. Updated `meridian-mlops` package to v3.0. Updated artifact immutability control following S3 bucket migration. |
| 4.0 | 2024-01-25 | R. Fernandez (AI Governance Analyst) | Full document restructure for clarity. Moved to new document metadata standard. Added detailed RACI matrix. Formalized peer review checklist. Added semi-annual AI reproducibility review procedure and associated KPIs. Expanded AI/ML workload capacity forecasting for Clinical AI Platform. |