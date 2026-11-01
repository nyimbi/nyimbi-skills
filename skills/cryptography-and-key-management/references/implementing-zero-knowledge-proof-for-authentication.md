# Implementing Zero Knowledge Proof For Authentication

## API Reference

## hashlib (Python Standard Library)

### PBKDF2 Key Derivation
```python
import hashlib
key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), iterations)
```

### SHA-256 Hashing (Fiat-Shamir Heuristic)
```python
challenge = int(hashlib.sha256(data.encode()).hexdigest(), 16) % prime
```

## secrets (Python Standard Library)

| Function | Description |
|----------|-------------|
| `secrets.randbelow(n)` | Cryptographically secure random int in [0, n) |
| `secrets.token_hex(n)` | Random hex string of n bytes |
| `secrets.token_bytes(n)` | Random bytes of length n |

## Schnorr Protocol Steps

| Step | Prover | Verifier |
|------|--------|----------|
| Setup | Private key x, public key y=g^x mod p | Knows g, p, y |
| Commit | Pick random k, send r=g^k mod p | Receive r |
| Challenge | - | Send random c |
| Response | Send s = k - c*x mod (p-1) | Check g^s * y^c == r mod p |

## Fiat-Shamir Heuristic (Non-Interactive)
```
c = H(g || r || y)   # Challenge derived from hash
s = k - c * x mod (p-1)
```

## ZKP Properties
| Property | Guarantee |
|----------|-----------|
| Completeness | Honest prover always convinces verifier |
| Soundness | Dishonest prover fails with high probability |
| Zero-Knowledge | Verifier learns nothing beyond validity |

## References
- Schnorr Protocol: https://en.wikipedia.org/wiki/Schnorr_identification
- RFC 8235 (Schnorr NIZK): https://www.rfc-editor.org/rfc/rfc8235
- hashlib docs: https://docs.python.org/3/library/hashlib.html
- secrets docs: https://docs.python.org/3/library/secrets.html

---

## Standards and Controls

## Academic References

### Schnorr Identification Protocol
- **Paper**: "Efficient Signature Generation by Smart Cards" (Claus-Peter Schnorr, 1989)
- **Standard**: ISO/IEC 9798-5 (Entity authentication using zero-knowledge techniques)

### Fiat-Shamir Heuristic
- **Paper**: "How To Prove Yourself" (Fiat, Shamir, 1986)
- **Description**: Converts interactive ZKP to non-interactive using hash function

### RFC 8235 - Schnorr Non-Interactive Zero-Knowledge Proof
- **URL**: https://www.rfc-editor.org/rfc/rfc8235
- **Description**: Standardized Schnorr NIZKP

### RFC 5054 - SRP (Secure Remote Password)
- **URL**: https://www.rfc-editor.org/rfc/rfc5054
- **Description**: Zero-knowledge password authentication protocol

## Python Libraries

### py-ecc
- **URL**: https://github.com/ethereum/py_ecc
- **Description**: Elliptic curve operations for ZKPs

### cryptography
- **URL**: https://cryptography.io/
- **Description**: Hash functions, modular arithmetic support

---

## Workflows

## Workflow 1: Schnorr Interactive ZKP

```
Prover (knows secret x)              Verifier (knows y = g^x mod p)
      |                                      |
      |-- Commitment: t = g^r mod p -------->|
      |                                      |
      |<-- Challenge: c (random) ------------|
      |                                      |
      |-- Response: s = (r + c*x) mod q ---->|
      |                                      |
      |                              [Verify: g^s == t * y^c mod p]
      |                              [Accept or Reject]
```

## Workflow 2: Non-Interactive ZKP (Fiat-Shamir)

```
Prover:
  1. Choose random r
  2. Compute t = g^r mod p
  3. Compute c = H(g || y || t)  (Fiat-Shamir)
  4. Compute s = (r + c*x) mod q
  5. Send proof (t, s) to verifier

Verifier:
  1. Compute c = H(g || y || t)
  2. Check g^s == t * y^c mod p
```

## Workflow 3: Registration and Authentication

```
[Registration]:
  User --> [Choose password/secret x]
       --> [Compute y = g^x mod p]
       --> [Send y to server]
  Server --> [Store y (public key only)]

[Authentication]:
  User <--> Server: [Run Schnorr protocol]
  Server: [Verifies proof without learning x]
  Server: [Grants session token on success]
```
