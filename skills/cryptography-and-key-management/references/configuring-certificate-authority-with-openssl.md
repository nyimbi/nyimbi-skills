# Configuring Certificate Authority With Openssl

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| cryptography | `pip install cryptography` | X.509 certificate generation, parsing, and validation |
| pyOpenSSL | `pip install pyOpenSSL` | OpenSSL wrapper for certificate operations |

## Key cryptography Methods

| Method | Description |
|--------|-------------|
| `x509.CertificateBuilder()` | Build X.509 certificates |
| `rsa.generate_private_key(65537, key_size)` | Generate RSA private key |
| `x509.load_pem_x509_certificate(data)` | Parse PEM certificate |
| `cert.subject.rfc4514_string()` | Get subject as RFC 4514 string |
| `x509.random_serial_number()` | Generate unique serial number |

## OpenSSL CLI Commands

| Command | Purpose |
|---------|---------|
| `openssl req -x509 -newkey rsa:4096 -sha256 -days 3650` | Create self-signed CA |
| `openssl req -new -key server.key -out server.csr` | Generate CSR |
| `openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key` | Sign certificate |
| `openssl verify -CAfile ca.crt server.crt` | Verify certificate chain |
| `openssl x509 -in cert.pem -text -noout` | Display certificate details |

## Certificate Best Practices

| Parameter | Recommended Value |
|-----------|-------------------|
| Root CA Key Size | RSA 4096 or EC P-384 |
| Server Key Size | RSA 2048+ or EC P-256 |
| Signature Algorithm | SHA-256 or SHA-384 |
| Root CA Validity | 10-20 years |
| Server Cert Validity | 1 year (398 days max for public) |

## External References

- [cryptography.io X.509 Docs](https://cryptography.io/en/latest/x509/)
- [OpenSSL Cookbook](https://www.feistyduck.com/library/openssl-cookbook/)
- [RFC 5280 X.509 PKI](https://datatracker.ietf.org/doc/html/rfc5280)

---

## Standards and Controls

## Primary Standards

### RFC 5280 - Internet X.509 PKI Certificate and CRL Profile
- **URL**: https://www.rfc-editor.org/rfc/rfc5280
- **Description**: Core X.509v3 certificate and CRL format specification

### RFC 6960 - X.509 OCSP
- **URL**: https://www.rfc-editor.org/rfc/rfc6960
- **Description**: Online Certificate Status Protocol

### RFC 3647 - Internet X.509 PKI Certificate Policy and Certification Practices Framework
- **URL**: https://www.rfc-editor.org/rfc/rfc3647
- **Description**: Framework for CP and CPS documents

### NIST SP 800-57 Part 1 Rev. 5
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final
- **Description**: Key management recommendations

### CA/Browser Forum Baseline Requirements
- **URL**: https://cabforum.org/baseline-requirements/
- **Description**: Requirements for publicly trusted CAs

## Tools

### OpenSSL
- **URL**: https://www.openssl.org/
- **Docs**: https://www.openssl.org/docs/man3.0/man1/

### Python cryptography library
- **URL**: https://cryptography.io/en/latest/x509/
- **Description**: X.509 certificate generation and parsing

---

## Workflows

## Workflow 1: Build Two-Tier CA Hierarchy

```
[Generate Root CA Key] (RSA 4096 / ECDSA P-384)
      |
[Create Root CA Self-Signed Certificate]
(validity: 20 years, basicConstraints: CA:TRUE)
      |
[Store Root CA Key Offline]
      |
[Generate Intermediate CA Key]
      |
[Create Intermediate CA CSR]
      |
[Sign Intermediate CSR with Root CA]
(pathLenConstraint: 0, keyUsage: keyCertSign, cRLSign)
      |
[Create CA Chain Bundle]
(intermediate.crt + root.crt)
```

## Workflow 2: Issue End-Entity Certificate

```
[Applicant Generates Key + CSR]
      |
[Submit CSR to Intermediate CA]
      |
[Validate CSR]
(check subject, SAN, key strength)
      |
[Sign with Intermediate CA Key]
(basicConstraints: CA:FALSE)
(extendedKeyUsage: serverAuth / clientAuth)
      |
[Issue Certificate]
      |
[Record in Certificate Database]
```

## Workflow 3: Certificate Revocation

```
[Revocation Request]
      |
[Verify Authorization]
      |
[Revoke Certificate]
(record serial number + reason + date)
      |
[Generate Updated CRL]
(sign with CA key, set nextUpdate)
      |
[Publish CRL to Distribution Point]
      |
[Update OCSP Responder Database]
```

## Workflow 4: OpenSSL CA Commands

```bash
# 1. Create CA directory structure
mkdir -p ca/{certs,crl,newcerts,private}
touch ca/index.txt
echo 1000 > ca/serial
echo 1000 > ca/crlnumber

# 2. Generate Root CA
openssl genrsa -aes256 -out ca/private/ca.key 4096
openssl req -config ca/openssl.cnf -key ca/private/ca.key \
    -new -x509 -days 7300 -sha256 -extensions v3_ca -out ca/certs/ca.crt

# 3. Generate Intermediate CA
openssl genrsa -aes256 -out intermediate/private/intermediate.key 4096
openssl req -config intermediate/openssl.cnf \
    -key intermediate/private/intermediate.key -new -sha256 -out intermediate/csr/intermediate.csr
openssl ca -config ca/openssl.cnf -extensions v3_intermediate_ca \
    -days 3650 -notext -md sha256 -in intermediate/csr/intermediate.csr \
    -out intermediate/certs/intermediate.crt

# 4. Issue server certificate
openssl req -config intermediate/openssl.cnf \
    -key server.key -new -sha256 -out server.csr
openssl ca -config intermediate/openssl.cnf -extensions server_cert \
    -days 365 -notext -md sha256 -in server.csr -out server.crt
```

---

## Working Template

## CA Directory Structure

```
pki/
  root-ca/
    private/root-ca.key
    certs/root-ca.crt
    serial.json
    index.json
  intermediate-ca/
    private/intermediate-ca.key
    certs/intermediate-ca.crt
    certs/ca-chain.crt
    certs/issued/
    crl/intermediate.crl
    serial.json
    index.json
```

## OpenSSL Configuration Template (openssl.cnf)

```ini
[ca]
default_ca = CA_default

[CA_default]
dir               = ./ca
certs             = $dir/certs
new_certs_dir     = $dir/newcerts
database          = $dir/index.txt
serial            = $dir/serial
private_key       = $dir/private/ca.key
certificate       = $dir/certs/ca.crt
default_md        = sha256
default_days      = 365
policy            = policy_strict

[policy_strict]
countryName       = match
organizationName  = match
commonName        = supplied

[v3_ca]
basicConstraints = critical, CA:true
keyUsage = critical, keyCertSign, cRLSign
subjectKeyIdentifier = hash

[v3_intermediate_ca]
basicConstraints = critical, CA:true, pathlen:0
keyUsage = critical, keyCertSign, cRLSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always

[server_cert]
basicConstraints = CA:FALSE
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always
```

## Certificate Issuance Checklist

- [ ] Verify CSR subject and SAN entries
- [ ] Validate key strength (minimum 2048-bit RSA or P-256 ECDSA)
- [ ] Check domain ownership or authorization
- [ ] Set appropriate validity period
- [ ] Include correct extensions (EKU, constraints)
- [ ] Sign with intermediate CA (never root)
- [ ] Record in certificate database
- [ ] Provide full chain to requester
