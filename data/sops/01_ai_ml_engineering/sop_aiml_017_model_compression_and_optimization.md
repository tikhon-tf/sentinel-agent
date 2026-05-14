---
sop_id: "SOP-AIML-017"
title: "Model Compression and Optimization"
business_unit: "AI/ML Engineering"
version: "1.1"
effective_date: "2024-02-16"
last_reviewed: "2025-04-21"
next_review: "2025-10-02"
owner: "Dr. Marcus Rivera, Chief AI Officer"
approver: "David Park, VP of Engineering"
classification: "Internal"
regulations:
  - "EU AI Act"
  - "NIST AI RMF"
status: "Active"
---

# Standard Operating Procedure: Model Compression and Optimization

## 1. Purpose and Scope

### 1.1 Purpose

The purpose of this Standard Operating Procedure (SOP) is to establish a standardized, auditable, and compliant framework for the compression and optimization of machine learning models developed, deployed, or maintained by Meridian Health Technologies, Inc. Model compression techniques—including quantization, pruning, and knowledge distillation—are essential for deploying performant AI systems within the computational, latency, and resource constraints of clinical and financial production environments. This document ensures that optimized models maintain their safety, efficacy, and regulatory compliance post-compression, adhering strictly to the requirements for high-risk AI systems under the EU AI Act and the internal risk management principles derived from our governing frameworks.

### 1.2 Scope

This SOP applies to all personnel within the AI/ML Engineering business unit and any cross-functional team members involved in the lifecycle of an AI/ML model, from design to decommissioning. Its requirements are mandatory for any model undergoing a compression technique before deployment or redeployment in a production environment.

**In Scope:**
- All models classified as **High-Risk AI Systems** under Annex III of the EU AI Act, specifically those deployed within the **Clinical AI Platform** (e.g., patient risk scoring, diagnostic imaging analysis, adverse event prediction).
- All models used in the **HealthPay Financial Services** business line subject to SR 11-7 model risk management guidance, including credit scoring, fraud detection, and medical lending models.
- All models processing **Protected Health Information (PHI)** under HIPAA within the MedInsight Analytics and Meridian SaaS platforms.
- All newly developed and legacy models undergoing optimization to improve inference latency, reduce cloud computing costs, or enable edge deployment (e.g., on-premise hospital servers).
- The full suite of compression techniques: **post-training quantization, quantization-aware training (QAT), unstructured and structured pruning, and knowledge distillation.**

**Out of Scope:**
- Preliminary feasibility studies or exploratory research conducted with synthetic, non-production data in isolated sandbox environments (e.g., a SageMaker notebook not connected to a Kubeflow pipeline).
- Hyperparameter tuning that does not fundamentally alter the model's learned parameters or architecture (standard training covered by SOP-AIML-004, *Model Training and Experiment Tracking*).
- Feature engineering and input data pipelines (covered by SOP-DE-001, *Data Engineering and Feature Store Management*).

### 1.3 Applicability

This SOP is binding upon the following roles: Chief AI Officer (CAIO); VP of Engineering; AI/ML Team Leads; ML Engineers; Data Scientists; Clinical Data Scientists; MLOps Engineers; Quality Assurance (QA) validators; and members of the AI Ethics and Compliance Review Board. Non-compliance shall be managed per the Exception Handling and Escalation process defined in Section 8.

---

## 2. Definitions and Acronyms

### 2.1 Definitions

| Term | Definition |
| :--- | :--- |
| **Calibration Data** | A representative, statistically-distributed subset of the original training data or held-out validation dataset, typically 500–2000 samples, used strictly to calibrate scaling factors during post-training quantization. |
| **Performance Parity Threshold** | The predefined, metric-specific maximum allowable degradation in a compressed model’s performance relative to its uncompressed baseline, as determined by the Pre-Compression Validation Baseline (PCVB). |
| **Pre-Compression Validation Baseline (PCVB)** | A comprehensive suite of quantitative performance, safety, and fairness metrics run on the fully-trained, uncompressed "teacher" or base model. This serves as the formal yardstick for all post-compression validation. |
| **Pruning (Structured)** | A compression technique that removes entire architectural substructures (e.g., attention heads, convolutional filters, layers) from a model, resulting in direct, predictable inference speedups on standard hardware. |
| **Pruning (Unstructured)** | A technique that sets individual, less-salient model weights to zero, creating a sparse matrix. Requires specialized hardware or software runtimes for effective speedups. |
| **Quantization** | A technique to reduce the numerical precision of a model’s weights and/or activations (e.g., from FP32 to INT8), resulting in smaller model size and faster inference on compatible hardware. |
| **Teacher-Student Model** | The architectural paradigm for knowledge distillation. The "teacher" is the large, uncompressed source model. The "student" is the smaller, compressed target model trained to mimic the teacher's output distribution. |

### 2.2 Acronyms

| Acronym | Definition |
| :--- | :--- |
| **AUPRC** | Area Under the Precision-Recall Curve (primary metric for imbalanced clinical datasets) |
| **AUROC** | Area Under the Receiver Operating Characteristic curve |
| **BCE** | Balanced Cross-Entropy |
| **CAIO** | Chief AI Officer (Owner) |
| **CCB** | Clinical Compliance Board |
| **CMR** | Compressed Model Registry (within MLflow) |
| **ECRB** | AI Ethics and Compliance Review Board |
| **HDI** | High-Risk Dataset Inventory |
| **KD** | Knowledge Distillation |
| **MAE** | Mean Absolute Error |
| **MER** | Medication Error Rate (a clinical safety metric) |
| **MLIR** | MLflow Instance Registry (Meridian's MLflow tracking server) |
| **PCVB** | Pre-Compression Validation Baseline |
| **PTQ** | Post-Training Quantization |
| **QAT** | Quantization-Aware Training |
| **RMSE** | Root Mean Squared Error |
| **TIR** | Technical Implementation Review |

---

## 3. Roles and Responsibilities

The following RACI matrix assigns accountability for the critical tasks detailed in this SOP.

| Task / Activity | CAIO (M. Rivera) | VP of Eng (D. Park) | AI/ML Team Lead | ML Engineer / Data Scientist | MLOps Engineer | QA Validator | ECRB |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Strategic Approval for New Compression Technique** | A | R | C | I | I | I | C |
| **Selection of Compression Candidate & Technique** | I | A | R | C | C | I | C |
| **Execution of PCVB** | I | I | A | R | C | C | I |
| **Execution of Compression Procedure** | I | I | A | R | C | I | I |
| **Post-Compression Technical & Safety Validation** | I | I | A | R | C | R | I |
| **Regulatory Compliance Package Preparation (EU AI Act Anx IV)** | A | R | R | C | C | C | C |
| **Final Sign-Off for Clinical/Regulated Deployment** | A | R | C | I | I | I | R |
| **CMR Entry and Model Card Update** | I | I | R | C | R | I | I |
| **Monitoring and Incident Escalation (Post-Deployment)** | I | R | A | C | R | I | I |

**Key:** R = Responsible (executes), A = Accountable (final sign-off), C = Consulted, I = Informed.

---

## 4. Policy Statements

Meridian Health Technologies establishes the following non-negotiable policy commitments for all model compression activities:

- **P01: Uncompromised Clinical Safety.** No compression technique shall be applied if the resulting student or pruned model fails to meet the clinical safety thresholds defined in its original conformity assessment under the EU Medical Device Regulation (MDR) and EU AI Act, Article 9. Safety is the paramount, non-negotiable metric.

- **P02: Mandatory Pre-Compression Baseline.** A formal Pre-Compression Validation Baseline (PCVB) must be established, peer-reviewed, and digitally signed in the Meridian MLIR before any compression procedure is initiated. No model shall be compressed without a corresponding, approved PCVB.

- **P03: Audit Trail Integrity.** Every artifact, dataset, configuration file, and metric generated during the compression process, from PCVB to final validation, must be immutably logged in the MLIR and linked to the compressed model in the Compressed Model Registry (CMR). The lineage from uncompressed teacher to compressed student must be unambiguous.

- **P04: Traceable Technical Documentation.** For all high-risk AI systems, compression activities shall generate a supplement to the model’s technical documentation, as required by EU AI Act Annex IV. This supplement shall detail the rationale, methodology, and validation outcomes.

- **P05: Human Oversight.** No compressed high-risk AI model shall be promoted to production without a final documented sign-off by a qualified human validator (the QA Validator role) who has verified the absence of critical performance regressions, as defined in the Detailed Procedures.

---

## 5. Detailed Procedures

This section outlines the step-by-step procedures for each main compression technique, the post-compression validation, and the production promotion process. The procedures serve as a formal operating model to ensure standardized, repeatable, and compliant execution.

### 5.1 General Pre-Compression Procedure (PR-COMP-001)

This procedure is mandatory for all techniques before any specific work begins.

1.  **Candidate Nomination and Justification:**
    - The **AI/ML Team Lead** nominates a model for compression, completing Form `COMP-01 Candidate Justification` in the Meridian AI/ML Confluence space.
    - The form must state the business justification (e.g., "Reduce inference latency for Clinical Platform Model `risk-calc-v3` from 150ms to <50ms on T4 GPU to meet clinician-facing SLA") and the proposed technique (e.g., Structured Pruning + INT8 QAT).

2.  **Data Sourcing and Sanitization:**
    - The **ML Engineer** identifies and sources a representative dataset for calibration (for PTQ) or fine-tuning (for QAT, pruning retraining, and KD), drawing from the *High-Risk Dataset Inventory (HDI-04)*, ensuring no data leakage from production hold-out sets.
    - PHI must be de-identified according to SOP-DE-003 (*Data De-identification for ML Workflows*) unless operating in the secure, air-gapped HIPAA production enclave.

3.  **PCVB Establishment and Formalization:**
    - The **ML Engineer** computes the PCVB by running the uncompressed model against the full official validation and test sets. The PCVB includes, at minimum, 6 metrics defined in Section 7.1.
    - The **AI/ML Team Lead** conducts a Technical Implementation Review (TIR) of the PCVB. The TIR verifies that the chosen metrics and baselines are accurate, properly measured, and clinically/business relevant. Upon approval, the Team Lead digitally signs the baseline run artifact within the MLIR, locking it as the reference point.

### 5.2 Quantization Procedures

Quantization reduces model numerical precision. Two methods are permitted, selected based on acceptable accuracy trade-offs.

#### 5.2.1 Post-Training Quantization (PTQ)

PTQ is the less-expensive technique, suitable when a small accuracy drop is permissible per the performance parity thresholds.

1.  **Hardware Target Specification:** The MLOps Engineer specifies the target deployment hardware's inference runtime (e.g., NVIDIA Triton Inference Server with TensorRT, ONNX Runtime on Intel CPU) in the `COMP-01` form. The quantization scheme (e.g., per-tensor symmetric INT8 for weights, per-token asymmetric INT8 for activations) must be compatible with this target.
2.  **Calibration Data Loading:** The ML Engineer loads the representative calibration dataset—typically 500-1000 random samples from the training distribution's validation set—into a purpose-built SageMaker processing job or Kubeflow pipeline step.
3.  **Static Quantization Application:** Using the target runtime's tools (e.g., TensorRT’s `trtexec` or PyTorch’s `quantization.fx`), the engineer applies static PTQ, where the calibration data is used to compute the optimal quantization parameters (scale and zero-point) for activations at each node.
4.  **Quantized Model Export:** The compressed model is exported to the MLIR as a versioned artifact in standard format (`model_v2_qat_int8.onnx`), tagged with `stage: quantization`.

#### 5.2.2 Quantization-Aware Training (QAT)

QAT is mandatory when PTQ fails to meet the Performance Parity Thresholds. It simulates quantization during a fine-tuning phase, allowing the model to adapt its parameters to the precision loss.

1.  **QAT Training Loop Insertion:** The ML Engineer modifies the uncompressed model's graph by inserting "fake-quantization" nodes before computationally intensive layers (e.g., multi-head attention, feed-forward networks).
2.  **Fine-Tuning Execution:** The model is fine-tuned using the uncompressed teacher model's logits as soft targets (integrating a KD-style loss if beneficial) against the full sanitized training dataset. The training objective combines the primary clinical/cost loss function with a quantization-aware regularization term.
3.  **Convergence Check:** Training logs are monitored in MLflow. The QAT job must converge—measured by a delta in validation loss less than 0.001 over 500 training steps—before exporting. If convergence fails, the **AI/ML Team Lead** is notified to re-evaluate the approach.

### 5.3 Pruning Procedure

Pruning eliminates redundant or non-salient parameters.

#### 5.3.1 Unstructured Pruning
1.  **Salience Criterion Selection:** The ML Engineer selects a weight salience criterion (e.g., magnitude, approximated Taylor expansion). Magnitude-based L1-norm pruning is the standard.
2.  **Gradual Pruning Schedule:** A polynomial decay pruning schedule is applied over a full re-training cycle. Starting from sparsity `s_i=0%`, sparsity increases to the target `s_f` (e.g., 80%) over `n` steps, defined by: `s_t = s_f + (s_i - s_f) * (1 - (t / n))^3`.
3.  **Mask Application and Re-Training:** The pruning mask is applied, zeroing out low-magnitude weights. The resulting sparse model is re-trained on the full training dataset to recover lost accuracy.
4.  **Format Export:** The sparse model is exported in a dense format for compatibility or a framework-native sparse format, explicitly documented. The primary export is via TorchScript or ONNX with explicit handling of the zero-masked weights.

#### 5.3.2 Structured Pruning (Head and Layer Removal)
This is the recommended technique for latency-critical Clinical AI systems due to its direct, predictable hardware benefits.

1.  **Component Salience Scoring:** An evaluation script systematically ablates structural components. For a Transformer model, the script iteratively removes individual attention heads and feed-forward network (FFN) filter blocks from each layer, measuring the resulting drop in a primary clinical metric (e.g., AUPRC) on a held-out validation set. The output is a *Component Salience Map*.
2.  **Retention Threshold Definition:** The **AI/ML Team Lead**, in consultation with a Clinical Safety SME, defines a retention threshold based on the Component Salience Map. For example: "Retain all heads whose ablation causes >0.5% reduction in AUPRC."
3.  **Sub-Structure Removal:** The ML Engineer programmatically removes the non-salient attention heads and filters from the model graph at every layer, producing a thinner, uniformly accelerated model.
4.  **Post-Prune Fine-Tuning:** This structurally-modified model undergoes a full fine-tuning procedure identical to the standard training process (SOP-AIML-016), using the original uncompressed model's logits as soft targets (a "soft" knowledge distillation stage).

### 5.4 Knowledge Distillation Procedure

Distillation is the preferred method when a drastic architectural change is required (e.g., deploying a complex Risk Calc model from an A100 cluster to a CPU-only clinical workstation).

1.  **Student Model Architecture Design:** The ML Engineer designs a student architecture. The design is documented in a *Student Model Architecture Justification* note, explaining the trade-offs between expressivity (layers, hidden dimensions) and target hardware latency budget.
2.  **Teacher-Student Transfer Setup:** The uncompressed "teacher" model's weights are frozen. The student model is initialized randomly.
3.  **Multi-Objective Loss Construction:** The training objective is a composite loss: `L_total = α * L_hard(student_output, ground_truth_label) + β * L_soft(student_logits, teacher_logits, temperature)`. Here, `L_hard` is the standard BCE loss, `L_soft` is the KL divergence between softened probability distributions, and the hyperparameter `α, β, temperature` are tuned and logged.
4.  **Distillation Training:** The student model is trained using this multi-objective loss on the full training dataset. Training logs are monitored in MLflow until performance on the validation set plateaus.

### 5.5 Unified Post-Compression Validation (PR-VAL-005)

This procedure is applied identically and rigorously to every compressed model, regardless of the technique used.

1.  **Automated Metric Execution:** The MLOps pipeline automatically executes the compressed model against the **exact same held-out production test set** used in the PCVB. It computes all metrics defined in Section 7.1.
2.  **Performance Parity Gate:** The pipeline automatically compares each metric against the PCVB, applying the thresholds defined in Table 1.
3.  **Failure Handling:**
    - **Automatic Gate Failure:** If the pipeline gate fails, a `CRITICAL` log event is raised. The model artifact is automatically quarantined in the MLIR, and deployment is blocked. The **AI/ML Team Lead** and **QA Validator** are auto-notified via ServiceNow.
    - **Tie-Breaking on Edge Metrics:** If a non-critical metric fails by a margin of ≤ 2% of the threshold, the **AI/ML Team Lead** can initiate a manual review by the full ECRB. This requires submitting a "Performance Deviation Risk Analysis" using Form `COMP-02`.

4.  **Clinical Safety Spot-Check:**
    - The **QA Validator** must independently perform a qualitative spot-check. This is not automated. The validator compares a minimum of 50 randomly selected, difficult test-set samples, comparing the teacher's output, the student's output, and the ground truth label.
    - The focus is on identifying clinically absurd errors (e.g., a Risk Calc model giving a 0% sepsis risk to a patient with a high fever and high WBC count). Any identified instance is a Safety Gate Failure, overriding all quantitative metrics.
5.  **Artifact Registration and Promotion:**
    - Upon passing all gates, the **MLOps Engineer** promotes the compressed model artifact in the CMR from `stage: candidate` to `stage: production-ready`.
    - The model’s MLflow Model Card is automatically supplemented with compression metadata, PCVB link, and validation results, forming the regulatory audit trail per EU AI Act Art. 12.

---

## 6. Controls and Safeguards

### 6.1 EU AI Act: Specific Compliance Controls

These controls are specifically mandated to ensure the compression of high-risk AI systems does not introduce new risks or undermine existing conformity.

#### Control 6.1.1: Technical Documentation Supplement (Ref: Art. 11, Annex IV)
For every high-risk model undergoing compression, a supplement to the technical documentation is a required output. This supplement must be version-controlled and linked to the CMR entry.
- **Required Content:**
    1.  A clear description of the compression methodology, algorithms, and tools.
    2.  The design specifications of the student model or pruned architecture, including a rationale for how the design continues to achieve the intended purpose.
    3.  A detailed log of the training, calibration, and fine-tuning processes, including final hyperparameters.
    4.  The complete PCVB and post-compression validation reports, explicitly highlighting any changes in all measured metrics.
- **Role:** Model Risk Officer (MRO), a designee of the CAIO.
- **Timeline:** Documentation supplement must be completed and linked in the CMR within 5 business days of `production-ready` status.

#### Control 6.1.2: Conformity Re-assessment Gate (Ref: Art. 43)
A material change to a high-risk AI system, including a fundamental algorithmic optimization, may trigger a need for a new conformity assessment. The change is defined as "material" if:
- The architectural change from pruning or distillation results in a >5% degradation in any single secondary clinical safety metric (see Table 1) relative to the PCVB.
- The compression method itself (e.g., QAT) is a new algorithm not covered in the original technical documentation.
- **Gatekeeper:** The Clinical Compliance Board (CCB). No compressed high-risk model can be deployed to Clinical Platform production environments without CCB sign-off, documented via a Jira ticket linked to the model. The SLA for standard CCB review is 10 business days.

#### Control 6.1.3: Record-Keeping and Traceability (Ref: Art. 12)
The Meridian MLflow Instance Registry (MLIR) serves as the system of record. Logging is mandatory and automated for:
- **Event Logging:** Every pipeline step (PCVB, PTQ, Pruning, Validation) must generate an immutable event log in ServiceNow from the Kubeflow pipeline, recording the user, timestamp, dataset/artifact URI, and pass/fail status.
- **Artifact Lineage:** The CMR must maintain a strict lineage graph (`mlflow artifact lineage`) showing the uncompressed teacher model's URI as the `source` of the compressed student model's URI.
- **Retention:** All logs, artifacts, and documentation related to compressed high-risk AI systems must be retained for a period not less than 10 years after the model’s final decommissioning, per EU MDR Annex II, Section 6.4.

### 6.2 Administrative Controls

#### Control 6.2.1: Segregation of Duties in Sign-Offs
The Technical Implementation Review (TIR) and the final Safety Gate validation cannot be performed by the same person. Specifically:
- **AI/ML Team Lead** is a prohibited role for the **QA Validator** on the same project.
- The **CAIO** is the ultimate accountable party, who can override, in writing, a metric-based gate failure with a compensating control documented in a risk management file. This is a `CRITICAL` severity authorization.

#### Control 6.2.2: Access Control and Environment Security
- **Production Artifacts:** The Compressed Model Registry (CMR) is write-only for CI/CD pipelines (the MLOps service account). Manual `put` or `delete` operations on `production-ready` model artifacts are denied for all human user accounts.
- **Data Access:** Access to the HDI-04 calibration and training datasets used in compression must be explicitly granted via the Data Governance Catalogue. Any exfiltration attempt is logged and alerts the Information Security team.

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Quantitative Performance Metrics for Validation Gate

These metrics form the Performance Parity Gate. The pipeline must explicitly fail if a *Primary* metric falls below its threshold or if two or more *Secondary* metrics fall below their respective thresholds.

**Table 1: Performance Parity Thresholds by Metric Class**

| Metric Class | Primary / Secondary | Primary Threshold (Max % Delta from PCVB) | Secondary Threshold (Max % Delta from PCVB) |
| :--- | :--- | :--- | :--- |
| **Discrimination (General)** | Primary | AUROC ≤ -1.5% | |
| **Discrimination (Imbalanced Data)** | Primary | AUPRC ≤ -2.0% | |
| **Calibration** | Secondary | | Expected Calibration Error (ECE) > +2.0% |
| **Clinical Safety Metric** | Primary | (Model-Specific, e.g., MER) ≤ 0.0% (No degradation permitted) | |
| **Regression Accuracy** | Primary | RMSE > +3.0% or MAE > +3.0% | |
| **Business KPI (HealthPay)** | Primary | | Kolmogorov-Smirnov (KS) statistic ≤ -2.5% |
| **Latency** | Secondary | | P95 Latency Reduction < 00% of Target (Must improve) |
| **Model Size** | Secondary | | Size Reduction < 00% of Target (Must improve) |

**Note:** The specific safety metric (e.g., Mortality Rate under curve, False Negative Rate for sepsis) is defined in the model's `model-card.md` and must be referenced during the PCVB step.

### 7.2 KPIs and Dashboards

A live Grafana dashboard (`AIML Model Compression Overview`) will be built to aggregate the following Key Performance Indicators, sourced from the MLflow and ServiceNow logs.

- **Compression Pipeline Success Rate:** (Number of `CRITICAL` Failures in Post-Compression Validation) / (Total Compression Jobs Initiated) * 100.
- **Mean Time to Recovery (MTTR) from Gate Failure:** Average time from pipeline `CRITICAL` failure to either successful re-compression or documented executive exception.
- **Latency Improvement Ratio:** For successful compressions, P95 Inference Latency (Teacher) / P95 Inference Latency (Student).
- **Compliance Lead Time:** Average time in business days from `production-ready` status to CCB final approval, tracked by Jira ticket.
- **Model Cost Per Million (CPM) Inference:** Compute cost per 1,000,000 inferences, measured daily.

### 7.3 Reporting Cadence

- **Automated Alerts:** Any Performance Parity Gate failure generates a `CRITICAL` alert in the #aiml-ops Slack channel and a Priority 1 ServiceNow ticket.
- **Weekly Sprint Report:** The AI/ML Team Lead presents a summary of active and failed compressions during the weekly sprint review.
- **Quarterly Management Review:** The CAIO and VP of Engineering will review the `AIML Model Compression Overview` dashboard and the aggregate KPIs. This review must include an analysis of any trends in clinical safety metric drift and a formal sign-off.

---

## 8. Exception Handling and Escalation

### 8.1 Exception Handling Process

Deviations from this SOP (e.g., deploying a compressed model that failed a non-critical secondary metric by a margin of ≤ 2%) require a formal, documented exception.

1.  **Request Initiation:** The **AI/ML Team Lead** initiates the exception by completing Form `EXC-AIML-017 Exception Request` in the GRC (Governance, Risk, and Compliance) system. The form requires:
    - The specific SOP section from which deviation is sought.
    - A detailed technical justification, including the quantified risk of not compressing vs. deploying a sub-optimal model.
    - A proposed compensating control (e.g., increased human-in-the-loop overrides, more frequent post-market surveillance reports).

2.  **Technical Review:** The **VP of Engineering, David Park**, conducts a technical review, evaluating the justification and the compensating control's feasibility.

3.  **Risk and Compliance Approval:** For all high-risk AI systems, the final approval rests with the **AI Ethics and Compliance Review Board (ECRB)** . The ECRB reviews the technical justification against the Clinical AI Platform's overall risk posture. The ECRB's decision must be documented within the ServiceNow ticket. The SLA for the ECRB to respond to a non-urgent exception is 5 business days.

### 8.2 Emergency Escalation (Urgent Safety Fix)

In the rare event that a model must be compressed and deployed immediately to address a direct, active clinical safety risk (e.g., an uncompressed model hallucinating at an unacceptable rate, and a pruned model is identified as a safer interim solution):

1.  The **CAIO (Dr. Marcus Rivera)** declares a Code Blue via the #incident-response channel. This verbally authorizes the promotion of a `candidate` model to `production`.
2.  The promotion is executed by a single, authorized SRE.
3.  A full retrospective and all missing documentation (PCVB, compliance supplement, ECRB review) must be completed and linked to the incident post-mortem within 72 hours. Failure to do so is an Audit Finding.

---

## 9. Training Requirements

### 9.1 Mandatory Training Curriculum

All personnel listed in the Roles and Responsibilities matrix must complete the following training modules within these timelines:

| Role(s) | Training Module ID | Description | Frequency | Initial Completion SLA |
| :--- | :--- | :--- | :--- | :--- |
| **ML Engineers, Data Scientists** | `TR-COMP-101` | *Hands-on Model Compression Workshop.* Covers QAT, structured pruning, KD using Meridian's standard tools (PyTorch, TensorRT). Includes an evaluated practical lab. | Annually | 60 days from SOP effective date or hire date. |
| **AI/ML Team Leads** | `TR-REG-201` | *Regulatory Compliance for AI Optimization.* In-depth review of EU AI Act Art. 11 & 43 requirements for "material changes," documentation standards per Annex IV. | Annually | 30 days from SOP effective date or hire date. |
| **QA Validators** | `TR-VAL-301` | *Post-Compression Safety Auditing.* Advanced techniques for clinical safety spot-checking, bias evaluation, and edge-case analysis using the "COMP-02" risk analysis framework. | Semi-annually | 45 days from SOP effective date or hire date. |

### 9.2 Tracking and Enforcement
- Training completion is tracked in the Workday Learning Management System.
- Access credentials to the High-Risk Dataset Inventory (HDI-04) and the Meridian MLIR registry are programmatically tied to training compliance. An engineer whose training expires will have their `write` access to the HDI-04 bucket automatically suspended until re-certification.

---

## 10. Related Policies and References

### 10.1 Internal Meridian SOPs

| SOP ID | Document Name |
| :--- | :--- |
| SOP-AIML-001 | *AI Model Lifecycle Management Policy* |
| SOP-AIML-004 | *Model Training and Experiment Tracking* |
| SOP-AIML-009 | *Clinical AI Model Conformity Assessment Procedure* |
| SOP-AIML-022 | *Post-Market Surveillance for AI as a Medical Device* |
| SOP-DE-001 | *Data Engineering and Feature Store Management* |
| SOP-DE-003 | *Data De-identification for ML Workflows* |
| SOP-SEC-015 | *AI/ML Pipeline Service Account and Access Control* |
| SOP-QA-004 | *Independent Quality Assurance Validation Protocol* |

### 10.2 External Standards and Regulations

- **Regulation (EU) 2024/1689** (Artificial Intelligence Act), Titles III and IV, Annex IV.
- **Regulation (EU) 2017/745** (Medical Device Regulation), Annex II.
- **NIST AI 600-1, Artificial Intelligence Risk Management Framework (AI RMF 1.0).**
- **IEC 62304: Medical Device Software - Software Life Cycle Processes**, specifically regarding changes to software items.

---

## 11. Revision History

| Version | Date | Author(s) | Description of Change |
| :--- | :--- | :--- | :--- |
| 0.1 | 2023-12-01 | Jane Roe (Lead MLE) | Initial Draft for internal review. |
| 0.2 | 2024-01-15 | M. Rivera (CAIO) | Refined scope to include HealthPay, added EU AI Act controls, clarified roles matrix. |
| 1.0 | 2024-02-16 | D. Park (VP Eng) | Approved for release. Added formal exception handling and training SLAs. |
| 1.1 | 2025-04-21 | L. Chen (MLOps Lead) | Updated PTQ procedure to use new TensorRT LLM toolkit; updated PCVB metric thresholds based on 2024-year review; revised ECRB escalation SLA from 10 days to 5. |