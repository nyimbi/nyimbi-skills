# Performing Hash Cracking With Hashcat

## API Reference

## Libraries Used
- **subprocess**: Execute hashcat with various attack modes
- **hashlib**: Generate test hashes (MD5, SHA1, SHA256, SHA512)
- **re**: Pattern matching for hash type identification
- **pathlib**: Read hash files and potfiles

## CLI Interface
```
python agent.py identify --hash <hash_string>
python agent.py identify --file hashes.txt
python agent.py crack --hash-file hashes.txt --mode 0 --attack dictionary --wordlist rockyou.txt [--rules best64.rule]
python agent.py crack --hash-file hashes.txt --mode 1000 --attack brute --mask "?u?l?l?l?d?d?d?s"
python agent.py parse --potfile hashcat.potfile
python agent.py gen --text "password123" --algo sha256
```

## Core Functions

### `identify_hash(hash_string)` — Detect hash type and hashcat mode
Matches against 12 patterns: MD5 (0), SHA1 (100), SHA256 (1400), SHA512 (1700),
NTLM (1000), bcrypt (3200), sha512crypt (1800), md5crypt (500), NetNTLMv2 (5600),
Kerberos TGS (13100), Kerberos AS-REP (18200).

### `run_hashcat(hash_file, mode, attack, wordlist, rules, mask)` — Execute hashcat
Attack modes: `dictionary` (-a 0), `brute` (-a 3), `combinator` (-a 1).

### `parse_hashcat_status(potfile)` — Analyze cracked passwords
Returns length distribution, charset analysis, top passwords from potfile.

### `generate_hash(plaintext, algorithm)` — Create test hashes
Supported: md5, sha1, sha256, sha512.

## Hashcat Mask Charsets
- `?l` lowercase, `?u` uppercase, `?d` digits, `?s` special, `?a` all

## Dependencies
System: hashcat (GPU-accelerated hash cracking)
No Python packages required — standard library only.

---

## Standards and Controls

## Tools

### Hashcat
- **URL**: https://hashcat.net/hashcat/
- **GitHub**: https://github.com/hashcat/hashcat
- **Wiki**: https://hashcat.net/wiki/
- **Hash modes**: https://hashcat.net/wiki/doku.php?id=hashcat

### Wordlists
- **SecLists**: https://github.com/danielmiessler/SecLists
- **RockYou**: Classic breach wordlist (14 million passwords)
- **CrackStation**: https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm

## Standards

### NIST SP 800-63B - Digital Identity Guidelines (Authentication)
- **URL**: https://pages.nist.gov/800-63-3/sp800-63b.html
- **Description**: Password requirements and memorized secret guidelines

### OWASP Password Storage Cheat Sheet
- **URL**: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

## Legal Framework

- Computer Fraud and Abuse Act (CFAA) - US
- Computer Misuse Act 1990 - UK
- Always obtain written authorization before testing
- Follow penetration testing rules of engagement

---

## Workflows

## Workflow 1: Hash Identification and Cracking

```
[Captured Hashes]
      |
[Identify Hash Type]
(hashcat --identify, hashid, haiti)
      |
[Select Attack Strategy]:
  1. Dictionary attack (rockyou.txt)
  2. Dictionary + rules (best64.rule)
  3. Mask attack (brute-force)
  4. Hybrid (wordlist + mask)
      |
[Execute Hashcat]
      |
[Analyze Results]
(cracked count, time, patterns)
      |
[Generate Password Strength Report]
```

## Workflow 2: Hashcat Command Examples

```bash
# Dictionary attack
hashcat -m 0 -a 0 hashes.txt rockyou.txt

# Dictionary + rules
hashcat -m 0 -a 0 hashes.txt rockyou.txt -r best64.rule

# Mask (brute-force 8-char lowercase)
hashcat -m 0 -a 3 hashes.txt ?l?l?l?l?l?l?l?l

# Hybrid (wordlist + 4 digits)
hashcat -m 0 -a 6 hashes.txt rockyou.txt ?d?d?d?d

# Show cracked passwords
hashcat -m 0 hashes.txt --show
```

## Workflow 3: Password Audit Report

```
[Cracking Results]
      |
[Categorize]:
  - Cracked in < 1 min: CRITICAL
  - Cracked in < 1 hour: HIGH
  - Cracked in < 1 day: MEDIUM
  - Not cracked: Acceptable
      |
[Pattern Analysis]:
  - Common base words
  - Character set distribution
  - Length distribution
  - Policy compliance
      |
[Generate Report with Recommendations]
```

---

## Working Template

## Authorization Verification

- [ ] Written authorization obtained from asset owner
- [ ] Scope of engagement defines which hashes may be cracked
- [ ] Data handling requirements documented
- [ ] Results reporting chain defined
- [ ] Data destruction timeline agreed

## Hashcat Quick Reference

```bash
# Identify hash type
hashcat --identify hash.txt

# MD5 dictionary
hashcat -m 0 -a 0 hashes.txt wordlist.txt

# NTLM with rules
hashcat -m 1000 -a 0 hashes.txt wordlist.txt -r rules/best64.rule

# bcrypt dictionary (slow)
hashcat -m 3200 -a 0 hashes.txt wordlist.txt

# Benchmark
hashcat -b
```

## Mask Charsets

| Charset | Characters | Symbol |
|---------|-----------|--------|
| ?l | a-z | lowercase |
| ?u | A-Z | uppercase |
| ?d | 0-9 | digits |
| ?s | special chars | symbols |
| ?a | ?l?u?d?s | all printable |

## Reporting Template

| Metric | Value |
|--------|-------|
| Total hashes | [count] |
| Cracked | [count] ([%]) |
| < 1 minute | [count] (CRITICAL) |
| < 1 hour | [count] (HIGH) |
| < 1 day | [count] (MEDIUM) |
| Not cracked | [count] (OK) |
