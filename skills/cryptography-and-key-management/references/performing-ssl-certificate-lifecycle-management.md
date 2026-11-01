# Performing Ssl Certificate Lifecycle Management

## API Reference

## cryptography Library - CSR Generation

| Class / Method | Description |
|----------------|-------------|
| `ec.generate_private_key(ec.SECP256R1())` | Generate ECDSA P-256 private key |
| `rsa.generate_private_key(65537, 2048)` | Generate RSA 2048-bit private key |
| `x509.CertificateSigningRequestBuilder()` | Build a PKCS#10 CSR |
| `.subject_name(x509.Name([...]))` | Set CSR subject |
| `.add_extension(SubjectAlternativeName(...))` | Add SAN extension |
| `.sign(private_key, hashes.SHA256())` | Sign CSR with private key |

## cryptography Library - Certificate Parsing

| Method | Description |
|--------|-------------|
| `x509.load_pem_x509_certificate(data)` | Parse PEM certificate |
| `x509.load_der_x509_certificate(data)` | Parse DER certificate |
| `cert.subject` | Get subject Distinguished Name |
| `cert.issuer` | Get issuer Distinguished Name |
| `cert.not_valid_after_utc` | Expiration datetime |
| `cert.serial_number` | Certificate serial number |
| `cert.extensions.get_extension_for_oid(OID)` | Get specific extension |

## Python ssl Module

| Function | Description |
|----------|-------------|
| `ssl.create_default_context()` | Create SSL context with system CAs |
| `ctx.wrap_socket(sock, server_hostname=host)` | TLS handshake |
| `s.getpeercert(binary_form=True)` | Get DER-encoded server certificate |
| `s.getpeercert()` | Get parsed certificate dict |

## Certificate Types

| Type | Validation | Typical Use |
|------|-----------|-------------|
| DV | Domain ownership | Websites, APIs |
| OV | Organization verified | Business applications |
| EV | Full legal verification | E-commerce, banking |
| Wildcard | `*.domain.com` | Multi-subdomain |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `cryptography` | >=41.0 | CSR generation, certificate parsing |
| `ssl` | stdlib | TLS handshake, remote cert fetch |
| `socket` | stdlib | TCP connections |

## References

- cryptography docs: https://cryptography.io/en/latest/x509/
- Let's Encrypt ACME: https://letsencrypt.org/docs/
- OCSP Stapling: https://datatracker.ietf.org/doc/html/rfc6960
- Certificate Transparency: https://certificate.transparency.dev/

---

## Standards and Controls

## Primary Standards

### RFC 5280 - Internet X.509 PKI Certificate and CRL Profile
- **URL**: https://www.rfc-editor.org/rfc/rfc5280
- **Description**: Core X.509 certificate format and Certificate Revocation List (CRL)

### RFC 6960 - X.509 Online Certificate Status Protocol (OCSP)
- **URL**: https://www.rfc-editor.org/rfc/rfc6960
- **Description**: Real-time certificate revocation checking

### RFC 8555 - Automatic Certificate Management Environment (ACME)
- **URL**: https://www.rfc-editor.org/rfc/rfc8555
- **Description**: Protocol for automating certificate issuance (Let's Encrypt)

### RFC 6962 - Certificate Transparency
- **URL**: https://www.rfc-editor.org/rfc/rfc6962
- **Description**: Public logging framework for TLS certificates

### RFC 2986 - PKCS #10: Certification Request Syntax
- **URL**: https://www.rfc-editor.org/rfc/rfc2986
- **Description**: CSR format specification

### NIST SP 800-57 Part 3 - Application-Specific Key Management
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-57-part-3/rev-1/final
- **Description**: Key management guidance for TLS certificates

## Tools

### Let's Encrypt / Certbot
- **URL**: https://letsencrypt.org/
- **Certbot**: https://certbot.eff.org/
- **Rate limits**: 50 certificates per domain per week

### Certificate Transparency Logs
- **Google**: https://ct.googleapis.com/logs
- **crt.sh**: https://crt.sh/ (certificate search)

### Mozilla Observatory
- **URL**: https://observatory.mozilla.org/
- **Description**: Web security scanning including TLS configuration

---

## Workflows

## Workflow 1: Certificate Request and Issuance

```
[Generate Private Key] (ECDSA P-256 or RSA 4096)
      |
[Create CSR] (PKCS#10)
(CN, SAN, Organization, etc.)
      |
[Submit CSR to CA]
      |
[CA Validates Domain/Org]
(DNS, HTTP, or Email challenge)
      |
[CA Issues Certificate]
      |
[Download Certificate + Chain]
      |
[Verify Certificate Chain]
      |
[Deploy to Server]
```

## Workflow 2: Expiration Monitoring

```
[Certificate Inventory] (list of all domains/endpoints)
      |
[For Each Endpoint]:
  [Connect and retrieve certificate]
  [Parse notAfter field]
  [Calculate days remaining]
      |
[Apply Threshold Rules]:
  > 30 days: OK
  15-30 days: WARNING
  < 15 days: CRITICAL
  Expired: ALERT
      |
[Generate Report / Send Alerts]
```

## Workflow 3: Automated Renewal (ACME)

```
[Cron Job / Scheduler]
      |
[Check Certificate Expiry]
      |
[< 30 days remaining?]
  NO  --> Sleep
  YES --> [Initiate ACME Renewal]
              |
          [Complete Challenge]
          (HTTP-01, DNS-01, TLS-ALPN-01)
              |
          [Receive New Certificate]
              |
          [Deploy and Reload Server]
              |
          [Verify New Certificate Works]
```

## Workflow 4: Certificate Revocation

```
[Security Incident Detected]
(key compromise, CA breach, etc.)
      |
[Revoke Certificate with CA]
(provide reason code)
      |
[Verify in CRL / OCSP]
      |
[Issue Replacement Certificate]
      |
[Deploy Replacement]
      |
[Update Certificate Inventory]
```

---

## Working Template

## Certificate Inventory Template

| Domain | Type | CA | Issued | Expires | Days Left | Status |
|--------|------|-----|--------|---------|-----------|--------|
| example.com | DV | Let's Encrypt | 2024-01-01 | 2024-04-01 | 90 | OK |
| api.example.com | DV | DigiCert | 2024-01-01 | 2025-01-01 | 365 | OK |

## Monitoring Thresholds

```yaml
monitoring:
  ok_threshold: 30        # days
  warning_threshold: 15   # days
  critical_threshold: 7   # days
  check_interval: 86400   # seconds (daily)
  notification:
    email: security@example.com
    slack: "#cert-alerts"
```

## CSR Generation Command

```bash
# ECDSA (recommended)
openssl ecparam -genkey -name prime256v1 -out server.key
openssl req -new -key server.key -out server.csr -subj "/CN=example.com"

# RSA 4096
openssl genrsa -out server.key 4096
openssl req -new -key server.key -out server.csr -subj "/CN=example.com"
```

## Renewal Automation (certbot)

```bash
# Initial issuance
certbot certonly --nginx -d example.com -d www.example.com

# Auto-renewal (cron)
0 0 * * * certbot renew --quiet --deploy-hook "systemctl reload nginx"
```

## Revocation Checklist

- [ ] Identify affected certificate(s)
- [ ] Contact CA to initiate revocation
- [ ] Provide revocation reason (key compromise, cessation, etc.)
- [ ] Verify revocation in CRL/OCSP
- [ ] Issue replacement certificate
- [ ] Deploy replacement to all affected servers
- [ ] Update certificate inventory
- [ ] Document incident
