# Performing Initial Access With Evilginx3

## API Reference

## Libraries Used
- **pyyaml**: Parse Evilginx3 phishlet YAML configuration files
- **subprocess**: Check Evilginx installation and version
- **pathlib**: Directory listing and file reading
- **re**: IP address extraction from session logs

## CLI Interface
```
python agent.py parse --phishlet office365.yaml
python agent.py logs --file sessions.log
python agent.py check
python agent.py list --dir /path/to/phishlets/
python agent.py detect --phishlet office365.yaml
```

## Core Functions

### `parse_phishlet(phishlet_path)` — Analyze phishlet configuration
Extracts proxy hosts, auth tokens, credential fields. Determines MFA bypass capability.

### `analyze_session_log(log_file)` — Parse Evilginx session captures
Identifies sessions with captured tokens and credentials. Extracts source IPs.

### `check_evilginx_installation()` — Verify Evilginx3 binary
Returns installed status and version string.

### `list_phishlets(phishlet_dir)` — Enumerate available phishlets
Lists .yaml/.yml files in phishlet directory with sizes.

### `generate_detection_rules(phishlet_path)` — Create defensive signatures
Generates DNS monitoring, cookie relay detection, and network anomaly rules.
Includes FIDO2/WebAuthn MFA recommendations.

## Phishlet Structure
- `proxy_hosts`: Domain-to-phishing-subdomain mappings
- `auth_tokens`: Session cookies to intercept (enables MFA bypass)
- `credentials`: Form fields to capture (username/password)
- `sub_filters`: Content replacement rules for convincing proxied pages

## Dependencies
```
pip install pyyaml
```
System: evilginx (optional, for live testing)

---

## Standards and Controls

## MITRE ATT&CK References

| Technique ID | Name | Tactic |
|-------------|------|--------|
| T1566.002 | Phishing: Spearphishing Link | Initial Access |
| T1557 | Adversary-in-the-Middle | Credential Access |
| T1539 | Steal Web Session Cookie | Credential Access |
| T1078 | Valid Accounts | Initial Access, Persistence |
| T1556 | Modify Authentication Process | Credential Access |
| T1550.004 | Use Alternate Authentication Material: Web Session Cookie | Lateral Movement |

## Industry Standards

- **PTES** - Pre-Engagement and Intelligence Gathering phases
- **OWASP Testing Guide** - Authentication Testing
- **NIST SP 800-63B** - Digital Identity Guidelines: Authentication
- **CISA Advisory AA22-277A** - Threat Actors Exploiting MFA Bypass Techniques

## Official Resources

- EvilGinx Project: https://github.com/kgretzky/evilginx2
- GoPhish: https://getgophish.com/
- EvilGoPhish: https://github.com/fin3ss3g0d/evilgophish
- Certificate Transparency Logs: https://crt.sh

## Research Papers

- Microsoft Storm-1167 AiTM Phishing Campaign Analysis (2023)
- Deepwatch: Catching the Phish - Detecting Evilginx & AiTM
- BDO Security: MFA-Phishing as Initial Access in Red Teaming

---

## Workflows

## End-to-End AiTM Phishing Workflow

```
1. Reconnaissance
   ├── Identify target authentication service (M365, Google, Okta)
   ├── Analyze target MFA implementation (SMS, Authenticator, FIDO2)
   ├── Register lookalike domain with appropriate TLD
   └── Categorize domain to avoid URL filtering

2. Infrastructure Setup
   ├── Deploy VPS and configure DNS records
   ├── Install and configure EvilGinx3
   ├── Enable phishlet for target service
   ├── Verify SSL certificate provisioning
   └── Create and test lure URLs

3. Phishing Delivery
   ├── Craft pretext email with social engineering
   ├── Configure GoPhish or SMTP relay for delivery
   ├── Send phishing emails to authorized targets
   └── Monitor delivery and open rates

4. Credential and Session Capture
   ├── Monitor EvilGinx3 session dashboard
   ├── Capture credentials as victims authenticate
   ├── Capture session cookies (MFA bypass tokens)
   └── Export session data for exploitation

5. Session Hijacking
   ├── Import session cookies into attacker browser
   ├── Navigate to target service with hijacked session
   ├── Validate access to victim's account
   └── Enumerate accessible resources

6. Persistence and Escalation
   ├── Create application-specific passwords
   ├── Register attacker device in Azure AD / Entra ID
   ├── Add OAuth application consents
   └── Establish email forwarding rules for persistence

7. Reporting
   ├── Document attack chain with evidence
   ├── Record number of successful captures
   ├── Identify defensive gaps exploited
   └── Provide remediation recommendations
```

## Cookie Import Workflow

```
1. From EvilGinx3 session output, copy cookie data
2. Open browser with Cookie-Editor extension
3. Navigate to target service login page
4. Clear existing cookies for the domain
5. Import captured cookies via Cookie-Editor
6. Refresh the page to obtain authenticated session
7. Verify access to victim's account
```

---

## Working Template

## Campaign Information

| Field | Value |
|-------|-------|
| Campaign Name | |
| Target Organization | |
| Authorization Reference | |
| Target Service | Microsoft 365 / Google / Okta / Other |
| Start Date | |
| End Date | |

## Infrastructure

| Component | Details |
|-----------|---------|
| Phishing Domain | |
| Server IP | |
| Phishlet | |
| SSL Certificate | Let's Encrypt (auto) |
| Redirector | Yes / No |

## Target List

| # | Email | Department | Pretext |
|---|-------|------------|---------|
| 1 | | | |
| 2 | | | |

## Session Captures

| # | Session ID | Username | Cookies Captured | Time | MFA Bypassed |
|---|-----------|----------|-----------------|------|--------------|
| 1 | | | Yes / No | | Yes / No |

## Results Summary

| Metric | Value |
|--------|-------|
| Emails Sent | |
| Emails Opened | |
| Links Clicked | |
| Credentials Captured | |
| Sessions Hijacked | |
| MFA Bypassed | |

## Evidence Checklist

- [ ] Phishing email screenshot
- [ ] EvilGinx3 session capture output
- [ ] Cookie export file
- [ ] Browser session hijack screenshot
- [ ] Post-authentication access evidence
- [ ] Target mailbox/resource access proof
