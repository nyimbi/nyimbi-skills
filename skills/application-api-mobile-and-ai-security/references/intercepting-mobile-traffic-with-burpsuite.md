# Intercepting Mobile Traffic With Burpsuite

## API Reference

## HAR (HTTP Archive) Format

### Structure
```json
{"log": {"entries": [{"request": {"method": "GET", "url": "https://...",
  "headers": [{"name": "Authorization", "value": "Bearer ..."}],
  "postData": {"text": "..."}},
  "response": {"status": 200, "headers": [...],
  "content": {"text": "..."}}}]}}
```

### Key HAR Fields
| Field | Description |
|-------|-------------|
| `request.url` | Full request URL |
| `request.method` | HTTP method |
| `request.headers` | Request headers array |
| `request.postData.text` | POST body content |
| `response.status` | HTTP status code |
| `response.content.text` | Response body |

## Burp Suite Proxy Setup for Mobile
1. Set proxy listener: `127.0.0.1:8080`
2. Configure device WiFi proxy to Burp IP:8080
3. Install Burp CA: `http://burp/cert`
4. Export traffic as HAR: Proxy > HTTP History > Save Items

## mitmproxy Alternative
```bash
mitmproxy --mode regular --listen-port 8080
mitmdump -w output.flow --set flow_detail=3
# Convert to HAR:
mitmproxy2har output.flow > capture.har
```

## Certificate Pinning Bypass
| Platform | Tool |
|----------|------|
| Android | Frida + objection (`objection explore --startup-command 'android sslpinning disable'`) |
| iOS | SSL Kill Switch 2 (Cydia) |

## Sensitive Data Patterns
| Type | Regex Pattern |
|------|---------------|
| Email | `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` |
| Credit Card | `\b(?:4\d{3}|5[1-5]\d{2})\d{12}\b` |
| JWT | `eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+` |

## References
- Burp Suite: https://portswigger.net/burp/documentation
- HAR spec: https://w3c.github.io/web-performance/specs/HAR/Overview.html
- mitmproxy: https://docs.mitmproxy.org/stable/

---

## Standards and Controls

## OWASP Mobile Top 10 2024 Mapping

| OWASP ID | Risk | Burp Suite Testing Coverage |
|----------|------|----------------------------|
| M1 | Improper Credential Usage | Identify credentials in plaintext, weak token formats in API traffic |
| M3 | Insecure Authentication/Authorization | Test auth bypass, session management, IDOR via request manipulation |
| M4 | Insufficient Input/Output Validation | SQL injection, XSS, command injection via Burp Scanner/Repeater |
| M5 | Insecure Communication | Detect cleartext HTTP, weak TLS, missing HSTS, certificate validation |
| M8 | Security Misconfiguration | Identify verbose error messages, debug endpoints, missing security headers |

## OWASP MASVS v2.0 Control Mapping

| MASVS Category | Burp Suite Assessment | Test Method |
|----------------|----------------------|-------------|
| MASVS-NETWORK | TLS configuration, certificate pinning, cleartext detection | Proxy interception, SSL scan |
| MASVS-AUTH | Token validation, session handling, credential transmission | Repeater manipulation |
| MASVS-STORAGE | Sensitive data in API responses cached client-side | Response header analysis |
| MASVS-PLATFORM | Deep link parameter injection, WebView URL loading | Request crafting |

## OWASP API Security Top 10 2023

| API Risk | Burp Suite Test |
|----------|----------------|
| API1: Broken Object Level Authorization | Modify object IDs in intercepted requests |
| API2: Broken Authentication | Replay tokens, test token expiration |
| API3: Broken Object Property Level Auth | Modify response/request properties |
| API5: Broken Function Level Authorization | Access admin endpoints with user tokens |
| API8: Security Misconfiguration | Check response headers, error handling |

## CWE Mappings

| CWE ID | Title | Detection Method |
|--------|-------|-----------------|
| CWE-200 | Exposure of Sensitive Information | Inspect API responses for data leakage |
| CWE-295 | Improper Certificate Validation | Test with self-signed proxy certificate |
| CWE-319 | Cleartext Transmission | Monitor for HTTP (non-HTTPS) requests |
| CWE-352 | Cross-Site Request Forgery | Check for anti-CSRF tokens in requests |
| CWE-613 | Insufficient Session Expiration | Test token validity after logout |

---

## Workflows

## Workflow 1: Standard Mobile API Testing

```
[Configure Burp Listener] --> [Set Device Proxy] --> [Install CA Cert] --> [Open Target App]
                                                                                |
                                                                                v
                                                                     [Capture HTTP History]
                                                                                |
                                                          +---------------------+---------------------+
                                                          |                     |                     |
                                                   [Map API surface]    [Identify auth flow]   [Check data exposure]
                                                          |                     |                     |
                                                          v                     v                     v
                                                   [Send to Scanner]    [Token analysis]       [PII in responses]
                                                   [Active scan]        [Session testing]      [Sensitive headers]
                                                          |                     |                     |
                                                          +---------------------+---------------------+
                                                                                |
                                                                         [Compile findings]
                                                                         [Generate report]
```

## Workflow 2: SSL Pinning Bypass Pipeline

```
[Set Proxy] --> [Open App] --> [Connection fails?]
                                    |
                              [Yes: Pinning active]
                                    |
                     +--------------+--------------+
                     |              |              |
              [Frida bypass]  [Objection]   [APK repackage]
              [Generic script] [sslpinning] [Remove pinning code]
                     |         [disable]          |
                     +--------------+--------------+
                                    |
                           [Verify traffic flows]
                           [Continue assessment]
```

## Workflow 3: Authentication Testing

```
[Intercept login request] --> [Capture auth token] --> [Analyze token format]
                                                              |
                                                   +----------+----------+
                                                   |                     |
                                            [JWT analysis]        [Opaque token]
                                            [Decode payload]      [Session management]
                                            [Check signature]     [Timeout testing]
                                            [Modify claims]       [Concurrent session]
                                                   |                     |
                                                   +----------+----------+
                                                              |
                                                    [Test IDOR with user IDs]
                                                    [Test privilege escalation]
                                                    [Test token replay after logout]
```

## Decision Matrix: Traffic Interception Approach

| Scenario | Android | iOS |
|----------|---------|-----|
| No pinning, API < 24 | Standard proxy + user CA | Standard proxy + profile install |
| No pinning, API 24+ | System CA or network_security_config mod | Standard proxy + profile install |
| Pinning implemented | Frida/Objection bypass + system CA | Frida/Objection bypass |
| Custom protocol | Wireshark + custom Frida hooks | Wireshark + custom Frida hooks |
| VPN tunnel | iptables redirect on rooted device | Not feasible without jailbreak |

---

## Working Template

## Engagement Information

| Field | Value |
|-------|-------|
| Application | [APP_NAME] |
| Platform | [Android/iOS] |
| Proxy Tool | Burp Suite [VERSION] |
| Assessment Date | [DATE] |
| Total Requests Captured | [COUNT] |
| Unique Endpoints | [COUNT] |

## API Surface Map

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| [METHOD] | [PATH] | [YES/NO] | [DESCRIPTION] |

## Traffic Security Findings

### Finding [N]: [TITLE]

- **Severity**: [CRITICAL/HIGH/MEDIUM/LOW]
- **OWASP Mobile**: [M1-M10]
- **CWE**: [CWE-ID]
- **Affected Endpoint**: [URL]
- **Description**: [DESCRIPTION]
- **Evidence**: [REQUEST/RESPONSE_SNIPPET]
- **Recommendation**: [REMEDIATION]

## Authentication Analysis

| Check | Result | Details |
|-------|--------|---------|
| Token Format | [JWT/Opaque/Other] | [DETAILS] |
| Token Expiration | [DURATION] | [DETAILS] |
| Token in URL | [YES/NO] | [DETAILS] |
| Refresh Mechanism | [Present/Absent] | [DETAILS] |
| Session Invalidation | [Works/Fails] | [DETAILS] |

## Security Header Compliance

| Header | Present | Value | Status |
|--------|---------|-------|--------|
| Strict-Transport-Security | [YES/NO] | [VALUE] | [PASS/FAIL] |
| Content-Security-Policy | [YES/NO] | [VALUE] | [PASS/FAIL] |
| X-Content-Type-Options | [YES/NO] | [VALUE] | [PASS/FAIL] |
| Cache-Control | [YES/NO] | [VALUE] | [PASS/FAIL] |

## Recommendations

1. [RECOMMENDATION]
