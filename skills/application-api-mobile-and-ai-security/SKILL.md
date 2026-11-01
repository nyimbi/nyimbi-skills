---
name: application-api-mobile-and-ai-security
description: >-
  Test and secure applications across every surface they expose: web apps, REST
  and GraphQL APIs, mobile clients, and AI/LLM systems, plus smart contracts.
  One reusable methodology — scope, discover, probe by class, rate with OWASP,
  remediate, retest — applied to XSS, injection, broken access control, BOLA and
  BFLA, mass assignment, JWT and OAuth flaws, rate-limit abuse, certificate
  pinning bypass, Android intents, prompt injection, RAG poisoning, and
  guardrails. Use when the user asks to "test this API for BOLA", "find XSS in
  this app", "audit our mobile app", "bypass certificate pinning", "is our RAG
  pipeline vulnerable to prompt injection", "why does rate limiting get
  bypassed", "is this JWT implementation safe", or "audit this smart contract".
  This skill owns the testing methodology and the remediation. Do not use for
  executing authorized attack campaigns (see offensive-security-and-red-teaming),
  for JWT/TLS/crypto design questions (see cryptography-and-key-management), or
  for prioritizing and SLA-tracking findings (see
  vulnerability-management-and-compliance).
license: Apache-2.0
---

# Application, API, Mobile, and AI Security

Application testing is one method applied to several tracks, not five separate
disciplines. What varies is the class catalogue and the harness — a proxy for
web, an OpenAPI spec and two user roles for an API, a rooted device for mobile,
a probe suite for an LLM. The scoping, discovery, evidence standard, risk
rating, and remediation loop are identical everywhere.

Two failures ruin application assessments: reporting a scanner's output instead
of a demonstrated exploit path, and testing only the happy path a UI exposes
rather than the object, function, and property authorisation the server is
supposed to enforce. The workflow below is built to make both impossible.

## When to use

- Testing a web application for XSS, CSRF, access control, injection, or logic flaws
- Testing REST/GraphQL APIs against the OWASP API Security Top 10
- Proving BOLA, BFLA, mass assignment, or excessive data exposure with a reproducible request pair
- Assessing an Android or iOS app: static analysis, traffic interception, pinning bypass, intents and deep links
- Testing JWT, OAuth 2.0/OIDC, session, and rate-limit implementations
- Probing an LLM or RAG application for prompt injection, leakage, or unsafe tool use, and wiring guardrails
- Auditing Solidity/Foundry smart contracts before deployment
- Turning findings into remediation with an owner and a retest

**Do not use for** — `offensive-security-and-red-teaming` when the goal is to
gain and demonstrate access in an authorized engagement: red team owns the
campaign, the exploitation chain, and the objective; this skill owns the test
procedure for a class, the two-request proof that a class is present, and the
fix. A finding you can prove with a minimal repro belongs here; a finding that
requires a full chain, C2, and evasion belongs there;
`cryptography-and-key-management` when the question is how a token, signature,
or cipher *should be designed* rather than whether this implementation can be
confused or bypassed; `vulnerability-management-and-compliance` when the ask is
how severe a scanner finding is, when it must be fixed, or how it maps to a
framework; `identity-zero-trust-and-endpoint-security` when the subject is
configuring the IdP, federation, or conditional access rather than testing an
application's login code.

For a quick vulnerability check of a single file or diff rather than a full application assessment, the **security-review** skill is the lighter-weight path.


## Workflow

1. **Fix scope, authorization, and the track.** Record what may be tested, the
   environment, the credentials provided, data-handling rules (no production
   personal data touched), and the stop conditions. Choose the track — web, API,
   mobile, AI/LLM, smart contract — and know that a mobile app's real attack
   surface is usually its backend API. Output: an agreed scope note, and a
   written statement of what is explicitly out of scope.

2. **Inventory the surface before probing anything.** Pull the OpenAPI/Swagger
   or GraphQL schema, enumerate paths, versions, and environments, fuzz for
   undocumented endpoints, and reconcile documented vs. observed (shadow,
   zombie, deprecated). Add subdomain and third-party endpoint discovery for
   web. Output: an endpoint inventory with an owner per version — testing
   coverage is meaningless without knowing what exists
   (`performing-api-inventory-and-discovery.md`).

3. **Map the auth and trust model.** Identify object identifiers and their
   format (sequential, UUID, encoded, composite, slug), record which roles exist
   and what each should reach, note token type and validation path, and list
   trust boundaries: proxies, WAFs, CDNs, gateways, and any content the app
   ingests from outside. Output: a role × resource × allowed-action table that
   the rest of the test compares against.

4. **Run automated discovery, then discard its verdicts.** SAST, DAST, API
   scanner, and fuzzer produce candidates; each candidate still needs a manual
   reproduction. Tune scope and authentication for the scanner so it exercises
   authenticated code paths. Output: a candidate list, nothing marked
   confirmed yet.

5. **Test authorization first — it is the highest-yield class.** For every object
   endpoint, capture a request pair from two users and swap identifiers
   (BOLA); for every state-changing function, replay it with a low-privilege
   token and with method/path/verb manipulation (BFLA); for every writable body,
   inject undocumented privileged fields and diff the resulting object (mass
   assignment); check responses for fields the UI never displays (excessive data
   exposure). Output: for each finding, two requests and two responses showing
   the violated expectation.

6. **Test input handling across contexts.** Injection classes are
   context-specific: HTML body, attribute, JS string, URL, SQL, NoSQL, template,
   shell, XML, LDAP, SMTP, host header. Test each sink with a payload matched to
   its context rather than a generic list, plus SSRF (internal services and
   cloud metadata), deserialization, prototype pollution, and traversal. For
   blind or WAF-fronted variants, use out-of-band and encoding-based delivery.
   Output: a demonstrated effect — executed script, retrieved file, reached
   internal endpoint — not a WAF 403 or a reflected string.

7. **Test session, token, and abuse controls.** Decode tokens and test the
   verification path: `alg:none`, RS→HS confusion, `kid`/`jku`/`x5u` key
   injection, weak secrets, missing `exp`/`aud`. Test OAuth redirect handling,
   PKCE, and scope escalation. For rate limiting: read the limit headers first,
   establish the threshold, then attempt bypass via forwarded headers, method,
   path, case, encoding, and version variation. Add cache, WebSocket, GraphQL
   depth/batching, and business-logic tests where they apply. Note that the
   token *design* questions (which algorithm, how to sign) are answered by
   `../cryptography-and-key-management/`.

8. **Apply the platform track's specifics.** Mobile: static scan (MobSF),
   traffic interception with pinning bypass (identify the pinning mechanism
   before choosing the bypass), exported components and intents, deep links,
   local storage, then re-run step 5 against the exposed API. AI/LLM: direct
   injection → indirect injection → RAG poisoning → tool invocation → system
   prompt extraction → output filter, in that order, with normalization
   (zero-width/Unicode-tag stripping, base64/ROT13 decode) applied before
   declaring a miss. Smart contract: static analysis, symbolic execution, then
   fuzz/invariant tests, all before deployment. See
   [`references/ai-llm-threat-surface.md`](references/ai-llm-threat-surface.md).

9. **Rate, remediate, retest.** Rate with the OWASP risk-rating method
   (likelihood × impact), and for each finding write: class, exact endpoint and
   parameter, the minimal reproduction, the violated rule, the concrete fix in
   the owning team's terms, and a suggested regression test. Retest after the
   fix and record the passing evidence. Re-run every prior test class against
   the change — fixes break authorization elsewhere more often than not.

## Quality bar

- [ ] Scope and authorization are written down, including stop conditions, before any request is sent
- [ ] The endpoint inventory reconciles spec, traffic, and scan output; undocumented and deprecated endpoints are named
- [ ] Every authorization finding is backed by a request pair from two distinct identities, not a single anomalous response
- [ ] Every injection finding demonstrates an executed effect (script fired, file read, internal host reached), not a reflected string or a WAF block
- [ ] Token findings identify the exact verification defect — header-trusted algorithm, missing audience check, unvalidated key source
- [ ] Rate-limit conclusions state the observed threshold and the specific bypass vector, or state that no limit exists
- [ ] Mobile findings distinguish client-side observations from server-side defects and cite the API call that proves the impact
- [ ] AI findings name the stage (input, retrieval, vector store, tool, output) and include the planted payload and the model's response
- [ ] Each finding carries OWASP class, likelihood × impact rating, a concrete fix, an owner, and a proposed regression test
- [ ] Tests are re-run after remediation and the retest result is recorded
- [ ] No test data touches production personal information; no finding reproduces with real user data attached

## Reference map

All 103 merged techniques are catalogued in
[`references/technique-index.md`](references/technique-index.md). Use it for
anything not named below.

Two synthesized topic files:

| Situation | Open |
|---|---|
| Choosing the right file for a vulnerability class, per track (web/API/mobile/contract) | [test-class-matrix.md](references/test-class-matrix.md) |
| LLM/RAG threat surface by stage, test order, guardrail placement | [ai-llm-threat-surface.md](references/ai-llm-threat-surface.md) |

Per-technique detail:

| Situation | Open |
|---|---|
| Structured sweep against the OWASP API Top 10 | [testing-api-security-with-owasp-top-10](references/testing-api-security-with-owasp-top-10.md) |
| BOLA/IDOR: object-level authorization across formats | [testing-api-for-broken-object-level-authorization](references/testing-api-for-broken-object-level-authorization.md) · [exploiting-idor-vulnerabilities](references/exploiting-idor-vulnerabilities.md) · [detecting-api-enumeration-attacks](references/detecting-api-enumeration-attacks.md) |
| BFLA: admin functions callable by low-privilege tokens | [exploiting-broken-function-level-authorization](references/exploiting-broken-function-level-authorization.md) · [testing-for-broken-access-control](references/testing-for-broken-access-control.md) |
| Mass assignment, excessive data exposure, property authorization | [testing-api-for-mass-assignment-vulnerability](references/testing-api-for-mass-assignment-vulnerability.md) · [exploiting-mass-assignment-in-rest-apis](references/exploiting-mass-assignment-in-rest-apis.md) · [exploiting-excessive-data-exposure-in-api](references/exploiting-excessive-data-exposure-in-api.md) · [detecting-broken-object-property-level-authorization](references/detecting-broken-object-property-level-authorization.md) |
| API authentication and session weaknesses | [testing-api-authentication-weaknesses](references/testing-api-authentication-weaknesses.md) · [testing-mobile-api-authentication](references/testing-mobile-api-authentication.md) |
| JWT — one topic across four techniques (confusion, `none`, weak secret, full audit) | [testing-jwt-token-security](references/testing-jwt-token-security.md) · [testing-for-json-web-token-vulnerabilities](references/testing-for-json-web-token-vulnerabilities.md) · [exploiting-jwt-algorithm-confusion-attack](references/exploiting-jwt-algorithm-confusion-attack.md) · [performing-jwt-none-algorithm-attack](references/performing-jwt-none-algorithm-attack.md) |
| OAuth 2.0 / OIDC implementation flaws | [testing-oauth2-implementation-flaws](references/testing-oauth2-implementation-flaws.md) · [exploiting-oauth-misconfiguration](references/exploiting-oauth-misconfiguration.md) |
| Rate limiting — one topic: implement, detect abuse, bypass | [implementing-api-rate-limiting-and-throttling](references/implementing-api-rate-limiting-and-throttling.md) · [implementing-api-abuse-detection-with-rate-limiting](references/implementing-api-abuse-detection-with-rate-limiting.md) · [performing-api-rate-limiting-bypass](references/performing-api-rate-limiting-bypass.md) |
| XSS testing with Burp and the CSP bypass that defeats the mitigation | [testing-for-xss-vulnerabilities-with-burpsuite](references/testing-for-xss-vulnerabilities-with-burpsuite.md) · [performing-content-security-policy-bypass](references/performing-content-security-policy-bypass.md) |
| SQL/NoSQL/second-order injection | [exploiting-sql-injection-with-sqlmap](references/exploiting-sql-injection-with-sqlmap.md) · [exploiting-nosql-injection-vulnerabilities](references/exploiting-nosql-injection-vulnerabilities.md) · [performing-second-order-sql-injection](references/performing-second-order-sql-injection.md) |
| SSRF, including blind and out-of-band | [exploiting-server-side-request-forgery](references/exploiting-server-side-request-forgery.md) · [performing-blind-ssrf-exploitation](references/performing-blind-ssrf-exploitation.md) · [exploiting-api-injection-vulnerabilities](references/exploiting-api-injection-vulnerabilities.md) |
| Template injection, XML/XXE, deserialization, prototype pollution, type juggling | [exploiting-template-injection-vulnerabilities](references/exploiting-template-injection-vulnerabilities.md) · [testing-for-xxe-injection-vulnerabilities](references/testing-for-xxe-injection-vulnerabilities.md) · [testing-for-xml-injection-vulnerabilities](references/testing-for-xml-injection-vulnerabilities.md) · [exploiting-insecure-deserialization](references/exploiting-insecure-deserialization.md) · [exploiting-prototype-pollution-in-javascript](references/exploiting-prototype-pollution-in-javascript.md) · [exploiting-type-juggling-vulnerabilities](references/exploiting-type-juggling-vulnerabilities.md) |
| CSRF, CORS, clickjacking, open redirect, headers, host/email injection | [performing-csrf-attack-simulation](references/performing-csrf-attack-simulation.md) · [testing-cors-misconfiguration](references/testing-cors-misconfiguration.md) · [performing-clickjacking-attack-test](references/performing-clickjacking-attack-test.md) · [testing-for-open-redirect-vulnerabilities](references/testing-for-open-redirect-vulnerabilities.md) · [performing-security-headers-audit](references/performing-security-headers-audit.md) · [testing-for-host-header-injection](references/testing-for-host-header-injection.md) · [testing-for-email-header-injection](references/testing-for-email-header-injection.md) |
| Business logic, forced browsing, traversal, data exposure | [testing-for-business-logic-vulnerabilities](references/testing-for-business-logic-vulnerabilities.md) · [bypassing-authentication-with-forced-browsing](references/bypassing-authentication-with-forced-browsing.md) · [performing-directory-traversal-testing](references/performing-directory-traversal-testing.md) · [testing-for-sensitive-data-exposure](references/testing-for-sensitive-data-exposure.md) |
| Cache poisoning/deception, smuggling, parameter pollution, race conditions, WebSockets | [performing-web-cache-poisoning-attack](references/performing-web-cache-poisoning-attack.md) · [performing-web-cache-deception-attack](references/performing-web-cache-deception-attack.md) · [exploiting-http-request-smuggling](references/exploiting-http-request-smuggling.md) · [performing-http-parameter-pollution-attack](references/performing-http-parameter-pollution-attack.md) · [exploiting-race-condition-vulnerabilities](references/exploiting-race-condition-vulnerabilities.md) · [testing-websocket-api-security](references/testing-websocket-api-security.md) · [exploiting-websocket-vulnerabilities](references/exploiting-websocket-vulnerabilities.md) |
| GraphQL introspection, batching, and depth abuse | [performing-graphql-security-assessment](references/performing-graphql-security-assessment.md) · [performing-graphql-introspection-attack](references/performing-graphql-introspection-attack.md) · [performing-graphql-depth-limit-attack](references/performing-graphql-depth-limit-attack.md) |
| SOAP and legacy web services | [performing-soap-web-service-security-testing](references/performing-soap-web-service-security-testing.md) |
| WAF bypass to deliver payloads; subdomain and surface discovery | [performing-web-application-firewall-bypass](references/performing-web-application-firewall-bypass.md) · [performing-subdomain-enumeration-with-subfinder](references/performing-subdomain-enumeration-with-subfinder.md) |
| API inventory, shadow endpoints, schema validation, gateway controls | [performing-api-inventory-and-discovery](references/performing-api-inventory-and-discovery.md) · [detecting-shadow-api-endpoints](references/detecting-shadow-api-endpoints.md) · [implementing-api-schema-validation-security](references/implementing-api-schema-validation-security.md) · [implementing-api-gateway-security-controls](references/implementing-api-gateway-security-controls.md) · [implementing-api-key-security-controls](references/implementing-api-key-security-controls.md) · [implementing-api-security-posture-management](references/implementing-api-security-posture-management.md) |
| Automated API testing: fuzzing, Postman collections, conformance | [performing-api-fuzzing-with-restler](references/performing-api-fuzzing-with-restler.md) · [performing-api-security-testing-with-postman](references/performing-api-security-testing-with-postman.md) · [implementing-api-security-testing-with-42crunch](references/implementing-api-security-testing-with-42crunch.md) |
| Full iOS or Android assessment: static, dynamic, instrumentation | [performing-ios-app-security-assessment](references/performing-ios-app-security-assessment.md) · [reverse-engineering-ios-app-with-frida](references/reverse-engineering-ios-app-with-frida.md) · [analyzing-ios-app-security-with-objection](references/analyzing-ios-app-security-with-objection.md) · [performing-android-app-static-analysis-with-mobsf](references/performing-android-app-static-analysis-with-mobsf.md) · [performing-dynamic-analysis-of-android-app](references/performing-dynamic-analysis-of-android-app.md) |
| Certificate pinning bypass and mobile traffic interception | [performing-mobile-app-certificate-pinning-bypass](references/performing-mobile-app-certificate-pinning-bypass.md) · [intercepting-mobile-traffic-with-burpsuite](references/intercepting-mobile-traffic-with-burpsuite.md) |
| Android intents/IPC, deep links, insecure local storage | [testing-android-intents-for-vulnerabilities](references/testing-android-intents-for-vulnerabilities.md) · [exploiting-deeplink-vulnerabilities](references/exploiting-deeplink-vulnerabilities.md) · [exploiting-insecure-data-storage-in-mobile](references/exploiting-insecure-data-storage-in-mobile.md) |
| Enterprise mobile protection and suspicious app behaviour | [implementing-mobile-application-management](references/implementing-mobile-application-management.md) · [detecting-mobile-malware-behavior](references/detecting-mobile-malware-behavior.md) |
| Direct prompt injection detection and classification | [detecting-ai-model-prompt-injection-attacks](references/detecting-ai-model-prompt-injection-attacks.md) |
| Indirect injection hidden in documents, pages, images | [detecting-indirect-prompt-injection](references/detecting-indirect-prompt-injection.md) |
| Prompt injection against RAG pipelines | [testing-prompt-injection-in-rag-pipelines](references/testing-prompt-injection-in-rag-pipelines.md) |
| Vector store and embedding weaknesses; training-data and model poisoning | [assessing-vector-and-embedding-weaknesses](references/assessing-vector-and-embedding-weaknesses.md) · [detecting-data-and-model-poisoning](references/detecting-data-and-model-poisoning.md) |
| Model extraction, inversion, membership inference via the inference API | [detecting-model-extraction-attacks](references/detecting-model-extraction-attacks.md) |
| System prompt and embedded-secret extraction | [testing-for-system-prompt-leakage](references/testing-for-system-prompt-leakage.md) |
| Guardrails: input/output classification and filtering | [defending-llms-with-guardrails](references/defending-llms-with-guardrails.md) · [implementing-llm-guardrails-for-security](references/implementing-llm-guardrails-for-security.md) |
| LLM red teaming: garak, PyRIT, continuous Promptfoo regression | [red-teaming-llms-with-garak](references/red-teaming-llms-with-garak.md) · [orchestrating-llm-attacks-with-pyrit](references/orchestrating-llm-attacks-with-pyrit.md) · [continuous-llm-red-teaming-with-promptfoo](references/continuous-llm-red-teaming-with-promptfoo.md) |
| Agentic tool invocation controls and MCP server audit | [securing-agentic-ai-tool-invocation](references/securing-agentic-ai-tool-invocation.md) · [auditing-mcp-servers-for-tool-poisoning](references/auditing-mcp-servers-for-tool-poisoning.md) |
| Smart contract audit in Foundry; Slither/Mythril analysis | [auditing-foundry-smart-contract-security](references/auditing-foundry-smart-contract-security.md) · [analyzing-ethereum-smart-contract-vulnerabilities](references/analyzing-ethereum-smart-contract-vulnerabilities.md) |
| RASP, WAF logging, and supply-chain simulation (defensive/testing hybrid) | [implementing-runtime-application-self-protection](references/implementing-runtime-application-self-protection.md) · [implementing-web-application-logging-with-modsecurity](references/implementing-web-application-logging-with-modsecurity.md) · [performing-supply-chain-attack-simulation](references/performing-supply-chain-attack-simulation.md) · [exploiting-broken-link-hijacking](references/exploiting-broken-link-hijacking.md) |
| Shift-left scanning wired into CI (SAST/DAST/SCA/secrets) | [implementing-devsecops-security-scanning](references/implementing-devsecops-security-scanning.md) |
| Binary and coverage-guided fuzzing | [performing-fuzzing-with-aflplusplus](references/performing-fuzzing-with-aflplusplus.md) |

Executable helpers for each technique live in `scripts/<technique-name>/` — read
the reference file first, then run it.

## Output format

For any test engagement, deliver:

```markdown
# <Application> — Security Test Report

## Scope and authorization
In scope | Out of scope | Track(s) | Credentials | Data rules | Dates

## Surface
Endpoint inventory: path | method | version | auth required | owner |
documented? (spec vs. observed vs. shadow)

## Auth model
Role | Resources reachable | Object ID format | Token type | Validation path

## Findings
| ID | OWASP class | Endpoint + parameter | Likelihood × Impact | Minimal reproduction (two requests max) |
|   | Violated rule | Concrete fix | Owner | Proposed regression test |

## Platform notes
Mobile: client vs. server split, pinning mechanism, bypass used.
AI/LLM: stage reached, planted payload, model response, guardrail hit or miss.

## Retest
Finding | Fix commit | Retest result | Evidence
```

Every finding must include the exact endpoint, the minimal reproduction, and a
fix the owning team can implement without asking a follow-up question. A
severity with no reproduction is a hypothesis, not a finding.
