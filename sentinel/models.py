from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class ComplianceLevel(str, Enum):
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    GAP = "gap"


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class RegulationClause(BaseModel):
    clause_id: str
    regulation: str
    title: str
    description: str
    reference: str


class SOPChunk(BaseModel):
    sop_id: str
    title: str
    business_unit: str
    chunk_text: str
    section: str = ""
    page_estimate: int = 0
    score: float = 0.0


class AuditFinding(BaseModel):
    clause_id: str
    clause_title: str
    regulation: str
    sop_id: str
    sop_title: str
    business_unit: str
    compliance_level: ComplianceLevel
    severity: Severity
    evidence_quote: str = ""
    gap_description: str = ""
    remediation: str = ""
    reasoning: str = ""


class AuditMetrics(BaseModel):
    total_clauses: int = 0
    total_sops_audited: int = 0
    total_findings: int = 0
    compliant_count: int = 0
    partial_count: int = 0
    gap_count: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    total_tokens: int = 0
    total_retrieval_steps: int = 0
    avg_latency_per_cell: float = 0.0
    total_latency: float = 0.0
    total_cost: float = 0.0


SOC2_CLAUSES = [
    RegulationClause(
        clause_id="CC1",
        regulation="SOC 2",
        title="Control Environment",
        description="The entity demonstrates a commitment to integrity and ethical values, exercises oversight responsibility, establishes structure/authority/responsibility, demonstrates commitment to competence, and enforces accountability.",
        reference="SOC 2 Trust Services Criteria — CC1.1 through CC1.5",
    ),
    RegulationClause(
        clause_id="CC2",
        regulation="SOC 2",
        title="Communication and Information",
        description="The entity obtains or generates relevant quality information, internally communicates information including objectives and responsibilities, and communicates with external parties.",
        reference="SOC 2 Trust Services Criteria — CC2.1 through CC2.3",
    ),
    RegulationClause(
        clause_id="CC3",
        regulation="SOC 2",
        title="Risk Assessment",
        description="The entity specifies suitable objectives, identifies and analyzes risk, assesses fraud risk, and identifies and analyzes significant change.",
        reference="SOC 2 Trust Services Criteria — CC3.1 through CC3.4",
    ),
    RegulationClause(
        clause_id="CC4",
        regulation="SOC 2",
        title="Monitoring Activities",
        description="The entity selects, develops, and performs ongoing and/or separate evaluations, and evaluates and communicates deficiencies.",
        reference="SOC 2 Trust Services Criteria — CC4.1 through CC4.2",
    ),
    RegulationClause(
        clause_id="CC5",
        regulation="SOC 2",
        title="Control Activities",
        description="The entity selects and develops control activities, deploys through policies and procedures, and uses relevant technology.",
        reference="SOC 2 Trust Services Criteria — CC5.1 through CC5.3",
    ),
    RegulationClause(
        clause_id="CC6",
        regulation="SOC 2",
        title="Logical and Physical Access Controls",
        description="The entity implements logical access security, manages credentials, restricts access, manages network security, manages data on endpoints, and implements physical access controls.",
        reference="SOC 2 Trust Services Criteria — CC6.1 through CC6.8",
    ),
    RegulationClause(
        clause_id="CC7",
        regulation="SOC 2",
        title="System Operations",
        description="The entity manages system operations, implements processing-integrity policies, manages data-recovery, and tests system resilience.",
        reference="SOC 2 Trust Services Criteria — CC7.1 through CC7.5",
    ),
    RegulationClause(
        clause_id="CC8",
        regulation="SOC 2",
        title="Change Management",
        description="The entity manages changes to infrastructure, data, software, and procedures.",
        reference="SOC 2 Trust Services Criteria — CC8.1",
    ),
    RegulationClause(
        clause_id="CC9",
        regulation="SOC 2",
        title="Risk Mitigation",
        description="The entity identifies, selects, and develops risk-mitigation activities and manages vendor and business partner risks.",
        reference="SOC 2 Trust Services Criteria — CC9.1 through CC9.2",
    ),
]

HIPAA_CLAUSES = [
    RegulationClause(
        clause_id="HIPAA-ADM-1",
        regulation="HIPAA Security Rule",
        title="Security Management Process",
        description="Implement policies and procedures to prevent, detect, contain, and correct security violations. Includes risk analysis and risk management.",
        reference="45 CFR § 164.308(a)(1) — Administrative Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-ADM-2",
        regulation="HIPAA Security Rule",
        title="Assigned Security Responsibility",
        description="Identify the security official responsible for developing and implementing security policies and procedures.",
        reference="45 CFR § 164.308(a)(2) — Administrative Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-ADM-3",
        regulation="HIPAA Security Rule",
        title="Workforce Security",
        description="Implement policies and procedures to ensure all workforce members have appropriate access to ePHI and prevent unauthorized access.",
        reference="45 CFR § 164.308(a)(3) — Administrative Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-ADM-4",
        regulation="HIPAA Security Rule",
        title="Information Access Management",
        description="Implement policies and procedures for authorizing access to ePHI consistent with the Privacy Rule.",
        reference="45 CFR § 164.308(a)(4) — Administrative Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-ADM-5",
        regulation="HIPAA Security Rule",
        title="Security Awareness and Training",
        description="Implement a security awareness and training program for all workforce members including management.",
        reference="45 CFR § 164.308(a)(5) — Administrative Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-ADM-6",
        regulation="HIPAA Security Rule",
        title="Security Incident Procedures",
        description="Implement policies and procedures to address security incidents, including response and reporting.",
        reference="45 CFR § 164.308(a)(6) — Administrative Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-ADM-7",
        regulation="HIPAA Security Rule",
        title="Contingency Plan",
        description="Establish policies and procedures for responding to an emergency that damages systems containing ePHI.",
        reference="45 CFR § 164.308(a)(7) — Administrative Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-ADM-8",
        regulation="HIPAA Security Rule",
        title="Evaluation",
        description="Perform periodic technical and nontechnical evaluations to establish the extent to which security policies meet Security Rule requirements.",
        reference="45 CFR § 164.308(a)(8) — Administrative Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-PHY-1",
        regulation="HIPAA Security Rule",
        title="Facility Access Controls",
        description="Implement policies and procedures to limit physical access to electronic information systems while ensuring properly authorized access.",
        reference="45 CFR § 164.310(a) — Physical Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-PHY-2",
        regulation="HIPAA Security Rule",
        title="Workstation Use and Security",
        description="Implement policies for proper workstation use and physical safeguards for all workstations that access ePHI.",
        reference="45 CFR § 164.310(b)-(c) — Physical Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-PHY-3",
        regulation="HIPAA Security Rule",
        title="Device and Media Controls",
        description="Implement policies governing the receipt and removal of hardware and electronic media containing ePHI.",
        reference="45 CFR § 164.310(d) — Physical Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-TECH-1",
        regulation="HIPAA Security Rule",
        title="Access Control",
        description="Implement technical policies and procedures for electronic information systems to allow access only to authorized persons or software programs.",
        reference="45 CFR § 164.312(a) — Technical Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-TECH-2",
        regulation="HIPAA Security Rule",
        title="Audit Controls",
        description="Implement hardware, software, and/or procedural mechanisms to record and examine activity in systems containing ePHI.",
        reference="45 CFR § 164.312(b) — Technical Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-TECH-3",
        regulation="HIPAA Security Rule",
        title="Integrity Controls",
        description="Implement policies and procedures to protect ePHI from improper alteration or destruction, including electronic mechanisms to corroborate that ePHI has not been altered or destroyed.",
        reference="45 CFR § 164.312(c) — Technical Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-TECH-4",
        regulation="HIPAA Security Rule",
        title="Person or Entity Authentication",
        description="Implement procedures to verify that a person or entity seeking access to ePHI is the one claimed.",
        reference="45 CFR § 164.312(d) — Technical Safeguards",
    ),
    RegulationClause(
        clause_id="HIPAA-TECH-5",
        regulation="HIPAA Security Rule",
        title="Transmission Security",
        description="Implement technical security measures to guard against unauthorized access to ePHI being transmitted over an electronic communications network.",
        reference="45 CFR § 164.312(e) — Technical Safeguards",
    ),
]

ALL_CLAUSES = SOC2_CLAUSES + HIPAA_CLAUSES

RELEVANT_BUSINESS_UNITS = [
    "05_information_security",
    "03_data_governance_privacy",
    "06_it_operations",
    "08_legal_compliance",
]
