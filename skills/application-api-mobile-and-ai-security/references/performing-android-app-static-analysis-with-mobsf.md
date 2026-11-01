# Performing Android App Static Analysis With Mobsf

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `requests` | HTTP client for MobSF REST API v1 |
| `json` | Parse scan reports and finding data |
| `os` | Read `MOBSF_URL` and `MOBSF_API_KEY` environment variables |

## Installation

```bash
pip install requests

# MobSF server (Docker)
docker pull opensecurity/mobile-security-framework-mobsf
docker run -it -p 8000:8000 opensecurity/mobile-security-framework-mobsf
```

## Authentication

MobSF uses API key authentication. The default key is shown on the MobSF dashboard:

```python
import requests
import os

MOBSF_URL = os.environ.get("MOBSF_URL", "http://localhost:8000")
MOBSF_KEY = os.environ["MOBSF_API_KEY"]
headers = {"Authorization": MOBSF_KEY}
```

## REST API v1 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/upload` | Upload APK, IPA, ZIP, or APPX for analysis |
| POST | `/api/v1/scan` | Trigger static analysis on uploaded file |
| GET | `/api/v1/report_json` | Get full JSON analysis report |
| POST | `/api/v1/download_pdf` | Download PDF report |
| GET | `/api/v1/scans` | List recent scans |
| POST | `/api/v1/delete_scan` | Delete a scan and its data |
| POST | `/api/v1/search` | Search scans by hash or filename |
| POST | `/api/v1/compare` | Compare two app scans |
| GET | `/api/v1/scorecard` | Get app security scorecard |
| GET | `/api/v1/scan_logs` | View live scan logs |

## Core Operations

### Upload an APK
```python
def upload_apk(file_path):
    with open(file_path, "rb") as f:
        resp = requests.post(
            f"{MOBSF_URL}/api/v1/upload",
            files={"file": (os.path.basename(file_path), f, "application/octet-stream")},
            headers=headers,
            timeout=120,
        )
    resp.raise_for_status()
    result = resp.json()
    return result["hash"], result["scan_type"], result["file_name"]
    # hash: SHA-256 of the uploaded file
    # scan_type: "apk", "ipa", "zip", "appx"
```

### Trigger Static Analysis
```python
def start_scan(file_hash, scan_type, file_name):
    resp = requests.post(
        f"{MOBSF_URL}/api/v1/scan",
        data={
            "hash": file_hash,
            "scan_type": scan_type,
            "file_name": file_name,
        },
        headers=headers,
        timeout=600,  # Scans can take several minutes
    )
    resp.raise_for_status()
    return resp.json()
```

### Retrieve JSON Report
```python
def get_report(file_hash):
    resp = requests.post(
        f"{MOBSF_URL}/api/v1/report_json",
        data={"hash": file_hash},
        headers=headers,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()
```

### Extract Key Findings
```python
def extract_findings(report):
    findings = {
        "security_score": report.get("security_score", "N/A"),
        "app_name": report.get("app_name"),
        "package_name": report.get("package_name"),
        "target_sdk": report.get("target_sdk"),
        "min_sdk": report.get("min_sdk"),
        "permissions": {
            "dangerous": [],
            "normal": [],
        },
        "manifest_issues": [],
        "code_issues": [],
        "binary_issues": [],
    }

    # Dangerous permissions
    for perm, details in report.get("permissions", {}).items():
        status = details.get("status", "normal")
        if status == "dangerous":
            findings["permissions"]["dangerous"].append(perm)
        else:
            findings["permissions"]["normal"].append(perm)

    # Manifest analysis
    for issue in report.get("manifest_analysis", []):
        if issue.get("severity") in ("high", "warning"):
            findings["manifest_issues"].append({
                "title": issue["title"],
                "severity": issue["severity"],
                "description": issue["description"],
            })

    # Code analysis
    for issue_key, issue_data in report.get("code_analysis", {}).items():
        findings["code_issues"].append({
            "rule": issue_key,
            "severity": issue_data.get("level"),
            "description": issue_data.get("description"),
            "files": issue_data.get("path", [])[:5],
        })

    return findings
```

### Download PDF Report
```python
def download_pdf(file_hash, output_path):
    resp = requests.post(
        f"{MOBSF_URL}/api/v1/download_pdf",
        data={"hash": file_hash},
        headers=headers,
        timeout=120,
    )
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(resp.content)
```

### Compare Two Applications
```python
resp = requests.post(
    f"{MOBSF_URL}/api/v1/compare",
    data={"hash1": hash_v1, "hash2": hash_v2},
    headers=headers,
    timeout=120,
)
comparison = resp.json()
# Shows permission changes, new vulnerabilities, code changes
```

## Output Format

```json
{
  "file_name": "app-debug.apk",
  "app_name": "TestApp",
  "package_name": "com.example.testapp",
  "security_score": 42,
  "target_sdk": "33",
  "min_sdk": "24",
  "permissions": {
    "android.permission.INTERNET": {"status": "normal", "description": "..."},
    "android.permission.READ_CONTACTS": {"status": "dangerous", "description": "..."}
  },
  "manifest_analysis": [
    {"title": "Application is debuggable", "severity": "high", "description": "..."}
  ],
  "code_analysis": {
    "android_insecure_random": {
      "level": "high",
      "description": "Insecure Random Number Generator",
      "path": ["com/example/CryptoUtils.java"]
    }
  },
  "binary_analysis": [
    {"title": "NX bit not set", "severity": "high"}
  ]
}
```

---

## Standards and Controls

## OWASP Mobile Top 10 2024 Mapping

| OWASP ID | Risk | MobSF Coverage |
|----------|------|----------------|
| M1 | Improper Credential Usage | Detects hardcoded API keys, passwords, tokens in source code and resources |
| M2 | Inadequate Supply Chain Security | Identifies third-party library versions with known CVEs |
| M5 | Insecure Communication | Flags missing certificate pinning, cleartext traffic, weak TLS |
| M7 | Insufficient Binary Protections | Checks ProGuard/R8 obfuscation, native binary protections |
| M8 | Security Misconfiguration | Analyzes AndroidManifest.xml for exported components, debug flags, backup settings |
| M9 | Insecure Data Storage | Detects SharedPreferences misuse, world-readable files, SQLite without encryption |
| M10 | Insufficient Cryptography | Identifies ECB mode, static IV, hardcoded encryption keys, weak algorithms |

## OWASP MASVS v2.0 Control Mapping

| MASVS Category | Controls | MobSF Static Checks |
|----------------|----------|---------------------|
| MASVS-STORAGE | Sensitive data storage | SharedPreferences analysis, file permission checks, database encryption |
| MASVS-CRYPTO | Cryptographic implementations | Algorithm strength, key management, IV randomness |
| MASVS-AUTH | Authentication mechanisms | Credential storage, biometric implementation review |
| MASVS-NETWORK | Network security | Network security config, certificate pinning, cleartext detection |
| MASVS-PLATFORM | Platform interaction | Intent filter analysis, content provider security, WebView configuration |
| MASVS-CODE | Code quality | Code obfuscation, debug symbols, error handling |
| MASVS-RESILIENCE | Reverse engineering resistance | Root detection, tamper detection, debugger detection |

## NIST SP 800-163 Rev 1: Vetting the Security of Mobile Applications

- Section 4.1: Static analysis as mandatory step in mobile app vetting process
- Section 4.2: Automated tools should check for known vulnerability patterns
- Section 5: Integration of vetting into enterprise mobile device management

## CWE Mappings for Common MobSF Findings

| CWE ID | Title | MobSF Finding Category |
|--------|-------|----------------------|
| CWE-312 | Cleartext Storage of Sensitive Information | Hardcoded credentials in source |
| CWE-319 | Cleartext Transmission of Sensitive Information | Missing HTTPS enforcement |
| CWE-327 | Use of Broken Cryptographic Algorithm | Weak crypto detection |
| CWE-330 | Use of Insufficiently Random Values | Static IV, predictable random |
| CWE-532 | Insertion of Sensitive Information into Log File | Logging sensitive data |
| CWE-749 | Exposed Dangerous Method or Function | Exported components without guards |
| CWE-919 | Weaknesses in Mobile Applications | General mobile-specific checks |
| CWE-925 | Improper Verification of Intent by Broadcast Receiver | Unprotected broadcast receivers |

---

## Workflows

## Workflow 1: Standalone APK Assessment

```
[Obtain APK] --> [Deploy MobSF Docker] --> [Upload via API] --> [Run Static Scan]
     |                                                               |
     v                                                               v
[Verify APK integrity]                                    [Review Manifest Analysis]
[Check signing certificate]                               [Review Code Analysis]
                                                          [Review Binary Analysis]
                                                          [Review Network Analysis]
                                                                     |
                                                                     v
                                                          [Triage HIGH/CRITICAL findings]
                                                          [Validate false positives]
                                                          [Generate PDF report]
```

## Workflow 2: CI/CD Pipeline Integration

```
[Developer pushes code] --> [Build APK] --> [Upload to MobSF] --> [Static Scan]
                                                                      |
                                                          +-----------+-----------+
                                                          |                       |
                                                   [Score >= 60]           [Score < 60]
                                                          |                       |
                                                   [Pass gate]            [Fail build]
                                                   [Archive report]       [Notify developer]
                                                   [Continue pipeline]    [Block deployment]
```

## Workflow 3: Third-Party App Vetting

```
[Receive third-party APK] --> [MobSF Static Scan] --> [Automated scoring]
                                                            |
                                                            v
                                                    [Manual review of:]
                                                    - Excessive permissions
                                                    - Data exfiltration indicators
                                                    - Known malware signatures
                                                    - C2 communication patterns
                                                            |
                                                            v
                                                    [Risk assessment report]
                                                    [Approve/Reject for enterprise use]
```

## Workflow 4: Comparative Analysis Across Versions

```
[APK v1.0] --> [MobSF Scan] --> [Baseline report]
                                       |
[APK v2.0] --> [MobSF Scan] --> [Compare findings] --> [New vulnerabilities introduced?]
                                       |                        |
                                       v                 [Yes: Block release]
                                [Regression report]      [No: Approve release]
```

## Decision Matrix: When to Escalate

| Finding Severity | MobSF Category | Action |
|-----------------|----------------|--------|
| CRITICAL | Hardcoded production API keys | Immediate key rotation, block release |
| HIGH | Exported activity with sensitive data | Manual verification, fix before release |
| MEDIUM | Missing certificate pinning | Add to sprint backlog, risk acceptance if internal app |
| LOW | Debug logging of non-sensitive data | Track in issue tracker, fix in next release |
| INFO | Missing ProGuard rules | Recommend but do not block |

---

## Working Template

## Engagement Information

| Field | Value |
|-------|-------|
| Application Name | [APP_NAME] |
| Package Name | [PACKAGE_NAME] |
| Version | [VERSION] |
| Target SDK | [TARGET_SDK] |
| Min SDK | [MIN_SDK] |
| File Hash (SHA256) | [HASH] |
| Analysis Date | [DATE] |
| Analyst | [ANALYST] |
| MobSF Version | [MOBSF_VERSION] |

## Executive Summary

**Security Score**: [SCORE]/100

**Overall Risk Rating**: [HIGH/MEDIUM/LOW]

[Brief narrative of key findings and overall security posture]

## Findings Summary

| Severity | Count | Categories |
|----------|-------|------------|
| Critical | [N] | [Categories] |
| High | [N] | [Categories] |
| Medium | [N] | [Categories] |
| Low | [N] | [Categories] |
| Info | [N] | [Categories] |

## Manifest Analysis

### Exported Components

| Component Type | Name | Permission Guard | Risk |
|---------------|------|-------------------|------|
| Activity | [NAME] | [PERMISSION/None] | [RISK] |
| Service | [NAME] | [PERMISSION/None] | [RISK] |
| Receiver | [NAME] | [PERMISSION/None] | [RISK] |
| Provider | [NAME] | [PERMISSION/None] | [RISK] |

### Permissions Requested

| Permission | Protection Level | Justification | Risk |
|-----------|-----------------|---------------|------|
| [PERMISSION] | [dangerous/normal/signature] | [JUSTIFICATION] | [RISK] |

### Manifest Flags

| Flag | Value | Expected | Status |
|------|-------|----------|--------|
| android:debuggable | [VALUE] | false | [PASS/FAIL] |
| android:allowBackup | [VALUE] | false | [PASS/FAIL] |
| android:usesCleartextTraffic | [VALUE] | false | [PASS/FAIL] |

## Code Analysis Findings

### Finding [N]: [TITLE]

- **Severity**: [CRITICAL/HIGH/MEDIUM/LOW]
- **CWE**: [CWE-ID]
- **OWASP Mobile**: [M1-M10]
- **MASVS**: [MASVS-CATEGORY]
- **Description**: [DESCRIPTION]
- **Affected Files**:
  - [FILE_PATH:LINE_NUMBER]
- **Evidence**: [CODE_SNIPPET]
- **Recommendation**: [REMEDIATION_STEPS]

## Network Security Analysis

| Check | Result | Details |
|-------|--------|---------|
| Certificate Pinning | [Present/Absent] | [DETAILS] |
| Network Security Config | [Present/Absent] | [DETAILS] |
| Cleartext Traffic | [Allowed/Blocked] | [DETAILS] |
| TLS Version | [VERSION] | [DETAILS] |

## Binary Analysis

| Check | Result | Details |
|-------|--------|---------|
| Code Obfuscation | [Yes/No] | [DETAILS] |
| Root Detection | [Present/Absent] | [DETAILS] |
| Debug Detection | [Present/Absent] | [DETAILS] |
| Emulator Detection | [Present/Absent] | [DETAILS] |
| Native Libraries (NX) | [Enabled/Disabled] | [DETAILS] |
| Native Libraries (PIE) | [Enabled/Disabled] | [DETAILS] |
| Native Libraries (Stack Canary) | [Present/Absent] | [DETAILS] |

## Recommendations

### Critical (Immediate Action Required)

1. [RECOMMENDATION]

### High (Fix Before Release)

1. [RECOMMENDATION]

### Medium (Address in Next Sprint)

1. [RECOMMENDATION]

### Low (Track in Backlog)

1. [RECOMMENDATION]

## OWASP Mobile Top 10 2024 Compliance

| ID | Risk | Status | Findings |
|----|------|--------|----------|
| M1 | Improper Credential Usage | [PASS/FAIL] | [DETAILS] |
| M2 | Inadequate Supply Chain Security | [PASS/FAIL] | [DETAILS] |
| M3 | Insecure Authentication/Authorization | [PASS/FAIL] | [DETAILS] |
| M4 | Insufficient Input/Output Validation | [PASS/FAIL] | [DETAILS] |
| M5 | Insecure Communication | [PASS/FAIL] | [DETAILS] |
| M6 | Inadequate Privacy Controls | [PASS/FAIL] | [DETAILS] |
| M7 | Insufficient Binary Protections | [PASS/FAIL] | [DETAILS] |
| M8 | Security Misconfiguration | [PASS/FAIL] | [DETAILS] |
| M9 | Insecure Data Storage | [PASS/FAIL] | [DETAILS] |
| M10 | Insufficient Cryptography | [PASS/FAIL] | [DETAILS] |
