---
sop_id: "SOP-AIML-011"
title: "ML Pipeline Orchestration"
business_unit: "AI/ML Engineering"
version: "1.9"
effective_date: "2024-02-03"
last_reviewed: "2025-07-18"
next_review: "2026-01-05"
owner: "Dr. Marcus Rivera, Chief AI Officer"
approver: "David Park, VP of Engineering"
classification: "Internal"
regulations:
  - "SOC 2"
  - "NIST AI RMF"
status: "Active"
---

# Standard Operating Procedure: ML Pipeline Orchestration

## 1. Purpose and Scope

### 1.1 Purpose
This Standard Operating Procedure (SOP) establishes the standardized framework for designing, deploying, orchestrating, monitoring, and maintaining machine learning (ML) pipelines across Meridian Health Technologies, Inc. The purpose is to ensure that all ML pipelines—from data ingestion through model serving—operate with consistency, reliability, auditability, and compliance with applicable regulatory requirements, particularly SOC 2 and the NIST AI Risk Management Framework (AI RMF).

This SOP defines the orchestration layer that governs Directed Acyclic Graph (DAG) management, dependency resolution, scheduling, retry logic, failure handling, artifact lineage tracking, and operational monitoring for all production ML workloads. By adhering to this document, Meridian ensures that model development, training, evaluation, deployment, and monitoring processes are repeatable, traceable, and defensible during internal and external audits.

### 1.2 Scope
This SOP applies to all ML pipelines operating in production, staging, and pre-production environments that support or feed into the following Meridian business lines:

| Business Line | Pipeline Types Covered | Environment |
|---|---|---|
| Clinical AI Platform | Diagnostic imaging inference, patient risk scoring, adverse event prediction, clinical decision support pipelines | Production, Staging |
| HealthPay Financial Services | Credit scoring, fraud detection, claims automation, medical lending underwriting models | Production |
| MedInsight Analytics | Population health analytics, care gap identification, outcomes prediction | Production |
| Meridian SaaS Platform | All supporting infrastructure pipelines (feature stores, data transformation, monitoring feeds) | Production, Staging |

All pipelines subject to this SOP must be implemented using the standardized Meridian technology stack: Kubeflow Pipelines (primary orchestrator), MLflow (experiment tracking and model registry), and SageMaker (managed training and hosting where applicable). Pipelines operating on the AWS (us-east-1, eu-west-1) and Azure (disaster recovery) environments are in scope.

### 1.3 Applicability
This SOP applies to all AI/ML Engineering personnel, Data Engineers, MLOps Engineers, Site Reliability Engineers (SRE), Clinical AI Product teams, Financial Services Model Development teams, and any contractor or third-party developer creating or modifying ML pipelines at Meridian. Compliance with this SOP is mandatory for all pipeline code merged to the `main` or `production` branches of Meridian's GitLab repositories. Non-compliance may result in pipeline promotion denial, access revocation, or escalation to the Chief AI Officer and VP of Engineering.

---

## 2. Definitions and Acronyms

| Term | Definition |
|---|---|
| **DAG (Directed Acyclic Graph)** | A directed graph with no cycles, representing pipeline components and their execution dependencies. Each node is a discrete pipeline step; edges define data flow and execution order. |
| **Pipeline** | A fully specified DAG with defined inputs, outputs, parameters, and execution environment, registered in the Kubeflow Pipelines system. |
| **Pipeline Run** | A single execution instance of a pipeline, associated with a unique Run ID, timestamp, and execution context. |
| **Artifact** | Any data object produced or consumed by a pipeline step, including datasets, model weights, evaluation reports, and metadata files. All artifacts must be versioned and tracked in MLflow. |
| **Lineage** | The complete, auditable provenance record linking a deployed model to its training data, code version, hyperparameters, and all intermediate artifacts. |
| **Model Registry** | The MLflow Model Registry, which serves as the authoritative repository for all production-deployed models, their versions, stage transitions, and approval records. |
| **Feature Store** | A centralized repository for curated, documented, and versioned features used across ML pipelines, implemented via the Meridian Feature Platform (Snowflake + Redis + Pinecone backend). |
| **Pipeline Template** | A reusable, parameterized pipeline definition stored in the Meridian GitLab Pipeline Catalog (`gitlab.meridian.health/ml-pipelines/catalog`). |
| **Retry Policy** | The defined strategy for automatically re-executing failed pipeline steps, including maximum retries, backoff intervals, and idempotency requirements. |
| **Circuit Breaker** | A pipeline-level safeguard that halts all execution if a specified threshold of failures is exceeded within a defined window, preventing cascading downstream impacts. |
| **SOC 2** | Service Organization Control 2, specifically the Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy) relevant to Meridian's SaaS Platform. |
| **NIST AI RMF** | National Institute of Standards and Technology Artificial Intelligence Risk Management Framework (AI RMF 1.0, January 2023), voluntarily adopted by Meridian for AI governance. |
| **PHI** | Protected Health Information as defined under HIPAA. |
| **PII** | Personally Identifiable Information as defined under GDPR and applicable state laws. |
| **CI/CD** | Continuous Integration / Continuous Delivery pipeline for ML code and configuration, governed by SOP-DEV-008. |
| **SLA** | Service Level Agreement. |
| **SLO** | Service Level Objective. |
| **SLI** | Service Level Indicator. |
| **Run ID** | A universally unique identifier (UUID v4) assigned to every pipeline run for traceability. |
| **Stage Transition** | The process of moving a registered model version from one stage (e.g., `Staging`) to another (e.g., `Production`), requiring documented approvals as per this SOP. |

---

## 3. Roles and Responsibilities

### 3.1 RACI Matrix

| Activity | ML Engineer (Developer) | MLOps Engineer | Data Engineer | SRE | Clinical AI Lead / FinServ Model Risk Manager | CAIO (Owner) | VP Engineering (Approver) |
|---|---|---|---|---|---|---|---|
| Pipeline Design and Development | R | C | A | I | C | I | I |
| Pipeline Template Approval | I | R | I | I | A | C | I |
| Production Pipeline Deployment | C | R | I | A | I | I | I |
| Feature Store Population | C | I | R | I | I | I | I |
| Pipeline Monitoring & Alerting | I | R | I | A | I | I | I |
| Failure Handling (Tier 1-2) | I | R | I | A | I | I | I |
| Failure Handling (Tier 3-4) | R | C | R | A | I | C | I |
| Model Registry Stage Transition | C | R | I | C | A | I | I |
| Exception Approval | I | I | I | I | R | A | C |
| Audit Response | I | R | I | C | C | A | I |
| Policy Review and Updates | C | R | C | C | C | A | A |

**Legend**: R = Responsible (executes), A = Accountable (approves), C = Consulted (input required), I = Informed (notification only)

### 3.2 Named Role Definitions

| Role | Individual / Team | Scope of Authority |
|---|---|---|
| **Chief AI Officer (CAIO)** | Dr. Marcus Rivera | Final authority on all AI/ML governance, exception approvals, and SOP sign-off |
| **VP of Engineering** | David Park | Approver for all pipeline infrastructure changes, CI/CD tooling, and platform-level decisions |
| **MLOps Engineering Lead** | [Designated by VP Engineering] | Owns the Kubeflow/MLflow infrastructure, pipeline catalog, and production deployment gates |
| **Clinical AI Lead** | [Designated by CAIO] | Accountable for Clinical AI Pipeline stage transitions and Clinical AI model risk reviews |
| **FinServ Model Risk Manager** | [Designated by CRO, dotted line to CAIO] | Accountable for HealthPay Financial Services model stage transitions and credit model risk reviews |
| **SRE Lead** | [Designated by VP Engineering] | Accountable for pipeline availability SLOs and incident response |
| **Data Engineering Lead** | [Designated by VP Engineering] | Accountable for feature store integrity and data pipeline integration |
| **ML Engineer** | Individual contributor, AI/ML Engineering | Responsible for pipeline code development and unit testing |

---

## 4. Policy Statements

### 4.1 Pipeline Design Standards
All ML pipelines shall be defined as Directed Acyclic Graphs (DAGs) using Kubeflow Pipelines SDK v2.x. Pipelines must be fully parameterized to enforce separation of configuration from code. Pipeline code must be stored in GitLab repositories with branch protection enabled; direct pushes to `main` are prohibited. All pipelines must declare typed inputs and outputs for every component.

### 4.2 Idempotency Requirement
Every pipeline component must be designed for idempotent execution. Re-running a component with identical inputs and parameters must produce identical outputs without causing data duplication, state corruption, or unintended side effects. This is a non-negotiable SOC 2 Availability criterion compliance requirement.

### 4.3 Artifact Versioning and Lineage
Every pipeline run must generate a complete, immutable artifact lineage record in MLflow Tracking. This record shall link the Run ID to: code commit hash, training dataset version hash, hyperparameter set, evaluation metrics, and output model artifacts. Lineage must be demonstrable upon auditor request within two (2) business hours.

### 4.4 Model Registry Governance
No model shall be promoted to the `Production` stage in the MLflow Model Registry without documented approval from the relevant accountable role (Clinical AI Lead or FinServ Model Risk Manager). All stage transitions must be logged immutably and be available for NIST AI RMF MAP (Measure 2.3) reviews.

### 4.5 Scheduled and Event-Driven Execution
Pipelines may be triggered via cron schedules (defined in GitLab CI/CD variables, never hardcoded), event-driven hooks (S3 bucket events, Pub/Sub messages), or manual approval. Scheduled pipelines must include a jitter window of ±5 minutes to prevent resource contention spikes.

### 4.6 SOC 2 Trust Services Criteria Alignment
All pipelines supporting the Meridian SaaS Platform must align with the following SOC 2 Trust Services Criteria:
- **CC6.1 (Logical and Physical Access Controls):** Pipeline deployment credentials must be managed via HashiCorp Vault, never stored in pipeline code or GitLab variables.
- **CC7.2 (System Operations):** Pipeline execution status must be monitored, with critical failures triggering PagerDuty alerts within five (5) seconds.
- **CC7.5 (Disposal):** Pipeline-generated artifacts containing PHI/PII must be automatically purged from temporary storage within 24 hours of pipeline completion or upon pipeline failure termination.
- **CC8.1 (Change Management):** All pipeline template changes must follow the change management process defined in SOP-CM-003.

### 4.7 NIST AI RMF Alignment
In alignment with the voluntarily-adopted NIST AI RMF 1.0, Meridian mandates:
- **GOVERN 1.2 (Organizational Risk Culture):** Pipeline failure modes must be documented in a Risk Card attached to each pipeline template.
- **MAP 2.3 (Model Impact):** Pipeline components that load or serve models must tag runs with the model purpose classification (`clinical_decision_support`, `financial_underwriting`, `population_analytics`, `infrastructure`).
- **MEASURE 2.6 (Model Performance):** Production inference pipelines must include continuous monitoring components for drift detection; pipeline runs serving stale models (beyond the defined drift threshold of 0.15 PSI) shall be automatically halted.

---

## 5. Detailed Procedures

### 5.1 Pipeline Design and DAG Construction

#### 5.1.1 Pipeline Template Creation
All new production pipelines must originate from a Meridian-approved pipeline template. Templates are stored in the GitLab Pipeline Catalog at `gitlab.meridian.health/ml-pipelines/catalog`.

**Steps:**
1. **Template Selection:** Navigate to the Pipeline Catalog and select the closest matching template (e.g., `template-training-image-classifier`, `template-inference-real-time`, `template-etl-feature-engineering`). If no suitable template exists, proceed to Step 2.
2. **New Template Creation:**
   a. Create a feature branch from `main` in the catalog repository.
   b. Author the pipeline DAG using the Kubeflow Pipelines SDK v2.x `@dsl.pipeline` decorator. The pipeline must declare all parameters with type annotations and default values in a `config.yaml` companion file.
   c. Each component function must be decorated with `@dsl.component` and specify `base_image` (from Meridian ECR: `012345678901.dkr.ecr.us-east-1.amazonaws.com/ml-ops/...`), `packages_to_install`, and resource requests (CPU, memory) as annotations.
   d. Include a `@dsl.component` step for data validation using Great Expectations; this step must run before any training or inference component that consumes external data.
      ```yaml
      # Example config.yaml snippet
      pipeline_name: "clinical_risk_scorer_training"
      components:
        - name: "validate_input_data"
          image: "012345678901.dkr.ecr.us-east-1.amazonaws.com/ml-ops/great-expectations:v2.0"
          resource_request:
            cpu: "4"
            memory: "16Gi"
        - name: "train_model"
          image: "012345678901.dkr.ecr.us-east-1.amazonaws.com/ml-ops/xgboost-training:v1.5"
          resource_request:
            cpu: "16"
            memory: "64Gi"
            gpu: "1"
      ```
   e. Commit the code with a descriptive commit message. Open a Merge Request (MR) assigned to the MLOps Engineering Lead for review. Include a Risk Card (template: `risk-card-template.md`) in the MR description.
3. **Review and Approval:** The MLOps Engineering Lead reviews for adherence to this SOP (SOP-AIML-011), security best practices, resource efficiency, and Risk Card completeness. Approval of the MR constitutes template approval.
4. **Registration:** Upon merge to `main`, a GitLab CI/CD pipeline (SOP-DEV-008) automatically registers the pipeline template in the Kubeflow Pipelines Central Dashboard with a unique template ID.

#### 5.1.2 DAG Dependency Management
All inter-component dependencies must be expressed explicitly through Kubeflow's `component_a.output().after(component_b...)` or via `dsl.PipelineTask` references. Implicit dependencies or shared state via file system paths are prohibited. Where multiple downstream components consume the same upstream output, the upstream component must produce an output artifact that downstream components reference by path in MLflow.

**Metric Requirement:** Every DAG must complete a static analysis scan (via `kfp-v2-inspector`) that checks for cycles, unreachable nodes, and missing output definitions. The MR pipeline will run this automatically; a failed scan blocks MR approval.

### 5.2 Pipeline Scheduling

#### 5.2.1 Creating a Recurring Schedule
Meridian uses Kubeflow Pipelines' Recurring Run functionality for all time-based scheduling.

**Steps:**
1. From the Kubeflow Central Dashboard, navigate to the registered pipeline template.
2. Click "Create Recurring Run."
3. Configure:
   | Parameter | Requirement |
   |---|---|
   | Run Name | Must follow naming convention: `<business_unit>-<model_name>-<environment>-recurring`, e.g., `clinical-risk-v3-prod-recurring` |
   | Schedule (Cron) | Defined in UTC. Must use `@daily`, `@weekly`, or a five-field cron string (`0 3 * * 1` for Monday 3AM UTC). |
   | Jitter | ±5 minutes; enabled by default. |
   | Catch-up | `False` for all production pipelines (prevents batch execution of missed windows). |
   | Parameters | All runtime parameters pre-populated with validated values from the `config.yaml` companion file. |
4. Before saving, the scheduler performs a dry-run of the pipeline with the supplied parameters. A successful dry-run is mandatory. Dry-run failures must be resolved before the schedule is activated.
5. Upon saving, the Recurring Run is created with status `Enabled`. An audit event is logged to the Meridian Audit Service (see Section 6).

#### 5.2.2 Event-Driven Triggers
For pipelines triggered by S3 bucket events:

1. Configure the S3 bucket event notification to publish to an AWS SQS queue (`ml-pipeline-triggers-queue-{env}`).
2. An AWS Lambda function (`ml-pipeline-event-handler`) reads the queue, validates the event payload against a schema, and calls the Kubeflow Pipelines API to create a new Run.
3. The Lambda function must implement idempotent deduplication using the S3 event's `objectCreated` `eTag` as the dedup key with a 30-minute TTL in DynamoDB.
4. Event-triggered runs follow the same execution and failure handling policies as scheduled runs.

### 5.3 Pipeline Execution and Monitoring

#### 5.3.1 Run-Level Observability
Every pipeline run automatically emits:
- **Run metadata:** Run ID, pipeline template ID, trigger source (schedule/event/manual), user (for manual), timestamp.
- **Component-level spans:** Each component execution is traced as an OpenTelemetry span, exported to Meridian's Honeycomb instance. Span attributes: component name, image SHA, resource utilization, execution duration, exit status.
- **Artifact metadata:** All MLflow-tracked artifacts are annotated with the Run ID.

**Monitoring Dashboard Configuration:**
MLOps Engineers and SREs must configure the following dashboards in Grafana (per pipeline family):
- **Pipeline Execution Overview:** Run success rate, average DAG duration, component-level durations (p50, p95, p99).
- **Failure Dashboard:** Component-level failure counts, categorized by error class (data validation, resource exhaustion, code exception, dependency timeout).
- **Resource Utilization:** CPU, memory, and GPU utilization per component, plotted against requested resources.

### 5.4 Failure Handling and Retry Logic

#### 5.4.1 Retry Policy Configuration
Every pipeline component susceptible to transient failures must be configured with a retry policy in the `config.yaml`:

```yaml
retry_policy:
  max_retries: 3
  backoff_strategy: "exponential"  # or "fixed"
  initial_delay_seconds: 30
  max_delay_seconds: 300
  retry_on_error_class:
    - "NetworkTimeout"
    - "ResourceTemporarilyUnavailable"
    - "DatabaseConnectionLost"
```

Retries are automated by the Kubeflow orchestrator. Each retry attempt increments a `retry_attempt` counter tracked in the span metadata. If a component exhausts all retries, it exits with status `Failed`, and the orchestrator marks the component as `Failed` in the DAG.

#### 5.4.2 Circuit Breaker
A pipeline-level circuit breaker protects against cascading failures. The breaker trips under the following condition:
- **Trip Condition:** ≥3 distinct component types within the same pipeline DAG fail with non-transient errors (error classes not in `retry_on_error_class`) within a single 10-minute rolling window.
- **Trip Action:** All running components are gracefully terminated (SIGTERM, with a 30-second grace period before SIGKILL). The pipeline run is marked `Aborted` with a status message `"CircuitBreakerTripped: cascading failure protection activated"`.
- **Recovery:** The circuit breaker auto-resets after 15 minutes. The next scheduled or triggered run proceeds normally. Manual intervention (SEV2 incident) is required to investigate the root cause.

#### 5.4.3 Failure Escalation
| Failure Type | Example | Escalation Path | Response Time |
|---|---|---|---|
| **Transient Retry Exhausted** | All 3 retries consumed; step marked `Failed` | P3 incident auto-created in PagerDuty; assigned to MLOps on-call | Initial response: 30 minutes |
| **Data Validation Failure** | Great Expectations validation step returns critical failure | P3 incident; Data Engineering Lead notified via Slack `#data-quality-alerts` | Acknowledge: 15 minutes; Root cause analysis: 24 hours |
| **Circuit Breaker Tripped** | 3+ non-transient components failed | SEV2 incident; SRE Lead and MLOps Lead paged | Initial response: 15 minutes |
| **Model Drift Threshold Exceeded** | PSI > 0.15 detected in Monitoring component; pipeline halted | P2 incident; Clinical AI Lead or FinServ Model Risk Manager paged | Containment: 30 minutes; Model Rollback: 1 hour |
| **Critical Infrastructure Failure** | Kubeflow API unavailability, MLflow server outage | SEV1 incident; SRE Lead, MLOps Lead, and VP Engineering paged per SOP-INC-001 | Response: immediate, per SOP-INC-001 SLOs |

---

## 6. Controls and Safeguards

### 6.1 Technical Controls

| Control ID | Control Description | Implementation | SOC 2 Criteria Mapping | NIST AI RMF Mapping |
|---|---|---|---|---|
| **AIML-011-C01** | Pipeline code integrity: All pipeline code changes must be code-reviewed and pass CI/CD checks (SAST scan via SonarQube, container image vulnerability scan via Trivy) before merge. Enforced by GitLab MR required pipelines. | Mandatory MR pipeline; SAST with critical/high block; Trivy with `CRITICAL` severity block | CC8.1 (Changes to Infrastructure, Data, and Software) | GOVERN 1.2 |
| **AIML-011-C02** | Credential isolation: Pipeline components authenticate to data sources and model registries exclusively via short-lived tokens provisioned by HashiCorp Vault. No static credentials in code, config files, or environment variables. | Vault Agent sidecar injector; token max TTL: 1 hour; rotation automatic. | CC6.1 (Logical Access Controls) | GOVERN 1.4 |
| **AIML-011-C03** | Pipeline run immutability: Once a pipeline run is `Completed`, `Failed`, or `Terminated`, its recorded Run ID, parameters, artifact paths, and logs are immutable. Kubeflow's underlying database (MySQL RDS) has audit logging enabled with `audit.log` configuration; DELETE and UPDATE queries on run metadata tables are prohibited by IAM policy for non-admin roles. Admin modifications require a break-glass procedure logged to AWS CloudTrail. | RDS parameter group `audit.log=ON`; CloudTrail enabled; admin access granted only via PagerDuty incident bridge. | CC7.2 (System Operations: Incident Detection) | MAP 2.3 (Artifact tracking immutability) |
| **AIML-011-C04** | PHI/PII artifact lifecycle: Temporary storage volumes (Kubernetes ephemeral volumes, `/tmp` directories) used by pipeline components handling PHI/PII must be encrypted at rest and automatically wiped upon component completion. A post-execution hook (`cleanup-ph-data`) verifies artifact wipe; failure triggers a P2 incident. | Kubeflow exit handler component; verification via `data-sanitizer` script executed as final DAG step. | CC6.5 (Disposal of Confidential Information) | MAP 2.1 |
| **AIML-011-C05** | Model Registry access control: Write access (`transition_to_stage`) is restricted to MLOps Engineers; approval for `Production` stage transition must come from Clinical AI Lead or FinServ Model Risk Manager. This is enforced via MLflow's permission system backed by Meridian SSO. | MLflow Registry permissions: `READ`: All AI/ML Engineering; `WRITE`: MLOps group; `MANAGE`: CAIO, VP Engineering. Stage transition approval via MLflow's `transition_model_version_stage` API with documented approval comment. | CC6.1, CC6.6 (Logical Access Over Protected Information) | GOVERN 1.5 (Accountability) |
| **AIML-011-C06** | Network segmentation: Pipeline components execute within the `ml-pipeline-{env}` Kubernetes namespace, which has network policies restricting egress to only approved Meridian services (MLflow, Feature Store, Vault, CloudWatch Logs). Ingress is denied by default. | Kubernetes NetworkPolicy resources; enforced by Calico CNI. | CC6.6 | GOVERN 1.1 |

### 6.2 Administrative Controls

| Control ID | Control Description | Evidence | Audit Artifact |
|---|---|---|---|
| **AIML-011-C07** | Annual pipeline governance review: Every production pipeline template must undergo an annual review by the CAIO or delegate. Review includes Risk Card update, drift threshold validation, and resource utilization assessment. | Meeting minutes in Confluence (`ML Pipeline Annual Review` space); updated Risk Card with review date stamp. | Risk Card vN; Review Sign-off |
| **AIML-011-C08** | Change management gate: Any modification to a pipeline template rated `Critical` (Business Impact Level 1: Clinical AI patient-facing, FinServ credit decision) requires a Change Request (CR) per SOP-CM-003, approved by the CAIO. | GitLab MR linked to a Jira CR ticket; approval comment from CAIO. | Jira CR ticket; MR approval log |
| **AIML-011-C09** | Segregation of duties: The individual authoring a pipeline template cannot approve the MR for that template. The individual deploying a pipeline to Production cannot be the same as the approver for the Model Registry stage transition. | GitLab MR records (author vs. approver); MLflow Registry audit log (deployer vs. transition approver). | MR data; MLflow audit log export |

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs)

| KPI ID | Metric | Target | Measurement Window | Reporting Dashboard |
|---|---|---|---|---|
| **KPI-011-01** | Pipeline Run Success Rate | ≥99.5% (rolling 30-day) | 30 days | Grafana `Pipeline Health Overview` |
| **KPI-011-02** | Mean Time to Detect (MTTD) Pipeline Failure | ≤5 seconds from component failure to PagerDuty alert | Per incident | PagerDuty + Datadog APM |
| **KPI-011-03** | Mean Time to Recovery (MTTR) for Pipeline Failures | ≤45 minutes for P3; ≤30 minutes for P2; ≤15 minutes for SEV1 | Per incident | PagerDuty incident lifecycle report |
| **KPI-011-04** | Stale Model Detection Rate | 100% of production inference pipelines running the `drift-monitor` component with active drift checks | Rolling 7-day | Grafana `Model Freshness Dashboard` |
| **KPI-011-05** | Artifact Lineage Completeness | 100% of Pipeline Runs have linked MLflow Run with full lineage (code commit, data hash, params, metrics, artifacts) | Rolling 7-day | MLflow Tracking + custom lineage validator |
| **KPI-011-06** | Circuit Breaker Activation Rate | ≤1 activation per pipeline family per month | Monthly | Grafana `Circuit Breaker Events` |

### 7.2 Reporting Cadence

| Report | Audience | Frequency | Owner |
|---|---|---|---|
| Pipeline Health Executive Summary | CAIO, VP Engineering, SRE Lead | Monthly (first Monday) | MLOps Engineering Lead |
| SOC 2 Control Evidence Package | Internal Audit, Compliance Officer | Quarterly | MLOps Engineering Lead + Security Lead |
| NIST AI RMF MAP Function Review | Clinical AI Lead, FinServ Model Risk Manager, CAIO | Quarterly | CAIO (coordination) |
| Pipeline Cost and Utilization Report | VP Engineering, Finance | Monthly | SRE Lead (FinOps) |
| Incident Postmortem Report (for any SEV1/SEV2) | CAIO, VP Engineering, all AI/ML Engineering | Within 5 business days of incident resolution | Incident Commander (SRE or MLOps Lead) |

### 7.3 Real-Time Dashboards
Accessible via Grafana:
1. **Pipeline Health Overview:** Run success rate, per-pipeline latency, retry counts, circuit breaker status.
2. **Model Freshness Dashboard:** Drift scores per deployed model, last training run timestamp, PSI trend graphs.
3. **Resource Utilization FinOps:** CPU/GPU/memory usage vs. requested, cost attribution per pipeline.
4. **Audit Log Viewer:** Immutable event log showing pipeline deployments, stage transitions, and exception approvals.

---

## 8. Exception Handling and Escalation

### 8.1 Exception Types

| Exception Category | Definition | Examples | Approval Authority |
|---|---|---|---|
| **Technical Exception** | Temporary deviation from a technical control due to a documented system limitation or emergency | Bypassing SAST scan for a critical hotfix that patches a zero-day vulnerability; using a static credential via Vault emergency break-glass | VP Engineering |
| **Process Exception** | Deviation from a prescribed procedural step | Conducting a Model Registry stage transition without the usual two-approver quorum during an after-hours incident (allowing single approver) | CAIO |
| **Scheduling Exception** | Modifying a Production pipeline's schedule outside the standard CR process | Pausing a scheduled pipeline for 24 hours to perform database maintenance | MLOps Engineering Lead |
| **Model Rollback Exception** | Rapid rollback of a production model bypassing standard staging validation due to a critical drift event | Rolling back to `v-1` immediately when `v-current` has PSI=0.35 and causing clinical alert fatigue | Clinical AI Lead or FinServ Model Risk Manager |

### 8.2 Exception Request Procedure
1. **Incident Declaration:** If the exception is in response to an active incident, declare the incident in PagerDuty per SOP-INC-001.
2. **Create Exception Ticket:** In Jira, create a ticket of type `ML Pipeline Exception`, linked to the pipeline template and, if applicable, the incident. Use the `exception-request` template.
3. **Document:**
   a. The control or procedure being deviated from (cite SOP section or Control ID).
   b. The business justification and impact of NOT granting the exception.
   c. The duration of the exception (max: 72 hours; renewable once with CAIO approval).
   d. Compensating controls in place during the exception period.
4. **Approval Route:** Jira routes to the appropriate approver based on the Exception Category. In incident scenarios, approval must occur within the MTTR target; approvers are expected to respond via their on-call channel or the incident bridge.
5. **Post-Exception:** Within 5 business days of exception expiry, the exception must be formally closed, compensating controls removed, and a post-exception review comment added to the Jira ticket.

### 8.3 Escalation Path for Unresolved Pipeline Failures
If a pipeline failure has not been acknowledged within the Response Time SLA defined in Section 5.4.3:
1. **On-call escalation** to Senior MLOps Engineer (15 minutes overdue).
2. **MLOps Engineering Lead** notification (30 minutes overdue).
3. **VP Engineering** notification (60 minutes overdue).
4. **CAIO** notification (90 minutes overdue).

---

## 9. Training Requirements

### 9.1 Required Training Modules

| Module ID | Title | Audience | Frequency | Delivery Method |
|---|---|---|---|---|
| **TR-AIML-011-01** | ML Pipeline Orchestration Fundamentals | All AI/ML Engineering, MLOps, SRE | Onboarding; then annually | Meridian LMS (Workday); includes hands-on lab with sandbox Kubeflow environment |
| **TR-AIML-011-02** | SOC 2 Compliance for ML Engineers | All AI/ML Engineering, MLOps, SRE | Annually | Online module; includes quiz (passing score: 90%). Covers CC6.1, CC7.2, CC7.5, CC8.1 as applicable to pipelines. |
| **TR-AIML-011-03** | NIST AI RMF for Pipeline Developers | All AI/ML Engineering (Clinical + FinServ focus), Clinical AI Lead, FinServ Model Risk Manager | Annually; updated when NIST releases minor updates | Instructor-led workshop (2 hours); covers MAP 2.3, MEASURE 2.6 risk mapping, Risk Card authoring. |
| **TR-AIML-011-04** | Pipeline Failure Handling and Escalation Drill | MLOps, SRE | Quarterly | Simulated failure scenario in staging environment; assessed on MTTD and MTTR against KPIs. |

### 9.2 Training Tracking and Compliance
- All training assignments are managed through Meridian's Workday Learning system.
- Completion is tracked; non-compliance beyond a 30-day grace period results in temporary suspension of pipeline deployment privileges (access revoked from GitLab and Kubeflow) until training is completed.
- The CAIO reviews training compliance quarterly as part of the governance review.

---

## 10. Related Policies and References

### 10.1 Internal Meridian SOPs

| SOP ID | Title | Relationship |
|---|---|---|
| SOP-DEV-008 | CI/CD for ML Applications and Infrastructure | Governs the GitLab CI/CD pipelines that build, test, and register pipeline templates referenced in SOP-AIML-011. |
| SOP-INF-003 | Kubernetes Cluster Operations | Defines the K8s cluster configuration and namespace management that hosts Kubeflow pipelines. |
| SOP-DATA-015 | Feature Store Management | Governs the Feature Store integration consumed by pipelines. |
| SOP-SEC-007 | Secrets Management with HashiCorp Vault | Defines Vault policy and secret lifecycle referenced in Control AIML-011-C02. |
| SOP-CM-003 | Change Management for Production Systems | Defines the CR process for Critical pipeline template changes (Control AIML-011-C08). |
| SOP-INC-001 | Incident Management and Response | Governs incident declaration, severity levels, and response SLAs referenced in incident escalation paths. |
| SOP-AIML-004 | Model Registry and Versioning | Complementary policy; defines Model Registry stage lifecycle that pipelines feed into. |
| SOP-AIML-009 | Model Drift Monitoring and Response | Governs drift thresholds and auto-halt logic consumed by pipeline monitoring components. |
| SOP-COMP-020 | PHI/PII Data Lifecycle | Governs data disposal mandates referenced in Control AIML-011-C04. |

### 10.2 External Standards and Regulations

| Reference | Version/Date | Applicable Sections |
|---|---|---|
| SOC 2 Trust Services Criteria (AICPA) | 2017 (revised 2022) | CC6.1, CC6.5, CC6.6, CC7.2, CC7.5, CC8.1 |
| NIST AI RMF 1.0 | January 26, 2023 | GOVERN 1.1, 1.2, 1.4, 1.5; MAP 2.1, 2.3; MEASURE 2.6 |
| HIPAA Security Rule | 45 CFR Part 160 and Part 164 | Technical safeguards for PHI handling |
| EU MDR 2017/745 | Annex I, Section 17 (Software as Medical Device) | For Clinical AI pipelines producing CE-marked model outputs |
| Meridian Internal Control Framework (MICF) | Version 4.2 | Control objectives referenced in Section 6 |

---

## 11. Revision History

| Version | Date | Author | Approver | Summary of Changes |
|---|---|---|---|---|
| 1.0 | 2022-06-15 | Dr. Marcus Rivera | David Park | Initial creation. Established baseline pipeline orchestration standards for Kubeflow 1.x era. |
| 1.1 | 2022-09-22 | MLOps Engineering Lead | Dr. Marcus Rivera | Added SOC 2 CC6.1 and CC7.2 control mappings. Introduced Risk Card requirement. |
| 1.2 | 2022-11-10 | SRE Lead | David Park | Incorporated Circuit Breaker pattern (post-incident #INC-2022-089 lesson learned). Defined retry policy schema. |
| 1.3 | 2023-02-01 | Director of AI Governance | Dr. Marcus Rivera | Major revision: Adopted NIST AI RMF 1.0 voluntary alignment. Mapped GOVERN and MAP functions. Added Section 7 KPIs. Reorganized Section 5 for clarity. |
| 1.4 | 2023-04-18 | MLOps Engineering Lead | David Park | Migration from Kubeflow Pipelines v1 to v2. Updated component decorator syntax. Added static analysis scan (AIML-011-C01 enhancement). |
| 1.5 | 2023-06-07 | Clinical AI Lead | Dr. Marcus Rivera | Refined Model Registry stage transition approval for Clinical AI products. Added drift threshold auto-halt per SOP-AIML-009. |
| 1.6 | 2023-08-29 | FinServ Model Risk Manager | Dr. Marcus Rivera | Extended scope to HealthPay Financial Services pipelines. Added FinServ Model Risk Manager as accountable role. Added `financial_underwriting` purpose classification tag. |
| 1.7 | 2023-11-15 | MLOps Engineering Lead, SRE Lead | David Park | Added jitter window requirement (post-mortem #PM-2023-042 for resource contention). Updated SLAs for incident response. Added Honeycomb tracing integration details. |
| 1.8 | 2024-01-10 | Director of AI Governance | Dr. Marcus Rivera | Updated NIST AI RMF references to incorporate additional MEASURE 2.6 guidance following industry benchmarking. Refined Retry Policy schema with error class categorization. Added Event-Driven Trigger Lambda dedup logic. |
| 1.9 | 2025-07-18 | Dr. Marcus Rivera | David Park | Comprehensive annual review. Re-validated all controls against SOC 2 criteria for upcoming audit preparation. Updated all role assignments to reflect current org chart. Added Post-Exception Review requirement to Section 8. Updated Kubernetes namespace policy to reflect current network segmentation rules. Confirmed alignment with latest MLflow 2.x Registry permission model. Updated Approved External Standards version references. Scheduled next review: January 2026. |

---

## Appendix A: Pipeline Risk Card Template

```markdown
---
risk_card_id: "RC-{SOP-AIML-011}-{PipelineName}-v{Version}"
date: "YYYY-MM-DD"
author: "[Name, Role]"
reviewer: "[Name, Role]"
---

# Pipeline Risk Card: {PipelineName}

## 1. Model Purpose Classification
- [ ] clinical_decision_support
- [ ] financial_underwriting
- [ ] population_analytics
- [ ] infrastructure

## 2. Data Sensitivity
- Does the pipeline consume or produce PHI/PII? Yes / No
- If yes, list all components handling PHI/PII:

## 3. Known Failure Modes
| Failure Mode | Likelihood (1-5) | Impact (1-5) | Mitigation | Residual Risk |
|---|---|---|---|---|
| | | | | |

## 4. Dependencies
- Upstream data sources:
- Feature Store views:
- Model Registry dependencies:

## 5. Retry and Circuit Breaker Configuration
- max_retries:
- backoff_strategy:
- circuit_breaker_trip_threshold:

## 6. Drift Thresholds
- PSI threshold:
- Stale model max age:
```

---

## Appendix B: Common Issue Log / Lessons Learned

| Date | Issue ID | Description | Root Cause | Lesson Learned / Prevention | Status |
|---|---|---|---|---|---|
| 2022-08-15 | LL-011-001 | Production pipeline deployed without code review; introduced data leak due to misconfigured train/test split. | Emergency hotfix bypassed MR checks. | **Never bypass MR for prod pipelines.** Implemented break-glass procedure with mandatory post-hoc review within 24 hours. | Closed; addressed in v1.2 |
| 2022-12-01 | LL-011-002 | Circuit breaker not triggering; cascading failure took down 3 pipelines, impacting Clinical dashboard refresh. | Trip condition threshold was 5; was not tuned for the environment scale. | **Review trip thresholds quarterly.** Set default trip=3 for all prod pipelines. Added SEV2 escalation for circuit breaker events. | Closed; addressed in v1.3 |
| 2023-05-20 | LL-011-003 | Artifact lineage gap: Model deployed without traceable code commit hash because ML engineer tagged commit manually instead of relying on CI/CD variable. | Human error; manual tag override possible. | **Disallow manual tag override via GitLab CI/CD variable injection only.** Enforce lineage completeness check (KPI-011-05) in pre-production gate. | Closed; addressed in v1.4 CI/CD pipeline changes |
| 2023-09-10 | LL-011-004 | FinServ pipeline consumed stale credit bureau features; 6-hour delay in model retraining detected only via manual check. | Drift monitor component not included in pipeline template for FinServ. | **Mandatory: All inference pipelines MUST include a drift-monitor component.** Audit all templates for component completeness annually. | Closed; drift-monitor component added to FinServ template in v1.6 |
| 2024-01-25 | LL-011-005 | OOMKilled errors on training pipeline due to hardcoded memory request mismatch with actual data volume growth. | Resource requests not parameterized; hardcoded in component code. | **Resource requests must be externalized in config.yaml and reviewed quarterly.** Implemented resource utilization FinOps dashboard. | Closed; addressed in v1.8 with parameterized resource config |

---

**End of Document**

*This document is governed by the Meridian Health Technologies Document Control Policy (SOP-QMS-001). Uncontrolled when printed. Verify current version in the Meridian Policy Portal.*