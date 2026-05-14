---
sop_id: "SOP-COPS-014"
title: "Knowledge Base Management"
business_unit: "Customer Operations"
version: "4.6"
effective_date: "2024-04-08"
last_reviewed: "2025-08-17"
next_review: "2026-02-20"
owner: "Michael Chang, VP of Customer Operations"
approver: "Robert Liu, VP of Financial Services"
classification: "Internal"
regulations:
  - "SOC 2"
status: "Active"
---

# Standard Operating Procedure: Knowledge Base Management

## 1. Purpose and Scope

### 1.1 Purpose

The purpose of this Standard Operating Procedure (SOP) is to establish a structured, controlled, and auditable framework for the creation, review, approval, publication, maintenance, and retirement of knowledge base (KB) content within Meridian Health Technologies, Inc. Customer Operations. This SOP ensures that all customer-facing and internally-facing knowledge artifacts are accurate, consistent, secure, and compliant with the SOC 2 (System and Organization Controls 2) Trust Services Criteria, specifically focusing on the Security, Availability, and Processing Integrity categories.

### 1.2 Scope

This SOP applies to all personnel—including full-time employees, contractors, and third-party vendors—who create, edit, approve, or manage content within the official Meridian knowledge management systems. The scope encompasses:

- **External Knowledge Base:** The customer-facing help center accessible via the Meridian SaaS Platform, HealthPay Patient Portal, and Clinical AI Platform clinician interface.
- **Internal Knowledge Base:** The repository used by Customer Operations, Support Engineering, and Implementation teams to diagnose and resolve issues.
- **Content Types:** Help articles, troubleshooting guides, FAQs, runbooks, standard response templates, release notes, known error records, and policy micro-snippets.
- **Systems in Scope:**
    - **ServiceNow Knowledge Management (SN-KM):** Primary platform for technical articles and known error records.
    - **Confluence Cloud (Atlassian):** Platform for internal runbooks, implementation guides, and long-form process documentation.
    - **Zendesk Guide:** Platform for customer-facing help articles.

This SOP does **not** cover the management of the Meridian Product Documentation (API references, SDK documentation), which is governed by **SOP-ENG-087 (Technical Documentation Lifecycle)**. Marketing collateral and blog posts are also explicitly out of scope.

---

## 2. Definitions and Acronyms

| Term | Definition |
|---|---|
| **KB** | Knowledge Base |
| **KB Article** | A single, discrete unit of knowledge content. |
| **KCS** | Knowledge-Centered Service; a methodology for integrating knowledge creation into the incident resolution process. |
| **SN-KM** | ServiceNow Knowledge Management, the system of record for technical KB articles. |
| **Approved Publisher** | A role authorized to publish content after review. |
| **CCCI** | Common Criteria for Controls Implementation, used internally to map SOC 2 criteria to specific technical controls. |
| **TSC** | Trust Services Criteria, the principles used to evaluate controls in a SOC 2 engagement (Security, Availability, Processing Integrity, Confidentiality, Privacy). |
| **Processing Integrity** | The SOC 2 principle that system processing is complete, valid, accurate, timely, and authorized. Applied here to ensure KB content is accurate and authorized. |
| **Known Error** | A problem that has a documented root cause and a workaround or permanent fix, recorded in SN-KM. |
| **Macro** | A pre-formatted response in Zendesk for use by Tier 1 support agents. |

---

## 3. Roles and Responsibilities

The following RACI matrix delineates responsibilities for the Knowledge Base lifecycle. Named roles correspond to the active organizational chart as of Q1 2024.

| Role | Persona | Responsibility | RACI (Create/Review/Approve/Support) |
|---|---|---|---|
| **Content Creator** | Tier 1-3 Support Agents, Implementation Specialists | Drafts new articles, flags outdated content. | R (Responsible) |
| **Technical Reviewer** | SME Tier 3, Clinical Informatics (CIU) for Clinical AI content, Financial Compliance for HealthPay content | Validates technical accuracy and regulatory compliance. | C (Consulted) |
| **Knowledge Manager** | Sarah Jenkins, CMgr | Manages the KB workflow, style guide adherence, duplicate detection. | A (Accountable) |
| **Content Approver** | Lead, Tier 2 Support; Manager, Implementation Success | Approves content for publishing based on completeness and tone. | A (Accountable) |
| **VP of Customer Ops** | Michael Chang | Exception handling, policy escalation, final authority on KB scope. | A (Accountable - Exceptions) |
| **VP of Financial Services** | Robert Liu | Approver for any KB content referencing HealthPay billing logic or financial reconciliation. | A (Accountable - HealthPay) |

---

## 4. Policy Statements

The Meridian Knowledge Base is a controlled, auditable asset that directly impacts customer satisfaction (CSAT), operational efficiency (MTTR - Mean Time to Resolve), and compliance with AICPA SOC 2 Trust Services Criteria (specifically **CC7.1 System Operations**, **PI1.2 Accuracy & Completeness**, and **A1.2 System Availability**). The following high-level policies govern all KB activities:

- **Policy 4.1 (Accuracy & Integrity):** All published content must be technically verified and free of logical contradictions. Under no circumstances shall a KB article prescribe a workflow that violates another Meridian SOP or bypasses a system security control.
- **Policy 4.2 (Proactive Creation):** Support follows the Knowledge-Centered Service (KCS) methodology. A draft KB article must be created during the resolution of any Priority 1 (P1) major incident, or whenever a recurring ticket cluster is identified (5+ related tickets in 30 days).
- **Policy 4.3 (Access Control & Confidentiality):** Access to the Authoring environment in Zendesk Guide and Confluence must be restricted via SSO and MFA. Public-facing content must never contain internal hostnames, IP addresses, database connection strings, or API keys.
- **Policy 4.4 (Content Freshness):** No article shall remain unreviewed for more than 180 days. Content linked to the HealthPay billing engine must be reviewed every 90 days or following any update to the billing rules, whichever is sooner.

---

## 5. Detailed Procedures

### 5.1 Article Creation

**5.1.1 Identification of Need**

A new Knowledge Base article is required when:
1. A new feature is released (triggered by the Product Release Management process, **SOP-ENG-002**).
2. A Tier 2 agent or Implementation Specialist identifies a recurring support gap (CSAT score < 80% for a specific topic area).
3. A Known Error record is created in ServiceNow following a Root Cause Analysis (RCA) for a P1 or P2 incident (**SOP-ITSM-005**).

**5.1.2 Drafting**

1. The **Content Creator** navigates to the respective Authoring tool (Zendesk Guide for external, Confluence for internal, ServiceNow Known Error form for technical bugs).
2. The Creator must select the appropriate **Template** from the global template library (see Section 5.1.3).
3. The Creator drafts the content, ensuring all placeholders (`<VARIABLE>`) are replaced with specific values.
4. The Creator must set an initial metadata tag: “Draft – Unverified.”

**5.1.3 Mandatory Templates**

To ensure Processing Integrity, all articles must use a standardized template:
- **External Article (Zendesk Guide):** “Standard Help Article – V4.” Includes sections: Issue, Environment, Resolution, Cause (optional).
- **Internal Runbook (Confluence):** “Diagnostic Runbook – V3.” Includes: Alert Trigger, Log Query (obfuscated), Remediation Steps, Rollback Procedure, Escalation Path.
- **Known Error (ServiceNow):** “KE Record Template.” Includes: Problem Record ID, Root Cause, Symptom, Workaround, Recovery Time Objective (RTO).

### 5.2 Peer Review & Technical Validation

All content must undergo a structured peer review before being submitted for formal approval.

**5.2.1 Self-Review Checklist**

The Creator must complete this checklist before sending for review:
- [ ] No internal URLs or IPs are exposed (8.8.8.8 or 10.x.x.x).
- [ ] Spelling/grammar verified via Grammarly Premium (Meridian Enterprise License).
- [ ] Screenshots have been sanitized (no visible customer data, user IDs, or API keys). Use Snagit Editor blur tool (protocol **OPS-SEC-003**).

**5.2.2 Formal Review**

1. The Creator submits the article for review via the built-in workflow in Zendesk/Confluence/ServiceNow.
2. The **Technical Reviewer (SME)** is auto-assigned via Round-Robin logic based on the Product Category tag. If the tag is `Clinical_AI`, the request is routed to the Clinical Informatics Unit (CIU) queue.
3. The SME must verify:
    - The technical steps result in the stated resolution success state.
    - The steps do not introduce security risks (e.g., suggesting disabling MFA for a user).
    - For HealthPay-related content, an automatic escalation is sent to **Robert Liu’s** delegate for financial reconciliation logic verification.
4. If the SME rejects the content, they must provide specific, actionable feedback in the "Rejection Notes" field. The status reverts to "Needs Revision."
5. Review SLA: Internal Runbooks must be reviewed within 8 business hours. External Knowledge articles must be reviewed within 24 business hours. P1 Outage post-mortem drafts must be reviewed within 4 hours.

### 5.3 Accuracy Verification (Publishing)

The final publishing step is gated on an independent “Accuracy Audit.”

1. The **Content Approver** checks the SME’s verification notes.
2. **Procedural Accuracy Check:** The Approver manually executes the steps on a sanitized Test environment (Meridian UAT Non-Prod) or follows the logic flow.
3. **Contextual Accuracy Check:** The Approver verifies that the article aligns with the current Meridian release nomenclature (e.g., verifying the UI label matches the current release `2024.02.1`, not `2024.01.0`).
4. Upon passing the Accuracy Audit, the Approver clicks **Publish**.
5. The Zendesk/Confluence connector syncs an uneditable copy of the published document and the complete audit log (timestamps, user IDs, approval notes) to the immutable compliance archive (Amazon S3 Glacier Deep Archive, bucket: `meridian-kb-compliance-archive`). Retention period: 7 years.

### 5.4 Scheduled Review Cycle

**5.4.1 Trigger**

The Knowledge Manager (Sarah Jenkins) receives an automated report from the KB Dashboard (Grafana) every Monday at 08:00 ET.

**5.4.2 Review Process**

1. **Verify:** The assigned Subject Matter Expert (original Creator or successor) attempts to execute the article’s instructions in the current production environment.
2. **Update:** If UI steps have changed, the article is updated. If a permanent fix has been released, the “Workaround” section is replaced with the fix version.
3. **Retire:** If the feature has been deprecated, the article status is changed to “Retired.” The KB record is kept for historical searchability but a large, red dismissible banner is added: “This article applies to a deprecated feature.”
4. **No Changes:** The SME clicks “Mark as Verified,” which timestamps the `last_verified` field in the metadata. This fulfills the 180-day freshness policy.

---

## 6. Controls and Safeguards

This section specifically maps internal controls to **SOC 2 Trust Services Criteria (TSC)** , ensuring Meridian meets the requirements of its Type II audit.

### 6.1 Logical Access Controls (SOC 2 CC6.1, CC6.3)

| Control | Description | Tool/System |
|---|---|---|
| **KB-AUTH-01** | Authoring system access is restricted via Single Sign-On (SSO) integrated with Okta IdP and enforced by Multi-Factor Authentication (MFA). | Okta, Duo |
| **KB-AUTH-02** | Role-Based Access Control (RBAC) restricts publishing capability strictly to the “Content Approver” AD group. Content Creators cannot publish directly to the Live KB. | Active Directory, Zendesk |
| **KB-AUTH-03** | Internal KB (Confluence) access is segregated. Finance Confluence Space is restricted to users with the `FIN_ACCESS` AD attribute, preventing unauthorized viewing of billing-sensitive runbooks. | Confluence Cloud |

### 6.2 Processing Integrity Controls (SOC 2 PI1.2, PI1.3)

Data is processed completely, accurately, and timely.

| Control | Description |
|---|---|
| **KB-PI-01** | **Stale Content Flagging:** A backend script (`kb_stale_check_v2.sh`) runs nightly. Any “Published” article lacking a `last_verified` timestamp within 180 days is automatically flagged with a visible “Potentially Outdated – Verify” banner and moved to an `Expiring` review queue. |
| **KB-PI-02** | **Broken Link Detection:** Integrity scanning via the `linkchecker` utility runs weekly against all Zendesk articles. Any detected 404 links generate an automated ticket (Zendesk via API). Broken links are the responsibility of the original Content Creator to fix within 5 business days. |

### 6.3 Change Management Controls

Per SOC 2 CC8.1, changes to the system must be authorized.

| Control | Description |
|---|---|
| **KB-CHG-01** | Every published state change (Create, Update, Deprecate) generates an immutable log entry containing the user ID, timestamp, article version, and approval ID. This log is shipped to Splunk for real-time monitoring. |
| **KB-CHG-02** | Bulk changes (e.g., mass updates due to a UI rebranding) require a Standard Change Request in ServiceNow, approval by the VP of Customer Operations, and must be performed in a "Sandbox" branch before merging to the production KB, per SOP-COPS-014 change protocol. |

---

## 7. Monitoring, Metrics, and Reporting

The health of the Knowledge Base is monitored continuously.

### 7.1 Key Performance Indicators (KPIs)

| Metric | Target | Measurement Tool | SOC 2 Relevance |
|---|---|---|---|
| **Time to Publish (TTP)** | < 5 hrs (Internal SEV1 fix), < 72 hrs (General Article) | SN-KM Analytics | Availability (A1.2) - Quick fix publication restores service. |
| **Article Reuse (KCS)** | > 80% of incidents linked to an existing KB article | Zendesk Solve API | Efficiency. |
| **Stale Content (< 10%)** | < 10% of total articles flagged as "Unverified" over 180 days | Grafana Dashboard | Processing Integrity (PI1.2) - Ensures accuracy. |
| **Deflection Rate** | > 700 tickets/month prevented by KB self-service | Google Analytics / Zendesk Web Widget | Availability (A1.2). |

### 7.2 Reporting Cadence

| Report | Audience | Frequency |
|---|---|---|
| **KB Operational Scorecard** | Director, Customer Support | Weekly (Mon) |
| **Content Quality Audits** | Knowledge Manager (Sarah Jenkins) | Bi-Weekly (Fri) |
| **SOC 2 PI Compliance Review** | CISO, VP Tech Ops, VP Customer Ops | Monthly |
| **Quarterly KB Roadmap** | Executive Leadership | Quarterly |

---

## 8. Exception Handling and Escalation

Deviations from this SOP must be documented and approved.

**8.1 Emergency Publishing (SOC 2 Exception)**

In the event of a Severity 1 (System Down) incident requiring an immediate customer-facing notice (status page update or emergency workaround):
1. The Incident Commander has authority to draft a KB article bypassing the formal peer review.
2. **Approval Bypass for P1:** The VP of Customer Operations (Michael Chang), or appointed delegate, may verbally approve publication via a recorded bridge line.
3. **Post-Incident Review:** Within 24 hours, the article must undergo the standard retrospective technical review and be retroactively logged as an "Emergency Change" to satisfy SOC 2 CC8.1 auditor expectations.

**8.2 Escalation Path for Content Disputes**

| Level | Role | Trigger |
|---|---|---|
| **Level 1** | Knowledge Manager (Sarah Jenkins) | Creators cannot agree on KB wording or procedure. |
| **Level 2** | VP of Customer Ops (Michael Chang) | Dispute involves inter-department conflict (e.g., Support vs. Engineering documentation). |
| **Level 3** | Chief Compliance Officer (CCO) | Content may contain a legal or regulatory risk related to Clinical AI medical claims (FDA/EU MDR). |

---

## 9. Training Requirements

Effective KB management requires skilled personnel.

**9.1 Required Initial Training**

All Customer Operations staff must complete the following internal certifications within 30 days of hire:
- **Course COP-101: Knowledge-Centered Service (KCS) Fundamentals.** Covers search before solve, content creation in the resolution flow.
- **Course COP-102: Meridian Technical Writing Standards.** Focus on the specific templates of Section 5.
- **Assessment:** Staff must submit three practice articles (one external help, one internal runbook, one Known Error) to the Knowledge Manager for review.

**9.2 Recurring Training**

- **Annual:** All KB Content Creators must complete a mandatory refresher: “SOC 2 Privacy & Processing Integrity in Customer Content.”
- **Audit Ad-Hoc:** If audit review reveals a major quality decline (e.g., consistent failure of the accuracy audit), the offending group will undergo targeted re-training via a "KB Quality Workshop."

---

## 10. Related Policies and References

### 10.1 Internal Meridian SOPs
- **SOP-ENG-087:** Technical Documentation Lifecycle (Product Docs)
- **SOP-ENG-002:** Product Release Management
- **SOP-ITSM-005:** Major Incident & Known Error Management
- **SOP-SEC-011:** Information Classification and Handling
- **SOP-COPS-003:** Social Media & Public Communication Policy

### 10.2 External Standards
- **AICPA SOC 2:** TSC 2017 (Trust Services Criteria for Security, Availability, and Processing Integrity).
- **ITIL 4:** Knowledge Management Practice (SKMS).
- **KCS v6 Consortium:** Knowledge-Centered Service Verified methodology.

---

## 11. Revision History

| Version | Date | Author | Description of Change |
|---|---|---|---|
| 1.0 | 2019-01-15 | Sarah Jenkins | Initial Draft – Separation from Incident SOP. |
| 2.1 | 2020-06-02 | Michael Chang | Added SOC 2 Processing Integrity Controls (Section 6). |
| 3.0 | 2021-10-20 | Sarah Jenkins | Merged Zendesk and Confluence workflows; Adopted KCS methodology officially. |
| 4.0 | 2023-02-14 | Sarah Jenkins | Complete rewrite for SOC 2 Type II audit readiness; Added HealthPay escalation path. |
| 4.2 | 2023-09-01 | Michael Chang | Updated RBAC definitions for Finance Segmentation Control (KB-AUTH-03). |
| 4.5 | 2024-01-10 | Sarah Jenkins | Adjusted Stale Content flag time from 365 to 180 days (CC7.1 Alignment). |
| 4.6 | 2024-04-08 | Michael Chang | Updated Approver (Robert Liu), added CE-marking Clinical context to Exception Handling. |