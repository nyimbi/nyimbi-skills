# Implementing Privileged Access Management With Cyberark

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `requests` | HTTP client for CyberArk PVWA REST API |
| `json` | Parse CyberArk JSON responses |
| `os` | Read environment variables for credentials |
| `urllib.parse` | URL-encode safe and account query parameters |

## Installation

```bash
pip install requests
```

## Authentication

CyberArk PVWA REST API requires session token authentication:

```python
import requests
import os

PVWA_URL = os.environ.get("CYBERARK_URL", "https://pvwa.example.com")

# CyberArk credential authentication
resp = requests.post(
    f"{PVWA_URL}/PasswordVault/api/auth/cyberark/logon",
    json={
        "username": os.environ["CYBERARK_USER"],
        "password": os.environ["CYBERARK_PASS"],
    },
    timeout=30,
    verify=True,
)
session_token = resp.json()  # Returns session token string
headers = {"Authorization": session_token}
```

### LDAP Authentication
```python
resp = requests.post(
    f"{PVWA_URL}/PasswordVault/api/auth/ldap/logon",
    json={"username": user, "password": password},
    timeout=30,
    verify=True,
)
```

### RADIUS Authentication
```python
resp = requests.post(
    f"{PVWA_URL}/PasswordVault/api/auth/radius/logon",
    json={"username": user, "password": otp_code},
    timeout=30,
    verify=True,
)
```

## REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/{method}/logon` | Authenticate (cyberark, ldap, radius) |
| POST | `/api/auth/logoff` | End session |
| GET | `/api/Accounts` | List privileged accounts |
| GET | `/api/Accounts/{id}` | Get account details |
| POST | `/api/Accounts` | Add a new privileged account |
| PATCH | `/api/Accounts/{id}` | Update account properties |
| DELETE | `/api/Accounts/{id}` | Delete an account |
| POST | `/api/Accounts/{id}/Password/Retrieve` | Retrieve account password |
| POST | `/api/Accounts/{id}/Change` | Trigger password change |
| POST | `/api/Accounts/{id}/Reconcile` | Reconcile password |
| POST | `/api/Accounts/{id}/Verify` | Verify password on target |
| GET | `/api/Safes` | List safes |
| GET | `/api/Safes/{name}` | Get safe details |
| POST | `/api/Safes` | Create a safe |
| GET | `/api/Safes/{name}/Members` | List safe members |
| POST | `/api/Safes/{name}/Members` | Add safe member |
| GET | `/api/Platforms` | List platforms |
| GET | `/api/ComponentsMonitoringDetails/{component}` | System health |

## Core Operations

### List Privileged Accounts
```python
resp = requests.get(
    f"{PVWA_URL}/PasswordVault/api/Accounts",
    headers=headers,
    params={"search": "Linux", "limit": 100},
    timeout=30,
    verify=True,
)
accounts = resp.json()
for acct in accounts.get("value", []):
    print(f"{acct['name']} — platform: {acct['platformId']}, safe: {acct['safeName']}")
```

### Retrieve a Password (Check-Out)
```python
resp = requests.post(
    f"{PVWA_URL}/PasswordVault/api/Accounts/{account_id}/Password/Retrieve",
    headers=headers,
    json={"reason": "Automated security audit"},
    timeout=30,
    verify=True,
)
password = resp.text  # Returns the password as plain text
```

### List Safes and Audit Permissions
```python
resp = requests.get(
    f"{PVWA_URL}/PasswordVault/api/Safes",
    headers=headers,
    params={"limit": 200},
    timeout=30,
    verify=True,
)
for safe in resp.json().get("value", []):
    members_resp = requests.get(
        f"{PVWA_URL}/PasswordVault/api/Safes/{safe['safeName']}/Members",
        headers=headers,
        timeout=30,
        verify=True,
    )
    members = members_resp.json().get("value", [])
    print(f"Safe: {safe['safeName']} — {len(members)} members")
```

### Trigger Password Rotation
```python
resp = requests.post(
    f"{PVWA_URL}/PasswordVault/api/Accounts/{account_id}/Change",
    headers=headers,
    json={"ChangeEntireGroup": False},
    timeout=60,
    verify=True,
)
```

### Logoff
```python
requests.post(
    f"{PVWA_URL}/PasswordVault/api/auth/logoff",
    headers=headers,
    timeout=10,
    verify=True,
)
```

## Output Format

```json
{
  "value": [
    {
      "id": "42_8",
      "name": "root-linux-prod01",
      "address": "10.0.1.50",
      "userName": "root",
      "platformId": "UnixSSH",
      "safeName": "LinuxRoot",
      "secretType": "password",
      "platformAccountProperties": {
        "LogonDomain": "",
        "Port": "22"
      },
      "secretManagement": {
        "automaticManagementEnabled": true,
        "lastModifiedTime": 1705334400
      }
    }
  ],
  "count": 1
}
```

---

## Standards and Controls

## NIST Standards
- **NIST SP 800-53 Rev 5**: Security and Privacy Controls
  - AC-2: Account Management
  - AC-5: Separation of Duties
  - AC-6: Least Privilege
  - AC-6(7): Review of User Privileges (Privileged Accounts)
  - AU-14: Session Audit
  - IA-5: Authenticator Management
- **NIST SP 800-171**: Protecting CUI - 3.1.5 Least Privilege, 3.1.7 Privileged Functions
- **NIST SP 800-63B**: Digital Identity Guidelines - Authentication
- **NIST Cybersecurity Framework**: PR.AC (Identity Management, Authentication, Access Control)

## CyberArk Documentation
- **CyberArk NIST 800-53 Rev 5 Whitepaper**: https://www.cyberark.com/resources/white-papers/nist-sp-800-53-revision-5-implementing-essential-security-controls-with-cyberark-solutions
- **CyberArk Privilege Cloud**: SaaS PAM platform
- **CyberArk Conjur**: Application secrets management
- **CyberArk EPM**: Endpoint privilege management

## Industry Standards
- **CIS Controls v8**: Control 5 - Account Management, Control 6 - Access Control Management
- **MITRE ATT&CK**: T1078 (Valid Accounts), T1003 (OS Credential Dumping)
- **PCI DSS 4.0**: Requirement 7 (Restrict Access), Requirement 8 (Identify and Authenticate)
- **SOX**: Section 404 - Internal controls for privileged access
- **ISO 27001**: A.9 Access Control

## Compliance Frameworks
- **FISMA**: Federal compliance requiring NIST 800-53 controls
- **HIPAA**: Access controls for PHI systems
- **GDPR**: Article 32 - Security of processing

---

## Workflows

## Workflow 1: Privileged Credential Checkout and Use

```
User -> PVWA -> Request Credential -> Dual Control Approval -> Vault Release -> PSM Session -> Target System
```

### Steps:
1. User authenticates to PVWA with MFA
2. User requests access to privileged account
3. If dual control enabled, request routed to approver
4. Approver reviews and approves/denies request
5. Vault releases credential through PSM
6. User connects to target via PSM (never sees password)
7. Session recorded (video, keystrokes, commands)
8. On disconnect, credential checked back in
9. If one-time password mode, CPM rotates credential immediately

## Workflow 2: Automated Credential Rotation

### Steps:
1. CPM checks rotation schedule for each platform
2. CPM connects to target system using reconciliation account
3. CPM generates new password meeting complexity requirements
4. CPM changes password on target system
5. CPM updates password in vault
6. CPM verifies new credential works on target
7. If verification fails, CPM triggers reconciliation
8. Rotation event logged to audit trail
9. SIEM alert triggered on rotation failure

## Workflow 3: Privileged Account Discovery

### Steps:
1. Configure account discovery scan targets (IP ranges, domains)
2. Discovery scanner connects to targets using scanning credentials
3. Scanner identifies privileged accounts:
   - Windows: Local admins, domain admins, service accounts
   - Linux: root, sudoers, service accounts
   - Database: DBA accounts, application accounts
   - Network: admin/enable accounts on switches/routers
4. Discovered accounts compared against vault inventory
5. Unmanaged accounts flagged for review
6. Security team reviews and prioritizes onboarding
7. Approved accounts onboarded to appropriate safes
8. CPM begins credential rotation per platform policy

## Workflow 4: Break-Glass Emergency Access

### Steps:
1. Normal vault access unavailable (outage, disaster)
2. Authorized personnel retrieve break-glass media (sealed envelope, USB)
3. Break-glass credentials used to access critical systems directly
4. All actions taken with break-glass credentials manually documented
5. When vault service restored, all break-glass credentials rotated immediately
6. Break-glass media re-sealed with new credentials
7. Incident report created documenting break-glass usage
8. All actions performed during break-glass reviewed by security team

## Workflow 5: Incident Response - Compromised Privileged Account

### Steps:
1. PTA detects anomalous privileged account behavior
2. Alert generated with risk score and indicators
3. Security analyst reviews alert in PVWA/SIEM
4. If confirmed compromise:
   a. Immediately rotate compromised credential via CPM
   b. Terminate any active PSM sessions using that account
   c. Review session recordings for malicious activity
   d. Check for lateral movement using audit logs
   e. Assess blast radius of compromised privilege level
5. Forensic analysis of session recordings
6. Post-incident review and policy updates

---

## Working Template

## Vault Architecture
- [ ] Primary vault server deployed in hardened network segment
- [ ] DR vault configured and tested
- [ ] Vault firewall rules (port 1858 only from authorized components)
- [ ] Vault OS hardened (CIS benchmark applied)
- [ ] Vault backup and recovery tested
- [ ] Break-glass procedure documented and sealed

## Safe Hierarchy
| Safe Name | Purpose | Dual Control | Retention |
|-----------|---------|--------------|-----------|
| DomainAdmins | Domain admin credentials | Yes | 365 days |
| LocalAdmins | Local admin credentials | No | 180 days |
| ServiceAccounts | Service account credentials | No | 365 days |
| DatabaseAdmins | DBA credentials | Yes | 365 days |
| NetworkDevices | Network device credentials | No | 180 days |
| CloudIAM | Cloud access keys | Yes | 365 days |

## Platform Rotation Policies
| Platform | Rotation | Verification | Reconciliation |
|----------|----------|--------------|----------------|
| Windows Domain Admin | 24 hours | 4 hours | On failure |
| Linux Root (SSH Key) | 72 hours | 12 hours | On failure |
| SQL Server SA | 24 hours | 4 hours | On failure |
| Oracle DBA | 24 hours | 4 hours | On failure |
| Cisco IOS | 7 days | 24 hours | On failure |
| Service Accounts | 30 days | 7 days | On failure |
| AWS IAM Keys | 90 days | 30 days | On failure |

## PSM Configuration
- [ ] PSM servers deployed behind load balancer
- [ ] RDP connection component configured
- [ ] SSH connection component configured
- [ ] Database connection components (SSMS, SQL*Plus)
- [ ] Web application connectors configured
- [ ] Session recording storage provisioned
- [ ] Recording retention policy: _____ days
- [ ] Live monitoring enabled

## Integration Checklist
- [ ] SIEM integration (Syslog/CEF)
- [ ] Ticketing system integration (ServiceNow/Jira)
- [ ] PTA deployed and configured
- [ ] LDAP/AD integration for vault authentication
- [ ] MFA integration (RADIUS/Duo)

## Compliance Mapping
| Requirement | CyberArk Control | Status |
|-------------|------------------|--------|
| NIST AC-2 Account Management | Vault account lifecycle | [ ] |
| NIST AC-5 Separation of Duties | Dual control, safe roles | [ ] |
| NIST AC-6 Least Privilege | Platform-based access | [ ] |
| NIST IA-5 Authenticator Management | CPM rotation | [ ] |
| NIST AU-14 Session Audit | PSM recording | [ ] |
| PCI DSS 7.1 Restrict Access | Safe-based access control | [ ] |
| PCI DSS 8.3.6 Password Complexity | Platform policies | [ ] |
