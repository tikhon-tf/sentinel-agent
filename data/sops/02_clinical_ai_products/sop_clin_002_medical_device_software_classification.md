---
sop_id: "SOP-CLIN-002"
title: "Medical Device Software Classification"
business_unit: "Clinical AI Products"
version: "4.0"
effective_date: "2024-09-01"
last_reviewed: "2025-01-07"
next_review: "2025-07-16"
owner: "Dr. Aisha Okafor, VP of Clinical AI Products"
approver: "Dr. Priya Patel, Chief Medical Officer"
classification: "Internal"
regulations:
  - "EU AI Act"
status: "Active"
---

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the framework, methodologies, and governance structure for classifying software products developed by the Clinical AI Products business unit at Meridian Health Technologies, Inc. as medical device software or non-medical device software. The purpose is to ensure consistent, defensible, and regulatorily compliant classification determinations that drive subsequent design controls, risk management activities, and regulatory submission strategies. This SOP operationalizes the requirements of the EU Medical Device Regulation (MDR) 2017/745, FDA guidance on Software as a Medical Device (SaMD), IEC 62304:2006/AMD1:2015, and the EU AI Act for high-risk AI systems.

Given Meridian's dual deployment across North American and European Union markets, classification decisions made under this SOP directly impact CE marking strategies, FDA 510(k) or De Novo pathways, and Article 16 compliance under the EU AI Act for high-risk AI systems. Misclassification exposes Meridian to product recall risk, regulatory enforcement actions, and erosion of notified body confidence.

### 1.2 Scope

This SOP applies to all software products, modules, algorithms, and updates developed or maintained by the Clinical AI Products business unit that perform or influence clinical decision-making, diagnostic analysis, patient risk assessment, or adverse event prediction. It covers:

- New software products in concept, development, or pre-market phases;
- Significant changes to existing classified software per SOP-DES-007 (Design Change Control);
- Software acquired through mergers, acquisitions, or technology licensing that will be integrated into Meridian's Clinical AI Platform;
- AI/ML models that drive clinical decisions or influence patient care pathways;
- Software components embedded within the MedInsight Analytics platform that present clinical risk scores or care gap recommendations to providers;
- Standalone mobile applications and API services delivering clinical AI functionality.

### 1.3 Out of Scope

The following are explicitly out of scope:

- Software solely performing administrative, billing, or practice management functions (covered under SOP-FIN-011);
- HealthPay Financial Services payment processing algorithms, even if they incorporate patient data (covered under SR 11-7 model risk governance);
- Population health dashboards that aggregate de-identified data without generating patient-specific clinical recommendations;
- Internal research tools not deployed to clinical environments.

### 1.4 Applicability

This SOP is binding upon all Clinical AI Products personnel, including software engineers, product managers, quality assurance specialists, regulatory affairs staff, and clinical evaluators. Contractors, consultants, and third-party development partners engaged in Clinical AI Products development must acknowledge and comply with this SOP as a condition of engagement per SOP-QUAL-001 (Supplier Quality Management).

---

## 2. Definitions and Acronyms

### 2.1 Definitions

| Term | Definition |
|---|---|
| **Software as a Medical Device (SaMD)** | Software intended to be used for one or more medical purposes that perform these purposes without being part of a hardware medical device (IMDRF/SaMD WG/N10:2013). |
| **Medical Device Software (MDSW)** | Software that is a medical device in its own right under EU MDR Article 2(1), regardless of platform or location. |
| **Intended Purpose** | The objective and intended use of the software as defined by the manufacturer, describing the medical condition, patient population, user profile, and clinical function. |
| **Risk Class** | The regulatory classification assigned to a medical device based on risk to patient and user: Class I, IIa, IIb, or III under EU MDR Annex VIII; Class I, II, or III under FDA 21 CFR. |
| **Software Safety Classification** | IEC 62304 classification assigning software to Class A (no harm), Class B (non-serious injury), or Class C (death or serious injury). |
| **Significant Change** | A modification to software that changes the intended purpose, introduces new risk dimensions, or substantively alters clinical functionality. Per SOP-DES-007. |
| **Algorithm Change Protocol (ACP)** | The predefined plan for updating AI/ML models, including triggers for reclassification review. |
| **Clinical Investigation** | Systematic clinical evaluation involving human subjects to establish safety and performance. |
| **Post-Market Surveillance (PMS)** | Proactive monitoring of deployed software to detect safety signals, performance degradation, or unintended use patterns. |

### 2.2 Acronyms

| Acronym | Definition |
|---|---|
| CMO | Chief Medical Officer |
| CRO | Clinical Regulatory Officer |
| DHF | Design History File |
| EUDAMED | European Database on Medical Devices |
| IFU | Instructions for Use |
| IMDRF | International Medical Device Regulators Forum |
| MDS2 | Manufacturer Disclosure Statement for Medical Device Security |
| NB | Notified Body |
| NCR | Non-Conformance Report |
| QMS | Quality Management System |
| RMF | Risk Management File |
| SaMD | Software as a Medical Device |
| SOUP | Software of Unknown Provenance |
| SRS | Software Requirements Specification |
| UDI | Unique Device Identification |

---

## 3. Roles and Responsibilities

### 3.1 Responsibility Matrix

The following RACI matrix defines accountability for each activity within this SOP:

| Activity | VP Clinical AI | CMO | Regulatory Affairs Lead | Software Engineering Director | Clinical Evaluation Lead | Quality Assurance Manager |
|---|---|---|---|---|---|---|
| Classification Decision (initial) | A | R | C | C | C | I |
| Intended Purpose Statement Approval | R | A | C | I | C | I |
| IEC 62304 Safety Classification | A | R | C | C | C | C |
| AI-Specific Risk Assessment | R | A | C | I | C | C |
| Post-Market Reclassification Trigger | A | R | R | I | C | I |
| Exception Approval | R | A | C | I | I | I |
| Notified Body Communication | I | I | A/R | I | I | I |

**Key:** R = Responsible (executes the work), A = Accountable (approves the decision), C = Consulted (provides input), I = Informed

### 3.2 Named Role Responsibilities

#### 3.2.1 VP of Clinical AI Products (Dr. Aisha Okafor)
- Serves as SOP Owner and retains final accountable authority for all software classification decisions within the business unit;
- Approves classification determinations for Class IIb/III (EU) and Class III (FDA) products;
- Escalates disputed classifications to the CMO and Quality Review Board;
- Reviews and approves updates to this SOP.

#### 3.2.2 Chief Medical Officer (Dr. Priya Patel)
- Provides ultimate clinical authority for intended purpose statements;
- Validates that classification determinations accurately reflect clinical risk;
- Approves clinical evaluation plans generated from classification outcomes;
- Serves as approver for this SOP and designated approver for exception handling.

#### 3.2.3 Regulatory Affairs Lead
- Prepares classification determination documentation and regulatory rationale memos;
- Maintains current knowledge of EU MDR, FDA SaMD guidance, IMDRF framework, and EU AI Act requirements;
- Manages notified body communications and pre-submission meetings with regulators;
- Maintains the Product Classification Register (see Section 6.1).

#### 3.2.4 Software Engineering Director
- Informs classification process with technical architecture details, algorithm behavior descriptions, and integration dependencies;
- Ensures that software development activities align with the assigned safety classification per IEC 62304;
- Reports significant changes per SOP-DES-007 that may trigger reclassification.

#### 3.2.5 Clinical Evaluation Lead
- Provides clinical evidence supporting intended purpose statements and clinical association claims;
- Contributes to risk class determination by identifying clinical hazards and potential harms;
- Participates in post-market surveillance review for deployed software.

#### 3.2.6 Quality Assurance Manager
- Audits classification documentation for completeness and QMS compliance;
- Verifies that design controls implemented match the assigned classification;
- Initiates non-conformance reports when classification procedures are not followed.

---

## 4. Policy Statements

### 4.1 Classification-Based Design Governance

Meridian's Clinical AI Products business unit shall classify every software product, module, and significant update before design and development activities commence, and prior to any regulatory submission. Classification cannot be deferred, waived, or conducted retrospectively. Products shall not progress beyond Gate 2 of the Product Development Lifecycle (see SOP-DES-005) without a finalized and approved classification determination.

### 4.2 Regulatory Alignment

Classification determinations shall simultaneously address:

- EU MDR 2017/745 Annex VIII classification rules, specifically Rules 11 (software), 4–8 (active devices), and 9–10 (therapeutic/diagnostic classification);
- FDA SaMD guidance and applicable device classification regulations (21 CFR Parts 862–892);
- IEC 62304 safety classification;
- EU AI Act risk categorization for products incorporating artificial intelligence or machine learning;
- IMDRF SaMD Framework (N12) for risk categorization by clinical situation and significance.

### 4.3 Documentation Mandate

Every classification determination shall be documented using Form CLIN-002-F01 (Software Classification Determination Record) and retained within the product's DHF. The documentation shall include a traceable rationale referencing the specific regulatory rules applied. Classification decisions without documented rationale are considered invalid.

### 4.4 Reclassification Triggers

A software product shall be reclassified when any of the following occur:

- Intended purpose changes;
- New clinical functionality is added that introduces new risk dimensions;
- Post-market surveillance data reveals a change in risk profile;
- Regulatory guidance or device classification rules change;
- Notified body or FDA feedback indicates classification disagreement.

Reclassification shall follow the same procedure as initial classification per Section 5 of this SOP.

### 4.5 EU AI Act High-Risk Classification

All software products incorporating AI/ML that qualify as medical devices shall additionally undergo EU AI Act high-risk assessment. Classification as high-risk under the EU AI Act shall trigger additional quality management system requirements for high-risk AI systems as defined in the regulation. Meridian maintains human oversight mechanisms for all AI-driven clinical functions across all risk levels. Transparency documentation shall accompany all product labeling per applicable transparency requirements.

### 4.6 Prohibition on Pre-Classification Regulatory Submissions

No regulatory submission, including 510(k), De Novo request, CE marking technical documentation submission, or UKCA application, shall proceed without an approved classification determination. Products without finalized classifications shall not be marketed, sold, or deployed in clinical environments.

---

## 5. Detailed Procedures

### 5.1 Classification Initiation

#### 5.1.1 Triggers

The classification procedure shall be initiated by the Product Manager or Engineering Lead upon:

1. Concept approval for a new Clinical AI product;
2. Detection of a significant change to an existing classified product per SOP-DES-007;
3. Receipt of post-market surveillance data indicating potential reclassification need;
4. Changes to applicable regulations that affect existing classifications;
5. Integration of acquired technology into the Clinical AI Platform.

#### 5.1.2 Initiation Steps

1. **Product Manager** completes Section A of Form CLIN-002-F01 capturing product identifier, concept description, and initial intended purpose hypothesis.
2. **Product Manager** submits Form CLIN-002-F01 to the **Regulatory Affairs Lead** via Meridian's QMS (Qualio platform, module "Classification Workflow").
3. **Regulatory Affairs Lead** logs the classification request in the Classification Register (see Section 6.1) within 2 business days and assigns a tracking ID.

### 5.2 Intended Purpose Definition

#### 5.2.1 Requirements

The Intended Purpose Statement must be finalized before classification rules can be applied. The statement shall address, at minimum:

- Medical condition(s) addressed;
- Patient population (including excluded populations);
- Intended user profile (e.g., radiologist, cardiologist, general practitioner, patient);
- Clinical function performed (diagnosis, prognosis, monitoring, treatment planning, triage, etc.);
- Clinical output type (numeric score, categorical classification, image overlay, alert, recommendation);
- Integration context (standalone, PACS-integrated, EHR-embedded);
- Level of automation (fully autonomous, assistive/recommendation, triage);
- Geographic markets intended for deployment.

#### 5.2.2 Procedure

1. **Clinical Evaluation Lead** drafts the Intended Purpose Statement using Template CLIN-002-T01.
2. **Regulatory Affairs Lead** reviews the draft for regulatory sufficiency and alignment with IMDRF SaMD definitions.
3. **Software Engineering Director** reviews for technical accuracy regarding algorithm output description.
4. **Product Manager** validates alignment with product concept and commercial strategy.
5. **CMO** reviews and approves the final Intended Purpose Statement.
6. **Regulatory Affairs Lead** records the finalized statement in Form CLIN-002-F01 Section B.

**Timeline:** Intended Purpose definition shall be completed within 15 business days of classification initiation.

### 5.3 EU MDR Classification (Annex VIII)

#### 5.3.1 Rule Application

The **Regulatory Affairs Lead** shall apply EU MDR Annex VIII classification rules in sequence:

1. **Rule 11** — Software-specific rule: Determine if software drives or influences the use of a medical device. If yes, classify per the driven device. If standalone:
   - **Rule 11a**: Software intended to provide information for diagnostic or therapeutic decisions → minimum Class IIa, unless decisions may cause serious deterioration (Class IIb) or death (Class III).
   - **Rule 11b**: Software intended to monitor physiological processes → minimum Class IIa, unless monitoring vital parameters where nature of variations could result in immediate danger → Class IIb.
   - **Rule 11c**: Software intended to diagnose or treat → Class IIa minimum, Class III if it diagnoses or screens for a disease in a manner that could result in serious deterioration or death.

2. **Rules 9 and 10** — Apply when software is an active therapeutic or diagnostic device:
   - Rule 9: Active therapeutic devices (energy delivery/monitoring) → risk escalation to Class IIb or III.
   - Rule 10: Active diagnostic devices (including monitoring) → Class IIa minimum.

3. **Cross-reference IMDRF N12** for SaMD risk categorization to ensure alignment between EU and international frameworks.

#### 5.3.2 Classification Documentation

The **Regulatory Affairs Lead** shall produce a "Regulatory Classification Rationale Memo" containing:

- Rule-by-rule analysis with justification for rules applied and not applied;
- Rationale for final classification with supporting clinical evidence;
- Comparable device classifications (predicate analysis for FDA alignment);
- Risk class determination with confidence assessment;
- Regulatory pathway recommendation (CE marking via self-declaration, Annex IX, or Annex X plus notified body audit).

**Quality Assurance Manager** reviews the memo for logical consistency, completeness, and QMS compliance before submission to the **VP of Clinical AI Products** for approval.

#### 5.3.3 Escalation Criteria

Classification determinations shall be escalated to the CMO when:

- Product is borderline between Class IIb and III;
- Rule 11c may apply (diagnosis leading to serious deterioration or death);
- Product includes autonomous decision-making without human intermediary;
- Clinical Evaluation Lead and Regulatory Affairs Lead disagree on classification;
- Notified body pre-submission feedback is ambiguous.

### 5.4 FDA Classification Determination

#### 5.4.1 Procedure

For products intended for US market deployment, the **Regulatory Affairs Lead** shall:

1. Determine if the software meets the definition of a medical device under Section 201(h) of the FD&C Act.
2. Search FDA classification regulations (21 CFR Parts 862–892) for applicable device types and product codes.
3. If no applicable classification regulation exists, classify as a De Novo candidate and prepare a classification request rationale.
4. Determine applicable premarket submission pathway: exempt, 510(k), De Novo, or PMA.
5. Document FDA classification determination in Form CLIN-002-F01 Section C.

#### 5.4.2 Dual-Market Products

Products deployed in both EU and US markets shall undergo parallel classification determination. If EU and FDA classifications differ (e.g., EU Class IIb vs FDA Class II), both classifications shall be documented, and the more stringent classification shall govern design control activities unless specific regulatory guidance dictates otherwise.

### 5.5 IEC 62304 Software Safety Classification

#### 5.5.1 Classification Criteria

Following EU MDR classification, the **Software Engineering Director** shall assign the IEC 62304 software safety classification based on the potential for creating hazardous situations:

| Safety Class | Description | Risk Criterion |
|---|---|---|
| A | No hazard | No risk of injury |
| B | Non-serious injury | Software failure may cause minor or reversible injury |
| C | Death or serious injury | Software failure may cause death or permanent impairment |

#### 5.5.2 Assignment Procedure

1. **Software Engineering Director** reviews the finalized risk management file (RMF) for the product per SOP-RISK-003.
2. Hazard severity analysis determines the worst-case harm from software failure.
3. Classification is documented in the Software Development Plan (SDP) per SOP-DES-005.
4. All downstream software development activities (documentation rigor, testing requirements, review procedures) are then scoped per IEC 62304 requirements for the assigned safety class.

**Note:** Software integrated into a larger medical device system inherits the safety classification of the parent device unless independent hazard analysis justifies a deviation.

### 5.6 EU AI Act High-Risk Classification

#### 5.6.1 Applicability

Any Clinical AI product that is already classified as a medical device under EU MDR and utilizes artificial intelligence or machine learning techniques shall undergo EU AI Act risk categorization assessment.

#### 5.6.2 Procedure

1. **Regulatory Affairs Lead** determines if the AI/ML functionality qualifies the product as a high-risk AI system under the EU AI Act, focusing on Annex III categories that may apply to medical devices.

2. **Regulatory Affairs Lead** documents the determination, including risk category assessment, in Form CLIN-002-F01 Section E.

3. For high-risk AI systems, the **Regulatory Affairs Lead** shall:
   - Document quality management system requirements triggered;
   - Verify that technical documentation requirements are addressed in the DHF structure;
   - Coordinate with Engineering to ensure appropriate risk management documentation is in place;
   - Initiate human oversight procedure documentation, ensuring that qualified human operators are identified for each AI-driven clinical function;
   - Ensure that transparency documentation is prepared for inclusion in product labeling and instructions for use.

### 5.7 Classification Review and Approval

#### 5.7.1 Review Gates

The classification determination shall pass through three review gates:

| Gate | Reviewer(s) | Criteria |
|---|---|---|
| Gate 1: Technical Accuracy | Software Engineering Director, Clinical Evaluation Lead | Algorithm description matches intended purpose; clinical hazards correctly identified |
| Gate 2: Regulatory Sufficiency | Regulatory Affairs Lead (peer review by second regulatory specialist) | All applicable rules addressed; rationale traceable; predicate analysis complete |
| Gate 3: Clinical Authority | CMO or designate | Clinical risk assessment validated; intended purpose clinically sound |

#### 5.7.2 Final Approval

Final approval authority is tiered by classification:

| Classification | Approver |
|---|---|
| EU Class I / FDA Class I | Regulatory Affairs Lead |
| EU Class IIa / FDA Class II | VP of Clinical AI Products |
| EU Class IIb / Class III; FDA Class III | CMO |

The approved Form CLIN-002-F01 and supporting Regulatory Classification Rationale Memo shall be uploaded to the product DHF in Qualio within 3 business days of approval.

### 5.8 Post-Market Reclassification Review

#### 5.8.1 Scheduled Review

All SaMD products shall undergo annual classification review as part of the post-market surveillance (PMS) cycle per SOP-PMS-004. The review shall evaluate:

- Post-market adverse event data;
- User feedback indicating off-label or unintended use;
- Published literature on comparable devices;
- Changes to regulatory classification rules or guidance.

#### 5.8.2 Event-Triggered Review

An unscheduled reclassification review shall be triggered per SOP-PMS-004 when any of the following events occur:

- Serious adverse event attributed to the software;
- Trend analysis demonstrating unexpected harm patterns;
- Notified body or FDA inquiry regarding classification;
- Internal audit finding of classification discrepancy;
- Product integration into a new clinical context or patient population.

#### 5.8.3 Procedure

Reclassification follows the same procedure as initial classification (Section 5.3–5.7). The revised classification determination supersedes all prior classifications. Products awaiting reclassification shall not be marketed or deployed until the reclassification review is complete.

---

## 6. Controls and Safeguards

### 6.1 Product Classification Register

The **Regulatory Affairs Lead** shall maintain a centralized Product Classification Register in Qualio containing for each product:

- Product identifier and version;
- Intended purpose statement (current);
- EU MDR classification (rule applied, rationale reference);
- FDA classification (product code, submission pathway);
- IEC 62304 safety class;
- EU AI Act risk category determination (if applicable);
- Classification determination date and approver;
- Next scheduled review date;
- Reclassification history.

The Register shall be reviewed quarterly by the **Quality Assurance Manager** for completeness and accuracy. Gaps shall trigger a CAPA per SOP-QUAL-004 (Corrective and Preventive Action).

### 6.2 Design Control Alignment

Upon classification finalization, the **Software Engineering Director** shall:

1. Update the Software Development Plan (SDP) to reflect the assigned IEC 62304 safety class;
2. Verify that requirements specifications, architecture documentation, and testing plans meet the documentation rigor appropriate to the safety class;
3. For Class C software: ensure independent verification and validation (IV&V) resources are assigned;
4. For AI/ML products classified as high-risk under the EU AI Act: ensure the Data Quality Plan and Model Governance Plan are established.

### 6.3 Classification Freeze

Classification determinations shall be frozen (locked from editing in Qualio) upon approval and prior to:

- Regulatory submission (510(k), CE marking technical documentation, De Novo request);
- Clinical investigation initiation;
- Commercial release.

Unfreezing requires documented rationale submitted by the **Regulatory Affairs Lead** and approval by the **CMO** or **VP of Clinical AI Products** as appropriate per Section 5.7.2.

### 6.4 Algorithm Change Protocol (ACP)

For AI/ML-driven SaMD products, an Algorithm Change Protocol shall be established per SOP-AI-005 specifying:

- Types of model updates that constitute significant changes vs. continuous learning updates;
- Reclassification evaluation triggers (performance threshold changes, input data shifts, output interpretation changes);
- Documentation requirements for each update type;
- Validation requirements proportional to classification risk.

The ACP shall be reviewed and approved during initial classification and updated whenever the product risk classification changes.

### 6.5 Documentation Retention

All classification documentation, including Form CLIN-002-F01, Regulatory Classification Rationale Memos, review records, and approved Intended Purpose Statements, shall be retained in Qualio for the product lifecycle plus a minimum of:

- EU MDR: 10 years after last device placed on market (15 years for implantable equivalents);
- FDA: 2 years after the product is no longer marketed in the US (minimum, Meridian policy extends to 15 years).

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Monitoring Mechanisms

#### 7.1.1 Continuous Monitoring

- **Qualio Dashboard:** Real-time tracking of classification workflow status for all active products, with automated alerts for overdue reviews or incomplete documentation.
- **CAPA Integration:** Non-conformances related to classification errors are automatically linked to a CAPA record in SOP-QUAL-004.

#### 7.1.2 Periodic Audits

The **Quality Assurance Manager** shall conduct classification compliance audits semi-annually (per SOP-QUAL-005, Internal Audit Program), sampling a minimum of 30% of active products or 5 products, whichever is greater.

### 7.2 Key Performance Indicators (KPIs)

| KPI | Definition | Target | Measurement Frequency |
|---|---|---|---|
| Classification Cycle Time | Days from initiation to final approval | ≤ 30 days (Class I/IIa); ≤ 45 days (Class IIb/III) | Monthly |
| Post-Market Reclassification Timeliness | Percentage of scheduled PMS reviews completed within ±15 days of due date | ≥ 95% | Quarterly |
| Classification Documentation Completeness | Percentage of DHF records containing all required classification documentation (Form CLIN-002-F01, Rationale Memo, approval signatures) | ≥ 98% | Quarterly |
| Misclassification Incidents | Number of products determined by notified body or FDA to be misclassified during active review cycle | 0 | Annually |
| CAPA Cycle Time | Days from NCR initiation to CAPA closure for classification-related CAPAs | ≤ 60 days | Monthly |

### 7.3 Reporting Cadence

| Report | Audience | Frequency | Content |
|---|---|---|---|
| Classification Register Status Report | VP of Clinical AI Products, CMO | Quarterly | All active classifications, upcoming review dates, open CAPAs related to classification |
| PMS Classification Review Summary | Clinical Evaluation Lead | Annually per product | Outcome of annual reclassification review |
| Audit Findings Report | CMO, Quality Review Board | Semi-annually | Results of classification compliance audits, identified non-conformances, remediation plans |

Metrics dashboards shall be maintained in Meridian's analytics platform (Tableau, Clinical AI Products Operational Dashboard) with direct feeds from Qualio and the CAPA tracking system.

---

## 8. Exception Handling and Escalation

### 8.1 Exception Types

Exceptions to this SOP may be requested for:

- **Expedited Classification:** Regulatory urgency (e.g., response to competitor product classification change, regulator inquiry requiring reclassification within 5 business days);
- **Parallel Classification and Development:** Permitting limited design activities (up to Gate 2 of SOP-DES-005) while classification is in progress, when business or clinical need is urgent;
- **Classification Disagreement Resolution:** When the classification determination team cannot reach consensus;
- **Regulatory Divergence:** When EU and FDA classification pathways are incompatible or conflicting.

### 8.2 Exception Request Procedure

1. **Requestor** completes Form SOP-ADM-001-F02 (SOP Exception Request) describing:
   - Specific SOP section for which exception is sought;
   - Rationale and justification (regulatory, clinical, or business);
   - Proposed alternative approach;
   - Risk assessment of the alternative approach;
   - Duration (if temporary exception).

2. **Regulatory Affairs Lead** reviews the request and provides a regulatory risk opinion within 3 business days.

3. **VP of Clinical AI Products** reviews and either approves or denies the exception. For exceptions related to Class IIb or Class III products, approval escalates to the **CMO**.

4. Approved exceptions shall be documented in Qualio, linked to the affected product classification record, assigned an expiration date (if temporary), and tracked quarterly for compliance.

### 8.3 Expedited Exception SLAs

For expedited exceptions:

- Regulatory Affairs Lead review and opinion: ≤ 1 business day;
- Final decision: ≤ 2 business days from request submission;
- Documentation completion: ≤ 1 business day after approval.

Expedited exceptions are valid for 30 days unless a renewal request is submitted and approved. No more than two consecutive renewals are permitted before full classification must be completed.

### 8.4 Escalation Pathways

Disputes not resolved by the classification determination team shall be escalated as follows:

1. **Level 1:** VP of Clinical AI Products, Clinical Evaluation Lead, Regulatory Affairs Lead — collaborative review and consensus-seeking;
2. **Level 2:** CMO review and binding decision;
3. **Level 3:** Quality Review Board review for systemic issues or precedent-setting situations.

Escalation shall not delay regulatory submissions unless the escalation specifically concerns a classification that materially affects the submission pathway.

### 8.5 Non-Conformance Handling

Classification procedure non-conformances identified during internal audits or post-market activities shall be documented in an NCR per SOP-QUAL-004. Root cause analysis shall be completed within 30 days. Repeat non-conformances (similar root cause within 12 months) shall trigger a mandatory escalation to the CMO and Quality Review Board.

---

## 9. Training Requirements

### 9.1 Required Training

All personnel with classification-related responsibilities, as designated in Section 3, shall complete:

| Training Module | Description | Duration | Delivery Method |
|---|---|---|---|
| CLIN-002-TRN-01 | SOP-CLIN-002 Overview and Classification Fundamentals | 2 hours | eLearning (Qualio LMS) |
| CLIN-002-TRN-02 | EU MDR Annex VIII Classification Rules: Practical Application | 4 hours | Instructor-led workshop (annual) |
| CLIN-002-TRN-03 | IEC 62304 Safety Classification and Design Control Alignment | 3 hours | eLearning + Virtual simulation |
| CLIN-002-TRN-04 | EU AI Act Classification and High-Risk System Requirements | 2 hours | eLearning (updated annually) |
| CLIN-002-TRN-05 | Qualio Classification Workflow Navigation | 1 hour | eLearning + Knowledge check |

### 9.2 Role-Specific Training Tracks

| Role | Required Modules | Assessment |
|---|---|---|
| Product Manager | TRN-01, TRN-05 | Knowledge check (80% pass threshold) |
| Regulatory Affairs Staff | TRN-01 through TRN-05 | Certification exam (90% pass threshold) |
| Software Engineers | TRN-01, TRN-03, TRN-05 | Knowledge check (80%) |
| Clinical Evaluation Staff | TRN-01, TRN-02, TRN-04 | Case-study application assessed by Regulatory Affairs Lead |
| Quality Assurance Auditors | TRN-01, TRN-02, TRN-03, TRN-05 | Auditor competency assessment |

### 9.3 Training Frequency

- Initial training: Within 30 days of role assignment or hire;
- Refresher training: Annual for all roles; Regulatory Affairs staff additionally complete quarterly regulatory watch updates covering classification-related guidance changes;
- Just-in-time training: When new regulatory guidance is published affecting classification (e.g., updated MDCG guidance, new FDA SaMD guidance), a targeted training update shall be developed and deployed within 45 calendar days.

### 9.4 Training Tracking

All training completions, assessment scores, and refresher dates shall be recorded in Meridian's Learning Management System (Workday Learning). The **Quality Assurance Manager** shall review training compliance quarterly and escalate overdue training to the relevant department head.

Regulatory Affairs personnel who fail the certification exam (TRN-02, TRN-03) on first attempt shall complete a remediation plan within 14 calendar days and retake the exam. Failure on second attempt triggers a mandatory review of the individual's classification responsibilities.

---

## 10. Related Policies and References

### 10.1 Internal Meridian SOPs

| SOP ID | Title | Relationship |
|---|---|---|
| SOP-DES-005 | Product Development Lifecycle Governance | Gate alignment; classification as pre-requisite for Gate 2 passage |
| SOP-DES-007 | Design Change Control | Significant change triggers reclassification review |
| SOP-RISK-003 | Medical Device Risk Management (ISO 14971) | Hazard severity analysis informing IEC 62304 safety class |
| SOP-QUAL-001 | Supplier Quality Management | Third-party developer compliance and training |
| SOP-QUAL-004 | Corrective and Preventive Action (CAPA) | NCR handling for classification-related non-conformances |
| SOP-QUAL-005 | Internal Audit Program | Semi-annual classification compliance audits |
| SOP-PMS-004 | Post-Market Surveillance for Medical Device Software | Annual reclassification review; event-triggered review criteria |
| SOP-AI-005 | AI/ML Algorithm Change Management | ACP relationship to classification; continuous learning governance |
| SOP-REG-001 | CE Marking Technical Documentation | Classification as foundation for technical documentation structure |
| SOP-REG-003 | FDA Premarket Submission Preparation | 510(k) and De Novo pathway determination |
| SOP-FIN-011 | Non-Medical Software Classification (Financial/Administrative) | Boundary definition between clinical and administrative software |
| SOP-CYB-006 | Medical Device Cybersecurity Classification | Security classification alignment with safety classification |

### 10.2 External Standards and Guidance

| Reference | Title | Version/Year |
|---|---|---|
| EU MDR 2017/745 | Medical Device Regulation, Annex VIII | 2017 (applicable date May 26, 2021) |
| IMDRF/SaMD WG/N10 | Software as a Medical Device: Key Definitions | 2013 |
| IMDRF/SaMD WG/N12 | Software as a Medical Device: Possible Framework for Risk Categorization | 2014 |
| IEC 62304:2006 + AMD1:2015 | Medical Device Software — Software Life Cycle Processes | 2015 |
| ISO 14971:2019 | Medical Devices — Application of Risk Management | 2019 |
| FDA Guidance | Policy for Device Software Functions and Mobile Medical Applications | September 2019 |
| FDA Guidance | Clinical Decision Support Software | September 2022 |
| EU AI Act | Regulation (EU) 2024/1689 | 2024 |
| MDCG 2019-11 | Guidance on Qualification and Classification of Software in MDR | 2019 |
| MDCG 2020-1 | Guidance on Clinical Evaluation (MDR) / Performance Evaluation (IVDR) | 2020 |

### 10.3 Meridian Forms and Templates

| Form/Template ID | Name | Location |
|---|---|---|
| CLIN-002-F01 | Software Classification Determination Record | Qualio, Clinical AI Forms Library |
| CLIN-002-T01 | Intended Purpose Statement Template | Qualio, Templates Library |
| SOP-ADM-001-F02 | SOP Exception Request Form | Qualio, Quality Templates Library |
| CLIN-002-T02 | Regulatory Classification Rationale Memo Template | Qualio, Templates Library |
| CLIN-002-R01 | Product Classification Register | Qualio, Clinical AI Registers |

---

## 11. Revision History

| Version | Date | Author | Changes Summary | Approver |
|---|---|---|---|---|
| 1.0 | 2021-03-15 | Dr. Aisha Okafor | Initial release. EU MDR classification framework established. IEC 62304 safety classification integrated. | Dr. Priya Patel |
| 2.0 | 2022-06-01 | Dr. Aisha Okafor | Added FDA classification determination procedure (Section 5.4). Expanded Post-Market Reclassification (Section 5.8). Added dual-market product guidance. Updated training modules. | Dr. Priya Patel |
| 3.0 | 2023-11-10 | Dr. Aisha Okafor | Major revision. Integrated EU AI Act high-risk classification procedures (Section 5.6). Added Algorithm Change Protocol controls (Section 6.4). Expanded KPIs and metrics (Section 7). Revised exception handling SLAs. | Dr. Priya Patel |
| 3.1 | 2024-02-28 | Regulatory Affairs Lead (M. Chen) | Interim update. Corrected MDCG guidance references updated for 2023 publications. Modified classification escalation thresholds for Class IIb products. Added Clarification on SOUP classification exclusion. | Dr. Aisha Okafor |
| 4.0 | 2024-08-15 | Dr. Aisha Okafor | Comprehensive revision. Updated Intended Purpose definition procedure to mandate geographic market specificity. Refined EU AI Act high-risk classification process. Updated all external regulation references. Added escalation pathway (Level 3). Updated training modules and assessment thresholds. Reorganized Section 5 for workflow clarity. | Dr. Priya Patel |