# Regulation Source Texts

Reference texts for Sentinel's target regulations. Used for grounding the compliance auditor's assessments.

## SOC 2

| File | Description | Source |
|------|-------------|--------|
| `soc2_trust_services_criteria_2017_revised_2022.pdf` | 2017 Trust Services Criteria with Revised Points of Focus (2022) | AICPA |
| `soc2_description_criteria_2018_revised_2022.pdf` | 2018 SOC 2 Description Criteria (revised 2022) | AICPA |

## HIPAA

| File | Description | Source |
|------|-------------|--------|
| `hipaa_45cfr_part160_general_admin.xml` | 45 CFR Part 160 — General Administrative Requirements (XML) | eCFR API |
| `hipaa_45cfr_part160_general_admin.txt` | Same, converted to plain text | eCFR API → convert script |
| `hipaa_45cfr_part162_admin_requirements.xml` | 45 CFR Part 162 — Administrative Requirements (XML) | eCFR API |
| `hipaa_45cfr_part162_admin_requirements.txt` | Same, converted to plain text | eCFR API → convert script |
| `hipaa_45cfr_part164_security_privacy.xml` | 45 CFR Part 164 — Security and Privacy (XML) | eCFR API |
| `hipaa_45cfr_part164_security_privacy.txt` | Same, converted to plain text — **this is the main HIPAA Security Rule** | eCFR API → convert script |
| `hipaa_ecfr_45cfr_parts_160_162_164.pdf` | Combined eCFR printout of all three parts | eCFR |
| `hipaa_public_law_104_191_1996.pdf` | Original HIPAA statute (Public Law 104-191) | HHS ASPE |

## GDPR

| File | Description | Source |
|------|-------------|--------|
| `gdpr_regulation_eu_2016_679.pdf` | Regulation (EU) 2016/679 — official EUR-Lex text | EUR-Lex |
| `gdpr_full_text.md` | Navigable article-by-article text (key chapters) | gdpr-info.eu |

## EU AI Act

| File | Description | Source |
|------|-------------|--------|
| `eu_ai_act_regulation_eu_2024_1689.pdf` | Regulation (EU) 2024/1689 — official EUR-Lex text | EUR-Lex |
| `eu_ai_act_full_text.md` | Navigable article-by-article text (key chapters) | artificialintelligenceact.eu |

Note: The AI Act entered into force 1 Aug 2024, fully applicable 2 Aug 2026. An "AI omnibus" simplification package had political agreement on 7 May 2026 — check the Commission page for latest amendments.

## NIST AI RMF

| File | Description | Source |
|------|-------------|--------|
| `nist_ai_rmf_100_1.pdf` | NIST AI 100-1: AI Risk Management Framework (Jan 2023) | NIST |
| `nist_ai_600_1_genai_profile.pdf` | NIST AI 600-1: Generative AI Profile | NIST |

## SR 11-7 (Model Risk Management)

| File | Description | Source |
|------|-------------|--------|
| *Manual download required* | OCC Bulletin 2011-12a: Supervisory Guidance on Model Risk Management | OCC |

The OCC site is behind Cloudflare bot protection. Download manually from:
https://www.occ.treas.gov/news-issuances/bulletins/2011/bulletin-2011-12a.pdf

Save as `sr_11_7_occ_model_risk_management.pdf`.

Note: OCC issued revised Model Risk Management guidance in 2026 (Bulletin 2026-13) — consider downloading that as well from https://www.occ.treas.gov/news-issuances/bulletins/2026/bulletin-2026-13.html.

## California AI Laws

| File | Description | Source |
|------|-------------|--------|
| `california_sb53_frontier_ai_transparency.txt` | SB 53: Transparency in Frontier AI Act (signed Sep 29, 2025) | CA leginfo |
| `california_sb942_ai_transparency_act.txt` | SB 942: California AI Transparency Act (signed Sep 19, 2024) | CA leginfo |
| `california_ab853_ai_transparency_amendments.txt` | AB 853: AI Transparency Act Amendments (signed Sep 16, 2025) | CA leginfo |

SB 1047 (Safe and Secure Innovation for Frontier AI Models Act) was vetoed by Governor Newsom in Sep 2024. SB 53 is its successor — a lighter-touch transparency requirement for frontier AI developers (>10^26 FLOPS, >$500M revenue).

## Utilities

| File | Description |
|------|-------------|
| `../../scripts/convert_ecfr_xml_to_txt.py` | Converts eCFR XML to readable plain text |
