---
sop_id: "SOP-CLIN-019"
title: "Clinical Data De-identification"
business_unit: "Clinical AI Products"
version: "1.7"
effective_date: "2024-10-09"
last_reviewed: "2025-01-22"
next_review: "2025-07-05"
owner: "Dr. Aisha Okafor, VP of Clinical AI Products"
approver: "Dr. Priya Patel, Chief Medical Officer"
classification: "Internal"
regulations:
  - "HIPAA"
  - "GDPR"
status: "Active"
---

# Standard Operating Procedure: Clinical Data De-identification

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the mandatory framework for the de-identification of Protected Health Information (PHI) and personal data within Meridian Health Technologies, Inc.’s Clinical AI Products business unit. The purpose of this SOP is to ensure that all clinical datasets used for model training, algorithm validation, product demonstration, and secondary research are rendered into a state where the risk of re-identification is mitigated to an acceptable legal and regulatory threshold, in alignment with HIPAA Privacy Rule, GDPR data protection principles, and internal AI governance commitments under the NIST AI Risk Management Framework (AI RMF).

De-identification is a foundational control enabling Meridian’s mission-critical activities—particularly the development of high-risk AI systems under the EU AI Act—while preserving patient privacy, maintaining the trust of our 340+ healthcare provider partners, and ensuring the integrity of the 12 million patient records managed under the MedInsight Analytics platform.

### 1.2 Scope

This SOP applies to all data in any structured, semi-structured, or unstructured format (including free-text clinical notes, DICOM imaging pixel data and headers, HL7v2 messages, FHIR R4 resources, and audio recordings of patient encounters) that meets all of the following criteria:

| Scope Criterion | Applicability |
| :--- | :--- |
| Data Contains Identifiers | The dataset includes at least one of the 18 HIPAA Safe Harbor identifiers or any personal data element as defined under GDPR Article 4(1). |
| Processing Purpose | The data is used for activities outside of direct patient treatment, payment, or healthcare operations for the originating covered entity. This includes model training, Research & Development (R&D), benchmarking, production of synthetic datasets, or product demonstrations. |
| Data Controller/Processor | Meridian acts as a Business Associate, Data Processor, or Co-Controller for the dataset in question. |
| Environment | Data resides within the Meridian SaaS Platform (AWS us-east-1, eu-west-1), Azure DR environments, or on approved local workstations governed by Meridian’s endpoint management. |

**Out of Scope:**
- Data used exclusively for providing real-time clinical decision support directly to an attending physician for a specific patient under a valid treatment relationship, where the full identified record is required and governed by SOP-CLIN-004 (Clinical Decision Support Data Handling).
- Anonymized data received from third-party data brokers under a contractual warranty that no identifiers exist, which is governed by SOP-DAT-007 (Third-Party Data Acquisition).
- Employee HR data, which is governed by SOP-HR-022 (Employee Data Privacy).

### 1.3 Applicability

All full-time employees, contractors, consultants, and interns within the Clinical AI Products business unit, the MedInsight Analytics team, the HealthPay Financial Services fraud model development team, and any Engineering roles with access to the Meridian data lake (Snowflake) must comply with this SOP. This SOP additionally binds any third-party vendors granted access to Meridian-managed clinical datasets.

---

## 2. Definitions and Acronyms

For the purposes of this SOP, the following terms shall be interpreted as defined below:

| Term / Acronym | Definition |
| :--- | :--- |
| **PHI** | Protected Health Information, as defined under 45 CFR § 160.103. |
| **De-identification** | The process by which health information is rendered neither to identify an individual nor provides a reasonable basis to identify an individual, per 45 CFR § 164.514. |
| **Safe Harbor** | A method of de-identification involving the removal of 18 enumerated identifiers, and actual knowledge by the covered entity/BA that remaining information cannot identify the individual. |
| **Expert Determination** | A method of de-identification where a qualified statistician applies analytical principles to render the risk of re-identification "very small," documenting the methods and results. |
| **Re-identification Risk** | The probability, on a scale from 0.0 to 1.0, that an unauthorized actor could link a de-identified record back to the data subject using reasonably available methods. |
| **Designated Record Set (DRS)** | A group of records maintained by or for a covered entity used in whole or in part to make decisions about individuals. |
| **Limited Data Set (LDS)** | PHI that excludes direct identifiers of the individual, relatives, employers, or household members, usable only with a Data Use Agreement. |
| **Pseudonymization** | A GDPR-compliant processing of personal data such that the data can no longer be attributed to a specific data subject without additional information (the "key"), provided the key is kept separately. This data remains "personal data." |
| **Data Subject** | An identified or identifiable natural person (the patient). |
| **k-Anonymity** | A privacy model ensuring that an individual's information in a dataset cannot be distinguished from at least k-1 individuals whose information also appears in the release. |
| **Dicomizer** | Meridian’s proprietary, internally-built tool for stripping PHI from DICOM pixel data (e.g., burned-in annotations) and headers (e.g., DICOM Tag (0010,0010) Patient Name). |
| **HIPAA** | Health Insurance Portability and Accountability Act of 1996, and its Privacy and Security Rules. |
| **GDPR** | General Data Protection Regulation (EU Regulation 2016/679). |
| **BA** | Business Associate. |
| **BAA** | Business Associate Agreement. |

---

## 3. Roles and Responsibilities

The following matrix defines the accountability model for de-identification activities. R = Responsible, A = Accountable, C = Consulted, I = Informed.

| Role / Title | Responsibility | RACI |
| :--- | :--- | :---: |
| **VP of Clinical AI Products**<br>(Dr. Aisha Okafor) | Owns the overall process; holds final sign-off for production de-identification pipeline deployments. | **A** |
| **De-identification Engineer**<br>(Clinical Data Engineering Team) | Executes the technical de-identification procedure, runs the Dicomizer tool, scripts Safe Harbor removal. Performs k-anonymity checks using the Meridian Privacy Analyzer (MPA) toolkit. | **R** |
| **Chief Medical Officer**<br>(Dr. Priya Patel) | Approver for all Expert Determination methodology reports; validates clinical context utility of de-identified datasets. | **A** (Expert Det.)<br>**C** (Safe Harbor) |
| **Data Privacy Officer (DPO)** | Consults on GDPR pseudonymization requirements and lawful basis documentation. Handles re-identification breach notification escalation. | **C** |
| **VP of Data Engineering**<br>(Kai Zhang) | Accountable for the maintenance of the Dicomizer and MPA technical infrastructure. Ensures the "key" for pseudonymized data is stored in an isolated vault. | **A** (Infrastructure)<br>**C** (Procedure) |
| **Machine Learning Engineers** | Consumed users of de-identified data; responsible for verifying the utility and format of received de-identified datasets before feeding into training pipelines (SOP-CLIN-021). | **I** |
| **QA & Validation Lead** | Responsible for running the quarterly re-identification attacks and validating the de-identification validation checklist. | **R** |
| **Business Unit Leaders** | Consulted for business impact analysis when a dataset cannot be used for a commercial purpose if identifiers must remain. | **C** |

---

## 4. Policy Statements

Meridian Health Technologies, Inc. commits to the following high-level policy mandates regarding clinical data privacy:

1.  **Privacy by Design:** All new Clinical AI product features, data pipelines, and analytical models shall incorporate de-identification as a default technical control prior to any non-treatment processing, consistent with the requirements for high-risk AI systems under the EU AI Act.
2.  **No Unauthorized Re-identification:** No employee shall attempt to re-identify a dataset unless they are a validated De-identification Engineer for the explicit purpose of performing a scheduled, controlled "re-identification attack" to calibrate risk, documented under Section 6.7 of this SOP. Unauthorized attempted re-identification is an immediate grounds for termination offense.
3.  **Utility Preservation:** De-identification methodologies shall balance maximum privacy with clinical utility. Procedures must document which Safe Harbor fields were "masked" (redacted with a placeholder) versus "generalized" (e.g., dates shifted), ensuring data science teams understand structural changes.
4.  **Data Minimization:** Only the minimum necessary PHI fields required to achieve the validated research or model-training purpose shall be included in the raw dataset submitted for de-identification.
5.  **Pseudonymization vs. Anonymization:** For GDPR-governed data, Meridian explicitly differentiates between anonymized data (out of scope of GDPR) and pseudonymized data (where the key is held by Meridian, still in scope). The lawful basis for processing pseudonymized clinical data shall be assessed. Meridian processes special category data under Article 9(2)(j) GDPR for scientific research purposes, where applicable.

---

## 5. Detailed Procedures

This section outlines the step-by-step procedural workflows.

### 5.1 Workflow Selection: Safe Harbor vs. Expert Determination

A De-identification Engineer must select the correct workflow based on the following decision matrix:

| Primary Use Case | Governing Regulation | Risk of "Burned-in" PHI* | Required Method |
| :--- | :--- | :--- | :--- |
| Large-scale ML model training on structured tabular data (labs, vitals, medication orders). | HIPAA | Low | **Safe Harbor** |
| NLP model training on free-text radiology reports or clinical notes from a single source system. | HIPAA | High (Mention of rare diseases, specific physician names). | **Expert Determination** |
| Release of an externally-facing open-source benchmark dataset for the research community. | GDPR & HIPAA | Medium | **Expert Determination** |
| Internal product demonstration to a prospective hospital client using existing Meridian data. | HIPAA | Medium (Requires realistic dates and locations for demo fidelity). | **Safe Harbor (LDS option)** |

*Burned-in PHI is patient identifiers physically burned into the pixel data of a medical image (e.g., a CT scan that has the patient's name on the top banner).

### 5.2 Procedure: The HIPAA Safe Harbor Method

This procedure is executed in the Meridian Secure Data Sandbox (AWS Account: `mrdn-clin-prod-sandbox`, VPC: `vpc-data-lake-east`).

**Step 5.2.1: Data Ingestion and Inventory**
1.  Ingest the raw dataset from the source (Epic Caboodle Clarity, external SFTP, or RedCap export) into a staging bucket (`s3://mrdn-phistaging`).
2.  Use the AWS Glue Crawler to infer the schema and populate the AWS Glue Data Catalog table `phistg_[project_code]`.
3.  Execute the `MeridianIdentifierScanner` Athena query (template: `sop_clin019_identifier_scan.sql`) to generate a comprehensive inventory of all columns containing potential HIPAA identifiers.

**Step 5.2.2: Removal of the 18 Identifiers**
1.  Using the inventory, build a Spark job in AWS Glue Studio to apply the following transformations to the raw staging table. All operations must be executed by a service role with limited permissions (`Role-SOP019-Executor`).

| # | Identifier Category | Meridian Transformation Rule |
| :---: | :--- | :--- |
| 1 | Names | Replace with a salted SHA-256 hash, unless required for name entity recognition (NER) model. If used, replace with a surrogate `[PATIENT_X]` generated by a map stored in the isolated Vault (`Vault-Naming`). |
| 2 | Geographic subdivisions smaller than State | Retain only the first 3 digits of the ZIP code if the total population within those 3-digit ZIPs exceeds 20,000 people according to the most recent US Census data embedded in the rule. Otherwise, set to NULL. |
| 3 | Dates (Birth, Admission, Discharge) | **Generalize:** Shift all dates by a random, consistent offset (per patient) between -30 to +90 days. Year-level granularity must be preserved. This offset value constitutes the "key" and must be deleted post-job, not stored. |
| 4 | Telephone/Fax Numbers | Set to NULL. |
| 5 | Email Addresses | Set to NULL. |
| 6 | Social Security Numbers | Set to NULL. |
| 7 | Medical Record Numbers (MRN) | Replace with a project-specific Study ID (`CLIN019_[random_UUID]`). The crosswalk is deleted. |
| 8 | Health Plan Beneficiary Numbers | Set to NULL. |
| 9 | Account Numbers (FIN) | Replace with `FIN_[random_UUID]`. The crosswalk is deleted. |
| 10 | Certificate/License Numbers | Set to NULL. |
| 11 | Vehicle Identifiers (VIN, Plate) | Set to NULL. |
| 12 | Device Identifiers and Serial Numbers | Retain, but only if essential for device-function analysis and the serial number is not otherwise easily linked to a patient. Generalize to a Device Type Category. |
| 13 | Web URLs | Set to NULL. |
| 14 | IP Addresses | Set to NULL. Data source origin is logged at the system level, not row level. |
| 15 | Biometric Identifiers | Set to NULL. |
| 16 | Full-face photos and comparable images | Pass entire image set through the `Dicomizer` tool for a pixel-level scrubbing pass, even if no banner exists. |
| 17 | Any other unique identifying number, code, or characteristic | The `MeridianIdentifierScanner` will flag columns with high cardinality not already categorized. A manual review by the De-identification Engineer is required. |
| 18 | Age > 89 | Censor any age field where the value is `> 89`. Replace with the aggregated category `90+`. |

**Step 5.2.3: Actual Knowledge Certification**
1.  The De-identification Engineer must review the remaining dataset and execute the Meridian `UniquenessProximity` algorithm.
2.  If a combination of remaining fields (e.g., Rare Disease + Occupation + Employer) creates a cell size smaller than `k=5`, those specific rows must be redacted.
3.  The Engineer signs the "Safe Harbor Attestation" (Form F-CLIN019a) certifying that they have no actual knowledge that the information could be used alone or in combination to identify an individual.

### 5.3 Procedure: The Expert Determination Method

This method is mandatory for all free-text clinical data, unstructured data, and any data intended for public release.

**Step 5.3.1: Selection of Qualified Statistician**
1.  The expert must be a qualified statistician with demonstrable experience in biomedical privacy. This may be the Meridian Data Privacy Officer (DPO) or an external contracted privacy expert (currently, `Kovan & Associates` under MSA-2024-88).
2.  The expert cannot be the Engineer who prepared the data.

**Step 5.3.2: Risk Analysis and Mitigation**
1.  The expert applies generally accepted statistical and scientific principles (e.g., k-anonymity, l-diversity, t-closeness, differential privacy) using the `Meridian Privacy Analyzer (MPA)`.
2.  A targeted "re-identification attack" (Section 6.7) is simulated using the MPA's adversarial module against a test subset of the data.
3.  The expert must produce an "Expert Determination Report" (Form F-CLIN019b) detailing:
    - The analytical methods used.
    - The measurement of re-identification risk.
    - The justification for why the risk is "very small" (specifically defined as a probability < 0.05 under a targeted attack scenario).
    - The clinical fields generalized, suppressed, or perturbed.

### 5.4 Procedure: The GDPR Pseudonymization Workflow

For data where a lawful basis for processing relies on pseudonymization rather than full anonymization (common when a future clinical re-link is contractually required by the Data Controller), the following workflow must be used:

1.  **Key Generation:** De-identification Engineer triggers the `PseudonymKeyManager` Lambda, generating a unique, cryptographically secure project key.
2.  **Identity Separation:** Patient identity data (Name, MRN, National ID Number) is physically moved to the `gdrp-privacy-vault` (AWS S3 bucket `s3://mrdn-gdpr-vault-eu-west-1`, encrypted with AWS KMS CMK `alias/gdpr-vault-key`).
3.  **Surrogation:** Clinical utility data is loaded into the processing sandbox with the surrogate identifier.
4.  **Consent Traceability:** If the Controller has provided a specific consent log for the processing activity, the Engineer links the surrogate ID to the consent assertion. This step addresses processing under a lawful basis for research.

### 5.5 De-identification Validation (The "Re-identification Resilience Score")

Before a de-identified dataset is released from the Sandbox to the `mrdn-clinical-curated` S3 bucket for ML training, it must pass an automated validation gate.

1.  **Pipeline:** AWS Step Function `mrdn-deid-validation-pipeline`.
2.  **Test Suite:**
    - **Prosecutor Re-identification Risk Check:** MPA runs a simulated attack (attacker has access to public voter registration data and hospital discharge logs) and scores the dataset risk. Score must be `>= 95` (out of 100) for Safe Harbor and `>= 99` for Expert Determination.
    - **Schema Compliance Check:** Verifies that the schema does not contain fields named `mrn`, `ssn`, `name`, `phone`.
    - **Free-Text NER Check:** A lightweight SpaCy model scans 20% of rows in the `clinical_note` field for residual PHI patterns (e.g., `\d{3}-\d{2}-\d{4}` for SSNs).
3.  **Gate Result:** PASS / FAIL. If FAIL, the Step Function notifies the QA Lead and the executing Engineer via SNS (`mrdn-deid-sops-topic`). The dataset is quarantined.

---

## 6. Controls and Safeguards

### 6.1 Technical Access Controls

- **Sandbox Isolation:** PHI-containing staging buckets live in a dedicated AWS account (`mrdn-phihosting`), network-isolated from the main production ML training VPCs. Data transfer is a one-way, audited pull to the de-id account.
- **Role-Based Access Control (RBAC):** Only roles authenticated via Meridian’s SSO (Azure Entra ID) and assigned to the `CLIN019-Engineers` security group can execute Glue jobs in the sandbox.

### 6.2 Administrative Safeguards

- **Data Use Agreements (DUAs):** All source data governed by an Expert Determination must be covered by a DUA that explicitly prohibits the recipient (Meridian) from re-identifying the data or contacting data subjects.
- **Limited Data Set Agreement:** If the Safe Harbor method requires retention of dates (Step 5.2.2, Generalization), the resulting dataset is a Limited Data Set. The De-identification Engineer must verify a signed LDS Agreement is on file for this project.

### 6.3 Audit Logging

AWS CloudTrail is enabled across all accounts. All `s3:GetObject` on `s3://mrdn-phistaging`, `glue:StartJobRun`, and `kms:Decrypt` calls are forwarded to the central SIEM (Sumo Logic). The log contains the dataset project code, IAM role of the executor, and timestamp.

### 6.4 De-identification Validation Checklist

Every dataset released must be accompanied by a digitally signed "De-identification Release Certificate" containing:
- [ ] `MeridianIdentifierScanner` inventory summary attached.
- [ ] HIPAA Safe Harbor Attestation OR Expert Determination Report approved by CMO.
- [ ] Re-identification Resilience Score: `PASS`.
- [ ] DUA/LDS verification (if applicable).
- [ ] Approval by VP of Clinical AI Products or delegate.

### 6.5 Breach Notification and Response

In the event Meridian discovers a breach of unsecured PHI that resulted from a failure in this SOP (e.g., a misconfigured bucket revealing unscrubbed data, a software bug in the Dicomizer), the following steps must be taken immediately:

1.  **Containment:** The De-identification Engineer must revoke all IAM permissions on the affected resource and quarantine the bucket/database within 1 hour.
2.  **Assessment:** The DPO and the Chief Information Security Officer (CISO) will conduct a risk assessment to determine the nature and extent of the PHI involved, the identity of affected individuals, and the probability of re-identification.
3.  **Notification:** If the incident involves unsecured PHI governed by HIPAA, Meridian will notify the affected Covered Entity without unreasonable delay. The Covered Entity is then responsible for notifying affected individuals, the Secretary of HHS, and prominent media outlets if required. Meridian will provide the Covered Entity with all necessary details to fulfill its breach notification obligations, including a forensic report of the incident, list of potentially compromised identifiers, and timeline of events.
4.  **Remediation:** The root cause (e.g., bug in `mrn-scrubber.py`) must be fixed, verified by the QA Lead, and a root cause analysis (RCA) document published to the SOP repository within 14 business days.

### 6.6 Data Subject Rights under GDPR

Data subjects whose data is held pseudonymized within Meridian systems have rights of access, rectification, and erasure. To invoke these rights, a validated request from the Data Controller must be submitted to the DPO. Meridian will use the pseudonym key vault to re-identify the specific records and satisfy the request, or permanently delete the record. Because the lawful basis for processing is typically documented for scientific research, certain rights may be limited per Article 89 GDPR. Requests for access are handled according to the Controller’s Data Processing Agreement.

### 6.7 Prohibition of Re-identification

No individual, including the qualified statistician performing an Expert Determination, may retain or output the re-identified dataset from the controlled testing environment. The purpose of a re-identification attack is solely to measure risk and destroy the re-identified output upon completion of the analysis.

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs)

The effectiveness and timeliness of data de-identification are tracked via the following KPIs, displayed on the Clinical AI Operational Excellence Grafana dashboard:

| KPI | Target | Measurement Method |
| :--- | :--- | :--- |
| **De-id Pipeline Run Time** | < 4 hours for datasets < 500GB | Monitored via Step Function execution time metric. |
| **Validation Gate Pass Rate** | > 99.5% on first run | Aggregated count of PASS / total run outcomes per quarter. |
| **Quarterly Re-id Attack Resilience** | 0 successful re-identifications per quarter | Scheduled output from MPA adversarial module. |
| **Audit Anomaly Rate** | < 0.01% of all S3 GetObject calls | SIEM (Sumo Logic) alerting based on deviation from baseline RBAC usage patterns. |

### 7.2 Reporting Cadence

- **Monthly:** Automated MPA report on residual uniqueness risk across all curated datasets is distributed to the VP of Clinical AI Products and Data Privacy Officer.
- **Quarterly:** A "Clinical Data Privacy Review" meeting is held, chaired by the Chief Medical Officer (CMO), with attendance from the VP of Clinical AI, DPO, and QA Lead. The meeting reviews all exceptions, the quarterly attack results, and any updates to re-identification risk statistics.

---

## 8. Exception Handling and Escalation

### 8.1 Exception Process

If a project team (e.g., a Machine Learning Engineer) requires a deviation from this SOP—for example, retaining a geographic identifier more granular than a 3-digit ZIP for a population health risk model—they must initiate the Exception process *prior* to altering the pipeline.

### 8.2 Request Submission

A "De-identification Exception Request" (Form F-CLIN019c) must be submitted via the Meridian ServiceNow portal (`Clinical AI > Data Privacy > Exception Request`). The form requires:
- Justification for why Safe Harbor or Expert Determination cannot meet the use case.
- Detailed technical documentation of the proposed compensating control (e.g., differential privacy with a specific epsilon value).
- A risk assessment from the DPO on the increased re-identification risk.

### 8.3 Approval Matrix

| Exception Risk Level | Approving Authority |
| :--- | :--- |
| **Low** (Safe Harbor violation mitigated by strong technological control, e.g., on-device processing, no human access) | VP of Clinical AI Products |
| **Medium** (Retention of a full identifier for a strictly internal, short-term audit purpose) | VP of Clinical AI Products + DPO |
| **High** (Retention of full dates of birth and geographic markers for a commercial product release) | Chief Medical Officer, VP of Clinical AI, and Data Privacy Officer jointly. |
| **Critical** (Any processing that does not fall under a valid lawful basis) | Not permissible; must be escalated to the Chief Legal Officer. |

All exceptions are granted for a maximum period of 12 months, after which they must be re-approved.

---

## 9. Training Requirements

### 9.1 Mandatory Training

All personnel within the applicability scope (Section 1.3) are required to complete the following annual training curriculum, managed through the Workday Learning Management System (LMS):

- **Module HIP-TRN-010: HIPAA Privacy and Security for Business Associates.** This foundational course covers PHI, the 18 identifiers, the distinction between PHI and De-identified Data, and Meridian’s obligations under a BAA.
- **Module SOP-CLIN019-TRN: Clinical Data De-identification Procedures.** This module is specific to this SOP and covers the Safe Harbor and Expert Determination workflows. A quiz with a minimum score of 85% is required to pass.

### 9.2 Cadence

Training shall be assigned upon onboarding (within the first 5 business days) and renewed annually. The LMS sends automated reminders 30, 14, and 7 days prior to an employee's training due date. Non-completion of training within 45 days of the due date results in an automatic temporary revocation of access to the AWS Clinical Sandbox accounts, overseen by the IAM Administrator.

---

## 10. Related Policies and References

### 10.1 Internal Meridian SOPs

| SOP ID | Title |
| :--- | :--- |
| SOP-INFRA-003 | AWS Account and VPC Segmentation and Security |
| SOP-INFRA-005 | IAM Role and Service Account Lifecycle Management |
| SOP-CLIN-004 | Clinical Decision Support Data Handling |
| SOP-CLIN-021 | Machine Learning Model Training Governance |
| SOP-SEC-012 | Security Incident and Breach Response Protocol |
| SOP-DAT-007 | Third-Party Data Acquisition and Validation |
| SOP-HR-022 | Employee Data Privacy |

### 10.2 External Standards and Regulations

- HIPAA Privacy Rule, 45 CFR § 164.514(a)-(c)
- HHS Guidance on Methods for De-identification of Protected Health Information (2012)
- GDPR, Articles 4(5), 25, 32, and 89
- NIST Internal Report (IR) 8222: A Risk Management Framework for AI
- NIST Special Publication (SP) 800-188: De-Identifying Government Data Sets

---

## 11. Revision History

| Version | Date | Author | Summary of Changes |
| :--- | :--- | :--- | :--- |
| 1.0 | 2020-03-15 | K. Zhang (Data Eng) | Initial draft created. Established Safe Harbor procedure only. |
| 1.3 | 2022-07-22 | L. Sterling (Privacy) | Added Expert Determination workflow and formalized roles into a RACI matrix in response to an internal audit finding. |
| 1.5 | 2023-09-01 | A. Okafor (VP, CAI) | Major revision incorporating GDPR requirements for EU expansion, adding the Pseudonymization workflow, and introducing the MPA Automated Pipeline Validation Gate in Section 5.5. |
| 1.6 | 2024-04-10 | A. Okafor (VP, CAI) | Updated the Breach Notification section in response to new FTC Health Breach Notification Rule interpretations; clarified that crosswalk destruction is required, not just isolation, for anonymization. |
| 1.7 | 2024-10-09 | A. Okafor (VP, CAI) | Replaced legacy Glue workflow with Step Function orchestration; updated Exception Handling to formalize ServiceNow submission; revised DPO notification procedures for the re-identification attack program; added k-anonymity to the QA gate. |