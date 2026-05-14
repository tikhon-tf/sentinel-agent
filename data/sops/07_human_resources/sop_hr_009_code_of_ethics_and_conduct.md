---
sop_id: "SOP-HR-009"
title: "Code of Ethics and Conduct"
business_unit: "Human Resources"
version: "4.4"
effective_date: "2024-01-28"
last_reviewed: "2025-03-05"
next_review: "2025-09-04"
owner: "Jennifer Walsh, Chief Human Resources Officer"
approver: "Dr. Sarah Chen, CEO"
classification: "Internal"
regulations:
  - "SOC 2"
status: "Active"
---

# Standard Operating Procedure: Code of Ethics and Conduct

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the Code of Ethics and Conduct (the "Code") for Meridian Health Technologies, Inc. and its global subsidiaries. The purpose of this Code is to codify the ethical principles, standards of behavior, and conduct expectations that govern all business activities. This SOP operationalizes the Code, providing detailed implementation procedures, controls, and accountability mechanisms to ensure compliance with applicable laws, regulatory requirements, and Meridian's core values.

Given Meridian's position at the intersection of advanced artificial intelligence, healthcare delivery, and financial services, this Code addresses unique ethical challenges including algorithmic fairness, patient data stewardship, responsible AI deployment, and the integrity of financial decisioning systems.

### 1.2 Scope

This SOP applies universally to all directors, officers, employees (full-time, part-time, temporary), independent contractors, consultants, and agents of Meridian Health Technologies, Inc. and its wholly-owned subsidiaries across all global offices (Boston, London, Berlin, Singapore, Toronto). References to "Meridian Personnel" in this document encompass all such individuals.

**Products and Systems in Scope:**
- Clinical AI Platform (high-risk AI systems under EU AI Act Annex III)
- HealthPay Financial Services (subject to SR 11-7 model risk management)
- MedInsight Analytics (PHI processing for ~12M patients)
- Meridian SaaS Platform (SOC 2 Type II certified infrastructure)

**Jurisdictional Scope:**
- United States (HIPAA, FDA regulations, state privacy laws)
- European Union (EU AI Act, GDPR, EU MDR)
- United Kingdom (UK GDPR, MHRA regulations)
- Canada (PIPEDA, provincial health privacy laws)
- Singapore (PDPA, MOH guidelines)
- All other jurisdictions where Meridian conducts business

### 1.3 Core Principles

This Code is built upon five foundational principles that guide all decision-making at Meridian:

| Principle | Description |
|-----------|-------------|
| **Patient-Centricity** | Patient safety, privacy, and welfare are paramount in every decision. Clinical AI outputs are decision-support tools, not autonomous decision-makers. |
| **Integrity** | Honest, transparent, and ethical conduct in all dealings with patients, providers, payers, regulators, and each other. |
| **Accountability** | Clear ownership, auditable records, and acceptance of responsibility for outcomes of systems we design and deploy. |
| **Fairness** | Active mitigation of bias in AI/ML models, equitable treatment of all stakeholders, and non-discriminatory practices. |
| **Stewardship** | Responsible guardianship of data, financial systems, intellectual property, and the trust placed in Meridian by the healthcare ecosystem. |

Violations of this Code may result in disciplinary action up to and including termination of employment or contractual relationship, civil litigation, and referral to law enforcement or regulatory authorities.

---

## 2. Definitions and Acronyms

### 2.1 Definitions

| Term | Definition |
|------|------------|
| **Breach Response Officer (BRO)** | Designated individual(s) responsible for coordinating all breach notification activities. Appointed by the CHRO and CISO jointly. |
| **Customer Data Breach** | Any confirmed unauthorized access, use, disclosure, modification, or destruction of customer data, including PHI, PII, financial information, or proprietary code/configurations entrusted to Meridian, that compromises the confidentiality, integrity, or availability of such data. Excludes unsuccessful attempts. |
| **Confirmation Time (T-confirm)** | The timestamp when the Meridian Security Incident Response Team (SIRT) Lead declares, based on forensic evidence, that a Customer Data Breach has been confirmed. This is distinct from initial detection time. |
| **Financial Materiality Threshold** | Any single incident or series of related incidents with an estimated financial impact (fines, remediation, legal fees, settlement) exceeding $50,000 or that has a >10% probability of exceeding $500,000, triggering mandatory escalation to the CFO and Audit Committee. |
| **Gift and Entertainment (G&E)** | Any item of value, meal, travel, hospitality, or entertainment provided to or received from a third party in connection with Meridian business. Specific monetary thresholds and approval requirements are defined in Section 5.4. |
| **High-Risk AI Decision** | Any output from the Clinical AI Platform that directly influences a diagnostic pathway, a treatment regimen triage, or a hospital resource allocation decision without direct, contemporaneous human licensed physician review. |
| **Kickback** | Any form of remuneration, including cash, gifts, services, or favors, intended to induce or reward the referral of patients, the ordering of devices/services, or the prescribing of pharmaceuticals that interact with Meridian platforms. |
| **Related Party Transaction** | Any financial arrangement, contract, or transaction between Meridian and any director, executive officer, beneficial owner of >5% of Meridian stock, or any immediate family member of the foregoing. |
| **Whistleblower** | Any Meridian Personnel who, in good faith, reports a suspected violation of law, regulation, or this Code. Protection against retaliation is absolute and governed by SOP-LEG-012. |

### 2.2 Acronyms

| Acronym | Full Form |
|---------|-----------|
| AI | Artificial Intelligence |
| AUP | Acceptable Use Policy |
| BRO | Breach Response Officer |
| CEO | Chief Executive Officer |
| CFO | Chief Financial Officer |
| CHRO | Chief Human Resources Officer |
| CISO | Chief Information Security Officer |
| CPO | Chief Privacy Officer |
| CRO | Chief Regulatory Officer |
| DPA | Data Processing Agreement |
| E&C | Ethics and Conduct (Committee) |
| GDPR | General Data Protection Regulation (EU 2016/679) |
| G&E | Gifts and Entertainment |
| HITECH | Health Information Technology for Economic and Clinical Health Act (US) |
| MLA | Machine Learning Algorithm |
| PHI | Protected Health Information |
| PII | Personally Identifiable Information |
| RACT | Responsible AI Compliance Team |
| SIRT | Security Incident Response Team |
| SOC 2 | System and Organization Controls 2 (AICPA Trust Services Criteria) |
| COSO | Committee of Sponsoring Organizations of the Treadway Commission |

---

## 3. Roles and Responsibilities

Effective execution of this SOP requires clear, pre-assigned responsibilities. The following matrix, based on the RACI model (Responsible, Accountable, Consulted, Informed), delineates authority for the lifecycle of an ethics incident or breach notification.

| Role | Title(s) | Key Responsibility |
|------|----------|-------------------|
| **Code Owner** | Jennifer Walsh, CHRO | Overall policy maintenance, annual review, training compliance, G&E policy interpretation. |
| **Regulatory Lead** | Marcus Thorne, CRO | GDPR Art. 33/34 notification authority, EU MDR vigilance reporting authority, and liaison to Data Protection Authorities (DPAs). |
| **Security Lead** | Priya Nair, CISO | T-confirm declaration, forensic evidence integrity, containment verification, SOC 2 control attestation. |
| **Privacy Lead** | Dr. Eleanor Vance, CPO | PHI/PII breach classification, HIPAA Breach Notification Rule compliance, patient impact assessment. |
| **AI Ethics Lead** | Dr. David Chen, Head of Responsible AI | Algorithmic bias assessment, AI discrimination risk evaluation, FDA/CE Mark deviation impact analysis. |
| **Financial Compliance** | Robert Hayes, CFO | Financial materiality assessment, anti-kickback statute analysis (HealthPay), related party transaction approval. |
| **Business Unit Leads** | VPs of Engineering, Product, Sales (See Appendix A) | Operational notification execution, contractual obligation review for specific customers. |
| **Whistleblower Ombuds** | Independent Audit Chair, Board of Directors | Anonymous reporting channel oversight, anti-retaliation compliance validation. |

### 3.1 RACI Matrix for Breach Notification

| Procedure Step | CHRO | CRO | CISO | CPO | BU VP | Legal | CEO |
|----------------|:----:|:---:|:----:|:---:|:-----:|:-----:|:---:|
| **Incident Verification & T-confirm** | I | I | **A/R** | C | I | I | I |
| **Patient Impact & PHI Breach Classification** | I | C | C | **A/R** | I | I | I |
| **Regulatory (GDPR, HIPAA) Notification Obligation** | C | **A/R** | C | C | I | C | I |
| **Drafting Customer-Facing Communication** | C | C | I | I | **R** | **A** | I |
| **Approval of Communication** | I | C | I | I | I | **A** | **I** |
| **Execution of Notification (Sending)** | C | I | I | I | **R/A** | I | I |
| **Related Party Transaction Disclosure** | I | C | I | I | I | C | **A** |

---

## 4. Policy Statements

### 4.1 Commitment to Ethical AI and Clinical Safety

Meridian designs, develops, and deploys AI systems to augment, not replace, clinical judgment. Every High-Risk AI Decision pathway requires explicit human-in-the-loop confirmation as a technical control. Meridian will not deploy any Clinical AI Platform component that demonstrates statistically significant bias (p < 0.05) against a legally protected demographic group in validation studies. All model release notes will include a "Fairness and Bias" impact statement reviewed by the Responsible AI Compliance Team (RACT).

### 4.2 Conflicts of Interest

All Meridian Personnel must avoid any situation where personal, familial, or financial interests conflict or appear to conflict with the interests of Meridian or its patients. Mandatory annual conflict-of-interest disclosures are required for all employees at Band 7 (Manager) and above, all members of product, sales, and procurement teams (regardless of band), and all Clinical AI data annotators.

### 4.3 Anti-Bribery and Anti-Corruption

Meridian maintains a zero-tolerance policy for bribery, kickbacks, and corruption. This applies globally, encompassing the U.S. Foreign Corrupt Practices Act (FCPA), the UK Bribery Act 2010, and equivalent local laws. No Meridian Personnel may offer, promise, authorize, or provide anything of value to any government official, healthcare provider, or employee of a commercial payer to improperly influence a decision. All interactions with Healthcare Professionals (HCPs) related to HealthPay and Clinical AI products must be tracked in the MedPro Compliance System (see Section 5.4.3).

### 4.4 Data Privacy and Stewardship

Patient data is a sacred trust. Meridian commits to the principles of data minimization and purpose limitation. Personal data, particularly PHI, will only be processed on lawful bases as defined under GDPR Art. 6 and Art. 9. De-identification processes for MedInsight Analytics must meet the HIPAA Expert Determination standard (§164.514(b)) prior to use in product development. Re-identification attempts are explicitly forbidden and constitute a Class I violation of this Code, resulting in immediate termination.

### 4.5 Trust and Security (SOC 2 Alignment)

Meridian is committed to the security, availability, and confidentiality of its systems, aligning with the AICPA Trust Services Criteria for SOC 2. We will design, implement, and operate controls to protect customer data against unauthorized access, disclosure, or destruction, meeting the requirements of Common Criteria 1.0 (CC1.0 - CC9.0) as detailed in Section 6. This commitment is fundamental to maintaining the trust of our healthcare and financial services clients.

### 4.6 Fair Competition and Antitrust

Meridian competes vigorously but fairly. Personnel shall not engage in price-fixing, bid-rigging, market allocation, or group boycotts. Informal information sharing with competitors poses significant risk and is prohibited.

---

## 5. Detailed Procedures

### 5.1 Reporting Violations and Seeking Guidance

Timely reporting is a personal obligation of every Meridian Personnel member. A failure to report a known or strongly suspected material violation is itself a violation of this Code.

#### 5.1.1 Reporting Channels

Meridian provides multiple confidential channels for reporting concerns or asking questions about ethics and conduct:

| Channel | Medium | Access Details | Best For |
|---------|--------|---------------|----------|
| **Meridian EthicsLine** | Web Portal | `ethicsline.meridian.health` (Anonymous option available) | Serious misconduct, financial fraud, hostile environment. |
| **EthicsLine Hotline** | Phone | +1-833-MER-ETHX (Operated by independent third-party, Convercent) | Anonymous voice reporting, available 24/7/365. |
| **Direct Manager/HRBP** | In-Person/Email | Standard contact list in Workday | Conflicts of interest, G&E clarification, interpersonal concerns. |
| **C-Suite Open Door** | Email | `open-door@meridian.health` | Escalation of unresolved issues or concerns about direct management chain. |

**Timeline Acknowledgment SLA:** All reports submitted via the EthicsLine portal or hotline will receive an automated acknowledgment via a unique report key within 1 hour. The CHRO's office (or, if concerning the CHRO, the CEO's office) will provide a human response or status update within 2 business days.

#### 5.1.2 Anonymous Reporting and Confidentiality

Meridian respects a reporter's choice to remain anonymous where legally permissible. The technical architecture of the Convercent reporting system is designed so that even Meridian system administrators cannot trace an IP address for reports explicitly submitted as anonymous. Information about an investigation will be shared strictly on a "need-to-know" basis. Meridian strictly prohibits retaliation against any individual who, in good faith, reports a suspected violation. Any act of retaliation is a direct violation of the Code and will result in disciplinary action up to and including termination of the retaliator.

### 5.2 Conflicts of Interest

#### 5.2.1 Mandatory Annual Disclosure Process (Workday Module)

All covered individuals (as defined in Section 4.2) must complete the "Ethics & Conflict Disclosure" task in Workday annually, by January 31st, and on an ad-hoc basis within 15 days of a triggering event. The disclosure covers:

1.  **Outside Employment/Directorships:** Roles at any entity in the healthcare, health IT, or financial services sectors.
2.  **Family Member Employment:** Details of immediate family members (spouse/domestic partner, parents, children, siblings) who hold decision-making positions at competitors, customers, or vendors.
3.  **Personal Financial Interests:** Any equity or debt holding >5% in a non-public entity that is a competitor, vendor, or customer, or any equity holding >0.5% in a public competitor.
4.  **Related Party Transactions:** Disclosure of any transaction involving Meridian and a Related Party.

Disclosures are routed to the CHRO and Legal. Disclosures involving the C-suite are automatically routed to the Audit Committee Chair.

### 5.3 External Communications and Social Media

Only authorized spokespersons may communicate on behalf of Meridian. The Investor Relations and Corporate Communications (IR/CC) function, under the CFO, is the sole authorized source for official financial and strategic comments. The Marketing department is authorized to speak to publicly available product specifications. No other Meridian Personnel may speak to media, analysts, or investors on behalf of the company. Personal social media activity must not imply Meridian endorsement, disclose confidential non-public information (like unreleased features, security vulnerabilities, or financial results), or disparage customers or competitors.

### 5.4 Gifts and Entertainment (G&E)

This procedure applies specifically to interactions surrounding the HealthPay and Clinical AI business lines, where interactions with healthcare providers and payers are high risk. The G&E policy is governed by a rules engine in the Coupa Travel and Expense system.

#### 5.4.1 Receiving G&E

Receiving a gift or entertainment from a vendor or prospective vendor requires pre-clearance through Coupa.

| Type | From/To | Threshold | Approval Required | Notes |
|------|---------|-----------|-------------------|-------|
| **Nominal Gift** (e.g., coffee mug, pen) | From vendor | <$25 FMV | None, but log in Coupa | Per occasion, $100 annual aggregate from single entity. |
| **Business Meal** | From vendor | <$75 per person | Manager (Pre-approval in Coupa) | Must be in connection with bona fide business discussion. |
| **Conference Attendance** | From vendor covering fees/travel | Any value | VP + Legal (SOP-LEG-005) | Must be approved 30+ days in advance. Company stands ready to pay if required policy dictates. |
| **Entertainment** (sporting events, concerts) | From vendor | Prohibited, unless Meridian pays full market price | — | "Subsidy" by vendor is not permissible. |

#### 5.4.2 Giving G&E to Healthcare Professionals (HCPs)

G&E given to HCPs or hospital administrators is governed by the AdvaMed Code of Ethics and Meridian's Sunshine Act compliance program.

| Type | Target | Threshold | Approval Required | Notes |
|------|--------|-----------|-------------------|-------|
| **Modest Meal** | HCP | <$40 per HCP | Manager | Must be in the context of a substantive educational presentation. Recorded in MedPro. |
| **Educational Item** | HCP | <$100 FMV aggregate/year | VP Sales + Medical Affairs | Must directly benefit patient education, e.g., anatomical model. No branded USB drives, pens, etc. |
| **Consulting Fees** | HCP | At Fair Market Value (FMV) | Legal + RACT (AI bias review) | Requires a written contract, legitimate need for HCP expertise, and time reporting via MedPro. |
| **Travel/Lodging for Evaluation** | Hospital Administrator | Economy class only, $250/night max | CFO + CRO | Only when a rigorous on-site evaluation of Clinical AI is strictly necessary and cannot be done remotely. |

#### 5.4.3 MedPro Compliance System

All interactions with HCPs and government officials must be logged in the Meridian Professional Interaction Registry (MedPro) within 5 business days, including attendee NPI number, nature, topic, and value of any item provided. The system generates quarterly transparency reports which are audited against Coupa expense data.

### 5.5 Customer Data Breach Notification Procedure (Operational Workflow)

This detailed procedure operationalizes the GDPR Art. 33/34 notification obligations and SOC 2 CC7.0 (Communication to Parties) for Meridian customers across all platforms. The workflow is initiated upon "T-confirm" (Confirmation Time) of a Customer Data Breach by the CISO.

**Step 1: Triage and Classification (First 2 Hours Post T-confirm)**
The SIRT Lead calls an emergency bridge with the BRO, CPO, and CRO. Using Form `SEC-001-BreachClassification`, they classify the breach on a critical 3-axis matrix:
- **Axis 1 - Data Type:** (P1) PHI/PII, (P2) Proprietary Customer Configuration/Code, (P3) Non-PII Operational Data.
- **Axis 2 - Risk of Harm:** (H1) Immediate Risk of Patient Harm (e.g., alteration of a clinical alert threshold), (H2) Risk of Financial/Reputational Harm, (H3) Low Risk.
- **Axis 3 - Scope:** (S1) >10,000 individual data subjects or multi-tenant compromise, (S2) 100-10,000 data subjects, (S3) Isolated, single-digit data subjects.

**Step 2: Notification Obligation Matrix & SLA Trigger**
The combination of axes from Step 1 triggers a mandatory Customer Notification SLA.

| Breach Classification Vector | Notification SLA to Customer (from T-confirm) | Template ID | Approver |
|------------------------------|-----------------------------------------------|-------------|----------|
| Any P1 or H1 + S1 | **2 Hours** | `BC-P1H-CRITICAL` | CEO + CRO + CISO |
| P1 or H1 + S2 | **4 Hours** | `BC-P1H-HIGH` | CRO + CISO |
| P1 or H1 + S3 | **8 Hours** | `BC-P1H-MEDIUM` | CPO + CISO |
| P2 + (S1 or S2) | **24 Hours** | `BC-P2-STANDARD` | BU VP + CISO |
| All other P3 combinations | **72 Hours** (next business day, best effort) | `BC-P3-ADVISORY` | SIRT Lead |

This matrix is pre-loaded into the PagerDuty and xMatters incident communication platform. Upon classification, the system automatically triggers the notification workflow with the correct template, approver list, and a countdown timer.

**Step 3: Drafting and Approval (Parallel Processing)**
The Breach Response Officer (BRO) retrieves the mandated template from the secured repository. Templates are designed as modular blocks:
- **Block A (Non-Negotiable):** Plain-language description of what happened. Approved by CISO.
- **Block B (Non-Negotiable):** Clear description of what customer PII/PHI was involved. Approved by CPO.
- **Block C (Non-Negotiable):** Steps Meridian has taken to contain the breach and secure data (remediation). Approved by CISO.
- **Block D (Responsive):** Specific recommendations for actions the customer should take to protect themselves (e.g., "Rotate all API keys for the Clinical AI v2.3 endpoint"). Approved by BU VP.
- **Block E (Regulatory):** GDPR-specific language regarding DPA notification (if applicable), DPIA update requirements, and data subject communication recommendations. Approved by CRO.

The CISO, CPO, and CRO review and approve their respective blocks in parallel via DocuSign within forced timelines:
- For 2-hour SLAs: 20 minutes
- For 4-hour SLAs: 45 minutes
- For 8-hour SLAs: 90 minutes

**Step 4: Transmission and Acknowledgment Tracking**
The approved notification is transmitted to the customer's designated Security and Privacy contacts (maintained in Salesforce under Account > "Emergency Contact" related list) via the xMatters system.
- **Transmission:** High-priority email. For 2- and 4-hour SLAs, this is followed by an automated phone call to all contacts using the pre-recorded script in xMatters, directing them to a secure portal containing the full details.
- **Acknowledgment Tracking:** The communication contains a tracked, single-use link. Receipt and click-through are monitored. If no acknowledgment click is received within 25% of the SLA window (e.g., 30 minutes for a 2-hour SLA), the Customer Success Manager (CSM) is auto-paged to begin manual outbound calls via Contact Center tools (Genesys Cloud).

**Step 5: Post-Incident Audit and DPIA Update**
Within 10 business days of incident closure, the SIRT Lead and BRO conduct a post-incident review. Findings are documented in a non-punitive after-action report in ServiceNow GRC. The CPO determines if the incident requires a formal update to the general Data Protection Impact Assessment (DPIA) for the affected product. A summary report is filed with the Audit Committee at the next quarterly meeting.

---

## 6. Controls and Safeguards

The following administrative, technical, and physical controls operationalize the Code of Ethics and Conduct, with specific reference to SOC 2 Trust Services Criteria (TSC) 2017.

| Control ID | Control Description | Type | TSC Alignment (SOC 2) | Metric/Evidence | Owner |
|------------|---------------------|------|------------------------|-----------------|-------|
| **CTRL-HR-009-01** | **Annual Code of Conduct Attestation:** All active users must digitally sign an acknowledgment of the Code, G&E policy, and Conflict of Interest policy via Workday. Non-completion triggers automated account suspension at 7 days overdue. | Administrative | CC1.1, CC1.2 | Workday task completion report; % of active users signed by Jan 31. | CHRO |
| **CTRL-HR-009-02** | **Background Check Verification:** All new hires undergo a background check commensurate with their data access level (Standard/Broad/PII-PHI) via Checkr, completed prior to start date. Includes identity, criminal (7-year, all jurisdictions), and OIG exclusion list checks. | Administrative | CC1.1, CC1.2, CC6.4 | HireRight completion report; % cleared prior to start date. | CHRO |
| **CTRL-HR-009-03** | **Conflict of Interest Disclosure Engine:** A rules engine in Workday flags disclosures based on keywords ("competitor," "vendor," "close relative") against a curated entity register. Flagged items route automatically to Legal and the CHRO for review. | Technical | CC1.2, CC4.2 | Queue of flagged disclosures and resolution status. | CHRO / Legal |
| **CTRL-HR-009-04** | **MedPro & Coupa Spend Reconciliation Audit:** A quarterly automated script (`FIN-SCR-200`) cross-references every vendor expense logged against an HCP in Coupa with a corresponding, pre-approved activity in MedPro. Any mismatch >$40 generates an exception for forensic review by Finance. | Technical / Detective | CC5.1, CC5.2, CC7.1 | Quarterly reconciliation report; % of transactions with a MedPro match. Variance/exception report. | CFO |
| **CTRL-LEG-009-01** | **EthicsLine Case Lifecycle Management:** Independent third-party (Convercent) manages the technical security and integrity of the case management system. Convercent SOC 2 Type II report is reviewed annually by Meridian's Vendor Risk Management team. | Technical / Administrative | CC1.3, CC2.3, CC7.3 | Convercent annual SOC 2 Type II report with clean opinion on security, availability, and confidentiality. | CISO |
| **CTRL-LEG-009-02** | **Whistleblower Anti-Retaliation Audit:** The Board Audit Committee Chair, with Internal Audit, reviews the performance ratings, compensation adjustments, and involuntary terminations of all individuals who made a substantiated whistleblower report in the prior 12 months. This review ensures no adverse action was taken related to the report. | Detective / Administrative | CC1.1, CC7.4 | Annual report to the Audit Committee, attesting to zero instances of substantiated retaliation. | Audit Committee Chair |
| **CTRL-TECH-009-01** | **Responsible AI Fairness Gate:** A mandatory JIRA workflow gate (`RAI-CHECK`) must pass before any new Clinical AI model version can be deployed to production. The gate validates the "Fairness & Bias" impact statement, ensuring metrics for demographic parity or equal opportunity are within approved thresholds (<5% differential). | Technical / Preventive | CC7.2, CC7.3 | JIRA deployment pipeline records; RAI gate approval status for each model version. | Head of Responsible AI |

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance and Risk Indicators (KPIs/KRIs)

The effectiveness of this Code of Ethics and Conduct is continuously monitored through a set of quantitative KPIs and KRIs aggregated in the ServiceNow GRC Dashboard and reviewed by the Executive Risk Committee (ERC) monthly.

| Metric ID | Metric Name | Target / Threshold | Measurement Owner | Reporting Cadence |
|-----------|-------------|--------------------|--------------------|-------------------|
| **ET-001** | **Code of Conduct Training Completion Rate** | **Target:** 100% completion by Jan 31 annually. **KRI Alert:** <90% completion by Jan 15 triggers escalation to CHRO and all BU Leads. | CHRO (LMS Reporting) | Weekly during January; Annually otherwise. |
| **ET-002** | **Annual COI Disclosure Completion Rate** | **Target:** 100% of covered individuals. **KRI Alert:** <95% completion by Jan 31. | CHRO (Workday) | Monthly during Q1-January; Annually otherwise. |
| **ET-003** | **EthicsLine Report Median Time to First Response** | **SLA Target:** <2 Business Days. **KRI Alert:** > 5% of reports exceed SLA in a quarter. | CHRO (Convercent) | Quarterly |
| **ET-004** | **Substantiated Retaliation Cases** | **Absolute Zero Tolerance.** Any single substantiated case is a Critical KRI requiring immediate Board notification. | Audit Chair (Audit) | Per Incident / Quarterly Audit |
| **ET-005** | **Critical Data Breach Notification SLA Compliance** | **Target:** 100% compliance with the 2-hour and 4-hour SLA windows defined in Section 5.5. <95% monthly triggers a root cause analysis and remediation plan presented to C-Suite. | CISO (xMatters) | Monthly |
| **ET-006** | **G&E Compliance Audit Failure Rate** | **Threshold:** <2% of audited transactions have a "critical" deviation (e.g., unreported HCP interaction, exceeded threshold without waiver). If >2%, triggers mandatory re-training for the offending Business Unit. | CFO (Coupa/MedPro Audit) | Quarterly |

### 7.2 Reporting Cadence

| Report Name | Recipient(s) | Content | Frequency |
|-------------|--------------|---------|-----------|
| **ERC Ethics & Compliance Snapshot** | Executive Risk Committee (CEO, CFO, CRO, CISO, CHRO, CPO) | Dashboard of KPIs ET-001 through ET-006, status of all open Class 1 (serious) investigations, and upcoming regulatory horizon scanning. | Monthly |
| **Audit Committee Ethics Program Review** | Board Audit Committee | Deep dive on whistleblower activity (anonymized trends), anti-retaliation audit results (CTRL-LEG-009-02), key investigation outcomes, and any material updates to the Code. | Quarterly |
| **Annual Code Effectiveness Report** | Full Board of Directors | Summary of year-over-year trends, program maturity assessment, comparison to industry benchmarks, and recommendations for Code updates for the coming year. | Annually (at Q4 meeting) |

---

## 8. Exception Handling and Escalation

### 8.1 Exception to Policy

Situations may arise where strict adherence to a procedural step in this Code is impossible or counterproductive. A "Policy Exception" is a temporary, documented approval to deviate from a specific, non-regulatory procedural requirement.

**Procedure for Requesting an Ethics Exception:**
1.  **Requester:** Initiates the "Code of Conduct Exception" workflow in ServiceNow (`sow_catalog → Ethics & Conduct → Request Exception`).
2.  **Justification:** Provides a clear, detailed business justification explaining why adhering to the standard procedure is not feasible and proposing an alternative control or mitigation measure.
3.  **Manager Review:** Direct Manager reviews and concurs or provides a counter-opinion in the workflow.
4.  **Decision Path:**
    - **G&E Limits (up to $500 excess):** Approved by BU VP + Chief Compliance Officer (CRO).
    - **Conflict of Interest (Nominal, e.g., small family business vendor):** Approved by CHRO + Legal. Involves implementing a formal "Conflict Management Plan" as an alternative to divestment.
    - **Breach Notification Timing (e.g., law enforcement delay):** Approved SOLELY by the CEO, on advice of the CISO + General Counsel. The delay must be documented, time-bound, and legally justified.
    - **AI Fairness Gate Override:** Approved by CEO + Chief Medical Officer + Head of Responsible AI (unanimous). This is a Critical Risk Exception documented and immediately reported to the Board Audit Committee.

Any exception with a duration exceeding one year must be re-approved annually by the original approver. The central Exception Register is maintained in ServiceNow GRC.

### 8.2 Escalation of Concerns

If a concern is not adequately addressed through normal channels, the following mandatory escalation path exists:
- **Level 1:** Direct Manager / HR Business Partner (HRBP).
- **Level 2:** Business Unit Vice President / CHRO.
- **Level 3:** Chief Legal Officer / Chief Compliance Officer (CRO).
- **Level 4:** Chair of the Board Audit Committee.
- **Level 5:** Any federal, state, or local governmental regulatory authority. Nothing in this Code restricts an individual's right to communicate directly with or report possible violations of law to a government agency.

---

## 9. Training Requirements

### 9.1 Curriculum and Assignment

Training is the bedrock of operationalizing the Code. All Meridian Personnel are assigned a role-based learning path, hosted on the Docebo Learning Management System (LMS), branded internally as "Meridian University."

| Role Group | Initial Onboarding Training (Within first 30 days) | Annual Refresh Training | Triggered Event-Based Training |
|------------|-----------------------------------------------------|-------------------------|--------------------------------|
| **All Personnel** | `ETH-101: Our Code, Our Commitment` (45 min) | `ETH-201R: Annual Code & Ethics Refresher` (25 min) | When a material Code update (e.g., version `4.x` to `5.x`) occurs. |
| **Managers (Band 7+)** | `ETH-110: Leading with Integrity: Manager's Duties` (60 min) | `ETH-210R: Handling Ethics Conversations & COI Management` (40 min) | When promoted to first management role. |
| **Sales & BU Commercial Teams** | `ETH-120: Competing Fairly: G&E, Anti-Kickback, and HCP Engagement` (90 min) | `ETH-220R: Advanced G&E and MedPro Compliance` (55 min) | If Business Unit G&E audit failure rate (Metric ET-006) exceeds 2% for a quarter. Retraining `ETH-220R` is triggered within 30 days. |
| **AI/ML Engineers & Data Scientists** | `ETH-130: Responsible AI: Fairness from the Ground Up` (120 min) | `ETH-230R: Advanced Fairness & Bias in Healthcare AI` (75 min) | Before receiving deployment credentials for the Clinical AI production environment. |

### 9.2 Tracking and Enforcement

- **Completion:** All training modules end with a scored assessment. A passing score of 85% is required. Unlimited retakes are permitted, but all failures are logged for trend analysis by the CHRO.
- **Non-Compliance:** Failure to complete assigned training by its due date results in:
    - **Day 1-7 Past Due:** Automated email reminders from Docebo, copied to Direct Manager.
    - **Day 8-14 Past Due:** Direct Manager receives formal notice from HR; matter discussed in 1:1.
    - **Day 15+ Past Due:** Access to core business systems (AWS `PHI-Read-Write` IAM role, Workday, Salesforce) is automatically suspended via an Identity Governance (Okta) lifecycle workflow triggered by the LMS. Access is restored immediately upon training completion.

---

## 10. Related Policies and References

This SOP is one component of a comprehensive compliance and ethics framework. It must be read and applied in conjunction with the following internal Meridian policies and external standards:

### 10.1 Meridian Internal Policies

| SOP ID | Title | Relationship |
|--------|-------|-------------|
| **SOP-LEG-012** | Whistleblower Protection and Anti-Retaliation Policy | Provides granular operational detail for the anti-retaliation principles in Section 5.1 of this Code. |
| **SOP-SEC-015** | Acceptable Use of IT Assets and Systems (AUP) | Defines technical boundaries for use of Meridian-provided assets, referenced in Data Stewardship. |
| **SOP-SEC-022** | Data Classification and Handling Standard | Defines PHI, PII, Proprietary, and Internal classifications that govern the breach notification procedure in Section 5.5. |
| **SOP-AI-001** | Clinical AI Development Lifecycle and Fairness Standard | Provides the detailed technical controls and JIRA gates for the `RAI-CHECK` procedure described in Section 6. |
| **SOP-FIN-016** | Global Anti-Bribery, Anti-Corruption (ABAC) and Gifts & Entertainment Policy | Is the source of authority for the monetary thresholds and MedPro system described in Section 5.4. |
| **SOP-PRI-030** | Privacy Incident and Breach Response Plan | Provides the technical forensic playbook that SIRT executes prior to T-confirm and triggering Section 5.5 of this Code. |

### 10.2 External Standards and Regulations

| Reference | Title / Description | Relevance |
|-----------|---------------------|-----------|
| **AICPA TSC 2017** | Trust Services Criteria for SOC 2 | The control framework against which Meridian's SOC 2 Type II examination is scoped. Controls in Section 6 are mapped to CC1.x - CC9.0. |
| **GDPR Art. 33 & 34** | EU General Data Protection Regulation, Articles on Breach Notification | Defines the 72-hour notification to DPAs and notification to data subjects, operationalized in the 2-72 hour SLAs in Section 5.5. |
| **COSO 2013** | Internal Control - Integrated Framework | Informs the enterprise risk management and internal control environment that supports the RACI matrix in Section 3. |
| **HIPAA Rules** | Breach Notification Rule (45 CFR §164.400-414) | Informs the CPO's PHI breach classification and notification obligations in the United States, parallel to GDPR, in Section 5.5. |
| **AdvaMed Code** | Code of Ethics on Interactions with Health Care Professionals | Directly referenced in the specific controls for giving G&E to HCPs in Section 5.4.2. |
| **ISO 31000:2018** | Risk Management Guidelines | Provides the risk framework used to develop the KRI thresholds and escalation criteria defined in Section 7 and 8. |

---

## 11. Revision History

| Version | Date | Author(s) | Summary of Changes |
|---------|------|-----------|--------------------|
| 1.0 | 2019-09-12 | J. Walsh, M. Thorne | Initial policy creation, consolidating separate ethics, G&E, and whistleblower policies. |
| 2.0 | 2020-11-03 | J. Walsh, P. Nair (CISO) | Major revision adding SOC 2 Control Mapping (Section 6) and formal Breach Notification SLA matrix (Section 5.5). Updated training curriculum. |
| 3.0 | 2021-06-20 | D. Chen (Head of RAI), J. Walsh | Added Section 1.3 (Core Principles), AI-specific ethics statements (Section 4.1), and RAI controls (Section 6, CTRL-TECH-009-01). |
| 3.5 | 2022-05-18 | J. Walsh, Internal Audit | Post-audit revision to strengthen conflict-of-interest disclosure process (SWORD to Workday workflow, Section 5.2.1) and MedPro G&E tracking. |
| 4.0 | 2023-02-01 | J. Walsh, M. Thorne, E. Vance (CPO) | Comprehensive rewrite for EU AI Act readiness and CE marking integration. Introduced H1/P1/S1 Breach Classification Matrix. Updated all templates. |
| 4.2 | 2023-07-14 | J. Walsh | Updated reporting channels to include Convercent integration. Added exception handling for fairness gate overrides. Revised related policies table. |
| 4.3 | 2023-10-11 | J. Walsh | Interim update: Revised training non-compliance escalations; updated approval thresholds for G&E exceptions; incorporated feedback from Q3 2023 ERC meeting. |
| **4.4** | **2025-03-05** | **J. Walsh, M. Thorne** | **Scheduled biennial review. Updated Section 7 Metrics (ET-005 SLA definition tightened to 2/4hr windows). Revised Section 9 Training curriculum IDs to current `ETH-2xx` series. Updated roles to reflect current org structure (new CPO). No substantive changes to controls.** |

---