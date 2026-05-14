---
sop_id: "SOP-AIML-018"
title: "Model Serving and Inference Infrastructure"
business_unit: "AI/ML Engineering"
version: "3.2"
effective_date: "2025-05-18"
last_reviewed: "2026-08-09"
next_review: "2027-02-25"
owner: "Dr. Marcus Rivera, Chief AI Officer"
approver: "David Park, VP of Engineering"
classification: "Internal"
regulations:
  - "SOC 2"
  - "EU AI Act"
status: "Active"
---

# Standard Operating Procedure: Model Serving and Inference Infrastructure

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the standardized requirements, operational controls, and governance framework for the deployment, serving, scaling, and lifecycle management of all machine learning (ML) and artificial intelligence (AI) models across the Meridian Health Technologies, Inc. production serving infrastructure. The purpose of this document is to ensure that all models—regardless of business line origin—are served in a secure, reliable, observable, and performant manner commensurate with their risk classification and business criticality.

This SOP defines the architectural standards, deployment pipelines, monitoring expectations, and incident response procedures necessary to maintain the integrity and availability of inference services that directly support clinical decision-making, financial transactions, and population health analytics.

### 1.2 Scope

This SOP applies to:

- All production and pre-production (staging, shadow, canary) model serving environments across all Meridian cloud tenants (AWS us-east-1, AWS eu-west-1, Azure DR).
- All business lines: Clinical AI Platform, HealthPay Financial Services, MedInsight Analytics, and the Meridian SaaS Platform.
- All model artifacts—including PyTorch, TensorFlow, ONNX, and containerized custom inference code—deployed via Kubeflow pipelines or SageMaker endpoints.
- All inference API endpoints exposed to internal services, customer-facing applications, and third-party integrators.
- Batch inference jobs processing PHI/PII on the Snowflake and Spark-based analytics clusters.
- Real-time synchronous inference (p99 latency ≤ 500ms target) and asynchronous inference (batch, streaming) workloads.
- Shadow deployments, A/B test routing, canary rollouts, and rollback procedures.
- All personnel—full-time employees, contractors, and vendors—involved in model deployment, infrastructure provisioning, performance tuning, or incident response for AI/ML systems.

### 1.3 Out of Scope

- Model training and experimentation workflows (see SOP-AIML-012: Model Development Lifecycle).
- Data pipeline ingestion and feature engineering operations (see SOP-DATA-005: Feature Store and Training Data Management).
- Clinical validation studies for model efficacy (see SOP-CLIN-022: Clinical AI Validation Protocol).
- End-user application logic consuming inference results (covered by product-specific engineering standards).

### 1.4 Target Audience

The primary audiences for this SOP are:

| Role | Relevance |
|------|-----------|
| ML Engineers (MLE) | Primary operators; responsible for containerization, deployment, and performance tuning |
| Platform Engineers | Infrastructure provisioning, cluster scaling, networking |
| DevOps/SRE Teams | Monitoring, alerting, incident response for inference services |
| Security Engineering | Model artifact signing, vulnerability scanning, access control |
| QA/Validation Engineers | Pre-production inference validation, load testing, regression testing |
| Product Managers | Understanding SLA commitments and deployment timelines |
| Compliance & Audit | Evidence collection for SOC 2 and HITRUST controls |

---

## 2. Definitions and Acronyms

### 2.1 Definitions

| Term | Definition |
|------|------------|
| **Model Serving** | The operational process of making a trained ML model available to receive inference requests and return predictions via a network-accessible endpoint. |
| **Inference** | The computational process of applying a trained model to input data to produce a prediction, classification, or recommendation output. |
| **Model Artifact** | The serialized file(s) representing a trained model (e.g., .pt, .pb, .onnx, .mar files), including associated tokenizers, preprocessing logic, and metadata. |
| **Inference Container** | A Docker/OCI-compliant container image encapsulating the model artifact, runtime dependencies, and serving logic (e.g., TorchServe, Triton Inference Server, custom Flask/FastAPI application). |
| **Shadow Deployment** | A deployment mode where a new model version receives live production traffic in parallel with the active model, but its outputs are logged for analysis rather than returned to the caller. |
| **Canary Deployment** | A deployment strategy where a percentage of production traffic is routed to a new model version, with gradual traffic shifting based on health metrics. |
| **A/B Routing** | Traffic splitting between two or more model versions based on predefined rules (headers, tenant IDs, random sampling) to compare performance characteristics. |
| **Cold Start** | The latency penalty incurred when a model container or endpoint is initialized from a dormant state, including container startup, model loading into memory, and first-inference warmup. |
| **Model Registry** | The centralized repository (MLflow Model Registry) storing versioned model artifacts, stage transitions, and deployment metadata. |
| **Inference SLA** | Service Level Agreement defining availability percentage and latency targets for production inference endpoints. |
| **Traffic Manager** | The infrastructure component (AWS Application Load Balancer with weighted target groups, or Istio VirtualService) responsible for routing inference requests to backend endpoints. |
| **Graceful Degradation** | The ability of the inference system to continue serving with reduced functionality or quality when dependent services or resources are unavailable. |

### 2.2 Acronyms

| Acronym | Definition |
|---------|------------|
| ALB | Application Load Balancer |
| AZ | Availability Zone |
| CIS | Center for Internet Security |
| CVE | Common Vulnerabilities and Exposures |
| DAG | Directed Acyclic Graph |
| DORA | DevOps Research and Assessment metrics |
| ECR | Elastic Container Registry |
| EKS | Elastic Kubernetes Service |
| GPU | Graphics Processing Unit |
| HPA | Horizontal Pod Autoscaler |
| KMS | Key Management Service |
| MTTR | Mean Time to Recovery |
| NIST | National Institute of Standards and Technology |
| OCI | Open Container Initiative |
| PHI | Protected Health Information |
| RPS | Requests Per Second |
| SLO | Service Level Objective |
| SRE | Site Reliability Engineering |
| TTL | Time To Live |

---

## 3. Roles and Responsibilities

The following RACI matrix defines accountability for activities governed by this SOP. All named roles correspond to Meridian organizational positions as of the effective date.

| Activity | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |
|----------|-----------------|-----------------|---------------|--------------|
| Model containerization and packaging | ML Engineer, AI/ML Engineering | VP of Engineering | Platform Engineering | Product Manager |
| Model Registry stage promotion (Staging → Production) | ML Engineer | Chief AI Officer or designee | QA Engineering | VP of Clinical AI Products (clinical models only) |
| Infrastructure provisioning for inference | Platform Engineer, IT Operations | VP of IT Operations | ML Engineer | VP of Engineering |
| Production deployment execution | ML Engineer, SRE | VP of Engineering | Platform Engineering | Product Manager, Customer Operations |
| A/B routing configuration | ML Engineer, SRE | VP of Engineering | Chief AI Officer | Product Manager |
| Canary rollout health evaluation | SRE | VP of Engineering | ML Engineer | VP of Clinical AI Products |
| Rollback execution | SRE (primary), ML Engineer (secondary) | VP of Engineering | Chief AI Officer | General Counsel, Chief Compliance Officer |
| Performance tuning and optimization | ML Engineer | VP of Engineering | Platform Engineering | VP of IT Operations |
| Security scanning of inference containers | Security Engineering | CISO | ML Engineer | Chief Compliance Officer |
| Monitoring and alert configuration | SRE, ML Engineer (joint) | VP of Engineering | CISO | VP of IT Operations |
| Incident response for inference outages | SRE | VP of Engineering | ML Engineer, Platform Engineering | CISO, General Counsel |
| SLA reporting and compliance | VP of IT Operations | CISO | SRE | Chief Compliance Officer, Customer Operations |
| Model decommissioning and endpoint teardown | ML Engineer | VP of Engineering | Chief AI Officer | Customer Operations |
| Cost governance for inference infrastructure | VP of IT Operations | CFO | VP of Engineering | Chief AI Officer |

### 3.1 Additional Role Descriptions

**Chief AI Officer (CAIO)** — Dr. Marcus Rivera holds final authority over model promotion to production for all clinical and financial models. The CAIO approves all A/B testing protocols involving patient-impacting or credit-impacting models and signs off on model decommissioning requests.

**VP of Engineering** — David Park is the accountable executive for the operational reliability of the serving infrastructure. All deployment runbooks, rollback procedures, and SLA definitions require VP of Engineering approval.

**SRE Lead** — A designated senior SRE within the Platform Operations team serves as the primary on-call escalation point for inference service incidents. The SRE Lead maintains the PagerDuty escalation policies for all model-serving services.

**Model Steward** — Each production model must have a designated Model Steward (typically the senior MLE who developed or last substantially modified the model). The Model Steward is listed in the MLflow Model Registry metadata and serves as the subject matter expert during incident triage.

---

## 4. Policy Statements

### 4.1 General Serving Principles

**PS-001: Immutable Artifacts** — All model artifacts deployed to production must be stored in the MLflow Model Registry with immutable versioning. Once a model version is promoted to the "Production" stage, its artifact binary shall not be overwritten or modified. Any change—including preprocessing logic, feature ordering, or runtime dependencies—constitutes a new model version requiring a new registry entry.

**PS-002: Containerized Serving Mandate** — All production model inference must execute within OCI-compliant container images. Bare-metal deployments, uncontainerized Python scripts, and Jupyter notebook-based serving are prohibited in production environments.

**PS-003: Infrastructure-as-Code** — All inference infrastructure—including EKS clusters, SageMaker endpoint configurations, ALB rules, and autoscaling policies—must be defined and managed through Terraform (Meridian's approved IaC tool) stored in the `meridian-infra` Git repository. Manual console-based infrastructure changes are prohibited except during declared incident response with VP of Engineering authorization.

**PS-004: Registry Stage Enforcement** — A model shall not be deployed to production unless its MLflow Model Registry stage is set to "Production" and the promotion was approved by the appropriate accountable authority per the RACI matrix in Section 3.

**PS-005: High Availability Minimum** — All production inference endpoints serving synchronous requests must be deployed across a minimum of two Availability Zones within their primary AWS region. Single-AZ deployments are permitted only for non-production environments and batch inference workloads that are not latency-sensitive.

### 4.2 Security and Access Control

**PS-006: Least Privilege Access** — Inference endpoints must be configured with IAM roles granting the minimum permissions necessary for operation. Model containers shall not have access to training data buckets, model registry write APIs, or infrastructure provisioning APIs.

**PS-007: Image Vulnerability Scanning** — Every inference container image must pass a vulnerability scan through AWS ECR scanning (enhanced scanning enabled) before deployment to any staging or production environment. Images with CRITICAL or HIGH CVEs that have a CVSS score ≥ 7.0 and an available fix are blocked from deployment unless a formal risk acceptance is approved by the CISO.

**PS-008: Model Artifact Signing** — All model artifacts promoted to production must be cryptographically signed using Cosign with a key stored in AWS KMS. Signature verification must be enforced at container build time; unsigned artifacts shall not be packaged into inference containers.

**PS-009: Data Encryption** — All inference traffic must be encrypted in transit using TLS 1.2 or higher. Data at rest—including model artifacts in ECR, cached predictions in Redis, and inference logs in S3—must be encrypted using AWS KMS-managed keys. Customer-managed keys (CMKs) are required for PHI-containing data stores.

### 4.3 Availability and Performance

**PS-010: Availability Commitment** — Production inference endpoints supporting synchronous clinical or financial transactions must be deployed with a target availability of 99.9% measured monthly, excluding scheduled maintenance windows approved 72 hours in advance.

**PS-011: Latency Targets** — The following latency targets apply to synchronous inference endpoints, measured at the 99th percentile (p99) over a rolling 5-minute window:

| Use Case Classification | p99 Latency Target | Measurement Point |
|-------------------------|-------------------|-------------------|
| Real-time clinical (diagnostic imaging, risk scoring) | ≤ 500ms | ALB target response time |
| Real-time financial (credit scoring, fraud detection) | ≤ 250ms | ALB target response time |
| Interactive analytics (dashboard queries) | ≤ 2 seconds | API gateway to response |
| Patient-facing applications | ≤ 1 second | ALB target response time |

**PS-012: Graceful Degradation** — All inference services must implement graceful degradation patterns. When dependent services (feature stores, databases) are unavailable, models must return a structured error response or fallback prediction rather than crashing or hanging. Fallback predictions for clinical models must be clearly flagged with `"fallback": true` in the response payload.

### 4.4 Lifecycle Management

**PS-013: Model Version Lifecycle** — Each model version shall proceed through the following lifecycle stages: Registered → Staging → Shadow (optional) → Canary → Production → Archived → Decommissioned. The criteria for each stage transition are defined in Section 5.

**PS-014: Decommissioning Requirement** — A model version must be decommissioned and its endpoint resources reclaimed when any of the following conditions are met: (a) it has been superseded by a newer version receiving 100% of production traffic for ≥ 30 days, (b) the business line owner confirms discontinuation, or (c) a critical security vulnerability is identified and cannot be remediated.

---

## 5. Detailed Procedures

### 5.1 Model Containerization and Packaging

This procedure defines the standardized process for converting a trained model artifact into a production-ready inference container.

#### 5.1.1 Container Specification Requirements

Every inference container must meet the following specifications:

| Requirement | Specification |
|-------------|---------------|
| Base Image | `meridian-ml-base:4.1` (hardened Ubuntu 22.04, Python 3.11) or `meridian-triton-base:2.8` (for Triton Inference Server deployments) |
| Health Check Endpoint | Must implement `GET /health` returning HTTP 200 with JSON `{"status": "healthy", "model_version": "<version>"}` |
| Readiness Check Endpoint | Must implement `GET /ready` returning HTTP 200 only when model is loaded in memory and ready to serve |
| Liveness Check Endpoint | Must implement `GET /live` returning HTTP 200 if container process is running |
| Prediction Endpoint | Must implement `POST /predict` accepting and returning JSON per model-specific schema |
| Metadata Endpoint | Must implement `GET /metadata` returning model version, framework, input schema, and build timestamp |
| Logging | All logs must be emitted to stdout/stderr in structured JSON format including `model_id`, `version`, `request_id`, and `timestamp` fields |
| Graceful Shutdown | Container must handle SIGTERM by draining in-flight requests (up to 30 seconds) and exiting cleanly |
| Resource Limits | Must define CPU and memory requests and limits in the Kubernetes pod spec or SageMaker endpoint configuration |

#### 5.1.2 Container Build Pipeline

1. **Trigger**: Container build is automatically triggered by any of the following events:
   - Model version promotion to "Staging" stage in MLflow Model Registry (via webhook).
   - Merge to `main` branch of the model's deployment repository (`meridian-models/<model-name>`).
   - Manual trigger via Jenkins pipeline `build-inference-container` with approved parameters.

2. **Build Steps** — The Jenkins pipeline (`Jenkinsfile` in the model repository) executes:
   ```
   Stage 1: Checkout model repository and fetch model artifact from MLflow
   Stage 2: Validate model artifact signature using Cosign/KMS
   Stage 3: Build Docker image with model artifact baked in
   Stage 4: Run container structure tests (Google Container Structure Test framework)
   Stage 5: Scan image with AWS ECR enhanced scanning + Trivy
   Stage 6: Run inference smoke tests against container:
       - Send 100 sample requests covering all prediction paths
       - Validate response schema compliance
       - Verify latency < 2x baseline
   Stage 7: Push image to ECR with tags: <version>, <git-sha>, latest-staging
   Stage 8: Update MLflow Model Registry with container image URI
   ```

3. **Image Tagging Convention**:
   - Pattern: `<ecr-registry>/<model-name>:<model-version>-<build-timestamp>-<git-short-sha>`
   - Example: `123456789012.dkr.ecr.us-east-1.amazonaws.com/patient-risk-scorer:v2.3.1-20260518-a3f2b1c`

4. **Build Failure Handling**: If any stage fails, the pipeline aborts. The ML Engineer receives automated notification via Slack (`#ml-build-alerts` channel) and email. Failed builds block stage promotion.

#### 5.1.3 Model-Specific Configuration

Each model repository must contain a `serving-config.yaml` file at the repository root:

```yaml
model_name: "patient-readmission-risk"
model_type: "pytorch"  # pytorch, tensorflow, onnx, custom
serving_framework: "torchserve"  # torchserve, triton, fastapi-custom
runtime:
  python_version: "3.11"
  cuda_version: "12.1"  # null if CPU-only
resources:
  cpu_request: "2"
  cpu_limit: "4"
  memory_request: "4Gi"
  memory_limit: "8Gi"
  gpu_count: 1  # 0 if CPU-only
  gpu_type: "nvidia-t4"  # nvidia-t4, nvidia-a10g, null
scaling:
  min_replicas: 3
  max_replicas: 20
  target_cpu_utilization: 70
  target_rps_per_pod: 50
inference:
  batch_size: 16  # for GPU-optimized batching
  max_batch_delay_ms: 50
  input_timeout_ms: 9500
  max_concurrent_requests: 100
health_checks:
  liveness_initial_delay: 30
  readiness_initial_delay: 60
  period_seconds: 10
  failure_threshold: 3
monitoring:
  metrics_port: 8080
  enable_detailed_latency_histograms: true
fallback:
  enabled: true
  fallback_value: {"risk_score": null, "fallback": true, "reason": "model_unavailable"}
```

The `serving-config.yaml` must be reviewed and approved as part of the staging promotion pull request.

### 5.2 Model Registry Stage Promotion

#### 5.2.1 Stage Transition Process

| From Stage | To Stage | Required Approvals | Validation Gates |
|------------|----------|-------------------|-----------------|
| Registered | Staging | ML Engineer (self-service) | Automated tests pass in CI |
| Staging | Shadow | QA Engineering | Staging performance test results, regression test pass |
| Shadow | Canary | VP of Engineering or designee | Shadow results reviewed by ML Engineer and Product Manager |
| Canary | Production (10%) | VP of Engineering | Canary health dashboard green for ≥ 2 hours |
| Production (10%) | Production (50%) | VP of Engineering | No P1/P2 incidents for ≥ 24 hours |
| Production (50%) | Production (100%) | VP of Engineering, Chief AI Officer (clinical/financial models) | Full traffic validation for ≥ 48 hours |
| Production (any %) | Archived | ML Engineer | Superseded by new version ≥ 30 days; no traffic detected |
| Archived | Decommissioned | VP of Engineering | Resources reclaimed; data retained per retention policy |

#### 5.2.2 Staging Deployment Procedure

1. ML Engineer creates a deployment pull request in the model's repository targeting the `staging` branch.
2. Pull request must include:
   - Updated `serving-config.yaml` with staging environment values.
   - Link to MLflow Model Registry version with "Staging" candidate stage.
   - Results from the automated container build pipeline.
3. QA Engineering reviews and approves the pull request.
4. Upon merge, the CI/CD pipeline deploys the model to the `ml-staging` EKS namespace.
5. QA executes the staging validation suite (Section 5.3).

#### 5.2.3 Production Promotion Request Template

Model Stewards must submit the following completed form via the `#model-promotion-requests` Slack channel or via Jira Service Management ticket:

```
MODEL PRODUCTION PROMOTION REQUEST
----------------------------------
Model Name: [e.g., patient-readmission-risk]
Current Version: [e.g., v2.3.1]
Target Stage: [Canary / Production 10% / Production 100%]
Business Line: [Clinical AI / HealthPay / MedInsight / SaaS]
Model Risk Classification: [High / Medium / Low]

Container Image URI: [ECR URI]
MLflow Registry Link: [URL]
serving-config.yaml attached: [Yes/No]

Pre-Promotion Checks:
[ ] Staging validation suite passed (attach results)
[ ] Load test completed: [RPS tested / Max RPS / p99 latency]
[ ] Regression test passed: accuracy/drift within thresholds
[ ] Security scan passed: 0 CRITICAL, 0 HIGH CVEs
[ ] Shadow results reviewed (if applicable): [attach summary]
[ ] Rollback plan documented in runbook: [link to runbook]

Business Approvals:
[ ] Product Manager approval: [Name, Date]
[ ] Chief AI Officer approval (if clinical/financial): [Name, Date]

Scheduled Promotion Window: [YYYY-MM-DD HH:MM UTC]
Rollback Trigger Criteria: [p99 latency > Xms, error rate > Y%, accuracy drop > Z%]

Model Steward: [Name]
On-Call SRE: [Name, PagerDuty schedule]
```

### 5.3 Staging and Pre-Production Validation

#### 5.3.1 Staging Validation Suite

Before any model version can be promoted beyond Staging, the following validation suite must be executed and passed:

1. **Functional Correctness Tests**:
   - 1,000 labeled test samples (held out from training data) processed through the inference endpoint.
   - Outputs compared against expected predictions; tolerance thresholds defined per model.
   - Edge case tests: empty inputs, maximum-length inputs, special characters, boundary values.

2. **Performance Benchmark Tests**:
   - Load test using Locust (Meridian's approved load testing tool) for a minimum of 30 minutes at 2x expected peak production RPS.
   - Must demonstrate p99 latency within target thresholds under sustained load.
   - CPU, memory, and GPU utilization must remain within 80% of defined limits.

3. **Regression Tests**:
   - Comparison of predictions against the current production model version on a standardized evaluation dataset (minimum 10,000 samples).
   - Prediction distributions must be compared using Kolmogorov-Smirnov or Chi-squared tests.
   - Significant drift (p < 0.01) requires documented justification from the Model Steward.

4. **Security Validation**:
   - Inference endpoint penetration testing using OWASP ZAP baseline scan.
   - Input validation fuzzing: malformed JSON, SQL injection attempts, excessively large payloads.
   - Authentication/authorization test: verify endpoint rejects unauthenticated requests.

#### 5.3.2 Shadow Deployment Validation

For models classified as High Risk (all clinical models and financial credit-scoring models), a shadow deployment of at least 72 hours is required:

1. Deploy the candidate model in shadow mode using the `shadow` namespace in the target production cluster.
2. Configure the ALB or Istio VirtualService to mirror 100% of production traffic to the shadow endpoint.
3. Shadow endpoint responses are logged to a dedicated S3 bucket (`meridian-shadow-results/<model-name>/`) but not returned to clients.
4. After the shadow period, the Model Steward analyzes:
   - Prediction distribution alignment with production model.
   - Latency characteristics under real traffic patterns.
   - Error rates and exception patterns.
   - Any evidence of model staleness or concept drift.
5. Analysis results are documented in a Shadow Deployment Report and attached to the promotion request.

### 5.4 Production Deployment and Traffic Management

#### 5.4.1 Deployment Strategies

Meridian supports three deployment strategies for production model serving. The strategy for each model is determined during the model architecture review and recorded in the MLflow Model Registry.

**Strategy A: Blue/Green with Instant Cutover** (approved for Low Risk models only)
- New version deployed to a separate, fully-scaled "green" endpoint.
- Traffic is switched 100% to green after successful health checks via DNS or ALB target group update.
- Blue endpoint retained for 1 hour as instant rollback target.
- **Not permitted** for clinical or financial models.

**Strategy B: Canary with Gradual Traffic Shifting** (required for Medium and High Risk models)
- New version deployed to a canary endpoint receiving a configurable percentage of traffic.
- Traffic percentage increased in pre-approved increments: 5% → 10% → 25% → 50% → 100%.
- Each increment requires a "hold and evaluate" period:
  - Low Risk: 30 minutes per increment.
  - Medium Risk: 2 hours per increment.
  - High Risk: 24 hours per increment.

**Strategy C: A/B Testing** (temporary, for comparative evaluation)
- Two model versions run concurrently with defined traffic splits.
- Maximum duration: 30 days without VP of Engineering extension approval.
- A/B test design, success metrics, and evaluation criteria must be documented before starting.
- Clinical A/B tests require Chief Medical Officer awareness. Financial A/B tests require VP of Financial Services awareness.

#### 5.4.2 Canary Rollout Procedure (Standard Path)

```
Step 1: Pre-Deployment Checklist
  □ Canary deployment window scheduled (preferably Tuesday-Thursday, 10:00-16:00 local time)
  □ On-call SRE confirmed available
  □ Model Steward confirmed available for 2 hours post-deployment
  □ Rollback runbook reviewed and accessible
  □ Monitoring dashboards loaded and verified
  □ Communication sent to #ml-production-announcements Slack
  □ Change request approved in ServiceNow (CRQ-XXXXX)

Step 2: Initial Canary Deployment (5% traffic)
  □ Deploy using `kubectl apply -f canary-deployment.yaml` or SageMaker update-endpoint
  □ Verify canary pods are Running and passing readiness checks
  □ Configure ALB weighted target group: production 95%, canary 5%
     (Or update Istio VirtualService weight)
  □ Monitor for 5 minutes before proceeding

Step 3: Health Evaluation (5% → 10% → 25% → 50% → 100%)
  For each increment:
    □ Adjust traffic weights
    □ Monitor health indicators for the hold period
    □ Evaluate against rollback triggers (Section 5.5)
    □ If all metrics green, proceed to next increment
    □ If any metric violates threshold, initiate rollback

Step 4: Full Cutover (100%)
  □ Set canary weight to 100%
  □ Verify old version pods are receiving 0 traffic
  □ Update MLflow Registry: old version to "Archived" stage, new version to "Production"
  □ Scale down old version to 0 replicas (retain for 7 days as hot rollback target)

Step 5: Post-Deployment Monitoring
  □ Model Steward and SRE monitor for 2 hours post-cutover
  □ 24-hour follow-up: review latency, error rates, and prediction drift metrics
  □ 7-day follow-up: confirm stability, decommission old endpoint
```

#### 5.4.3 A/B Testing Configuration

A/B routing rules are implemented at the API Gateway (Kong) or service mesh (Istio) layer:

| Routing Mechanism | Use Case | Configuration |
|-------------------|----------|---------------|
| Header-based routing | Testing based on tenant or organization | Route `X-Meridian-Tenant-ID: <list>` to specific model version |
| User-session based | Consistent user experience across requests | Route `X-Session-ID: hash % 2` for 50/50 split |
| Random sampling | Statistical comparison | Route `random() < 0.5` for 50/50 split |
| Geographic routing | Regional model variants | Route based on `CloudFront-Viewer-Country` header |

All A/B test configurations must be declared in the `ab-test-config.yaml` file committed to the model repository and reviewed by the Chief AI Officer before implementation.

### 5.5 Rollback Procedures

#### 5.5.1 Automatic Rollback Triggers

The following conditions, when detected by the Datadog monitoring system, will automatically trigger a rollback via the PagerDuty + Runbook automation (Rundeck) pipeline:

| Trigger | Threshold | Applicable To |
|---------|-----------|---------------|
| Error rate spike | 5xx error rate > 5% for 5 consecutive minutes | All production models |
| Latency violation | p99 latency > 3x target for 5 consecutive minutes | Synchronous endpoints only |
| Availability drop | Endpoint health check failure rate > 10% | All production models |
| Prediction anomaly | Output distribution Z-score > 4.0 vs. baseline (if drift monitoring enabled) | Clinical and financial models |

#### 5.5.2 Manual Rollback Procedure

1. **Decision to Rollback**: The on-call SRE or Model Steward declares a rollback in the `#ml-incident-response` Slack channel using the command `/rollback <model-name> <from-version> <to-version>`.

2. **Traffic Cutover**:
   ```bash
   # For ALB-based routing:
   aws elbv2 modify-rule --rule-arn <rule-arn> \
     --actions Type=forward,TargetGroupArn=<stable-target-group-arn>,Weight=100

   # For Istio-based routing:
   kubectl apply -f rollback-virtualservice.yaml -n ml-production
   ```

3. **Verification**:
   - Confirm 100% of traffic is routed to the stable version within 30 seconds.
   - Monitor error rates and latency for 10 minutes.
   - If metrics stabilize, declare rollback complete.

4. **Post-Rollback Actions**:
   - Log incident in the Incident Management System (ServiceNow).
   - Set rolled-back version pods to 0 replicas (but do not delete).
   - Schedule a root cause analysis (RCA) meeting within 2 business days.
   - Update MLflow Registry: rolled-back version moved to "Archived" stage with rollback annotation.

#### 5.5.3 Rollback Runbook Template

Each model repository must contain a `rollback-runbook.md` with the following minimum content:

```markdown
# Rollback Runbook: <Model Name>

## Stable Version
- Version: <version>
- Container Image: <ECR URI>
- Last Known Good Deployment: <timestamp>

## Rollback Commands
### ALB-Based (us-east-1 production)
\```bash
aws elbv2 modify-rule --rule-arn arn:aws:elasticloadbalancing:us-east-1:... \\
  --actions Type=forward,TargetGroupArn=<STABLE-TG-ARN>,Weight=100
\```

### Istio-Based (eu-west-1 production)
\```bash
kubectl apply -f /runbooks/<model-name>/rollback-virtualservice.yaml
\```

## Rollback Verification
- Datadog dashboard: [link]
- Health check endpoint: curl https://<endpoint>/health
- Expected latency: <baseline>ms at p99

## Post-Rollback
- Notify: #ml-production-announcements
- Create ServiceNow incident
- Disable canary deployment pipeline for this version
```

### 5.6 Model Decommissioning

#### 5.6.1 Decommissioning Criteria

A model version endpoint shall be decommissioned when:
- The version has been fully superseded (0% traffic) for ≥ 30 days.
- The business line owner submits a written decommissioning request via ServiceNow.
- A critical security vulnerability (CVSS ≥ 9.0) is identified in the model serving stack and cannot be patched within the SLA window.

#### 5.6.2 Decommissioning Procedure

1. **Approval**: Obtain VP of Engineering and Chief AI Officer (if clinical/financial) approval via the Model Production Promotion Request form (check "Decommissioning" box).

2. **Notification**: Announce decommissioning to `#ml-production-announcements` and affected product teams at least 14 days prior for production endpoints.

3. **Traffic Drain**: Set traffic weight to 0% and monitor for 7 days to confirm no residual traffic.

4. **Resource Reclamation**:
   ```bash
   # Remove Kubernetes resources
   kubectl delete namespace ml-production/<model-name>-v<version>

   # OR: Delete SageMaker endpoint
   aws sagemaker delete-endpoint --endpoint-name <endpoint-name>
   aws sagemaker delete-endpoint-config --endpoint-config-name <config-name>
   ```

5. **Artifact Retention**: Model artifacts and inference logs are retained per Meridian's Data Retention Policy (SOP-DATA-009):
   - Model artifacts: 7 years for clinical models, 5 years for financial models, 2 years for others.
   - Inference logs: 3 years minimum; longer if required by clinical audit or financial compliance.

6. **Registry Update**: Set MLflow Registry stage to "Decommissioned" with annotation including decommissioning date, reason, and approver.

---

## 6. Controls and Safeguards

### 6.1 Access Controls

| Resource | Access Mechanism | Authorization Level | Approval Required |
|----------|-----------------|--------------------|--------------------|
| MLflow Model Registry (promote to Production) | MLflow REST API / UI | Write access limited to MLE role + CAIO | RBAC via Okta SSO |
| Inference endpoint (modify configuration) | kubectl / AWS Console | ml-sre role only | MFA required |
| ECR image repository (push production images) | AWS IAM | ml-build-service-account | Pipeline-only, no human users |
| Terraform state (modify infrastructure) | Git-based PR merge | platform-engineering role | PR review by 2 approvers |
| Model artifact S3 buckets | AWS IAM | Read: ml-serving-role; Write: ml-training-role only | Read-only for production serving |
| Inference logs and prediction data | Datadog / S3 | Read: ml-operators, compliance; Write: none for human users | Access reviewed quarterly |
| A/B test configuration | Git repository | MLE + Product Manager | PR review required |

### 6.2 Network Controls

| Control | Implementation | Verification |
|---------|---------------|--------------|
| Inference endpoints in private subnets | All production inference services in private VPC subnets; ALB in public subnet only | AWS Config rule: `subnet-auto-assign-public-ip-disabled` |
| Service-to-service authentication | mTLS between services within the mesh (Istio STRICT mode in production) | Istio peer authentication policy audit |
| Egress filtering | Inference pods restricted to required egress destinations only via NetworkPolicy | Kubernetes NetworkPolicy validation in CI |
| DDoS protection | AWS Shield Advanced on all public-facing ALBs; WAF rate limiting rules | Monthly DDoS simulation test |
| API authentication | Kong API Gateway with OAuth2 client credentials; all inference APIs require valid bearer token | Automated penetration test quarterly |

### 6.3 Data Protection Controls

| Control | Implementation |
|---------|---------------|
| PHI in inference requests/responses | TLS 1.2+ in transit; PHI fields marked in schema; audit logging enabled for all PHI access |
| Inference cache data | Redis cache for PHI-carrying data must encrypt at rest (Redis Enterprise with encryption) and set TTL ≤ 1 hour |
| Log sanitization | PHI/PII must be masked or redacted in application logs; Datadog log pipelines configured with PHI scrubbing rules |
| Cross-region data transfers | Clinical inference data for EU patients must remain in eu-west-1; cross-region replication blocked at network policy level |

### 6.4 Integrity Controls

| Control | Implementation | Frequency |
|---------|---------------|-----------|
| Model artifact signing | Cosign signatures verified at container build and deployment admission time (OPA/Kyverno policy) | Every deployment |
| Inference output validation | Schema validation on all prediction responses; responses failing schema trigger alert + logged sample | Continuous |
| Drift monitoring | Reference distribution comparison for selected models (Evidently AI integration) | Daily batch job |
| Immutable deployment tags | Git SHA and build timestamp baked into container labels; verification at pod startup | Every deployment |

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Monitoring Architecture

All inference services must emit metrics to Datadog via the Datadog Agent (Kubernetes DaemonSet) or the StatsD sidecar. The following monitoring components are required:

- **Live dashboards**: Datadog dashboards for real-time health monitoring of all production endpoints.
- **Synthetic checks**: Datadog Synthetic API tests running from multiple geographic locations, calling inference endpoints with authenticated sample requests every 60 seconds.
- **Alert rules**: Defined in Datadog Monitors and routed to PagerDuty.
- **Log aggregation**: All inference logs forwarded to Datadog Log Management, retained for 30 days hot, 1 year cold (S3 archive).

### 7.2 Key Performance Indicators (KPIs)

| KPI | Definition | Target | Measurement Window |
|-----|-----------|--------|-------------------|
| Availability | (Total minutes - Downtime minutes) / Total minutes × 100 | ≥ 99.9% | Monthly, per endpoint |
| Inference Latency (p50) | 50th percentile end-to-end latency from request receipt to response | < Target × 0.7 | Rolling 24 hours |
| Inference Latency (p99) | 99th percentile end-to-end latency | Per Section 4.3, PS-011 | Rolling 5 minutes |
| Throughput (RPS) | Requests per second processed successfully | Per capacity plan | Peak hour |
| Error Rate | (5xx responses + timeout errors) / Total requests × 100 | < 1% | Rolling 1 hour |
| Deployment Success Rate | Successful deployments / Total deployment attempts × 100 | ≥ 95% | Quarterly |
| MTTR | Mean time from incident detection to resolution | < 30 minutes for P1, < 4 hours for P2 | Quarterly |
| Cold Start Latency | Time from pod scheduling to first successful inference | < 60 seconds | Per deployment |
| Model Staleness | Days since last model retraining or validation | < 90 days for clinical models | Monthly scan |

### 7.3 Required Dashboards

Each production model must have the following Datadog dashboards provisioned:

1. **Real-Time Health Dashboard** (per model):
   - Request rate (RPS) — time series
   - Error rate (%) — time series with threshold line at 5%
   - p50/p95/p99 latency — time series with target threshold lines
   - Active replicas count
   - CPU/Memory/GPU utilization per pod
   - Health check status (up/down) per AZ

2. **Business Metrics Dashboard** (per model):
   - Prediction volume by category/class
   - Prediction confidence score distribution
   - Fallback invocation count (if fallback enabled)
   - A/B test metrics (if applicable)

3. **Infrastructure Dashboard** (shared, cluster-wide):
   - Cluster node utilization
   - GPU allocation and utilization
   - Pending pod count
   - ECR image pull latency

### 7.4 Alert Configuration

| Alert Name | Condition | Severity | Notification Channel | Runbook |
|-----------|----------|----------|---------------------|---------|
| High Error Rate | Error rate > 5% for 5 minutes | P1 | PagerDuty + Slack #ml-incident-response | RUNBOOK-AIML-ERR |
| Critical Latency | p99 > 3x target for 5 minutes | P1 | PagerDuty + Slack #ml-incident-response | RUNBOOK-AIML-LAT |
| Endpoint Unavailable | Health check failing for > 2 minutes | P1 | PagerDuty + Slack #ml-incident-response | RUNBOOK-AIML-AVAIL |
| GPU Utilization Imbalance | GPU utilization variance > 30% across pods | P3 | Slack #ml-ops | RUNBOOK-AIML-GPU |
| Deployment Stalled | Deployment not completed within 15 minutes | P2 | Slack #ml-production-announcements | RUNBOOK-AIML-DEPLOY |
| Near Quota Limit | GPU/resource quota usage > 80% | P3 | Slack #platform-engineering | RUNBOOK-AIML-QUOTA |
| Stale Model Detected | Last retraining date > 90 days (clinical models) | P2 | Slack #ml-model-stewardship | RUNBOOK-AIML-STALE |
| Prediction Drift Detected | Distribution drift p-value < 0.001 vs. baseline | P2 | Slack #ml-model-stewardship | RUNBOOK-AIML-DRIFT |
| Shadow Model Anomaly | Shadow prediction divergence > 20% from production | P3 | Slack #ml-model-stewardship | N/A (investigation only) |

### 7.5 Reporting Cadence

| Report | Audience | Frequency | Owner |
|--------|----------|-----------|-------|
| Inference SLA Dashboard | VP of Engineering, Customer Operations | Weekly (automated email) | SRE Lead |
| Model Performance Review | Chief AI Officer, Model Stewards | Monthly | VP of Engineering |
| Capacity Planning Report | VP of IT Operations, CFO | Monthly | Platform Engineering Lead |
| SOC 2 Control Evidence Package | Chief Compliance Officer, External Auditors | Quarterly | CISO |
| Incident Summary and MTTR Report | VP of Engineering, CISO | Quarterly | SRE Lead |

---

## 8. Exception Handling and Escalation

### 8.1 Exception Types

The following categories of exceptions to this SOP may be requested:

| Exception Type | Example | Approval Authority | Maximum Duration |
|---------------|---------|-------------------|-----------------|
| Single-AZ deployment | Dev/test environment or batch job | VP of Engineering | 90 days (renewable) |
| Unscanned container deployment | Emergency hotfix requiring immediate deployment | CISO (emergency approval), VP of Engineering | 24 hours; must be scanned within that window |
| Elevated latency SLO | Model known to require longer inference time (e.g., large 3D imaging model) | Chief AI Officer + VP of Engineering | Permanent with documented justification |
| Manual deployment | Jenkins pipeline failure requiring manual kubectl apply | VP of Engineering | Per incident |
| Skip shadow deployment | Low-risk model with proven stability record | VP of Engineering | Permanent with risk acceptance |
| Extended A/B test | Comparative study requiring longer evaluation | VP of Engineering + Chief AI Officer | Additional 30 days |

### 8.2 Exception Request Process

1. Requester submits an exception request via ServiceNow using the "SOP Exception Request" form.
2. The request must include:
   - Specific SOP section(s) for which exception is sought.
   - Business justification.
   - Risk assessment and compensating controls.
   - Proposed duration.
   - Alternative compliance approach.
3. The designated approval authority reviews within 2 business days (or within 1 hour for emergency exceptions).
4. Approved exceptions are:
   - Logged in the Exception Register (maintained by Chief Compliance Officer).
   - Annotated in the affected model's MLflow Registry entry.
   - Reviewed at the next AI Governance Committee meeting.
5. Expired exceptions that are not renewed revert to full SOP compliance automatically.

### 8.3 Incident Escalation Path

| Level | Trigger | Escalation Target | Response Time |
|-------|--------|-------------------|--------------|
| L1 - Initial Detection | Alert fires or user report | On-call SRE | Acknowledge within 5 minutes |
| L2 - Team Escalation | SRE unable to resolve within 15 minutes | SRE Lead + Model Steward | Join incident channel within 10 minutes |
| L3 - Management Escalation | Incident unresolved at 30 minutes; or P1 incident confirmed | VP of Engineering | Join incident bridge within 15 minutes |
| L4 - Executive Escalation | P1 incident > 1 hour; or customer-facing impact confirmed | CISO, Chief AI Officer | Notified immediately; join within 30 minutes |
| L5 - Crisis Management | PHI breach confirmed; regulatory notification required | General Counsel, Chief Compliance Officer, CEO | Crisis management protocol activated |

### 8.4 Emergency Change Procedure

In the event of a Severity 1 incident requiring an emergency model update or configuration change:

1. The on-call SRE declares an emergency change in the `#ml-incident-response` channel.
2. The VP of Engineering (or CISO for security emergencies) provides verbal approval, documented in the incident channel.
3. The emergency change is implemented; all actions are logged.
4. Within 24 hours of resolution, a retrospective ServiceNow change request must be filed documenting the change, justification, and approval.
5. Any SOP violations during the emergency change are noted but not penalized if properly documented.

---

## 9. Training Requirements

### 9.1 Required Training Courses

| Training Module | Target Audience | Frequency | Delivery Method | Provider |
|----------------|-----------------|-----------|----------------|----------|
| SOP-AIML-018: Model Serving Procedures | All ML Engineers, SRE | Annually + upon revision | E-learning + hands-on lab | Internal L&D / AI/ML Engineering |
| Production Deployment and Rollback Workshop | ML Engineers, SRE, Platform Engineers | Annually | Instructor-led simulation | VP of Engineering team |
| Inference Security and PHI Handling | All personnel with production inference access | Annually | E-learning + assessment | CISO / Security Engineering |
| Incident Response for AI/ML Services | SRE, SRE Lead, Model Stewards | Bi-annually | Tabletop exercise | SRE Lead + CISO |
| Datadog Monitoring and Alert Management | ML Engineers, SRE | Upon onboarding + annually | Self-paced + certification | Datadog University (internal account) |
| Kubeflow and SageMaker Operations | ML Engineers, Platform Engineers | Upon tool version upgrade | Hands-on workshop | VP of Engineering team |

### 9.2 Training Tracking and Compliance

- All training completions are tracked in Meridian's Learning Management System (Workday Learning).
- Training compliance is reviewed quarterly by the Chief Human Resources Officer and reported to the AI Governance Committee.
- Personnel who are non-compliant with required training shall have their production access suspended until training is completed.
- Training materials are version-controlled alongside this SOP; when SOP-AIML-018 is revised, training materials must be updated within 30 days.

### 9.3 Onboarding Requirements

New hires in roles covered by this SOP must complete the following before being granted production access:

1. SOP-AIML-018 e-learning module (with passing score ≥ 80% on assessment).
2. Shadow a senior team member through at least one production deployment and one rollback drill.
3. Complete the Datadog monitoring certification.
4. Obtain sign-off from their direct manager and the VP of Engineering.

---

## 10. Related Policies and References

### 10.1 Meridian Internal SOPs

| SOP ID | Title | Relationship |
|--------|-------|-------------|
| SOP-AIML-012 | Model Development Lifecycle | Precedes model serving; defines training and experimentation standards |
| SOP-AIML-015 | Model Validation and Approval | Defines validation criteria; outputs validated models for serving |
| SOP-AIML-022 | Model Monitoring and Drift Detection | Complements this SOP with detailed drift detection procedures |
| SOP-DATA-005 | Feature Store and Training Data Management | Defines feature pipelines consumed at inference time |
| SOP-DATA-009 | Data Retention and Disposal Policy | Governs retention of inference logs, predictions, and model artifacts |
| SOP-SEC-007 | Container Security Standards | Defines base image hardening, scanning, and vulnerability management |
| SOP-SEC-012 | Incident Response and Management | Overarching incident response framework; invoked by this SOP |
| SOP-INFRA-003 | Kubernetes Cluster Operations | Infrastructure standards for EKS clusters hosting inference workloads |
| SOP-INFRA-008 | Disaster Recovery and Business Continuity | DR procedures for mission-critical inference services |
| SOP-COMP-001 | SOC 2 Control Framework | Maps SOC 2 trust services criteria to operational controls |
| SOP-COMP-005 | Model Risk Management (SR 11-7) | Governance for financial models under SR 11-7 |
| SOP-CLIN-022 | Clinical AI Validation Protocol | Clinical-specific validation requirements before production deployment |

### 10.2 External Standards and Frameworks

| Standard | Reference | Applicability |
|----------|-----------|---------------|
| NIST AI RMF 1.0 | AI 100-1 | Adopted voluntarily; risk management framework for all AI systems |
| NIST SP 800-53 Rev. 5 | Security and Privacy Controls | Reference for security control selection |
| ISO 27001:2022 | Information Security Management | Meridian is certified; Annex A controls mapped to this SOP |
| HITRUST CSF v11 | Healthcare Security Framework | Meridian HITRUST Certified; control inheritance applies |
| SOC 2 Trust Services Criteria | Security, Availability, Confidentiality | Annual SOC 2 Type II audit scope includes inference infrastructure |
| CIS Kubernetes Benchmark v1.7 | Container Security | EKS clusters must achieve ≥ 90% CIS benchmark compliance |
| FDA 510(k) | Premarket Notification | Applies to diagnostic imaging AI products with FDA clearance |
| EU MDR 2017/745 | Medical Device Regulation | Applies to CE-marked clinical AI products |

### 10.3 Key Internal Resources

| Resource | Location | Owner |
|----------|----------|-------|
| MLflow Model Registry | `https://mlflow.meridian.health` | AI/ML Engineering |
| Model serving runbooks repository | `github.com/meridian-health/runbooks-ml-serving` | SRE Team |
| Terraform infrastructure repository | `github.com/meridian-health/meridian-infra` | Platform Engineering |
| Production deployment Jenkins pipelines | `https://jenkins.meridian.health/job/ml-serving/` | Platform Engineering |
| Datadog dashboards (ML Serving) | Datadog Dashboard List → "ML Serving" | SRE Team |
| PagerDuty escalation policies | PagerDuty → Escalation Policies → "ML Serving" | SRE Lead |
| ServiceNow change management | `https://servicenow.meridian.health/change` | IT Operations |

---

## 11. Revision History

| Version | Date | Author | Changes | Approver |
|---------|------|--------|---------|----------|
| 1.0 | 2021-03-15 | David Park (VP of Engineering) | Initial release; established basic containerized serving standards for Meridian SaaS Platform | David Park |
| 1.1 | 2021-09-22 | ML Engineering Team | Added GPU support specifications; introduced canary deployment patterns; expanded health check requirements | David Park |
| 2.0 | 2022-06-10 | Dr. Marcus Rivera (CAIO) | Major revision: incorporated HealthPay Financial Services models; added SR 11-7 awareness; introduced A/B testing framework; added Model Registry stage enforcement | David Park |
| 2.1 | 2023-01-18 | SRE Team | Added Infrastructure-as-Code mandate; introduced automatic rollback triggers; expanded monitoring and alerting section with PagerDuty integration details | David Park |
| 3.0 | 2024-11-05 | Dr. Marcus Rivera (CAIO), David Park | Comprehensive revision: added shadow deployment requirements; refined risk-based deployment strategies; added model decommissioning procedures; introduced MLflow Model Registry as authoritative artifact store; aligned with NIST AI RMF adoption; strengthened SOC 2 controls mapping | David Park |
| 3.1 | 2025-02-14 | Dr. Marcus Rivera (CAIO) | Minor revision: updated GPU instance types to reflect AWS availability; added LangSmith tracing integration for AI observability; clarified PHI handling for EU data subjects in eu-west-1; added quarterly capacity planning report requirement | David Park |
| 3.2 | 2025-05-18 | Dr. Marcus Rivera (CAIO) | Updated effective date per annual review cycle; refined cold start latency measurement methodology; added Cosign artifact signing requirement (PS-008); updated training module references to Workday Learning; revised decommissioning retention periods to align with SOP-DATA-009 v2.1; added emergency change procedure (Section 8.4) | David Park |

---

**Document Status: Active**

**Next Scheduled Review: 2027-02-25**

**Questions regarding this SOP should be directed to the owner: Dr. Marcus Rivera, Chief AI Officer (m.rivera@meridian.health)**

---

*© 2025 Meridian Health Technologies, Inc. All rights reserved. This document contains proprietary and confidential information intended solely for authorized Meridian personnel. Distribution or reproduction outside of authorized channels is prohibited.*