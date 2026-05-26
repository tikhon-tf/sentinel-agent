# Sentinel Regulations — Customer API Guide

A pre-built knowledge context covering 50 regulatory documents across 9
core compliance frameworks plus ~27 referenced standards. Query it via
HTTP from any language or runtime — no SDK or CLI install required.

This document is everything you need. It does not assume access to any
internal repository, design doc, or admin tool.

## What's in the corpus

| Group | Documents |
|---|---|
| **HIPAA** | 45 CFR Parts 160, 162, 164 (current + 2017 / 2020 / 2024 editions of Part 164) |
| **SOC 2** | 2017 Trust Services Criteria (revised 2022), 2018 Description Criteria (revised 2022) |
| **GDPR** | Regulation (EU) 2016/679, full article-by-article text |
| **EU AI Act** | Regulation (EU) 2024/1689 (current text) + 2021 Commission proposal |
| **NIST AI RMF** | AI 100-1 (final + 2 drafts), AI 600-1 GenAI Profile |
| **NIST Cybersecurity Framework** | CSF 2.0 |
| **NIST Special Publications** | SP 800-53 Rev 5, 800-88, 800-61, 800-63B, 800-207, 800-34, 800-161, 800-218, SP 1270, Privacy Framework 1.0 |
| **Model Risk Management** | SR 11-7 (2011) + SR 26-2 (2026 revised interagency guidance) |
| **California AI laws** | SB 53 (Frontier AI Transparency), SB 942 (AI Transparency Act), AB 853 (Amendments) |
| **FDA / 21 CFR** | Part 11 (electronic records), Part 807 (premarket), Part 820 (QSR), AI/ML SaMD framework, Clinical Decision Support guidance |
| **EU directives & regulations** | MDR 2017/745, SCCs 2021/914, ePrivacy 2002/58, AMLD4 2015/849, Funds Transfer 2015/847 |
| **OWASP** | Top 10 (2021), API Security Top 10 (2023) |
| **Financial laws** | BSA (31 CFR Chapter X), ECOA (Reg B, 12 CFR 1002), FCRA, PCI DSS |

Total: 50 source documents, ~21 MB of regulation text. Every answer
preserves verbatim text from the source and returns a citation back to
the originating document.

## Connection details

| Item | Value |
|---|---|
| Base URL | `https://prod.nexus.pinecone.io` |
| Auth endpoint | `POST /api/v0/auth/login` |
| Query endpoint | `POST /knowql` (note: outside `/api/v0`) |
| Project | `dbljkrx` |
| Context slug | `sentinel-regs-test` |
| Token type | JWT (HS256), expires after ~30 days |

## Prerequisites

1. **A Pinecone API key** for project `dbljkrx`. If your key is for a
   different project, you won't have access to this context — contact
   your account representative.
2. A way to make HTTPS requests. Every example below uses `curl`, but any
   HTTP client in any language works. SDK-free examples for Python,
   Node.js, and Go are at the bottom of this guide.

There is no CLI install and no library to download.

## Authentication model

Authentication is two steps:

1. Exchange your **Pinecone API key** (long-lived, treat like a password)
   for a **Nexus JWT** (short-lived, ~30 days) via `POST /api/v0/auth/login`.
2. Send the JWT as a `Authorization: Bearer <jwt>` header on every
   subsequent call.

The Pinecone key is never sent to `/knowql` directly. Cache the JWT and
re-login only when it expires (or proactively on a `401` response).

**Never log, echo, or commit either the API key or the JWT.** Treat them
both as secrets.

## Set up your shell

```sh
export NEXUS_BASE_URL="https://prod.nexus.pinecone.io"
export PINECONE_API_KEY="pcsk_..."   # your Pinecone API key (project dbljkrx)
```

## 1. Login — exchange the API key for a JWT

```sh
export NEXUS_TOKEN="$(
  curl -fsS -X POST "$NEXUS_BASE_URL/api/v0/auth/login" \
    -H 'Content-Type: application/json' \
    -d "{\"api_key\":\"$PINECONE_API_KEY\"}" \
  | jq -r '.token'
)"
export AUTH_HEADER="Authorization: Bearer $NEXUS_TOKEN"
```

Verify the login worked and confirm the project:

```sh
curl -fsS "$NEXUS_BASE_URL/api/v0/auth" -H "$AUTH_HEADER" | jq
```

Expected response:

```json
{
  "principal": "pc_...",
  "project_id": "dbljkrx",
  "project_name": "dbljkrx"
}
```

If `project_id` is anything other than `dbljkrx`, your key is for a
different project and the context won't be visible to you.

## 2. Ask a question

The query path is `POST /knowql`. Pass the context slug in `scope` (as an
array — exactly one entry today) and your question in `ask`, with
`ground: true` to get a cited answer.

```sh
curl -fsS -X POST "$NEXUS_BASE_URL/knowql" \
  -H "$AUTH_HEADER" \
  -H 'Content-Type: application/json' \
  -d '{
    "scope": ["sentinel-regs-test"],
    "ask": "Under GDPR, how quickly must a controller notify the supervisory authority of a personal data breach?",
    "ground": true
  }' | jq
```

Abridged response:

```json
{
  "id": "2de06dc3-...",
  "state": "completed",
  "ask": "Under GDPR, how quickly...",
  "ground": true,
  "output": {
    "answer": [
      {
        "requirement": "Notification of a personal data breach to the supervisory authority",
        "deadline": "The controller shall notify the personal data breach to the supervisory authority without undue delay and, where feasible, not later than 72 hours after having become aware of it [c1].",
        "exceptions_and_conditions": "Notification is not required if the personal data breach is unlikely to result in a risk to the rights and freedoms of natural persons [c1]..."
      }
    ],
    "citations": [
      {
        "file": {"name": "gdpr_full_text.md", "path": "uploads/gdpr_full_text.md"},
        "pages": [],
        "origin": "source"
      }
    ],
    "sources_used": ["gdpr_full_text.md"],
    "model": "gemini-3-flash-preview",
    "query_variants": ["Under GDPR, how quickly...", "GDPR Article 33 notification timeline", "..."]
  }
}
```

Key fields:

| Field | Meaning |
|---|---|
| `id` | Persistent query ID — fetch the same record later via `GET /knowql/queries/{id}` |
| `state` | `completed` on success; `failed` on error |
| `output.answer` | The grounded answer. Shape is dynamic — usually a structured array, sometimes a `raw` string for open-ended questions. Inline citation markers (`[c1]`, `[c2]`) reference the `citations` array |
| `output.citations` | Ordered — `[c1]` is `citations[0]`, `[c2]` is `citations[1]`, etc. Each citation names the source file |
| `output.sources_used` | Deduplicated list of source filenames consulted |
| `output.model` | LLM that produced the answer |
| `output.query_variants` | Alternative phrasings that were searched in addition to your original `ask`. Useful for understanding *why* a particular answer came back |

## 3. Constrain the answer to a JSON schema

If you're piping answers into downstream code, force a fixed shape with
`shape`. The schema follows JSON Schema (OpenAPI 3.0 subset).

```sh
curl -fsS -X POST "$NEXUS_BASE_URL/knowql" \
  -H "$AUTH_HEADER" \
  -H 'Content-Type: application/json' \
  -d '{
    "scope": ["sentinel-regs-test"],
    "ask": "What is the maximum administrative fine under GDPR Article 83 for the most serious infringements?",
    "ground": true,
    "shape": {
      "type": "object",
      "properties": {
        "regulation":             {"type": "string"},
        "citation":               {"type": "string"},
        "absolute_max_eur":       {"type": "string"},
        "percentage_of_turnover": {"type": "string"}
      },
      "required": ["regulation", "citation", "absolute_max_eur", "percentage_of_turnover"]
    }
  }' | jq '.output.answer'
```

Returns an object matching the schema:

```json
{
  "regulation": "General Data Protection Regulation (GDPR) Article 83",
  "citation": "Article 83(5) [c1]",
  "absolute_max_eur": "20,000,000 EUR",
  "percentage_of_turnover": "4% of total worldwide annual turnover of the preceding financial year"
}
```

## 4. Query history and stats

```sh
# List recent queries against this context
curl -fsS "$NEXUS_BASE_URL/knowql/queries?context_id=sentinel-regs-test&limit=20" \
  -H "$AUTH_HEADER" | jq

# Fetch a single past query by id
curl -fsS "$NEXUS_BASE_URL/knowql/queries/<query-id>" -H "$AUTH_HEADER" | jq

# Delete a query record
curl -fsS -X DELETE "$NEXUS_BASE_URL/knowql/queries/<query-id>" -H "$AUTH_HEADER"

# Per-project usage stats
curl -fsS "$NEXUS_BASE_URL/knowql/stats" -H "$AUTH_HEADER" | jq
```

## Sample question catalog

These question shapes work well against the corpus. Reuse them as
templates.

### Direct citation lookups

Pull a specific clause from a specific article or section.

```json
{"ask": "What exactly does 45 CFR 164.404 say about timing of breach notification to individuals? Quote the regulation."}
```

```json
{"ask": "How does GDPR Article 4 define 'personal data'?"}
```

```json
{"ask": "What does SOC 2 Common Criterion CC6.1 address?"}
```

### Quantified penalty / timing questions

```json
{"ask": "What is the maximum administrative fine under GDPR Article 83 for the most serious infringements?"}
```

```json
{"ask": "What administrative fines apply to non-compliance with the prohibited AI practices under Article 5 of the EU AI Act?"}
```

```json
{"ask": "Under the HIPAA Breach Notification Rule, what is the maximum time a covered entity has to notify affected individuals after discovering a breach?"}
```

### Enumerated-list questions

```json
{"ask": "Under Article 5 of the EU AI Act, which biometric and remote-identification AI practices are prohibited?"}
```

```json
{"ask": "What are the six core Functions of the NIST Cybersecurity Framework 2.0?"}
```

```json
{"ask": "What three categories of safeguards does the HIPAA Security Rule require covered entities and business associates to implement?"}
```

### Cross-framework reasoning

```json
{"ask": "Compare the breach notification timelines under GDPR, HIPAA, and the EU AI Act. Cite each."}
```

```json
{"ask": "What is the #1 risk in the OWASP API Security Top 10 2023, and how does it differ from OWASP Top 10 2021?"}
```

```json
{"ask": "List every NIST AI RMF function and its categories. Where does each function map to in the NIST CSF 2.0 framework?"}
```

### Multi-regulation scenarios

```json
{"ask": "If a US health-tech company deploys an AI diagnostic tool in the EU that uses patient data and gives a wrong recommendation, which regulations apply and what are the worst-case penalties? Be specific with citations."}
```

```json
{"ask": "What does California SB 53 (Transparency in Frontier AI Act) require of frontier AI developers?"}
```

### Temporal / edition diffs

The corpus includes 4 editions of HIPAA Part 164 (current, 2017, 2020,
2024) and both SR 11-7 (2011, rescinded) and SR 26-2 (2026 successor).

```json
{"ask": "Did HIPAA §164.312 change between 2017 and 2024? Show the specific differences in the technical safeguards."}
```

```json
{"ask": "Under SR 11-7 / SR 26-2, what are the key elements of effective model risk management for a banking organization?"}
```

## What the API can and can't do

### Can

- Quote regulation text verbatim with the structural locator (article
  number, CFR section, criterion code) preserved.
- Synthesize across multiple frameworks in a single answer with separate
  citations per framework.
- Distinguish editions of the same regulation when asked temporally
  (e.g. HIPAA Part 164 in 2017 vs 2024, SR 11-7 in 2011 vs SR 26-2 in 2026).
- Refuse to invent facts. If the corpus doesn't contain a claim, the
  answer says so rather than fabricate. Example: asking "what does HIPAA
  say about quantum-resistant encryption?" returns "the regulations do
  not explicitly mention quantum-resistant encryption" plus what HIPAA
  *does* say about encryption — not a hallucinated rule.

### Can't

- Answer questions about regulations not in the corpus (e.g. UK DPA,
  Brazil LGPD, Singapore PDPA, Canada PIPEDA — none are loaded). Ask
  your account rep about expanding the corpus.
- Provide legal advice or substitute for qualified counsel. Answers are
  verbatim retrieval against regulation text, not a legal opinion.
  Always validate with counsel before relying on an answer for a
  compliance decision.
- Track regulatory changes after the corpus was last updated. The corpus
  is a point-in-time snapshot. If an authority publishes an amendment
  after that snapshot, the answer won't reflect it until the corpus is
  refreshed (contact your account rep).
- Resolve cross-references to documents not in the corpus. If a
  regulation cites another directive that isn't loaded, the answer can
  quote the reference but can't pull text from the referenced document.

## When an answer looks wrong

1. **Check `sources_used` and `citations`.** They name the source
   documents the answer was drawn from. If those documents wouldn't
   plausibly contain the claim, the answer is suspect — report it.
2. **Ask more specifically.** "What does GDPR Article 33(1) require?"
   outperforms "what's the GDPR rule about breaches?". Citing structural
   locators (article numbers, section codes, criterion codes) in your
   question produces more reliable answers.
3. **Ask more narrowly.** Long enumerated-list questions ("list every
   prohibited AI practice with all sub-points") occasionally lose items
   at the end of long articles. Split into two narrower questions.
4. **Report it.** Send the question, the answer, the `id` field from the
   response, and what you expected, to your account rep.

## Error handling

| HTTP status | Meaning | What to do |
|---|---|---|
| `200 OK` | Success | Read `output.answer` and `output.citations` |
| `400 Bad Request` | Malformed request body | Validate JSON; confirm `scope` is an array with exactly one slug |
| `401 Unauthorized` | JWT missing or expired | Re-login and retry |
| `403 Forbidden` | JWT valid but project doesn't have access to the context | Verify your key is for project `dbljkrx` |
| `404 Not Found` | Wrong context slug or wrong endpoint path | Confirm `sentinel-regs-test` exists; KnowQL is at `/knowql`, not `/api/v0/knowql` |
| `409 Conflict` | Context temporarily unavailable | Retry shortly; if it persists, contact your account rep |
| `429 Too Many Requests` | Rate limit hit | Honor the `Retry-After` header and `retry_after_seconds` field in the body |
| `5xx` | Server error | Retry with exponential backoff; report persistent failures |

## Operational notes

- **JWT lifetime:** ~30 days. Cache the JWT and re-login on `401`.
  Don't login on every request.
- **Latency:** typical end-to-end query is 4–15 seconds depending on
  question complexity.
- **Citations are by file.** `output.citations[i].file.name` identifies
  the source document; the inline `[c<i+1>]` markers in the answer text
  point back to that citation.
- **`scope` is an array but exactly one entry today.** Multi-context
  fan-out is reserved. Always pass `"scope": ["sentinel-regs-test"]`.
- **`ground: false` returns a bare answer string** without citations.
  Avoid it for compliance work — the value of this context is in the
  citations.
- **Rate limits:** per-project caps apply. 429 responses include
  `retry_after_seconds` and a `Retry-After` header. Retry no sooner than
  the indicated time.

## Language SDK examples

No SDK is required — every example below uses only HTTP and the
language's standard library.

### Python

```python
import os
import requests

BASE = "https://prod.nexus.pinecone.io"
API_KEY = os.environ["PINECONE_API_KEY"]

# 1. Login — exchange API key for short-lived JWT
token = requests.post(
    f"{BASE}/api/v0/auth/login",
    json={"api_key": API_KEY},
).json()["token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Ask a question
resp = requests.post(
    f"{BASE}/knowql",
    headers=headers,
    json={
        "scope": ["sentinel-regs-test"],
        "ask": "Under HIPAA, how long does a covered entity have to notify individuals after discovering a breach?",
        "ground": True,
    },
).json()

print(resp["output"]["answer"])
for c in resp["output"]["citations"]:
    print(f"  cited: {c['file']['name']}")
```

### Node.js / TypeScript

```ts
const BASE = "https://prod.nexus.pinecone.io";
const apiKey = process.env.PINECONE_API_KEY!;

// 1. Login
const loginResp = await fetch(`${BASE}/api/v0/auth/login`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ api_key: apiKey }),
});
const { token } = await loginResp.json();

// 2. Ask a question
const askResp = await fetch(`${BASE}/knowql`, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    scope: ["sentinel-regs-test"],
    ask: "What does SOC 2 Common Criterion CC6.1 address?",
    ground: true,
  }),
});
const result = await askResp.json();
console.log(result.output.answer);
```

### Go

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
)

const base = "https://prod.nexus.pinecone.io"

func main() {
    apiKey := os.Getenv("PINECONE_API_KEY")

    // 1. Login
    loginBody, _ := json.Marshal(map[string]string{"api_key": apiKey})
    resp, _ := http.Post(base+"/api/v0/auth/login", "application/json", bytes.NewReader(loginBody))
    var login struct{ Token string }
    json.NewDecoder(resp.Body).Decode(&login)

    // 2. Ask
    askBody, _ := json.Marshal(map[string]any{
        "scope":  []string{"sentinel-regs-test"},
        "ask":    "What are the six core Functions of the NIST Cybersecurity Framework 2.0?",
        "ground": true,
    })
    req, _ := http.NewRequest("POST", base+"/knowql", bytes.NewReader(askBody))
    req.Header.Set("Authorization", "Bearer "+login.Token)
    req.Header.Set("Content-Type", "application/json")
    resp, _ = http.DefaultClient.Do(req)

    var out map[string]any
    json.NewDecoder(resp.Body).Decode(&out)
    fmt.Printf("%+v\n", out["output"])
}
```

## Support

For new features, additional regulations, expanded jurisdictions, or
issues with answers that look incorrect: contact your account
representative with the question, the answer, and what you expected to
see. Include the `id` field from the response — it's the persistent
query ID and lets us pull the full trace.
