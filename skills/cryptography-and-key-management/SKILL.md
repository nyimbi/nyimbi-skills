---
name: cryptography-and-key-management
description: >-
  Design, implement, audit, and migrate cryptographic systems: symmetric and
  asymmetric encryption, key management and HSMs, PKI and certificate
  lifecycles, TLS configuration, digital signatures, JWT/token signing,
  password hashing, and post-quantum migration. Use when the user asks to
  encrypt data at rest or in transit, choose an algorithm or key size, stand
  up a CA or HSM, rotate or escrow keys, sign or verify artifacts, harden TLS,
  evaluate a crypto implementation, crack or audit a hash, plan a
  harvest-now-decrypt-later migration, or asks "which encryption should I
  use", "is this JWT safe", "how do I store these keys", "how do we get
  quantum-ready". Do not use for breaking into systems (see
  offensive-security-and-red-teaming), recovering evidence from a compromise
  (see digital-forensics-and-evidence), or choosing which cloud workload
  consumes a KMS key (see cloud-container-and-devsecops-security).
---

# Cryptography and Key Management

Cryptography fails far more often through misuse than through broken math. The
single highest-value thing this skill does is prevent the classic misuse
failures: raw passwords used as keys, nonces reused under GCM, `none`
algorithm accepted in a JWT, static RSA padding where OAEP was required, a CA
key sitting on the same disk as the web server, and a "quantum-safe" claim
backed by nothing but a marketing page.

Treat every recommendation as if it will be reviewed by someone who will ask
"what is the failure mode if this is wrong?" Answer that question before you
answer the design question.

## When to use

- Encrypting files, databases, object stores, backups, or message queues at rest
- Choosing an algorithm, mode, key size, or KDF for a new system
- Designing key hierarchy, rotation policy, escrow, or ceremony
- Standing up or operating a CA, issuing/expiring/revoking certificates
- Configuring TLS 1.2/1.3, mTLS, cipher suite selection, or HSTS
- Implementing signing/verification for artifacts, firmware, JWTs, or documents
- Reviewing an existing implementation for cryptographic weakness
- Planning post-quantum migration, CBOM, or hybrid key exchange
- Auditing where keys live, who can use them, and what happens when they leak

**Do not use for** — `offensive-security-and-red-teaming` when the goal is to
gain access or crack a target you are authorized to attack (hash cracking *for
a pentest* stays here only as part of credential-strength assessment);
`digital-forensics-and-evidence` when the question is what already happened on
a compromised host; `identity-zero-trust-and-endpoint-security` when the
question is who is allowed to authenticate rather than how the credential is
protected; `cloud-container-and-devsecops-security` when the ask is wiring a
cloud KMS into an application's runtime permissions rather than designing the
encryption scheme itself.

## Workflow

1. **Establish the threat model and assets.** Write down: what asset is being
   protected, against whom (opportunistic, organized, nation-state), over what
   time horizon, and what "failure" looks like. Data that must remain
   confidential for 30 years is a different problem from a session token that
   expires in 15 minutes.

2. **Classify the requirement.** Map to the binding constraints first, not the
   algorithm: regulatory (FIPS 140-3, PCI DSS 3.6.x, HIPAA, GDPR Art. 32),
   data lifetime vs. adversary capability, performance envelope (ops/sec,
   bytes/sec, latency budget), and platform support (does the runtime actually
   ship the primitive?).

3. **Pick primitives, then parameters.** Defaults that hold up under review:
   - Data at rest — AES-256-GCM (or AES-XTS for block/disk layers). Never CBC
     without an independent MAC; never ECB.
   - Data in transit — TLS 1.3, or TLS 1.2 with AEAD suites only. X25519 for
     key exchange, ECDSA-P256 or Ed25519 for signatures where FIPS is not
     required; RSA-3072+ where it is.
   - Passwords / secrets from humans — Argon2id (m=64 MiB, t=3, p=4 floor);
     PBKDF2-HMAC-SHA256 at ≥600,000 iterations only where Argon2 is
     unavailable.
   - Artifact signing — Ed25519 (or ML-DSA / RSA-PSS when FIPS or
     compatibility demands it).
   - Token signing — EdDSA or ES256. `HS256` only with a high-entropy secret.
     Reject `none`, `RS1`, and any algorithm taken from the token header.
   Anything relying on RSA, ECDH, or ECDSA for confidentiality or signature
   binding is quantum-vulnerable and enters the migration path in step 6.

4. **Design the key hierarchy before writing code.** Establish: master key
   (HSM-held, never exported) → key-encryption-keys (per purpose, per
   environment) → data-encryption-keys (per record/asset, short-lived). Name
   every key with owner, purpose, environment, creation date, and rotation
   date. If you cannot state where the root of trust physically lives, the
   design is not finished.

5. **Implement with the platform's library, never hand-rolled primitives.**
   Use `cryptography` (Python), `crypto`/`x/crypto` (Go), `javax.crypto`,
   BoringSSL/OpenSSL 3.x. Generate nonces from a CSPRNG, store nonce +
   ciphertext + auth tag together, and zeroize key material after use where
   the runtime allows it. Every code path that touches keys needs an explicit
   failure mode for entropy exhaustion and clock skew.

6. **Check migration exposure.** For any asset with a confidentiality horizon
   beyond ~10 years, or that is already being collected now for later
   decryption: build the cryptographic inventory (CBOM), classify by
   harvest-now-decrypt-later exposure, and stage hybrid `X25519MLKEM768`
   key exchange plus ML-DSA signatures. Confirm OpenSSL 3.5+ (or oqs-provider)
   before promising PQC support.

7. **Verify against the quality bar, then document.** Run the checks below.
   Record the design decision (algorithm, parameters, key locations, rotation
   cadence, threat model) in a short ADR-style note — crypto decisions that
   are not written down get reverted by the next engineer.

## Quality bar

- [ ] Threat model names the adversary, asset, and time horizon explicitly
- [ ] No raw password or user-supplied string is ever used directly as key
      material; a KDF with salt and recorded parameters is always in between
- [ ] AEAD is used everywhere; any non-AEAD mode has a stated, documented
      reason and an independent MAC
- [ ] Nonces/IVs are unique per key — for GCM, generated by CSPRNG or a
      monotonic counter, never a loop counter persisted across restarts
- [ ] Key hierarchy is written down with owner, purpose, environment, and
      rotation cadence; root keys are in an HSM or KMS and are never exported
- [ ] Algorithm/parameter choices are justified against the *binding*
      constraint (regulation, platform, performance), not by preference
- [ ] Token verification rejects `alg: none`, enforces expected algorithm,
      validates `exp`/`nbf`/`aud`, and pins the key or kid
- [ ] Certificates have explicit expiry, revocation checking (CRL or OCSP) is
      implemented, and the CA key is offline and physically separated
- [ ] Post-quantum exposure is assessed for anything with a >10-year
      confidentiality horizon, with hybrid deployment staged where it applies
- [ ] A written record exists of algorithm, parameters, key locations,
      rotation policy, and the threat model it was chosen against
- [ ] Keys can be rotated and revoked without downtime, and the procedure has
      been rehearsed at least once

## Reference map

Per-technique detail is one file per topic, indexed in
[`references/technique-index.md`](references/technique-index.md). Load the
file for the primitive you are implementing rather than reading the index.

| Situation | Open |
|---|---|
| Encrypting files or a data store, choosing modes/nonces | [implementing-aes-encryption-for-data-at-rest](references/implementing-aes-encryption-for-data-at-rest.md) |
| Wrapping DEKs with a cloud KMS, envelope-encryption design | [implementing-envelope-encryption-with-aws-kms](references/implementing-envelope-encryption-with-aws-kms.md) |
| RSA key generation, padding choice, storage formats | [implementing-rsa-key-pair-management](references/implementing-rsa-key-pair-management.md) |
| Signing documents/artifacts with Ed25519 | [implementing-digital-signatures-with-ed25519](references/implementing-digital-signatures-with-ed25519.md) |
| JWT signing, verification, and algorithm-confusion defence | [implementing-jwt-signing-and-verification](references/implementing-jwt-signing-and-verification.md) |
| Issuing, renewing, revoking certificates; CA hierarchy | [configuring-certificate-authority-with-openssl](references/configuring-certificate-authority-with-openssl.md) |
| Certificate inventory, expiry, and renewal process | [performing-ssl-certificate-lifecycle-management](references/performing-ssl-certificate-lifecycle-management.md) |
| TLS 1.3 configuration and cipher suite selection | [configuring-tls-1-3-for-secure-communications](references/configuring-tls-1-3-for-secure-communications.md) |
| HSM selection, PKCS#11 integration, key object model | [configuring-hsm-for-key-storage](references/configuring-hsm-for-key-storage.md) · [performing-hardware-security-module-integration](references/performing-hardware-security-module-integration.md) |
| Messaging end-to-end encryption, forward secrecy | [implementing-end-to-end-encryption-for-messaging](references/implementing-end-to-end-encryption-for-messaging.md) |
| Zero-knowledge proof for authentication | [implementing-zero-knowledge-proof-for-authentication](references/implementing-zero-knowledge-proof-for-authentication.md) |
| Auditing an application's cryptographic usage | [performing-cryptographic-audit-of-application](references/performing-cryptographic-audit-of-application.md) |
| Password/credential hash strength assessment | [performing-hash-cracking-with-hashcat](references/performing-hash-cracking-with-hashcat.md) |
| Post-quantum migration, CBOM, hybrid TLS (two entries, one topic) | [migrating-to-post-quantum-cryptography](references/migrating-to-post-quantum-cryptography.md) · [performing-post-quantum-cryptography-migration](references/performing-post-quantum-cryptography-migration.md) |

Executable helpers for each technique live in
`scripts/<technique-name>/` — read the reference file first to learn what the
script expects, then run it.

## Output format

For any design or audit request, deliver:

```markdown
# <System> — Cryptographic Design / Audit

## Decision
One paragraph: what was chosen and why it satisfies the binding constraint.

## Threat model
Asset | Adversary | Horizon | Failure consequence

## Primitives and parameters
Use | Algorithm | Parameters | Justification

## Key management
Key | Level | Owner | Location | Rotation | Destruction

## Verification
Quality-bar checklist, checked items only where actually verified.

## Residual risk / migration exposure
What remains weak, including harvest-now-decrypt-later exposure and any
post-quantum work required, with a staged plan.
```

For an audit, add a findings table ordered by severity with the concrete fix
for each, and cite the exact line, config key, or API call that is wrong.
