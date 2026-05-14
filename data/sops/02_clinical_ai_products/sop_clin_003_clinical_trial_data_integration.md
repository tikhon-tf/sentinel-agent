---
sop_id: "SOP-CLIN-003"
title: "Clinical Trial Data Integration"
business_unit: "Clinical AI Products"
version: "5.9"
effective_date: "2024-01-28"
last_reviewed: "2025-09-18"
next_review: "2026-03-21"
owner: "Dr. Aisha Okafor, VP of Clinical AI Products"
approver: "Dr. Priya Patel, Chief Medical Officer"
classification: "Internal"
regulations:
  - "HIPAA"
  - "GDPR"
status: "Active"
---

# Standard Operating Procedure: Clinical Trial Data Integration

## 1. Purpose and Scope

### 1.1 Purpose
This Standard Operating Procedure (SOP) establishes the framework, procedures, and controls for ingesting, validating, transforming, and integrating clinical trial data into the Meridian Health Technologies Clinical AI Platform and MedInsight Analytics environments. The purpose is to ensure that all clinical trial data incorporated into Meridian products meets rigorous standards for data integrity, traceability, regulatory compliance, and patient privacy, thereby ensuring the safety and efficacy of AI models trained or fine-tuned on such data.

### 1.2 Scope
This SOP applies to all employees, contractors, subcontractors, and third-party vendors involved in the end-to-end lifecycle of clinical trial data within Meridian Health Technologies, Inc. This includes, but is not limited to:

- **Data Acquisition:** The legal, regulatory, and commercial process of procuring clinical trial datasets from sponsors, Contract Research Organizations (CROs), academic medical centers, and data consortiums.
- **Data Ingestion:** The technical process of receiving data from external sources via secure transfer protocols into the Meridian AWS (us-east-1, eu-west-1) boundary.
- **Data Standards & Transformation:** The mapping and transformation of source data (e.g., CDISC SDTM, ADaM, non-standard legacy formats) into the Meridian Canonical Data Model (MCDM).
- **Data Quality Assurance:** The execution of automated and manual quality checks to assess completeness, conformance, and plausibility.
- **Data Integration:** The merging of validated trial data with Real-World Data (RWD) assets in the MedInsight Analytics platform for secondary analysis and Clinical AI model development.
- **Geographic Applicability:** This SOP applies globally across all Meridian offices (Boston, London, Berlin, Singapore, Toronto), with specific enhanced controls for data involving European Union data subjects as mandated by the General Data Protection Regulation (GDPR).

### 1.3 Out of Scope
- The collection of primary data directly from patients in Meridian-sponsored interventional clinical trials (Meridian does not currently act as a trial sponsor).
- The integration of genomic sequencing data (see SOP-RES-007: Genomic Data Management).
- The operational management of the HealthPay Financial Services platform.

---

## 2. Definitions and Acronyms

| Term | Definition |
| :--- | :--- |
| **ADaM** | Analysis Data Model. CDISC standard for analysis-ready datasets. |
| **Anonymization** | The irreversible process of rendering personal data non-personal, such that the data subject is no longer identifiable (per GDPR Recital 26), assessed against all means reasonably likely to be used. |
| **BIMO** | FDA Bioresearch Monitoring program, applicable to certain clinical data standards. |
| **CDISC** | Clinical Data Interchange Standards Consortium. Global standards for clinical research data. |
| **CRO** | Contract Research Organization. An external entity contracted to conduct clinical trial activities. |
| **Data Controller** | The entity which determines the purposes and means of the processing of personal data. |
| **Data Processor** | The entity which processes personal data on behalf of the Controller. |
| **DPIA** | Data Protection Impact Assessment. A process required by GDPR Art. 35 for high-risk processing. |
| **DPO** | Data Protection Officer. Dr. Klaus Weber, based in Berlin. |
| **eCRF** | Electronic Case Report Form. |
| **GDPR** | General Data Protection Regulation (Regulation (EU) 2016/679). |
| **MCDM** | Meridian Canonical Data Model. The internal, unified data schema for the Clinical AI Platform. |
| **PHI** | Protected Health Information. |
| **Pseudonymization** | The processing of personal data in such a manner that it can no longer be attributed to a specific data subject without additional information, provided such additional information is kept separately and subject to technical and organizational measures (GDPR Art. 4(5)). |
| **ROPA** | Record of Processing Activities (GDPR Art. 30). |
| **SDTM** | Study Data Tabulation Model. CDISC standard for tabulating clinical trial data. |
| **SLA** | Service Level Agreement. |
| **SOC 2** | Service Organization Control 2. An auditing procedure for managing customer data. |
| **TMF** | Trial Master File. A collection of essential documents for a clinical trial. |

---

## 3. Roles and Responsibilities

The following RACI matrix delineates the responsibility assignment for the Clinical Trial Data Integration lifecycle:

- **R: Responsible** (Executes the task)
- **A: Accountable** (Ultimate ownership, sign-off authority)
- **C: Consulted** (Subject matter expert, provides input)
- **I: Informed** (Kept up-to-date on progress/decisions)

| Activity / Decision Point | Data Ops Engineer | Clinical Data Steward | VP Clinical AI (Dr. Okafor) | DPO (Dr. Weber) | Security (CISO Kim) | Compliance (Anderson) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1. Data Acquisition Agreement & DPIA | I | C | A | R | C | C |
| 2. Secure File Transfer Setup | R | I | I | C | A | I |
| 3. Source-to-MCDM Mapping Spec | C | R | A | I | I | I |
| 4. Ingest & Validation Pipeline Execution | R | C | A | I | I | I |
| 5. Data Quality Exception Resolution | C | R | A | I | I | I |
| 6. GDPR Data Subject Access Request (DSAR) | I | I | C | A/R | C | C |
| 7. ROPA Update for New Data Source | I | C | C | R | I | A |
| 8. Approval of Anonymization Status | C | R | A | C | I | I |

---

## 4. Policy Statements

Meridian Health Technologies is committed to the responsible and compliant use of clinical trial data to power insights and AI-driven solutions. The following high-level policies govern this SOP:

- **Policy of Lawful, Fair, and Transparent Processing (GDPR Art. 5(1)(a)):** Meridian will only process clinical trial data containing personal data of EU data subjects after establishing a valid legal basis (e.g., data subject consent obtained by the Controller, or legitimate interest balanced against data subject rights) and ensuring full transparency as articulated in the Controller's privacy notice. Meridian, as a Processor, will verify this basis contractually.
- **Policy of Purpose Limitation (GDPR Art. 5(1)(b)):** Trial data will be integrated solely for the purposes of secondary research, clinical AI model development, and population health analytics as specified in the Data Use Agreement (DUA) with the data provider. Any new purpose requires a new DPIA and DUA amendment.
- **Policy of Data Minimization (GDPR Art. 5(1)(c)):** Meridian will only ingest data variables that are adequate, relevant, and limited to what is necessary for the defined analytical purpose. A mandatory variable-necessity review is part of the source-to-MCDM mapping process.
- **Policy of Storage Limitation (GDPR Art. 5(1)(e)):** Clinical trial data containing personal data will be retained only for the duration defined in the DUA and the associated ROPA. Automated data lifecycle policies in AWS S3 will enforce retention and secure deletion upon contract termination.
- **Policy of Integrity and Confidentiality (GDPR Art. 5(1)(f)):** Meridian employs state-of-the-art technical and organizational measures, including pseudonymization and encryption at rest and in transit, to ensure appropriate security of personal data against unauthorized or unlawful processing and against accidental loss, destruction, or damage.

---

## 5. Detailed Procedures

### 5.1 Phase 1: Data Acquisition and Intake

This phase covers the process from initial data identification through legal agreement execution and technical receipt.

#### 5.1.1 Data Source Identification
1.  A Meridian stakeholder (typically a Product Manager from the Clinical AI Products business unit or a Data Scientist) identifies a clinical trial dataset that could enhance a product feature.
2.  The stakeholder submits a "Data Acquisition Request" via the Jira Service Management (JSM) portal, selecting the "Clinical Data Intake" request type.
3.  The request must include:
    - Link to ClinicalTrials.gov identifier or EU Clinical Trials Register (EUCT) number.
    - Proposed analytical use case.
    - Estimated number of data subjects and volume (GB/TB).
    - Known geographic origin of data subjects (critical for GDPR flagging).

#### 5.1.2 Legal and Privacy Review
1.  The General Counsel, Maria Gonzalez, receives the JSM ticket and initiates a legal review of the data provider’s DUA template or drafts a new one.
2.  **GDPR-Specific Gate (Art. 35 Trigger):** If the dataset contains data of EU data subjects, the Data Protection Officer (Dr. Klaus Weber) is a mandatory approver and performs or commissions a Data Protection Impact Assessment (DPIA) before signature.
    - The DPIA describes the processing operations, assesses necessity and proportionality, evaluates risks to rights and freedoms, and details measures to mitigate those risks, including technical controls and pseudonymization.
    - The DPIA outcome is logged in the central Privacy Register (OneTrust), with a risk rating (Low, Medium, High). "High" residual risk requires consultation with the supervisory authority.
3.  The Compliance Officer (Thomas Anderson) verifies that the proposed use aligns with SOC 2 contractual commitments and internal data classification policies.
4.  Upon satisfactory review, the DUA is signed by an authorized Meridian officer.

#### 5.1.3 Secure Data Transfer Setup
1.  The VP of IT Operations, Samantha Torres, or her delegate, provisions a dedicated, encrypted AWS S3 bucket with a unique prefix (e.g., `meridian-clinical-trial-intake/provider-{id}/study-{id}`).
2.  The Data Ops Engineer configures a Secure File Transfer Protocol (SFTP) endpoint using AWS Transfer Family with Okta Single Sign-On (SSO) multi-factor authentication as the identity provider.
3.  An encryption strategy is established: data must be encrypted at rest using AWS Key Management Service (KMS) with a customer-managed key, and in transit via TLS 1.3.

### 5.2 Phase 2: Data Ingestion and Staging

#### 5.2.1 Data Landing
1.  The external data provider uploads the dataset(s) to the provisioned SFTP endpoint.
2.  A file manifest (CSV or Excel format) is required from the provider, containing:
    - Filename
    - Checksum (SHA-256)
    - File size
    - Description (e.g., "DM domain SDTM dataset")

#### 5.2.2 Automated Ingestion Pipeline
1.  Upon arrival of a file matching the manifest, an AWS EventBridge rule triggers a Step Functions state machine named `TrialDataIngestionWorkflow`.
2.  **Checksum Verification:** The workflow computes the SHA-256 checksum of the landed file and compares it to the manifest. A mismatch immediately halts the pipeline and triggers a PagerDuty alert to the Data Ops team.
3.  **Anti-Malware Scan:** The file is scanned in-place using CrowdStrike Falcon. A "malware detected" result quarantines the file and triggers a critical security incident response process.
4.  **Staging:** Successfully verified files are moved to a staging zone: `s3://meridian-clinical-trial-staging/provider-{id}/study-{id}/YYYY-MM-DD/`.
5.  **Metadata Registration:** The ingestion event is logged immutably in the Meridian Data Catalog (Apache Atlas), tagged with the SOP-ID `SOP-CLIN-003`.

### 5.3 Phase 3: Data Transformation and Standards Mapping

This is the most complex phase, standardizing heterogeneous source data into the MCDM.

#### 5.3.1 Source Data Profiling
1.  A Clinical Data Steward uses a SageMaker notebook (with restricted network access) to profile landed data, generating a report using the "YData Profiling" library.
2.  The report identifies all source variables, data types, value distributions, and a "GDPR Personal Data Flag" if variables contain direct identifiers or potentially quasi-identifiable data (defined per Meridian's internal re-identification risk thresholds).

#### 5.3.2 Mapping Specification
1.  The Clinical Data Steward documents a formal "Source-to-MCDM Mapping Specification" in a controlled spreadsheet (XLSX) stored in SharePoint.
2.  The specification must include:
    - Source Variable Name → MCDM Variable Name
    - Data Type Conversion (e.g., Char to Integer)
    - Value Transformation Logic (e.g., `SEX = 'M'` → `GENDER_CONCEPT_ID = 8507`, a SNOMED CT code)
    - Codelist Harmonization (e.g., mapping MedDRA terms from source to OMOP Standard Vocabulary concepts)
    - Date shifting logic (for pseudonymization, see Section 5.3.3)
    - **Variable Necessity Justification:** A mandatory column where the Steward confirms the mapped variable is necessary for the defined analytical purpose, fulfilling the data minimization principle.

#### 5.3.3 Pseudonymization Procedure
1.  All direct identifiers (Names, Medical Record Numbers, Social Security Numbers, etc.) are strictly prohibited for ingestion. The Data Ops pipeline is configured with a regex-based filter to reject any file containing pattern-matched direct identifiers.
2.  For identifiers integral to analysis (e.g., Site ID, Subject ID), an irreversible, salt-cryptographic hashing algorithm (SHA-256) with a key managed by HashiCorp Vault is applied, generating a Meridian Subject Key (MSK).
3.  Dates (Birth, Screening, Visit, AE Start) are algorithmically shifted by a random, study-specific offset (between -90 and +90 days) to maintain temporal relationships for analysis while preventing re-identification. The original dates are discarded.

#### 5.3.4 Transformation Pipeline Execution
1.  The Data Ops Engineer translates the Mapping Specification into a DBT (data build tool) SQL or Python transformation model.
2.  The DBT model is committed to a Git repository (GitHub Enterprise), must undergo a peer review, and is executed via a CI/CD pipeline.
3.  The transformation run creates the MCDM-compliant datasets in the `meridian-integrated-clinical-trial` S3 bucket, partitioned by `study_id` and `data_version`.

### 5.4 Phase 4: Data Quality Assurance

#### 5.4.1 Automated Quality Checks
The transformation pipeline runs a suite of automated quality checks using the "Great Expectations" framework. Checks include:

| Check Category | Description | Threshold | Action on Failure |
| :--- | :--- | :--- | :--- |
| **Completeness** | Percentage of non-null values in mandatory MCDM columns (e.g., `SUBJECT_KEY`, `AETERM`). | > 99.5% | Pipeline stops; error queue to Steward. |
| **Conformance** | Source values match expected codelists (e.g., `SEX` in ['M','F']). | 100% | Pipeline stops; error queue to Steward. |
| **Uniqueness** | `SUBJECT_KEY` is unique within a domain. | 100% | Pipeline stops; error queue to Steward. |
| **Referential Integrity** | Each record in the Adverse Events table (`AE`) has a corresponding valid `SUBJECT_KEY` in Demographics (`DM`). | > 99.9% | Warning logged; records with no key are routed to a quarantine table. |
| **Plausibility** | Visit dates are after birth dates; subject age is within a plausible range. | 100% | Warning logged; anomalous records flagged for review. |

#### 5.4.2 Manual Steward Review
1.  Each time a study is integrated, the Clinical Data Steward must perform a manual review of a 10% random sample of patient-level trajectories, tracing a Subject Key across DM, AE, and LB (Labs) domains.
2.  A "Data Quality Certification Report" (DQCR) is generated via a Jupyter Notebook template and signed by the Steward.
3.  The DQCR includes a specific attestation: *“I confirm that the data transformation was executed in accordance with SOP-CLIN-003 and that the output data in the MCDM is a true, pseudonymized representation of the source SDTM.”*

### 5.5 Phase 5: Integration and Release

#### 5.5.1 Integration into MedInsight
1.  The released MCDM dataset is registered as a new "Data Asset" in the MedInsight Analytics platform's data catalog (Snowflake).
2.  The Data Product team maps the dataset into predefined subject area mart tables (e.g., `CARDIOVASCULAR_V2`, `ONCOLOGY_V3`).
3.  Access permissions are managed through Okta groups and Snowflake Role-Based Access Control (RBAC).

#### 5.5.2 Integration for AI Training
1.  To use the data for Clinical AI Platform model training, a separate "AI Training Data Request" is filed in JSM.
2.  The Chief AI Officer (Dr. Marcus Rivera) reviews the request for model risk tier (High-Risk under EU AI Act).
3.  For high-risk AI use cases, the dataset name and version are entered into the Model Card under the "Training Data" section, ensuring traceability from model output back to source data, as required by the NIST AI RMF “Traceability” characteristic (GOVERN 4.1).
4.  A frozen, version-controlled copy of the dataset is created for the training run to ensure reproducibility (`s3://meridian-ml-training-data/frozen/`).

---

## 6. Controls and Safeguards

### 6.1 Technical Controls
- **Access Control:** All access is governed by the principle of least privilege, enforced via Okta Universal Directory groups and AWS IAM roles. Direct bucket access is prohibited; only programmatic access via approved pipelines is permitted.
- **Encryption:** AES-256 encryption at rest (AWS KMS CMK) and TLS 1.3 in transit.
- **Network Segmentation:** Data storage accounts reside in a dedicated Virtual Private Cloud (VPC) with no direct internet egress. Outbound connections are proxied via a strict web gateway.
- **Audit Logging:** All data access, transformation, and movement events are logged to a centralized Datadog SIEM with immutable, write-once-read-many (WORM) storage. Logs are retained for 7 years.

### 6.2 Administrative Controls
- **ROPA Maintenance:** Dr. Klaus Weber (DPO) is responsible for updating the central Record of Processing Activities (ROPA) under GDPR Art. 30 within 5 business days of a new clinical trial data integration. The ROPA entry includes: name of data source, purpose of processing, categories of data subjects and personal data, and technical safeguards applied.
- **Data Processing Addendum (DPA):** No clinical trial data integration proceeds without an executed Data Processing Addendum with the data provider, containing the mandatory Standard Contractual Clauses (SCCs) for EU personal data transfers, as required by GDPR Art. 28 and Art. 46.
- **Third-Party Audit:** The effectiveness of these controls against SOC 2 criteria is tested annually by an external auditor.

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs)
The Data Operations team will track the following metrics on a Datadog real-time dashboard and report them at the monthly Clinical AI Operations Review:

| Metric | Target Source | SLA / Threshold |
| :--- | :--- | :--- |
| **Time-to-Insight** | Jira, Step Functions | Time from DUA signature to data being released in MedInsight. Target: < 30 calendar days. |
| **Pipeline Success Rate** | Step Functions | Percentage of pipeline runs that complete without a fatal error. Target: > 98%. |
| **Data Quality Defect Rate** | Great Expectations | Number of records quarantined / total records ingested. Target: < 0.1%. |
| **GDPR DSAR Response Time** | JSM, OneTrust | Time to locate and report on all data for a specific MSK. Target: < 10 calendar days (vs. GDPR 30-day limit). |
| **Out-of-Policy Data Storage** | AWS Config | Number of S3 buckets containing trial data without a valid lifecycle policy. Target: 0. |

### 7.2 Reporting Cadence
- **Weekly:** Operational pipeline health report to VP of IT Operations (Samantha Torres).
- **Monthly:** KPI dashboard review with VP of Clinical AI Products (Dr. Aisha Okafor).
- **Quarterly:** Governance review with the Clinical AI Risk Committee, including a summary of any exceptions or DPIA updates.

---

## 8. Exception Handling and Escalation

### 8.1 Non-Standard Data Ingestion Request
A formal exception is required for any of the following:
- Ingestion of clinical data not in a CDISC-compliant format.
- Ingestion of data containing an unplanned, direct identifier deemed “non-removable” for a critical business reason.
- Processing data for a new purpose not covered in the original DUA or DPIA.

### 8.2 Exception Procedure
1.  The requesting party documents the business justification and the specific technical or procedural deviation in an "SOP Exception Form" in JSM.
2.  **Risk Assessment:** The Clinical Data Steward and the CISO (Rachel Kim) conduct a joint technical risk assessment.
3.  **Escalation and Approval Authority:**
    - **Standard Exceptions:** Approved by VP of Clinical AI Products (Dr. Aisha Okafor) and Data Protection Officer (Dr. Klaus Weber).
    - **High-Risk Exceptions:** Any exception materially affecting EU data subject rights or involving high-risk personal data under GDPR Art. 9 must be escalated to and approved by the General Counsel (Maria Gonzalez) and the Chief Compliance Officer (Thomas Anderson).
4.  All approved exceptions are time-bound and must be re-validated annually.

---

## 9. Training Requirements

| Role | Required Training | Frequency | Platform |
| :--- | :--- | :--- | :--- |
| **Data Ops Engineer** | 1. SOP-CLIN-003 Deep Dive <br> 2. Secure Coding & Pipeline Security | 1. Annually <br> 2. Annually | Workday LMS |
| **Clinical Data Steward** | 1. CDISC Standards Refresher <br> 2. GDPR for Data Stewards (focus on Pseudonymization & Anonymization) | 1. Bi-annually <br> 2. Annually | Workday LMS / External |
| **Product Manager** | 1. Clinical Data Acquisition & Ethics Overview | Annually | Workday LMS |
| **All Staff with Data Access** | 1. GDPR Core Principles <br> 2. HIPAA & PHI Awareness | Annually | Workday LMS |

Training completion is tracked in Workday. Access to clinical trial data S3 buckets is programmatically revoked for any individual whose mandatory training has lapsed beyond a 15-day grace period.

---

## 10. Related Policies and References

- **EU General Data Protection Regulation (GDPR) (Regulation (EU) 2016/679)**
- **SOP-IS-005: Information Classification and Handling Policy**
- **SOP-SEC-012: Cryptographic Key Management**
- **SOP-AI-001: AI Model Risk Management Framework (NIST AI RMF)**
- **SOP-ANALYTICS-008: MedInsight Data Mart Access Control**
- **Meridian Clinical AI Data Standard: MCDM v4.2 Specification**
- **CDISC SDTM Implementation Guide v3.4**

---

## 11. Revision History

| Version | Date | Author(s) | Summary of Changes |
| :--- | :--- | :--- | :--- |
| 5.9 | 2024-01-28 | Dr. Aisha Okafor, Dr. Klaus Weber | Major revision. Overhauled Phase 3 for GDPR pseudonymization depth; added MCDM v4.2 mapping; integrated DPO into DPIA gate; updated RACI matrix to reflect new Compliance Officer role. |
| 5.5 | 2023-08-14 | James Park (former Data Ops Lead), Dr. Weber | Updated Data Quality Assurance thresholds for Referential Integrity based on audit finding #CLIN-2023-08; added SHA-256 checksum verification step. |
| 5.1 | 2023-02-01 | James Park | Switched transformation engine from Airflow/Kotlin to DBT. Updated Phase 3 procedure. Updated all component names to reflect new stack. |
| 4.3 | 2022-09-22 | Dr. Aisha Okafor | Replaced manual SFTP with AWS Transfer Family with Okta SSO. Updated Section 5.1.3. |
| 4.0 | 2021-11-15 | Dr. Priya Patel, Legal | Initial formal release incorporating GDPR framework and formal DPIA process. |