---
sop_id: "SOP-COPS-010"
title: "Customer Consent Management"
business_unit: "Customer Operations"
version: "5.6"
effective_date: "2024-01-06"
last_reviewed: "2025-12-24"
next_review: "2026-06-21"
owner: "Michael Chang, VP of Customer Operations"
approver: "Robert Liu, VP of Financial Services"
classification: "Internal"
regulations:
  - "GDPR"
  - "HIPAA"
status: "Active"
---

# Standard Operating Procedure: Customer Consent Management

## 1. Purpose and Scope

This Standard Operating Procedure (SOP) establishes the enterprise-wide framework for managing customer consent preferences across all Meridian Health Technologies, Inc. (“Meridian”) business lines, products, and geographies. The purpose of this document is to ensure that all customer-facing systems capture, store, propagate, and honor consent choices in a consistent, auditable, and automated manner throughout the full customer lifecycle.

This SOP applies to:

- **All Meridian Business Lines**: Clinical AI Platform, HealthPay Financial Services, MedInsight Analytics, and the Meridian SaaS Platform.
- **All Customer Touchpoints**: Web-based applications, mobile interfaces, API integrations deployed by Meridian, call center workflows, paper-based intake forms that are subsequently digitized, and in-person enrollment kiosks at provider partner locations.
- **All Data Subjects**: Patients, healthcare provider staff users, payer plan administrators, guarantors, and any individual whose personal data is processed within Meridian systems.
- **All Geographies**: Operations in the United States, Canada, the European Union (including the European Economic Area), the United Kingdom, and Singapore.
- **All Consent Dimensions**: Consent for processing of special categories of personal data, marketing communications (email, SMS, push notifications, postal mail), cookies and tracking technologies, automated decision-making within the Clinical AI Platform, secondary research use of de-identified data, and financial product eligibility assessments within HealthPay.

This SOP is binding on all full-time employees, contractors, temporary workers, consultants, and third-party partners who design, develop, deploy, operate, or support customer-facing systems that collect or process consent. Compliance with this SOP is mandatory and subject to periodic audit as described in Section 7.

**Out of Scope**: Consent for employee human resources data processing and consent related to clinical trial enrollment conducted by sponsored research partners (managed under SOP-RSCH-042).

## 2. Definitions and Acronyms

The following defined terms are used throughout this SOP:

| Term / Acronym | Definition |
|---|---|
| **Consent** | Any freely given, specific, informed, and unambiguous indication of a data subject's wishes by which they, by a statement or by clear affirmative action, signify agreement to the processing of their personal data for one or more specified purposes. |
| **Consent Record** | The immutable digital artifact capturing the full context of a consent event, including timestamp, channel, purpose specification, identity of the data subject, and the text of the disclosures presented at the moment of capture. |
| **Preference Center** | The self-service portal available to authenticated users at `preferences.meridian.com` where data subjects may view, modify, or withdraw consent choices at any time. |
| **Consent Propagation** | The automated technical process by which a consent state changed in one Meridian system is transmitted to all downstream consuming systems, data warehouses, and processing pipelines within the SLA defined in Section 5. |
| **Active Consent** | A consent that has been affirmatively granted and has not expired, been withdrawn, or been administratively invalidated due to material change in processing purpose. |
| **Withdrawn Consent** | A previously Active Consent that the data subject has subsequently revoked via any supported channel. Withdrawal does not affect the lawfulness of processing based on consent before its withdrawal. |
| **Expired Consent** | A consent that has exceeded its defined validity period as specified in the consent disclosure presented at the time of capture. Default global expiration is 36 months from date of capture unless a shorter period is specified for a given purpose. |
| **Legitimate Interest** | A lawful basis for processing personal data where such processing is necessary for purposes of Meridian's legitimate interests or those of a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject. |
| **Soft Opt-In** | An exception applicable in certain jurisdictions allowing marketing communications about similar products or services to existing customers without explicit prior consent, provided clear and easy opportunity to opt out is given at the time of collection and in each subsequent communication. |
| **Processing Activity Inventory (PAI)** | The centralized record of all processing activities maintained by the Privacy Office in the OneTrust privacy management platform, indexed by Processing Activity ID. |
| **GDPR** | Regulation (EU) 2016/679 of the European Parliament and of the Council (General Data Protection Regulation). |
| **HIPAA** | Health Insurance Portability and Accountability Act of 1996 and its implementing regulations. |
| **PHI** | Protected Health Information. |
| **DSAR** | Data Subject Access Request. |
| **CMP** | Consent Management Platform (OneTrust, hosted at `consent.meridian.com`). |
| **CRM** | Customer Relationship Management system (Salesforce Health Cloud). |
| **CDP** | Customer Data Platform (Segment). |
| **IAP** | Identity and Access Platform (Okta Customer Identity Cloud). |
| **SLA** | Service Level Agreement. |

## 3. Roles and Responsibilities

The RACI matrix below allocates accountability, responsibility, consultation, and information roles for all activities governed by this SOP.

| Activity / Deliverable | VP Customer Ops (Owner) | Privacy Office / DPO | CISO | Product Managers | Engineering | Legal & Compliance | Customer Support |
|---|---|---|---|---|---|---|---|
| Consent architecture design | A | C | C | R | R | C | I |
| Consent disclosure drafting | C | R | I | C | I | A | I |
| CMP configuration & maintenance | A | R | C | I | R | I | I |
| Consent propagation testing | I | I | I | R | R | I | I |
| Audit & compliance monitoring | I | R | I | I | I | A | I |
| Regulatory change impact assessment | I | A | I | C | C | R | I |
| Data subject withdrawal processing | I | I | I | I | R | I | R |
| Consent preference support tickets | A | I | I | I | I | I | R |
| Third-party consent integration | A | C | R | R | R | C | I |

**Specific Role Details:**

- **Michael Chang, VP of Customer Operations (Policy Owner)**: Bears ultimate accountability for the effectiveness of this SOP. Reviews and approves exceptions escalated beyond standard delegation thresholds. Chairs the quarterly Consent Governance Review meeting.
- **Dr. Klaus Weber, Chief Privacy Officer / DPO**: Owns the legal sufficiency of consent disclosures, in coordination with General Counsel. Maintains the Processing Activity Inventory mapping all consent purposes to lawful bases. Approves all new consent purpose codes before deployment.
- **Rachel Kim, CISO**: Ensures that consent data flows comply with data security policies and that encryption and access control controls are implemented for consent records at rest and in transit.
- **Samantha Torres, VP of IT Operations**: Responsible for the operational availability of the Consent Management Platform and preference center infrastructure. Ensures SLA compliance per Section 6.
- **Customer Support Managers (all product lines)**: Operate the Tier 1 and Tier 2 consent support queues. Process manual consent withdrawals received via telephone or postal mail within the timelines specified in Section 5.
- **Product Managers (all product lines)**: Ensure that consent collection touchpoints are embedded in user journeys at the appropriate point before data processing commences. Maintain product-specific consent requirement specifications.

## 4. Policy Statements

Meridian Health Technologies is committed to processing personal data with transparency and respect for individual autonomy. The following policy statements constitute the mandatory principles governing all customer consent activities:

**PS-CNS-001 — Affirmative Consent Requirement**: Consent must be obtained through a clear affirmative action by the data subject. Pre-ticked checkboxes, silence, inactivity, or bundled consent for multiple purposes not individually selectable are prohibited. Each processing purpose requiring consent must be presented with its own opt-in mechanism.

**PS-CNS-002 — Granularity of Choice**: Data subjects must be able to consent to specific processing purposes independently. Consent for marketing communications must be separable from consent for clinical data processing, financial assessments, or any other purpose. Where Meridian processes special categories of personal data, explicit consent must be obtained separately for each category.

**PS-CNS-003 — Right to Withdraw**: Withdrawal of consent must be possible at any time and must be as easy as giving consent. No detriment shall result from withdrawal. All consent collection interfaces must include clear, visible instruction on how to withdraw consent, including a direct link to the Preference Center.

**PS-CNS-004 — Record-Keeping**: Meridian shall maintain demonstrable records of all consent events, including: the identity of the data subject, the timestamp of the consent action, the specific text of disclosures presented, the version identifier of the consent interface, the IP address and user agent string (where collected), and the specific processing purposes consented to or withdrawn.

**PS-CNS-005 — Purpose Limitation**: Personal data shall be processed only for the specific purposes for which consent was obtained. Before any Meridian system begins processing personal data for a given purpose, the CMP consent state for that subject-purpose pair must be verified programmatically. If no active consent is found, processing must not commence.

**PS-CNS-006 — Data Minimization in Consent Collection**: The act of collecting consent shall itself collect only the minimum personal data necessary to establish a consent record. Where possible, consent preferences shall be associated with a pseudonymous identifier rather than directly with the data subject's full profile, with resolution to the full profile performed only when necessary for propagation.

**PS-CNS-007 — Periodic Renewal**: Consent for marketing communications shall be deemed expired after 36 months of inactivity (defined as no interaction with any Meridian digital channel). At or before expiry, an automated renewal prompt shall be sent. If the data subject does not affirmatively renew consent within 30 days of the prompt, the consent status shall transition to Expired and all processing predicated on that consent shall cease.

**PS-CNS-008 — Minor Data Subject Consent**: Where Meridian processes personal data of individuals below the digital age of consent (16 years in most jurisdictions, subject to local variance), consent must be given or authorized by the holder of parental responsibility. The Clinical AI Platform and HealthPay enrollment flows shall implement age gating in accordance with jurisdiction-specific thresholds maintained in the CMP configuration.

**PS-CNS-009 — Consent for Automated Decision-Making**: The Clinical AI Platform shall obtain explicit, separate consent before subjecting any patient data to fully automated processing that produces legal effects or similarly significant effects. This consent purpose code is `AUTOMATED-DECISION-001` and must be accompanied by meaningful information about the logic involved and the envisaged consequences.

**PS-CNS-010 — Privacy Notice**: A layered privacy notice must be presented at every consent capture point. The notice must identify the controller (Meridian Health Technologies, Inc. and its relevant subsidiary by jurisdiction), describe the purposes of processing with specificity, and describe the data subject's rights regarding their personal data. Full privacy notice text is maintained in the OneTrust Notice Management module.

## 5. Detailed Procedures

This section describes the operational workflows for consent management at Meridian. All Meridian personnel involved in consent operations must follow these procedures precisely. Deviations are managed per Section 8.

### 5.1 Initial Consent Capture

This procedure applies whenever a new data subject establishes a relationship with Meridian through any digital or assisted channel.

**5.1.1 Digital Consent Capture (Web and Mobile)**

1. The product interface shall render the consent collection module from the CMP via the JavaScript tag or mobile SDK configured in the CDP.
2. The consent interface shall present, in sequence:
   a. **Jurisdiction Detection**: The interface auto-detects the data subject's jurisdiction based on IP geolocation and browser locale settings. The detected jurisdiction determines the legal basis options and disclosure language presented. The data subject may manually override the detected jurisdiction via a dropdown selector.
   b. **Privacy Notice Layer 1 (Summary)**: A concise summary of key processing activities and purposes. Must include a link to the full Layer 2 notice hosted at `privacy.meridian.com/{jurisdiction}/{product}`.
   c. **Cookie and Tracking Consent**: A four-category granular consent panel with the following categories, each individually toggleable:
      - *Strictly Necessary* (always on, non-consentable)
      - *Functional / Preference*
      - *Analytics and Performance* (Meridian first-party analytics)
      - *Marketing and Advertising* (including third-party ad network cookies and tracking pixels)
   d. **Marketing Communications Consent**: Individual channels presented separately: Email, SMS/Text Message, Push Notification, Postal Mail. Each channel includes a brief description of typical content and anticipated frequency.
   e. **Product-Specific Processing Consent**: Additional consent questions specific to the Meridian product line being accessed. For Clinical AI Platform, this includes the automated decision-making consent. For HealthPay, this includes consent for credit and financial eligibility assessments.
3. The data subject makes their selections and clicks the "Save Preferences" button.
4. Upon button click, the CMP:
   a. Generates a unique Consent Receipt ID (format: `CR-{datacenter}-{timestamp}-{random-hex-16}`).
   b. Captures the full payload in an immutable Consent Record, including the data subject's session identifier, the exact disclosures rendered (version controlled), the selections made, the timestamp (UTC), and the channel identifier.
   c. Stores the Consent Record in the CMP database, encrypted at rest.
   d. Transmits the Consent Record to the CDP via the Segment Consent API endpoint.
5. The CDP propagates the consent state to all downstream destinations (see Section 5.4).
6. The data subject receives a confirmation email at their registered email address summarizing their consent choices and providing a direct link to the Preference Center.

**5.1.2 Assisted Consent Capture (Call Center and In-Person)**

This procedure applies when consent is collected by a Meridian Customer Support agent (Tier 1 or Tier 2) or by an authorized provider partner staff member.

1. The assisting personnel authenticate to the Meridian Customer Service Console (Salesforce Health Cloud Service Console).
2. The personnel navigate to the "Consent Management" tab associated with the data subject's record.
3. The personnel verbally present the consent disclosures for each applicable processing purpose, using the jurisdiction-appropriate disclosure scripts maintained in the Knowledge Base (KB-CNS-Category).
4. The data subject indicates their choices verbally.
5. The personnel record each choice in the CMP via the Service Console integration, selecting the appropriate purpose code from the dropdown.
6. The personnel must read the "Verification Statement" displayed on screen, confirming the data subject's identity and that the choices recorded accurately reflect the data subject's expressed wishes.
7. The personnel sets the "Collection Method" field to `ASSISTED` and the "Assisting Agent" field to their Staff ID.
8. The personnel clicks "Submit." The CMP generates a Consent Record as in 5.1.4(c) above, with an additional metadata field specifying the assisted collection context.
9. For telephone collections, a recording of the consent interaction is retained for 90 days in the call recording system linked to the CRM interaction record, after which it is automatically purged.
10. A confirmation of consent preferences is sent to the data subject via email or postal mail, depending on the primary contact method on file.

### 5.2 Preference Center Access and Usage

The Preference Center is the central self-service portal for consent management, accessible at `preferences.meridian.com`.

**5.2.1 Authentication**

1. The data subject navigates to `preferences.meridian.com`.
2. The data subject is prompted to authenticate using one of the following methods:
   a. Email + Magic Link (IAP sends a one-time login code to the registered email address, valid for 15 minutes).
   b. SMS + One-Time Passcode (sent to the registered mobile number).
   c. Social login (Google, Apple ID — where federated identity is configured and linked to the Meridian profile).
3. Upon successful authentication, the Preference Center renders all current consent states for the data subject, organized by purpose category.

**5.2.2 Viewing and Modifying Consents**

1. The data subject views their current consents in a table format listing:
   - Processing Purpose (plain language description)
   - Purpose Code (internal reference)
   - Current Status (Active, Withdrawn, Expired)
   - Date of Last Action
   - Expiry Date
2. To modify a consent, the data subject toggles the switch for the relevant purpose. The interface presents a confirmation dialog: "You are changing your consent for [Purpose]. Are you sure you wish to [Grant / Withdraw] consent for this purpose?"
3. Upon confirmation, the CMP generates a new Consent Record reflecting the updated state.
4. The withdrawal or granting propagates downstream per Section 5.4.
5. A confirmation email is sent summarizing the change.

**5.2.3 Global Withdrawal**

The Preference Center provides a "Withdraw All Optional Consents" button at the top of the consent listing. Executing this action:

1. Withdraws all consents except those strictly necessary for the performance of a contract to which the data subject is a party or for compliance with a legal obligation.
2. Sets the global marketing suppression flag in Salesforce Marketing Cloud.
3. Queues the data subject's profile for processing activity cessation in all batch and streaming pipelines (target: completion within SLA per Section 5.4.3).

### 5.3 Marketing Consent Management

Marketing consent is managed distinctly from processing consent due to the Soft Opt-In provision and the use of separate marketing automation systems.

**5.3.1 Consent Capture for Marketing**

1. Marketing consent collection points (website footers, HealthPay enrollment checkout, webinar registration, white-paper downloads) present a clear, unticked checkbox with text specific to the communication channel.
2. The text must include: "I consent to receive marketing communications from Meridian Health Technologies by [Channel]. I understand that I may withdraw my consent at any time by [link to Preference Center] or by clicking the unsubscribe link in any communication."
3. Upon check and form submission, the consent event is recorded in the CRM Marketing Consent object, tagged with the `Marketing_Channel` picklist value and the campaign source identifier.

**5.3.2 Soft Opt-In Application (Existing Customer Communications)**

For existing customers of a specific Meridian product line (e.g., HealthPay users), Meridian may send marketing communications about similar Meridian products or services via email without prior explicit consent, provided:
1. The data subject's email was collected in the context of a sale or registration for the service.
2. A clear and conspicuous opportunity to opt out of marketing was given at the time of collection (the initial sign-up form must include an "I do not wish to receive marketing communications" checkbox, unchecked by default).
3. Each subsequent marketing communication includes a valid, one-click unsubscribe mechanism.
4. The data subject has not previously opted out.

The Soft Opt-In applies only to Email and only to Meridian's own similar products. It does not apply to SMS, push notifications, postal mail, or any third-party marketing communications.

**5.3.3 Unsubscribe Processing**

1. Every marketing email sent from Meridian systems includes an unsubscribe link in the footer. The link is unique to the recipient and includes an encoded identifier.
2. Clicking the unsubscribe link:
   a. Immediately records an unsubscribe event in the CRM.
   b. Sets the `Marketing_Email_Opt_Out` flag to `TRUE` on the contact record.
   c. Adds the email address to the Global Marketing Suppression List in Salesforce Marketing Cloud.
3. Unsubscribe processing must complete within 60 seconds of link activation.
4. The data subject is redirected to a confirmation page: "You have been unsubscribed from marketing emails from Meridian Health Technologies. Please allow up to 24 hours for our systems to fully update. You may manage all your communication preferences in our [Preference Center link]."
5. For SMS, the recipient may reply "STOP" to any Meridian SMS short code to immediately opt out of SMS marketing for that product.

### 5.4 Consent Propagation and Lifecycle Management

Consent propagation ensures that a consent state change in the CMP is reflected across all systems that process data for the affected purpose.

**5.4.1 Propagation Architecture**

```
Consent Event (CMP) → CDP (Segment) → Downstream Destinations
                                    ├── CRM (Salesforce Health Cloud)
                                    ├── Marketing Cloud (Salesforce)
                                    ├── Clinical AI Platform (Meridian Data Lake)
                                    ├── HealthPay Platform (Account Service)
                                    ├── MedInsight Analytics (Snowflake Data Warehouse)
                                    └── Third-Party Processors (via API)
```

**5.4.2 Propagation SLA**

| Consent State Change | Propagation Initiation | Propagation Completion (All Destinations) |
|---|---|---|
| Withdrawal (Global or per purpose) | Real-time (< 5 seconds) | < 5 minutes |
| New Consent Grant | Real-time (< 5 seconds) | < 2 minutes |
| Consent Expiry (automated) | Batch, hourly | < 3 hours from expiry event |
| Administrative Invalidation | Manual, initiated by Privacy Office | < 24 hours |

**5.4.3 Propagation Verification**

1. Upon each consent state change, the CDP emits a "Consent Sync" event to each destination.
2. Each destination acknowledges receipt back to the CDP's monitoring endpoint.
3. The CDP maintains a Sync Status dashboard, refreshed every 30 seconds, showing the propagation status for each destination system.
4. If any destination fails to acknowledge the consent sync event within the SLA period, an automatic alert is generated in PagerDuty to the Data Platform Engineering on-call engineer.

**5.4.4 Consent Expiry and Renewal**

1. A nightly batch process (Meridian Consent Lifecycle Job, `consent-lifecycle-v3`) runs in Apache Airflow that scans all Active Consent records.
2. For each consent record where `Current_Date > Expiry_Date`, the job:
   a. Sets the consent status to `Expired`.
   b. Logs the expiry in the Consent Audit Log.
   c. Triggers propagation per 5.4.2.
3. For consents expiring within 30 days, the Consent Lifecycle Job identifies associated data subjects and, for those with an active email address and non-withdrawn marketing email consent, triggers an automated "Consent Expiration Notice" email via Marketing Cloud. The email includes a direct link to the Preference Center to renew consent.

### 5.5 Withdrawal Handling and Data Processing Cessation

Withdrawal of consent triggers processing cessation across all affected systems.

**5.5.1 Automated Cessation**

Upon propagation of a Withdrawn Consent event:
1. The CRM sets the contact's `Data_Processing_Opt_Out` flag for the relevant processing activity to `TRUE`.
2. The Clinical AI Platform (Data Pipeline) removes the subject's identifier from active processing queues for the relevant AI/ML model runs.
3. HealthPay ceases eligibility pre-screening assessments for the withdrawn purpose.
4. MedInsight Analytics removes the subject's data from active analytic population cohorts (the Subject Access Management module in the Snowflake data warehouse, `snowflake-subject-access-mgmt`, handles row-level enforcement).
5. Marketing Cloud suppresses the contact for the specific marketing channel withdrawn.

**5.5.2 Non-Automated Cessation Verification**

For high-risk processing activities (automated decision-making, special category data processing), the Privacy Office conducts a quarterly cessation verification audit:
1. A sample of 50 withdrawn consents from the preceding quarter is selected.
2. For each sample, the Privacy Office queries the relevant processing system to confirm that the data subject's data is no longer being actively processed for the withdrawn purpose.
3. Results are documented in the Consent Cessation Audit Report, maintained in the Privacy Office's audit folder.

### 5.6 Consent for Financial Product Eligibility (HealthPay)

HealthPay processes personal data for creditworthiness and eligibility assessments. This processing requires explicit, separate consent.

1. During HealthPay product enrollment or credit application, the interface presents a dedicated "Financial Processing Consent" section after the general consent capture.
2. The disclosure text must state: "I consent to Meridian Health Technologies, Inc. conducting an assessment of my financial eligibility, which may include automated processing of my financial and personal data to determine my eligibility for payment plans and related financial products. This assessment may be conducted by Meridian or an authorized third-party processor. I understand I may withdraw this consent at any time by visiting [Preference Center link] or by contacting Customer Support."
3. If the data subject does not grant this consent, Meridian shall not conduct the automated eligibility assessment. The data subject may still be offered manual underwriting options where available.
4. If consent for financial processing is withdrawn, any in-progress applications dependent on that consent shall be paused, and the data subject notified via their primary contact method.

## 6. Controls and Safeguards

### 6.1 Technical Controls

| Control ID | Control Description | Implementation |
|---|---|---|
| TC-CNS-001 | CMP Database Encryption at Rest | AES-256; keys managed in AWS KMS, rotated annually |
| TC-CNS-002 | Consent Record Immutability | CMP database configured with append-only tables; no UPDATE or DELETE operations permitted on consent history |
| TC-CNS-003 | Consent API Authentication | All inter-service consent API calls authenticated via OAuth 2.0 client credentials grant with short-lived tokens (60-minute expiry) |
| TC-CNS-004 | Consent Data in Transit Encryption | TLS 1.3 enforced for all consent data flows between Meridian services |
| TC-CNS-005 | PII Pseudonymization in Logs | Consent service logs redact data subject email, phone, and name fields; only anonymized Consent Receipt ID is logged |
| TC-CNS-006 | Preference Center Rate Limiting | WAF rate limit: 10 requests per second per IP; 30 requests per minute per authenticated user |
| TC-CNS-007 | SIEM Integration | All consent events streamed to Splunk SIEM for anomalous pattern detection (e.g., bulk consent withdrawal spikes) |

### 6.2 Administrative Controls

| Control ID | Control Description | Implementation |
|---|---|---|
| AC-CNS-001 | Consent Disclosure Change Management | All changes to consent disclosure text must be reviewed by Privacy Office and Legal, versioned in OneTrust, and deployed via standard change control (Jira ticket, peer review) |
| AC-CNS-002 | Quarterly Consent Governance Review | VP Customer Ops, CPO, and CISO review consent metrics, propagation failures, and regulatory updates; minutes documented |
| AC-CNS-003 | Consent Deletion Freeze | During active litigation holds or regulatory investigations, consent records subject to hold shall not be deleted even if retention period has expired; hold is managed by Legal in OneTrust |
| AC-CNS-004 | Separation of Duties | Engineers deploying CMP configurations do not have Write access to Consent Audit Logs; Privacy Office personnel auditing logs do not have Write access to CMP configurations |

### 6.3 Records Retention

| Record Type | Retention Period | Justification |
|---|---|---|
| Consent Records (Active and Expired) | Duration of data subject relationship + 6 years | Regulatory defense and auditability |
| Withdrawn Consent Records | 6 years from date of withdrawal | Defense against claims; evidence of withdrawal compliance |
| Consent Audit Logs | 7 years | Security investigation support |
| Consent Disclosure Versions | Indefinite (archived) | Required to reconstruct the exact disclosure presented at any past consent event |

Retained consent records are eventually transferred to the Meridian Glacier Archive (AWS S3 Glacier Deep Archive) after 2 years of inactivity, with retrieval SLA of 48 hours.

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs)

| KPI ID | Metric | Target | Measurement Method |
|---|---|---|---|
| KPI-CNS-001 | Consent Propagation Latency (Real-Time) | Mean < 60 seconds, P99 < 5 minutes | CDP propagation monitoring dashboard; Datadog APM traces |
| KPI-CNS-002 | Withdrawal Processing Time (Automated) | 100% completion within 5 minutes | Cessation verification script, executed daily |
| KPI-CNS-003 | Preference Center Availability | 99.9% uptime (monthly) | Pingdom synthetic monitor; Okta authentication status |
| KPI-CNS-004 | Consent Capture Abandonment Rate | < 15% (users who start but do not complete consent flow) | Segment funnel analysis |
| KPI-CNS-005 | Manual Withdrawal Ticket SLA Compliance | 100% processed within 2 business days of receipt | Zendesk reporting, filtered by ticket tag `consent_withdrawal_manual` |
| KPI-CNS-006 | Consent Record Integrity | 0 records with unpropagated state mismatch | Weekly reconciliation script comparing CMP, CDP, and CRM consent states |
| KPI-CNS-007 | Expired Consent Renewal Rate | Not targeted (informational only) | Monthly report; renewals / (renewals + expirations) |

### 7.2 Dashboards and Reporting Cadence

**7.2.1 Operational Dashboards (Real-Time)**
- CMP Health Dashboard (Grafana): API response times, error rates, consent event rate.
- Propagation Status Dashboard (Segment + Datadog): Real-time sync status per destination.
- Preference Center Availability Monitor (Pingdom public status page).

Access: Engineering teams, IT Operations (Samantha Torres' team), on-call personnel.

**7.2.2 Monthly Reporting**
- **Audience**: VP Customer Ops, VP Product Management, Privacy Office.
- **Contents**: All KPIs, trend charts (MoM comparison), exception log summary (Section 8), top five consent-related support ticket categories.
- **Distribution**: PDF report emailed by the 5th business day of each month.

**7.2.3 Quarterly Regulatory Reporting**
- **Audience**: Executive Leadership Team, Board Audit Committee (summary).
- **Contents**: Consent withdrawal volumes by purpose, DSAR trends correlated with consent events, regulatory landscape updates impacting consent, material consent disclosure changes.
- **Prepared by**: Privacy Office, with data inputs from Customer Operations.

## 8. Exception Handling and Escalation

Deviation from the procedures defined in this SOP must follow the exception process below. Routine operational incidents (e.g., a failed consent propagation that self-recovers) are handled via standard incident management and do not require a formal exception ticket.

### 8.1 Exception Request Process

1. The requester (any Meridian personnel) opens a Jira ticket in the `CNS-EXCP` project.
2. The ticket must include:
   a. **SOP Section**: The specific section of this SOP from which deviation is requested.
   b. **Nature of Exception**: Detailed explanation of what will differ from the standard procedure.
   c. **Scope**: Specific data subjects, products, or time periods affected.
   d. **Risk Assessment**: Analysis of the data subject impact and regulatory risk introduced.
   e. **Mitigating Controls**: Technical or procedural controls compensating for the deviation.
   f. **Duration**: Proposed start and end dates for the exception.
3. The ticket is routed to the Privacy Office for risk assessment.
4. Privacy Office annotates the ticket with regulatory risk classification: **Low**, **Medium**, or **High**.

### 8.2 Approval Authority

| Risk Classification | Approver |
|---|---|
| Low | Privacy Office designee (any Privacy Analyst) |
| Medium | Dr. Klaus Weber, CPO / DPO |
| High | Dr. Klaus Weber, CPO / DPO + Michael Chang, VP Customer Operations (joint approval) |

All exceptions classified High must be logged in the Enterprise Risk Register and reported to the quarterly Consent Governance Review.

### 8.3 Escalation Path

For consent-related incidents requiring urgent resolution (e.g., CMP outage preventing consent capture, global consent propagation failure):

1. **Detection**: Automated alerting in PagerDuty (Datadog monitor for CMP availability or consent sync failure thresholds).
2. **Tier 1 Response**: Engineering on-call acknowledges within 15 minutes, begins diagnosis.
3. **If unresolved within 2 hours**: Incident escalated to Data Platform Engineering Manager.
4. **If unresolved within 6 hours or if incident is customer-facing and widespread**: Executive notification (VP Customer Operations, VP IT Operations, CISO, CPO). A customer-facing status page update is published at `status.meridian.com`.
5. **Post-Incident**: Root Cause Analysis (RCA) document prepared within 5 business days; reviewed at next Consent Governance Review.

### 8.4 Business Continuity

If the CMP is fully unavailable, a "degraded consent mode" is activated:
1. Consent collection interfaces display a static fallback notice (hosted in CDN edge cache) informing the user: "We are experiencing technical difficulties affecting consent management. By proceeding, your consent choices will be captured and honored once our systems recover. You may manage your preferences at [Preference Center link] once service is restored."
2. Where feasible, essential consent events are queued client-side (in browser local storage as a temporary buffer) and replayed to the CMP upon service restoration.

## 9. Training Requirements

All Meridian personnel with responsibilities under this SOP must complete applicable consent management training.

### 9.1 Training Curriculum

| Course Code | Course Title | Audience | Frequency |
|---|---|---|---|
| CNS-TRN-101 | Consent Management Fundamentals | All Customer Operations, all Product Managers, all Engineering personnel | Onboarding + Annual |
| CNS-TRN-201 | Advanced Consent Configuration (OneTrust) | Consent Administrators (Privacy Office, select Engineers) | Onboarding + Bi-annual |
| CNS-TRN-301 | Consent in Clinical Contexts | Clinical AI Platform product and support teams | Onboarding + Annual |
| CNS-TRN-401 | Financial Consent Compliance | HealthPay product and support teams | Onboarding + Annual |

**CNS-TRN-101 Modules**:
1. What is Consent? Concepts and Definitions
2. Meridian Consent Architecture Overview
3. Consent Capture Procedures (Digital and Assisted)
4. Withdrawal Processing and Escalation
5. Preference Center and Support Ticket Handling
6. SOP-COPS-010 Policy Assessment (20 multiple-choice questions; pass mark: 80%)

### 9.2 Training Tracking

1. All training assignments are managed through the Meridian Learning Management System (LMS: Workday Learning).
2. Course completion is tracked by employee ID.
3. Managers receive monthly LMS compliance reports listing team members with overdue training.
4. Non-completion of mandatory consent training within 30 days of assignment results in an automated notification to the employee's manager and the Privacy Office. Continued non-compliance after 60 days is escalated to the VP of the relevant business unit.

### 9.3 Training Content Review

Training materials are reviewed at least annually by the Privacy Office and the VP of Customer Operations to ensure alignment with current regulatory guidance and Meridian procedures. The review is triggered at the Next Review date of this SOP.

## 10. Related Policies and References

This SOP does not exist in isolation. Personnel must be familiar with the following interconnected policies:

### 10.1 Meridian Internal Policies

| SOP ID | Title | Relationship |
|---|---|---|
| SOP-ISMS-003 | Information Security Incident Response | Incident response procedures for consent system breaches |
| SOP-PRIV-002 | Personal Data Retention and Deletion | Governs deletion of personal data after consent withdrawal or expiry |
| SOP-PRIV-005 | Data Subject Rights Request Handling | Procedure for fulfilling DSARs referencing consent records |
| SOP-PRIV-008 | Processing Activity Inventory Management | Maintains the PAI referenced in consent purposes |
| SOP-PRIV-012 | Cookie and Tracking Technology Governance | Technical standards complementing this SOP for web tracking |
| SOP-ENG-015 | Change Management for Customer-Facing Systems | Change control for consent interface and CMP modifications |
| SOP-COPS-005 | Customer Communication Standards | Branding, tone, and accessibility standards for consent disclosures |
| SOP-RSCH-042 | Research Partner Consent and Enrollment | Out-of-scope consent scenarios for clinical research |
| SOP-LEGAL-009 | Litigation Hold and Legal Preservation | Overrides standard consent record retention during legal holds |

### 10.2 External References

| Reference | Identifier |
|---|---|
| Regulation (EU) 2016/679 (General Data Protection Regulation) | GDPR |
| ICO Guidance on Consent under GDPR | ICO Consent Guidance (May 2021) |
| EDPB Guidelines 05/2020 on Consent | EDPB 05/2020 |
| CAN-SPAM Act of 2003 (United States) | 15 U.S.C. §§ 7701-7713 |
| Canada's Anti-Spam Legislation (CASL) | S.C. 2010, c. 23 |
| Singapore Personal Data Protection Act 2012 | PDPA |
| Meridian OneTrust CMP Configuration Guide | Internal Wiki: /wiki/onetrust-cmp-config |
| Meridian Customer Data Platform Architecture | Internal Wiki: /wiki/cdp-architecture-v4 |

## 11. Revision History

| Version | Date | Author / Editor | Summary of Changes |
|---|---|---|---|
| 5.6 | 2025-12-24 | J. Lee (Privacy) | Annual review: Updated Soft Opt-In language per latest regulatory guidance; revised SLA timings for batch propagation; added Financial Consent (HealthPay) procedure subsection 5.6. No structural changes. |
| 5.5 | 2025-06-21 | M. Chang (VP Cust Ops) | Mid-cycle review: Adjusted consent expiry from 24 to 36 months (PS-CNS-007); updated CMP vendor from legacy platform to OneTrust migration completion; revised roles reflecting post-migration responsibilities. |
| 5.4 | 2024-11-15 | K. Weber (CPO) | Incorporated Automated Decision-Making consent per Clinical AI Platform launch (PS-CNS-009, Section 5.1.2.e). Added Consent Renewal flow in Section 5.4.4. Updated training curricula for CNS-TRN-301. |
| 5.3 | 2024-06-10 | S. Torres (VP IT Ops) | Technical update: Revised consent propagation architecture diagram (Section 5.4.1) to reflect CDP migration to Segment. Updated propagation SLA from 15 minutes to 5 minutes (Section 5.4.2). |
| 5.2 | 2024-01-06 | J. Lee (Privacy) | Full policy rewrite: aligned to new corporate template. Expanded procedures from conceptual guidance to step-by-step. Introduced RACI matrix, KPI framework, formal exception handling. Changed document owner to VP Customer Operations. |
| 4.1 | 2023-05-12 | K. Weber (CPO) | Interim update: Added Minor Data Subject Consent policy (PS-CNS-008) in response to Clinical AI Platform expansion to pediatric providers. |