---
sop_id: "SOP-COPS-011"
title: "Customer Feedback and NPS Program"
business_unit: "Customer Operations"
version: "3.0"
effective_date: "2024-06-08"
last_reviewed: "2025-10-17"
next_review: "2026-04-16"
owner: "Michael Chang, VP of Customer Operations"
approver: "Robert Liu, VP of Financial Services"
classification: "Internal"
regulations:
  - "GDPR"
status: "Active"
---

# Standard Operating Procedure: Customer Feedback and NPS Program

## 1. Purpose and Scope

### 1.1 Purpose

This Standard Operating Procedure (SOP) establishes the framework for systematically collecting, analyzing, and acting upon customer feedback across all Meridian Health Technologies, Inc. product lines. The Customer Feedback and Net Promoter Score (NPS) Program is designed to:

- Measure and track customer loyalty, satisfaction, and sentiment across the Clinical AI Platform, HealthPay Financial Services, MedInsight Analytics, and Meridian SaaS Platform
- Identify systemic issues, feature gaps, and service delivery failures before they result in customer churn
- Provide structured input into product roadmap prioritization and engineering sprint planning
- Support compliance with EU AI Act transparency obligations by capturing end-user feedback on AI system performance and human oversight adequacy
- Generate quantitative benchmarks for executive quarterly business reviews (QBRs) and Board-level AI Governance Committee reporting
- Enable closed-loop action planning that assigns accountability for remediation and tracks resolution through to customer confirmation

### 1.2 Scope

This SOP applies to:

| **In Scope** | **Out of Scope** |
|---|---|
| All production customers of Clinical AI Platform, HealthPay, MedInsight, and Meridian SaaS | Internal employee satisfaction surveys |
| Transactional feedback (post-interaction surveys) | FDA Adverse Event reporting (see SOP-RAQA-042) |
| Relationship NPS surveys (quarterly pulse) | Security incident reporting (see SOP-ISMS-019) |
| Feature-specific feedback campaigns tied to releases | Formal complaints subject to regulatory grievance procedures |
| Win/loss analysis for sales opportunities | Vendor or partner satisfaction assessments |
| In-app feedback widgets within the SaaS Platform | Clinical outcomes data collection |
| All customer-facing personas: clinicians, administrators, financial officers, patients (via provider portal) | Unstructured social media monitoring (Marketing responsibility) |

### 1.3 Applicability

This SOP is binding on all Meridian employees, contractors, and third-party service providers who design, deploy, analyze, or act upon customer feedback mechanisms. Non-compliance shall be managed per SOP-HR-007 (Employee Disciplinary Action Policy).

---

## 2. Definitions and Acronyms

| **Term/Acronym** | **Definition** |
|---|---|
| **NPS** | Net Promoter Score; a customer loyalty metric derived from the question "How likely are you to recommend [Meridian/Product] to a colleague?" on a 0-10 scale |
| **Promoter** | Respondent scoring 9-10; loyal enthusiasts who will fuel growth |
| **Passive** | Respondent scoring 7-8; satisfied but unenthusiastic customers vulnerable to competitive offerings |
| **Detractor** | Respondent scoring 0-6; unhappy customers at risk of churn and capable of negative word-of-mouth |
| **Relational NPS (rNPS)** | Periodic (quarterly) survey measuring overall relationship health with Meridian |
| **Transactional NPS (tNPS)** | Event-triggered survey following a specific interaction (e.g., support ticket closure, implementation milestone) |
| **CSAT** | Customer Satisfaction Score; typically a 1-5 Likert scale measuring satisfaction with a specific interaction |
| **CES** | Customer Effort Score; measures the ease of accomplishing a task with Meridian products |
| **Feedback Loop** | The end-to-end process from feedback collection through analysis, action assignment, resolution, and customer follow-up |
| **Closed-Loop** | A feedback loop where the customer is informed of the action taken in response to their input |
| **Detractor Recovery** | A structured outreach process to understand and resolve Detractor concerns, typically within defined SLA |
| **Qualtrics** | Meridian's enterprise survey platform, integrated with Salesforce Service Cloud, AWS, and Snowflake |
| **Feedback Taxonomy** | A hierarchical classification of feedback themes mapped to product modules, business processes, and organizational owners |
| **PHI** | Protected Health Information; individually identifiable health information subject to HIPAA |
| **Customer Health Score** | A composite metric combining NPS, product adoption, support ticket volume, and payment timeliness |

---

## 3. Roles and Responsibilities

### 3.1 Responsibility Assignment Matrix (RACI)

| **Activity** | **VP Cust Ops (Michael Chang)** | **Customer Success Manager (CSM)** | **Product Manager** | **CISO (Rachel Kim)** | **CPO/DPO (Klaus Weber)** | **VP Financial Svcs (Robert Liu)** | **AI Governance Comm.** |
|---|---|---|---|---|---|---|---|
| Survey design and approval | A | R | C | C | C | C | C (for AI products) |
| Survey distribution | A | R | I | I | I | I | I |
| NPS calculation methodology | A | I | C | I | I | C | I |
| Detractor recovery (<48hr contact) | I | R | C | I | I | A (HealthPay) | I |
| Closed-loop action assignment | A | R | R | I | I | R | I |
| Feedback taxonomy maintenance | R | C | C | I | I | I | A (AI taxonomy) |
| AI-related feedback triage | I | C | C | I | I | I | A |
| Data retention compliance | I | C | I | I | A | I | I |
| Quarterly NPS reporting to Board | R | C | C | I | I | C | C |

### 3.2 Detailed Role Descriptions

**VP of Customer Operations (Michael Chang)**
- Executive owner of the NPS program
- Approves all survey instruments prior to fielding
- Reviews quarterly NPS trends and approves corrective action plans for accounts with sustained Detractor status (3+ consecutive quarters)
- Holds quarterly NPS deep-dive with the CEO and Board AI Governance Committee
- Authorizes exceptions to survey suppression rules for strategic accounts

**Customer Success Manager (CSM)**
- Primary owner of Detractor Recovery SLA adherence (first contact within 2 business days of Detractor response)
- Documents Detractor concerns and root cause analysis in Salesforce per SOP-COPS-008 (Case Management Policy)
- Coordinates closed-loop action planning with Product, Engineering, and Professional Services
- Conducts Detractor follow-up within 14 calendar days to confirm customer acknowledgment of remediation plan
- Maintains Customer Health Score dashboards in Gainsight for assigned portfolio

**Product Manager**
- Reviews NPS survey items within their product domain prior to fielding
- Triages feature-specific feedback themes within 5 business days of CSM escalation
- Assigns feedback themes to Engineering backlog items with tracking IDs
- Reports on feedback-driven feature releases in quarterly product review meetings

**VP of Financial Services (Robert Liu)**
- Approves NPS surveys that relate to HealthPay billing, invoicing, or payment processing experiences
- Reviews financial services-related Detractor themes monthly
- Authorizes service credits, billing adjustments, or remediation pricing for Detractor accounts, per delegation of authority schedule
- Participates in Detractor recovery calls for accounts where feedback relates to financial disputes

**CISO (Rachel Kim)**
- Reviews survey technical implementation for data security compliance
- Approves data pipeline architecture (Qualtrics → Snowflake → Tableau)
- Ensures survey data is classified per SOP-ISMS-002 (Data Classification Policy) and handled accordingly
- Reviews any PHI-related survey design considerations

**AI Governance Committee**
- Reviews all survey items relating to AI system performance, transparency, and human oversight capability (per Article 14 of the EU AI Act)
- Triage AI-specific Detractor feedback that may indicate systematic performance issues requiring model retraining or algorithmic fairness review
- Quarterly review of AI-related NPS themes aggregated across all Clinical AI Platform customers

---

## 4. Policy Statements

### 4.1 Survey Design Principles

P-011-01: All customer-facing surveys shall be designed in accordance with the Meridian Survey Design Standards (Appendix A). Surveys shall not exceed 12 questions for relational NPS instruments and 5 questions for transactional instruments, except where the AI Governance Committee approves extended batteries for AI Act compliance.

P-011-02: The standard NPS question ("How likely are you to recommend Meridian to a colleague or peer organization?") shall be included in every relational survey and shall be presented as a 0-10 Likert scale with anchors at 0 ("Not at all likely") and 10 ("Extremely likely").

P-011-03: All NPS and CSAT surveys shall include a mandatory free-text follow-up question soliciting the primary reason for the rating provided. This verbatim text shall be retained for no less than 36 months from the date of collection and shall be linked to the respondent's rating and account record.

### 4.2 Data Collection and Integration

P-011-04: All customer feedback data shall be collected exclusively through Meridian's approved enterprise survey platform (Qualtrics). No survey data shall be collected through email, spreadsheets, informal phone calls, or unapproved third-party tools.

P-011-05: NPS response data shall be integrated into the Customer Data Platform (Salesforce Service Cloud) within 1 hour of survey submission, and into the enterprise data warehouse (Snowflake) within 4 hours via the approved Qualtrics-Snowflake connector pipeline.

P-011-06: Survey invitations shall be suppressed for customers who have received a survey in the preceding 14 calendar days, or who have an open Severity 1 support case (per SOP-ITS-004). The suppression logic shall be maintained in the Qualtrics contact frequency rules engine.

### 4.3 Detractor Management

P-011-07: Every Detractor (score 0-6) shall trigger an automated Salesforce Case creation, assigned to the account's designated CSM, with a Priority of "High" and a due date of 2 business days from survey submission.

P-011-08: CSMs shall conduct first outreach to Detractors within 2 business days of the Detractor survey submission timestamp. Outreach shall be logged in the Salesforce Case Comments with the method (phone, email, video conference), a summary of the customer's concerns, and a preliminary root cause category from the Feedback Taxonomy.

P-011-09: For any Detractor whose concerns relate to patient safety, clinical accuracy of AI outputs, or potential regulatory non-compliance, the CSM shall escalate to the Chief Medical Officer (CMO) and VP of Clinical Affairs within 4 business hours of the customer conversation, per SOP-CLIN-003 (Clinical Safety Escalation).

### 4.4 Transparency and Contestability

P-011-10: Survey instruments directed at Clinical AI Platform end-users shall include items assessing the user's understanding of the AI system's capabilities and limitations, and the adequacy of the human oversight interface, consistent with the transparency obligations for high-risk AI systems.

P-011-11: Customers who provide Detractor feedback related to AI system outputs shall be offered a structured review pathway with a Meridian Clinical AI Specialist, who can explain the algorithmic reasoning, training data provenance, and known limitations relevant to the specific use case.

### 4.5 Confidentiality and Attribution

P-011-12: Individual NPS scores and free-text verbatim comments shall be visible to the assigned CSM, the VP of Customer Operations, and the relevant Product Manager. Access shall be logged in the Salesforce audit trail.

P-011-13: Aggregate and anonymized NPS trends may be shared externally (e.g., in marketing materials, sales references) only in accordance with SOP-MKT-003 (External Communications Policy) and only with the explicit documented approval of the VP of Customer Operations.

P-011-14: NPS data containing PHI shall be immediately classified as "Restricted" per the Data Classification Policy, and any handling of such data shall comply with SOP-ISMS-004 (PHI Handling Policy).

---

## 5. Detailed Procedures

### 5.1 Relational NPS (rNPS) Quarterly Pulse

#### 5.1.1 Pre-Launch Activities (T-14 Calendar Days)

1. **Contact List Preparation**
   - CS Operations Analyst extracts active customer contacts from Salesforce using the "NPS Eligible Contacts" report (Report ID: SF-RPT-COPS-011-01).
   - Eligibility criteria: Primary contact or designated survey contact on an active MSA with at least 90 days since go-live date; contact has an active email address; contact is not on the Global Survey Suppression List.
   - HealthPay customers must additionally be flagged as "Billing Contact Verified" by the Finance Operations team before inclusion.
   - The contact list CSV shall contain the following columns: `Contact_ID, Account_ID, Account_Name, Product_Line, CSM_Name, Tier, Region, Email, Last_Survey_Date`.

2. **Survey Instrument Build**
   - The CS Operations team builds the quarterly rNPS survey in Qualtrics using the approved template (`Qualtrics Template ID: QT-rNPS-v3.2`).
   - Core questions (mandatory, unmodifiable except by exception approval from VP Cust Ops):
     - Q1: "How likely are you to recommend [Product Line] to a peer organization or colleague?" (0-10, single-select)
     - Q2: "What is the primary reason for the score you provided?" (Open text, 500-char limit)
     - Q3: "Please rate your overall satisfaction with [Product Line] over the past quarter." (1-5 Likert, 1=Very Dissatisfied, 5=Very Satisfied)
   - Rotating topical modules (select maximum 3 per quarter, approved by VP Cust Ops):
     - Module A: Implementation & Onboarding (applicable only to customers live <180 days)
     - Module B: Support Experience (aligned to SOP-COPS-015)
     - Module C: Product Feature Set & Roadmap Alignment
     - Module D: AI System Trust & Transparency (mandatory for Clinical AI Platform customers, per AI Governance Committee directive Q2-2024)
     - Module E: Billing & Invoicing (mandatory for HealthPay customers, approved by Robert Liu)

3. **AI Governance Committee Review**
   - For surveys that include Module D (AI System Trust), the draft instrument shall be submitted to the AI Governance Committee for review at least 10 business days prior to fielding.
   - The Committee shall verify that questions adequately probe for:
     - User understanding of system capabilities and limitations
     - Satisfaction with the human oversight interface
     - Perceived transparency of algorithmic reasoning
   - Committee review shall be documented in the Meridian AI Governance Register (SharePoint: AI-Gov-Register).

4. **Survey Approval**
   - Final survey instrument, contact list, and fielding plan shall be submitted to Michael Chang (VP Cust Ops) for approval via the Qualtrics Survey Approval Workflow.
   - Approval shall be logged with timestamp and approver identity in the Qualtrics Survey Audit Log.

#### 5.1.2 Fielding

1. **Distribution**
   - Surveys are distributed via Qualtrics' email distribution engine, using the `noreply-surveys@meridianhealthtech.com` sender address.
   - Subject line: "Tell us about your Meridian experience – 3-minute survey"
   - Distribution occurs on the **first Tuesday** of each calendar quarter (Jan, Apr, Jul, Oct).
   - The survey remains open for exactly **21 calendar days**.

2. **Reminder Schedule**
   - Reminder 1: T+7 calendar days, sent only to non-respondents
   - Reminder 2: T+14 calendar days, sent only to non-respondents
   - No further reminders after T+14.

3. **Response Monitoring**
   - CS Operations Analyst monitors daily response rates by account tier.
   - For Strategic Accounts (Tier 1, defined in SOP-SALES-003) with zero responses by T+10, the assigned CSM shall personally email the primary contact encouraging participation. CSM outreach shall not be scripted but shall not pressure the customer.
   - CSM personal outreach shall be logged in the relevant Salesforce Contact record as an Activity of type "NPS Follow-Up."

#### 5.1.3 Data Processing and Calculation

1. **NPS Calculation**
   - NPS = (% Promoters) - (% Detractors)
   - Promoter = Score 9-10
   - Passive = Score 7-8
   - Detractor = Score 0-6
   - Calculation performed at: Overall Company Level, Product Line Level, Account Tier Level, Individual Account Level, Region Level.
   - NPS shall be calculated to one decimal place (e.g., 34.7).

2. **Response Weighting**
   - No statistical weighting is applied to rNPS scores. Each respondent carries equal weight.
   - For accounts with multiple respondents, the account-level NPS is the arithmetic mean of individual respondent NPS classifications.

3. **Data Ingestion**
   - At survey close (T+21), Qualtrics automatically exports response data to Snowflake via the pre-configured ETL pipeline (`ETL-Feedback-01`).
   - The export includes: Respondent Contact ID, Account ID, Date/Time of Response, Q1 Score, Q2 Verbatim (raw text), Q3 Score, Module Responses, Survey Completion Status, IP Address, User Agent String.
   - The Snowflake destination table is `CUSTOPS.NPS_RESPONSES_RAW`, partitioned by `Survey_Period` and `Product_Line`.

### 5.2 Transactional Feedback (tNPS and CSAT)

#### 5.2.1 Triggers

Transactional feedback surveys are automatically triggered by the following events in Salesforce:

| **Trigger Event** | **Survey Type** | **Instrument Template** | **Delay from Trigger** |
|---|---|---|---|
| Support Case Closed (per SOP-COPS-008) | tNPS + CSAT | QT-tNPS-Support-v2.0 | 1 business day |
| Implementation Milestone Completed | CSAT | QT-CSAT-Impl-v1.5 | 3 business days |
| Feature Adoption Milestone (Admin activates new module) | CSAT (Feature) | QT-CSAT-Feature-v1.1 | 7 calendar days |
| Quarterly Business Review Completed (logged by CSM) | rNPS-lite (3 questions) | QT-QBR-Followup-v1.0 | 1 business day |

#### 5.2.2 Support Case Closure tNPS

1. Upon Case Closure (status changed to "Closed" in Salesforce), a workflow rule waits 1 business day (to ensure resolution stability), then sends a Qualtrics survey to the case contact.
2. Survey includes:
   - Q1: "How satisfied were you with the resolution of your recent support case?" (1-5 CSAT)
   - Q2: "How easy was it to get your issue resolved?" (1-7 CES scale)
   - Q3: "Based on this support experience, how likely are you to recommend Meridian?" (0-10 tNPS)
   - Q4: "Please share any additional feedback about your support experience." (Open text, 250-char limit)
3. If CSAT ≤ 2, an immediate Case Re-open is triggered in Salesforce, assigned to the Support Team Lead who originally closed the case, with a 24-business-hour SLA for re-engagement.

#### 5.2.3 Survey Suppression Rules for Transactional Surveys
- A contact shall not receive more than one transactional survey in any 7-calendar-day period.
- If multiple triggers fire within the suppression window, the following priority order determines which survey is sent: (1) Support Case Closed > (2) Implementation Milestone > (3) QBR Follow-up > (4) Feature Adoption.

### 5.3 Detractor Recovery Workflow

This is the core operational workflow for managing Detractor responses and is subject to strict SLA monitoring.

1. **Detection (T+0)**
   - Upon any rNPS or tNPS survey submission with a score of 0-6, the Qualtrics-Salesforce connector automatically creates a Case in Salesforce.
   - Case Record Type: "Detractor Recovery"
   - Case Owner: Auto-assigned to the Account's designated CSM (as per Account Team in Salesforce)
   - Case Priority: "High"
   - Case SLA Due Date: `TODAY + 2 BUSINESS DAYS` (for First Contact)
   - The Case is populated with: Respondent Name, Respondent Score, Verbatim Comment (Q2), Account Name, Product Line, Survey Date/Time.

2. **CSM Triage and Preparation (T+0 to T+1 Business Day)**
   - CSM reviews the verbatim comment, account health score, recent support case history, and any prior Detractor cases for the same account.
   - CSM determines preliminary root cause category from the Feedback Taxonomy (see Section 5.6).
   - For HealthPay Detractors where the verbatim references billing or payment issues, the CSM notifies the VP of Financial Services (Robert Liu) or their designate via the assigned Case Chatter feed.
   - For Clinical AI Platform Detractors referencing AI performance or transparency, the CSM adds the `AI_Governance_Flag` checkbox to the Case and tags the AI Governance Committee distribution list.

3. **First Contact (T+0 to T+2 Business Days)** — **SLA CRITICAL**
   - CSM initiates outreach to the Detractor using the customer's preferred contact method (as recorded in Salesforce Contact Preferences).
   - Outreach is by phone first, with a follow-up email if no phone answer.
   - Email template `DT-OUTREACH-V1` (available in Salesforce Email Templates) may be used but must be personalized.
   - **Goals of the conversation**:
     - Thank the customer sincerely for their candid feedback
     - Listen actively without defensiveness; let the customer fully express their concerns
     - Ask clarifying questions to deeply understand the root cause
     - DO NOT promise specific product features, timelines, or compensation without explicit approval
     - Set expectations for follow-up: "I will personally investigate this and get back to you with a concrete plan by [date: within 14 calendar days]."
   - CSM documents the conversation in the Case Comments within 4 business hours of the call, including: date/time of contact, customer's key concerns, any immediate remediation actions taken, and the date promised for follow-up.

4. **Root Cause Investigation (T+2 to T+7 Business Days)**
   - CSM convenes an internal "Detractor Triage" meeting (virtual, 30 minutes) with:
     - Relevant Product Manager
     - Support Team Lead (if support-related)
     - Professional Services Lead (if implementation or services-related)
     - VP Cust Ops or designate (for Tier 1 & 2 accounts only)
   - The team analyzes the Detractor feedback, identifies root cause(s), and develops a remediation action plan.
   - Action Plan elements:
     - Root cause category (from taxonomy)
     - Specific actions to address root cause
     - Owner for each action
     - Due date for each action
     - Proposed customer follow-up date (must be ≤ 14 calendar days from First Contact)
   - Action Plan is documented in the Salesforce Case, in the "Detractor Action Plan" related list.

5. **Customer Follow-Up (T+2 to T+14 Calendar Days)** — **SLA CRITICAL**
   - CSM re-contacts the customer by phone or video conference (not email, unless customer explicitly prefers email).
   - CSM presents the action plan: what was learned, what Meridian will do, by when, and what the customer should expect.
   - For actions requiring product changes, CSM explains the Product team's assessment without over-promising specific release dates (unless the feature is already committed to a numbered release with a published date).
   - CSM asks: "Does this plan address your concerns?" and documents the customer's response.
   - If the customer indicates the plan does NOT address their concerns, the CSM escalates to the VP of Customer Operations for executive engagement.

6. **Case Closure Criteria**
   - A Detractor Recovery Case can only be closed (Status = "Closed") when all the following are true:
     - First Contact was made within the 2-business-day SLA
     - Root cause is documented in the Case
     - An Action Plan is documented with at least one specific action item
     - Customer follow-up was completed and customer response documented
     - If the action plan includes product backlog items, those Jira tickets are created and linked to the Salesforce Case (via the Salesforce-Jira integration)
   - Cases that are not closed within 30 calendar days are automatically escalated to the VP Cust Ops.

### 5.4 Closed-Loop Action Planning

Beyond Detractor Recovery, the Closed-Loop Action Planning process ensures that all substantive feedback (Promoter, Passive, Detractor) drives organizational action.

1. **Feedback Review Cadence**
   - **Weekly**: CS Operations Analyst produces a "Weekly NPS Flash" report (Tableau Dashboard: NPS-Flash-WKLY) showing week-over-week NPS movement by product line and all new Detractor verbatims.
   - **Monthly**: Product Managers review all feedback verbatims tagged to their product domain, using the Feedback Taxonomy, and prepare a "Monthly Feedback Digest" for their engineering team's sprint planning.
   - **Quarterly**: Full NPS program review with VP Cust Ops, Product VPs, CISO, and AI Governance Committee Chair. The QBR deck includes NPS trend, Detractor recovery rates, top 10 systemic issues identified from feedback themes, and status of action plans from prior quarter.

2. **Feedback → Backlog Workflow**
   - CS Operations Analyst tags verbatim comments using the Feedback Taxonomy within Qualtrics (Text iQ auto-tagging, with manual CS Ops Analyst review).
   - Product Managers review auto-tagged themes for their domain and validate or re-classify tags within 10 business days of survey close.
   - Validated themes that indicate product gaps or feature requests are entered into Aha! as "Feedback-Driven Ideas" with the source traced back to the specific Salesforce Case and NPS survey response (via Contact ID).
   - Engineering reviews Feedback-Driven Ideas during quarterly PI Planning; ideas that are accepted into the roadmap are linked to Jira Epics.

3. **Promoter Activation**
   - Promoters (score 9-10) who provide verbatim comments indicating strong advocacy are flagged for the Customer Advocacy Program (managed by Marketing, per SOP-MKT-005).
   - CSMs ask Promoters (during QBRs) if they would be willing to participate in case studies, reference calls, or product advisory boards. Any such engagement requires the customer's documented consent (email confirmation minimum).

### 5.5 In-App Feedback Collection

1. **Feedback Widget**
   - The Meridian SaaS Platform includes an in-app feedback widget (powered by Pendo, integrated with Qualtrics via API).
   - The widget is configurable per product module and can be set to appear after specific user actions (e.g., completing a report generation, using a new AI-powered feature for the 5th time).
   - Widget surveys are limited to 3 questions maximum and include a thumbs-up/thumbs-down CSAT and optional free-text.

2. **Integration Governance**
   - Any new in-app feedback trigger point must be approved by the Product Manager and the VP Cust Ops.
   - Changes to in-app survey frequency or targeting logic require a Change Request in ServiceNow, per SOP-IT-003 (Change Management Policy).

### 5.6 Feedback Taxonomy

All verbatim feedback shall be classified using the Meridian Feedback Taxonomy, maintained by the Customer Operations Analytics team.

**Level 1 Categories (Product/Process Domain):**
| **Category ID** | **Category Label** | **Description** |
|---|---|---|
| CAT-PROD | Product Functionality | Core features, UX/UI, performance, reliability |
| CAT-AI | AI System Performance | Accuracy, explainability, transparency, trust, human oversight |
| CAT-SUPP | Support Experience | Case resolution speed, quality, communication, technical competence |
| CAT-IMPL | Implementation & Onboarding | Go-live timeline, data migration, training, Professional Services quality |
| CAT-BILL | Billing & Invoicing | Invoice accuracy, payment terms, pricing transparency (HealthPay-specific) |
| CAT-ACCT | Account Management | CSM responsiveness, QBR quality, strategic guidance |
| CAT-DOCS | Documentation & Knowledge Base | Completeness, accuracy, searchability of help content |
| CAT-INT | Integrations & APIs | Quality of third-party integrations, API documentation, reliability |

**Level 2 Categories (Sub-theme):** — Refer to Appendix B: Full Feedback Taxonomy (internal SharePoint:Taxonomy-COPS-011).

---

## 6. Controls and Safeguards

### 6.1 Technical Controls

| **Control ID** | **Control Description** | **Implementation** |
|---|---|---|
| TC-011-01 | All survey data transmitted between Qualtrics, Salesforce, and Snowflake must be encrypted in transit using TLS 1.2 or higher | Enforced via Qualtrics connector configurations; validated quarterly by Security Engineering |
| TC-011-02 | Survey response data at rest in Snowflake is encrypted using AES-256 | Default Snowflake encryption; validated annually in SOC 2 Type II audit |
| TC-011-03 | Access to raw NPS response data in Snowflake is restricted to the `CUSTOPS_ANALYTICS` and `DATA_ENGINEERING` role groups | Role-Based Access Control (RBAC) managed via Snowflake roles, reviewed semi-annually by Data Governance team |
| TC-011-04 | Salesforce NPS Case objects have field-level security preventing CSMs from modifying the Respondent Score field after Case creation | Salesforce Validation Rule: `ISPICKVAL(Status, "Closed")` AND `ISCHANGED(NPS_Score__c)` → Error |
| TC-011-05 | Survey suppression logic is implemented in Qualtrics Contact Frequency Rules and validated before each quarterly fielding | Pre-launch checklist (see Section 5.1.1) item: "Validate suppression rules in Qualtrics Test Send" |
| TC-011-06 | Any API integration between survey platform and Meridian systems uses OAuth 2.0 for authentication | Enforced in MuleSoft Anypoint Platform API policies |

### 6.2 Administrative Controls

| **Control ID** | **Control Description** |
|---|---|
| AC-011-01 | Annual review of survey instruments for continued relevance and regulatory alignment; review documentation stored in Qualtrics Survey Audit Log |
| AC-011-02 | Semi-annual audit of Detractor Recovery SLA adherence; audit report delivered to VP Cust Ops, with copy to Chief Compliance Officer |
| AC-011-03 | All users with access to Qualtrics survey design functions must complete SOP-COPS-011 training (see Section 9) prior to receiving Qualtrics Designer role |
| AC-011-04 | Survey data exports to external parties (e.g., for benchmarking studies) require approval of VP Cust Ops, CISO, and General Counsel; no individual respondent-level data shall be shared externally |
| AC-011-05 | Feedback data retention: Raw survey response data retained in Snowflake for 36 months; aggregated NPS metrics retained indefinitely in Tableau published data sources; Detractor Case data retained per Salesforce data retention policy (SOP-IT-014) |

### 6.3 PHI Handling in Feedback

- Survey invitations and instruments shall not request, solicit, or encourage the inclusion of PHI in free-text fields. Survey instructions clearly state: "Please do not include patient-specific health information in your responses."
- If PHI is nonetheless present in a verbatim response, it shall be manually redacted by the CS Operations Analyst upon identification, with the redacted text replaced by "[REDACTED-PHI]". The original text is retained in an encrypted, access-restricted Snowflake column viewable only to the Privacy Office.
- Any detection of PHI in survey responses triggers a notification to the Privacy Office (`privacy@meridianhealthtech.com`) within 24 hours of identification.

---

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs)

| **KPI** | **Definition** | **Target** | **Measurement Frequency** | **Owner** |
|---|---|---|---|---|
| Overall Company NPS | Standard NPS formula across all product lines | ≥ 40 | Quarterly | VP Cust Ops |
| Clinical AI Platform NPS | NPS for Clinical AI customers only | ≥ 35 | Quarterly | VP Cust Ops |
| HealthPay Financial Services NPS | NPS for HealthPay customers | ≥ 30 | Quarterly | VP Financial Svcs (Robert Liu) |
| Detractor Recovery SLA – First Contact | % of Detractor Cases where First Contact occurred within 2 business days | ≥ 95% | Monthly | VP Cust Ops |
| Detractor Recovery SLA – Follow-Up | % of Detractor Cases where Customer Follow-Up occurred within 14 calendar days | ≥ 90% | Monthly | VP Cust Ops |
| Survey Response Rate (rNPS) | (Completed Surveys / Delivered Surveys) * 100 | ≥ 25% | Quarterly | CS Operations |
| Detractor-to-Promoter Conversion Rate | % of Detractor accounts in Q(N) that become Promoters in Q(N+2) | ≥ 20% | Quarterly (lagging indicator) | VP Cust Ops |
| Closed-Loop Action Completion | % of Detractor Action Plan items completed by due date | ≥ 85% | Monthly | CS Operations |

### 7.2 Dashboards and Reports

| **Report/Dashboard** | **Location** | **Audience** | **Refresh Cadence** |
|---|---|---|---|
| NPS Executive Dashboard | Tableau: "CX Exec Dash" | C-Suite, VPs | Daily (during fielding period), Weekly (off-peak) |
| CSM Portfolio NPS | Gainsight: "My Accounts NPS" | Individual CSMs | Near real-time (Salesforce sync) |
| Product Feedback Themes | Aha! Reports: "Feedback to Feature" | Product Managers | Weekly |
| Detractor Recovery Queue | Salesforce: "Detractor Cases - My Queue" | CSMs, CS Team Leads | Real-time |
| AI Governance Feedback Digest | Tableau: "AI Feedback Monitor" | AI Governance Committee | Monthly |
| Quarterly NPS Board Report | Tableau Storyboard + PDF to Board Portal | Board of Directors | Quarterly (aligned to board meeting schedule) |

### 7.3 Quarterly Business Review Reporting

At each Quarterly Business Review (internal, with CEO and executive leadership), the VP of Customer Operations shall present:

1. Company-level NPS trend (rolling 8 quarters)
2. NPS by product line, account tier, and region
3. Top 5 Detractor themes (from Feedback Taxonomy) with aggregate verbatim excerpts
4. Detractor Recovery SLA performance
5. Notable Detractor-to-Promoter conversions (case studies, minimum 2 per QBR)
6. Key actions taken in the quarter in response to feedback (product changes, process improvements)
7. Forward-looking NPS targets for the next 2 quarters, with rationale

---

## 8. Exception Handling and Escalation

### 8.1 Exception Request Process

Any deviation from the procedures defined in this SOP must be authorized through a formal Exception Request, documented in the Meridian Governance, Risk, and Compliance (GRC) platform (ServiceNow GRC module).

**Exception Request Required Fields:**
- Requestor Name and Role
- Specific SOP Section from which deviation is requested
- Description of the deviation, including scope and duration
- Business justification for the deviation
- Compensating controls that will be in place during the deviation period
- Risk assessment (impact and likelihood if deviation is exploited)

### 8.2 Exception Approval Authority

| **Exception Type** | **Approval Authority** | **Max Duration** |
|---|---|---|
| Survey suppression override for specific strategic account | VP Cust Ops | One quarter (renewable upon re-approval) |
| Extension of Detractor Recovery SLA (first contact beyond 2 business days) | VP Cust Ops | 5 additional business days (one-time) |
| Use of non-Qualtrics survey tool for ad-hoc feedback | VP Cust Ops + CISO (Rachel Kim) | 30 calendar days |
| Sharing of identifiable NPS data with external auditor or consultant | VP Cust Ops + General Counsel | Duration of engagement, not to exceed 90 days |
| Modification of standard NPS question wording | VP Cust Ops + AI Governance Committee (if AI product) | Duration of specific survey campaign |

### 8.3 Escalation Pathways

| **Scenario** | **Escalation Path** |
|---|---|
| Detractor not contacted within SLA; Case overdue >3 business days | Case auto-escalates to Director of Customer Success; if still overdue at 5 business days, auto-escalates to VP Cust Ops |
| Detractor expresses threat of litigation, regulatory complaint, or public campaign | Immediate escalation to VP Cust Ops, General Counsel, and Chief Compliance Officer via `legal-escalation@meridianhealthtech.com` |
| Detractor feedback suggests systemic patient safety risk from AI outputs | Immediate escalation to CMO, VP Clinical Affairs, and VP Cust Ops; per SOP-RAQA-042, evaluate for regulatory reportability within 24 hours |
| Multi-account Detractor theme indicating a systemic product defect | CS Operations Analyst escalates to VP Cust Ops and VP of Engineering; joint remediation meeting convened within 5 business days |
| Survey data breach or Qualtrics platform compromise | Immediate escalation to CISO (Rachel Kim) per SOP-ISMS-019 (Security Incident Response) |

---

## 9. Training Requirements

### 9.1 Training Curriculum

| **Training Module** | **Code** | **Audience** | **Delivery Method** | **Required Frequency** |
|---|---|---|---|---|
| SOP-COPS-011 Policy Awareness | TR-COPS-011-AW | All employees with access to survey design, NPS data, or Detractor cases | Workday Learning (e-learning, 20 min) | Within 30 days of hire/role change; annual refresher |
| Detractor Recovery Workshop | TR-COPS-011-DRW | All Customer Success Managers | Live virtual workshop (2 hours, led by VP Cust Ops or designate) | Within 30 days of CSM role assignment; biennial refresher |
| Survey Design & Compliance | TR-COPS-011-SDC | CS Operations Analysts, Product Managers who design surveys | Live virtual workshop (3 hours, co-led by VP Cust Ops and CISO) | Annually |
| Qualtrics Technical Training | TR-COPS-011-QTT | CS Operations Analysts | Qualtrics-provided e-learning + Meridian-specific lab (1 day) | Within 60 days of role assignment; retake upon Qualtrics major version upgrade |

### 9.2 Training Tracking and Compliance

- All training completions are recorded in Workday Learning.
- CSMs who have not completed TR-COPS-011-DRW within the required window shall have their Qualtrics respondent-contact access suspended until training is completed.
- Quarterly NPS Program compliance audits (per SOP-COMP-001) shall verify that all personnel with SOP-COPS-011-assigned training have current completion status.
- Training content is reviewed annually by the VP Cust Ops, with updates incorporated per feedback from the AI Governance Committee and any procedural changes arising from Detractor root cause analysis.

---

## 10. Related Policies and References

### 10.1 Internal Meridian SOPs

| **SOP ID** | **SOP Title** | **Relationship to SOP-COPS-011** |
|---|---|---|
| SOP-COPS-008 | Case Management Policy | Governs the Salesforce Case lifecycle for Detractor Recovery Cases |
| SOP-COPS-015 | Customer Support Quality Standards | Defines support interactions that trigger tNPS surveys |
| SOP-CLIN-003 | Clinical Safety Escalation | Escalation pathway for Detractor feedback involving patient safety |
| SOP-ISMS-002 | Data Classification Policy | Defines classification handling for NPS data, especially PHI-containing responses |
| SOP-ISMS-004 | PHI Handling Policy | Controls for PHI discovered in survey free-text |
| SOP-ISMS-019 | Security Incident Response Policy | Incident response for survey platform breach or data exposure |
| SOP-IT-003 | Change Management Policy | Governs changes to in-app feedback triggers and survey integrations |
| SOP-IT-014 | Data Retention Policy | Retention schedules for Salesforce Cases and Snowflake data |
| SOP-RAQA-042 | Adverse Event and Product Complaint Handling | Determination of whether Detractor feedback constitutes a reportable event under MDR or vigilance obligations |
| SOP-HR-007 | Employee Disciplinary Action Policy | Consequences for non-compliance with this SOP |
| SOP-MKT-003 | External Communications Policy | Use of NPS data in external marketing materials |
| SOP-MKT-005 | Customer Advocacy Program | Referral of Promoters willing to participate as references |
| SOP-SALES-003 | Account Tiering and Segmentation | Definition of Tier 1 (Strategic) accounts for response monitoring |

### 10.2 External References

| **Reference** | **Description** |
|---|---|
| NPS Best Practice Framework (Bain & Company) | Methodology guidance for NPS survey design and governance; reference copy maintained in Meridian Policy Library |
| EU AI Act (Regulation 2024/XXXX) | Regulatory framework governing high-risk AI systems, including Clinical AI Platform; transparency and human oversight articles inform Module D (AI Trust) survey design |
| Qualtrics Security White Paper (v2024.1) | Technical security documentation for the enterprise survey platform; reviewed annually by CISO |

---

## 11. Revision History

| **Version** | **Effective Date** | **Author** | **Description of Changes** | **Approver** |
|---|---|---|---|---|
| 1.0 | 2021-02-15 | Sarah Chen (Dir. CS Ops) | Initial release; established NPS program for Meridian SaaS Platform only (pre-HealthPay acquisition) | Michael Chang |
| 1.1 | 2021-11-03 | Sarah Chen | Added Module D (AI Trust) survey module for Clinical AI Platform, per AI Governance Committee recommendation; added Detractor Recovery SLA tracking to Section 7 KPIs | Michael Chang |
| 2.0 | 2023-03-22 | Jamal Harris (Sr. CS Ops Manager) | Major revision: Expanded scope to include HealthPay product line following acquisition (Q4-2022); added Robert Liu as Approver for financial services-related survey content; integrated Qualtrics-Snowflake pipeline; added in-app feedback widget governance; revised Detractor Recovery workflow with 2-business-day SLA | Michael Chang, Robert Liu |
| 2.1 | 2023-09-14 | Jamal Harris | Updated Feedback Taxonomy to add CAT-BILL (Billing) category; added Module E (Billing) to rotating rNPS modules for HealthPay customers; updated SLA monitoring dashboards per Q3 process improvement | Michael Chang |
| 3.0 | 2024-06-08 | Elena Rossi (VP Cust Ops, CX Strategy) | Comprehensive rewrite: restructured document per new Meridian Policy Template v4.0; added RACI matrix; expanded training requirements; integrated CE marking and EU MDR considerations per SOP-RAQA-042 cross-reference; added Section 8 Exception Handling; deprecated legacy SurveyMonkey platform references (migration to Qualtrics fully complete Q1-2024); updated all role titles to current org chart | Michael Chang, Robert Liu |

---

**Document Control**
- This SOP shall be reviewed at least semi-annually by the Document Owner.
- Any employee may submit suggested revisions via the Meridian Policy Feedback Portal (ServiceNow).
- Printed copies are uncontrolled. Refer to the Meridian Policy Library for the current version.