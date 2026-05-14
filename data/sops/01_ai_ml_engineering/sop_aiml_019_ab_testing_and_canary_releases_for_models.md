---
sop_id: "SOP-AIML-019"
title: "A/B Testing and Canary Releases for Models"
business_unit: "AI/ML Engineering"
version: "4.7"
effective_date: "2025-07-19"
last_reviewed: "2026-11-09"
next_review: "2027-05-15"
owner: "Dr. Marcus Rivera, Chief AI Officer"
approver: "David Park, VP of Engineering"
classification: "Internal"
regulations:
  - "EU AI Act"
  - "NIST AI RMF"
status: "Active"
---

# Standard Operating Procedure: A/B Testing and Canary Releases for Models

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the mandatory framework for conducting A/B testing and canary release deployments of machine learning (ML) models within Meridian Health Technologies, Inc. The purpose is to ensure that all model changes—whether new versions, architectural modifications, or hyperparameter optimizations—are validated in a controlled, statistically rigorous manner prior to full-scale production deployment. This framework is designed to protect patient safety, maintain model risk management integrity, ensure compliance with applicable regulations, and preserve the trust of healthcare providers, payers, and patients who rely on Meridian's products.

### 1.2 Scope

This SOP applies to all models deployed or intended for deployment across all Meridian business lines:

| Business Unit | Products Covered | Model Types |
|---|---|---|
| Clinical AI Platform | Diagnostic imaging analysis, patient risk scoring, adverse event prediction, clinical decision support tools | All high-risk AI models per EU AI Act Annex III classification; all models with direct or indirect patient impact |
| HealthPay Financial Services | Credit scoring models, fraud detection systems, medical lending underwriting models, claims automation classifiers | All SR 11-7 scoped models; all models influencing financial decisions or credit determinations |
| MedInsight Analytics | Population health models, care gap identification algorithms, outcomes prediction engines | All models processing PHI or generating clinical insights |
| Meridian SaaS Platform | Infrastructure-level models (auto-scaling predictors, anomaly detection, resource optimization) | All models supporting platform reliability and security |

### 1.3 Applicability

This SOP applies to:

- All AI/ML Engineering personnel, including Data Scientists, ML Engineers, MLOps Engineers, and ML Platform Engineers
- Clinical AI product teams
- HealthPay Financial Services modeling teams
- MedInsight Analytics teams
- Quality Assurance (QA) personnel involved in model validation
- Site Reliability Engineering (SRE) teams supporting model deployment infrastructure
- Product Managers responsible for model-centric features
- Compliance and Risk Management personnel overseeing model governance

### 1.4 Out of Scope

- Pure infrastructure changes with no model behavioral impact (e.g., container base image updates without logic changes)
- Front-end UI-only changes with no model inference pathway modifications
- Emergency security patches (governed by SOP-SEC-042 – Emergency Change Management)
- Non-production exploratory research conducted exclusively within sandboxed environments (governed by SOP-AIML-007 – Research and Experimentation Governance)

### 1.5 Geographic Applicability

This SOP applies globally to all Meridian offices and remote personnel operating in Boston, London, Berlin, Singapore, Toronto, and any future locations. Where regional regulatory requirements (e.g., EU AI Act vs. FDA requirements) diverge, the more stringent requirement shall prevail unless a formal exception is granted per Section 8 of this SOP.

---

## 2. Definitions and Acronyms

### 2.1 Definitions

| Term | Definition |
|---|---|
| **A/B Testing** | A controlled experiment in which two or more model variants (Control and Treatment(s)) are deployed simultaneously to mutually exclusive segments of production traffic, enabling statistical comparison of performance metrics under real-world conditions. |
| **Canary Release** | A phased deployment strategy in which a new model version is initially exposed to a small, monitored subset of production traffic. Traffic is progressively increased contingent upon successful validation at each phase, enabling rapid rollback if anomalies are detected. |
| **Control Variant** | The currently deployed production model serving as the baseline for comparison. |
| **Treatment Variant** | The new or modified model being evaluated against the Control. |
| **Traffic Split** | The proportion of inference requests routed to each variant, expressed as a percentage. |
| **Shadow Mode** | A deployment configuration where a Treatment variant receives a copy of production traffic and generates predictions that are logged but not served to end-users, allowing performance evaluation without user impact. |
| **Statistical Significance** | A determination, calculated via pre-registered hypothesis testing, that observed differences between variants are unlikely to have occurred by random chance. Meridian's default significance threshold is p < 0.05 with a minimum statistical power of 80% (β = 0.20), unless a more stringent threshold is specified in the experiment protocol. |
| **Minimum Detectable Effect (MDE)** | The smallest meaningful difference between variants that the experiment is designed to detect, expressed in the same units as the primary evaluation metric. |
| **Guardrail Metric** | A metric that must **not** degrade beyond a pre-specified absolute or relative threshold during an experiment, regardless of primary metric performance. Guardrail metrics protect against unintended harm (e.g., fairness degradation, error rate increases in protected subgroups, latency violations). |
| **Rollback** | The immediate cessation of traffic routing to a Treatment variant and reversion of 100% of traffic to the Control variant or previous stable version. |
| **Experiment Protocol** | A formal document, pre-registered in the Meridian Experiment Registry prior to experiment initiation, describing all parameters, metrics, stopping rules, and statistical analysis plans. |
| **High-Risk AI System** | Per EU AI Act Article 6 and Annex III, an AI system intended to be used as a safety component of a product, or that poses a significant risk of harm to health, safety, or fundamental rights. All Clinical AI Platform models are classified as high-risk. |
| **Model Risk Tier** | A classification (Tier 1-Critical, Tier 2-High, Tier 3-Moderate, Tier 4-Low) assigned per SOP-AIML-004 – Model Risk Classification and Governance, determining the minimum duration and rigor of testing required. |
| **Stratified Sampling** | An allocation method ensuring that traffic assigned to Control and Treatment groups maintains proportional representation across pre-defined segments (e.g., demographics, clinical conditions, risk scores). |

### 2.2 Acronyms

| Acronym | Full Term |
|---|---|
| ML | Machine Learning |
| MDE | Minimum Detectable Effect |
| SRM | Sample Ratio Mismatch |
| SRE | Site Reliability Engineering |
| QA | Quality Assurance |
| SLA | Service Level Agreement |
| SLI | Service Level Indicator |
| RTO | Recovery Time Objective |
| CI/CD | Continuous Integration / Continuous Deployment |
| PHI | Protected Health Information |
| HIPAA | Health Insurance Portability and Accountability Act |
| MDR | Medical Device Regulation (EU) |
| IRB | Institutional Review Board |
| DAG | Directed Acyclic Graph |
| KPI | Key Performance Indicator |
| RACI | Responsible, Accountable, Consulted, Informed |

---

## 3. Roles and Responsibilities

### 3.1 RACI Matrix

| Activity | ML Engineer | Data Scientist | Product Manager | QA Lead | SRE | ML Platform Engineer | Chief AI Officer | Compliance Officer |
|---|---|---|---|---|---|---|---|---|
| Experiment Protocol Design | C | R | A | C | I | C | I | I |
| Statistical Analysis Plan | C | R | I | C | I | I | I | I |
| Traffic Split Configuration | R | C | I | I | C | A | I | I |
| Guardrail Monitoring Setup | R | C | I | C | A | C | I | I |
| Experiment Execution | R | C | I | I | C | A | I | I |
| Daily Monitoring During Experiment | R | A | I | I | C | I | I | I |
| Statistical Significance Determination | C | R | I | I | I | I | I | I |
| Rollback Decision (Standard) | R | C | A | I | C | I | I | I |
| Rollback Decision (Emergency) | I | I | I | I | R | I | A | I |
| Experiment Conclusion Report | R | A | C | C | I | I | I | I |
| Final Approval for Full Rollout | I | C | A | C | I | I | R | I |
| Regulatory Compliance Review | I | I | I | I | I | I | C | R |
| Exception Approval | I | I | C | I | I | I | R | R |

**R = Responsible** (executes the work) | **A = Accountable** (approves and answers for outcome) | **C = Consulted** (provides input) | **I = Informed** (kept up to date)

### 3.2 Role Descriptions

**Chief AI Officer (Dr. Marcus Rivera):**
- Ultimate accountable authority for all model A/B testing and canary release activities
- Approves exceptions to this SOP
- Authorizes emergency rollbacks above Tier 3
- Reviews and signs off on all Tier 1 Critical model experiment conclusion reports

**VP of Engineering (David Park):**
- Approves this SOP and all subsequent revisions
- Escalation point for unresolved disputes regarding experiment design or rollback decisions
- Authorizes infrastructure changes that affect traffic splitting capabilities at the platform level

**ML Engineer:**
- Configures traffic routing rules in Meridian's ML serving infrastructure (currently MLFlow Serving with Istio/Envoy-based traffic management on Kubernetes)
- Implements guardrail metric instrumentation
- Monitors experiment health dashboards daily
- Executes rollback procedures when triggered
- Maintains experiment audit trail in the Meridian Experiment Registry

**Data Scientist:**
- Designs the experiment protocol, including hypothesis formulation, metric selection, and sample size calculations
- Conducts statistical analysis at pre-defined checkpoints
- Determines whether statistical significance thresholds are met
- Authors the experiment conclusion report
- Ensures fairness metrics are evaluated per regulatory requirements

**Product Manager:**
- Defines the business objectives and success criteria for the experiment
- Aligns experiment design with product roadmap priorities
- Accountable for rollback decisions (standard path)
- Communicates experiment outcomes to stakeholders

**QA Lead:**
- Validates that experimental setup meets testing standards
- Reviews offline evaluation results prior to experiment approval
- Audits monitoring dashboard configurations
- Verifies that guardrail thresholds are correctly implemented

**Site Reliability Engineer (SRE):**
- Ensures deployment infrastructure health during experiments
- Manages alert routing and escalation for infrastructure-level anomalies
- Responsible for emergency rollback execution when automated triggers fire
- Monitors latency, error rate, and resource utilization SLIs

**ML Platform Engineer:**
- Maintains and operates the traffic splitting infrastructure
- Accountable for the correctness of traffic routing mechanisms
- Ensures experiment isolation (no cross-contamination between Control and Treatment groups)
- Manages feature flag and experiment configuration systems

**Compliance Officer:**
- Reviews high-risk model experiments for EU AI Act compliance prior to initiation
- Ensures documentation meets regulatory evidence requirements
- Audits experiment registries for completeness and accuracy
- Escalates compliance concerns directly to the Chief AI Officer

---

## 4. Policy Statements

### 4.1 General Principles

**P-001: Mandatory Validation.** No model modification that alters inference behavior shall be deployed to 100% of production traffic without first undergoing A/B testing or canary release validation, except where explicitly exempted per Section 1.4 of this SOP.

**P-002: Pre-Registration.** All A/B tests and canary releases must be pre-registered in the Meridian Experiment Registry with a complete Experiment Protocol at least 48 hours prior to experiment initiation. Late registrations require Chief AI Officer approval.

**P-003: Informed Consent and Ethical Review.** Any A/B test involving models that directly impact patient care decisions, diagnoses, or treatment recommendations must undergo ethical review by Meridian's Clinical AI Ethics Board prior to protocol approval. The board evaluates whether the experiment design respects patient autonomy, ensures equitable distribution of risk, and provides meaningful opt-out mechanisms where applicable.

**P-004: Fairness Monitoring.** All experiments on models processing demographic, clinical, or financial data must include pre-defined fairness guardrail metrics evaluated across at minimum the following protected attributes where available: age group, sex, race/ethnicity, and geographic region (per EU AI Act Article 10(2)(f) requirements for training data examination extended to testing). Degradation of fairness metrics beyond pre-specified thresholds constitutes an automatic stop condition.

**P-005: Transparency.** The existence of any A/B test on a clinical model must be disclosed in the model's technical documentation (per EU AI Act Article 11 and Annex IV). Patients and providers must be able to ascertain, upon request, which model variant served a particular prediction affecting their case.

### 4.2 Experiment Design Policies

**P-006: Hypothesis Pre-Registration.** All experiments must define a falsifiable null hypothesis and specify the statistical test to be employed before data collection begins. Post-hoc hypothesis modification invalidates the experiment's statistical conclusions and requires a new protocol and registration.

**P-007: Sample Size Requirements.** Experiments must achieve a minimum of 80% statistical power for the pre-specified MDE. Sample size calculations must be documented in the Experiment Protocol. Experiments failing to reach the target sample size within the planned duration require an extension request or early termination analysis, both subject to the original power analysis assumptions.

**P-008: Minimum Duration.** A/B tests and canary releases must run for a minimum duration to capture temporal variation:

| Model Risk Tier | Minimum Duration | Minimum Full Business Cycles |
|---|---|---|
| Tier 1 – Critical | 14 days | 2 complete cycles |
| Tier 2 – High | 10 days | 1 complete cycle |
| Tier 3 – Moderate | 7 days | 1 complete cycle |
| Tier 4 – Low | 48 hours | Not required |

**P-009: Traffic Split Configuration.** Canary releases must follow a phased traffic increase schedule as specified in Section 5.3. No canary shall jump directly from initialization to 50% without passing through intermediate phases.

### 4.3 Rollback Policies

**P-010: Automatic Rollback Triggers.** The following conditions automatically trigger immediate rollback:

- Primary guardrail metric degrades beyond its pre-specified absolute or relative threshold
- Any fairness metric degrades by >5% relative change with p < 0.10
- Service latency at p99 increases by >200% relative to Control
- Error rate (HTTP 5xx or equivalent) exceeds 1% of requests
- Any patient safety incident is reported and plausibly attributable to the Treatment variant
- Sample Ratio Mismatch (SRM) detected with chi-squared p < 0.001

**P-011: Manual Rollback Authority.** Any member of the roles listed below may initiate a manual rollback at any time if they reasonably believe continued exposure to the Treatment variant poses a risk:

- Chief AI Officer
- VP of Engineering
- Product Manager (for their product's experiment only)
- SRE Lead (on-call, for infrastructure-related concerns)
- Compliance Officer (for regulatory compliance concerns)

**P-012: Post-Rollback Investigation.** Every rollback, whether automatic or manual, triggers a mandatory post-incident review to be conducted within 5 business days per SOP-INC-011 – AI Incident Response and Learning.

### 4.4 EU AI Act Specific Policies

**P-013: High-Risk System Documentation.** For all Clinical AI Platform models classified as high-risk per EU AI Act Annex III, A/B test and canary release documentation constitutes part of the technical documentation required under Article 11. All experiment protocols, monitoring logs, and conclusion reports must be retained for a minimum of 10 years after the model is last placed on the EU market per Article 11(2).

**P-014: Human Oversight.** Per EU AI Act Article 14, any A/B test on a high-risk AI system must maintain human oversight capability throughout the experiment. Human reviewers must be able to override model outputs from both Control and Treatment variants with equal facility. Oversight must not be degraded by the experimental configuration.

**P-015: Accuracy and Robustness Reporting.** Performance metrics collected during A/B testing and canary releases on high-risk systems must be included in the model's accuracy and robustness reporting required under Article 15.

**P-016: Serious Incident Reporting.** Any serious incident (as defined in EU AI Act Article 3(44)) or malfunction discovered during A/B testing or canary releases that could constitute a serious incident must be reported to the relevant market surveillance authority within 15 days per Article 62.

### 4.5 NIST AI RMF Alignment

**P-017: Risk Management Integration.** A/B testing and canary release activities are integral to Meridian's implementation of the NIST AI Risk Management Framework (AI RMF 1.0). These activities directly support the MAP function by establishing context for model behavior understanding, the MEASURE function by providing empirical performance data against defined metrics, and the MANAGE function by informing risk treatment decisions through controlled exposure and monitoring. All experiment-related risks identified shall be documented in the model's risk register and reviewed during quarterly AI risk committee meetings.

**P-018: Stakeholder Engagement.** Stakeholders affected by model changes under test—including clinical end-users, patient advocacy representatives, and operational staff—shall be informed of ongoing experiments through established communication channels. Feedback received during the experiment period shall be considered in the final evaluation, though structured formal feedback collection mechanisms are developed and maintained at the business unit level.

---

## 5. Detailed Procedures

### 5.1 Experiment Protocol Development

This procedure must be completed and approved prior to any traffic being routed to a new model variant.

#### 5.1.1 Protocol Document Template

All experiments must use the standard Experiment Protocol Template (Form AIML-019-EPT, latest version maintained in the Meridian Document Management System). The protocol must contain the following completed sections:

1. **Experiment Identification**
   - Unique Experiment ID (format: EXP-YYYY-MM-NNN)
   - Model Name and Version(s)
   - Model Risk Tier
   - Experiment Type (A/B Test | Canary Release | Shadow Mode Deployment)
   - Business Unit and Product
   - Primary Data Scientist (Protocol Author)
   - Responsible ML Engineer
   - Product Manager Approver

2. **Hypothesis Statement**
   - Null Hypothesis (H₀): The Treatment and Control variants do not differ with respect to the primary evaluation metric by more than the MDE.
   - Alternative Hypothesis (H₁): The Treatment variant differs from the Control by at least the MDE on the primary evaluation metric.
   - Explicit statement of directionality (one-tailed vs. two-tailed test with justification).

3. **Metrics Specification**
   - **Primary Evaluation Metric(s):** Maximum of 2. Must be defined with precise calculation methodology.
   - **Secondary Evaluation Metrics:** Maximum of 5. Exploratory comparisons; no statistical significance claim without correction for multiple comparisons (Bonferroni or Benjamini-Hochberg).
   - **Guardrail Metrics:** Minimum of 3. Must include at least one fairness metric per sensitive attribute and at least one operational metric (latency, error rate, or resource utilization). Each guardrail must specify an absolute threshold and a relative degradation threshold.

4. **Experimental Design Parameters**
   - Sample size calculation with assumptions and formula
   - MDE specification
   - Traffic split ratios per phase
   - Randomization unit (user ID, session ID, case ID, clinical encounter ID, etc.)
   - Stratification variables (if applicable)
   - Planned duration and phases per Section 5.3

5. **Statistical Analysis Plan**
   - Primary statistical test (e.g., two-sample t-test, Mann-Whitney U, chi-squared)
   - Significance threshold (α)
   - Desired statistical power (1 - β)
   - Interim analysis checkpoints (if planned)
   - Multiple comparison correction method
   - Stopping rules (efficacy and futility)

6. **Risk Assessment**
   - Identified risks specific to this experiment
   - Mitigation controls
   - Rollback trigger thresholds (customized from baseline in Section 4.3)

7. **EU AI Act Compliance Section (for high-risk models)**
   - Confirmation of human oversight continuity
   - Technical documentation retention plan
   - Serious incident reporting readiness confirmation

#### 5.1.2 Protocol Approval Workflow

```
[Data Scientist drafts protocol]
          │
          ▼
[Peer Review by second Data Scientist (2 business days)]
          │
          ▼
[QA Lead review for guardrail adequacy (2 business days)]
          │
          ▼
[ML Engineer review for implementation feasibility (2 business days)]
          │
          ▼
[Product Manager approval for business alignment]
          │
          ▼
{If Tier 1 or Clinical AI Platform model}
          │
          ▼
[Clinical AI Ethics Board review (5 business days)]
          │
          ▼
[Compliance Officer review for EU AI Act alignment (3 business days)]
          │
          ▼
{All experiments}
          │
          ▼
[Chief AI Officer final sign-off (Tier 1 only)]
          │
          ▼
[Protocol registered in Meridian Experiment Registry]
```

Total approval lead time: 6-10 business days for Tier 2-4 models; 11-15 business days for Tier 1 models. Teams must plan experiment timelines accordingly.

### 5.2 Pre-Experiment Validation

Before traffic routing is enabled, the following pre-flight checks must pass:

#### 5.2.1 Offline Evaluation Gate

| Gate | Criteria | Required For |
|---|---|---|
| Offline test suite pass | All pre-defined offline evaluation test cases pass with no regressions > 2% on any metric | All tiers |
| Adversarial robustness check | Treatment model passes Meridian's standard adversarial input test suite (AIML-SEC-TS-042) | Tier 1, Tier 2 |
| Fairness benchmark | Treatment model's offline fairness metrics do not degrade >3% from Control on any protected attribute | All tiers |
| Latency benchmark | Treatment model p95 latency ≤ 150% of Control p95 latency in isolated environment | All tiers |
| Memory profile | Treatment model peak memory usage ≤ 130% of Control allocation | All tiers |

QA Lead documents results in the experiment's pre-validation report (Form AIML-019-PVR).

#### 5.2.2 Infrastructure Readiness

The ML Engineer and SRE must confirm:

1. Traffic splitting infrastructure (Istio VirtualService rules) configured and tested with synthetic traffic.
2. Monitoring dashboards deployed and populating with data (per Section 7.1).
3. Alert thresholds configured per guardrail specifications.
4. Rollback automation verified with a dry-run rollback test.
5. Experiment ID tagged on all Treatment variant inference telemetry.
6. Log isolation verified: Treatment and Control logs do not intermix in downstream pipelines.

#### 5.2.3 Experiment Initiation Approval

A formal Go/No-Go meeting is held with the Data Scientist, ML Engineer, Product Manager, and QA Lead. The following checklist items must be affirmed:

- [ ] Experiment Protocol fully approved and registered
- [ ] Offline evaluation gates passed
- [ ] Infrastructure readiness confirmed
- [ ] Guardrail monitoring dashboards operational
- [ ] Rollback procedure tested
- [ ] On-call rotation briefed on experiment

Upon unanimous Go decision, the ML Engineer initiates traffic routing per Section 5.3.

### 5.3 Traffic Splitting and Phase Progression

#### 5.3.1 Standard Canary Release Phases

All canary releases follow this phased progression. Advancement to the next phase requires successful completion of the current phase's monitoring period without triggering any rollback condition.

| Phase | Traffic to Treatment | Traffic to Control | Minimum Duration | Advancement Criteria |
|---|---|---|---|---|
| Phase 0: Shadow | 0% served; 100% logged in shadow | 100% | 24 hours | All guardrail metrics within thresholds; no critical errors in shadow logs |
| Phase 1: Initial Exposure | 2% | 98% | 24 hours | No rollback triggers; Product Manager approval |
| Phase 2: Low Traffic | 10% | 90% | 48 hours | No rollback triggers; QA Lead approval |
| Phase 3: Medium Traffic | 25% | 75% | 72 hours | No rollback triggers; no fairness guardrail activations |
| Phase 4: High Traffic | 50% | 50% | Duration per P-008 minimum from this point | No rollback triggers; interim statistical analysis showing no significant degradation |
| Phase 5: Full Rollout | 100% | 0% | N/A (full deployment) | Final statistical analysis; Experiment Conclusion Report approved |

#### 5.3.2 Standard A/B Test Traffic Configuration

For formal hypothesis-testing experiments:

| Configuration Element | Requirement |
|---|---|
| Traffic Allocation | 50% Control / 50% Treatment, unless sample size calculation justifies unequal allocation |
| Allocation Mechanism | Deterministic hash-based assignment on the pre-defined randomization unit; no self-selection permitted |
| Allocation Consistency | Same randomization unit must always route to the same variant (sticky assignment) |
| SRM Monitoring | Sample Ratio Mismatch test run every 6 hours; automated alert if chi-squared p < 0.01 |
| Stratification Verification | If stratified sampling is employed, distribution parity across strata is validated every 24 hours |

#### 5.3.3 Traffic Routing Mechanism

Meridian's ML serving infrastructure implements traffic splitting at the service mesh layer:

1. **Istio VirtualService** rules define weight-based traffic distribution between model variant Kubernetes Services.
2. **Envoy sidecar proxies** in the inference service pods enforce traffic routing rules.
3. **Consistent hashing** on the `x-meridian-randomization-unit` header ensures sticky assignment.
4. **Telemetry headers** (`x-meridian-experiment-id`, `x-meridian-variant`) are injected and propagated through all downstream logging and monitoring systems.
5. **Feature flag override** capability is maintained for emergency traffic shifting without deployment changes.

The ML Platform Engineer is responsible for the correctness of this configuration. Any configuration change to traffic routing rules during an active experiment is prohibited except in the execution of a rollback.

### 5.4 During-Experiment Monitoring

#### 5.4.1 Daily Monitoring Checklist

The Responsible ML Engineer must complete the following checks at minimum once per 24-hour period during any active A/B test or canary release:

1. **Dashboard Review (Section 7.1 describes dashboard contents)**
   - Primary metric trending: Are Control and Treatment diverging?
   - Guardrail metrics: Any approaching warning thresholds (<80% of trigger threshold)?
   - Fairness metrics: Any subgroup showing unexpected divergence?
   - SRM test: Last chi-squared p-value > 0.05?

2. **Alert Review (past 24 hours)**
   - Any guardrail warning alerts (not yet at critical)?
   - Any infrastructure alerts (CPU throttling, memory pressure, OOM events on Treatment pods)?
   - Any user-reported issues potentially related to model behavior?

3. **Log Sampling Review**
   - Random sample of 100 Treatment inferences reviewed for obvious anomalies (e.g., out-of-range predictions, nonsensical outputs, NaN values).
   - For Clinical AI Platform models: sample size increased to 500 inferences and review includes clinician-annotated correctness check where feasible.

4. **Daily Check-in Post in Experiment Channel**
   - ML Engineer posts status update to the experiment's dedicated Slack channel (`#exp-{EXPERIMENT_ID}`)
   - Template: "Day [N] - [Phase] - Traffic: Treatment [X]% / Control [Y]% - Primary metric: Control [value], Treatment [value], Δ [delta] - Guardrails: All green / [N] in warning - SRM: p=[value] - Status: CONTINUE / CONCERN / ESCALATE"

#### 5.4.2 Interim Statistical Analysis

For experiments with planned duration exceeding 7 days, interim analyses are conducted at the midpoint:

1. Data Scientist performs pre-specified interim analysis per the protocol's statistical analysis plan.
2. If the stopping rule for efficacy is met (Treatment is conclusively superior with p < adjusted threshold), the Product Manager may decide to accelerate the phase progression schedule. Minimum durations per phase still apply.
3. If the stopping rule for futility is met (unlikely to reach significance by planned end), the Product Manager may decide to terminate the experiment early and abandon the Treatment variant.
4. All interim analysis results are documented in the Experiment Registry.

### 5.5 Experiment Conclusion

#### 5.5.1 Statistical Conclusion

Upon completion of the planned experiment duration and achievement of the target sample size:

1. Data Scientist performs the final statistical analysis per the pre-registered plan.
2. Results are categorized:

| Conclusion | Criteria |
|---|---|
| **Treatment Superior** | Primary metric improvement exceeds MDE with p < α; all guardrail metrics within thresholds; no fairness degradation |
| **Treatment Non-Inferior** | Primary metric within MDE of Control with p < α for non-inferiority test; all guardrail metrics within thresholds |
| **Treatment Inferior** | Primary metric degradation exceeds MDE with p < α or any guardrail metric breached |
| **Inconclusive** | Sample size insufficient for statistical power target despite reaching planned duration; or effects observed but not reaching significance threshold |

#### 5.5.2 Experiment Conclusion Report

The Data Scientist authors the Experiment Conclusion Report (Form AIML-019-ECR) within 5 business days of experiment termination. The report includes:

1. Summary of experiment parameters (link to approved protocol)
2. Actual sample sizes achieved (Control and Treatment)
3. Final statistical analysis results with p-values and confidence intervals
4. All primary, secondary, and guardrail metric results
5. Fairness metric analysis across protected attributes
6. Any deviations from protocol and their justifications
7. Recommendation:
   - **Proceed to full rollout** (Treatment Superior or Non-Inferior)
   - **Abandon Treatment** (Treatment Inferior)
   - **Extend experiment** with justification (Inconclusive)

#### 5.5.3 Full Rollout Approval

Before a Treatment variant can be promoted to 100% of traffic:

1. Experiment Conclusion Report must be approved by:
   - Product Manager (all tiers)
   - Chief AI Officer (Tier 1 only)
   - Compliance Officer (high-risk AI systems and SR 11-7 models)
2. Model version must be tagged in the Meridian Model Registry as `production-ready`.
3. Model card must be updated with experiment results (per SOP-AIML-008 – Model Documentation and Cards).
4. Full rollout proceeds via the standard CI/CD pipeline, not as an extension of the experiment's traffic rules.

### 5.6 Rollback Procedure

#### 5.6.1 Automated Rollback

When any automatic rollback trigger condition is detected (Section 4.3, P-010):

1. Monitoring system fires `CRITICAL` alert to PagerDuty (escalation policy: ML Engineering on-call, secondary: SRE on-call).
2. Automated rollback script (`aiml-rollback-model`) executes:
   - Updates Istio VirtualService weight to 100% Control / 0% Treatment
   - Gracefully drains in-flight Treatment requests (30-second timeout)
   - Logs rollback event with full context (triggering metric, threshold, observed value, timestamp)
   - Posts rollback notification to `#exp-{EXPERIMENT_ID}` Slack channel and `#ai-incidents`
3. ML Engineer on-call acknowledges within 15 minutes.
4. Post-rollback investigation initiated per SOP-INC-011.

**RTO Target:** Rollback completion within 2 minutes of trigger detection.

#### 5.6.2 Manual Rollback

When any authorized role (Section 4.3, P-011) initiates a manual rollback:

1. Authorized individual executes rollback either:
   - Via the Meridian ML Ops Dashboard "Emergency Rollback" button (requires authentication and confirms authorization scope)
   - By direct command to SRE on-call if dashboard is unavailable
2. Rollback procedure identical to automated steps 2-4 above.
3. Rollback rationale documented in post-incident review.

#### 5.6.3 Post-Rollback State

After any rollback:
- The experiment is placed in `TERMINATED` status.
- Traffic remains at 100% Control until root cause analysis is complete.
- Re-initiation of the experiment requires a new or amended Experiment Protocol addressing the root cause.

---

## 6. Controls and Safeguards

### 6.1 Technical Controls

| Control ID | Control Description | Implementation |
|---|---|---|
| TC-001 | Traffic Isolation | Istio VirtualService rules enforce strict traffic separation; Envoy sidecar configuration verified by ML Platform Engineer before experiment initiation; no cross-contamination possible at the networking layer |
| TC-002 | Consistent Assignment | Deterministic SHA-256 hash on `x-meridian-randomization-unit` header ensures sticky variant assignment; hash seed rotated per experiment to prevent cross-experiment correlation |
| TC-003 | Telemetry Integrity | All Treatment inferences tagged with `x-meridian-experiment-id` and `x-meridian-variant` headers; headers propagated through all services in the call graph; missing headers trigger `WARNING` log and alert if >0.1% of requests |
| TC-004 | Automated Rollback Hook | Pre-deployed rollback automation with 2-minute RTO; dry-run tested within 24 hours of experiment initiation; health-check endpoint monitored independently of experiment metrics |
| TC-005 | Feature Flag Kill Switch | Global kill switch (`meridian.exp.global_kill`) disables all experimental traffic routing; tested during each quarterly disaster recovery exercise |
| TC-006 | Log Immutability | Experiment logs written to append-only storage (AWS S3 with Object Lock in compliance mode, retention 10 years per EU AI Act Article 11(2) for high-risk models); tamper-proof audit trail |
| TC-007 | Capacity Safety Margin | Treatment variant resource allocation includes 200% headroom over offline-benchmarked requirements to absorb unexpected load; auto-scaling policies validated before Phase 1 |

### 6.2 Administrative Controls

| Control ID | Control Description | Implementation |
|---|---|---|
| AC-001 | Experiment Registry | All experiments logged in the Meridian Experiment Registry (Backstage plugin backed by PostgreSQL with audit logging); entries immutable post-creation; all modifications append-only |
| AC-002 | Pre-Registration Requirement | Experiment Protocol must be registered ≥48 hours prior to traffic routing; registry enforces timestamp check; late registrations blocked without Chief AI Officer override |
| AC-003 | Four-Eyes Approval | Traffic routing configuration changes require approval by both the Responsible ML Engineer and the Product Manager or their delegates; enforced via GitOps pull request workflow with mandatory reviewers |
| AC-004 | Segregation of Duties | Protocol author (Data Scientist) cannot approve their own protocol; traffic routing implementer (ML Engineer) cannot be the sole approver of phase advancement |
| AC-005 | Ethical Review Board | Per Section 4.1 P-003, Clinical AI Ethics Board reviews all patient-impacting experiments; board includes at minimum: one practicing clinician, one patient advocate (external), one bioethicist, one regulatory specialist |
| AC-006 | Experiment Duration Enforcement | Experiment registry automatically transitions experiments exceeding planned duration + 20% buffer without extension request to `PENDING_EXTENSION_OR_TERMINATION` status; automatic notification to Product Manager and Compliance Officer |

### 6.3 EU AI Act Specific Controls

| Control ID | Control Description | EU AI Act Reference |
|---|---|---|
| EU-001 | Technical Documentation Retention | All experiment artifacts (protocol, monitoring logs, conclusion report, rollback records) retained for 10 years minimum in immutable storage, indexed by model version and experiment ID | Article 11(2), Annex IV |
| EU-002 | Human Oversight Continuity | During any A/B test, human reviewers retain override capability for both Control and Treatment predictions with equal latency and availability; override rate monitored as a guardrail metric; any increase in override necessity for Treatment >10% triggers review | Article 14(1)-(5) |
| EU-003 | Accuracy Reporting Integration | Performance metrics collected during experiments automatically fed into the model's EU AI Act technical documentation package; model cards updated within 10 business days of experiment conclusion | Article 15, Annex IV |
| EU-004 | Serious Incident Detection Pipeline | Experiment monitoring includes automated detection of patterns matching serious incident definitions (Article 3(44)); any such detection triggers immediate rollback AND notification to Compliance Officer for Article 62 reporting evaluation | Article 62, Article 3(44) |
| EU-005 | Fairness and Bias Documentation | Fairness guardrail metric results, including any degradations observed, documented in the technical documentation irrespective of whether thresholds were breached; serves as evidence of Article 10(2)(f) compliance during testing phase | Article 10(2)(f), Recital 44 |
| EU-006 | CE Marking Impact Assessment | For CE-marked models under EU MDR, any A/B test that could indicate a change in the model's safety or performance characteristics triggers a notified body impact assessment per SOP-RA-027 – Regulatory Change Impact Assessment | MDR Article 120, Annex II |

### 6.4 Data Privacy Controls

- No PHI is logged in experiment telemetry. All PHI is processed within the inference service boundary and stripped before telemetry emission.
- Experiment logs, including shadow mode prediction logs, are subject to the same data access controls as production inference logs per SOP-DSG-011 – Data Classification and Handling.
- A/B test group assignment does not persist in user-identifiable records beyond the experiment duration, except where required for regulatory audit (clinical models: group assignment retained per retention policy with justification of clinical necessity).

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Experiment Monitoring Dashboards

Every active experiment must have a dedicated monitoring dashboard provisioned from the standard Meridian Experiment Dashboard Template (Datadog dashboard template `aiml-exp-monitor-v3`). The dashboard includes the following panes:

| Pane | Content | Refresh Interval | Alerting |
|---|---|---|---|
| Primary Metric Comparison | Time-series line chart: Control vs. Treatment on primary metric(s), with cumulative mean overlay and confidence interval bands | 5 minutes | No direct alerting; used for visual trend detection |
| Guardrail Metric Dashboard | Multi-panel display: each guardrail metric as a time series with warning threshold (yellow dashed line) and critical threshold (red dashed line) overlaid | 5 minutes | Warning: PagerDuty `P3` (1-hour acknowledgment) Critical: PagerDuty `P1` (5-minute acknowledgment, automatic rollback trigger) |
| Fairness Subgroup Analysis | Small multiples: primary metric stratified by protected attribute categories, Treatment vs. Control overlaid per subgroup; relative change percentage tile per subgroup | 15 minutes | PagerDuty `P2` (15-minute acknowledgment) if any subgroup relative change exceeds protocol threshold |
| Sample Ratio Mismatch | Bar chart: expected vs. actual traffic proportion per variant; chi-squared p-value trend line | 30 minutes (SRM test runs every 6 hours) | PagerDuty `P2` if chi-squared p < 0.01 |
| Operational Health | Standard service health panes: p50/p95/p99 latency, request rate, error rate (5xx), CPU/memory utilization, all split by Control vs. Treatment | 1 minute | Standard SRE thresholds (SOP-SRE-001); Treatment-specific thresholds per Section 4.3 P-010 |
| Traffic Split Visualization | Pie chart: current traffic proportion, overlaid with phase target markers; bar chart: cumulative request counts per variant | 5 minutes | No alerting; informational |

### 7.2 Key Performance Indicators (KPIs)

The AI/ML Engineering organization tracks the following KPIs related to A/B testing and canary releases:

| KPI | Target | Measurement Method | Reporting Cadence |
|---|---|---|---|
| Experiment Protocol Pre-Registration Compliance | ≥ 98% of experiments registered ≥ 48 hours before traffic routing | Meridian Experiment Registry timestamp audit | Monthly, included in AI Governance Dashboard |
| Canary Phase Adherence | 100% compliance; no phase skipping | Phase progression audit log review | Per experiment; aggregate monthly |
| Rollback Rate | ≤ 10% of experiments triggering rollback | Rollback event log | Monthly |
| Mean Time to Detect (MTTD) Guardrail Violations | ≤ 15 minutes from threshold crossing to alert acknowledgment | PagerDuty analytics + Datadog event correlation | Monthly, reviewed at ML Ops retrospective |
| Mean Time to Recover (MTTR) Post-Rollback | ≤ 2 minutes to traffic reversion (RTO); ≤ 5 business days to root cause analysis completion | Incident management system | Per incident; aggregate quarterly |
| Experiment Conclusion Report Timeliness | ≥ 95% submitted within 5 business days of experiment end | Experiment Registry status tracking | Monthly |
| Fairness Guardrail Activation Rate | ≤ 5% of experiments triggering fairness guardrail | Experiment Registry event log | Quarterly, included in AI Fairness Report |
| Stakeholder Communication Compliance | 100% of Tier 1-2 experiments have documented stakeholder notification prior to Phase 1 | Experiment Registry checklist verification | Monthly |

### 7.3 Reporting Cadence

| Report | Audience | Frequency | Content |
|---|---|---|---|
| Active Experiment Status Brief | VP of Engineering, Chief AI Officer | Weekly (every Monday) | Summary of all active experiments: phase, duration elapsed/planned, any warnings or concerns |
| Experiment Completion Summary | Product Managers, Data Science Leads | Per experiment + monthly rollup | Conclusion report summaries; win/loss/inconclusive rates |
| Quarterly AI Testing Governance Report | Chief AI Officer, Compliance Officer, AI Ethics Board | Quarterly | Aggregate KPI performance; EU AI Act compliance metrics; incident summaries; fairness guardrail analysis; recommendations for SOP revisions |
| Annual AI RMF Alignment Review | Chief AI Officer, CISO, General Counsel | Annual | Review of A/B testing framework against NIST AI RMF and EU AI Act; identification of gaps and remediation planning; input to SOP review cycle |

---

## 8. Exception Handling and Escalation

### 8.1 Exception Types

| Exception Type | Definition | Examples |
|---|---|---|
| **Protocol Deviation** | Minor departures from the approved protocol that do not affect the validity of statistical conclusions or risk management posture | Experiment initiated 4 hours after Go/No-Go instead of immediately; daily check-in missed by 6 hours |
| **Protocol Variance** | Departures from protocol that may affect statistical interpretation but do not increase patient or business risk | Traffic split unintentionally 52/48 instead of 50/50 for 2 hours; stratification variable not collected for 0.5% of traffic due to upstream data pipeline issue |
| **Protocol Waiver** | Intentional exemption from a specific policy requirement, approved in advance | Skipping Phase 0 shadow mode for a latency-critical Tier 4 infrastructure model; reducing minimum duration for a model with no patient impact |
| **SOP Exception** | Circumstances where full compliance with this SOP is not feasible or would be counterproductive to Meridian's mission | Emergency model hotfix requiring immediate deployment; model change that is objectively non-substantive but triggers SOP scope |

### 8.2 Exception Approval Authority

| Exception Scope | Approver Required | Maximum Duration |
|---|---|---|
| Protocol Deviation (minor, self-detected) | ML Engineer + Product Manager (documentation only; no pre-approval needed if detected post-hoc) | Documented in conclusion report; no duration limit for experiment |
| Protocol Deviation (minor, externally flagged) | QA Lead | 2 business days to resolve or escalate |
| Protocol Variance | Product Manager + QA Lead | Duration of experiment; documented in conclusion report with impact assessment |
| Protocol Waiver (Tier 3-4 models) | Product Manager + Chief AI Officer (delegatable to Director of ML Engineering) | Single experiment; renewed per experiment |
| Protocol Waiver (Tier 1-2 models) | Chief AI Officer + Compliance Officer | Single experiment |
| SOP Exception (non-clinical, non-financial model) | Chief AI Officer | Single instance; time-bound |
| SOP Exception (clinical or financial model) | Chief AI Officer + Compliance Officer + VP of Engineering | Single instance; time-bound; documented with regulatory impact assessment |

### 8.3 Exception Request Procedure

1. Requestor completes the Exception Request Form (Form AIML-019-ERF) including:
   - Experiment ID or proposed experiment identification
   - Specific SOP section or policy identifier from which exception is sought
   - Justification: why compliance is not feasible or appropriate in this instance
   - Risk assessment: what risks does non-compliance introduce, and what compensating controls are proposed?
   - Duration: if time-bound, specify start and end

2. Form routed to approvers per Section 8.2 table.

3. Approvers may:
   - **Approve:** Exception recorded in Experiment Registry; approved compensating controls become binding requirements for the experiment.
   - **Approve with Conditions:** Additional compensating controls or monitoring requirements specified; must be met for approval to take effect.
   - **Reject:** With written rationale; requestor may revise and resubmit once.

4. Approved exceptions are linked to the experiment in the Experiment Registry and visible in the experiment's audit trail.

5. No experiment with a pending exception request may proceed beyond Phase 1 (Initial Exposure) until the exception is approved.

### 8.4 Escalation Path

```
Issue identified by any role
          │
          ▼
[Immediate supervisor or experiment's Product Manager]
          │ (1 business day if unresolved)
          ▼
[Director of ML Engineering / Director of Data Science (depending on issue nature)]
          │ (1 business day if unresolved)
          ▼
[Chief AI Officer]
          │ (1 business day if unresolved)
          ▼
[VP of Engineering (final escalation for operational issues)]
```

For regulatory compliance concerns, the Compliance Officer has a direct escalation path to the Chief AI Officer without intermediate steps.

---

## 9. Training Requirements

### 9.1 Required Training Modules

| Training Module | Course Code | Required For | Frequency | Delivery Method |
|---|---|---|---|---|
| A/B Testing and Canary Release Fundamentals | AIML-TRN-019-BASE | All AI/ML Engineering personnel, all Data Scientists working on production models, all Product Managers overseeing model-centric features | Initial onboarding; refresher every 24 months | Self-paced e-learning (LMS) + hands-on workshop with sandbox environment (4 hours) |
| Statistical Rigor in Online Experimentation | AIML-TRN-019-STAT | All Data Scientists, all ML Engineers involved in experiment design | Initial; refresher every 18 months | Instructor-led (2 days) covering: power analysis, sequential testing, multiple comparison correction, SRM diagnosis, stratification techniques |
| EU AI Act Compliance for Model Testing | REG-TRN-032 | All personnel working on Clinical AI Platform models; all Compliance Officers; all QA Leads | Initial; refresher annually (due to regulatory evolution) | Instructor-led (1 day) covering: high-risk classification, technical documentation requirements, serious incident definitions, Article 14 human oversight, Article 62 reporting obligations |
| Canary Rollback and Incident Response Drill | AIML-TRN-019-DRILL | All ML Engineers, all SREs | Initial; refresher quarterly (hands-on drill) | Simulated rollback exercise in staging environment; timed assessment; RTO must be met within 2 attempts |

### 9.2 Training Tracking

- All training completion is recorded in Meridian's Learning Management System (Workday Learning).
- Managers are responsible for ensuring their direct reports maintain current training status.
- Experiment Protocol submission is blocked by the Experiment Registry if the protocol author's `AIML-TRN-019-STAT` certification is expired or not on file.
- Compliance Officer audits training compliance quarterly for all personnel working on high-risk AI systems.

### 9.3 Role-Based Minimum Certification Requirements for Experiment Participation

| Role | Minimum Active Certifications |
|---|---|
| Data Scientist (Protocol Author) | AIML-TRN-019-BASE, AIML-TRN-019-STAT; plus REG-TRN-032 if working on Clinical AI Platform models |
| ML Engineer (Experiment Implementer) | AIML-TRN-019-BASE, AIML-TRN-019-DRILL (must be current within 90 days); plus REG-TRN-032 if implementing experiments on Clinical AI Platform models |
| Product Manager (Experiment Approver) | AIML-TRN-019-BASE; plus REG-TRN-032 if approving experiments on Clinical AI Platform models |
| QA Lead (Experiment Quality Reviewer) | AIML-TRN-019-BASE, AIML-TRN-019-STAT; REG-TRN-032 mandatory |
| SRE (Infrastructure Support) | AIML-TRN-019-DRILL |

---

## 10. Related Policies and References

### 10.1 Internal Meridian SOPs

| SOP ID | Title | Relationship |
|---|---|---|
| SOP-AIML-001 | Model Development Lifecycle | Defines the overall lifecycle that A/B testing fits within |
| SOP-AIML-004 | Model Risk Classification and Governance | Defines the Tier system used throughout this SOP for scoping requirements |
| SOP-AIML-007 | Research and Experimentation Governance | Governs pre-production experimentation in sandbox environments |
| SOP-AIML-008 | Model Documentation and Model Cards | Specifies documentation update requirements triggered by experiment conclusion |
| SOP-AIML-012 | Model Registry and Versioning | Governs model versioning; referenced for production-ready tagging post-experiment |
| SOP-AIML-021 | Offline Model Evaluation Procedures | Defines offline evaluation gates required before experiment initiation |
| SOP-RA-027 | Regulatory Change Impact Assessment | Triggered for CE-marked model changes; referenced in EU-006 control |
| SOP-SEC-042 | Emergency Change Management | Governs emergency deployments; referenced as out-of-scope for standard experiment flow |
| SOP-INC-011 | AI Incident Response and Learning | Governs post-rollback investigation and incident management |
| SOP-DSG-011 | Data Classification and Handling | Governs PHI handling; referenced for log data privacy controls |
| SOP-SRE-001 | Service Level Objectives and Error Budgets | Defines SRE alerting thresholds integrated with operational health monitoring |

### 10.2 External Standards and Regulations

| Reference | Description | Applicability |
|---|---|---|
| EU AI Act (Regulation 2024/1689) | Harmonized rules on artificial intelligence; Articles 6, 10, 11, 14, 15, 62, Annex III, Annex IV specifically referenced | Mandatory for all Clinical AI Platform models placed on EU market |
| EU Medical Device Regulation (MDR) 2017/745 | Regulation on medical devices; CE marking requirements referenced for models classified as medical device software | Mandatory for CE-marked clinical AI products |
| NIST AI RMF 1.0 | AI Risk Management Framework; MAP, MEASURE, MANAGE functions provide overarching risk governance structure | Adopted as Meridian's AI risk governance framework |
| ISO 13485:2016 | Quality management systems for medical devices | Applicable to Clinical AI Platform model development processes |
| HIPAA | Health Insurance Portability and Accountability Act | Privacy controls for PHI in experiment logs |

### 10.3 Internal Tools and Systems Referenced

| System | Purpose |
|---|---|
| Meridian Experiment Registry | Central system of record for all experiment protocols, statuses, approvals, and results (built on Backstage with PostgreSQL backend) |
| MLFlow Serving | Model serving framework managing variant deployments |
| Istio / Envoy (Kubernetes Service Mesh) | Traffic splitting and routing infrastructure |
| Datadog | Monitoring, dashboarding, and alerting platform |
| PagerDuty | Incident alerting and on-call management |
| Workday Learning | Learning Management System for training tracking |
| GitOps Repository (GitHub Enterprise) | Infrastructure-as-code for traffic routing configuration |

---

## 11. Revision History

| Version | Effective Date | Author | Change Summary | Approver |
|---|---|---|---|---|
| 1.0 | 2024-03-01 | Dr. Marcus Rivera, Chief AI Officer | Initial release. Established baseline A/B testing and canary release framework for Meridian. | David Park, VP of Engineering |
| 2.0 | 2024-08-15 | Dr. Marcus Rivera, Chief AI Officer | Major revision. Incorporated EU AI Act requirements following publication of Regulation 2024/1689 (effective August 2024). Added clinical model-specific controls, expanded fairness guardrail definitions, introduced mandatory ethical review board gate. Extended document retention to 10 years for high-risk systems. | David Park, VP of Engineering |
| 3.0 | 2025-01-22 | Sarah Chen, Director of ML Engineering (delegated revision) | Updated traffic routing infrastructure references from deprecated `Seldon Core` to current `MLFlow Serving + Istio/Envoy`. Revised canary phase durations based on 9 months of operational data. Added SRM monitoring requirement. Standardized dashboard template references. | Dr. Marcus Rivera, Chief AI Officer |
| 3.3 | 2025-04-05 | Compliance Working Group | Interim revision. Added serious incident detection pipeline control (EU-004). Updated EU AI Act article references to final numbering. Clarified training certification blocking in Experiment Registry. | Dr. Marcus Rivera, Chief AI Officer |
| 4.0 | 2025-07-19 | Dr. Marcus Rivera, Chief AI Officer | Major revision. Aligned with NIST AI RMF 1.0 adoption across Meridian. Restructured P-017/018 for RMF alignment. Introduced formal stakeholder engagement language. Expanded protocol template to include risk assessment section. Added formal exception type taxonomy and approval matrix. Increased minimum duration for Tier 1 from 10 to 14 days based on post-market surveillance data. | David Park, VP of Engineering |
| 4.5 | 2026-02-10 | Dr. Marcus Rivera, Chief AI Officer | Interim revision. Updated RACI matrix to reflect reorganization within ML Engineering. Clarified shadow mode phase requirements. Added KPI targets and reporting cadence detail. Incorporated regulatory feedback from notified body audit. | David Park, VP of Engineering |
| 4.7 | 2026-11-09 | Dr. Marcus Rivera, Chief AI Officer | Current version. Refined fairness monitoring requirements to include geographic region per updated regulatory guidance. Added detailed sample size calculation documentation requirements. Updated training module codes and LMS integration details. Minor procedural clarifications to phase advancement criteria. Incorporated lessons learned from 3 incident post-mortems (INC-2026-084, INC-2026-112, INC-2026-197). | David Park, VP of Engineering |

---

**End of Document**

© Meridian Health Technologies, Inc. – Internal Use Only – Distribution Controlled by Document Owner