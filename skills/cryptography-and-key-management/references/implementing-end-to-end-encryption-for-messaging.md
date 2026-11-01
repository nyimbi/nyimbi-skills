# Implementing End To End Encryption For Messaging

## API Reference

## Libraries Used
- **cryptography**: X25519 key exchange, HKDF key derivation, AES-256-GCM encryption

## CLI Interface

```
python agent.py keygen                                    # Generate X25519 key pair
python agent.py exchange                                  # Simulate key exchange
python agent.py demo                                      # Full E2EE demo flow
python agent.py encrypt --message <text> --key <hex>      # Encrypt message
python agent.py decrypt --nonce <hex> --ciphertext <hex> --key <hex>
```

## Core Functions

### `generate_keypair()`
Generates X25519 key pair for Diffie-Hellman key exchange.
- `X25519PrivateKey.generate()` -> private key
- `private_key.public_key()` -> public key
- Returns hex-encoded private and public keys.

### `derive_shared_secret(my_private_hex, their_public_hex)`
Performs X25519 ECDH key exchange and derives symmetric key via HKDF-SHA256.
- `my_private.exchange(their_public)` -> 32-byte raw shared secret
- `HKDF(algorithm=SHA256(), length=32, info=b"e2ee-messaging-v1").derive(shared)`

### `encrypt_message(message, shared_key_hex)`
Encrypts plaintext using AES-256-GCM with random 12-byte nonce.
- `AESGCM(key).encrypt(nonce, plaintext, None)` -> ciphertext with GCM tag

### `decrypt_message(nonce_hex, ciphertext_hex, shared_key_hex)`
Decrypts and authenticates ciphertext. Raises `InvalidTag` if tampered.

## Cryptography API Calls

| Class | Module | Purpose |
|-------|--------|---------|
| `X25519PrivateKey` | `cryptography.hazmat.primitives.asymmetric.x25519` | ECDH private key |
| `X25519PublicKey` | same | ECDH public key |
| `AESGCM` | `cryptography.hazmat.primitives.ciphers.aead` | Authenticated encryption |
| `HKDF` | `cryptography.hazmat.primitives.kdf.hkdf` | Key derivation |

## Dependencies
```
pip install cryptography>=41.0
```

---

## Standards and Controls

## Signal Protocol Specifications

### The Double Ratchet Algorithm
- **URL**: https://signal.org/docs/specifications/doubleratchet/
- **Description**: Core key management algorithm for E2EE messaging

### The X3DH Key Agreement Protocol
- **URL**: https://signal.org/docs/specifications/x3dh/
- **Description**: Initial key exchange using Extended Triple Diffie-Hellman

### The Sesame Algorithm
- **URL**: https://signal.org/docs/specifications/sesame/
- **Description**: Multi-device session management

## Cryptographic Standards

### RFC 7748 - Elliptic Curves for Security (X25519)
- **URL**: https://www.rfc-editor.org/rfc/rfc7748
- **Description**: X25519 Diffie-Hellman key exchange

### RFC 5869 - HKDF (HMAC-based Key Derivation Function)
- **URL**: https://www.rfc-editor.org/rfc/rfc5869
- **Description**: Key derivation for chain key updates

### RFC 8032 - Edwards-Curve Digital Signature Algorithm (Ed25519)
- **URL**: https://www.rfc-editor.org/rfc/rfc8032
- **Description**: Identity key signatures

### NIST SP 800-38D - AES-GCM
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-38d/final
- **Description**: Authenticated encryption for messages

## Python Libraries

### cryptography
- **X25519**: `cryptography.hazmat.primitives.asymmetric.x25519`
- **HKDF**: `cryptography.hazmat.primitives.kdf.hkdf`
- **AES-GCM**: `cryptography.hazmat.primitives.ciphers.aead.AESGCM`

---

## Workflows

## Workflow 1: X3DH Key Agreement

```
Alice (initiator)                 Server                  Bob (responder)
  |                                 |                         |
  |                                 |<-- Register:            |
  |                                 |    Identity Key (IK_B)  |
  |                                 |    Signed PreKey (SPK_B)|
  |                                 |    One-Time PreKeys     |
  |                                 |                         |
  |-- Fetch Bob's Keys ----------->|                         |
  |<-- IK_B, SPK_B, OPK_B --------|                         |
  |                                 |                         |
  [Compute shared secret]:                                    |
  DH1 = DH(IK_A, SPK_B)                                     |
  DH2 = DH(EK_A, IK_B)                                      |
  DH3 = DH(EK_A, SPK_B)                                     |
  DH4 = DH(EK_A, OPK_B)                                     |
  SK = HKDF(DH1 || DH2 || DH3 || DH4)                      |
  |                                 |                         |
  |-- Send Initial Message ------->|-- Forward to Bob ------>|
  |   (IK_A, EK_A, OPK_id, msg)   |                         |
  |                                 |   [Bob computes same SK]|
```

## Workflow 2: Double Ratchet (Sending)

```
[Message to Send]
      |
[Check: Do we have recipient's new DH public key?]
  YES --> [DH Ratchet Step]
          - Generate new DH key pair
          - Compute DH shared secret
          - Derive new root key + sending chain key via HKDF
  NO  --> [Continue with current sending chain]
      |
[Symmetric Ratchet: Derive message key from sending chain]
(chain_key, message_key) = HMAC(chain_key, constants)
      |
[Encrypt message with AES-256-GCM using message_key]
      |
[Include header: DH public key, previous chain length, message number]
      |
[Delete message_key from memory]
```

## Workflow 3: Double Ratchet (Receiving)

```
[Received Encrypted Message + Header]
      |
[Check DH public key in header]
  [New key?]
    YES --> [DH Ratchet Step]
            - Compute DH shared secret
            - Derive new root key + receiving chain key
    NO  --> [Use current receiving chain]
      |
[Symmetric Ratchet: Derive message key]
      |
[Decrypt message with AES-256-GCM]
      |
[Verify authentication tag]
  FAIL --> Reject message
  PASS --> Return plaintext
      |
[Delete message_key from memory]
```

## Workflow 4: Session Lifecycle

```
[Initial Contact] --> [X3DH Key Exchange]
                            |
                      [Initialize Double Ratchet]
                            |
                      [Exchange Messages]
                      (DH ratchet + symmetric ratchet)
                            |
                      [Periodic DH Ratchet]
                      (every N messages or on reply)
                            |
                      [Session End / Archive]
```

---

## Working Template

## Protocol Summary

| Phase | Algorithm | Purpose |
|-------|-----------|---------|
| Key Exchange | X3DH (X25519) | Initial shared secret |
| Key Ratchet | Double Ratchet | Per-message key derivation |
| Encryption | AES-256-GCM | Message confidentiality + integrity |
| Key Derivation | HKDF-SHA256 | Derive keys from DH outputs |
| Chain KDF | HMAC-SHA256 | Advance symmetric ratchet |

## Security Properties Checklist

- [ ] Forward secrecy: Past messages safe if current keys compromised
- [ ] Post-compromise security: Recovery after temporary key compromise
- [ ] Deniability: No cryptographic proof of message authorship
- [ ] Authenticated encryption: Tampered messages detected and rejected
- [ ] Replay protection: Message counters prevent replay attacks
- [ ] Out-of-order delivery: Skipped keys stored for late messages

## Message Format

```
[Header (40 bytes)]
  - DH Public Key: 32 bytes
  - Previous Chain Length: 4 bytes (big-endian)
  - Message Number: 4 bytes (big-endian)

[Encrypted Payload]
  - Nonce: 12 bytes
  - Ciphertext + Tag: variable
```

## Integration Notes

- Identity keys should be stored in secure device storage (Keychain, TEE)
- Implement safety number verification for identity key comparison
- Handle device changes by re-running X3DH with new identity keys
- Store skipped message keys with a maximum limit (e.g., 1000)
- Delete message keys immediately after successful decryption
