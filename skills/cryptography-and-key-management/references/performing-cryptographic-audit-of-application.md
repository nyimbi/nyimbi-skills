# Performing Cryptographic Audit Of Application

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `ssl` | TLS connection inspection and cipher suite enumeration |
| `socket` | TCP connections for TLS handshake testing |
| `cryptography` | Certificate parsing, key strength analysis |
| `json` | Structure audit findings |
| `datetime` | Check certificate validity periods |

## Installation

```bash
pip install cryptography
```

## TLS Configuration Audit

### Check TLS Version and Cipher Suite
```python
import ssl
import socket

def check_tls_config(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port), timeout=10) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            return {
                "hostname": hostname,
                "protocol": ssock.version(),
                "cipher": ssock.cipher()[0],
                "cipher_bits": ssock.cipher()[2],
                "compression": ssock.compression(),
            }
```

### Test for Weak TLS Versions
```python
WEAK_PROTOCOLS = {
    ssl.PROTOCOL_TLSv1: "TLSv1.0",
    ssl.PROTOCOL_TLSv1_1: "TLSv1.1",
}

def test_weak_tls(hostname, port=443):
    findings = []
    for protocol_const, name in WEAK_PROTOCOLS.items():
        try:
            ctx = ssl.SSLContext(protocol_const)
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with ctx.wrap_socket(sock) as ssock:
                    findings.append({
                        "protocol": name,
                        "supported": True,
                        "severity": "high",
                        "issue": f"{name} is supported — deprecated and insecure",
                    })
        except (ssl.SSLError, ConnectionRefusedError, OSError):
            findings.append({"protocol": name, "supported": False})
    return findings
```

### Enumerate Supported Cipher Suites
```python
WEAK_CIPHERS = {
    "RC4", "DES", "3DES", "MD5", "NULL", "EXPORT", "anon", "CBC",
}

def check_cipher_suites(hostname, port=443):
    context = ssl.create_default_context()
    context.set_ciphers("ALL:COMPLEMENTOFALL")
    findings = []
    try:
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cipher_name, protocol, bits = ssock.cipher()
                is_weak = any(w in cipher_name for w in WEAK_CIPHERS)
                findings.append({
                    "cipher": cipher_name,
                    "bits": bits,
                    "weak": is_weak,
                    "severity": "high" if is_weak else "pass",
                })
    except ssl.SSLError as e:
        findings.append({"error": str(e)})
    return findings
```

## Certificate Analysis

### Parse and Audit Certificate
```python
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from datetime import datetime, timezone

def audit_certificate(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port), timeout=10) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            der_cert = ssock.getpeercert(binary_form=True)

    cert = x509.load_der_x509_certificate(der_cert)
    pub_key = cert.public_key()

    findings = []
    # Key strength check
    if isinstance(pub_key, rsa.RSAPublicKey):
        key_size = pub_key.key_size
        if key_size < 2048:
            findings.append({
                "check": "key_size",
                "severity": "critical",
                "detail": f"RSA key {key_size} bits — minimum 2048 required",
            })
    elif isinstance(pub_key, ec.EllipticCurvePublicKey):
        key_size = pub_key.curve.key_size
        if key_size < 256:
            findings.append({
                "check": "key_size",
                "severity": "high",
                "detail": f"EC key {key_size} bits — minimum 256 required",
            })

    # Signature algorithm
    sig_algo = cert.signature_algorithm_oid._name
    if "sha1" in sig_algo.lower():
        findings.append({
            "check": "signature_algorithm",
            "severity": "high",
            "detail": f"SHA-1 signature ({sig_algo}) — deprecated",
        })

    # Validity period
    now = datetime.now(timezone.utc)
    days_remaining = (cert.not_valid_after_utc - now).days
    if days_remaining < 0:
        findings.append({"check": "expiry", "severity": "critical", "detail": "Certificate expired"})
    elif days_remaining < 30:
        findings.append({"check": "expiry", "severity": "warning", "detail": f"Expires in {days_remaining} days"})

    return {
        "subject": cert.subject.rfc4514_string(),
        "issuer": cert.issuer.rfc4514_string(),
        "not_before": cert.not_valid_before_utc.isoformat(),
        "not_after": cert.not_valid_after_utc.isoformat(),
        "days_remaining": days_remaining,
        "serial_number": hex(cert.serial_number),
        "signature_algorithm": sig_algo,
        "key_type": "RSA" if isinstance(pub_key, rsa.RSAPublicKey) else "EC",
        "key_size": key_size,
        "findings": findings,
    }
```

### Check HSTS Header
```python
import requests

def check_hsts(url):
    resp = requests.get(url, timeout=10, allow_redirects=True)
    hsts = resp.headers.get("Strict-Transport-Security", "")
    findings = []
    if not hsts:
        findings.append({"check": "hsts", "severity": "medium", "detail": "HSTS header missing"})
    else:
        if "includeSubDomains" not in hsts:
            findings.append({"check": "hsts", "severity": "low", "detail": "HSTS missing includeSubDomains"})
        max_age = 0
        for part in hsts.split(";"):
            if "max-age" in part:
                max_age = int(part.split("=")[1].strip())
        if max_age < 31536000:
            findings.append({"check": "hsts_max_age", "severity": "low", "detail": f"max-age {max_age} < 1 year"})

    return {"hsts_header": hsts, "findings": findings}
```

## Output Format

```json
{
  "hostname": "example.com",
  "tls_version": "TLSv1.3",
  "cipher": "TLS_AES_256_GCM_SHA384",
  "certificate": {
    "subject": "CN=example.com",
    "issuer": "CN=R3,O=Let's Encrypt",
    "days_remaining": 62,
    "key_type": "EC",
    "key_size": 256
  },
  "weak_tls_supported": ["TLSv1.0"],
  "hsts_enabled": true,
  "findings": [
    {
      "check": "weak_tls",
      "severity": "high",
      "detail": "TLSv1.0 is supported — deprecated and insecure"
    }
  ]
}
```

---

## Standards and Controls

## NIST Guidelines

### NIST SP 800-131A Rev. 2 - Transitioning Cryptographic Algorithms
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-131a/rev-2/final
- **Description**: Defines deprecated, legacy, and acceptable algorithms

### NIST SP 800-57 Part 1 Rev. 5 - Key Management
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final
- **Description**: Minimum key sizes and algorithm recommendations

## OWASP References

### OWASP Cryptographic Failures
- **URL**: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- **Description**: OWASP Top 10 #2 - Cryptographic Failures

### OWASP Cheat Sheet - Cryptographic Storage
- **URL**: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
- **Description**: Guidelines for secure cryptographic storage

### OWASP Cheat Sheet - Password Storage
- **URL**: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- **Description**: Password hashing best practices

## Tools

### Bandit
- **URL**: https://bandit.readthedocs.io/
- **Description**: Python security linter with crypto checks

### Semgrep
- **URL**: https://semgrep.dev/
- **Crypto rules**: https://semgrep.dev/r?q=crypto
- **Description**: Static analysis with crypto-specific rules

### CryptoGuard
- **URL**: https://github.com/AkshayaVS/CryptoGuard
- **Description**: Specialized cryptographic misuse detector

---

## Workflows

## Workflow 1: Automated Source Code Scan

```
[Target Application Source]
      |
[Scan for Crypto Patterns]:
  - Deprecated algorithms (MD5, SHA-1, DES, RC4)
  - Insecure modes (ECB)
  - Hardcoded secrets (keys, passwords, tokens)
  - Weak KDF parameters
  - Insecure random number generation
      |
[Scan Configuration Files]:
  - TLS/SSL settings
  - Cipher suite configurations
  - Certificate paths and validity
      |
[Generate Findings with Severity]
      |
[Produce Audit Report]
```

## Workflow 2: Manual Crypto Review

```
[Identify All Crypto Touchpoints]:
  - Encryption/decryption operations
  - Hashing operations
  - Key generation and storage
  - TLS/SSL connections
  - Token generation (JWT, API keys)
  - Password handling
      |
[For Each Touchpoint]:
  [Verify algorithm choice]
  [Verify mode/padding]
  [Verify key management]
  [Verify entropy sources]
  [Verify error handling]
      |
[Document Findings]
```

## Workflow 3: Remediation Prioritization

```
[All Findings]
      |
[Classify by Severity]:
  CRITICAL: Hardcoded keys, broken encryption
  HIGH: Weak algorithms, ECB mode, weak KDF
  MEDIUM: Short key sizes, deprecated protocols
  LOW: Missing best practices, informational
      |
[Prioritize by Risk]:
  1. CRITICAL findings (immediate fix)
  2. HIGH findings (fix in current sprint)
  3. MEDIUM findings (plan for next release)
  4. LOW findings (backlog)
```

---

## Working Template

## Executive Summary

| Metric | Value |
|--------|-------|
| Target | [Application Name] |
| Scan Date | [Date] |
| Overall Risk | [CRITICAL/HIGH/MEDIUM/LOW] |
| Total Findings | [Count] |
| Critical | [Count] |
| High | [Count] |
| Medium | [Count] |
| Low | [Count] |

## Audit Scope

- [ ] Source code review (Python, JavaScript, Java, Go)
- [ ] Configuration file review (YAML, JSON, INI)
- [ ] TLS/SSL configuration assessment
- [ ] Key management practices review
- [ ] Dependency vulnerability check
- [ ] Deployed infrastructure scan

## Approved Algorithms

| Purpose | Approved | Deprecated |
|---------|----------|-----------|
| Hashing (integrity) | SHA-256, SHA-3 | MD5, SHA-1 |
| Password hashing | Argon2id, bcrypt, scrypt | MD5, SHA-1, plain SHA-256 |
| Symmetric encryption | AES-256-GCM, ChaCha20-Poly1305 | DES, 3DES, RC4, Blowfish |
| Asymmetric encryption | RSA-OAEP (3072+), ECIES | RSA-PKCS1v15 |
| Digital signatures | Ed25519, RSA-PSS (3072+), ECDSA (P-256+) | RSA-PKCS1v15 |
| Key exchange | X25519, ECDH (P-256+), DH (3072+) | DH (1024) |
| TLS | TLS 1.2 (approved ciphers), TLS 1.3 | SSLv3, TLS 1.0, TLS 1.1 |

## Finding Template

```
### Finding F-001: [Title]

**Severity**: CRITICAL / HIGH / MEDIUM / LOW
**Category**: [Category]
**CWE**: [CWE-XXX]
**File**: [file_path:line_number]

**Description**:
[Description of the vulnerability]

**Code**:
[Code snippet]

**Remediation**:
[Steps to fix]

**References**:
- [NIST/OWASP reference]
```

## Remediation Priority

1. CRITICAL: Hardcoded secrets, broken encryption (fix immediately)
2. HIGH: Weak algorithms, insecure modes (fix in current sprint)
3. MEDIUM: Suboptimal parameters, deprecated protocols (next release)
4. LOW: Informational, best practice improvements (backlog)
