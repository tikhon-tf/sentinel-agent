---
sop_id: "SOP-AIML-016"
title: "Synthetic Data Generation"
business_unit: "AI/ML Engineering"
version: "4.1"
effective_date: "2024-02-05"
last_reviewed: "2025-06-08"
next_review: "2025-12-20"
owner: "Dr. Marcus Rivera, Chief AI Officer"
approver: "David Park, VP of Engineering"
classification: "Internal"
regulations:
  - "GDPR"
  - "HIPAA"
  - "NIST AI RMF"
status: "Active"
---

# Standard Operating Procedure: Synthetic Data Generation

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the governance framework, technical standards, and operational processes for the generation, validation, and use of synthetic data within Meridian Health Technologies, Inc. Synthetic data serves as a critical enabler for AI/ML model development, software testing, and analytics while reducing exposure risk associated with production data containing Protected Health Information (PHI) and personal data.

This SOP is designed to ensure that synthetic data produced and consumed across Meridian's business lines meets defined quality thresholds, preserves the statistical properties necessary for its intended use case, and maintains appropriate privacy guarantees. It operationalizes Meridian's commitment to privacy-by-design principles and supports compliance with applicable data protection regulations, particularly the General Data Protection Regulation (GDPR) for EU data subjects.

### 1.2 Scope

This SOP applies to:

- **All personnel** involved in the generation of synthetic datasets derived from production data sources containing PHI or personal data, including data engineers, ML engineers, data scientists, and research scientists.
- **All systems and pipelines** used to produce, store, or distribute synthetic data across Meridian's technology stack, including AWS SageMaker, Snowflake environments, Kubeflow pipelines, and MLflow tracking servers.
- **All business units** leveraging synthetic data: Clinical AI Platform, HealthPay Financial Services, MedInsight Analytics, and the Meridian SaaS Platform.
- **All data domains**: structured clinical data (EHR extracts, claims data, lab results), unstructured clinical data (physician notes, radiology reports), medical imaging data (DICOM, NIfTI), and financial transaction data.
- **All geographic regions** where Meridian operates: North America (Boston, Toronto) and the European Union (London, Berlin).

### 1.3 Out of Scope

- Synthetic data generated from publicly available datasets that have never been derived from Meridian production systems.
- Mock data created manually for unit testing that does not originate from production data sources.
- Third-party synthetic datasets procured from external vendors (see SOP-TPM-011, *Third-Party Data Acquisition*).

---

## 2. Definitions and Acronyms

| Term | Definition |
|---|---|
| **Synthetic Data** | Artificially generated data that mimics the statistical properties and structure of real-world data without containing actual individual-level records. Created algorithmically rather than measured or collected. |
| **Generative Model** | A machine learning model trained on real data to learn the underlying joint probability distribution, used to produce synthetic samples. May include GANs, VAEs, diffusion models, or LLM-based generators. |
| **Privacy Budget (ε, epsilon)** | A quantitative measure of privacy loss in differentially private data generation, expressed as epsilon. Lower epsilon values indicate stronger privacy guarantees. Meridian default: ε ≤ 1.0 for general use; ε ≤ 4.0 for approved high-utility use cases. |
| **Statistical Fidelity** | The degree to which synthetic data preserves the statistical properties, correlations, and distributions of the source data. Measured via quantitative metrics including Jensen-Shannon divergence, pairwise correlation difference, and propensity score overlap. |
| **Membership Inference Attack (MIA)** | A privacy attack method where an adversary attempts to determine whether a specific individual's record was included in the training dataset. Used as a validation metric for synthetic data privacy. |
| **Attribute Disclosure Risk** | The probability that an adversary can infer sensitive attributes about an individual from the synthetic dataset, even if record linkage is not possible. |
| **Holdout Validation** | A privacy evaluation technique where synthetic data is compared against a held-out test set (not used during generative model training) to detect overfitting and memorization. |
| **Data Synthesis Pipeline** | The end-to-end technical workflow encompassing source data extraction, preprocessing, generative model training, synthetic data generation, validation, and release. |
| **Use Case Owner** | The individual or team requesting synthetic data generation, accountable for defining fitness-for-purpose requirements and ensuring appropriate downstream use. |
| **Generative Adversarial Network (GAN)** | A class of generative models where two neural networks (generator and discriminator) are trained adversarially to produce high-fidelity synthetic data. |
| **Variational Autoencoder (VAE)** | A probabilistic generative model that learns a compressed latent representation of data and generates new samples by sampling from this latent space. |
| **Differential Privacy (DP)** | A mathematical framework providing formal privacy guarantees by introducing calibrated noise into algorithm outputs, ensuring that the inclusion or exclusion of any single individual's data does not significantly alter results. |
| **DP-SGD** | Differentially Private Stochastic Gradient Descent, a training algorithm that clips gradients and adds Gaussian noise to provide provable DP guarantees during model training. |
| **SDV** | Synthetic Data Vault, an open-source ecosystem for synthetic data generation and evaluation, used as Meridian's primary platform for tabular data synthesis. |
| **PHI** | Protected Health Information, as defined under applicable healthcare data protection frameworks. |
| **GDPR** | General Data Protection Regulation (Regulation (EU) 2016/679). |
| **DPO** | Data Protection Officer. |

---

## 3. Roles and Responsibilities

### 3.1 Responsibility Assignment Matrix

| Role | Responsibility | Accountable | Consulted | Informed |
|---|---|---|---|---|
| **Chief AI Officer (Dr. Marcus Rivera)** | Approves synthetic data generation for high-risk use cases; chairs AI Governance Committee review of generative models | X | | |
| **VP of Engineering (David Park)** | Approves synthetic data infrastructure; signs off on architecture changes | X | | |
| **Chief Privacy Officer / DPO (Dr. Klaus Weber)** | Approves privacy budgets; reviews DPIA for synthetic data generation involving EU data subjects; consults on GDPR Art. 35 compliance | | X | |
| **VP of Clinical AI Products (Dr. Aisha Okafor)** | Approves fitness-for-purpose criteria for clinical use cases | X | | |
| **VP of Financial Services (Robert Liu)** | Approves use cases for HealthPay synthetic financial data | X | | |
| **AI Ethics Lead (Reporting to CAIO)** | Validates fairness metrics on synthetic data; reviews for representational harm | | X | |
| **ML Engineering Manager** | Oversees synthesis pipeline execution; ensures adherence to technical standards; approves code-level changes | X | | |
| **Data Synthesis Engineer** | Executes synthesis pipelines; runs validation suites; documents model parameters and results | X | | |
| **Use Case Owner** | Defines requirements; submits use case approval request; confirms fitness-for-purpose of delivered synthetic data | X | | |
| **Information Security Officer** | Reviews and approves encryption controls; validates access management; authorizes data storage locations | | X | |
| **Compliance Officer (Thomas Anderson)** | Audits adherence to this SOP; reviews exception requests; maintains central log of approved use cases | | | X |
| **Data Steward** | Approves source data provisioning; ensures data catalog entries for synthetic datasets | | X | |

### 3.2 Key Decision Authorities

| Decision | Approval Authority | Delegable |
|---|---|---|
| Use case approval (non-clinical, low-risk) | ML Engineering Manager | Yes (to Senior Data Synthesis Engineer) |
| Use case approval (clinical, high-risk per EU AI Act Annex III) | Chief AI Officer + Chief Medical Officer | No |
| Privacy budget ε > 1.0 | Chief Privacy Officer / DPO | No |
| Privacy budget ε ≤ 1.0 | ML Engineering Manager | Yes (to AI Ethics Lead) |
| Release of synthetic data to external parties | Chief AI Officer + General Counsel | No |
| Architecture change to synthesis infrastructure | VP of Engineering | No |
| Exception to validation thresholds | Chief AI Officer + Chief Privacy Officer | No |

---

## 4. Policy Statements

### 4.1 General Principles

**P4.1.1** Meridian Health Technologies generates synthetic data as a privacy-enhancing measure to reduce reliance on production data containing PHI and personal data for AI/ML development, testing, and analytics activities.

**P4.1.2** All synthetic data generated from PHI or personal data sources shall undergo a formal use case approval process prior to synthesis pipeline initiation. No generative model shall be trained on production data without documented approval.

**P4.1.3** Meridian employs a defense-in-depth approach to synthetic data privacy, combining generative model safeguards, output validation, and access controls. Reliance on any single safeguard is insufficient.

**P4.1.4** Synthetic data shall never be treated as inherently privacy-safe. Every synthetic dataset must be empirically validated against privacy metrics before release to consumers.

**P4.1.5** The minimum necessary principle applies to source data provisioning for generative model training. Only fields, records, and populations required for the stated use case shall be included in training corpora.

### 4.2 Privacy and Data Protection

**P4.2.1** All generative models trained on data containing personal data of EU data subjects shall comply with GDPR requirements, including Article 25 (Data Protection by Design and by Default) and Article 35 (Data Protection Impact Assessment) where applicable.

**P4.2.2** A Data Protection Impact Assessment (DPIA) shall be conducted under the supervision of the Chief Privacy Officer / DPO prior to any synthesis pipeline where:

- Source data includes personal data of EU data subjects AND
- The synthesis involves large-scale processing of special categories of personal data per GDPR Article 9 (health data, genetic data) OR
- The synthesis involves systematic and extensive profiling.

**P4.2.3** Meridian's default differential privacy guarantee for synthetic data released to internal consumers is ε ≤ 1.0. Higher ε values (up to ε ≤ 4.0) require explicit documented justification and DPO approval.

**P4.2.4** The re-identification of individuals from synthetic data — whether through linkage attacks, inference, or any other method — is strictly prohibited. Any personnel who discover a potential re-identification pathway shall immediately report it to the Chief Privacy Officer and the CISO per the Incident Response Procedure (SOP-IS-005).

**P4.2.5** Synthetic datasets shall be clearly labeled and tagged in all data catalogs, feature stores, and MLflow tracking servers with the prefix `SYNTHETIC_` and metadata including generation date, source dataset, privacy budget, and approved use case ID.

**P4.2.6** Under GDPR Article 22 and the EU AI Act, individuals have the right not to be subject to decisions based solely on automated processing that produce legal effects. Models trained on synthetic data that are subsequently used in automated decision-making contexts must include human oversight mechanisms. Model cards shall document whether synthetic data was used in training and the privacy guarantees applied.

**P4.2.7** Data subjects exercising their rights under GDPR Article 17 (Right to Erasure) regarding source data shall have such requests evaluated for potential impact on any generative models previously trained on that data. While models themselves may not contain personal data post-training, model retraining may be required if the source data deletion substantively alters the representational validity of the remaining corpus. The DPO shall make this determination within 30 calendar days of the erasure request.

**P4.2.8** GDPR Article 30 (Records of Processing Activities) shall be maintained to include a catalog of all generative models trained on personal data of EU data subjects, including model architecture, training data provenance, privacy budget consumed, and synthesis dates. This catalog shall be updated within 10 business days of any new model training event.

### 4.3 Quality and Fitness-for-Purpose

**P4.3.1** Synthetic data shall meet quantitative quality thresholds before release. The specific thresholds shall be defined by the Use Case Owner in consultation with the ML Engineering Manager and documented in the use case approval form.

**P4.3.2** Default minimum fidelity thresholds:

| Domain | Metric | Threshold |
|---|---|---|
| Tabular clinical data | Jensen-Shannon divergence (per column) | < 0.15 |
| Tabular clinical data | Pairwise correlation difference (mean absolute) | < 0.10 |
| Tabular clinical data | Propensity score mean squared error (pMSE) | < 0.005 |
| Time-series clinical data | Marginal distribution overlap (per timepoint) | > 0.85 |
| Medical imaging (DICOM) | Fréchet Inception Distance (FID) | < 50 |
| Medical imaging (DICOM) | Learned Perceptual Image Patch Similarity (LPIPS) | < 0.30 |
| Financial transaction data | Kolmogorov-Smirnov statistic (per field) | < 0.10 |
| Financial transaction data | Autocorrelation preservation (lag-1 through lag-7) | MAE < 0.05 |

**P4.3.3** Use cases requiring lower fidelity than default thresholds shall be explicitly documented with justification. Thresholds exceeding defaults (tighter requirements) shall require additional compute resources as approved by the ML Engineering Manager.

### 4.4 Governance and Oversight

**P4.4.1** The AI Governance Committee shall review synthetic data generation activities quarterly as part of its regular review cycle, receiving a report including: number of synthesis pipelines executed, privacy budgets consumed, validation outcomes, incidents, and exception approvals.

**P4.4.2** All generative models used in synthesis pipelines shall be versioned and tracked in MLflow with immutable model artifacts. Models shall be retrained at minimum every 6 months or when source data distributions shift materially (population drift > 0.20 as measured by the Datadog monitoring dashboard).

**P4.4.3** Synthetic datasets containing PHI-derived structures (even if no actual PHI remains) shall be classified as "Confidential" under Meridian's Data Classification Policy (SOP-IS-002) and handled accordingly.

---

## 5. Detailed Procedures

### 5.1 End-to-End Synthesis Workflow Overview

The synthetic data generation lifecycle comprises seven sequential phases:

```
Phase 1: Use Case Intake → Phase 2: Source Data Preparation → Phase 3: Model Training
→ Phase 4: Synthesis → Phase 5: Validation → Phase 6: Release → Phase 7: Monitoring
```

Each phase is detailed below with specific procedures, systems, and responsible roles.

---

### 5.2 Phase 1: Use Case Intake and Approval

#### 5.2.1 Use Case Submission

The Use Case Owner shall initiate the process by completing the Synthetic Data Use Case Request Form (FRM-AIML-016-01) in Meridian's ServiceNow portal. The form captures:

- **Business justification**: Why synthetic data is needed; why production data cannot be used
- **Data domain specification**: Source tables/fields, approximate record count, time range
- **Fitness-for-purpose requirements**: Minimum acceptable fidelity thresholds
- **Desired privacy budget**: ε target with justification if > 1.0
- **Consumer identification**: All teams and individuals who will access the synthetic data
- **Downstream use description**: Models to be trained, analytics to be performed, tests to be run
- **Storage requirements**: Anticipated dataset size, retention period, storage location
- **Regulatory context**: Whether source data contains EU data subject information
- **Existing DPIA reference**: If a DPIA already covers this use case (per SOP-PRIV-003)

#### 5.2.2 Initial Triage (2 Business Days)

Upon submission, the ServiceNow ticket is routed to the ML Engineering Manager (or delegate) for initial triage within 2 business days. The triage determines:

| Criterion | Routing |
|---|---|
| Source data contains EU personal data AND involves health/genetic data at scale | Route to DPO for DPIA determination |
| Privacy budget ε > 1.0 requested | Route to DPO for privacy budget approval |
| Clinical use case (affects EU AI Act high-risk classification) | Route to CAIO + CMO |
| Financial services use case (affects SR 11-7 model risk) | Route to VP of Financial Services |
| Standard internal use, ε ≤ 1.0, non-clinical | Direct approval by ML Engineering Manager |

#### 5.2.3 DPIA Trigger Assessment

If the triage indicates a new DPIA is required, the DPO shall initiate the DPIA process (SOP-PRIV-003) within 5 business days. The synthesis pipeline shall not proceed until the DPIA is complete and approved. Key DPIA considerations for synthetic data:

- **Necessity and proportionality**: Is synthetic data generation the least intrusive approach?
- **Risk assessment**: What are the risks of re-identification if privacy guarantees fail?
- **Mitigation measures**: What DP guarantees, access controls, and retention limits apply?
- **Data subject communication**: Whether and how data subjects are informed (GDPR Art. 13-14)

#### 5.2.4 Approval and Ticket Creation

Upon all necessary approvals, a Jira epic is created in the `AIML-SYNTH` project with linked ServiceNow ticket reference. The epic includes tasks for each subsequent phase. The Use Case Owner is notified of approval and assigned as the business stakeholder, with the expected delivery timeline communicated (standard SLA: 15 business days from source data provisioning; expedited: 10 business days with VP approval).

---

### 5.3 Phase 2: Source Data Preparation

#### 5.3.1 Source Data Extraction (Data Steward + Data Synthesis Engineer)

The Data Steward approves and provisions source data access based on the approved use case specification. The Data Synthesis Engineer executes the extraction query from the designated source system:

- **Clinical data**: Snowflake `PROD_CLINICAL` database (read-only replica `SYNTH_SOURCE_REPLICA`)
- **Financial data**: Snowflake `PROD_HEALTHPAY` database (read-only replica `SYNTH_SOURCE_REPLICA`)
- **Imaging data**: S3 bucket `s3://meridian-clinical-imaging-prod/` (pre-signed read-only access)
- **Claims/analytics data**: Snowflake `PROD_MEDINSIGHT` database (read-only replica)

#### 5.3.2 Preprocessing Pipeline

The Data Synthesis Engineer executes the preprocessing pipeline (`kubeflow/pipelines/synth_preprocess.py`), which performs:

1. **Field filtering**: Remove fields not listed in the approved use case specification
2. **Record filtering**: Apply temporal and demographic filters per use case approval
3. **Direct identifier removal**: Strip any remaining direct identifiers not caught upstream (names, exact dates of birth, MRNs, SSNs, email addresses, IP addresses) using the `meridian-deid-v3` module, which has been validated against Meridian's standard de-identification specification
4. **Rare category collapsing**: Values with frequency < k (default k=5) in categorical fields are collapsed into an "OTHER" category to reduce re-identification risk
5. **Data type standardization**: Enforce consistent data types, missing value representations
6. **Train/holdout split**: Randomly split into training (80%) and holdout (20%) sets (using deterministic hash-based split on a salted record identifier to ensure reproducibility). The holdout set is stored in the `SYNTH_HOLDOUT` schema, access-restricted to the AI Ethics Lead and designated validators
7. **Metadata generation**: Produce a data profile (column statistics, histograms, correlation matrices) saved as a `synth_profile.json` artifact attached to the MLflow run

#### 5.3.3 Preprocessing Quality Gate

The preprocessing output is checked against automated quality gates in the Kubeflow pipeline:

- **Direct identifier detection scan**: The `meridian-deid-v3` module runs a secondary scan on the processed output to confirm zero direct identifier matches. Pipeline halts on any detection. Sensitivity: tuned to detect MRN patterns, email patterns, and SSN patterns with 99.9% recall
- **Completeness check**: Processed records within 5% of expected count
- **Schema validation**: Output schema matches the approved field specification exactly

Pipeline artifacts are logged to MLflow with the tag `phase:preprocessing` and linked to the Jira epic.

---

### 5.4 Phase 3: Generative Model Training

#### 5.4.1 Model Selection

The Data Synthesis Engineer selects the appropriate generative model architecture based on the data modality, as specified in the Meridian Generative Model Registry:

| Data Modality | Default Architecture | Implementation |
|---|---|---|
| Tabular (mixed dtypes, < 50 columns) | CTGAN (from SDV ecosystem) | `meridian-sdv-ctgan:v2.3` container |
| Tabular (mixed dtypes, ≥ 50 columns) | TVAE (from SDV ecosystem) | `meridian-sdv-tvae:v1.8` container |
| Tabular with DP guarantees | DP-CTGAN (custom fork with DP-SGD) | `meridian-dpctgan:v3.1` container |
| Time-series clinical (lab values, vitals) | TimeGAN (custom implementation) | `meridian-timegan:v2.0` container |
| Medical imaging (DICOM) | StyleGAN3-ADA (custom fork for medical) | `meridian-medgan:v4.2` container |
| Unstructured clinical text | Meridian ClinicalLLM-Synth (fine-tuned GPT-4o base with DP fine-tuning) | `meridian-clinicalllm-synth:v1.0` container, restricted |
| Financial transaction data | DP-TVAE with temporal conditioning | `meridian-dptvae:v2.5` container |

#### 5.4.2 Differential Privacy Integration

For synthesis pipelines requiring formal DP guarantees, the following procedures apply:

1. **Privacy budget allocation**: The total ε budget is allocated: 50% for model training (DP-SGD iterations), 25% for hyperparameter tuning, 25% as contingency
2. **DP-SGD configuration**: The `meridian-dpctgan` and `meridian-dptvae` containers use the following default DP-SGD parameters:
   - Noise multiplier (σ): 1.1 (calibrated to achieve target ε given dataset size)
   - Clipping norm (C): 1.0
   - Microbatches: Equal to batch size (no microbatching by default)
   - δ (delta): Set to `< 1/N` where N is the number of training records (GDPR-compliant default)
3. **Privacy accountant logging**: The `opacus` privacy accountant output is captured and logged to MLflow with the tag `dp:epsilon_consumed` and `dp:delta_consumed`. The privacy budget consumed is recorded in the central privacy budget ledger maintained by the DPO's office
4. **Budget exhaustion**: If hyperparameter tuning exhausts the contingency budget before achieving acceptable fidelity, the synthesis engineer must request a supplemental privacy budget from the DPO. No training shall exceed ε = 4.0 under any circumstances

#### 5.4.3 Training Execution

Training is executed on AWS SageMaker using the approved container image:

- **Instance type**: `ml.g5.2xlarge` (default) or `ml.p4d.24xlarge` (imaging)
- **VPC**: `sagemaker-processing-enclave` (no internet egress, VPC endpoints only)
- **IAM role**: `meridian-synth-trainer-role` (scoped to specific S3 bucket and SageMaker actions only)

The training pipeline performs automatic hyperparameter optimization (50 trials max, Bayesian optimization) targeting the best fidelity at the lowest ε. Model checkpoints are saved to the restricted S3 bucket `s3://meridian-models-synthetic/` with server-side encryption (SSE-KMS using CMK `arn:aws:kms:us-east-1:123456789012:key/synth-models-key`).

Training completion triggers an MLflow run tagged with `phase:training` and `model_architecture:{selected_container}`.

---

### 5.5 Phase 4: Synthesis

#### 5.5.1 Generation Execution

Using the trained and validated model, the Data Synthesis Engineer executes the generation script specified in the approved use case:

- **Record count**: As specified in use case (default: 1.3x source record count to oversample rare patterns; capped at 10x)
- **Output format**: Parquet (default), with optional CSV for legacy consumers. Parquet files include embedded metadata per section 6.4

Generation jobs run in the SageMaker processing enclave and output directly to a staging bucket: `s3://meridian-synthetic-staging/{sop_id}/{jira_epic_id}/`.

#### 5.5.2 Post-Generation Integrity Check

Immediately following generation, an automated integrity check verifies:

- **Record count**: Within 1% of target
- **Schema conformity**: All expected columns present, no unexpected columns
- **Value range sanity**: All values within plausible ranges (e.g., systolic BP 60-250 mmHg, age 0-120)
- **Null rate concordance**: Null rates within 20% relative difference compared to source data (to detect generation artifacts)

Any failure triggers an automatic halt and notification to the Data Synthesis Engineer (PagerDuty alert, severity: Medium).

---

### 5.6 Phase 5: Validation

#### 5.6.1 Validation Suite Overview

Validation is the most critical phase, comprising three independent evaluation modules executed sequentially. No synthetic dataset may be released until all three modules pass their defined thresholds. The full validation suite is contained in `kubeflow/pipelines/synth_validate.py` and produces a `validation_report.html` artifact.

#### 5.6.2 Module A: Statistical Fidelity Validation (Executed by Data Synthesis Engineer)

Automated comparison of synthetic data against the holdout dataset on metrics defined in Section 4.3:

| Test | Method | Tool |
|---|---|---|
| Column-wise distribution comparison | Jensen-Shannon divergence, Wasserstein distance | SDV `evaluate()` + Meridian custom `synth_fidelity` package |
| Pairwise correlation preservation | Pearson/Spearman correlation matrix difference | `synth_fidelity.correlation_matrix_diff()` |
| Propensity score discrimination | pMSE and AUROC of discriminator | `synth_fidelity.propensity_score()` |
| Multivariate structure | PCA component overlap, t-SNE plot qualitative review | `synth_fidelity.multivariate_structure()` |
| Temporal coherence (time-series) | Autocorrelation difference, trend preservation | `synth_fidelity.temporal_coherence()` |
| Image quality (imaging) | FID, LPIPS, SSIM against holdout | `torch-fidelity`, custom LPIPS pipeline |

**Pass condition**: All applicable metrics meet thresholds defined in use case approval form. Metrics failing thresholds are highlighted in the validation report with detailed diagnostics comparing source, holdout, and synthetic distributions. The Data Synthesis Engineer may iterate on generation (max 3 generation attempts) to tune outputs. If 3 attempts fail, escalation to the ML Engineering Manager is required.

#### 5.6.3 Module B: Privacy Validation (Executed by AI Ethics Lead or Designated Validator)

This module must be executed by a role independent of the Data Synthesis Engineer — either the AI Ethics Lead or a designated validator from the AI Ethics team — to ensure separation of duties.

| Test | Method | Tool | Threshold |
|---|---|---|---|
| Nearest Neighbor Distance Ratio (NNDR) | Compute ratio of synthetic-to-holdout nearest neighbor distance vs. synthetic-to-training. High ratio indicates no memorization | `synth_privacy.nndr_test()` | Ratio > 1.0 for 95% of records |
| Membership Inference Attack (MIA) | Train black-box and white-box MI classifiers to distinguish training from holdout; test on synthetic. MIA AUROC should approach 0.5 (no detectable membership) | `synth_privacy.mia_test()` | MIA AUROC < 0.60 |
| Attribute Disclosure Risk | Train inference attack models to predict sensitive attributes from non-sensitive attributes in synthetic data; measure accuracy improvement over baseline | `synth_privacy.attr_disclosure()` | Accuracy improvement < 20% relative |
| Exact Match Rate | Percentage of synthetic records exactly matching a real record in the training set | `synth_privacy.exact_match_rate()` | < 0.1% |
| DP Auditor Verification | For DP-trained models: replay privacy accountant and verify ε consumed matches declared budget within ±0.05 | `synth_privacy.dp_audit()` | ε_actual ≤ ε_approved |

**Pass condition**: All privacy tests must pass. Any failure results in:
1. Immediate quarantine of the synthetic dataset (retained in staging bucket, all consumer access revoked)
2. Notification to the DPO, CISO, and CAIO within 4 hours
3. Investigation per Section 8 (Exception Handling)

The AI Ethics Lead signs off on the privacy validation report via electronic attestation in MLflow.

#### 5.6.4 Module C: Fitness-for-Purpose Validation (Executed by Use Case Owner)

Upon receipt of the synthetic dataset (in the staging environment, not released to production), the Use Case Owner executes their own fitness-for-purpose evaluation within 5 business days:

- **Model training parity**: For ML use cases, train target model on synthetic vs. holdout; compare performance (e.g., AUROC difference < 5% absolute)
- **Analytics parity**: For analytics use cases, execute the planned analysis on synthetic vs. holdout and compare key metrics (e.g., aggregate statistics within 10% relative error)
- **Test adequacy**: For testing use cases, verify test suite pass rates on synthetic are comparable to production data pass rates
- **Edge case representation**: Manually review synthetic data for representation of known edge cases and rare conditions

Results are documented in the `Fitness-for-Purpose Attestation` form (FRM-AIML-016-02) and uploaded to the Jira epic.

#### 5.6.5 Validation Sign-off

All three validation modules must pass. The ML Engineering Manager performs the final review of the complete validation report and confirms in Jira that the synthetic dataset is approved for release. This constitutes the release gate.

---

### 5.7 Phase 6: Release

#### 5.7.1 Dataset Registration

Upon validation sign-off, the synthetic dataset is registered in Meridian's data catalog (Atlan) with the following metadata:

```yaml
dataset_id: "SYNTH_{jira_epic}_{date}"
source_datasets: ["PROD_CLINICAL.PATIENT_ENCOUNTERS", "PROD_CLINICAL.LAB_RESULTS"]
synthesis_date: "2025-06-08T14:23:00Z"
model_mlflow_run_id: "mlflow-run-abc123"
privacy_budget_epsilon: 0.8
validation_fidelity_score: 0.92
validation_privacy_risk_score: 0.12
approved_use_case_id: "UC-SYNTH-2025-042"
data_retention_days: 365
data_steward: "jane.smith@meridian.health"
tags: ["SYNTHETIC", "PHI-DERIVED-STRUCTURE", "GDPR-ART35-DPIA-REF-DPIA-2025-031"]
```

#### 5.7.2 Storage and Distribution

Released synthetic datasets are stored in the production bucket: `s3://meridian-synthetic-released/{dataset_id}/` with SSE-KMS encryption. Access is controlled via IAM policies scoped to the approved consumer list from the use case form.

For Snowflake consumers, a secure view `SYNTHETIC_{dataset_id}` is created in the `SYNTH_LIB` schema with access grants limited to approved consumer roles. Views include row-level security to enforce consumer-specific access limits if multiple teams consume the same dataset for different purposes.

#### 5.7.3 Release Notification

Automated notification (Slack channel `#synthetic-data-releases`, email to approved consumer list) includes:

- Dataset ID and catalog link
- Synthesis parameters summary (ε, fidelity scores)
- Approved use case reference
- Retention date (auto-deletion date)
- Link to consumer documentation and acceptable use policy

---

### 5.8 Phase 7: Monitoring and Continuous Validation

#### 5.8.1 Drift Monitoring

Synthetic datasets in active use are monitored for distribution drift relative to the current production data distributions (which may have shifted since initial synthesis). A weekly drift detection job (`cron: 0 2 * * 1`) runs on all active synthetic datasets:

- **Drift metric**: Jensen-Shannon divergence between synthetic and current production data (same fields, same population filters)
- **Alert threshold**: Any field with JS divergence > 0.20 triggers a warning to the Use Case Owner and ML Engineering Manager
- **Retraining trigger**: If > 25% of fields exceed JS divergence > 0.25, the dataset is flagged for retraining

#### 5.8.2 Consumer Audit Logging

All access to released synthetic datasets is logged:

- S3 access: CloudTrail logs to `s3://meridian-compliance-logs/synthetic-access/`
- Snowflake access: Query history with tag `synthetic_dataset_id` captured in centralized audit log
- Monthly audit report: Generated by the Compliance Officer summarizing all synthetic data access for anomaly detection

#### 5.8.3 Scheduled Revalidation

Every 90 days, the validation suite (Module A and B) is re-executed against the current consumer access patterns and updated production data. If the dataset fails revalidation (new privacy risks or fidelity degradation), it is quarantined pending investigation.

---

## 6. Controls and Safeguards

### 6.1 Technical Controls

| Control | Implementation | Enforcement |
|---|---|---|
| **Training environment isolation** | SageMaker processing jobs run in dedicated VPC `sagemaker-processing-enclave` with no internet egress; VPC endpoints for S3, SageMaker, ECR only | AWS IAM policy + VPC SCP, validated quarterly by CISO |
| **Encryption at rest** | All source data, model artifacts, synthetic data, and holdout data encrypted with AES-256-GCM using KMS CMKs; separate CMKs for each sensitivity tier | KMS key policy; CloudTrail monitoring of key usage |
| **Encryption in transit** | TLS 1.3 required for all inter-service communication; S3 pre-signed URLs limited to 1-hour expiry | VPC endpoint policies; S3 bucket policies |
| **Access control (S3)** | IAM role-based access; bucket policies scoped to specific principals; no public access ever; Block Public Access enabled at account level | AWS Config rule `s3-bucket-public-read-prohibited` |
| **Access control (Snowflake)** | Role-based access control via Snowflake roles `SYNTH_CONSUMER_{ROLENAME}`; column-level masking for quasi-identifier fields in shared views | Snowflake access policy; audit via query history |
| **Immutable logging** | All synthesis pipeline events logged to CloudWatch Logs with log group retention 7 years; tamper-proof log replication to compliance S3 bucket | IAM deny policy on `logs:DeleteLogGroup` and `logs:DeleteLogStream` |
| **Code immutability** | Pipeline code stored in GitHub Enterprise with branch protection; no direct pushes to `main`; PR requires ML Engineering Manager approval | GitHub branch protection rules; AWS CodePipeline enforcement |
| **Container signing** | All synthesis containers signed via AWS Signer; SageMaker configured to only pull signed images | AWS Signer + SageMaker ImageConfig |

### 6.2 Administrative Controls

| Control | Cadence | Owner |
|---|---|---|
| **Quarterly access review** | All IAM roles and Snowflake grants to synthetic data reviewed; unused access revoked | CISO + Data Steward |
| **Semi-annual SOP review** | Review and update this SOP; incorporate lessons learned from incidents and exceptions | Chief AI Officer |
| **Monthly privacy budget audit** | DPO reconciles privacy budgets consumed vs. approved; flags any excess consumption | Chief Privacy Officer / DPO |
| **Synthetic data inventory** | Maintain central inventory of all active synthetic datasets, their consumers, and retention dates | Compliance Officer |

### 6.3 Access Control Table

| Resource | Data Synthesis Engineer | AI Ethics Lead | Use Case Owner | Other Consumers |
|---|---|---|---|---|
| Source data (training) | Read, temporary | No access | No access | No access |
| Holdout data | No access | Read, Analytics | No access | No access |
| Generative model artifact | Read, Write | Read | No access | No access |
| Synthetic data (staging) | Read, Write | Read | Read (validation only) | No access |
| Synthetic data (released) | Read (audit) | Read (audit) | Read, Query | Read, Query (via IAM/Snowflake grant) |
| Validation reports | Read, Write | Read, Write, Sign-off | Read | No access |
| Privacy budget ledger | Read | Read | No access | No access |

### 6.4 Data Labeling and Tagging

Every synthetic data asset shall carry the following metadata tags, embedded in file headers (Parquet metadata or sidecar JSON for non-Parquet formats):

```json
{
  "synthetic_data_policy": {
    "sop_reference": "SOP-AIML-016",
    "dataset_id": "SYNTH_2025-042_a3f2",
    "is_synthetic": true,
    "synthesis_date": "2025-06-08",
    "generative_model_version": "meridian-dpctgan:v3.1",
    "privacy_budget_epsilon": 0.8,
    "privacy_budget_delta": 1e-6,
    "source_data_provenance": "PROD_CLINICAL.PATIENT_ENCOUNTERS, PROD_CLINICAL.LAB_RESULTS (date range: 2023-01-01 to 2024-12-31)",
    "approved_use_case_id": "UC-SYNTH-2025-042",
    "dpia_reference": "DPIA-2025-031",
    "retention_date": "2026-06-08",
    "data_steward_contact": "data-stewardship@meridian.health",
    "prohibited_uses": ["PRODUCTION_DECISION_MAKING", "REIDENTIFICATION", "EXTERNAL_DISTRIBUTION_WITHOUT_APPROVAL"],
    "acceptable_uses": ["MODEL_DEVELOPMENT", "MODEL_TESTING", "ANALYTICS_DEVELOPMENT"],
    "warning": "THIS IS SYNTHETIC DATA. IT MUST NOT BE USED FOR PRODUCTION CLINICAL DECISIONS. ANY ATTEMPT AT RE-IDENTIFICATION IS A POLICY VIOLATION AND MAY BE SUBJECT TO DISCIPLINARY ACTION."
  }
}
```

### 6.5 Retention and Disposal

| Data Category | Default Retention | Disposal Method |
|---|---|---|
| Source data extracts (in synthesis enclave) | 7 days after synthesis completion | Automated deletion via S3 lifecycle policy; KMS key revocation for additional security |
| Holdout datasets | 2 years (to enable revalidation) | Manual deletion by Data Steward upon retention expiry; quarterly review of holdout store |
| Generative model artifacts | 3 years (for reproducibility) | Archive to Glacier Deep Archive at 1 year; permanent deletion at 3 years |
| Synthetic datasets (released) | As specified in use case (max 3 years) | Automated S3 object expiration; Snowflake view drop; catalog entry marked as expired |
| Validation reports | 7 years (compliance record) | Immutable storage in compliance S3 bucket; no deletion permitted during retention period |

### 6.6 GDPR-Specific Controls

**Article 25 Compliance (Data Protection by Design and by Default):**
- Differential privacy is applied by default (ε ≤ 1.0) unless explicitly increased with DPO approval
- Data minimization is enforced at the preprocessing stage; only approved fields are extracted
- The synthesis pipeline is designed to never expose raw source data to end consumers
- Privacy metrics are calculated and reported before any dataset release
- The holdout-based validation architecture ensures no individual-level contamination between training and evaluation

**Article 30 Compliance (Records of Processing Activities):**
- The ML Engineering Manager is responsible for updating the Article 30 record within 10 business days of any new:
  - Generative model training event involving EU personal data
  - Synthetic dataset release containing EU personal data-derived structures
- Records include: controller name (Meridian Health Technologies, Inc., EU Representative: Meridian EU GmbH, Berlin), purpose of synthesis, categories of source data subjects, categories of synthetic data fields, privacy budget consumed, recipient categories, retention periods
- The DPO reviews Article 30 records for synthetic data processing quarterly

**Article 35 Compliance (Data Protection Impact Assessment):**
- DPIAs for synthetic data generation are stored in the central DPIA register maintained by the DPO (SharePoint: `DPIA Register`)
- Each approved use case requiring a DPIA receives a DPIA reference number linked in the ServiceNow ticket and dataset metadata
- DPIAs must be reviewed and reapproved every 3 years or upon significant change to the synthesis pipeline

**Article 44-49 Compliance (International Data Transfers):**
- If source data contains EU personal data and the synthesis pipeline uses infrastructure located outside the EEA, an adequacy decision or appropriate safeguards (Standard Contractual Clauses) must be in place
- Currently, all EU personal data synthesis pipelines are restricted to AWS Frankfurt (`eu-central-1`) region resources
- Any transfer of synthetic data derived from EU source data to US-based Meridian infrastructure shall be documented with an SCC reference in the use case approval

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs)

| KPI | Target | Measurement Method | Reporting Frequency |
|---|---|---|---|
| **Synthesis pipeline success rate** | ≥ 95% (pipelines completing all phases on first attempt) | Jira `AIML-SYNTH` project dashboard | Monthly |
| **Mean synthesis turnaround time** | ≤ 15 business days (standard), ≤ 10 business days (expedited) | Jira workflow duration (Phase 1-6) | Monthly |
| **Validation failure rate (privacy)** | < 2% of synthesis runs failing Module B | Validation report aggregation | Monthly |
| **Use case approval cycle time** | ≤ 5 business days from submission to approval (standard, no DPIA) | ServiceNow ticket timestamps | Monthly |
| **Privacy budget utilization** | < 80% of total quarterly privacy budget allocation per business unit | Privacy budget ledger (DPO-maintained) | Quarterly |
| **Consumer audit anomalies** | Zero high-severity anomalies (e.g., unauthorized access patterns) | Datadog anomaly detection on CloudTrail + Snowflake audit logs | Real-time alerting; monthly summary |
| **Drift-triggered retrainings** | < 10% of active datasets per quarter | Drift monitoring pipeline | Quarterly |
| **Revalidation failure rate** | < 5% of datasets failing 90-day revalidation | Revalidation pipeline | Quarterly |

### 7.2 Monitoring Dashboards

| Dashboard | Audience | Refresh Rate | Access |
|---|---|---|---|
| **Synthesis Operations Dashboard** (Datadog) | ML Engineering team, CAIO | Near real-time (5-min lag) | `#aiml-engineering` Slack channel |
| **Privacy Budget Consumption Dashboard** (Looker) | DPO, CAIO, AI Governance Committee | Daily batch | Restricted (DPO office + AI Governance Committee) |
| **Synthetic Data Inventory Dashboard** (Atlan + Custom) | Compliance Officer, Data Stewards | Daily sync | Restricted (Compliance + Data Stewardship) |
| **Validation Health Dashboard** (MLflow + Grafana) | ML Engineering Manager, AI Ethics Lead | Per-run refresh | `#aiml-engineering` Slack channel |

### 7.3 Reporting Cadence and Content

| Report | Recipients | Frequency | Content |
|---|---|---|---|
| **Synthesis Activity Report** | AI Governance Committee | Quarterly | Pipelines executed, ε budgets consumed, validation pass/fail rates, incidents, exceptions |
| **Privacy Budget Reconciliation** | DPO, CAIO, CISO | Monthly | Budget allocated vs. consumed, per-BU breakdown, any excesses, DP auditor findings |
| **Synthetic Data Inventory Report** | Data Stewardship Council | Monthly | Active datasets, consumers, upcoming retention expiries, drift status |
| **Incident Summary** | CISO, CAIO, DPO, CTO | As needed (within 24h of incident closure) | Incident description, root cause analysis, remediation actions, timeline |
| **GDPR Article 30 Update Summary** | DPO | Quarterly (or upon change) | New generative models, new synthetic datasets, changes in processing purpose |

### 7.4 Alerting and Escalation Thresholds

| Alert | Trigger Condition | Severity | Notify | Response SLA |
|---|---|---|---|---|
| **Synthesis Pipeline Failure** | Any pipeline phase failure | Medium | ML Engineering Manager (PagerDuty) | Acknowledge: 1h; Resolve: 1 business day |
| **Privacy Validation Failure** | Module B any test failure | High | CAIO, DPO, CISO (PagerDuty) | Acknowledge: 30min; Initiate investigation: 2h |
| **Privacy Budget Exhaustion** | ε consumed > ε approved for any run | High | DPO, CAIO (Email + PagerDuty) | Acknowledge: 1h; Freeze pipeline: Immediate |
| **Unauthorized Access Detected** | CloudTrail/Snowflake anomaly detection triggers | Critical | CISO, CAIO, DPO (PagerDuty + Phone) | Acknowledge: 15min; Contain: 1h; Incident response per SOP-IS-005 |
| **Drift Threshold Exceeded** | Any field JS divergence > 0.25 | Low | Use Case Owner, ML Engineering Manager (Email) | Assess: 5 business days; Retrain decision: 10 business days |
| **Retention Expiry Approaching** | Dataset within 30 days of retention expiry | Low | Data Steward, Use Case Owner (Email) | Confirm disposal or request extension: 14 calendar days before expiry |
| **DPIA Expiry Approaching** | DPIA > 2.5 years since last review | Medium | DPO (Email) | Review and reapprove: 30 calendar days |

---

## 8. Exception Handling and Escalation

### 8.1 Exception Types

Meridian recognizes that certain situations may require deviation from standard procedures defined in this SOP. Exceptions shall be formally documented and approved before deviation occurs, except in emergency situations where post-hoc documentation is permitted within 2 business days.

| Exception Type | Description | Approval Authority | Max Validity |
|---|---|---|---|
| **Fidelity Threshold Exception** | Request to release synthetic data that fails one or more fidelity metrics (Section 5.6.2) but is deemed adequate for the specific use case | CAIO + Use Case Owner VP | 90 days (one-time renewal permitted) |
| **Privacy Budget Exception** | Request for ε > 4.0 (absolute cap; exceptions beyond this are not permitted under any circumstances) | DPO + CAIO + General Counsel | Per-run only |
| **Retention Extension** | Extension of synthetic dataset retention beyond approved duration | Data Steward + DPO | 12 months max per extension |
| **Consumer Expansion** | Adding new consumers not listed in original use case approval | ML Engineering Manager | Until next quarterly access review |
| **Accelerated Timeline** | Request to bypass standard approval queue for urgent business need | VP of Engineering (if < 5 business days timeline requested) | Per-use case |
| **Holdout Access** | Request for access to the holdout split by non-validated role | DPO + CAIO + CISO | Granted for specific audit/investigation only; maximum 48-hour access window |

### 8.2 Exception Request Process

1. **Submission**: Use Case Owner or Data Synthesis Engineer submits Exception Request Form (FRM-AIML-016-03) via ServiceNow, selecting "Synthetic Data Exception" category
2. **Assessment**: ML Engineering Manager assesses technical feasibility and risk within 2 business days
3. **Routing**: Based on exception type, routed to required approvers per table above
4. **Approval/Denial**: Approvers respond within 3 business days (expedited: 1 business day with VP escalation)
5. **Documentation**: Approved exceptions are logged in the central Exceptions Register (Confluence: `Synthetic Data Exceptions`) with unique exception ID, linked to the Jira epic
6. **Implementation**: If approved, the ML Engineering Manager updates the Jira epic with exception parameters; the synthesis pipeline configuration is updated to accommodate the exception

### 8.3 Emergency Situations

In the event of a privacy incident involving synthetic data (e.g., suspected re-identification, privacy budget violation, unauthorized access):

1. **Immediate Containment**: The CISO (or delegate) revokes all consumer access to the affected synthetic dataset within 1 hour of notification. IAM policies are modified; Snowflake grants are suspended
2. **Incident Declaration**: Declared per SOP-IS-005 (Incident Response), severity level "High" or "Critical"
3. **Investigation Team**: Convened within 4 hours: CISO, CAIO, DPO, ML Engineering Manager, General Counsel representative
4. **Root Cause Analysis**: Completed within 5 business days; preliminary findings reported to AI Governance Committee within 2 business days
5. **Remediation**: Approved by CAIO and CISO; implemented within timeline specified in incident response plan
6. **Post-Mortem**: Presented to AI Governance Committee within 15 business days of incident closure; any resulting SOP amendments proposed within 30 business days

### 8.4 Escalation Path

```
Level 1: ML Engineering Manager (operational issues, standard exceptions)
    ↓ (if unresolved or if issue relates to privacy/ethics)
Level 2: Chief AI Officer + Chief Privacy Officer / DPO
    ↓ (if involves legal risk or external communication)
Level 3: General Counsel + Chief Medical Officer + CISO
    ↓ (if involves executive decision or regulatory notification)
Level 4: CEO + Board Audit Committee
```

### 8.5 Regulatory Notification Triggers

The following events trigger mandatory regulatory notification assessment by the General Counsel and DPO within 24 hours:

- Confirmed or highly probable re-identification of individuals from Meridian synthetic data
- Privacy budget violation exceeding ε = 4.0 (absolute cap breach)
- Unauthorized exfiltration of synthetic data generated from EU personal data
- Any incident involving synthetic data that may trigger GDPR Article 33 (Data Breach Notification) or Article 34 (Communication to Data Subject) obligations

---

## 9. Training Requirements

### 9.1 Role-Based Training Matrix

| Training Module | Data Synthesis Engineer | AI Ethics Lead | Use Case Owner | ML Engineering Manager | Compliance Officer |
|---|---|---|---|---|---|
| **SYNTH-101: Synthetic Data Fundamentals** | Required | Required | Required | Required | Recommended |
| **SYNTH-201: Privacy-Preserving Synthesis** | Required | Required | Not required | Required | Recommended |
| **SYNTH-301: Validation Suite Operation** | Required | Required | Not required | Required | Not required |
| **SYNTH-401: GDPR and Synthetic Data** | Required | Required | Recommended | Required | Required |
| **SYNTH-102: Use Case Owner Responsibilities** | Not required | Not required | Required | Not required | Not required |
| **Annual Refresher: SOP-AIML-016** | Required | Required | Required | Required | Required |

### 9.2 Training Descriptions

**SYNTH-101: Synthetic Data Fundamentals (4 hours, e-learning)**
- What synthetic data is and is not
- Meridian's synthetic data lifecycle
- Roles and responsibilities under this SOP
- Use case intake process
- Data labeling and handling requirements
- Quiz: 80% pass mark; 2 retake attempts before manager intervention

**SYNTH-201: Privacy-Preserving Synthesis (8 hours, instructor-led + hands-on lab)**
- Differential privacy fundamentals (ε, δ, privacy budgets, composition)
- DP-SGD and its application in Meridian's synthesis containers
- Re-identification risks and attack vectors
- Hands-on: Configuring privacy budgets, running DP synthesis, interpreting privacy accountant output
- Assessment: Practical exercise (synthesize with specified ε budget, pass privacy validation)

**SYNTH-301: Validation Suite Operation (4 hours, hands-on lab)**
- Running Modules A, B, and C
- Interpreting validation reports
- Debugging common fidelity failures
- Privacy validation deep dive (MIA, NNDR, attribute disclosure)
- Assessment: Execute full validation suite on a provided dataset, correctly interpret results, recommend pass/fail

**SYNTH-401: GDPR and Synthetic Data (4 hours, instructor-led)**
- GDPR articles relevant to synthetic data (Art. 25, 30, 35)
- DPIA process for synthesis pipelines
- Data subject rights impact on generative models
- Article 30 record-keeping for synthetic data
- International transfer restrictions and SCC requirements
- Assessment: Case-study based exam (2 scenarios, written responses)

**SYNTH-102: Use Case Owner Responsibilities (2 hours, e-learning)**
- Defining fitness-for-purpose requirements
- Completing the use case request form
- Fitness-for-purpose validation execution
- Consumer responsibilities and prohibited uses
- Quiz: 80% pass mark

### 9.3 Training Cadence and Tracking

- **Initial training**: All personnel in assigned roles must complete required training before receiving access to synthesis systems or synthetic data
- **Annual refresher**: All personnel with active access must complete the Annual Refresher (SYNTH-RFS-016, 2 hours, e-learning, covers SOP changes)
- **Change-triggered training**: When this SOP undergoes a major version change (e.g., v4.x → v5.0), all personnel must complete updated training within 30 calendar days
- **Training tracking**: Managed via Workday Learning; ML Engineering Manager receives monthly training compliance report; non-compliance (overdue training > 30 days) results in automatic suspension of synthesis system access until training is completed
- **Training content review**: CAIO reviews training content annually in conjunction with SOP review; updates incorporated within 30 days of SOP revision approval

---

## 10. Related Policies and References

### 10.1 Internal Meridian SOPs

| SOP ID | Title | Relationship |
|---|---|---|
| SOP-PRIV-003 | Data Protection Impact Assessment | DPIA process triggered for certain synthetic data use cases |
| SOP-IS-002 | Data Classification Policy | Synthetic data classification and handling requirements |
| SOP-IS-005 | Incident Response Procedure | Response to privacy incidents involving synthetic data |
| SOP-AIML-002 | AI Model Development Lifecycle | Governs downstream models trained on synthetic data |
| SOP-AIML-008 | Model Risk Management | Risk tiering for models trained on synthetic data |
| SOP-AIML-012 | Feature Store Governance | Registration of synthetic features in the Meridian Feature Store |
| SOP-TPM-011 | Third-Party Data Acquisition | Procured datasets vs. internally generated synthetic data |
| SOP-DATA-004 | Data Retention and Disposal | Retention schedules referenced by this SOP |
| SOP-IS-007 | Identity and Access Management | IAM policy framework for synthesis infrastructure |
| SOP-GDPR-001 | GDPR Compliance Framework | Cross-reference for GDPR-specific controls |

### 10.2 External Standards and Regulations

| Standard/Regulation | Reference | Applicability |
|---|---|---|
| **GDPR (Regulation EU 2016/679)** | Articles 5, 9, 13, 14, 17, 22, 25, 30, 33, 34, 35, 44-49 | All synthetic data derived from EU personal data |
| **NIST AI 100-1** | AI Risk Management Framework | Referenced in AI Governance Committee charter; not directly implemented in this SOP |
| **ISO/IEC 27001:2022** | Information Security Management | Meridian's ISMS scope includes synthetic data systems |
| **ISO/IEC 27701:2019** | Privacy Information Management | PIMS controls for processing environments |
| **SOC 2 Type II** | Trust Services Criteria (Security, Confidentiality) | Synthetic data controls within scope of Meridian's SOC 2 audit |
| **EU MDR 2017/745** | Medical Device Regulation | Clinical AI products using synthetic data in training require notified body notification of training data changes |
| **MITRE ATLAS** | Adversarial Threat Landscape for AI Systems | Referenced in threat modeling for generative models |

### 10.3 Tools and Platforms Referenced

| Tool/Platform | Purpose |
|---|---|
| **Synthetic Data Vault (SDV)** | Primary tabular data synthesis and evaluation library |
| **Opacus (Meta/PyTorch)** | Differential privacy training library; privacy accounting |
| **MLflow** | Experiment tracking, model registry, artifact storage |
| **Kubeflow** | Pipeline orchestration (`meridian-kf-pipelines` repository) |
| **AWS SageMaker** | Managed training and generation infrastructure |
| **Snowflake** | Source data warehouse, synthetic data serving |
| **Amazon S3** | Data lake storage (all tiers: source, staging, released, compliance) |
| **AWS KMS** | Encryption key management |
| **AWS CloudTrail** | API audit logging |
| **Amazon CloudWatch** | Application logging and monitoring |
| **Datadog** | Observability dashboards and anomaly detection |
| **Atlan** | Data catalog and metadata management |
| **ServiceNow** | Use case intake, exception requests, workflow tracking |
| **Jira** | Project tracking (`AIML-SYNTH` project) |
| **Workday Learning** | Training assignment and tracking |
| **PagerDuty** | Incident alerting and escalation |

---

## 11. Revision History

| Version | Date | Author | Approver | Summary of Changes |
|---|---|---|---|---|
| 1.0 | 2021-03-15 | Dr. Sarah Chen (former AI Ethics Lead) | David Park, VP of Engineering | Initial release. Established foundational synthetic data governance. Covered CTGAN-only synthesis for tabular clinical data. Privacy budget default ε ≤ 2.0. |
| 2.0 | 2022-01-20 | Dr. Marcus Rivera, CAIO | David Park, VP of Engineering | Major revision. Expanded to all data modalities (imaging, text, financial). Introduced Module B independent privacy validation. Reduced default ε from 2.0 to 1.0. Added holdout validation framework. |
| 2.1 | 2022-07-11 | Dr. Marcus Rivera, CAIO | David Park, VP of Engineering | Minor revision. Updated SDV to v1.0 release. Added DP-CTGAN container. Refined NNDR privacy metric thresholds based on empirical evaluation results. Updated related SOP cross-references. |
| 3.0 | 2023-04-03 | Dr. Marcus Rivera, CAIO + Dr. Klaus Weber (DPO input) | David Park, VP of Engineering | Major revision to incorporate GDPR-specific controls (Art. 25, 30, 35). Added DPIA trigger criteria. Integrated privacy budget ledger. Added Article 30 record-keeping procedure. Introduced EU-only synthesis infrastructure requirement. Expanded training module SYNTH-401. |
| 3.1 | 2023-09-18 | ML Engineering Manager (Review) | David Park, VP of Engineering | Minor revision. Corrected privacy budget allocation formula. Updated SageMaker instance types. Added financial transaction data modality and DP-TVAE container. Clarified retention for model artifacts. |
| 4.0 | 2024-02-05 | Dr. Marcus Rivera, CAIO | David Park, VP of Engineering | Major revision. Restructured procedures into 7-phase lifecycle. Introduced fitness-for-purpose validation (Module C). Added EU AI Act high-risk classification routing in use case triage. Updated medical imaging architecture reference. Added continuous drift monitoring (Phase 7). Tightened privacy thresholds (MIA AUROC < 0.60). Added exception handling framework. Expanded to approximately 20 pages. |
| 4.1 | 2025-06-08 | Dr. Marcus Rivera, CAIO | David Park, VP of Engineering | Minor revision. Updated ClinicalLLM-Synth container reference to v1.0. Adjusted drift monitoring threshold to 0.25 JS divergence. Added `meridian-deid-v3` module reference in preprocessing. Updated MLflow tagging conventions. Added quarterly revalidation requirement. Corrected KPI target for synthesis turnaround time. Updated tool/platform references table. |

---

**Document Control:** This SOP is maintained in Meridian's Controlled Document Repository (SharePoint: `Policies/SOPs/AI-ML/`). The official controlled copy is the PDF version digitally signed by the Approver. Printed copies are uncontrolled.

**Next Review Date:** 2025-12-20

**End of Document**