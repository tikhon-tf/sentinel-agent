# Regulation Source Texts

Reference texts for Sentinel's target regulations. Used for grounding the compliance auditor's assessments.

## SOC 2

| File | Description | Source |
|------|-------------|--------|
| `soc2_trust_services_criteria_2017_revised_2022.pdf` | 2017 Trust Services Criteria with Revised Points of Focus (2022) | AICPA |
| `soc2_description_criteria_2018_revised_2022.pdf` | 2018 SOC 2 Description Criteria (revised 2022) | AICPA |

## HIPAA

### Current (2025)

| File | Description | Source |
|------|-------------|--------|
| `hipaa_45cfr_part160_general_admin.xml` | 45 CFR Part 160 — General Administrative Requirements (XML) | eCFR API |
| `hipaa_45cfr_part160_general_admin.txt` | Same, converted to plain text | eCFR API → convert script |
| `hipaa_45cfr_part162_admin_requirements.xml` | 45 CFR Part 162 — Administrative Requirements (XML) | eCFR API |
| `hipaa_45cfr_part162_admin_requirements.txt` | Same, converted to plain text | eCFR API → convert script |
| `hipaa_45cfr_part164_security_privacy.xml` | 45 CFR Part 164 — Security and Privacy (XML) | eCFR API |
| `hipaa_45cfr_part164_security_privacy.txt` | Same, converted to plain text — **main HIPAA Security Rule** | eCFR API → convert script |
| `hipaa_ecfr_45cfr_parts_160_162_164.pdf` | Combined eCFR printout of all three parts | eCFR |
| `hipaa_public_law_104_191_1996.pdf` | Original HIPAA statute (Public Law 104-191) | HHS ASPE |

### Historical Editions

| File | Description | Date | Source |
|------|-------------|------|--------|
| `hipaa_45cfr_part164_2017.xml` / `.txt` | Part 164 as of Jan 2017 (earliest in eCFR, post-Omnibus Rule) | 2017-01-01 | eCFR API |
| `hipaa_45cfr_part164_2020.xml` / `.txt` | Part 164 as of Jan 2020 (pre-pandemic baseline) | 2020-01-01 | eCFR API |
| `hipaa_45cfr_part164_2024.xml` / `.txt` | Part 164 as of Jan 2024 (before 2025 cybersecurity update) | 2024-01-01 | eCFR API |
| `hipaa_45cfr_part160_2020.xml` / `.txt` | Part 160 as of Jan 2020 | 2020-01-01 | eCFR API |
| `hipaa_45cfr_part162_2020.xml` / `.txt` | Part 162 as of Jan 2020 | 2020-01-01 | eCFR API |

## GDPR

| File | Description | Source |
|------|-------------|--------|
| `gdpr_regulation_eu_2016_679.pdf` | Regulation (EU) 2016/679 — official EUR-Lex text | EUR-Lex |
| `gdpr_full_text.md` | Navigable article-by-article text (key chapters) | gdpr-info.eu |

GDPR has not been substantively amended since adoption (April 2016, effective May 2018).

## EU AI Act

| File | Description | Source |
|------|-------------|--------|
| `eu_ai_act_regulation_eu_2024_1689.pdf` | Regulation (EU) 2024/1689 — official final text | EUR-Lex |
| `eu_ai_act_full_text.md` | Navigable article-by-article text (key chapters) | artificialintelligenceact.eu |
| `eu_ai_act_2021_commission_proposal.pdf` | COM/2021/206 — original Commission proposal (108 pages) | EUR-Lex |

The AI Act entered into force 1 Aug 2024, fully applicable 2 Aug 2026. An "AI omnibus" simplification package had political agreement on 7 May 2026.

## NIST AI RMF

| File | Description | Source |
|------|-------------|--------|
| `nist_ai_rmf_100_1.pdf` | NIST AI 100-1: AI Risk Management Framework (final, Jan 2023) | NIST |
| `nist_ai_600_1_genai_profile.pdf` | NIST AI 600-1: Generative AI Profile (Jul 2024) | NIST |
| `nist_ai_rmf_100_1_draft1_2022.pdf` | NIST AI 100-1: 1st public draft (Mar 2022) | NIST |
| `nist_ai_rmf_100_1_draft2_2022.pdf` | NIST AI 100-1: 2nd public draft (Aug 2022) | NIST |

## SR 11-7 / Model Risk Management

| File | Description | Source |
|------|-------------|--------|
| `sr_11_7_occ_model_risk_management.pdf` | OCC Bulletin 2011-12a: original guidance (2011) | OCC |
| `sr_26_2_model_risk_management_2026.pdf` | Fed SR 26-2: revised interagency guidance (Apr 2026) | Federal Reserve |

SR 11-7 was rescinded April 2026 and replaced by interagency guidance (OCC 2026-13 / Fed SR 26-2 / FDIC). The revised guidance excludes generative/agentic AI from scope and applies to banks >$30B total assets.

## California AI Laws

| File | Description | Source |
|------|-------------|--------|
| `california_sb53_frontier_ai_transparency.txt` | SB 53: Transparency in Frontier AI Act (signed Sep 29, 2025) | CA leginfo |
| `california_sb942_ai_transparency_act.txt` | SB 942: California AI Transparency Act (signed Sep 19, 2024) | CA leginfo |
| `california_ab853_ai_transparency_amendments.txt` | AB 853: AI Transparency Act Amendments (signed Sep 16, 2025) | CA leginfo |

SB 1047 was vetoed Sep 2024. SB 53 is its successor — lighter-touch transparency for frontier AI developers (>10^26 FLOPS, >$500M revenue).

## Utilities

| File | Description |
|------|-------------|
| `../../scripts/convert_ecfr_xml_to_txt.py` | Converts eCFR XML to readable plain text |
| `../../scripts/fetch_gdpr_articles.py` | Fetches GDPR articles from gdpr-info.eu |
| `../../scripts/fetch_eu_ai_act_articles.py` | Fetches EU AI Act articles from artificialintelligenceact.eu |
