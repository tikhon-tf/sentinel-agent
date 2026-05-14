---
sop_id: "SOP-AIML-012"
title: "GPU and Compute Resource Management"
business_unit: "AI/ML Engineering"
version: "3.5"
effective_date: "2025-12-03"
last_reviewed: "2026-03-20"
next_review: "2026-09-23"
owner: "Dr. Marcus Rivera, Chief AI Officer"
approver: "David Park, VP of Engineering"
classification: "Internal"
regulations:
  - "SOC 2"
status: "Active"
---

# Standard Operating Procedure: GPU and Compute Resource Management

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the framework for the lifecycle management, provisioning, monitoring, and decommissioning of Graphics Processing Unit (GPU) and high-performance compute (HPC) resources at Meridian Health Technologies, Inc. The exponential growth of large language models (LLMs), diffusion models for diagnostic imaging, and real-time patient risk scoring engines requires a disciplined approach to resource allocation that balances the velocity of AI innovation against the material cost footprint of our infrastructure.

This document defines the operational controls necessary to ensure that compute resources—particularly the scarce and expensive GPU instances powering the Clinical AI Platform and MedInsight Analytics—are allocated based on business priority, utilized efficiently, and continuously optimized to prevent resource hoarding, idle capacity, and unbudgeted cloud expenditure.

### 1.2 Scope

This SOP applies to all compute resources within the Meridian SaaS Platform infrastructure that are classified as accelerated compute, including but not limited to:

| Resource Category | Examples | Primary Use Cases |
|---|---|---|
| GPU Instances (Training) | Amazon EC2 p4d.24xlarge, p5.48xlarge | Model training, fine-tuning clinical LLMs, diffusion model training for diagnostic imaging |
| GPU Instances (Inference) | Amazon EC2 g5.xlarge, g5.12xlarge, AWS Inferentia2 | Real-time inference endpoints for patient risk scoring, imaging analysis, fraud detection |
| GPU Instances (Development) | Amazon EC2 g4dn.xlarge, g4dn.2xlarge | Model development, experimentation, Jupyter notebook environments |
| HPC CPU Clusters | Amazon EC2 c6i.32xlarge, hpc6id.32xlarge | Population health analytics batch processing, claims data transformation |
| Vector Database Compute | Pinecone index pods, GPU-accelerated vector search | MedInsight patient similarity search, clinical document retrieval |

**In Scope:**
- Provisioning, allocation, and decommissioning of all GPU and HPC compute instances across AWS us-east-1 and eu-west-1 regions.
- Cost allocation, tagging enforcement, and chargeback mechanisms for compute resources.
- Capacity planning and quota management for AI/ML Engineering, Clinical AI Products, HealthPay Financial Services, and MedInsight Analytics teams.
- Monitoring of utilization metrics, idle resource detection, and automated reclamation.
- Access control mechanisms and isolation boundaries for multi-tenant compute environments.

**Out of Scope:**
- End-user device compute (laptops, workstations) managed by IT Operations under SOP-IT-045.
- Non-accelerated general-purpose compute for web application hosting and API gateways (covered under SOP-IT-022).
- CI/CD pipeline compute resources managed by Platform Engineering (covered under SOP-ENG-018).

### 1.3 Applicability

This SOP applies to all Meridian Health Technologies personnel, contractors, and vendors who provision, configure, access, or decommission accelerated compute resources. Compliance is mandatory for:

- AI/ML Engineering (including ML Operations, MLOps, and Research teams)
- Clinical AI Products team
- HealthPay Financial Services data science and fraud detection teams
- MedInsight Analytics engineering team
- IT Operations (for infrastructure-level provisioning)
- Any Meridian employee or contractor with IAM permissions to launch EC2 GPU instances or submit SageMaker training jobs

Non-compliance with this SOP may result in immediate revocation of compute provisioning privileges, mandatory training reassignment, and escalation to the Chief AI Officer and VP of Engineering for remediation.

## 2. Definitions and Acronyms

| Term/Acronym | Definition |
|---|---|
| **GPU** | Graphics Processing Unit; specialized processor designed for parallel computation, essential for deep learning workloads. |
| **HPC** | High-Performance Computing; aggregated computing resources delivering performance at scale for complex analytical workloads. |
| **CUDA** | Compute Unified Device Architecture; NVIDIA's parallel computing platform and programming model for GPUs. |
| **VRAM** | Video Random Access Memory; dedicated memory on a GPU device, measured in gigabytes (GB). |
| **Multi-Instance GPU (MIG)** | NVIDIA technology enabling a single physical GPU to be partitioned into multiple isolated GPU instances. |
| **Compute Quota** | The maximum number of concurrent accelerator instances (by type) a team may provision within a given AWS region. |
| **Resource Reservation** | A time-bound claim on a defined set of compute resources for a specific purpose, managed via the Meridian Compute Reservation System. |
| **Idle Resource** | A GPU instance with <15% aggregate utilization sustained for >2 hours during business days (0600–2200 ET), excluding defined maintenance windows. |
| **Chargeback** | The monthly allocation of compute infrastructure costs to the business unit that consumed the resources, based on resource tags. |
| **Spot Instance** | AWS EC2 instance running on spare capacity that can be interrupted with two minutes' notice; used for interruptible training workloads. |
| **Reserved Instance (RI)** | A billing commitment for one or three years providing significant discount over on-demand pricing for predictable workloads. |
| **Savings Plan** | A flexible pricing model offering lower prices in exchange for a committed hourly spend over a one- or three-year term. |
| **Model Training Job** | A reproducible, containerized workload that trains or fine-tunes a machine learning model, tracked via MLflow and orchestrated by Kubeflow. |
| **Inference Endpoint** | A deployed model serving predictions in real-time, autoscaled based on request throughput. |
| **PHI** | Protected Health Information; individually identifiable health information subject to HIPAA protections. |
| **CAGE** | Clinical AI Governance Engine; Meridian's custom system for tracking model lineage, training data provenance, and compute resource utilization for AI risk management. |
| **Resource Tag** | An AWS resource metadata label used to associate instances with projects, teams, cost centers, and compliance classifications. |

## 3. Roles and Responsibilities

The following RACI matrix defines the roles, accountabilities, consultation relationships, and information flows for GPU and compute resource management:

| Activity | Chief AI Officer | VP of Engineering | AI/ML Engineering Leads | IT Operations | Data Science Teams | Finance (FP&A) |
|---|---|---|---|---|---|---|
| Strategic capacity planning | **A** | R | C | C | I | I |
| Compute quota approval (>$50K/mo) | **A** | C | R | C | I | I |
| Compute quota approval (<$50K/mo) | I | **A** | R | C | I | I |
| Daily resource provisioning | I | I | R | **A** | C | I |
| Resource tagging enforcement | I | **A** | R | R | C | I |
| Idle resource detection and reclamation | I | C | R | **A** | I | I |
| Monthly chargeback reconciliation | I | C | C | R | I | **A** |
| Cost optimization (RI/SP purchasing) | C | **A** | C | R | I | R |
| Compliance monitoring (CAGE integration) | **A** | R | R | C | I | I |
| Access control and IAM governance | I | R | C | **A** | I | I |

**R** = Responsible (performs the work)
**A** = Accountable (approves the work)
**C** = Consulted (provides input)
**I** = Informed (receives notification)

### 3.1 Specific Role Descriptions

**Dr. Marcus Rivera, Chief AI Officer (Owner):**
- Serves as the executive sponsor for this SOP.
- Approves annual compute capacity plans and total budget allocations.
- Chairs the monthly AI Infrastructure Review Board meeting.
- Adjudicates escalated resource conflicts between business units.
- Approves any exception requests exceeding $100,000 in incremental monthly spend.

**David Park, VP of Engineering (Approver):**
- Authorizes infrastructure-as-code (IaC) changes that modify compute provisioning templates.
- Approves Reserved Instance and Savings Plan purchase commitments.
- Validates technical feasibility of capacity plans against AWS service quotas and regional availability.
- Escalation point for GPU availability incidents that risk breaching Clinical AI Platform SLAs.

**AI/ML Engineering Leads:**
- Submit quarterly compute capacity forecasts with granular project-level justification.
- Enforce resource tagging standards within their teams’ provisioning pipelines.
- Review weekly utilization reports and initiate action on idle resources.
- Maintain a prioritized queue of training jobs for resource scheduling.

**Samantha Torres, VP of IT Operations:**
- Owns the AWS Organizations and Service Control Policies governing GPU instance types.
- Provisions Reserved Instances and Savings Plans per approved purchase orders.
- Manages the Meridian Compute Reservation System (MCRS) platform.
- Monitors real-time GPU availability and triggers pre-provisioned fallback instance types when primary types are unavailable.
- Generates monthly chargeback reports.

**Robert Liu, VP of Financial Services:**
- Must approve any compute usage from HealthPay Financial Services that processes credit scoring or lending model training data, ensuring SR 11-7 model risk management requirements are met for the compute environment.

**Thomas Anderson, Chief Compliance Officer:**
- Reviews quarterly audit logs of compute resource access for environments processing regulated data.
- Approves changes to compute resource tagging taxonomy that impact compliance classification.

## 4. Policy Statements

### 4.1 Resource Allocation by Business Priority

Meridian classifies all compute workloads into three priority tiers. Resource allocation and preemption rules follow these tiers absolutely:

| Priority Tier | Description | Example Workloads | Preemption Authorization |
|---|---|---|---|
| **Tier 1 – Critical** | Production inference serving patients or processing live financial transactions | Clinical AI Platform inference endpoints, HealthPay fraud detection scoring, MedInsight real-time risk calculation | Cannot be preempted. Must maintain ≥99.9% availability. |
| **Tier 2 – Essential** | Model training for validated project roadmaps with regulatory deadlines | FDA submission model retraining, EU AI Act mandated bias audits, quarterly model refresh cycles | Can be preempted only for Tier 1 capacity recovery. 24-hour notice required. |
| **Tier 3 – Discretionary** | Exploratory research, academic collaborations, hackathon infrastructure, non-validated proofs of concept | Early-stage LLM experimentation, internal tool prototyping, student intern projects | Subject to immediate preemption for Tier 1 or Tier 2. No notice required. |

### 4.2 Tagging Mandate

Every GPU instance, SageMaker training job, and HPC cluster launched within Meridian's AWS environments must carry a minimum set of nine mandatory resource tags at the time of provisioning. Instances launched without compliant tagging will be automatically terminated after a 60-minute grace period.

The mandatory tag set is enumerated in Section 6.2 of this SOP.

### 4.3 Cost Allocation and Chargeback

All accelerated compute costs are charged back to the consuming business unit within 45 days of month-end close. The Finance (FP&A) team, in coordination with IT Operations, publishes a monthly Compute Cost Attribution Report (CCAR) that details:

- Total GPU compute spend by business unit and project
- Idle resource cost waste (calculated as cost × duration of below-threshold utilization)
- Reserved Instance and Savings Plan coverage rates
- Month-over-month and year-over-year variance analysis

Business unit leaders (clinical AI, healthpay, medinsight platform leads) must sign off on the CCAR within five business days of publication. Disputed charges are escalated to the Chief AI Officer for adjudication within 30 days.

### 4.4 Resource Hoarding Prohibition

Provisioning GPU instances and leaving them idle constitutes "resource hoarding" and is prohibited. Specifically:

- GPU instances must not remain in a running state with <15% aggregate GPU utilization for >2 consecutive hours between 0600 and 2200 ET on business days.
- Exceptions apply for instances actively running long-duration training jobs that are tracked in the Meridian Compute Reservation System (MCRS) or via MLflow with an active run ID.
- Teams with >10% idle resource cost waste across three consecutive months will have their compute quotas reduced by 25% for the subsequent quarter.

### 4.5 Capacity Planning Cadence

All teams consuming GPU or HPC resources must submit quarterly capacity forecasts, due on the 15th of the final month of each fiscal quarter:

| Quarter | Forecast Due Date | Covers Period |
|---|---|---|
| Q1 FY26 | March 15, 2026 | July–September 2026 |
| Q2 FY27 | June 15, 2026 | October–December 2026 |
| Q3 FY27 | September 15, 2026 | January–March 2027 |
| Q4 FY26 | December 15, 2025 | April–June 2026 |

Forecasts are submitted via the Meridian Capacity Planning Portal (MCPP) and must include project-level justification, expected instance types, hourly usage estimates, and funding source confirmation.

## 5. Detailed Procedures

### 5.1 GPU Instance Provisioning

**Procedure ID: PROC-AI-012-01**

This procedure covers the end-to-end workflow for requesting, approving, and provisioning GPU instances for both interactive (e.g., JupyterLab development) and batch (e.g., training job) workloads.

#### 5.1.1 Request Submission

All GPU instance provisioning requests must be submitted through the Meridian Compute Reservation System (MCRS), accessible at `https://mcrs.internal.meridian.health`. Direct EC2 console or AWS CLI provisioning is not permitted except under the emergency procedure defined in Section 5.1.6.

The MCRS request form requires the following fields:

| Field | Description | Validation |
|---|---|---|
| Project ID | CAGE-registered project identifier (e.g., `CAGE-MRI-SEG-V4`) | Must exist in CAGE registry |
| Requestor | Individual Meridian employee ID | AD-authenticated |
| Instance Type | AWS EC2 instance type (e.g., `p4d.24xlarge`) | Must be in approved instance type catalog |
| Instance Count | Number of concurrent instances (1–64) | Subject to team quota limits |
| Estimated Duration | Hours or days (maximum 30-day reservation) | >30 days requires escalation |
| Priority Tier | 1–3 per Section 4.1 definitions | Tier 1 requires VP-level approval |
| Environment | dev, staging, production, sandbox | production triggers additional PHI controls |
| Justification | Free-text technical justification (minimum 100 characters) | Required for Tier 2 and Tier 1 requests |
| Cost Center | Finance department cost center code | Must match project funding |
| PHI Processing | Yes/No indicator | Yes triggers HIPAA-compliant environment provisioning |

#### 5.1.2 Approval Workflow

Upon submission, MCRS routes the request for approval according to the following matrix:

| Request Parameter | Approval Route |
|---|---|
| Tier 3, ≤4 g4dn.xlarge or equivalent, ≤24 hours | Auto-approved (no human review) |
| Tier 3, any size, >24 hours | AI/ML Engineering Lead approval within 8 business hours |
| Tier 2, any size, any duration | AI/ML Engineering Lead + Project Lead, within 24 hours |
| Tier 1, any size, any duration | AI/ML Engineering Lead + Project Lead + VP of Engineering or Chief AI Officer, within 48 hours |
| Monthly cost estimate >$50,000 | Additional Finance (FP&A) approval required |
| PHI Processing = Yes | Additional Chief Compliance Officer notification (not approval, but automated notification for logging) |

Approvers receive automated Slack notifications via the `#compute-approvals` channel. Unactioned approvals for Tier 2 or Tier 1 escalate first to the direct manager, then to the Chief AI Officer after 72 hours of dormancy.

#### 5.1.3 Automated Provisioning

Once all approvals are obtained, MCRS triggers the automated provisioning pipeline:

1. **Template Selection:** The AWS CloudFormation or Terraform module appropriate to the instance type and environment class is selected from the Meridian IaC Repository (GitHub: `meridian-iac/compute-provisioning`).
2. **Tag Injection:** The nine mandatory tags (see Section 6.2) are injected from MCRS metadata into the launch template user data and AWS resource tags.
3. **IAM Role Attachment:** The appropriate instance profile is attached, granting only the minimum required permissions. The instance profile is determined by the environment and PHI-processing flag.
4. **VPC Placement:** Instances are placed in the appropriate VPC subnet: development instances in the `dev-ai` VPC, staging in `staging-ai`, and production in `prod-ai` (isolated network).
5. **Launch Confirmation:** The instance ID, private IP, and reservation expiration timestamp are written back to MCRS. The requestor receives an automated email and Slack DM with connection instructions.
6. **CAGE Registration:** A compute session record is created in the Clinical AI Governance Engine (CAGE) linking the instance ID to the project, model lineage, and data provenance metadata.

**Provisioning SLA:** Auto-approved Tier 3 requests must be fulfilled within 15 minutes of submission, 98% of the time. Tier 2 and Tier 1 requests must be fulfilled within 60 minutes of final approval, 95% of the time.

#### 5.1.4 Connection and Access

Provisioned instances are accessed exclusively via AWS Systems Manager Session Manager. SSH (port 22) is blocked at the security group level in all environments. Connection instructions:

1. From the Meridian-managed workstation, authenticate to the AWS Management Console using Okta SSO with MFA.
2. Navigate to AWS Systems Manager → Fleet Manager.
3. Locate the provisioned instance by Instance ID (provided in the provisioning confirmation email).
4. Select "Start Session" to initiate an interactive shell session.
5. All session activity is logged to AWS CloudTrail and a session transcript is written to the `meridian-ssm-logs` S3 bucket.

#### 5.1.5 Decommissioning and Reservation Expiry

GPU instances are automatically decommissioned by MCRS at the reservation expiration timestamp. The decommissioning process:

1. **15-minute pre-expiration warning:** A notification is emitted to the requestor via Slack, email, and (for Tier 1 instances) PagerDuty. The notification includes an option to extend the reservation subject to quota availability.
2. **At expiration:** MCRS initiates an EC2 Stop or Terminate API call (Stop for development instances so that data volumes persist for 72 hours; Terminate for staging and production instances for cost optimization).
3. **Post-termination processing:** Resource tags are archived to the Meridian Cost Attribution data warehouse. The CAGE compute session record is closed.
4. **Data persistence:** EBS volumes attached to development instances persist in a stopped state for 72 hours before deletion. Teams must snapshot volumes they wish to retain beyond 72 hours (using SOP-IT-041 for backup procedures).

#### 5.1.6 Emergency Provisioning Procedure

In the event that a Tier 1 production inference endpoint requires immediate scale-out and the normal MCRS approval workflow would introduce unacceptable latency, the "break-glass" procedure may be invoked:

1. The on-call MLOps engineer (contact via PagerDuty rotation `mlops-oncall`) assesses the situation and determines that the MCRS workflow SLA cannot be met.
2. The engineer sends a templated Slack message to `#incident-response` with the header `EMERGENCY GPU PROVISION REQUEST`.
3. The VP of Engineering or Chief AI Officer acknowledges the request in-channel within 15 minutes.
4. The on-call engineer manually provisions instances via the `emergency-provision` Lambda function, which applies a minimal tag set (Instance ID, cost center, emergency reason).
5. Within 24 hours post-incident, the provisioned instances must be retroactively registered in MCRS with full metadata and approvals (post-hoc).

### 5.2 Compute Cost Management

**Procedure ID: PROC-AI-012-02**

This procedure defines the monthly cycle for monitoring, reporting, and optimizing GPU compute costs.

#### 5.2.1 Daily Cost Anomaly Detection

IT Operations maintains an automated cost anomaly detection system (AWS Cost Anomaly Detection integrated with Meridian custom dashboards). Alerts are triggered when:

- Daily GPU compute spend exceeds the trailing 30-day average by >40%.
- Any single instance incurs >$5,000 in 24-hour cost.
- Any business unit exceeds its monthly forecast allocation by >20% before the 15th of the month.

Alerts are routed to:
- `#finops-alerts` Slack channel (real-time)
- Weekly cost anomaly digest email to AI/ML Engineering Leads and Finance (FP&A)

#### 5.2.2 Monthly Chargeback Reconciliation

The monthly reconciliation procedure proceeds as follows:

| Day | Action | Responsible |
|---|---|---|
| 1st of month | IT Operations freezes the prior month's cost and utilization data in the Meridian Cost Attribution data warehouse. | IT Operations |
| 5th of month | Finance (FP&A) produces the draft Compute Cost Attribution Report (CCAR) from the warehouse. | Finance (FP&A) |
| 10th of month | Draft CCAR distributed to business unit leads: Clinical AI (Dr. Rivera's team), HealthPay (Robert Liu's team), MedInsight. | Finance (FP&A) |
| 15th of month | Business unit leads submit dispute tickets via the FinOps portal for any contested line items. | Business unit leads |
| 25th of month | Disputes adjudicated by Chief AI Officer and VP of Engineering; final CCAR published. | Chief AI Officer |
| 30th of month | Chargebacks posted to business unit Profit & Loss statements. | Finance (FP&A) |

#### 5.2.3 Reserved Instance and Savings Plan Purchasing

IT Operations, in coordination with VP of Engineering, executes Reserved Instance (RI) and Savings Plan (SP) purchases quarterly based on capacity forecasts.

**Purchase Triggers:**
- RI purchase when a workload demonstrates stable 24/7 usage for >3 consecutive months.
- Compute Savings Plan purchase when aggregate on-demand GPU spend exceeds $150,000/month for >2 consecutive months.
- All RI and SP commitments must be approved by VP of Engineering via the Meridian Purchase Order system.

### 5.3 Capacity Planning

**Procedure ID: PROC-AI-012-03**

#### 5.3.1 Quarterly Forecast Submission

By the 15th of the final month of each fiscal quarter (see Section 4.5), each AI/ML Engineering Lead submits a capacity forecast via the Meridian Capacity Planning Portal (MCPP).

The forecast form requires:

| Forecast Element | Granularity |
|---|---|
| Instance type × region × quarter | Monthly average running hours |
| Reserved Instance coverage request | Instance type × count × 1yr or 3yr term |
| New instance type qualification request | Instance type, justification, estimated adoption timeline |
| Spot Instance eligibility (interruptible training) | Yes/No per workload, estimated spot percentage |
| Multi-region failover requirements | Primary region, failover region, replication requirements |

#### 5.3.2 Quarterly Capacity Review Board

Within 10 business days of the forecast deadline, the Chief AI Officer convenes the AI Infrastructure Review Board. Attendees include:

- Chief AI Officer (Chair)
- VP of Engineering
- AI/ML Engineering Leads (all business units)
- IT Operations representative
- Finance (FP&A) representative

The Board reviews:
1. Consolidated capacity demand vs. AWS service quotas and regional availability.
2. Reserved Instance and Savings Plan optimization opportunities.
3. Conflict resolution for over-subscribed instance types.
4. New instance type qualification decisions.
5. Budget allocation adjustments.

Decisions are documented in the Meridian AI Infrastructure Review Board Decision Log (Confluence: `https://confluence.internal.meridian.health/display/AIIRB`).

### 5.4 Idle Resource Detection and Reclamation

**Procedure ID: PROC-AI-012-04**

#### 5.4.1 Automated Detection

The Meridian Idle Resource Detector (MIRD) is a scheduled Lambda function that runs every 15 minutes, scanning all running GPU instances across Meridian AWS accounts. For each instance:

1. MIRD queries Amazon CloudWatch for the `gpu_utilization` and `gpu_memory_utilization` custom metrics (collected via NVIDIA DCGM exporter, shipped to CloudWatch via a unified CloudWatch agent installed in all Meridian GPU AMIs).
2. If average aggregate GPU utilization is <15% for a rolling 120-minute window AND the current time is between 0600–2200 ET business day, the instance is flagged as "idle."
3. MIRD cross-references the instance with MCRS active reservations. If the instance has a non-expired reservation and the justification indicates "long-running training job with periodic low utilization," the instance is exempted.
4. MIRD posts the idle instance list to the `#idle-resources` Slack channel.

#### 5.4.2 Notification and Remediation

Upon detection:

- **Tier 3 instances:** The instance owner receives an automated Slack DM and email with a 60-minute remediation window. If utilization has not risen above 15% after 60 minutes, the instance is automatically **stopped** (not terminated) by MIRD.
- **Tier 2 instances:** The instance owner and their AI/ML Engineering Lead receive notification. The remediation window is 120 minutes. If not remediated, the instance is stopped.
- **Tier 1 instances:** The AI/ML Engineering Lead and on-call DevOps engineer receive a PagerDuty alert (severity: LOW). No automated action is taken. Manual investigation is required within 4 hours.

#### 5.4.3 Idle Cost Waste Dashboard

IT Operations maintains a real-time Idle Cost Waste Dashboard (accessible via `https://grafana.internal.meridian.health/d/idle-gpu`) that displays:

- Current idle instances (count and $/hour burn rate)
- Idle cost waste trailing 7-day and 30-day totals by team
- Top-10 worst offenders (individual users)
- Automated reclamation actions taken in prior 24 hours

### 5.5 Multi-Tenancy and GPU Sharing

**Procedure ID: PROC-AI-012-05**

#### 5.5.1 Multi-Instance GPU (MIG) Partitioning

For workloads that do not fully utilize a large GPU (e.g., g5.12xlarge or p4d.24xlarge), Meridian enables NVIDIA Multi-Instance GPU (MIG) partitioning. MIG allows a physical A100 GPU to be partitioned into up to seven isolated GPU instances, each with dedicated VRAM and compute resources.

**Partitioning Configuration:**
- The default MIG profile on p4d instances splits each A100-40GB GPU into: `2g.20gb` (two instances with 20GB VRAM each) or `3g.40gb` (one full GPU; for workloads requiring >20GB VRAM).
- MIG configurations are encoded in the AMI launch template and cannot be modified by end users.
- Each MIG instance maintains hard isolation: workloads in one MIG slice cannot observe or impact the others.

#### 5.5.2 Kubernetes GPU Scheduling

All model training and batch inference workloads are orchestrated via Kubeflow on Amazon EKS. The Kubernetes GPU device plugin enforces hard VRAM and compute limits per pod:

- Pods specify GPU requirements declaratively: `resources.limits.nvidia.com/gpu: 1`
- The scheduler enforces node-level quotas: a p4d.24xlarge node with eight GPUs can host a maximum of eight concurrent single-GPU pods.
- Teams are isolated via Kubernetes namespaces and ResourceQuotas.

#### 5.5.3 Priority and Preemption

Kubeflow pipelines are annotated with PriorityClass labels corresponding to the priority tiers defined in Section 4.1. The Kubernetes scheduler preempts lower-priority pods to make room for higher-priority ones:

- Tier 1 scheduling: guaranteed, pods are never evicted.
- Tier 2 scheduling: can be preempted by Tier 1 with 120-second graceful termination period.
- Tier 3 scheduling: can be preempted by Tier 1 or Tier 2 with 30-second termination period.

### 5.6 Spot Instance Utilization

**Procedure ID: PROC-AI-012-06**

Meridian uses AWS Spot Instances to reduce cost for interruptible workloads. Spot Instances can provide 60–70% discount over on-demand pricing.

**Eligibility:**
- All Tier 3 training workloads.
- Tier 2 training workloads that are checkpointed at intervals ≤15 minutes (so that minimal work is lost on interruption).
- Tier 1 inference workloads are **not** eligible for Spot Instances.

**Spot Reclamation Handling:**
When AWS reclaims a Spot Instance:
1. The instance receives a two-minute interruption notice.
2. The `meridian-spot-daemon` agent running on the instance receives this notice and triggers a checkpoint save to the designated S3 bucket.
3. The training orchestration system (Kubeflow) resubmits the workload on a replacement instance (Spot if available, on-demand fallback if not).
4. Training resumes from the last saved checkpoint.

Failure to checkpoint within the two-minute window results in training progress loss; this is an acceptable risk for Tier 2 and Tier 3 workloads per Section 4.1 tolerances.

## 6. Controls and Safeguards

### 6.1 Access Controls and IAM Governance

Access to GPU compute resources is governed by AWS Identity and Access Management (IAM) policies enforced through AWS Organizations Service Control Policies (SCPs). No individual user possesses unrestricted permission to launch EC2 GPU instances.

| Role | IAM Permissions | Restriction |
|---|---|---|
| ML Engineer (Standard) | `ec2:RunInstances` (g4dn.*, g5.* only) | Must specify a `project` tag matching their assigned projects in CAGE. Cannot launch p4d or p5 instances. |
| Senior ML Engineer | `ec2:RunInstances` (all GPU types except p5) | Must specify `project` tag. Weekly quota: 8 × p4d instances concurrently. |
| ML Operations (MLOps) | `ec2:RunInstances` (all GPU types) | Break-glass access for incident response. All launches logged with mandatory `emergency-reason` tag. |
| IT Operations (Infrastructure) | Full EC2 access for provisioning IaC pipelines | No interactive EC2 console access. All actions via CDK/Terraform pipelines only. |
| All other personnel | No GPU provisioning permissions | Can only use pre-provisioned SageMaker environments or shared JupyterHub clusters. |

IAM policies enforce the following mandatory conditions:

- `aws:RequestTag/project` must be present and match `^CAGE-[A-Z]{3,5}-[A-Z0-9-]+$`
- `ec2:InstanceType` must be in the `approved-gpu-instance-types` condition key
- Instance launches in `prod-ai` VPC require an additional `PHI-approved` tag (applied only by pre-authorized IAM roles)

All IAM policy changes affecting GPU access require approval via the Meridian Change Advisory Board (CAB), with the Chief AI Officer as mandatory approver.

### 6.2 Resource Tagging Enforcement

The mandatory tag taxonomy is enforced at two levels: AWS Service Control Policies (SCP) prevent launching untagged instances, and the MIRD automated detection system terminates non-compliant instances.

**Mandatory Tags (All Accelerated Compute Instances):**

| Tag Key | Description | Example Value | Enforcement |
|---|---|---|---|
| `meridian:project` | CAGE project identifier | `CAGE-MRI-SEG-V4` | SCP: `ec2:RunInstances` fails without it |
| `meridian:environment` | Deployment environment tier | `production` | SCP: Must be one of `dev`, `staging`, `production`, `sandbox` |
| `meridian:cost-center` | Finance cost center code | `FIN-AI-2024-0182` | SCP: Must match active cost center list |
| `meridian:owner` | Individual Meridian email | `alice.chen@meridian.health` | SCP: Must be valid AD user |
| `meridian:priority-tier` | Priority classification | `tier-2` | Cloud Custodian rule: Terminates mismatched tier/instance-type combinations |
| `meridian:expires-at` | ISO 8601 reservation expiry | `2026-03-21T18:00:00Z` | MIRD: Terminates instances 24 hours past expiry |
| `meridian:phi-processing` | Boolean indicating PHI exposure | `true` | MIRD: Instances tagged `true` without `prod-ai` VPC placement are immediately terminated |
| `meridian:sop-version` | SOP version governing the instance | `SOP-AIML-012 v3.5` | Audit: Flagged if version is stale (>2 versions behind current) |
| `meridian:workload-type` | Category of workload | `training`, `inference`, `development` | Cloud Custodian: Validates alignment with instance type (e.g., p4d for training) |

**Tag Governance Dashboard:**
IT Operations maintains a Tag Compliance Dashboard (in Grafana) that shows, for each business unit: tag compliance rate, most common missing tags, and instances at risk of termination. Business units below 98% compliance for three consecutive weeks will have provisioning quotas frozen until compliance is restored.

### 6.3 Isolation Boundaries

Meridian enforces three isolation boundaries for GPU compute environments:

| Boundary | Mechanism | Purpose |
|---|---|---|
| **Network** | VPC segmentation: `dev-ai` (CIDR 10.32.0.0/16), `staging-ai` (10.33.0.0/16), `prod-ai` (10.34.0.0/16) | Prevents cross-environment network access. `prod-ai` has no internet egress (traffic routed through VPC endpoints + internal proxy). |
| **IAM** | Separate AWS accounts: `meridian-ai-dev` (123456789012), `meridian-ai-prod` (210987654321) | Blast-radius containment. Production account has separate root credentials. |
| **Data** | PHI-processing instances launch in `prod-ai` VPC with encrypted EBS (CMK) and no outbound internet access | HIPAA technical safeguards for compute processing PHI. |

Multi-tenant environments (Kubeflow + EKS) use Kubernetes Namespaces with NetworkPolicy restrictions, preventing pods in namespace `healthpay` from communicating with pods in namespace `clinical-ai` unless explicitly authorized via NetworkPolicy allow-lists.

### 6.4 GPU Driver and Firmware Management

NVIDIA GPU drivers and CUDA toolkit versions are managed through a controlled AMI pipeline:

- All Meridian GPU AMIs are built from a golden image pipeline that bakes in validated NVIDIA driver versions.
- New NVIDIA driver releases are tested by IT Operations for a 30-day validation period before promotion to the production AMI catalog.
- Critical security patches to NVIDIA drivers bypass the 30-day validation window but require VP of Engineering approval.

Current validated driver versions (as of March 2026):

| Environment | Driver Version | CUDA Version | AMI ID (us-east-1) |
|---|---|---|---|
| Development | NVIDIA 545.23.08 | CUDA 12.3 | `ami-0a1b2c3d4e5f60001` |
| Staging | NVIDIA 550.54.15 | CUDA 12.4 | `ami-0a1b2c3d4e5f60002` |
| Production | NVIDIA 550.54.15 | CUDA 12.4 | `ami-0a1b2c3d4e5f60003` |

End users are prohibited from installing drivers or CUDA versions outside the AMI catalog. Instances detected with non-standard GPU drivers will be terminated within 60 minutes by MIRD.

### 6.5 Network Security

GPU compute instances reside in security groups that enforce the principle of least privilege:

- **Inbound:** All ports blocked except: port 443 for HTTPS from the Meridian corporate CIDR for JupyterLab/notebook access; and ephemeral ports for inter-service communication within the same VPC and security group.
- **Outbound (prod-ai):** Only approved AWS service endpoints (S3, ECR, CloudWatch Logs, Systems Manager) via VPC endpoints. No outbound internet connectivity.
- **Outbound (dev-ai, staging-ai):** Permitted to approved package registries (PyPI, Conda-forge, NVIDIA NGC) via a transparent HTTP proxy with content filtering.

## 7. Monitoring, Metrics, and Reporting

### 7.1 Real-Time Monitoring Dashboard

The Meridian GPU Operations Dashboard (Grafana, `https://grafana.internal.meridian.health/d/gpu-ops`) provides a unified operational view. The dashboard is displayed on the AI/ML Engineering office wall monitors and accessible via any authenticated browser.

**Dashboard Panels:**

| Panel | Metrics Displayed | Refresh Interval |
|---|---|---|
| Fleet Overview | Total running GPU instances; count by instance type, environment, priority tier, and team | 1 minute |
| Utilization Heatmap | GPU utilization and VRAM utilization (% of total) per instance; color-coded: green (>70%), yellow (30–70%), red (<30%) | 5 minutes |
| Cost Burn Rate | Current dollar-per-hour burn rate by team; projected daily total | 15 minutes |
| Idle Resource Alert Feed | Chronological list of idle resource detections with instance ID, owner, cost impact | 15 minutes |
| Spot Interruption Tracker | Real-time feed of Spot Instance reclaim notifications; tracks successful vs. failed checkpoint completions | Real-time (stream) |
| Quota Consumption Gauge | Per-team quota consumption as percentage of allocation | 1 minute |

### 7.2 Key Performance Indicators (KPIs)

The following KPIs are tracked monthly and reviewed at the AI Infrastructure Review Board:

| KPI | Definition | Target | Measurement Method |
|---|---|---|---|
| GPU Utilization Efficiency (GUE) | Average aggregate GPU utilization across all running instances during business hours | ≥65% | CloudWatch metrics aggregation |
| Idle Resource Waste Rate (IRWR) | Cost of idle instances as percentage of total GPU spend | ≤5% | MIRD log × AWS Cost Explorer |
| Reserved Instance Coverage Rate (RICR) | Percentage of total GPU running hours covered by Reserved Instances or Savings Plans | ≥70% | AWS Cost Explorer RI/SP report |
| Tag Compliance Rate | Percentage of GPU instances with all nine mandatory tags | ≥99% | Tag Governance Dashboard query |
| Spot Interruption Recovery Rate | Percentage of interrupted spot workloads successfully checkpointed and resumed | ≥95% | Kubeflow pipeline logs + Spot interruption events |
| Provisioning SLA Attainment | Percentage of Tier 3 auto-approved requests fulfilled within 15-minute SLA | ≥98% | MCRS audit log analysis |
| Chargeback Dispute Rate | Percentage of monthly CCAR line items disputed by business units | ≤3% | Finance (FP&A) dispute tracking |

### 7.3 Weekly Utilization Report

Every Monday at 0900 ET, MCRS distributes a Weekly GPU Utilization Report to all AI/ML Engineering Leads (via email and Confluence publication). The report includes:

- Per-team utilization breakdown (average utilization, peak utilization, idle hours, cost)
- Per-project utilization breakdown (same metrics)
- Top 10 idle offenders (individual users with highest idle cost waste)
- Instance type availability snapshot (current on-demand capacity status for Meridian's commonly used instance types in us-east-1 and eu-west-2)
- Recommendations: instances recommended for termination, rightsizing opportunities, RI/SP coverage gaps

Team leads must acknowledge the report within 48 hours by commenting on the Confluence page (acknowledgement tracked via Confluence page view analytics and required explicit `@mention` confirmation).

### 7.4 Monthly Compute Cost Attribution Report (CCAR)

As described in Section 5.2.2, the monthly CCAR is the authoritative cost allocation report. It is published to the Meridian Financial Reporting portal and retained for a minimum of seven fiscal years.

### 7.5 Compliance and Audit Reporting

The Chief Compliance Officer (CCO) receives a quarterly GPU Compute Audit Package containing:

- All instances that processed PHI data, including instance ID, project, duration, and IAM access logs.
- All break-glass emergency provisioning invocations, including post-hoc approvals.
- Tag compliance trend line.
- Log of all policy exception approvals.

The CCO reviews and signs the audit package. Signed packages are retained for seven fiscal years.

## 8. Exception Handling and Escalation

### 8.1 Exception Request Process

Requests for deviations from this SOP must be submitted via the Meridian Policy Exception Portal (`https://exceptions.internal.meridian.health`). The exception request must include:

- **SOP Reference:** `SOP-AIML-012 v3.5`
- **Section Reference:** Specific policy section for which exception is sought
- **Justification:** Business or technical justification with supporting evidence (minimum 250 words)
- **Duration:** Start and end dates for the exception (maximum 90 days; extensions require a new request)
- **Impact Assessment:** Acknowledged risk and impact of the deviation
- **Alternative Mitigations:** Any compensating controls to be implemented during the exception period

### 8.2 Exception Approval Authority

| Exception Type | Approver | Maximum Duration |
|---|---|---|
| Quota exceeding ≤25% of current allocation, duration ≤14 days | AI/ML Engineering Lead | 14 days |
| Quota exceeding ≤50% of current allocation, duration ≤30 days | VP of Engineering | 30 days |
| Quota exceeding >50% of allocation OR any Tier 1 quota exception | Chief AI Officer | 90 days |
| PHI-processing exception | Chief AI Officer + Chief Compliance Officer (joint approval) | 30 days |
| Cost exception >$100,000 incremental monthly spend | Chief AI Officer + CFO | 90 days |
| Tagging exception (any) | VP of Engineering | 14 days |

### 8.3 Escalation Path

Resource conflicts and policy violations escalate as follows:

1. **Level 1 – Team Lead Resolution:** AI/ML Engineering Leads negotiate directly to resolve inter-team resource conflicts, documented in `#ai-infra-resolution` Slack channel.
2. **Level 2 – VP of Engineering:** Escalated if Level 1 fails to resolve within three business days or if conflict involves production (Tier 1) resources. VP of Engineering renders a binding decision within two business days.
3. **Level 3 – Chief AI Officer:** Escalated for any conflict with >$50,000/month cost impact, any conflict involving both GPU compute and data pipeline resources, or any conflict that DP cannot resolve within two business days.

### 8.4 Incident Response for GPU Availability

If GPU capacity in us-east-1 becomes unavailable (e.g., AWS InstanceType availability failures), the following escalation procedure triggers:

1. **IT Operations monitoring** detects GPU capacity constraint via AWS Service Health Dashboard and Meridian synthetic provisioning tests.
2. **Pre-provisioned fallback instance types** (defined in the MCRS launch template) are automatically attempted:
   - `p4d.24xlarge` → `p4de.24xlarge` → `p3dn.24xlarge`
   - `g5.12xlarge` → `g5.24xlarge` → `g4dn.12xlarge`
3. If fallback types are also unavailable, the on-call DevOps engineer is paged (PagerDuty severity: HIGH).
4. The on-call engineer evaluates cross-region failover to eu-west-2 for non-PHI workloads (PHI workloads cannot leave us-east-1 production VPC).
5. VP of Engineering is notified for any availability incident lasting >2 hours.

## 9. Training Requirements

### 9.1 Initial Training

All personnel who provision or access GPU compute resources must complete the following training within 30 days of onboarding or role transition:

| Training Module | Delivery Method | Duration | Frequency |
|---|---|---|---|
| **GPU-CMPL-101: Meridian Compute Resource Management Fundamentals** | LMS (self-paced with knowledge check) | 2 hours | Once, at onboarding |
| **GPU-CMPL-201: MCRS Provisioning Walkthrough** | Hands-on lab (instructor-led via video conference + sandbox environment) | 3 hours | Once, at onboarding |
| **GPU-CMPL-301: Cost Awareness and Tagging Compliance** | LMS (self-paced, interactive) | 1 hour | Once, at onboarding |
| **GPU-CMPL-401: PHI-Aware Compute Environment Operations** | Instructor-led (mandatory for any personnel working in `prod-ai` VPC) | 2 hours | Once, at onboarding; reassigned upon any HIPAA incident |

### 9.2 Refresher Training

All personnel who provision GPU resources must complete refresher training:

- **Annual Refresher: GPU-CMPL-501: Annual GPU Policy Refresher** (LMS, 1 hour) — covers policy changes, new instance types, updated procedures.
- **Spot Instance Training: GPU-CMPL-601: Running Spot-Interruptible Workloads on Meridian** (LMS, 45 minutes) — mandatory for any team using Spot Instances for Tier 2 training.

### 9.3 Non-Compliance Remediation

Personnel who violate this SOP (e.g., provisioning untagged instances, hoarding idle resources, bypassing MCRS) are subject to the following progressive remediation:

1. **First Violation (rolling 12 months):** Automated email warning; required re-completion of GPU-CMPL-101 within 7 days.
2. **Second Violation (rolling 12 months):** Manager notification; one-week suspension of GPU provisioning privileges; mandatory instructor-led retraining (GPU-CMPL-201, in-person or live remote).
3. **Third Violation (rolling 12 months):** Permanent revocation of GPU provisioning privileges; access reduced to pre-provisioned shared environments only. Escalation to VP of Engineering for final determination.

### 9.4 Training Tracking and Reporting

All training completion records are maintained in the Meridian LMS (Workday Learning). IT Operations produces a monthly training compliance report for the Chief AI Officer, listing any individual whose GPU-CMPL training is expired or incomplete. Individuals who are out of compliance for >30 days have their GPU provisioning IAM permissions suspended until training is completed.

## 10. Related Policies and References

### 10.1 Meridian Internal SOP Cross-References

| SOP ID | Title | Relationship |
|---|---|---|
| SOP-IT-022 | General-Purpose Compute Resource Management | Complementary SOP covering non-GPU compute (EC2 CPU instances, Lambda, ECS tasks) |
| SOP-IT-045 | End-User Device and Workstation Management | Manages laptop and workstation GPU allocation; not covered by this SOP |
| SOP-ENG-018 | CI/CD Pipeline Infrastructure Management | Pipeline compute resources are managed by Platform Engineering under separate governance |
| SOP-IT-041 | Data Backup and Retention | Cross-referenced for EBS volume snapshot procedures |
| SOP-SEC-104 | IAM Access Governance | IAM policy governance framework for all AWS access |
| SOP-AIML-008 | MLflow Experiment Tracking and Model Registry | Tracks training jobs referenced by this SOP |
| SOP-AIML-009 | Clinical AI Governance Engine (CAGE) Operations | CAGE compute session record management |
| SOP-CMPL-019 | Vendor Security Risk Management | Reference for third-party access to compute environments (if applicable) |

### 10.2 External Standards and References

| Reference | Description | Applicability |
|---|---|---|
| NIST SP 800-53 Rev. 5 | Security and Privacy Controls for Information Systems | Controls related to audit logging, access enforcement |
| AWS Well-Architected Framework – Cost Optimization Pillar | Cloud financial management best practices | Reserved Instance/Savings Plan strategy |
| NVIDIA Multi-Instance GPU (MIG) Documentation | GPU partitioning for multi-tenant environments | MIG configuration and isolation |
| NVIDIA DCGM | Data Center GPU Manager for telemetry export | Utilization metric collection |

## 11. Revision History

| Version | Effective Date | Author/Owner | Summary of Changes |
|---|---|---|---|
| 1.0 | 2022-06-15 | Dr. Marcus Rivera | Initial SOP publication. Established basic GPU provisioning, tagging, and cost management framework for the newly formed AI/ML Engineering team. Covered only us-east-1; no MIG support; manual provisioning via Jira tickets. |
| 2.0 | 2023-02-10 | Dr. Marcus Rivera | Major revision: Introduced MCRS automated provisioning system. Added priority tier classification (Tier 1–3) with preemption rules. Added idle resource detection (manual review). Expanded chargeback procedure. Added initial Spot Instance guidance. |
| 2.1 | 2023-07-19 | Dr. Marcus Rivera | Minor revision: Updated Kubernetes GPU scheduling section to reflect migration to EKS with Kubeflow. Added NVIDIA driver version table (pinned to Driver 535). Updated IAM policy conditions for SCP enforcement. |
| 3.0 | 2024-04-02 | David Park (VP of Engineering) | Major revision: Introduced MIG partitioning support. Added automated idle resource detection and reclamation (MIRD Lambda). Added `prod-ai` isolated VPC for PHI workloads. Added CAGE integration for compute session tracking. Updated tagging taxonomy from 5 to 9 mandatory tags. Added MCPP capacity planning portal. Break-glass emergency provisioning procedure added. |
| 3.2 | 2025-01-21 | Dr. Marcus Rivera | Revised cost thresholds upward by 15% to reflect 2025 infrastructure pricing adjustments. Updated Kubernetes priority class preemption timings. Added `eu-west-2` region cross-reference for failover planning. Updated NVIDIA driver to 545.23.08 for development environments. |
| 3.5 | 2025-12-03 | Dr. Marcus Rivera | Current revision. Updated for new p5.48xlarge instance type availability (H100 GPUs). Updated NVIDIA driver table to v550.54.15 for staging and production. Revised Reserved Instance/Savings Plan triggers to reflect 2025 purchasing benchmarks. Added `Spot Interruption Recovery Rate` KPI. Expanded exception handling escalation path with specific dollar thresholds. Added `GPU-CMPL-601` Spot Instance training requirement. Formalized the Weekly GPU Utilization Report cadence. Updated cross-references to SOP-AIML-009, SOP-SEC-104, SOP-ENG-018. |
| 3.5 (this rev) | 2026-03-20 | Dr. Marcus Rivera | Last reviewed. No changes. Next review scheduled for September 23, 2026. |