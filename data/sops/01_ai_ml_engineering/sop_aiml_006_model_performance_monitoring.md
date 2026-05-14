```yaml
---
sop_id: "SOP-AIML-006"
title: "Model Performance Monitoring"
business_unit: "AI/ML Engineering"
version: "2.6"
effective_date: "2024-03-04"
last_reviewed: "2025-03-15"
next_review: "2025-09-05"
owner: "Dr. Marcus Rivera, Chief AI Officer"
approver: "David Park, VP of Engineering"
classification: "Internal"
regulations:
  - "EU AI Act"
  - "SR 11-7"
  - "NIST AI RMF"
status: "Active"
---

# Standard Operating Procedure: Model Performance Monitoring

**SOP-AIML-006 | Version 2.6**
**Effective: 2024-03-04**
**Owner: Dr. Marcus Rivera, Chief AI Officer**
**Business Unit: AI/ML Engineering**

---

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the framework for the continuous monitoring of machine learning (ML) and artificial intelligence (AI) model performance across all business lines at Meridian Health Technologies, Inc. The purpose of this document is to define the standardised processes, quantitative metrics, alerting thresholds, and remediation protocols required to ensure that all production-deployed models operate within the risk appetite and performance tolerances approved during model validation.

Effective model performance monitoring is critical to maintaining the safety, efficacy, and compliance of Meridian's products, including the Clinical AI Platform, HealthPay Financial Services, MedInsight Analytics, and the underlying Meridian SaaS Platform. This SOP ensures that model degradation, data drift, and concept drift are detected early and addressed systematically, thereby protecting patient safety, maintaining financial integrity, and upholding regulatory obligations. A core objective of this monitoring is to provide transparency into automated decision-making processes, ensuring that the logic and performance of systems can be explained to relevant stakeholders upon request.

### 1.2 Scope

This SOP applies to all models—defined broadly as any algorithm, statistical model, or machine learning system—that have been promoted to a `Production` or `Shadow Deployment` environment and are managed within the Meridian Model Registry (MMR). This includes, but is not limited to:

| Category | Business Unit | Examples |
| :--- | :--- | :--- |
| **High-Risk AI Systems** | Clinical AI Platform | Diagnostic imaging analysis models, patient risk scoring models (e.g., sepsis prediction, 30-day readmission), adverse event prediction systems. |
| **Financially Regulated Models** | HealthPay Financial Services | Credit scoring models, medical lending underwriting algorithms, fraud detection models, claims adjudication automation. |
| **Population Health Models** | MedInsight Analytics | Care gap identification models, disease progression predictors, hospitalisation risk stratifiers. |
| **Platform and Operational Models** | Meridian SaaS Platform | Anomaly detection systems, user behaviour analytics, resource auto-scaling predictors. |

The scope covers all phases of the model lifecycle post-deployment, including active monitoring, trigger-based re-validation, and systematic degradation response. This SOP applies to models deployed on both primary (AWS `us-east-1`, `eu-west-1`) and disaster recovery (Azure) environments. All full-time employees, contractors, and third-party vendors involved in the development, deployment, maintenance, and governance of AI/ML systems are subject to this procedure.

---

## 2. Definitions and Acronyms

For the purposes of this document, the following terms are defined:

| Term | Definition |
| :--- | :--- |
| **Model Risk Appetite** | The aggregate level and types of risk Meridian's Board of Directors and executive management are willing to accept in pursuit of its strategic objectives regarding model-driven products. Defined per model in its Model Risk Tiering document. |
| **Model Risk Tier** | A classification (Tier 1-Critical, Tier 2-High, Tier 3-Moderate, Tier 4-Low) assigned to each model based on its potential for patient harm, financial loss, or regulatory non-compliance. Determines monitoring frequency and response timelines. |
| **Production Model** | A model whose outputs are actively consumed by a business-facing application, directly affecting decisions, clinical workflows, or financial transactions without a human-in-the-loop gate. |
| **Shadow Model** | A model deployed in production infrastructure to generate inferences on live data without impacting business processes. Used for "silent" champion/challenger testing and performance validation. |
| **Drift** | A change in the statistical properties of the model's inputs (Feature Drift), conditional distribution of the target given inputs (Concept Drift), or the distribution of the model's predictions (Output Drift) over time. |
| **Prediction Stability Index (PSI)** | A metric quantifying the divergence of a distribution (e.g., a feature or model score) in a monitoring window from a reference distribution (typically the validation sample). |
| **Characteristic Stability Index (CSI)** | A metric quantifying the divergence of a single feature's distribution from its training distribution. |
| **Baseline Performance** | The reference set of performance metrics (e.g., AUC, F1-score, RMSE) recorded during the official model validation stage prior to production release, as documented in the Model Validation Report (SOP-VAL-001). |
| **Meridian Model Registry (MMR)** | The central, governed repository for all model artifacts, metadata, approval statuses, and monitoring configurations. Implemented as a hosted `mlflow` server with a Postgres backend. |
| **Meridian Observability Platform (MOP)** | The company-wide observability stack (Grafana, Prometheus, Loki, Tempo) used for aggregating application logs, infrastructure metrics, and business-level KPIs, including model monitoring metrics. |

### 2.1 Acronyms

- **AI/ML:** Artificial Intelligence / Machine Learning
- **CSD:** Clinical Safety Dashboard
- **FPD:** Financial Performance Dashboard
- **MOP:** Meridian Observability Platform
- **MMR:** Meridian Model Registry
- **MRE:** Model Risk Engineer (AI/ML Engineering)
- **PSI:** Prediction Stability Index
- **CSI:** Characteristic Stability Index
- **MSE:** Mean Squared Error
- **AUC:** Area Under the Receiver Operating Characteristic Curve
- **SLO:** Service Level Objective
- **MTTD:** Mean Time to Detect
- **MTTR:** Mean Time to Resolve

---

## 3. Roles and Responsibilities

A clear assignment of accountability is essential for the integrity of the model monitoring lifecycle. The following Responsibility Assignment Matrix (RACI) outlines the roles for all key procedures defined in this SOP.

**RACI Key:**
- **R**esponsible: The role performing the work.
- **A**ccountable: The role ultimately answerable for the completion and correctness of the task. Only one 'A' per task.
- **C**onsulted: Subject matter experts who are involved before a decision or action is taken.
- **I**nformed: Roles who are kept up-to-date on progress after the action is taken.

| Procedure / Task | Model Risk Engineer (AI/ML) | Model Owner (Product/Clinical/Fin) | VP of Engineering (Approver) | MLOps Engineer (Platform) | Clinical Safety Lead | Compliance Officer |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Configuration of Monitoring Dashboards** | **A/R** | C | I | R | C | I |
| **Daily Review of Tier 1 Model Dashboards** | **A/R** | — | — | — | — | — |
| **Weekly Performance Report Generation** | **A** | R | — | R | — | — |
| **Detection and Initial Triage of Drift Alerts** | **A/R** | — | — | C | — | — |
| **Clinical Impact Assessment During Degradation** | R | C | I | I | **A/R** | I |
| **Financial Impact Assessment During Degradation (HealthPay)** | R | **A/R** | I | I | — | I |
| **Approval of Model Rollback or Shutdown** | C | R | **A** | — | C | C |
| **Post-Mortem Facilitation and Root Cause Analysis** | **A/R** | C | C | C | C | — |
| **Annual SOP Review and Update** | C | C | I | — | C | **A/R** |

**Role Descriptions:**

- **Model Risk Engineer (AI/ML Engineering):** The primary operational role. Responsible for the health, performance, and accurate execution of all production models. Sets monitoring configurations, analyses drift reports, manages the MMR performance log, and executes tier-appropriate degradation response protocols.
- **Model Owner (Product, Clinical, or Financial Lead):** A business-line owner accountable for the business and safety outcomes of a specific model. For a Clinical AI model, this is a Clinical Safety Lead. For a HealthPay model, this is a VP of Financial Risk. They are accountable for articulating the business impact of model degradation and approving remediation plans.
- **VP of Engineering:** The approval authority for high-impact actions such as a full model shutdown or an emergency rollback of a Tier 1 model. Escalations for Tier 1 clinical model risks are routed here.
- **MLOps Engineer (Platform):** Responsible for the tooling and infrastructure (MOP, MMR, Feature Store) that enables the monitoring procedures. Acts as a consultant for complex technical troubleshooting.

---

## 4. Policy Statements

The following policy statements establish the non-negotiable requirements for all model monitoring activities at Meridian Health Technologies.

**PS-001: Mandatory Monitoring**
All Production and Shadow Models must have a full suite of operational and performance monitoring configured in the Meridian Observability Platform (MOP) and the Meridian Model Registry (MMR) prior to production activation. No model shall be promoted to Production without a corresponding, approved Monitoring Configuration document in its MMR artifact package.

**PS-002: Risk-Tiered Monitoring Cadence**
Monitoring is not a uniform process. The frequency of automated metric calculation and human review is governed by the model's Model Risk Tier, ensuring resources are allocated proportionally to risk.

| Model Risk Tier | Automated Metric Evaluation | Dashboard Review Cadence | Full Re-Validation Trigger |
| :--- | :--- | :--- | :--- |
| **Tier 1 (Critical)** | Continuous (per-inference batch) | Daily (human review) | Bi-Annual or upon Alert Trigger |
| **Tier 2 (High)** | Hourly | Weekly (human review) | Annual or upon Alert Trigger |
| **Tier 3 (Moderate)** | Daily | Monthly (automated report) | Upon Alert Trigger |
| **Tier 4 (Low)** | Weekly | Quarterly (automated report) | Upon Alert Trigger |

**PS-003: Threshold-Based Alerting**
All Tier 1 and Tier 2 models must have specific, quantitative alerting thresholds configured in MOP for both drift metrics and core performance metrics. Alerts must be actionable. Generic health checks without defined thresholds are prohibited. All alerting thresholds must be reviewed and approved during the Model Validation stage.

**PS-004: Degradation Response Lifecycle**
Every detected anomaly that breaches a defined `Warning` threshold must be formally tracked as an Issue in the MMR, regardless of whether it is a confirmed or false-positive alert. This log serves as an auditable record of model stability and operational transparency.

**PS-005: Prohibition of Data Unblinding**
For Clinical AI models deployed in "Shadow" mode for validation, the monitoring pipeline must never route model outputs to a clinical user interface or back into the Electronic Health Record (EHR) feed. Shadow data pipelines must be physically or logically isolated.

---

## 5. Detailed Procedures

This section defines the step-by-step operational workflows for the core monitoring lifecycle. All model operators shall adhere to these procedures.

### 5.1 Procedure: Model Monitoring Onboarding (Pre-Deployment)

This procedure is executed jointly by the Model Risk Engineer and the MLOps Engineer during the `Staging` phase of the Model Lifecycle, prior to a `Promotion to Production` request.

1.  **Obtain Approved Model Risk Tier:** The Model Risk Engineer locates the `Model_Risk_Tier` tag in the MMR artifact. This tier governs all subsequent steps.
2.  **Retrieve Baseline Performance:** Navigate to the Model Validation Report artifact (`SOP-VAL-001`) in the MMR and extract the baseline performance metrics. For a classification model, this includes AUC, F1-score, Precision, Recall. For regression, RMSE, MAE, R-squared.
3.  **Define Metrics and Thresholds:**
    a.  **Performance Metrics:** Select a primary and secondary performance metric from the baseline. Set a `Critical` threshold as a 10% absolute drop from baseline for Tier 1 models, and a `Warning` threshold as a 5% absolute drop.
    b.  **Drift Metrics:** For the top 10 most important features (as defined in the model's SHAP explainability report), calculate CSI. Set a `Warning` threshold at CSI > 0.1 and a `Critical` threshold at CSI > 0.2. Set a `Critical` threshold for Concept Drift (via proxy metric) at a 5% PSI of model outputs week-over-week.
4.  **Create Monitoring Configuration YAML:** Commit a file named `monitoring_config.yaml` to the model's MMR artifact directory. This file precisely defines all metrics, lookback windows, and thresholds.
5.  **Configure MOP Dashboard:** In Grafana, clone the standard `Meridian_Model_Monitoring_Template` dashboard and bind it to the model's MMR ID. Configure the panels using the exact queries derived from the `monitoring_config.yaml` file.
6.  **Configure Alerting Rules:** Implement alerting rules in Prometheus AlertManager. Route `Warning` alerts to the owning team's Slack channel (`#ml-eng-alerts-general`) and `Critical` alerts to the `#ml-eng-critical-alerts` channel with PagerDuty escalation.
7.  **Post-Deployment Smoke Test:** Immediately after the model's first production inference, manually execute a query in MOP to confirm data logging, metric calculation, and dashboard rendering are functional.

### 5.2 Procedure: Daily Monitoring Review for Tier 1 Models

This is a mandatory, daily-start-of-day task for the on-call Model Risk Engineer.

1.  **Access MOP Dashboard:** Log into the Meridian Observability Platform (MOP) and navigate to the `Tier 1 Model Monitoring` folder. Verify all dashboards are reporting valid data streams without `NO DATA` errors.
2.  **Systematically Inspect Each Model:**
    a.  **Check for Active Alerts:** In the `Alerting` panel, note any alerts generated in the last 24 hours. Acknowledge each active alert in AlertManager.
    b.  **Review Output Distribution:** Inspect the "Model Output Distribution" panel. Visually compare the histogram of the last 24 hours' predictions against the "Baseline (Validation)" distribution. Any visually obvious and sustained shift constitutes a drift anomaly, irrespective of whether a threshold breached.
    c.  **Inspect Top Feature CSI Trends:** Review the "Top 5 Feature Drift" panel. Check for any feature with a CSI > 0.1 that is trending upward over a 7-day rolling window.
3.  **Logging the Review:** For every Tier 1 model, generate an automated daily report from the MOP dashboard using the `Generate Report` function. This report must include the core metrics, drift charts, and an explicit "No Anomalies / Anomalies Detected" tag. This report is automatically stored in the MMR as an `Operational_Log` artifact.
4.  **Incident Detection:** If any of the following conditions are true, the Monitoring Review is considered "FAILED," and the Model Degradation Response Procedure (Section 5.4) must be initiated immediately.
    - A `Critical` performance or drift alert is firing.
    - A `Warning` alert has been firing continuously for >24 hours.
    - A CSI > 0.25 is observed for any single critical feature.
    - The model has served a `NaN` or `null` value to a downstream application in the last hour.

### 5.3 Procedure: Scheduled Model Performance Re-Evaluation

This procedure formalises the periodic re-calculation of baseline metrics against a held-out, labelled ground-truth dataset to detect concept drift. It is performed according to the risk-tiered cadence in Policy Statement PS-002.

1.  **Acquire Ground-Truth Data:**
    a.  **Clinical AI Models:** Query the Clinical Data Lake `cln_datalake_production.labels` for the relevant patient outcome labels that correspond to the inference window being evaluated (e.g., 6-month readmission status for predictions made 6 months ago).
    b.  **HealthPay Models:** Query the `fin_warehouse.transactions_reconciled` table for the final fraud flags, loan defaults, or claim adjudication outcomes.
2.  **Generate Evaluation Script:** Create a containerised evaluation job using the model artifact's scoring image. The script must join the logged inference data (Model Input Features + Model Score + Timestamp) with the ground-truth labels on a unique record identifier.
3.  **Calculate Performance Metrics:** Execute the evaluation job. Compute the primary and secondary performance metrics (e.g., AUC, RMSE) on the new data window.
4.  **Compare to Baseline:** Compare the computed windowed metric against the Baseline Performance recorded in the MMR.
5.  **Document Results:** Create a `Model_Performance_Reevaluation_Report` (using template `TEMP-AIML-006A`) and attach it as an artifact to the model in the MMR. The report must state the evaluated period, the calculated metric, the baseline metric, and a variance analysis.
6.  **Initiate Alert if Degraded:** If the windowed metric breaches the `Warning` threshold (5% absolute drop), an Issue must be created in the MMR and the Model Degradation Response Procedure triggered.

### 5.4 Procedure: Model Degradation Response

This procedure is the core reactive workflow for managing model performance decay or severe drift.

**Phase 1: Alert & Triage (Target: < 1 hour)**

1.  **Acknowledge Alert:** The Model Risk Engineer acknowledges the `Critical` PagerDuty alert or manually creates a high-priority Issue in the MMR based on a `Warning` threshold breach flag.
2.  **Create MMR Issue:** In the Meridian Model Registry, create a new `Degradation` type Issue linked to the specific model. Populate the `Initial Diagnosis` field with the specific alert, metric threshold breached, and time of detection.
3.  **Conduct Triage:** The Model Risk Engineer performs a 45-minute triage to determine the likely root cause category.
    - **Category A - Data Pipeline Drift:** An upstream data source has changed. This is often indicated by many features simultaneously breaching a CSI > 0.15 threshold. Triage Action: Rollback deployment of the upstream data processing job (e.g., Spark job) and investigate data producer systems.
    - **Category B - Model Performance Degradation:** Core metrics (e.g., AUC) are falling against ground-truth labels, but feature distributions are stable. Triage Action: This is a fundamental loss of predictive power (Concept Drift). Proceed to Phase 2.
    - **Category C - Operational Code Bug:** A bug in the model serving container or inference script introduced a calculation error (e.g., NaNs). Triage Action: Initiate a hotfix in the Software Development Lifecycle (SOP-ENG-101) to revert to the prior stable container image.
4.  **Initial Notification:** Based on the triage category, notify stakeholders. For Category B for a Tier 1 Clinical AI model, immediately inform the Clinical Safety Lead and VP of Engineering via the `#aet-incident-response` Slack channel.

**Phase 2: Impact Assessment & Interim Mitigation (Target: < 4 hours)**

1.  **Conduct Impact Assessment:** The Model Owner must complete the `Model_Impact_Assessment_Form` (TEMP-AIML-006B) within 2 hours. This form details the operational, clinical, and financial impact of the model's current degraded state.
2.  **Determine Mitigation Strategy:** The Model Risk Engineer and Model Owner jointly decide on an interim mitigation. Options include:
    - **Mitigation-A: Threshold Adjustment:** If the degradation is safe but suboptimal (e.g., a false-positive rate increase on a non-critical alert), adjust the model's operating point decision threshold via a feature flag to restore operational utility.
    - **Mitigation-B: Fallback to Heuristic:** For Tier 1 models, immediately fall back to a validated heuristic rules engine or manual human review queue. This is activated via a global circuit breaker in the application.
    - **Mitigation-C: Full Rollback:** Trigger a CI/CD rollback to the last known-good production model version. This requires VP of Engineering approval for Tier 1 models.
3.  **Execute Interim Mitigation:** The chosen mitigation is implemented by the MLOps Engineer and Model Risk Engineer. A `Model_Rollback` or `Mitigation_Implementation` event is logged in the MMR.

**Phase 3: Root Cause Analysis & Long-Term Remediation (Target: < 5 business days)**

1.  **Facilitate Post-Mortem:** The Model Risk Engineer facilitates a blameless post-mortem within 5 days. The output is a remediation plan attached to the MMR Issue.
2.  **Execute Remediation:** Long-term fixes, such as retraining the model on new data, re-architecting the feature pipeline, or commissioning a new "Challenger" model, are tracked as sub-tasks of the MMR Issue.
3.  **Close Issue:** The MMR Issue is only closed once the remediation plan is fully implemented, and the newly retrained or hotfixed model has been successfully re-promoted to Production through the standard Model Validation procedure (SOP-AIML-005).

---

## 6. Controls and Safeguards

This section describes the administrative and technical controls that enforce the procedures and policy statements defined in this SOP.

### 6.1 Administrative Controls

- **Issue Tracking and Audit Trail:** The Meridian Model Registry (MMR) serves as the immutable, auditable system of record for every degradation event, triage decision, and remediation action for each model version. All lifecycle events are timestamped and linked to an authenticated user.
- **Annual Model Performance Review:** As part of the broader model governance framework, every production model must undergo a comprehensive annual review, culminating in a `Model Performance Summary Report`. This report is reviewed by the AI/ML Governance Committee.
- **Transparency Reporting:** To support the organization's commitment to openness in automated systems, a generic register of high-impact automated decision-making systems is maintained. For inquiries received through standard channels, authorized personnel can provide the operational status and intended purpose of the system, and, upon request, furnish the high-level logic of the decision-making process.
- **Technical Documentation Pack:** A formal `Model Technical Documentation Pack` is maintained for all Tier 1 and Tier 2 models. This pack contains the model development lifecycle, a description of training data and methodology, validation results, and the operational monitoring configuration.

### 6.2 Technical Controls

- **Immutable Logging:** Model inputs, outputs, and the exact serving environment (Docker SHA256 digest) for every inference are streamed to an immutable, append-only event store (`meridian-lake.events.inference`) for subsequent auditing, drift analysis, and ground-truth evaluation.
- **Circuit Breaker Pattern:** All Tier 1 Critical model services are deployed behind an application-level circuit breaker. If the model endpoint's error rate exceeds 5% or response latency P99 exceeds 2 seconds, the circuit breaker "trips" to an `Open` state, rerouting traffic to a pre-defined fallback heuristic or a safe return value.
- **Inference Pipeline Validation (Guard Script):** A pre-execution "guard script" validates each incoming feature record before inference. It ensures all required features are present, are within valid data types (e.g., no string in a numeric field), and are within 5 standard deviations of the training data mean for critical features. Records failing validation are routed to a dead-letter queue and logged.
- **Shadow Deployment Isolation:** Shadow models (e.g., for champion/challenger testing) are deployed into a logically separate Kubernetes namespace (`model-inference-shadow`) with no network policy allowing egress to production application databases or queues. Their outputs are written exclusively to a dedicated analytics sink.

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs) for the Monitoring Process

To ensure the model monitoring process itself is effective, the AI/ML Engineering function will track the following operational KPIs:

| KPI | Description | Target |
| :--- | :--- | :--- |
| **Mean Time to Detect (MTTD)** | The average time from the onset of a mathematically verifiable `Critical` drift/prediction degradation to its detection by either an automated alert or a human review. Measured retrospectively via post-mortems. | Tier 1: < 1 hour; Tier 2: < 8 hours |
| **Mean Time to Resolve (MTTR)** | The average time from MMR Issue creation for a `Critical` degradation to the execution of an interim mitigation (Phase 2 of Response). | Tier 1: < 4 hours |
| **Alert Signal-to-Noise Ratio** | The ratio of `(Actionable Alerts)` to `(Actionable Alerts + False-Positive Alerts)` over a rolling 30-day period. | ≥ 70% |
| **% Models Compliant with Monitoring** | The percentage of Production models with a fully configured and healthy MOP dashboard vs. total Production models. | 100% |

### 7.2 Model Monitoring Dashboards

The Meridian Observability Platform (MOP) will serve as the single pane of glass for model health. Each model has a tier-specific, standardised dashboard.

**Tier 1 & 2 Model Dashboard Panels:**
- **Real-time Prediction Output:** A live histogram of prediction scores, overlayed with warning and critical control bands based on the validation baseline.
- **Top 5 Feature Stability:** Time-series line charts for the PSI/CSI of the top 5 most critical features. Horizonal lines indicate `Warning` (0.1) and `Critical` (0.2) thresholds.
- **Service-Level Objective (SLO) Burn Rate:** A panel displaying the burn rate for SLOs, such as prediction latency P95 < 500ms and availability of the scoring endpoint.
- **Evaluation Performance Trend:** A line chart showing re-evaluation scores (e.g., AUC, RMSE) from the last four Scheduled Re-Evaluations, plotted against the `Warning` performance threshold.

### 7.3 Reporting Cadence

| Report Type | Audience | Frequency | Content |
| :--- | :--- | :--- | :--- |
| **Automated Daily Digest (Tier 1 only)** | Model Risk Engineers, Clinical Safety Lead | Daily | A system-generated summary of nightly batch performance, alert statuses, and output distribution histograms for all Tier 1 models. |
| **Model Performance Weekly Snapshot** | AI/ML Engineering Director, Model Owners | Weekly | A scorecard of all Tier 1 and Tier 2 models, showing a "Red/Amber/Green" (RAG) status for each major metric category. |
| **Model Health Quarterly Report** | AI/ML Governance Committee, VP of Engineering | Quarterly | An aggregated review of model ecosystem health, including MTTD/MTTR trends, major degradation incidents, and KPI compliance. |
| **Technical Documentation for Individual Inquiries** | Compliance Officer, Legal Counsel | Ad-hoc | A report detailing the performance envelope, intended use, and operational logic for a specified system to be furnished as part of a structured transparency request. |

---

## 8. Exception Handling and Escalation

### 8.1 Exception Handling

Any proposed deviation from the mandatory monitoring procedures or thresholds defined in this SOP must be managed through a formal exception process.

1.  **Exception Request Initiation:** The Model Owner must submit a `Model Monitoring Exception Request` (TEMP-AIML-006C) through the Meridian Model Registry. The request must clearly state the specific procedure or threshold for which an exception is sought, provide a compelling business or technical rationale, detail a compensating control, and specify the duration of the exception.
2.  **Risk Assessment:** The Model Risk Engineer conducts a risk assessment of the proposed exception and annotates the request form with their findings.
3.  **Approval Authority:**
    - Exceptions for Tier 4 models: Approved by the Director of AI/ML Engineering.
    - Exceptions for Tier 3 models: Approved by the Director of AI/ML Engineering and the responsible Model Owner.
    - Exceptions for Tier 1 or Tier 2 models: This constitutes a significant increase in risk and must be approved by the **VP of Engineering**. The approval must be documented in writing and attached to the request in the MMR.
4.  **Tracking and Expiry:** Every approved exception is a time-bound, tracked artifact in the MMR. A system-generated notification is sent to the owner 48 hours prior to its expiration. Expired exceptions automatically trigger a requirement for re-validation of the model's monitoring configuration.

### 8.2 Escalation Matrix

Model risk issues identified during monitoring that cannot be resolved at the operator level are escalated on a strict timeline using the following matrix.

| Severity | Condition | First Contact | Escalation (if no ACK in 30 min) | Escalation (Critical only, if no resolution in 2 hrs) |
| :--- | :--- | :--- | :--- | :--- |
| **Critical (P1)** | - `Critical` threshold breach on a Tier 1 model. - Any model serving errors to patient care. | On-call Model Risk Engineer (via PagerDuty). | VP of Engineering, Clinical Safety Lead (if applicable). | Chief AI Officer (Dr. Marcus Rivera), Chief Medical Officer (for clinical models). |
| **High (P2)** | - `Critical` threshold breach on a Tier 2 model. - Tier 1 model `Warning` breach sustained for >24hrs. | On-call Model Risk Engineer (via Slack `#ml-eng-critical`). | Model Owner, Director of AI/ML Engineering. | Chief AI Officer. |
| **Moderate (P3)** | - `Warning` threshold breach on any model. | Assigned Model Risk Engineer (via MMR ticket). | Model Owner (next business day). | N/A |

---

## 9. Training Requirements

### 9.1 Required Training

All personnel identified in the Roles and Responsibilities matrix (Section 3) must complete the assigned training modules commensurate with their role before being granted operational privileges (e.g., MMR approval permissions, MOP editor access).

| Training Module Code | Module Name | Target Audience | Frequency | Format |
| :--- | :--- | :--- | :--- | :--- |
| **AIML-TRN-001** | Model Lifecycle and Governance Fundamentals | All AI/ML engineers, MLOps, Model Owners | Annually | Online, self-paced (Workday) |
| **AIML-TRN-006** | **SOP-AIML-006 in Practice: Performance Monitoring Operations** | Model Risk Engineers, MLOps Engineers | Annually, and within 30 days of hire | Instructor-led workshop with hands-on MOP sandbox |
| **AIML-TRN-007** | Degradation Response & Root Cause Analysis | Model Risk Engineers, Model Owners | Annually | Simulated incident tabletop exercise |
| **REG-TRN-001** | General Data Protection and Automated Decision-Making | All employees with access to production model artifacts | Annually | Online, self-paced (Workday) |

### 9.2 Training Tracking and Compliance

- Completion of training is tracked in the Workday Learning Management System.
- Compliance status is audited quarterly by the AI/ML Governance Committee. The Director of AI/ML Engineering is accountable for ensuring a 100% completion rate for their direct and indirect reports.
- Access to the `prod` and `shadow` namespaces in the Meridian Model Registry is automatically revoked for any user whose mandatory annual training is more than 30 days overdue.

---

## 10. Related Policies and References

The following internal Meridian Health Technologies policies and external standards are directly relevant and binding to this SOP.

### 10.1 Internal Meridian SOPs

| SOP ID | Title | Relationship to This SOP |
| :--- | :--- | :--- |
| **SOP-AIML-005** | Model Validation and Approval | Defines the process that establishes the `Baseline Performance` metrics and `Model Risk Tier` used herein. |
| **SOP-DATA-001** | Data Access and Lake Management | Governs the Clinical Data Lake and Financial Warehouse tables queried for ground-truth data during performance re-evaluation. |
| **SOP-SEC-005** | Identity and Access Management (IAM) | Defines the role-based access controls enforced in MMR and MOP. |
| **SOP-ENG-101** | CI/CD and Production Change Management | Governs the process for executing code hotfixes and rollbacks to model serving containers. |
| **SOP-INC-002** | Enterprise Incident Management | The overarching framework for critical incident (P1/P2) response and post-mortem facilitation. |

### 10.2 External Standards and Frameworks

| Reference ID | Description |
| :--- | :--- |
| **MHD-RMF-FRM-001** | Meridian Health Technologies Board-approved Risk Management Framework. Defines the 5-Point model risk tiering and associated risk appetite. |
| **NIST AI 100-1** | National Institute of Standards and Technology - Artificial Intelligence Risk Management Framework (AI RMF 1.0). Used as a guide for structuring the model risk lifecycle. The `MANAGE` function is conceptualized within our overall governance structure, and stakeholder engagement regarding risk trade-offs is conducted through existing product and committee review channels. |

---

## 11. Revision History

| Version | Date | Author | Approver | Summary of Changes |
| :--- | :--- | :--- | :--- | :--- |
| **1.0** | 2022-01-10 | Dr. Marcus Rivera | David Park | Initial publication of model monitoring procedures. |
| **2.0** | 2022-08-15 | Jane Tran (MLOps Lead) | Dr. Marcus Rivera | Major revision to integrate Meridian Observability Platform (MOP) and replace legacy Prometheus dashboards. Formalised RACI matrix. |
| **2.1** | 2023-01-20 | Dr. Marcus Rivera | David Park | Updated Section 5.4 (Degradation Response) to include the new circuit breaker fallback pattern. Added escalation matrix for P1 incidents. |
| **2.4** | 2023-09-10 | Dr. Aris Singh | David Park | Refined Model Risk Tiers to align with EU MDR application scope. Added Section 6.1.3 (Transparency Reporting). |
| **2.5** | 2024-01-05 | Dr. Marcus Rivera | David Park | Replaced "Shadow Testing Approval Committee" with the streamlined VP of Engineering approval path for rollbacks. Introduced the `TEMP-AIML-006B` Impact Assessment form. |
| **2.6** | 2024-03-04 | Dr. Marcus Rivera | David Park | Annual review. Updated training module list to reflect new incident simulation tabletop (`AIML-TRN-007`). Clarified daily reporting for Tier 1 models. Effective date aligned with new release train. |
| **2.7** | 2025-03-15 | Dr. Marcus Rivera | David Park | Scheduled review completed. Minor language updates to Monitoring, Metrics, and Reporting section for clarity. Next review date set per governance schedule. |