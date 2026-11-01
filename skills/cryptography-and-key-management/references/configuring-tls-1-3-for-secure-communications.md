# Configuring TLS 1.3 For Secure Communications

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| cryptography | `pip install cryptography` | X.509 certificate parsing |
| ssl | stdlib | TLS connection testing |
| sslyze | `pip install sslyze` | Comprehensive TLS/SSL scanner |

## Python ssl Module Methods

| Method | Description |
|--------|-------------|
| `ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)` | Create TLS client context |
| `ctx.minimum_version = ssl.TLSVersion.TLSv1_3` | Set minimum TLS version |
| `ctx.wrap_socket(sock, server_hostname=)` | Wrap socket with TLS |
| `ssock.cipher()` | Get negotiated cipher tuple |
| `ssock.getpeercert(binary_form=True)` | Get server certificate DER bytes |

## TLS 1.3 Cipher Suites

| Cipher Suite | Security |
|-------------|----------|
| TLS_AES_256_GCM_SHA384 | Recommended |
| TLS_AES_128_GCM_SHA256 | Recommended |
| TLS_CHACHA20_POLY1305_SHA256 | Recommended (mobile) |

## Deprecated Versions

| Version | Status | Risk |
|---------|--------|------|
| SSL 3.0 | Deprecated (RFC 7568) | POODLE attack |
| TLS 1.0 | Deprecated (RFC 8996) | BEAST, CRIME |
| TLS 1.1 | Deprecated (RFC 8996) | Weak ciphers |

## External References

- [RFC 8446 TLS 1.3](https://datatracker.ietf.org/doc/html/rfc8446)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [sslyze Documentation](https://nabla-c0d3.github.io/sslyze/documentation/)
- [cryptography.io Docs](https://cryptography.io/)

---

## Standards and Controls

## Primary Standards

### RFC 8446 - The Transport Layer Security (TLS) Protocol Version 1.3
- **URL**: https://www.rfc-editor.org/rfc/rfc8446
- **Description**: The core TLS 1.3 specification
- **Key changes**: 1-RTT handshake, mandatory PFS, removed RSA key transport, encrypted handshake messages

### RFC 8447 - IANA Registry Updates for TLS and DTLS
- **URL**: https://www.rfc-editor.org/rfc/rfc8447
- **Description**: Updates IANA registries for TLS cipher suites and extensions

### RFC 8449 - Record Size Limit Extension for TLS
- **URL**: https://www.rfc-editor.org/rfc/rfc8449
- **Description**: Allows endpoints to negotiate maximum record size

### RFC 8470 - Using Early Data in HTTP (0-RTT)
- **URL**: https://www.rfc-editor.org/rfc/rfc8470
- **Description**: Defines how 0-RTT early data works with HTTP, including replay protections

### RFC 6961 - TLS Multiple Certificate Status Extension (OCSP Stapling)
- **URL**: https://www.rfc-editor.org/rfc/rfc6961
- **Description**: Allows servers to provide OCSP responses during handshake

### RFC 6797 - HTTP Strict Transport Security (HSTS)
- **URL**: https://www.rfc-editor.org/rfc/rfc6797
- **Description**: Forces browsers to use HTTPS for all connections

## NIST Guidelines

### NIST SP 800-52 Rev. 2 - Guidelines for TLS Implementations
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-52/rev-2/final
- **Description**: Federal guidelines for TLS deployment
- **TLS 1.3**: Recommended for all new deployments
- **TLS 1.2**: Acceptable with approved cipher suites
- **TLS 1.0/1.1**: Prohibited

### NIST SP 800-57 Part 3 Rev. 1 - Application-Specific Key Management
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-57-part-3/rev-1/final
- **Description**: Key management guidance for TLS

## Testing Tools

### testssl.sh
- **URL**: https://testssl.sh/
- **GitHub**: https://github.com/drwetter/testssl.sh
- **Description**: Command-line tool for checking TLS/SSL configurations

### SSL Labs Server Test
- **URL**: https://www.ssllabs.com/ssltest/
- **Description**: Online TLS configuration analyzer (Qualys)

### Mozilla SSL Configuration Generator
- **URL**: https://ssl-config.mozilla.org/
- **Description**: Generate recommended TLS configurations for various servers

## Compliance

### PCI DSS v4.0
- TLS 1.0 and early TLS prohibited since June 2018
- TLS 1.2+ required; TLS 1.3 recommended
- Strong cipher suites must be configured

### HIPAA
- Encryption in transit required for ePHI
- TLS 1.2+ satisfies the requirement

---

## Workflows

## Workflow 1: TLS 1.3 Handshake (1-RTT)

```
Client                              Server
  |                                    |
  |--- ClientHello ------------------>|
  |    (supported_versions: TLS 1.3)  |
  |    (key_share: x25519)            |
  |    (signature_algorithms)         |
  |    (cipher_suites)                |
  |                                    |
  |<-- ServerHello -------------------|
  |    (selected cipher suite)        |
  |    (key_share: x25519)            |
  |<-- {EncryptedExtensions} ---------|
  |<-- {Certificate} -----------------|
  |<-- {CertificateVerify} -----------|
  |<-- {Finished} --------------------|
  |                                    |
  |--- {Finished} ------------------->|
  |                                    |
  |<== Application Data ==============>|
```

## Workflow 2: nginx TLS 1.3 Configuration

```
1. Check OpenSSL version (>= 1.1.1)
   $ openssl version

2. Generate ECDSA certificate
   $ openssl ecparam -genkey -name prime256v1 -out server.key
   $ openssl req -new -x509 -key server.key -out server.crt -days 365

3. Configure nginx
   Edit /etc/nginx/nginx.conf

4. Test configuration
   $ nginx -t

5. Reload nginx
   $ systemctl reload nginx

6. Verify TLS 1.3
   $ openssl s_client -connect localhost:443 -tls1_3
```

## Workflow 3: TLS Configuration Validation

```
[Server] --> [openssl s_client test]
                  |
          [Check protocol version]
          [Check cipher suite]
          [Check certificate chain]
                  |
          [testssl.sh full scan]
                  |
          [Check for vulnerabilities]
          - BEAST, POODLE, Heartbleed
          - ROBOT, DROWN, FREAK
          - Weak ciphers, expired certs
                  |
          [SSL Labs grade assessment]
          Target: A+ rating
```

## Workflow 4: Certificate Lifecycle

```
[Generate Key Pair]
      |
[Create CSR] --> [Submit to CA]
                       |
               [CA Issues Certificate]
                       |
               [Install Certificate]
                       |
               [Configure OCSP Stapling]
                       |
               [Set Up Auto-Renewal]
               (certbot / ACME)
                       |
               [Monitor Expiration]
```

---

## Working Template

## Pre-Configuration Checklist

- [ ] Verify OpenSSL version >= 1.1.1 (`openssl version`)
- [ ] Obtain valid TLS certificate from trusted CA
- [ ] Identify all server endpoints requiring TLS
- [ ] Determine minimum TLS version (1.2 or 1.3 only)
- [ ] Plan certificate renewal automation (Let's Encrypt / ACME)
- [ ] Review compliance requirements (PCI-DSS, HIPAA)

## nginx Configuration Template

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
ssl_prefer_server_ciphers off;
ssl_ecdh_curve X25519:secp256r1:secp384r1;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

## Python TLS 1.3 Client Template

```python
import ssl
import socket

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.minimum_version = ssl.TLSVersion.TLSv1_3
context.load_default_certs()

with socket.create_connection(("example.com", 443)) as sock:
    with context.wrap_socket(sock, server_hostname="example.com") as tls:
        print(f"Protocol: {tls.version()}")
        print(f"Cipher: {tls.cipher()}")
```

## Validation Commands

```bash
# Test TLS 1.3 support
openssl s_client -connect example.com:443 -tls1_3

# Show full certificate chain
openssl s_client -connect example.com:443 -showcerts

# List supported cipher suites
openssl s_client -connect example.com:443 -cipher 'ALL' -tls1_3

# Test with testssl.sh
./testssl.sh --protocols --ciphers --headers example.com
```

## Security Headers Checklist

| Header | Value | Purpose |
|--------|-------|---------|
| Strict-Transport-Security | max-age=63072000; includeSubDomains; preload | Force HTTPS |
| X-Content-Type-Options | nosniff | Prevent MIME sniffing |
| X-Frame-Options | DENY | Prevent clickjacking |
| Content-Security-Policy | default-src 'self' | Prevent XSS |
| Referrer-Policy | strict-origin-when-cross-origin | Limit referrer leakage |
