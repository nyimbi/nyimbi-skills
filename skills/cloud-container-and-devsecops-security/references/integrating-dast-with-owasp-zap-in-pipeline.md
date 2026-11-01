# Integrating Dast With Owasp Zap In Pipeline

## API Reference

## ZAP Docker Scan Scripts

### Baseline Scan (Passive Only)
```bash
docker run --rm -v $(pwd):/zap/wrk zaproxy/zap-stable \
  zap-baseline.py -t https://target.com -J report.json -I
```

### Full Scan (Active + Passive)
```bash
docker run --rm -v $(pwd):/zap/wrk zaproxy/zap-stable \
  zap-full-scan.py -t https://target.com -J report.json -m 5 -I
```

### API Scan (OpenAPI/Swagger)
```bash
docker run --rm -v $(pwd):/zap/wrk zaproxy/zap-stable \
  zap-api-scan.py -t https://target.com/openapi.json -f openapi -J report.json
```

### Return Codes
| Code | Meaning |
|------|---------|
| 0 | No alerts above threshold |
| 1 | Warnings found |
| 2 | Failures found |

### Common Flags
| Flag | Description |
|------|-------------|
| `-t` | Target URL |
| `-J` | JSON report filename |
| `-m` | Max scan duration in minutes |
| `-I` | Do not return failure on warnings |
| `-f` | API spec format (`openapi`, `soap`) |
| `-r` | HTML report filename |
| `-c` | Config file for rule tuning |

## ZAP JSON Report Structure
```json
{"site": [{"alerts": [{"name": "...", "riskdesc": "High (Medium)",
  "cweid": "79", "count": 3, "solution": "..."}]}]}
```

### Risk Levels
| Level | Action |
|-------|--------|
| High | Block deployment |
| Medium | Require review |
| Low | Track as tech debt |
| Informational | Log only |

## References
- ZAP Docker: https://www.zaproxy.org/docs/docker/
- ZAP Automation: https://www.zaproxy.org/docs/automate/

---

## Standards and Controls

## OWASP Top 10 - DAST Coverage

| OWASP Category | ZAP Detection | Alert IDs |
|----------------|---------------|-----------|
| A01: Broken Access Control | Partial | 10020, 10035, 40012 |
| A02: Cryptographic Failures | Yes | 10003, 10041 |
| A03: Injection | Yes | 40012, 40014, 40018, 40019 |
| A05: Security Misconfiguration | Yes | 10015, 10020, 10021, 10035 |
| A07: Auth Failures | Partial | 10010, 10054 |
| A09: Logging Failures | Yes | 10035 |
| A10: SSRF | Partial | Custom scan |

## OWASP SAMM - Verification: Security Testing

### Level 2: DAST Integration
- Automated DAST scanning in CI/CD pipelines
- Baseline scans on every deployment, full scans weekly
- Findings tracked and triaged with defined SLAs

### Level 3: Advanced DAST
- Authenticated scanning with session management
- API-specific scanning with OpenAPI specifications
- Custom scan policies tuned for application-specific risks

## NIST SSDF (SP 800-218)

### PW.8: Test Executable Code
- PW.8.1: Test executable code using dynamic analysis
- DAST validates running application behavior against security requirements
- Integration into CI/CD automates regular testing

## PCI DSS v4.0

- 6.2.4: Use automated methods to prevent common attacks (XSS, SQLi)
- 6.4.1: Web applications are protected against known attacks
- 11.3.1: Internal vulnerability scans performed at least quarterly

---

## Workflows

## DAST Pipeline Integration

```
Build & Deploy to Staging
       │
       ▼
┌──────────────────┐
│ Health Check      │
│ (wait for ready)  │
└──────┬───────────┘
       │
       ├──────────────┐
       ▼              ▼
┌───────────┐  ┌───────────┐
│ ZAP       │  │ ZAP API   │
│ Baseline  │  │ Scan      │
│ Scan      │  │ (OpenAPI) │
└─────┬─────┘  └─────┬─────┘
      │               │
      └───────┬───────┘
              ▼
       ┌──────────────┐
       │ Report Gen   │
       │ + Upload     │
       └──────┬───────┘
              │
       ┌──────┴──────┐
       ▼             ▼
     PASS          FAIL
     Deploy to     Block +
     Production    Alert
```

## ZAP Scan Types Comparison

| Scan Type | Duration | Coverage | CI/CD Suitable | Active Attacks |
|-----------|----------|----------|----------------|----------------|
| Baseline | 2-5 min | Passive only | Yes | No |
| Full Scan | 30-120 min | Comprehensive | Scheduled | Yes |
| API Scan | 5-15 min | API endpoints | Yes | Yes |

## ZAP Docker Commands

```bash
# Baseline scan (passive)
docker run --rm -v $(pwd):/zap/wrk zaproxy/zap-stable \
  zap-baseline.py -t http://target:8080 \
  -r report.html -J report.json -c rules.tsv

# Full scan (active)
docker run --rm -v $(pwd):/zap/wrk zaproxy/zap-stable \
  zap-full-scan.py -t http://target:8080 \
  -r report.html -J report.json -c rules.tsv -T 60

# API scan (OpenAPI)
docker run --rm -v $(pwd):/zap/wrk zaproxy/zap-stable \
  zap-api-scan.py -t http://target:8080/openapi.json \
  -f openapi -r report.html -J report.json
```

## Authenticated Scanning Configuration

```yaml
# zap-auth-config.yaml
authentication:
  method: form
  loginUrl: http://target:8080/login
  parameters:
    username: testuser
    password: testpass123
  loggedInIndicator: "\\QWelcome\\E"
  loggedOutIndicator: "\\QSign In\\E"

context:
  name: "auth-context"
  include:
    - "http://target:8080/.*"
  exclude:
    - "http://target:8080/logout"
    - "http://target:8080/static/.*"
```

---

## Working Template

## ZAP Rules File

```tsv
# .zap/rules.tsv
# Rule ID	Action	Description
10003	IGNORE	# Vulnerable JS Library (handled by SCA tools)
10015	WARN	# Incomplete Cache-control Header
10020	WARN	# X-Frame-Options Header Not Set
10021	FAIL	# X-Content-Type-Options Missing
10035	FAIL	# Strict-Transport-Security Missing
10038	FAIL	# Content Security Policy Missing
10098	IGNORE	# Cross-Domain Misconfiguration (CDN expected)
40012	FAIL	# XSS Reflected
40014	FAIL	# XSS Persistent
40018	FAIL	# SQL Injection
40019	FAIL	# SQL Injection (MySQL)
40024	FAIL	# SQL Injection (PostgreSQL)
40032	WARN	# .htaccess Info Leak
90033	WARN	# Loosely Scoped Cookie
```

## GitHub Actions: Complete DAST Pipeline

```yaml
# .github/workflows/dast.yml
name: DAST Pipeline

on:
  workflow_run:
    workflows: ["Deploy to Staging"]
    types: [completed]

jobs:
  zap-scan:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - uses: actions/checkout@v4

      - name: Wait for staging
        run: |
          for i in $(seq 1 30); do
            if curl -sf https://staging.example.com/health; then break; fi
            sleep 10
          done

      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.12.0
        with:
          target: 'https://staging.example.com'
          rules_file_name: '.zap/rules.tsv'

      - name: ZAP API Scan
        uses: zaproxy/action-api-scan@v0.12.0
        with:
          target: 'https://staging.example.com/api/v1/openapi.json'
          format: openapi
          rules_file_name: '.zap/rules.tsv'

      - name: Upload Reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: dast-reports
          path: report_*.html
```

## Docker Compose for Local DAST Testing

```yaml
# docker-compose.dast.yml
services:
  app:
    build: .
    ports: ["8080:8080"]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 5s
      retries: 10

  zap:
    image: zaproxy/zap-stable:latest
    depends_on:
      app:
        condition: service_healthy
    volumes:
      - ./zap-reports:/zap/wrk
      - ./.zap/rules.tsv:/zap/wrk/rules.tsv
    command: >
      zap-baseline.py
        -t http://app:8080
        -r /zap/wrk/report.html
        -J /zap/wrk/report.json
        -c /zap/wrk/rules.tsv
        -I
```
