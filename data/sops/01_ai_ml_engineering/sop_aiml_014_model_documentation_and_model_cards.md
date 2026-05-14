---
sop_id: "SOP-AIML-014"
title: "Model Documentation and Model Cards"
business_unit: "AI/ML Engineering"
version: "2.9"
effective_date: "2024-10-02"
last_reviewed: "2025-01-12"
next_review: "2025-07-28"
owner: "Dr. Marcus Rivera, Chief AI Officer"
approver: "David Park, VP of Engineering"
classification: "Internal"
regulations:
  - "EU AI Act"
  - "NIST AI RMF"
  - "SR 11-7"
status: "Active"
---

# Standard Operating Procedure: Model Documentation and Model Cards

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the mandatory framework for the creation, review, approval, and maintenance of model documentation and model cards for all artificial intelligence (AI) and machine learning (ML) models developed, deployed, or procured by Meridian Health Technologies, Inc. The purpose of this framework is to ensure a standardized, auditable, and transparent record of all algorithmic systems, to facilitate robust model risk management, and to provide clear, accessible information to downstream consumers including internal developers, product teams, regulatory compliance officers, and external auditors.

This SOP operationalizes the principles of transparency and accountability by ensuring that every model is accompanied by a comprehensive dossier that describes its design, development, performance characteristics, and operational constraints. Adherence to this procedure is critical for maintaining the safety and soundness of our automated decision-making systems, particularly those within the HealthPay Financial Services business line, and for demonstrating responsible AI practices to regulators and partners.

### 1.2 Scope

This SOP applies to all employees, contractors, and third-party vendors who are involved in the lifecycle of an AI/ML model at Meridian Health Technologies. The scope encompasses all models across all business units, from initial research through decommissioning.

Specifically, the requirements herein apply to:

| Business Unit | Model Types Covered | Data Types | Deployment Environment |
| :--- | :--- | :--- | :--- |
| **Clinical AI Platform** | Diagnostic imaging analysis, patient risk scoring, adverse event prediction, clinical decision support algorithms | De-identified and PHI-radiology images, EHR data | AWS (us-east-1, eu-west-1), Azure (DR) |
| **HealthPay Financial Services** | Credit scoring, fraud detection, claims automation, patient lending, payment integrity models | PHI, PII, financial account data, claims data | AWS (us-east-1), On-premise HSM |
| **MedInsight Analytics** | Population health risk stratification, care gap identification, readmission prediction, outcomes forecasting | Aggregated and patient-level PHI, claims data | AWS (us-east-1), Snowflake |
| **Meridian SaaS Platform** | Core infrastructure AI for IAM anomaly detection, platform health prediction, cost optimization | System logs, metadata | AWS (us-east-1, eu-west-1) |

The scope includes:
- All new models in development.
- All existing models in production (retroactive documentation to be completed per Section 5.10).
- All significant updates or retrains of existing models.
- Models procured from third-party vendors, including those embedded in licensed software or API-accessible services.

### 1.3 Exclusions

The following are explicitly out of scope for this SOP:
- Simple rule-based heuristic systems that do not learn from data (e.g., a static SQL `WHERE` clause rule). However, if such a rule is used as an output of a model or is derived from a statistical analysis of data, the source model is in scope.
- Exploratory data analysis scripts that are not intended for production deployment.
- General-purpose productivity tools using generative AI (e.g., Microsoft Copilot) when not integrated into Meridian products. Integration of such tools into Meridian workflows or products brings them immediately into scope.

---

## 2. Definitions and Acronyms

### 2.1 Definitions

| Term | Definition |
| :--- | :--- |
| **Accountable Executive** | The most senior leader with authority over the business unit operating the model, ultimately answerable for model-derived decisions. |
| **Bias** | A systematic error in a model's predictions that results in unfair or inequitable outcomes for a specific group, not related to the underlying risk or clinical reality. |
| **Concept Drift** | A change in the statistical properties of the target variable, which the model is predicting, over time in unforeseen ways. |
| **Data Drift** | A change in the statistical properties of the input features to the model over time. |
| **Intended Use** | A detailed, prescriptive description of the precise purpose for which a model was designed, including the clinical or financial context, target population, and operational workflow. |
| **Limitation** | A specific, known condition, constraint, or scenario under which the model’s performance has been shown to degrade, or where its use is not recommended or is forbidden. |
| **Model Card** | A concise, structured, and human-readable document that provides key information about a deployed AI/ML model, intended for transparency with stakeholders. It is a summary derived from the full model documentation. |
| **Model Documentation** | The comprehensive technical dossier, containing all design choices, data provenance, bias analyses, validation results, and risk assessments.
| **Model Owner** | The individual (non-human-singular title) who is responsible for the day-to-day management, performance monitoring, and maintenance of a specific model. |
| **Model Risk Management (MRM)** | The overarching framework and processes for identifying, measuring, monitoring, and controlling risks associated with the use of models. |
| **Significant Model Update** | Any alteration to a model's architecture, hyperparameters, or training data distribution that, upon review by the Model Owner and MRM Committee, is expected to result in a material change (>5% delta) to a core performance metric (e.g., AUC, F1 score, precision, error rate) or its functional use case. |

### 2.2 Acronyms

| Acronym | Definition |
| :--- | :--- |
| **AI** | Artificial Intelligence |
| **AUROC** | Area Under the Receiver Operating Characteristic curve |
| **CAIO** | Chief AI Officer |
| **CCO** | Chief Compliance Officer |
| **DPD** | Detailed Procedural Document |
| **EU** | European Union |
| **F1** | Harmonic mean of precision and recall |
| **FPR** | False Positive Rate |
| **GDPR** | General Data Protection Regulation |
| **GRC** | Governance, Risk, and Compliance |
| **HIPAA** | Health Insurance Portability and Accountability Act |
| **JIRA** | Issue and project tracking software |
| **KPI** | Key Performance Indicator |
| **ML** | Machine Learning |
| **MRE** | Model Risk Exception |
| **MRM** | Model Risk Management |
| **PHI** | Protected Health Information |
| **RACI** | Responsible, Accountable, Consulted, Informed |
| **RMSE** | Root Mean Square Error |
| **SDLC** | Software Development Lifecycle |
| **V&V** | Verification and Validation |

---

## 3. Roles and Responsibilities

The following RACI matrix defines the roles and their specific duties for the model documentation lifecycle.

| Activity / Task | Model Developer | Model Owner | Quality Assurance (QA) Lead | VP of Clinical/FinServ | MRM Committee | CAIO Office | CCO / Legal |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Creation of Draft Model Docs & Card** | **R** | A | C | I | I | C | I |
| **Technical Validation of Metrics** | C | R | **R** | I | I | A | I |
| **Intended Use & Limitation Sign-off** | C | R | I | **A** | C | C | C |
| **SR 11-7 Compliance Assessment** | C | R | I | C | **R** | A | C |
| **Final Approval for Low-Risk Model** | I | R | C | C | A | **A** | I |
| **Final Approval for High-Risk Model** | I | C | C | C | **R** | C | **A** |
| **Annual Model Docs Revalidation** | R | **R** | C | I | A | C | I |
| **Exception Handling & Escalation** | C | R | I | I | **A** | C | R |

**Key Responsibility Descriptions:**

- **Model Developer (e.g., Senior ML Engineer, Data Scientist):** Responsible for creating the initial model documentation and card by completing the `MER-FORM-AIML-014` template. They must provide complete, accurate, and evidence-backed technical information.
- **Model Owner (e.g., Director of Credit Risk Modeling, Lead Clinical Data Scientist):** The primary point of contact for the model's documentation throughout its lifecycle. Accountable for ensuring documentation is current, accurate, and complete. Must review and approve developer drafts before wider review.
- **Quality Assurance (QA) Lead:** Independently verifies all reported performance metrics by replicating results or reviewing source code and validation plans. Signs off on the technical accuracy of the model card's performance benchmarks.
- **VP of Business Unit (VP of Financial Services - Robert Liu / VP of Clinical AI Products - Dr. Aisha Okafor):** Holds ultimate authority to sign off on the documented Intended Use and Limitations, confirming alignment with business strategy and product roadmap.
- **Model Risk Management (MRM) Committee:** A cross-functional committee chaired by the CAIO. Evaluates all documentation for high-risk models, assesses inherent and residual risk, and approves the model for deployment or continued use in line with SR 11-7.
- **Office of the Chief AI Officer (Dr. Marcus Rivera):** Provides final approval on all model documentation, ensuring adherence to this SOP and overall AI strategy. Maintains the central repository of approved model cards.
- **Chief Compliance Officer / Legal (Thomas Anderson / Maria Gonzalez):** Consults on regulatory language, reviews documentation for compliance with legal obligations, and must approve documentation for any model under a consent order or regulatory finding.

---

## 4. Policy Statements

4.1. **No Undocumented Models in Production:** No AI/ML model may be deployed to a production environment, including shadow or "dry-run" deployment, without fully approved model documentation and a corresponding model card, compliant with this SOP.

4.2. **Single Source of Truth:** The official model documentation, managed in the Meridian GRC Platform (OneTrust) and the Model Registry (MLflow), serves as the single, authoritative source of truth for all information related to a model's state, purpose, and risks.

4.3. **Model Cards for External Transparency:** For any model that directly or indirectly impacts external partners, patients, or financial consumers, an approved external-facing model card must be published on the Meridian Developer Portal within 30 calendar days of deployment.

4.4. **Mandatory Intended Use and Limitations:** Every model card shall explicitly define a rigid, non-ambiguous Intended Use and a section detailing known Limitations. Use of the model outside of the stated Intended Use is prohibited.

4.5. **SR 11-7 Alignment for Financial Models:** All models used within HealthPay Financial Services for credit adjudication, line assignment, or fraud detection shall adhere to the validation, documentation, and governance principles specified in Federal Reserve SR Letter 11-7. The documentation package is the primary evidence for exams.

4.6. **Lifecycle Event Triggers:** Documentation must be reviewed and, if necessary, updated at the following trigger events:
    - Prior to initial production deployment.
    - Prior to the approval of a Significant Model Update.
    - Within 10 business days of a material performance degradation event (e.g., a silent PagerDuty alert for model drift exceeding thresholds for >24 hours).
    - At least annually, as part of the formal model revalidation process.
    - Within 30 days of a major change to the underlying data source or the operational environment.

---

## 5. Detailed Procedures

This section outlines the step-by-step procedures for creating, approving, and maintaining model documentation and model cards. The procedure is integrated with the Meridian SDLC and JIRA Model Lifecycle project (`MLC-PROJ`).

### 5.1 Step 1: Initiation and Template Selection

1.1. Upon JIRA issue creation for a new model (`JIRA: MLC-NEW`) or a significant update (`JIRA: MLC-UPD-###`), the Model Developer is assigned the task "Complete Model Documentation."
1.2. The Model Developer accesses the official template file from the Meridian GRC SharePoint site at `https://sharepoint.meridian.tech/sites/GRC/ModelDocs/Templates/`.
1.3. Two templates exist and must be selected based on the model's complexity and risk tier as described in SOP-RMG-002:
    - **`MER-FORM-AIML-014a` (Standard Template):** For Tier 1 and Tier 2 models (Low/Moderate Risk).
    - **`MER-FORM-AIML-014b` (SR 11-7 Comprehensive Template):** For Tier 3 models (High Risk) and all models within the HealthPay Financial Services business line. This template includes sections for detailed conceptual soundness review, outcome analysis, and an extensive bibliography of developmental evidence.
1.4. The Developer creates a copy of the correct template, renames it according to the convention `ModelID_v[X.Y]_Documentation_[YYYYMMDD].docx`, and stores it in the model's dedicated GRC folder.

### 5.2 Step 2: Technical Population of the Documentation Template

The Model Developer must complete all applicable sections of the selected template. The following sub-sections detail the critical elements required.

#### 5.2.1 Model Identity and Executive Summary
- **Model ID:** A unique identifier from the MLflow Model Registry (e.g., `HP-CS-V2` for HealthPay Credit Score V2).
- **Model Name:** Human-readable name.
- **Version:** Semantic version (e.g., `2.3.1`).
- **Ownership:** Model Owner, Developer(s), and Accountable Executive.
- **Business Objective:** A 3-5 sentence summary of the model's purpose, framed as a business objective to be achieved, suitable for a non-technical executive audience.

#### 5.2.2 Intended Use and Limitations
- **Intended Use:** A detailed, prescriptive statement. Must specify:
    - The population on which the model is to be used (e.g., "All adult patients (>=18) presenting for an initial primary care visit in a non-emergency setting").
    - The specific outcome being predicted or optimized.
    - How the model output is designed to be used in a workflow (e.g., "The score is an input to the loan officer's decision matrix, not the sole determinant of credit approval.").
    - The geographical and temporal validity scope (e.g., "Validated for use in the United States only, using patient data from 2019-2023. Performance is expected to be stable through 2025-12-31.").
- **Out-of-Scope Use Cases:** Explicit statement of known misuses (e.g., "Not to be used for emergency room triage," "Not for use on pediatric populations").
- **Limitations and Warnings:** A numbered list of specific, quantifiable limitations.
    1.  "Performance degrades to an AUROC of 0.62 for patients with fewer than 2 years of claims history."
    2.  "False negative rate may be unacceptably high for patients with specific rare disease codes defined in Appendix A."
    3.  "Not validated for use with ICD-11 codes; limited to ICD-10-CM."

#### 5.2.3 Data Provenance and Preprocessing
- **Source Systems:** List all data sources (e.g., Snowflake `PROD_EDW_MED.CLAIMS_V`, Kafka topic `patient-registration`).
- **Data Fields:** Comprehensive data dictionary with field name, description, data type, and PHI/PII classification.
- **Data Splitting Strategy:** Detailed methodology for train/validation/test splits, including temporal cutoffs or stratified splitting to prevent leakage.
- **Preprocessing Steps:** Version-controlled reference to the feature engineering pipeline code in the `meridian-ml/feature-store` Git repository.

#### 5.2.4 Model Architecture and Training
- **Algorithm Class:** (e.g., XGBoost, Transformer, Random Forest Classifier).
- **Final Hyperparameters:** The exact hyperparameters used for the deployed model.
- **Training Environment:** (e.g., SageMaker training job ID `training-job-2024-09-15-...`).
- **Training Metrics:** Log loss, accuracy, AUROC, F1, etc., as tracked in MLflow run `[MLflow-Run-Link]`.

### 5.3 Step 3: Performance Benchmarks and Ethical Considerations

This section is subject to rigorous review by the QA Lead and the MRM Committee.

#### 5.3.1 Performance Benchmarks
This is the definitive record of model performance. The Developer must populate this section from MLflow directly. A manual override of metrics is strictly prohibited.

**Table 5.3.1a: Aggregate Performance Metrics**

| Metric | Overall Score | Threshold Target |
| :--- | :---: | :---: |
| **AUROC** | 0.89 | > 0.85 |
| **F1 Score** | 0.79 | > 0.75 |
| **Precision** | 0.82 | > 0.78 |
| **Recall (Sensitivity)** | 0.76 | > 0.72 |
| **RMSE** | N/A (Classification) | N/A |

**Table 5.3.1b: Segment-Level Performance Metrics (Excerpt)**
*This section must be completed for all Tier 2 and Tier 3 models, evaluating at least race, gender, and age per SOP-AIML-008.*

| Segment | Value | AUROC | F1 Score | FPR at threshold 0.5 | Assessment |
| :--- | :--- | :---: | :---: | :---: | :--- |
| Race | White, Non-Hispanic | 0.90 | 0.81 | 0.20 | Pass |
| Race | Black or African American | 0.86 | 0.74 | 0.28 | **Review** |
| Gender | Female | 0.88 | 0.80 | 0.18 | Pass |
| Gender | Male | 0.89 | 0.78 | 0.22 | Pass |
| Age | 65+ | 0.82 | 0.69 | 0.30 | **Fail - Limitation Trigger** |

If any primary metric for a segment falls below the target threshold, it must be explicitly flagged as an Ethical Consideration and automatically triggers the addition of a specific Limitation statement. The "Fail" and "Review" flags in the Assessment column auto-generate a JIRA ticket for Quantitative Bias Review (`JIRA: BIAS-###`).

#### 5.3.2 Ethical Considerations
A narrative section addressing fairness and equity, containing:
- **Bias Mitigation Strategy:** Describe the pre- or in-processing techniques used (e.g., re-weighting, adversarial debiasing) and reference the technical report.
- **Disparate Impact Analysis Summary:** A plain-language summary of the fairness metrics, referencing the full report in SOP-AIML-008.

### 5.4 Step 4: Documentation Review and Approval Workflow

Once the Model Developer signs off on the draft, the document enters the formal review workflow in the Meridian GRC Platform.

1.  **Developer Review:** Developer self-attests to completeness and technical accuracy, attaching all evidentiary links. Assigns to Model Owner.
2.  **Model Owner Review:** The Model Owner performs a thorough review of the document. If issues are found, it is returned to the Developer. If approved, it is assigned to the QA Lead.
3.  **QA Lead Validation:** The QA Lead independently reproduces the performance benchmark figures from the test dataset and the production MLflow run. The QA Lead must sign off on a `QA Validation Checklist` confirming the results are within a ±1% tolerance of the metrics in the document. Signs off in GRC and assigns to the Business VP.
4.  **Business VP Sign-off:** The relevant VP (Dr. Aisha Okafor for Clinical, Robert Liu for Financial Services) reviews and formally signs off on the Intended Use and Limitations. This signature is a regulatory attestation that the business will not use the model for other purposes.
5.  **MRM Committee / CAIO Office Approval (Risk-Tier Dependent):**
    - **Tier 1 Models:** Auto-approved upon Business VP sign-off. A notification is sent to the CAIO Office for final registration.
    - **Tier 2 Models:** The CAIO Office (or delegate) performs a final completeness check and grants approval.
    - **Tier 3 Models (including all HealthPay models):** The full package is presented to the MRM Committee at its next weekly meeting. The committee votes on a formal "Approval to Deploy" motion per Section 5 of the MRM Committee Charter (SOP-RMG-001). The CCO/Legal representative must concur for the approval to be valid.
6.  **Final Registration:** Upon final approval, the GRC system automatically:
    - Sets the document status to `Approved`.
    - Registers the model ID and version in the central Model Inventory.
    - Publishes the model card to the internal API endpoint.
    - Creates a task for the Developer to publish the external model card, if applicable.

**SLA Timelines for Reviewers:**

| Role | Max Time in Review (Calendar Days) |
| :--- | :---: |
| Model Owner | 5 |
| QA Lead | 10 |
| Business VP | 7 |
| MRM Committee / CAIO | 14 (from next meeting date) |

### 5.5 Step 5: Model Card Generation and Publication

The model card is an immutable, versioned JSON file (conforming to the `meridian-model-card-schema-v2`) generated from the final approved documentation.

5.5.1. The GRC Platform's `ModelCardPublisher` module auto-populates the JSON file by extracting data from the `MER-FORM-AIML-014a/b` document.
5.5.2. The Model Owner is notified to review the JSON. After approval, the JSON file's hash is immutably stored.
5.5.3. The model card is published to two endpoints:
    - **Internal:** `api.meridian.tech/internal/model-cards/` for cross-team transparency and integration with Datadog dashboards.
    - **External:** `developer.meridian.tech/cards/` (for applicable models), providing a clean, branded HTML view of the model card for customers and partners.
5.5.4. The external model card includes a "Subscribe to Updates" function, managed by the Customer Operations team under VP Michael Chang, which notifies subscribers of critical changes to limitations or intended use.

### 5.6 Step 6: Specific Procedures for HealthPay Financial Services Models (SR 11-7 Alignment)

This procedure applies in addition to the steps above for all HealthPay models, directly addressing supervisory expectations under SR 11-7.

`[Note: This section is intentionally detailed to demonstrate thorough SR 11-7 coverage as per Federal Reserve guidance on Model Risk Management.]`

#### 5.6.1 Evidence of Developmental Evidence per SR 11-7, Attachment 1
The documentation package must be self-contained and demonstrate rigorous conceptual soundness. The `MER-FORM-AIML-014b` template includes a dedicated "Conceptual Soundness Dossier" appendix, which must contain:
- **A. Theory and Design:** A detailed white paper describing the theory, statistical methodology, and a literature review of alternative approaches considered. Reference to the specific JIRA research spike (`JIRA: RSCH-###`).
- **B. Data Evaluation:** An in-depth analysis of data quality, completeness, and representativeness. This must include a formal analysis of missing data mechanisms (MCAR, MAR, MNAR) and the impact of any imputation strategies on model outcomes.
- **C. Variable Selection:** A rigorous justification for the selection of every predictor variable, including bivariate and multivariate analyses. The iterative feature elimination process must be documented and reproducible.

#### 5.6.2 Independent Validation per SR 11-7, Section III.B
An independent validation report, produced by a party not responsible for model development or use, is required. For Meridian, this function is fulfilled by the QA Lead, who must not report to David Park (VP of Engineering) but instead has a dotted-line reporting capability to the MRM Committee. The independent validation report must include:
- **Outcome Analysis (Back-testing):** Detailed comparison of model predictions against actual outcomes on an out-of-time sample. A table showing actual vs. predicted loss rates across deciles must be included, along with a binomial test of the distribution of outcomes.
- **Sensitivity Analysis:** An assessment of the model's sensitivity to changes in key inputs. This must show the marginal effect on the credit score of a 10% shock to critical macroeconomic variables (e.g., unemployment rate under CECL scenarios).
- **Benchmarking:** Direct comparison of the model's performance against a challenger model or an incumbent model, using the same out-of-time dataset. The QA Lead must explain and justify any performance degradation.

#### 5.6.3 Ongoing Monitoring Plan per SR 11-7, Section III.C
The documentation must include a link to the live, automated monitoring plan. This is not a static document but a pointer to the specific Datadog dashboard and PagerDuty service configuration for the model.
- **Monitoring Dashboard (`dashboard-meridian-{modelID}`).** Must exist at the time of model approval.
- **Key Drift Metrics Tracked:** Population Stability Index (PSI), Characteristic Stability Index (CSI) for top 10 features, and Kolmogorov-Smirnov (KS) statistic on credit scores.
- **Alerting Thresholds:** PagerDuty alerts must be configured to fire a `Severity-3` warning for a PSI > 0.1 and a `Severity-2` critical alert for a PSI > 0.25, directly to the Model Owner and the Dev Ops on-call rotation.

### 5.7 Step 7: Post-Deployment Monitoring and Revalidation

7.7.1. The Model Owner is responsible for reviewing the live Datadog dashboards daily for any anomalies.
7.7.2. Every quarter, the Model Owner generates an "Automated Quarterly Model Health Report" (JIRA Automation `ML-QR-GEN`). This report, compiled from Datadog logs versus the benchmarks in the model card, is submitted to the CAIO office for review.
7.7.3. The annual revalidation process (Step 5.10) includes a full re-execution of the back-testing and sensitivity analysis by the QA Lead, documented as an addendum to the original validation report.

### 5.8 Step 8: Model Card for Third-Party Models

For vendor-supplied models (e.g., a credit score from a major bureau):
8.1. The Procuring Manager (with support from the Vendor Risk Management team) is the Model Owner.
8.2. They must complete the `MER-FORM-AIML-014c` Third-Party Model Documentation Supplement, demanding equivalent information from the vendor.
8.3. If the vendor provides their own model card in a standard format, it can be attached, but the Meridian supplement evaluating the vendor's card against our standards must be completed. Any gaps (e.g., vendor does not provide segment-level performance) must be documented as a Limitation and an MRE (Model Risk Exception, see Section 8) must be filed.

### 5.9 Step 9: Decommissioning a Model

9.1. To decommission a model, the Model Owner must create a JIRA issue: `JIRA: MLC-RET-###`.
9.2. Attach a "Model Decommissioning Report" to the model documentation, which details the reason for retirement, the date of final inference, the disposal of model artifacts, and the plan for monitoring any residual downstream impacts.
9.3. The MRM Committee reviews the decommissioning report at its next weekly meeting. If approved, the model's status in the MLflow Registry is changed to `Archived`. The model card JSON and all documentation remain in the GRC system as an immutable audit record but are marked with a `Decommissioned` badge.

### 5.10 Step 10: Retroactive Documentation for Existing Models

A phased approach is mandated for all models that were in production prior to the effective date of this SOP version (2024-10-02).

| Model Tier | Inventory Completion Deadline | Full Documentation & Approval Deadline | Accountable Leader |
| :--- | :--- | :--- | :--- |
| Tier 3 (High Risk) | 2024-11-15 | 2025-01-31 | Dr. Marcus Rivera, CAIO |
| Tier 2 (Moderate Risk) | 2024-12-31 | 2025-03-31 | Respective VPs |
| Tier 1 (Low Risk) | 2025-01-31 | 2025-06-30 | Respective Directors |

The CCO, Thomas Anderson, will provide a monthly compliance status report to the Executive Leadership Team, tracking completion against these deadlines. Non-compliance will be escalated per Section 8 of this SOP.

---

## 6. Controls and Safeguards

### 6.1 Technical Controls

| Control ID | Control Description | Tool/Implementation |
| :--- | :--- | :--- |
| **TEC-AIML-014-01** | Immutable documentation versions are enforced. All approved documents are hashed (SHA-256) and stored in a write-once-read-many (WORM) compliant GRC repository. | Meridian GRC Platform (OneTrust) |
| **TEC-AIML-014-02** | Model registry enforces a gated promotion policy. A model artifact cannot be moved from the `Staging` to `Production` stage unless the status of the linked documentation object in the GRC system is `Approved`. | MLflow Model Registry API integration with OneTrust GRC API |
| **TEC-AIML-014-03** | Performance metric population in the model card template must be automated and auditable. A direct API link between the MLflow run and the GRC template is the only permitted method for populating final benchmark tables. Manual typing is blocked. | MLflow Tracking API, GRC Form Automation |
| **TEC-AIML-014-04** | Access to "Approved" model documentation is read-only for all roles except the GRC Administrators in the CAIO office and the CISO’s office. Editing requires a new version (check-out/check-in process). | Role-Based Access Control (RBAC) in Meridian GRC Platform, synced with Okta (`group: grc_modeldoc_admin`) |
| **TEC-AIML-014-05** | An audit log captures all views and changes to the documentation, providing a non-repudiable chain of custody. | AWS CloudTrail, OneTrust audit logs |

### 6.2 Administrative Controls

- **Segregation of Duties:** The QA Lead performing the independent validation per SR 11-7 (Section 5.6.2) must not have been involved in the model's development. Their compensation and performance review are structured to not be dependent on model deployment timelines.
- **Committee Governance:** The MRM Committee must maintain a documented quorum, including the CAIO, CCO (or delegate), and at least one non-voting technical expert. Formal meeting minutes documenting all approval and risk acceptance decisions are mandatory.
- **Mandatory Templates:** Only officially approved templates (`MER-FORM-AIML-014a/b/c`) may be used. Any deviation requires a formal template exemption approved by the CAIO office.

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Process KPIs for Model Documentation

These KPIs measure the health and compliance of the documentation process itself and are reported to the MRM Committee monthly.

| KPI | Target | Owner | Dashboard Tile |
| :--- | :---: | :--- | :--- |
| **Documentation Completeness** | 100% of Tier 3 models, 95% of Tier 1 & 2 | Model Owners | GRC_DOCS_001 |
| **Average Time-to-Approval (Tier 3)** | < 30 calendar days from initial submission | MRM Committee Chair | GRC_DOCS_002 |
| **Overdue Annual Revalidations** | 0 | CAIO Office | GRC_DOCS_003 |
| **Models Flagged with Active MREs (Model Risk Exceptions)** | < 5% of total model inventory total | CCO | GRC_RISK_001 |

### 7.2 Quarterly Documentation Health Audits

The CAIO office will perform a random sampling audit each quarter, selecting 10 models (with a mandatory minimum of 3 HealthPay models). The audit checks:
- Existence and currency of all required documentation.
- Accuracy and completeness of the Intended Use and Limitations against current product functionality.
- Validity of all links in the model card (Datadog dashboards, source code, etc.).
- Adherence to the review and sign-off workflow.

A report of the audit is presented to the Board-level AI Governance Committee.

---

## 8. Exception Handling and Escalation

### 8.1 Model Risk Exception (MRE) Process

Any deviation from the requirements of this SOP must be formally managed through the Model Risk Exception process.

1.  **Identification:** The Model Owner identifies a non-compliance or a need to deviate from the standard process (e.g., inability to obtain segment-level data from a vendor, requesting a 10-day extension to complete the revalidation).
2.  **Submission:** The Model Owner creates a `Model Risk Exception` record in the GRC system, linked to the model's record. The submission must include:
    - A clear description of the non-compliance.
    - A documented compensating control or justification.
    - An impact assessment explaining the risk of accepting the exception.
    - A proposed remediation plan with a hard deadline (not to exceed 90 days).
3.  **Approval Authority:**
    - **Minor Exceptions** (e.g., extension of an annual review deadline by < 30 days, minor template field omission): Approval by the Director of Model Risk Management in the CAIO Office.
    - **Major Exceptions** (e.g., deploying a Tier 3 model without full segment-level fairness analysis, accepting an external model card without performance benchmarks, any exception related to a credit model): Approval by the full MRM Committee, with mandatory non-concurrence documentation from the CCO if the exception is accepted.
4.  **Tracking:** All open MREs are tracked on the GRC_RISK_001 dashboard. Any MRE exceeding its remediation deadline is automatically escalated to the CEO, Dr. Sarah Chen, and the CISO, Rachel Kim, for a formal risk acceptance decision.

### 8.2 Emergency Escalation

If a critical model failure is observed that violates the stated Limitations or renders the model documentation dangerously inaccurate (e.g., a 50% drift in population stability overnight), the Model Owner must:
1.  Immediately initiate a `Severity-1` PagerDuty incident using the `model-risk-immediate` service.
2.  This pages the VP of Engineering (David Park), the on-call SRE, the CISO (Rachel Kim), and the CAIO (Dr. Marcus Rivera).
3.  Within two hours, the incident commander (first responder from the on-call rotation) must decide whether to automatically roll back the model to the last known good version or shut down its API endpoint, per SOP-OPS-120.
4.  A post-mortem analysis, including an immediate update to the model card, is required within 48 hours. This is a regulatory-critical process for financial models under SR 11-7.

---

## 9. Training Requirements

### 9.1 Mandatory Training

All personnel in the "Responsible" or "Accountable" roles in the RACI matrix must complete the following training.

| Training Module | Code | Frequency | Target Audience | Delivery Method |
| :--- | :--- | :--- | :--- | :--- |
| **SOP-AIML-014 Compliance Training** | TRN-AI-014 | Annually | Model Developers, Owners, QA, VPs | Meridian LMS (Workday) - Interactive Course & Assessment |
| **SR 11-7 Model Risk Management for AI/ML** | TRN-RMG-110 | Annually | All HealthPay Model Developers, Owners, and the MRM Committee | Instructor-led by CCO Thomas Anderson |
| **Writing Effective Intended Use and Limitations** | TRN-AI-015 | Once, and then upon SOP update | All Model Developers and Owners | Workshop led by Dr. Aisha Okafor's design team |
| **Bias Detection and Fairness Analysis** | TRN-AI-008 | Annually | All Model Developers, QA Leads | Online Course via Coursera for Enterprise |

### 9.2 Training Compliance Tracking

The Chief Human Resources Officer, Jennifer Walsh, is accountable for ensuring the Meridian LMS (Workday) accurately tracks training completion. A "Training Compliance" dashboard is published monthly, and 100% completion is required for any individual to be granted permissions to the MLflow `Staging` or `Production` environments. The Okta integration with MLflow will automatically suspend access for any user whose mandatory training is >30 days past due.

---

## 10. Related Policies and References

### 10.1 Internal Meridian SOPs

| SOP ID | Policy Name | Relationship |
| :--- | :--- | :--- |
| SOP-RMG-001 | Model Risk Management Governance and Committee Charter | Defines the MRM Committee that governs this procedure. |
| SOP-SEC-005 | Access Control and Identity Management Policy | Governs the Okta RBAC for GRC and MLflow. |
| SOP-AIML-008 | Algorithmic Fairness, Bias Testing, and Remediation | Details the fairness and bias analysis referenced in Section 5.3. |
| SOP-AIML-022 | Model Inventory and Lifecycle Management | The procedural counterpart for model asset management. |
| SOP-DATA-003 | Data Classification and Handling Standard | Governs PHI/PII data source annotations in the model card. |
| SOP-GRC-010 | Regulatory Exam and Audit Management | Manages interactions with auditors reviewing model documentation. |
| SOP-OPS-120 | Incident Management and Major Incident Response | Governs the emergency escalation in Section 8.2. |

### 10.2 External References

| Reference | Description |
| :--- | :--- |
| Federal Reserve SR Letter 11-7 | Guidance on Model Risk Management |
| Meridian Model Card Schema v2 (`meridian-model-card-schema-v2.json`) | JSON/YAML schema definition for model cards |
| Meridian MLflow Tracking Server Operations Guide | Internal wiki for MLflow usage standards |
| HITRUST CSF v11 | Control framework for security and privacy controls |

---

## 11. Revision History

| Version No. | Effective Date | Author(s) | Description of Changes |
| :--- | :--- | :--- | :--- |
| 1.0 | 2021-05-15 | Dr. Elena Ross (former CAIO) | Initial creation of formal Model Card procedure. Aligned with initial SOC 2 requirements. |
| 2.2 | 2022-11-08 | Dr. Marcus Rivera | Major revision. Introduced Tiered risk approach and mandatory model card JSON schema. Integrated with MLflow. |
| 2.5 | 2023-03-22 | Thomas Anderson (CCO) | Added specific SR 11-7 evidentiary requirements in Section 5.6 for HealthPay models per Federal Reserve feedback. |
| 2.8 | 2024-02-10 | Dr. Aisha Okafor & Robert Liu | Clarified Intended Use/Limitation sign-off roles. Added detailed SLAs to the review workflow (Section 5.4). |
| 2.9 | 2024-10-02 | Dr. Marcus Rivera | Finalized retroactive documentation mandate (Section 5.10). Strengthened independent QA validation controls. Added emergency escalation contact list. Effective date for v2.9 mandate. |