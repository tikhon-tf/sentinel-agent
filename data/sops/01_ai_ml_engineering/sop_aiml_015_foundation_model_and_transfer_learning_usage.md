---
sop_id: "SOP-AIML-015"
title: "Foundation Model and Transfer Learning Usage"
business_unit: "AI/ML Engineering"
version: "3.5"
effective_date: "2024-07-08"
last_reviewed: "2025-05-22"
next_review: "2025-11-07"
owner: "Dr. Marcus Rivera, Chief AI Officer"
approver: "David Park, VP of Engineering"
classification: "Internal"
regulations:
  - "EU AI Act"
  - "NIST AI RMF"
status: "Active"
---

# SOP-AIML-015: Foundation Model and Transfer Learning Usage

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the mandatory governance framework, technical controls, and operational processes for the evaluation, selection, procurement, fine-tuning, deployment, and ongoing monitoring of Foundation Models (FMs) and transfer learning methodologies across all Meridian Health Technologies, Inc. business units and product lines. The purpose is to ensure that all utilization of pre-trained models aligns with regulatory obligations under the EU AI Act (Regulation 2024/1689), NIST AI Risk Management Framework (AI RMF 1.0), HIPAA, SOC 2, and SR 11-7, while maintaining the highest standards of clinical safety, data privacy, and model explainability.

This SOP operationalizes the Board-level AI Governance Committee charter by providing detailed, auditable procedures for managing the unique risks associated with foundation models, including supply chain provenance, open-source license compliance, catastrophic forgetting during domain adaptation, and emergent bias amplification.

### 1.2 Scope

This SOP applies to:

- **All Personnel:** Full-time employees, contractors, interns, and third-party vendors engaged in the development, deployment, or maintenance of machine learning models at Meridian Health Technologies.
- **All Foundation Model Architectures:** Transformer-based models, large language models (LLMs), vision transformers (ViTs), diffusion models, multimodal models, and any future architectures trained on broad data at scale and adapted for downstream tasks.
- **All Transfer Learning Modalities:** Full fine-tuning (FFT), parameter-efficient fine-tuning (PEFT) including LoRA, QLoRA, and adapters, prompt engineering, retrieval-augmented generation (RAG), and in-context learning (ICL).
- **All Business Units:**
    - Clinical AI Platform (high-risk AI under EU AI Act Annex III)
    - HealthPay Financial Services (subject to SR 11-7 model risk management)
    - MedInsight Analytics (processes PHI from ~12M patients)
    - Meridian SaaS Platform (multi-tenant infrastructure)
- **All Lifecycle Phases:** Model discovery, initial evaluation, proof-of-concept, production deployment, ongoing monitoring, and retirement.
- **All Geographies:** Operations in North America (Boston, Toronto) and the European Union (London, Berlin). Models serving EU data subjects must comply with GDPR and the EU AI Act irrespective of where the model training occurs.

**Out of Scope:** Statistical models that do not utilize neural network-based transfer learning (e.g., logistic regression, gradient-boosted trees trained de novo on proprietary data only). Traditional machine learning model development is governed by SOP-AIML-003. Generative AI usage by non-engineering staff (e.g., using ChatGPT Enterprise for email drafting) is governed by SOP-IT-042 (Acceptable Use of Generative AI Tools).

## 2. Definitions and Acronyms

| Term / Acronym | Definition |
| :--- | :--- |
| **Foundation Model (FM)** | A machine learning model trained on broad data at scale such that it can be adapted to a wide range of downstream tasks. Defined per the EU AI Act, Article 3(1)(44). |
| **Transfer Learning** | The reuse of a pre-trained model's learned feature representations on a second, related task. |
| **Fine-Tuning** | The process of updating the weights of a pre-trained FM using a domain-specific dataset. Includes full fine-tuning (FFT) and parameter-efficient fine-tuning (PEFT). |
| **Parameter-Efficient Fine-Tuning (PEFT)** | Methods such as Low-Rank Adaptation (LoRA) or adapters that update only a small fraction of the model's parameters. |
| **Catastrophic Forgetting** | The tendency of a neural network to abruptly and drastically forget previously learned information upon learning new information. |
| **High-Risk AI System** | An AI system classified under Annex III of the EU AI Act. Meridian’s Clinical AI Platform products fall under this classification. |
| **Model Card** | A standardized, structured document that describes the technical details, evaluation results, intended uses, and limitations of an ML model. Follows the schema defined in SOP-AIML-010. |
| **Supply Chain Risk** | Risks inherited from upstream pre-trained models, including poisoned datasets, backdoor triggers, and unverified provenance. |
| **Alignment** | The degree to which an AI system's outputs conform to intended human values, ethical principles, and specified design objectives. |
| **Hallucination** | A generated output that is nonsensical or unfaithful to the provided source content. |
| **SBOM (Software Bill of Materials)** | A nested inventory for software, extended in this SOP to include AI model components (AI-BOM). |
| **AI RMF** | NIST AI Risk Management Framework 1.0. |
| **SR 11-7** | Federal Reserve/OCC/FFIEC guidance on Model Risk Management. |
| **DPO** | Data Protection Officer (Dr. Klaus Weber). |
| **AI-GC** | Meridian AI Governance Committee, established 2024. |
| **CAIO** | Chief AI Officer (Dr. Marcus Rivera). |
| **MRL** | Model Risk Level, a tiered classification (Low, Moderate, High) defined in SOP-AIML-001. |

## 3. Roles and Responsibilities

The following RACI matrix defines the roles responsible for the execution and oversight of this SOP.

| Role | Responsibility | RACI (for Key Procedures) |
| :--- | :--- | :---: |
| **VP of Engineering (David Park)** | Ultimate authority for the engineering implementation of all FMs, including deployment approvals in the Meridian SaaS Platform. | A |
| **Chief AI Officer (Dr. Marcus Rivera)** | Executive owner of this SOP. Approver for all exceptions related to foundation model usage strategy. Chair of the AI Governance Committee. | A |
| **VP of Clinical AI Products (Dr. Aisha Okafor)** | Responsible for clinical domain-specific fine-tuning protocols and ensuring clinical safety standards for any FM used in clinical decision support. | R |
| **VP of Financial Services (Robert Liu)** | Responsible for SR 11-7 compliance in HealthPay models, including fine-tuned FMs for credit scoring and fraud detection. | R |
| **AI/ML Engineering Leads (Technical Leads)** | Responsible for authoring model cards, executing PEFT procedures, maintaining the AI Model Registry, and implementing model monitoring. | R |
| **Chief Information Security Officer (Rachel Kim)** | Accountable for the technical security controls governing FM supply chains, including container security, weight integrity, and adversarial robustness testing. | A |
| **Chief Privacy Officer / DPO (Dr. Klaus Weber)** | Accountable for ensuring no EU personal data is inadvertently processed in non-compliant jurisdictions during fine-tuning. Reviews Data Protection Impact Assessments (DPIAs) for FM use cases involving personal data. | A |
| **General Counsel (Maria Gonzalez)** | Responsible for reviewing and approving licenses for all third-party foundation models, particularly non-standard or restrictive open-source licenses (e.g., RAIL, BSL). | A |
| **Chief Compliance Officer (Thomas Anderson)** | Monitors adherence to this SOP and regulatory change management. Owns the Model Risk Register. | R |
| **VP of IT Operations (Samantha Torres)** | Ensures the computational environment (AWS SageMaker, GPU clusters) is configured according to the data isolation requirements of this SOP. | R |
| **Data Stewards (Business Unit Assigned)** | Responsible for the curation, anonymization, and quality assurance of the datasets used to fine-tune FMs. | R |

**Key:** R = Responsible for execution, A = Accountable for approval/sign-off, C = Consulted, I = Informed.

## 4. Policy Statements

Meridian Health Technologies adopts the following high-level policy commitments regarding foundation models and transfer learning:

1.  **Human-Centric Oversight:** All foundation models, especially those deployed in high-risk clinical workflows, shall be subject to human oversight measures as required by EU AI Act Article 14. Autonomously generated outputs that affect patient care or financial decisions must be reviewable and overridable by a qualified human professional.
2.  **Provenance and Integrity:** No foundation model shall be downloaded, fine-tuned, or deployed without a fully verified chain of custody. Weights, training code, and configuration files must be sourced from authenticated, trusted repositories and validated against cryptographic hashes prior to integration into our AWS environments.
3.  **License Compliance First:** The use of any foundation model is contingent upon a legal review by General Counsel. FMs released under restrictive non-commercial, non-compete, or viral open-source licenses (e.g., specific RAIL variants, SSPL, BSL) are prohibited for use in commercial Meridian products without explicit written exception.
4.  **Data Isolation:** No proprietary Meridian data, including PHI, PCI, or confidential financial data, shall be transmitted to third-party commercial API endpoints (e.g., OpenAI, Anthropic, Cohere) for the purpose of model fine-tuning or embedding generation. All fine-tuning must occur within Meridian’s secured Virtual Private Cloud (VPC) boundaries.
5.  **Bias and Fairness:** A quantitative bias audit using SOP-AIML-012 standards must be performed on the base FM before fine-tuning begins, and again on the fine-tuned, task-specific model before it can be promoted to staging. Models exhibiting group fairness metrics below defined thresholds will be quarantined.
6.  **Transparency and Explainability:** For every deployed FM, an EU AI Act-compliant Model Card and a system-level transparency notice must be published in the AI Model Registry (MLflow). This satisfies the transparency obligations under Article 13 and the documentation requirements of Annex IV.
7.  **Resilience and Security:** Foundation models are subject to the same vulnerability management lifecycle as the rest of the technology stack. Models must be hardened against adversarial prompt injection, data extraction, and model inversion attacks, with controls scaled to the Model Risk Level (MRL).

## 5. Detailed Procedures

### 5.1 Foundation Model Discovery and Initial Screening

This procedure governs the exploratory phase where a team identifies a potential foundation model for a new use case.

**Step 5.1.1: Identify Business Need and Constraints**
The AI/ML Engineering Lead, in collaboration with the Product Manager, shall document the following in a "Foundation Model Intake Form" (see Appendix A of the AI Governance Charter):
- Intended use case and classification (Clinical, Financial, Analytics, Productivity).
- Performance metric targets (e.g., accuracy, F1-score, perplexity, ROUGE-L).
- Latency requirements (inference time in milliseconds).
- Computational budget constraints (total GPU hours for fine-tuning and inference).
- Languages required for deployment.
- Regulatory classification (e.g., EU AI Act High-Risk, SR 11-7 relevant).

**Step 5.1.2: Model Discovery and Long-Listing**
Engineers shall source models exclusively from the Meridian-approved FM Repository list maintained in Confluence. The approved sources are:
1.  **Hugging Face Hub:** Only models from verified organizations and those achieving an Open Source Initiative (OSI)-compliant license tag.
2.  **AWS SageMaker JumpStart:** Models hosted and screened by AWS, as per our BAA with AWS.
3.  **NVIDIA NGC Catalog:** Curated, containerized models with signed provenance.
4.  **Direct Academic Releases:** Only if the hash is published in a peer-reviewed paper and is independently verifiable.

A long-list of 3-5 candidate models shall be identified.

**Step 5.1.3: Initial Security Screening (CISO/Rachel Kim's Team)**
Before any model weights are downloaded to a Meridian-managed environment, the CISO team executes the following automated and manual checks:
- **Weight File Scanning:** Weights must be scanned using Vault's integration with JFrog Xray for embedded malware, malicious pickle files, or corrupt data structures. **Control:** Any model weight file flagged by the scanner is immediately quarantined in an air-gapped S3 bucket and undergoes forensic analysis. Use of the model is halted.
- **Configuration Audit:** The model's config.json and tokenizer files are inspected for hardcoded external URLs, callback hooks, or shell commands.
- **Sandbox Execution:** The base model is loaded in an ephemeral, network-isolated SageMaker notebook instance. A smoke test with synthetic data is performed to observe for unexpected network calls or file system modifications. This sandbox is destroyed after the test.
- **Supply Chain Verification:** The team verifies the model's lineage using a Software Bill of Materials (SBOM) or an AI-BOM if available. They cross-reference training data sources disclosed in the model card for known problematic datasets (e.g., LAION-5B in its raw form, which is banned due to CSAM concerns).

### 5.2 Model Evaluation and Selection (The "Greenlight" Review)

Once a model passes the Initial Security Screening, the AI/ML Engineering Lead schedules a "Greenlight Review" with the AI-GC subcommittee.

**Step 5.2.1: Prepare the Model Comparison Matrix**
A matrix comparing the shortlisted models must be presented, containing:
- **Benchmark Performance:** Results on domain-specific benchmarks (e.g., MedQA, USMLE) and general benchmarks (e.g., MMLU, TruthfulQA), clearly delineated.
- **Bias Audit Results:** Base model bias audit findings using the Meridian Fairness Toolkit (SOP-AIML-012) across demographic axes relevant to the use case (race, gender, age, geography).
- **License Analysis:** A summary from General Counsel on the license compatibility with Meridian's commercial SaaS model.
- **Computational Cost Estimate:** Total cost of ownership (TCO) projection for fine-tuning on a Meridian-standard GPU cluster (p4d.24xlarge) for the target number of epochs.
- **Risk Assessment:** A preliminary score on the Meridian MRL matrix (SOP-AIML-001), considering factors like model hallucination rates and data provenance transparency.

**Step 5.2.2: Greenlight Review Meeting**
The AI-GC subcommittee (minimum: CAIO Marcus Rivera, VP of Engineering David Park, CISO Rachel Kim, General Counsel Maria Gonzalez) reviews the matrix. The meeting has the authority to:
- **Approve:** One model is selected for Proof-of-Concept (PoC) fine-tuning.
- **Request Modifications:** e.g., "Approve Model X, but only after additional red-teaming."
- **Reject:** All models on the list are deemed unsuitable.

**Decision Logging:** The decision, rationale, and any conditions of approval are logged in the Model Risk Register (ServiceNow GRC) by the CCO, Thomas Anderson. The selected model receives a unique `FOUNDATION_MODEL_ID`.

### 5.3 Fine-Tuning and Transfer Learning Execution

This procedure applies to all forms of transfer learning within the Meridian SaaS Platform’s VPC.

**Step 5.3.1: Data Preparation and Isolation**
The Data Steward assigned to the project must prepare the fine-tuning dataset in accordance with SOP-DATA-005 (Data Handling for AI/ML).
- **Anonymization:** All direct and indirect identifiers must be removed or tokenized. For clinical data used to train high-risk models, the DPO must sign off on the de-identification protocol, confirming it meets GDPR Recital 26 standards.
- **Data Segregation:** The fine-tuning dataset must reside in a dedicated, encrypted S3 bucket with a lifecycle policy that restricts access to the specific SageMaker Training Job IAM role only. No cross-project data mixing is permitted.
- **Data Formatting:** Data must be formatted into the exact tokenizer structure required by the foundation model (e.g., ChatML, Alpaca template). A validation script, checked into the project's Git repository, must confirm zero formatting errors before training begins.

**Step 5.3.2: Environment Configuration**
The VP of IT Operations (Samantha Torres) ensures that the SageMaker training environment is provisioned with these mandatory configurations, which are audited automatically by AWS Config Rules:
1.  **Network Isolation:** The training job runs in a private subnet with no internet gateway. Egress traffic is routed through a Squid proxy that enforces an allowlist of only approved package repositories (PyPI mirror, Conda mirror, approved external API endpoints).
2.  **Encryption:** All data volumes (EBS) and model artifact storage (S3) are encrypted using AWS KMS Customer-Managed Keys (CMKs). Key access is logged via AWS CloudTrail.
3.  **Immutability Check:** A pre-training container init script verifies the SHA-256 hash of the base FM weights against the trusted hash recorded during the Greenlight Review. If the hashes do not match, the job is immediately aborted, and an alert is sent to the CISO via PagerDuty.

**Step 5.3.3: Parameter-Efficient Fine-Tuning (PEFT) Mandate**
To mitigate catastrophic forgetting and reduce the attack surface for weight injection, all fine-tuning shall utilize PEFT methodologies by default.
- **Default Method:** LoRA (Low-Rank Adaptation) on the attention projection layers is the standard. Full fine-tuning (FFT) is the exception and requires a separate exception request (see Section 8), as it represents a higher risk of data memorization and catastrophic forgetting.
- **Hyperparameter Tracking:** All hyperparameters (learning rate, rank `r`, alpha, dropout, number of epochs) must be logged to MLflow with the `FOUNDATION_MODEL_ID` tag.
- **Checkpointing:** Checkpoints saved every N steps must include not just the LoRA adapter weights, but also a snapshot of the optimizer state, enabling full replay and audit capability.

**Step 5.3.4: Continuous Evaluation During Training**
The training pipeline, orchestrated by Kubeflow, includes a sidecar evaluation process:
- **Metrics:** Training and validation loss are tracked. For clinical models, a domain-specific metric (e.g., sensitivity, specificity on a hold-out set) is computed after every epoch.
- **Catastrophic Forgetting Monitor:** A separate "world knowledge" hold-out set, containing general benchmarks (a subset of MMLU), is evaluated concurrently. A drop of more than 15% in this score relative to the base model triggers an automated warning to the Engineering Lead. A drop of more than 30% causes the training job to pause, as this indicates severe knowledge degradation unacceptable for a production system.
- **Emergent Toxicity Check:** Every 500 steps, an internal toxicity classifier (a fine-tuned RoBERTa-based model) scores 1000 generated outputs. A statistically significant increase in the toxicity rate triggers an alert and a manual review.

**Step 5.3.5: Model Registration and Staging Promotion**
Upon successful training completion, the AI/ML Engineering Lead must register the final model in the MLflow Model Registry.
- **Registration Artifacts:** The registration must include the adapter weights, the full training dataset's provenance summary (but not the raw data itself), the training metrics log, and a signed, comprehensive **Model Card**.
- **Model Card Content (EU AI Act Annex IV Alignment):**
    - Intended purpose and intended users.
    - List of geographic regions and demographic groups validated.
    - Performance metrics, including accuracy, robustness, and known limitations.
    - Bias audit results from the Meridian Fairness Toolkit.
    - Levels of accuracy, robustness, and cybersecurity against which the model was tested and can be expected to perform.
    - Known or foreseeable circumstances that may impact performance.
    - A copy of the "human oversight mechanism" workflow diagram.
- **Staging Promotion:** A model can only be promoted from `Development` to `Staging` once the Model Card is reviewed and digitally signed by both the CAIO (Marcus Rivera) and the CISO (Rachel Kim).

### 5.4 Deployment and Human Oversight

This section applies to deploying the fine-tuned adapter into a live inference endpoint within the Meridian SaaS Platform.

**Step 5.4.1: Adversarial Red-Teaming**
Before production deployment, a designated red team from the CISO’s office, independent from the development team, must perform a structured adversarial attack on the staging endpoint:
- **Prompt Injection:** Attempts to jailbreak or bypass system prompts.
- **Data Extraction:** Attempts to retrieve PHI or PII from the fine-tuning dataset by crafting specific queries.
- **Adversarial Perturbations:** For vision models, input images modified with FGSM or PGD attacks to assess robustness.

The red team’s report, with a severity score for each vulnerability found, is reviewed during the production readiness assessment. Only models achieving a "Low" or "Acceptable" risk rating may proceed.

**Step 5.4.2: Configuration of Human Oversight (EU AI Act Article 14)**
For high-risk AI systems within Clinical AI Platform and specific HealthPay credit decisioning models, a human oversight interface must be configured.
- **Clinical Workflow Integration:** The model's prediction (e.g., a diagnostic suggestion) is displayed within the hospital's EHR interface with a confidence score and a link to the relevant Model Card. The “decision-override” button must be prominently displayed.
- **Record Keeping:** All instances of a human operator overriding the model’s output must be logged to the `ai_oversight_logs` database, recording the operator’s ID, timestamp, original model output, and the final human decision. This log is auditable by the Chief Medical Officer (Dr. Priya Patel).
- **Financial Workflow Integration (SR 11-7):** For credit scoring models, an "adverse action" code must be attributed to the model if it contributes more than 25% weight to a denial decision. This ensures compliance with explainability requirements in lending decisions.

**Step 5.4.3: Canary Deployment**
All new model versions must follow a canary deployment strategy via the gateway layer (AWS API Gateway / MLflow Serving):
1.  **Phase 1:** Route 5% of inference traffic to the new model version for a minimum of 24 hours.
2.  **Monitoring Period (See Section 6):** Compare business KPIs and model drift metrics for the canary versus the baseline model.
3.  **Ramp-Up:** If all metrics are within acceptable bounds, traffic is increased to 33%, then 66%, and finally 100% over a 72-hour period. Any critical alert automatically rolls back traffic to the baseline model.

### 5.5 Prohibited Practices

The following activities are strictly prohibited and constitute a violation of this SOP, subject to disciplinary action:

1.  **Shadow AI:** Downloading or using any foundation model from a non-approved source (e.g., personal HuggingFace accounts, torrents) on a Meridian-managed device or within Meridian's cloud infrastructure. Our endpoint detection and response (EDR) tool (CrowdStrike) is configured to alert on the download of known weight file extensions (`.safetensors`, `.pt`, `.bin` > 100MB).
2.  **Unauthorized Data Transmission:** Inputting any PHI, PCI, or proprietary Meridian source code into a public-facing inference endpoint, including ChatGPT, Claude 3, or Gemini via their standard web UIs, for the purpose of prompt engineering or evaluation. A separate, approved environment for evaluating non-PHI data via APIs (with legal and security review) is available upon request.
3.  **License Violations:** Using a model with a restrictive license in a product or feature without explicit written approval from General Counsel.
4.  **Unattended Automation:** Deploying any foundation model as a fully autonomous agent without a human-in-the-loop, where the model’s output directly triggers an irreversible clinical action or a financial transaction exceeding $50,000, without an explicit exception from the AI-GC.

## 6. Controls and Safeguards

Meridian implements a defense-in-depth control framework to enforce the policies in this SOP.

### 6.1 Technical Controls

| Control ID | Control Name | Description | Implementation |
| :--- | :--- | :--- | :--- |
| **FM-T01** | Model Origin Verification | Validate the cryptographic provenance of all base model weights. | Automated SHA-256 hash check in the training pipeline init script. Hash values are stored in the AI Model Registry and compared during deployment. |
| **FM-T02** | Network Air-Gapping for Training | Isolate all fine-tuning workloads from the public internet. | All SageMaker training jobs run in a VPC private subnet. A Squid proxy with a strict allowlist restricts egress. AWS Network Firewall blocks all other outbound connections. |
| **FM-T03** | PHI De-identification Enforcement | Automatically detect and block the inclusion of PHI in fine-tuning datasets. | AWS Macie is configured to scan fine-tuning S3 buckets. A pre-training script validates that the dataset passes a PHI regex and context-based classifier. Training aborts if the fail rate exceeds 0.01%. |
| **FM-T04** | Dynamic Model Scanning | Real-time detection of anomalous model behavior post-deployment. | An inference-time guardrail, implemented via a sidecar proxy (based on NVIDIA NeMo Guardrails), scans all inputs and outputs for patterns of data leakage, prompt injection, and toxic generation. High-severity violations block the response and return a standard error code. |
| **FM-T05** | Immutable Model Storage | Prevent tampering with model artifacts. | S3 Object Lock in governance mode is applied to the model registry bucket. No overwrite or delete operations are permitted for versioned model packages without multi-person approval. |

### 6.2 Administrative and Procedural Controls

| Control ID | Control Name | Description | Implementation |
| :--- | :--- | :--- | :--- |
| **FM-A01** | AI Model Inventory | Maintain a complete, accurate, and continuously updated inventory of all FMs. | All models, from PoC to production, are recorded in the MLflow Model Registry and the ServiceNow CMDB. Monthly reconciliation is performed against running SageMaker endpoints. |
| **FM-A02** | AI-BOM Requirement | Require a machine-readable Software Bill of Materials for AI models. | The procurement or selection of any new FM must include a CycloneDX-format AI-BOM. If the supplier cannot provide one, an exception must be filed, and a manual SBOM generation from the model card is required. |
| **FM-A03** | Segregation of Duties | Separate the functions of model development, model validation, and model release management. | Developers can submit models to staging. The AI Governance Committee (validation) approves the model card. The VP of Engineering (David Park) and CAIO (Marcus Rivera) must jointly approve the production release button in the CI/CD pipeline. |
| **FM-A04** | Third-Party API Approval | Control and govern the use of external AI APIs to prevent data leakage. | The use of any external, black-box inference API (e.g., OpenAI) must be approved by the CISO, DPO, and General Counsel. Only APIs within the scope of a BAA and DPA are considered. The OWASP Top 10 for LLM Applications must be covered. |

## 7. Monitoring, Metrics, and Reporting

Continuous monitoring is instrumental to the responsible scaling of foundation models. The AI/ML Engineering team and CISO use the following metrics, which are displayed on a real-time observability dashboard in Datadog.

### 7.1 Key Performance Indicators (KPIs)

**Data Drift and Model Health (Monitored in Datadog, traced in LangSmith)**
- **Embedding Distribution Drift:** The Wasserstein distance between the embedding vectors of the reference data distribution and the live traffic distribution. Alert threshold: p-value < 0.05 for a maximum mean discrepancy test.
- **Hallucination Rate (RAG Systems):** The percentage of output tokens identified as ungrounded relative to the retrieved context. A custom hallucination detection model, validated on a per-use-case basis, runs on a sampled subset of inferences. Alert threshold: > 5% hallucination rate in a rolling 1-hour window.
- **Inference Latency (p95/p99):** Measured in milliseconds. SLA: 200ms p95 for clinical diagnostic models, 500ms p95 for MedInsight analytics models.
- **Token Generation Toxicity:** The Toxicity Score (0-1) from our internal guardrail classifier. Alert threshold: 30-day rolling average > 0.02, or any single score > 0.8 (immediate alarm to Security Operations Center).

**Security and Supply Chain (Monitored by CISO/Rachel Kim's team)**
- **New Critical CVE Sighting:** Any new, critical vulnerability applicable to a deployed FM or its core dependency (e.g., PyTorch, vLLM, Transformers). Mean Time to Remediation (MTTR): 72 hours for critical CVEs.
- **Unauthorized Model Download Attempts:** Count of alerts per month from CrowdStrike on the `ML_WEIGHT_DOWNLOAD` rule.

**Governance and Operations**
- **Model Inventory Freshness:** Percentage of models in MLflow with a Model Card reviewed within the last 6 months. Target: 100%.
- **Outstanding SOP Exceptions:** Number of active, approved exceptions. Reviewed at each monthly AI-GC meeting.

### 7.2 Reporting Cadence

| Report | Audience | Frequency | Owner |
| :--- | :--- | :--- | :--- |
| **AI System Dashboard** | AI-GC, CISO, VP of Engineering | Real-time (24/7) | N/A (automated via Datadog) |
| **AI Governance Monthly Report** | AI-GC, CEO (Dr. Chen), Chief Medical Officer (Dr. Patel) | Monthly (1st business day) | CAIO (Dr. Rivera) |
| **Model Risk Register Review** | CCO, Board Audit Committee | Quarterly | CCO (Thomas Anderson) |
| **EU AI Act Compliance Sprint Review** | EU Legal Team, DPO | Weekly (during the sprint, bi-weekly after 2025-08-01) | DPO (Dr. Weber) |
| **Red Team and Adversarial Testing Review** | CISO, VP of Engineering | Per-Promotion Event | CISO (Rachel Kim) |

### 7.3 Key Metrics for EU AI Act Compliance

For high-risk systems, the following metrics are essential for the conformity assessment and post-market monitoring (PMS) plan required by Article 61:
- **Incidence Rate:** Number of serious incidents per 10,000 inferences, where an incident is defined per the EU AI Act Article 3(1)(49a) – a major error or harm-producing event. Target: < 1 per 10,000.
- **Human Override Rate:** The percentage of decisions where a clinician or analyst overrides the model's primary recommendation. This is monitored by Dr. Patel to detect either model degradation or alert fatigue. A sudden 20% swing in this rate triggers a model effectiveness review.

## 8. Exception Handling and Escalation

### 8.1 Exception Types

There are three tiers of exceptions:

- **Technical Exception:** e.g., Request to use full fine-tuning (FFT) instead of mandated PEFT, use of a non-PyPI package during training, or extension of a remediation deadline for a non-critical vulnerability.
- **License Exception:** Request to use a model with an otherwise prohibited license (e.g., a CC BY-NC-SA model for a purely internal research tool).
- **Strategic Exception:** Request to use a black-box third-party API (e.g., for evaluating a new model against held-out PHI data) or to deploy a fully autonomous agent for transactions > $50,000.

### 8.2 Exception Request Process

1.  **Initiation:** The requestor (AI/ML Engineering Lead) documents the exception in the ServiceNow GRC "SOP Exception" module. The documentation must state the specific SOP section being violated, the business justification, the proposed compensating control, and the requested duration of the exception (not to exceed 90 days).
2.  **Risk Assessment:** The CISO (Rachel Kim) and DPO (Dr. Klaus Weber) append their technical risk and privacy assessments, respectively.
3.  **Approval Workflow:**
    - *Technical Exception*: Approval by VP of Engineering (David Park).
    - *License Exception*: Approval by General Counsel (Maria Gonzalez).
    - *Strategic Exception*: Joint approval by CAIO (Marcus Rivera) and CEO (Sarah Chen).
4.  **Tracking and Expiry:** All exceptions are tracked in the Model Risk Register. Three days before the expiration date, the system sends automated reminders to the requestor and approver. Failure to close or renew an exception triggers an automatic escalation to the Chief Compliance Officer.

### 8.3 Escalation Protocol for Emergent Critical Risks

If a real-time monitoring alert indicates a severe, active risk (e.g., spike in data leakage detections in a production endpoint):

1.  **Immediate Action (5 minutes):** The on-call Site Reliability Engineer (SRE) has the authority to trigger a "Kill Switch" (a blue/green deployment rollback to a null-returning safe endpoint) for the specific model endpoint, without prior management approval. This is a pre-authorized break-glass procedure.
2.  **Incident Declaration (15 minutes):** The SRE declares a Severity 1 incident in PagerDuty. The CISO, CAIO, and VP of Engineering are paged immediately.
3.  **Post-Mortem (24 hours):** The incident commander (typically the CAIO) leads a post-mortem analysis. The model is not reinstated until the root cause is identified, a permanent fix is deployed, and the CISO co-signs a "Return to Service" request.

## 9. Training Requirements

To ensure all relevant personnel are proficient in the execution of this SOP, the following training is mandatory.

| Training Module ID | Training Title | Audience | Frequency | Provider |
| :--- | :--- | :--- | :--- | :--- |
| **T-AIML-015.1** | SOP-AIML-015: FM Standards for Engineers | All AI/ML Engineering staff, including contractors | **Annual** (and within 30 days of hire) | Internal (LMS - Docebo) |
| **T-AIML-015.2** | Foundation Model Supply Chain & License Awareness | All AI/ML Engineering staff, Product Managers, Procurement | **Annual** | CISO & General Counsel (Joint Webinar) |
| **T-AIML-015.3** | EU AI Act & High-Risk Systems for AI Developers | All AI/ML staff working on Clinical AI Platform | **Bi-Annual** | External Legal Partner & CCO |
| **T-AIML-015.4** | Adversarial Red-Teaming for Foundation Models | Dedicated Red Team members in CISO office | **Quarterly** (updates on latest tactics) | External Cybersecurity Firm |
| **T-AIML-015.5** | Human Oversight and Override Procedures | Clinicians (through CMO) & Credit Analysts (through VP of Finance) | **Annual** | Business Unit Leads |

**Training Metrics:** The Chief Compliance Officer tracks:
- **Completion Rate:** > 95% within the assigned window. Non-compliance triggers a notification to the employee’s manager and the CCO.
- **Assessment Scores:** Each module has a post-training quiz with a passing score of 80%. Scores, timestamps, and completion status are recorded in the employee's permanent HR file via the LMS.

## 10. Related Policies and References

### 10.1 Internal Meridian Policies

| SOP ID | Policy Name |
| :--- | :--- |
| SOP-AIML-001 | ML Model Risk Management Framework |
| SOP-AIML-003 | Traditional Machine Learning Model Lifecycle |
| SOP-AIML-010 | Model Cards and AI Documentation Standards |
| SOP-AIML-012 | AI Fairness, Bias, and Ethics Control Standard |
| SOP-DATA-005 | Data Handling and Sanitization for AI/ML |
| SOP-IS-020 | Vulnerability and Patch Management for AI Assets |
| SOP-IT-042 | Acceptable Use of Generative AI Tools |
| SOP-PRIV-008 | Data Protection Impact Assessment (DPIA) Procedure |
| SOP-IR-001 | Security Incident Response and Escalation |
| SOP-VEND-009 | Third-Party AI Risk and Compliance Management |

### 10.2 External Standards and Regulations

- **EU AI Act (Regulation (EU) 2024/1689):** Articles 3 (Definitions), 9 (Risk Management System), 13 (Transparency), 14 (Human Oversight), 15 (Accuracy, Robustness, and Cybersecurity), 61 (Post-Market Monitoring), and Annex IV (Technical Documentation).
- **NIST AI RMF 1.0:** Govern, Map, Measure, and Manage functions. Specific sections referenced in this SOP include Map 2.1 (Context), Map 3.2 (Known Capabilities), Measure 2.10 (Teaming), and Manage 4.3 (Risk Transfer).
- **Model Risk Management (SR Letter 11-7 / OCC 2011-12):** Federal Reserve guidance on model risk management, including standards for model validation, governance, and documentation for financial models in HealthPay.
- **HIPAA Security Rule:** 45 CFR § 164.312 (Technical Safeguards) for access control, audit controls, and integrity controls to protect PHI used in AI models.
- **SOC 2® (System and Organization Controls):** Specifically, the Common Criteria of Change Management (A1), Logical and Physical Access Controls (A2), and System Operations (A3) govern the CI/CD pipeline, deployment, and monitoring described in this SOP.
- **OWASP Top 10 for LLM Applications:** Guiding security technical controls in Section 6.1.

## 11. Revision History

| Version | Date | Author | Summary of Changes |
| :--- | :--- | :--- | :--- |
| 1.0 | 2023-03-15 | Dr. Jane Roe (former CAIO) | Initial version. Focus on basic model selection criteria for early-stage LLM explorations. |
| 2.2 | 2023-09-22 | Dr. Marcus Rivera | Added comprehensive Section 6 (Controls) to address growing SaaS compliance requirements. Introduced Greenlight Review process. |
| 3.0 | 2024-01-10 | Dr. Marcus Rivera | Major revision to align with the provisional text of the EU AI Act. Introduced the concepts of high-risk classification and the mandatory Human-in-the-Loop (HITL) override. |
| 3.5 | 2024-07-08 | Dr. Marcus Rivera | Post-CE marking update. Incorporated post-market monitoring (PMS) metrics from MDR and final EU AI Act text (Regulation 2024/1689). Added AI-BOM (SBOM for AI) requirements to the Greenlight review. |
| 4.0 | 2025-02-01 | David Park | Technical rewrite of Section 5.3: mandated PEFT as the default fine-tuning strategy, introduced catastrophic forgetting monitoring metrics. Added Section 5.5 (Prohibited Practices) post an internal shadow-AI incident. |
| 4.8 | 2025-11-24 | Dr. Marcus Rivera | Current version. Full alignment with the NIST AI RMF 1.0, formalizing the RACI matrix. Added detailed Canary Deployment procedures (Section 5.4.3). Updated OWASP LLM Top 10 references. Approved by David Park and Dr. Sarah Chen. |