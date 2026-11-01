# Test class matrix — pick the track, then the class, then the file

The testing method below (scope → discover → probe → rate → remediate → retest)
is the same for every application type. What changes is the class catalogue.
Use this file to choose the right reference instead of opening the index first.

Each row is one class. Where several merged techniques describe the same class
with different tools, they are listed together — they are one topic, not several.

## Web application

| Class | First open | Notes |
|---|---|---|
| XSS (reflected, stored, DOM) | `testing-for-xss-vulnerabilities-with-burpsuite.md` | Identify the reflection context first — HTML body, attribute, JS string, URL — then use a context-matched payload |
| CSP bypass (how to land the XSS anyway) | `performing-content-security-policy-bypass.md` | Read after XSS, not before |
| Broken access control / forced browsing | `testing-for-broken-access-control.md`, `bypassing-authentication-with-forced-browsing.md` | Function-level and object-level checks together |
| CSRF | `performing-csrf-attack-simulation.md` | Token presence is not the test; token *binding* is |
| CORS misconfiguration | `testing-cors-misconfiguration.md` | Origin reflection + credentials is the real finding |
| Clickjacking, open redirect, security headers | `performing-clickjacking-attack-test.md`, `testing-for-open-redirect-vulnerabilities.md`, `performing-security-headers-audit.md` | Cheap checks; run them in every engagement |
| Host / email header injection | `testing-for-host-header-injection.md`, `testing-for-email-header-injection.md` | Password-reset poisoning is the impact that matters |
| Path traversal, XML/XXE/XPath | `performing-directory-traversal-testing.md`, `testing-for-xxe-injection-vulnerabilities.md`, `testing-for-xml-injection-vulnerabilities.md` | |
| Deserialization, prototype pollution, type juggling | `exploiting-insecure-deserialization.md`, `exploiting-prototype-pollution-in-javascript.md`, `exploiting-type-juggling-vulnerabilities.md` | Language-specific; pick by the stack |
| SSTI, HTTP smuggling, parameter pollution | `exploiting-template-injection-vulnerabilities.md`, `exploiting-http-request-smuggling.md`, `performing-http-parameter-pollution-attack.md` | |
| Cache poisoning / deception | `performing-web-cache-poisoning-attack.md`, `performing-web-cache-deception-attack.md` | Needs a CDN in front to be exploitable |
| WebSockets, SOAP | `exploiting-websocket-vulnerabilities.md`, `testing-websocket-api-security.md`, `performing-soap-web-service-security-testing.md` | Upgrade handshake auth is usually the gap |
| Business logic | `testing-for-business-logic-vulnerabilities.md` | Scanners never find these; requires a workflow map |
| WAF bypass (to deliver any of the above) | `performing-web-application-firewall-bypass.md` | Only when a WAF is actually in the path |
| Sensitive data exposure | `testing-for-sensitive-data-exposure.md` | Response bodies, not just requests |

## API

| Class | First open | Notes |
|---|---|---|
| Full API Top 10 pass | `testing-api-security-with-owasp-top-10.md` | Entry point when you have a spec and time for a structured sweep |
| BOLA / IDOR | `testing-api-for-broken-object-level-authorization.md`, `exploiting-idor-vulnerabilities.md`, `detecting-api-enumeration-attacks.md` | Classify ID type first — sequential, UUID, encoded, composite, slug |
| BFLA (admin/privileged functions) | `exploiting-broken-function-level-authorization.md` | Method/verb and path manipulation, with a low-privilege token |
| Mass assignment / property authorization / excessive exposure | `testing-api-for-mass-assignment-vulnerability.md`, `exploiting-mass-assignment-in-rest-apis.md`, `exploiting-excessive-data-exposure-in-api.md`, `detecting-broken-object-property-level-authorization.md` | Inject undocumented fields and compare against the data model |
| Broken authentication, token handling, session | `testing-api-authentication-weaknesses.md`, `testing-mobile-api-authentication.md` | |
| JWT — one topic, four entry points | `testing-jwt-token-security.md`, `testing-for-json-web-token-vulnerabilities.md`, `exploiting-jwt-algorithm-confusion-attack.md`, `performing-jwt-none-algorithm-attack.md` | Decode header/payload, then test `alg:none`, RS→HS confusion, `kid`/`jku`/`x5u` injection, weak secret |
| OAuth 2.0 / OIDC implementation flaws | `testing-oauth2-implementation-flaws.md`, `exploiting-oauth-misconfiguration.md` | Redirect URI, code interception, PKCE bypass, scope escalation |
| Rate limiting — one topic: build and break | `implementing-api-rate-limiting-and-throttling.md`, `implementing-api-abuse-detection-with-rate-limiting.md`, `performing-api-rate-limiting-bypass.md` | Read the headers (`X-RateLimit-*`, `Retry-After`) before bypassing; bypass via forwarded headers, method/path/encoding variation |
| Injection through API parameters | `exploiting-api-injection-vulnerabilities.md`, `exploiting-sql-injection-with-sqlmap.md`, `performing-second-order-sql-injection.md`, `exploiting-nosql-injection-vulnerabilities.md` | |
| SSRF, including blind and metadata-targeted | `exploiting-server-side-request-forgery.md`, `performing-blind-ssrf-exploitation.md` | Cloud metadata endpoint is the escalation path |
| Shadow / zombie / undocumented endpoints | `performing-api-inventory-and-discovery.md`, `detecting-shadow-api-endpoints.md` | OWASP API9; do this before judging coverage |
| Schema-contract testing, fuzzing, conformance | `implementing-api-schema-validation-security.md`, `performing-api-fuzzing-with-restler.md`, `performing-api-security-testing-with-postman.md`, `implementing-api-security-testing-with-42crunch.md` | Stateful fuzzing needs a spec |
| GraphQL | `performing-graphql-security-assessment.md`, `performing-graphql-introspection-attack.md`, `performing-graphql-depth-limit-attack.md` | Introspection, batching brute force, nested-query DoS |
| Gateway and key controls (defensive side) | `implementing-api-gateway-security-controls.md`, `implementing-api-key-security-controls.md`, `implementing-api-threat-protection-with-apigee.md`, `implementing-api-security-posture-management.md` | Reach for these when remediating, not when testing |

## Mobile

| Class | First open | Notes |
|---|---|---|
| Full iOS or Android assessment | `performing-ios-app-security-assessment.md`, `performing-android-app-static-analysis-with-mobsf.md`, `performing-dynamic-analysis-of-android-app.md` | Static first, then runtime |
| Traffic interception — certificate pinning bypass | `performing-mobile-app-certificate-pinning-bypass.md` | Identify the pinning method (NSC, OkHttp, TrustManager, TrustKit) before choosing the bypass; Objection first, custom Frida script second |
| Proxy traffic analysis against the backend API | `intercepting-mobile-traffic-with-burpsuite.md` | The backend is usually the real finding |
| Android intents / IPC / exported components | `testing-android-intents-for-vulnerabilities.md` | Drozer attack-surface enumeration |
| Deep links and scheme hijacking | `exploiting-deeplink-vulnerabilities.md` | |
| Insecure local storage | `exploiting-insecure-data-storage-in-mobile.md` | SharedPreferences, Keychain/Keystore usage |
| Enterprise app protection / BYOD data separation | `implementing-mobile-application-management.md` | Defensive counterpart |
| Suspicious or malicious mobile app behaviour | `detecting-mobile-malware-behavior.md` | |

## Blockchain / smart contracts

| Class | First open | Notes |
|---|---|---|
| Full Foundry project audit | `auditing-foundry-smart-contract-security.md` | Static + symbolic + fuzz/invariant testing before deploy |
| Slither/Mythril analysis of Solidity | `analyzing-ethereum-smart-contract-vulnerabilities.md` | Reentrancy, access control, arithmetic, oracle manipulation |
| Pre-deployment key and deploy hygiene | `auditing-foundry-smart-contract-security.md` | No plaintext keys, encrypted keystore |

AI/LLM applications have their own surface — see
[`ai-llm-threat-surface.md`](ai-llm-threat-surface.md).
