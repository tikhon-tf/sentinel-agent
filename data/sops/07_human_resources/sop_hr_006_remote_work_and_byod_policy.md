---
sop_id: "SOP-HR-006"
title: "Remote Work and BYOD Policy"
business_unit: "Human Resources"
version: "2.2"
effective_date: "2024-05-16"
last_reviewed: "2025-09-24"
next_review: "2026-03-18"
owner: "Jennifer Walsh, Chief Human Resources Officer"
approver: "Dr. Sarah Chen, CEO"
classification: "Internal"
regulations:
  - "SOC 2"
  - "HIPAA"
  - "GDPR"
status: "Active"
---

# Standard Operating Procedure: Remote Work and BYOD Policy

## 1. Purpose and Scope

### 1.1 Purpose
The purpose of this Standard Operating Procedure (SOP) is to define the security, privacy, and operational requirements for Meridian Health Technologies, Inc. personnel working remotely or utilizing personally owned devices to access Meridian corporate systems, business applications, and protected data. This document establishes a unified control framework that ensures compliance with the Health Insurance Portability and Accountability Act (HIPAA), General Data Protection Regulation (GDPR), System and Organization Controls (SOC) 2 Type II criteria, and internal risk management policies.

### 1.2 Scope

**In-Scope Personnel:**
- All full-time and part-time regular employees of Meridian Health Technologies, Inc., regardless of location (United States, Canada, United Kingdom, Germany, Singapore).
- Independent contractors, temporary workers, and consultants issued a Meridian corporate identity (`@meridianhealth.com`).
- Third-party vendors and business associates granted remote access to Meridian systems under the terms of a Business Associate Agreement (BAA) or Data Processing Agreement (DPA).
- Board members and members of the AI Governance Committee accessing Meridian resources.

**In-Scope Devices:**
- Corporate-managed laptops (Apple macOS, Lenovo Windows) issued by IT Operations.
- Personally owned mobile devices (smartphones, tablets) enrolled in the Meridian Bring-Your-Own-Device (BYOD) program via Microsoft Intune.
- Personally owned desktop or laptop computers used to access Meridian virtual desktop infrastructure (VDI) or web-based applications through secure, thin-client access methods.
- Home networking equipment directly facilitating work connectivity (routers, access points).

**In-Scope Data:**
- Electronic Protected Health Information (ePHI) as defined by HIPAA.
- Personal Data of EU data subjects as defined by GDPR Article 4(1).
- Payment Card Information (PCI) and financial model data governed by SR 11-7.
- Meridian proprietary information classified as "Internal" or "Confidential" as defined in SOP-IS-001 (Information Classification and Labeling).

**Out-of-Scope:**
- Dedicated Meridian physical office locations in Boston, London, and Singapore (addressed in SOP-PHY-001).
- Fully air-gapped research and development (R&D) lab environments that do not permit external connectivity.

### 1.3 Policy Enforcement
Violations of this policy, including intentional circumvention of technical controls, failure to report a compromised device, or unauthorized storage of protected data, will be subject to disciplinary action up to and including termination of employment and referral to law enforcement authorities.

## 2. Definitions and Acronyms

| Term | Definition |
| :--- | :--- |
| **BYOD** | Bring Your Own Device. A personal mobile device enrolled in the Meridian Mobile Device Management (MDM) platform, Microsoft Intune, with a containerized work profile. |
| **ePHI** | Electronic Protected Health Information. Individually identifiable health information transmitted or maintained in electronic media, as defined in 45 CFR § 160.103. |
| **HITRUST** | The Health Information Trust Alliance Common Security Framework, which informs Meridian’s integrated control set. |
| **MDM** | Mobile Device Management. Specifically, the Microsoft Intune platform used for BYOD policy enforcement. |
| **MFA** | Multi-Factor Authentication. An authentication mechanism requiring at least two of the following: something you know (password), something you have (Okta Verify push/hardware token), or something you are (Windows Hello biometric). |
| **VPN** | Virtual Private Network. A secure, encrypted tunnel connecting a remote endpoint to the Meridian corporate network. Meridian uses Palo Alto Networks GlobalProtect with split tunneling disabled for Tier-1 data access. |
| **VDI** | Virtual Desktop Infrastructure. Specifically, the VMware Horizon platform providing access to a virtualized Windows desktop within Meridian-owned data centers. |
| **WAF** | Web Application Firewall. A security service protecting Meridian telehealth web applications. |
| **ZTNA** | Zero Trust Network Access. The architectural principle governing access: no implicit trust based on network location. |
| **SEIM** | Security Information and Event Management. The Splunk ES platform used for log aggregation and threat detection. |
| **EDR** | Endpoint Detection and Response. The CrowdStrike Falcon suite deployed to all corporate and VDI endpoints. |
| **UEBA** | User and Entity Behavior Analytics. Algorithms in Splunk used to detect anomalous user behavior. |

## 3. Roles and Responsibilities

### 3.1 Responsibility Assignment Matrix (RACI)

| Activity / Task | Chief HR Officer (Owner) | Chief InfoSec Officer | VP, IT Operations | Employee / Worker | Direct Manager | Data Protection Officer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Policy Maintenance & Annual Review** | **A** | C | C | I | I | C |
| **Employee Eligibility Approval (Remote)** | I | I | I | R | **A** | I |
| **Corporate Device Issuance & Asset Mgt** | I | I | **A/R** | I | C | I |
| **BYOD Device Enrollment (Intune)** | I | C | **A/R** | C | I | I |
| **Security Posture Verification (Pre-Connect)** | I | **A** | R | I | I | I |
| **Data Classification & Handling (End-User)** | I | C | C | **A/R** | C | I |
| **Incident Reporting (Lost Device / Breach)** | I | C | I | **A/R** | I | I |
| **VPN Gateway Availability** | I | C | **A/R** | I | I | I |
| **Remote Home Network Risk Assessment** | I | I | I | **R** | **A** | I |
| **DPIA Consultation (New Processing)** | I | C | C | I | I | **A/R** |

**Key:**
- **R:** Responsible (executes the work)
- **A:** Accountable (ultimate ownership, must sign off)
- **C:** Consulted (provides input before action)
- **I:** Informed (notified after action/decision)

### 3.2 Named Role Responsibilities

**Jennifer Walsh, Chief Human Resources Officer (SOP Owner)**
- Authorize and formally approve exceptions to this SOP related to human capital management.
- Approve the assignment of fully remote status for positions not primarily designated as field or remote.

**Chief Information Security Officer (VP, Information Security)**
- Define the technical security architecture for remote access and mobile device management.
- Investigate and authorize deviations from technical baseline controls.
- Authorize the use of personal laptops (non-Intune) for VDI-only thin-client access under defined technical constraints.

**VP, IT Operations**
- Provision and de-provision corporate laptops, ensuring CrowdStrike Falcon EDR and Microsoft Intune enrollment prior to hand-off.
- Monitor and enforce the health of the VPN infrastructure and VDI farms, maintaining a 99.9% uptime SLA for critical gateways.
- Manage the BYOD mobile device enrollment lifecycle and enforce compliance policies.

**Employee / Contractor**
- Maintain the physical security of Meridian-issued equipment and any device used to process Meridian data.
- Immediately report loss, theft, or unauthorized access of Meridian equipment or data to the Meridian Security Operations Center (SOC) via `soc@meridianhealth.com` (24/7).
- Complete the mandatory Annual Information Security and Privacy Awareness Training within 30 days of hire and annually thereafter, as tracked in the Workday Learning Management System.

**Data Protection Officer (Meridian Europe Ltd.)**
- Provide advisory oversight on matters related to GDPR Article 39.
- Maintain the Record of Processing Activities (RoPA) for remote data collection tools.

## 4. Policy Statements

### 4.1 Access Authorization
Access to Meridian’s Clinical AI Platform and any associated ePHI or Personal Data from a remote location is a privilege, not a right. Access is granted based on a defined business need, verification of identity through strong authentication, and validation of device security posture at the point of access and continuously during the session.

### 4.2 Zero Trust Architecture
Meridian operates a Zero Trust security model for remote access. No traffic is inherently trusted. All access attempts from corporate-managed or BYOD endpoints are subject to real-time identity verification, device compliance checks, and behavioral analytics before and during the session. Access is explicitly restricted by the principle of least privilege, scoped by user identity and data sensitivity classification.

### 4.3 Data Residency and Locality
Remote workers must not physically relocate, on a permanent or extended interim basis, to countries outside of their approved employment jurisdiction without a formal security and privacy review. Any relocation requires a 60-day advance written request to HR and the Chief InfoSec Officer to assess cross-border data transfer implications.

### 4.4 Right to Audit and Remote Wipe
Meridian maintains the unconditional right to monitor, access, and audit Meridian information stored on or transmitted through Meridian systems and BYOD corporate profiles. Upon termination of employment or a reported security incident, Meridian retains the right to execute a remote, selective wipe of the Meridian corporate container on the personal device via Microsoft Intune.

## 5. Detailed Procedures

### 5.1 Remote Work Eligibility and Onboarding

**Procedure: Initial Remote Work Request**
1. The requesting employee completes the *Meridian Remote Work and Equipment Request Form* (Form ID: RWF-001) within ServiceNow HR Service Delivery.
2. The employee’s Direct Manager evaluates the request based on role suitability, team interaction needs, and performance history. The Manager is responsible for determining if the role is eligible for hybrid or fully remote work.
3. The Manager approves or denies the request within the ServiceNow workflow. If approved, HR Operations performs a jurisdictional compliance check (e.g., employment law, payroll tax nexus).
4. For first-time remote workers or new hires designated as remote, the ServiceNow workflow automatically generates a hardware provisioning ticket to IT Operations.

**Procedure: Corporate Laptop Issuance (US, Canada, UK)**
1. IT Operations receives the approved hardware ticket. A standard laptop build (macOS Ventura or Windows 11 Enterprise) is deployed via JAMF Pro or Windows Autopilot.
2. The following baseline software and agents are included in the image:
    - CrowdStrike Falcon EDR (pre-installed, tamper-proof)
    - Microsoft Intune Company Portal (enrollment enforced at OOBE)
    - Palo Alto GlobalProtect VPN Client (pre-configured with portal address `vpn.meridianhealth.com`)
    - Okta Verify MFA agent
    - Splunk Universal Forwarder
3. IT Operations tags the physical device asset in ServiceNow Asset Management and ships the device to the employee's recorded home address via a tracked, signature-required courier.
4. Upon receipt, the employee powers on the device. The Out-of-Box Experience (OOBE) forces authentication against Meridian's Azure AD tenant. The Intune Company Portal automatically enrolls the device, pushing configuration profiles for disk encryption (FileVault/BitLocker), screen lock (10-minute inactivity timeout), and password complexity.

### 5.2 Bring Your Own Device (BYOD) Enrollment

This procedure applies strictly to personally owned mobile phones and tablets. Personal laptops/desktops are **not** permitted for direct native application work with sensitive data; they must use the VDI thin-client method described in Section 5.3.

**Procedure: Mobile Device Enrollment**
1. The employee installs the **Microsoft Intune Company Portal** app from the Apple App Store or Google Play Store.
2. The employee signs into the Company Portal using their Meridian corporate credentials (`user@meridianhealth.com`) and Okta Verify MFA challenge.
3. The employee follows the guided enrollment, which triggers enrollment into the Mobile Device Management (MDM) platform.
4. The employee must accept the Meridian Terms of Use, which explicitly state management boundaries.
5. Upon successful enrollment, the following app-based protection policies are pushed:
    - **Microsoft Edge for iOS/Android:** Automatically configured to route corporate traffic through the Meridian GlobalProtect proxy and block screenshots within the work context.
    - **Microsoft Outlook for iOS/Android:** Containerized corporate email. Prevents copying data to personal apps.
    - **Microsoft OneDrive & Teams:** Containerized access. Data is encrypted-at-rest within the corporate container.

**Enrollment Validation:**
The Intune compliance engine automatically checks the device posture. The enrollment is not successful, and corporate apps will refuse to launch until:
- The device OS version is not jailbroken (iOS) or rooted (Android).
- The device encryption is active.
- A device PIN/passcode of minimum 6 digits is set.

### 5.3 Non-Managed Personal Computer Access (Thin-Client / VDI Only)

IT Operations recognizes that some contractors or temporary staff may use non-Meridian issued computers. This procedure defines the highly restrictive controls for this path.

1.  **Approval:** The contractor's Meridian sponsor submits an exception request through ServiceNow IT Service Catalog, "Request: VDI-only Access". This must be approved by the VP of IT Operations.
2.  **Access Flow:**
    - The user opens a hardened, supported web browser (latest versions of Google Chrome or Microsoft Edge on Windows/macOS).
    - The user navigates to the VMware Horizon HTML5 web client URL.
    - Authentication enforces Okta MFA with device posture checks via the Okta browser plugin. The device is checked for the presence of specific client certificates if available, but primarily the connection is restricted to user authentication.
    - **Clipboard Redirection:** Disabled (cut/paste between local and virtual desktop is blocked).
    - **Drive Redirection:** Blocked.
    - **Printing:** Restricted to a single, managed virtual print driver that outputs PDF to the corporate network shared drive. Local printing is disabled.
    - **Watermarking:** The session overlay includes a visible, semi-transparent, persistent user identifier and timestamp watermark on the virtual desktop to deter screen photography of ePHI.

### 5.4 Secure Connectivity and VPN Requirements

**Procedure: Establishing a Secure Connection**
1. The employee connects their Meridian-managed device to a secure wireless network (home or public). The connection to the Meridian enterprise is only permitted through the pre-installed Palo Alto GlobalProtect client.
2. The employee initiates the GlobalProtect VPN connection, authenticating with their Meridian credentials and an Okta Verify push MFA challenge.
3. **Security Posture Assessment:** Before the VPN tunnel is fully established, the GlobalProtect client performs a Host Information Profile (HIP) check coordinated with CrowdStrike Falcon and Intune. The connection is blocked if:
    - CrowdStrike Falcon is not running or is in a reduced-functionality mode.
    - The operating system is not within the approved patch-management window (critical patches must be installed within 7 days of release, per SOP-IS-004).
    - The firewall is disabled on the endpoint.
    - The device's hard drive is not encrypted.
4. Upon passing the posture assessment, the encrypted IPsec tunnel is established. All outbound traffic from the device is routed through the Meridian data center (full tunnel, no-split), enforcing corporate web filtering via Zscaler Internet Access and egress firewall rules.

### 5.5 Data Handling and Classification for Remote Work

**Physical Handling of Data:**
- The remote work environment is considered a "secured micro-perimeter." The employee must prevent unauthorized visual access ("shoulder surfing") to Meridian data on screens. Privacy filters must be used on laptops when working in public locations like airport lounges or cafes, as mandated by SOP-IS-001.
- All physical documents containing Meridian "Confidential" data or ePHI must be stored in a locked desk drawer or filing cabinet within the employee's home. Documents must never be left unattended in open view.
- Upon disposal, physical documents with sensitive data must be cross-shredded to a particle size not exceeding 1/2-inch by 1/2-inch using a P-4 rated micro-cut shredder purchased by the employee (a one-time stipend for this equipment is provided).

**Digital Data Handling:**
- ePHI and GDPR "Special Categories of Personal Data" must never be stored on the local endpoint hard drive. All processing must occur within approved, server-side environments:
    - **Product Suite Workstation:** VMware Horizon VDI session.
    - **Collaboration:** Microsoft Teams and SharePoint Online in designated secure sites.
    - **AI Model Interaction:** Web-interface to the Meridian Clinical AI Platform hosted in AWS PrivateLink infrastructure.
- Use of unapproved, consumer-grade file-sharing services (e.g., personal Dropbox, personal Google Drive, WeTransfer) to transmit any Meridian business data is a violation of this SOP and SOP-IS-002 (Data Loss Prevention).

### 5.6 Remote Work Environment Security

Every employee designated as fully remote must complete the *Meridian Home Network and Workspace Self-Assessment Checklist* (Form ID: RWF-002) annually, submitted to their Manager.
Key elements of the checklist include:

| Control Area | Minimum Requirement |
| :--- | :--- |
| **Access Point** | Home Wi-Fi must use WPA3 or WPA2-AES encryption. WEP, WPA, or open networks are prohibited for business traffic. Default SSID and admin credentials for the router must be changed. |
| **Firmware** | Home router firmware must be kept reasonably up-to-date, following vendor support patches. |
| **Screen Privacy** | Visual barriers or privacy screens must prevent unauthorized viewing from windows, doors, or family members for ePHI processing. |
| **Voice Assistants** | Always-listening smart speakers (e.g., Amazon Alexa, Google Home) must be physically muted or located outside of the dedicated workspace during sensitive business calls, especially those involving ePHI. |

## 6. Controls and Safeguards

### 6.1 Technical Controls

| Control ID | Control Category | Control Description (SOC 2 - CC Series Alignment) | Implementation Tool |
| :--- | :--- | :--- | :--- |
| **TEL-RW-01** | Endpoint Protection (CC6.6) | Next-gen antivirus and EDR deployed on all endpoints, providing real-time IOC detection, threat hunting, and containment. | CrowdStrike Falcon |
| **TEL-RW-02** | Device Encryption (CC6.1) | Full-disk AES-256 encryption enforced on all corporate laptops and container encryption on BYOD profiles. | FileVault2, BitLocker, Intune MDM |
| **TEL-RW-03** | Network Segmentation (CC6.6) | Remote user traffic automatically placed in a restricted VLAN. Access to Tier-0 assets and clinical databases occurs only through jump host or VDI proxy, never directly from the endpoint. | Palo Alto Firewalls, VDI Gateway |
| **TEL-RW-04** | Idle Session Lock (CC6.1) | Interactive user sessions must lock after a maximum of 15 minutes of inactivity, requiring re-authentication with MFA. Screen savers with password protection activate automatically. | Group Policy Object, MDM Profile |
| **TEL-RW-05** | Web Content Filtering (CC6.6) | Full-tunnel VPN traffic routed through Zscaler for URL filtering, blocking categories: `hacking`, `peer-to-peer`, `phishing`, and `newly-registered-domains`. | Zscaler Internet Access, GlobalProtect |

### 6.2 Administrative Controls

| Control ID | Control Category | Control Description (HIPAA, GDPR alignment) | Owner | Frequency |
| :--- | :--- | :--- | :--- | :--- |
| **TEL-RW-A01** | Workforce Security (HIPAA §164.308(a)(3)(i)) | Annual Information Security and Privacy Training, including a specific module on "Securing Telehealth and Remote Work". Completion tracked in Workday. | HR / InfoSec | Annual |
| **TEL-RW-A02** | Information Access Mgmt (HIPAA §164.308(a)(4)(i)) | Quarterly Access Recertification (QAR). Managers must verify that direct reports' remote and general system access remains appropriate for their role. Access for terminated employees is revoked within <1 hour. | Direct Manager, IAM Team | Quarterly |
| **TEL-RW-A03** | Device and Media Controls (HIPAA §164.310(d)(1)) | Device media reuse and disposal. All corporate media leaving a remote location for disposal must be sanitized according to NIST SP 800-88 Rev. 1 via a Meridian IT logistics chain. | IT Operations | As needed |
| **TEL-RW-A04** | Security Incident Response (HIPAA §164.308(a)(6)(i)) | Mandatory incident response process. Remote workers must report suspected or actual security incidents to the SOC within 1 hour of discovery via phone and email. | Employee, SOC | As needed |
| **TEL-RW-A05** | Risk Assessment (HIPAA §164.308(a)(1)(ii)(A)) | Annual enterprise risk assessment that specifically includes "Remote Work and Telehealth Endpoint Security" as a defined risk domain. | Chief InfoSec Officer | Annual |

### 6.3 GDPR-Specific Safeguards (Pseudonymisation and Minimization)

To reduce risk to data subjects, the default configuration for telehealth data access is pseudonymised. The Clinical AI Platform web interface accessed remotely strips direct identifiers (Name, MRN) and displays them only via a secondary, explicit click-to-reveal action, which is fully logged. This provides appropriate protection for data viewed in potentially uncontrolled physical environments.

## 7. Monitoring, Metrics, and Reporting

### 7.1 Key Performance Indicators (KPIs) and Key Risk Indicators (KRIs)

Metrics are reported via dashboards in Splunk and ServiceNow, displayed in the Security Operations Center and the monthly Governance, Risk, and Compliance (GRC) council meeting co-chaired by the Chief InfoSec Officer and the Chief HR Officer.

| Metric / KPI | Target / SLA | Data Source | Responsible Reporter |
| :--- | :--- | :--- | :--- |
| **BYOD Device Compliance Rate** | > 98% | Microsoft Intune Dashboard | VP, IT Operations |
| **Managed Laptop Patch Lag** | < 7 days for critical vulns | CrowdStrike / JAMF Pro | VP, IT Operations |
| **VPN Posture Assessment Failures** (trend analysis) | Reduce month-over-month; investigate spikes | Palo Alto GlobalProtect logs | CISO |
| **User Authentication Anomalies** (UEBA alerts) | < 5 "Impossible Travel" alerts/week (not false-positive) | Splunk UEBA | SOC Manager |
| **Annual Privacy Training Completion** | 100% completion by deadline | Workday LMS | Chief HR Officer |
| **Incident Response Time (from report)** | Acknowledged by SOC within 15 min | ServiceNow ITSM | SOC Manager |

### 7.2 Reporting Cadence
- **Monthly:** Automated IT compliance report on patch levels and device encryption posture distributed to VP of IT Operations.
- **Quarterly:** SOC Manager reports to the CISO on remote-access security events, blocked intrusion attempts, and VPN utilization trends.
- **Annually:** Chief HR Officer and CISO present a unified "Remote Work State of Compliance" report to the CEO and the Board’s Audit and Risk Committee, summarizing training completion, exception counts, and risk posture updates.

## 8. Exception Handling and Escalation

### 8.1 Standard Exception Process
Deviations from the technical controls defined in this SOP (e.g., requirement to use a specific VPN client due to a vendor limitation) require a formal, temporary exception.
1.  **Request:** The employee initiates a ServiceNow "Policy Exception Request" and attaches a business justification and a compensating control proposal (e.g., "I cannot use the GlobalProtect client; I will instead use the dedicated IP-locked site-to-site VPN tunnel from my secured home office").
2.  **Technical Review:** The Chief InfoSec Officer reviews the compensating controls and determines if the residual risk is tolerable.
3.  **Authorization:** Exceptions are approved on a matrix basis:
    - **Minor Exception (< 30 days, non-ePHI data):** VP of IT Operations.
    - **Major Exception (> 30 days or involving ePHI):** Chief InfoSec Officer and Chief Data Protection Officer joint signature.
4.  **Documentation:** Approved exceptions are tracked in the GRC module of ServiceNow with an automatic expiration trigger. No exception is permanent.

### 8.2 Escalation for Urgent Security Matters
If an employee suspects an active intrusion, ransomware event, or lost/stolen device, the standard ServiceNow path is bypassed. The employee must execute the "Phone Tree" escalation path:
1.  Call the Meridian SOC at the internal emergency hotline.
2.  If SOC is unavailable, directly page the on-call Information Security Officer via PagerDuty.

## 9. Training Requirements

### 9.1 Mandatory Training Curriculum
All personnel within scope are assigned the following mandatory training modules within the Workday Learning Management System (LMS).

| Course ID | Training Title | Initial Assignment (New Hire) | Annual Refresher | Target Audience |
| :--- | :--- | :--- | :--- | :--- |
| **SEC-RW-101** | Securing Your Remote Workspace: Home Network and Physical Security | Within 30 days of hire | Mandatory, Annual | All Remote Workers |
| **SEC-BYD-201** | BYOD and Mobile Device Security Awareness | Within 30 days of enrollment | Mandatory, Annual | All BYOD Users |
| **PRI-GDP-301** | Privacy Essentials: Handling Data Remotely (GDPR and HIPAA focus) | Within 30 days of hire | Mandatory, Annual | All Personnel |
| **TELE-402** | Telehealth and Clinical AI Platform Compliance | Before Clinical AI Access Grant | Mandatory, Semi-Annual | Clinical Users, AI Developers |

### 9.2 Training Tracking and Remediation
- The Chief HR Officer, Jennifer Walsh, receives a monthly completion report from the Workday LMS.
- Managers are notified of non-compliance for their direct reports 14 days before the training deadline.
- If an employee fails to complete annual training by the deadline, their VPN and application access (Okta group membership for `VPN-Users`, `O365-Users`) is automatically suspended until training completion is recorded, per the enforcement workflow in Okta Workflows.

## 10. Related Policies and References

### 10.1 Internal Meridian SOPs

| SOP ID | Document Title | Relationship |
| :--- | :--- | :--- |
| **SOP-IS-001** | Information Classification and Labeling | Defines data sensitivity levels and corresponding handling requirements. |
| **SOP-IS-002** | Data Loss Prevention (DLP) and Endpoint Monitoring | Controls for preventing unauthorized exfiltration of data from endpoints, including USB blocking. |
| **SOP-IS-004** | Vulnerability and Patch Management | Specifies mandatory SLAs for applying security patches on endpoints referenced in this document. |
| **SOP-IS-007** | Incident Response and Breach Notification | Detailed incident handling lifecycle. |
| **SOP-IS-009** | Identity and Access Management (IAM) | Defines Okta authentication policies, MFA requirements, and access reviews. |
| **SOP-PRI-001** | Protected Data Governance and Minimization | The enterprise standard for de-identification and pseudonymisation strategies. |
| **SOP-VND-002** | Third-Party Contractor Access Management | Defines the lifecycle for granting and revoking access to external parties referenced in this document. |

### 10.2 External Standards and Regulations

| Reference | Title / Section |
| :--- | :--- |
| **HIPAA** | 45 CFR Part 164, Subparts A, C, and D (Security Rule, Privacy Rule, Breach Notification Rule) |
| **GDPR (EU) 2016/679** | Article 5 (Principles), Article 32 (Security of processing), Article 35 (DPIA) |
| **SOC 2 (AICPA)** | Trust Services Criteria CC6.1 (Logical and Physical Access Controls), CC6.6 (External Threats), CC7.1 (Monitoring of Controls) |
| **NIST SP 800-53 Rev. 5** | Control families AC (Access Control), PE (Physical and Environmental Protection), IR (Incident Response) |
| **ISO 27001:2013** | Annex A.6.2 (Mobile devices and teleworking) |

## 11. Revision History

| Version | Date | Author | Nature of Revision |
| :--- | :--- | :--- | :--- |
| 1.0 | 2021-04-04 | A. Gupta, IT Ops | Initial policy creation. Laptop and VPN focus only. |
| 2.0 | 2022-09-20 | J. Walsh, HR | Major rewrite, adding BYOD program, VDI access, and Workday LMS integration. Formal alignment with NIST 800-53. |
| 2.1 | 2023-06-14 | L. Chen, InfoSec | Added detailed endpoint posture assessments (HIP check), CrowdStrike Falcon EDR controls, and ZTNA architecture. Updated device issuance to Autopilot. |
| 2.2 | 2024-05-16 | J. Walsh, HR / CISO | Annual review cycle. Added physical home network self-assessment form (RWF-002), cross-cut shredder requirement, and strengthened MFA for VDI. Updated RACI matrix to clarify Data Protection Officer consult role. Aligned with new Meridian UK entity structure. |
| 2.2 Rev. 1 | 2025-09-24 | M. Dubois, Compliance | Minor revision to reflect new CE marking status under EU MDR, added reference to product suite-specific clinical AI platform controls in Section 10. No change to core procedural steps. |