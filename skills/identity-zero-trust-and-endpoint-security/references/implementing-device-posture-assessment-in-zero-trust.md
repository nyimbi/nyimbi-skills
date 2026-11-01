# Implementing Device Posture Assessment In Zero Trust

## API Reference

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| (stdlib only) | Python 3.8+ | Platform detection, subprocess for OS security checks |

## CLI Usage

```bash
python scripts/agent.py --output-dir /reports/ --output device_posture.json
```

## Functions

### `check_os_version() -> dict`
Uses `platform.system()`, `platform.version()` for OS identification.

### `check_disk_encryption() -> dict`
Windows: `manage-bde -status C:` (BitLocker). macOS: `fdesetup status` (FileVault). Linux: `lsblk` for LUKS.

### `check_firewall_status() -> dict`
Windows: `netsh advfirewall show allprofiles state`. Linux: `ufw status`.

### `check_antivirus() -> dict`
Windows: PowerShell `Get-MpComputerStatus` for Defender real-time protection.

### `check_screen_lock() -> dict`
Windows: Registry `InactivityTimeoutSecs` check.

### `compute_posture_score(checks) -> dict`
Weighted scoring: encryption (25), firewall (20), AV (25), screen lock (15), OS (15). Returns COMPLIANT/PARTIAL/NON_COMPLIANT.

## Posture Checks

| Check | Weight | Tool |
|-------|--------|------|
| Disk Encryption | 25 | BitLocker/FileVault/LUKS |
| Firewall | 20 | Windows Firewall/UFW |
| Antivirus/EDR | 25 | Defender/endpoint agent |
| Screen Lock | 15 | OS policy |
| OS Supported | 15 | Platform detection |

## Output Schema

```json
{
  "hostname": "WORKSTATION-01",
  "posture": {"score": 85, "compliance": "COMPLIANT"},
  "recommendations": ["Enable disk encryption"]
}
```

---

## Standards and Controls

## NIST SP 800-207: Zero Trust Architecture
- **Section 2, Tenet 5**: "The enterprise monitors and measures the integrity and security posture of all owned and associated assets"
- **Section 3.3**: Agent/Gateway Model includes device health as access input
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-207/final

## CISA Zero Trust Maturity Model v2.0 - Device Pillar
- **Traditional**: Limited visibility into device health
- **Initial**: Compliance enforcement via MDM
- **Advanced**: Continuous monitoring with automated remediation
- **Optimal**: Real-time posture integrated into every access decision
- **URL**: https://www.cisa.gov/zero-trust-maturity-model

## NIST SP 800-124r2: Guidelines for Managing Mobile Device Security
- **Section 3.2**: Device compliance checking requirements
- **Section 4.1**: MDM security capabilities for posture enforcement
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-124/rev-2/final

## CrowdStrike ZTA Documentation
- **ZTA Overview**: https://www.crowdstrike.com/products/zero-trust-protection/
- **ZTA API**: https://falcon.crowdstrike.com/documentation/156/zero-trust-assessment-apis
- **ZTA Scoring Methodology**: OS signals + sensor configuration signals

## Microsoft Intune Compliance
- **Compliance Policies**: https://learn.microsoft.com/en-us/mem/intune/protect/device-compliance-get-started
- **Conditional Access Integration**: https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-grant
- **Device Health Attestation**: https://learn.microsoft.com/en-us/windows/security/operating-system-security/system-security/protect-high-value-assets-by-controlling-the-health-of-windows-10-based-devices

## Jamf Pro Compliance
- **Smart Groups**: https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Smart_Groups.html
- **Compliance Reporter**: https://learn.jamf.com/en-US/bundle/jamf-compliance-editor-documentation/page/Jamf_Compliance_Editor.html

## HIPAA Security Rule (45 CFR 164.312)
- **(a)(1)**: Access control - device posture as access control mechanism
- **(d)**: Device and media controls - encryption and integrity requirements

---

## Workflows

## Phase 1: Baseline Assessment (Week 1)

### 1.1 Inventory Current State
1. Export all managed devices from Intune/Jamf/SCCM
2. Identify unmanaged devices accessing corporate resources
3. Document OS distribution, patch levels, and encryption status
4. Measure current compliance rate before enforcement

### 1.2 Define Posture Requirements
1. Establish minimum requirements per device tier:
   - **Tier 1 (Basic)**: OS updated within 90 days, screen lock enabled
   - **Tier 2 (Standard)**: Disk encryption, firewall, antivirus, OS within 60 days
   - **Tier 3 (Enhanced)**: EDR running, ZTA score >= 70, OS within 30 days, TPM/Secure Boot
   - **Tier 4 (Critical)**: ZTA score >= 90, fully managed, patched within 7 days
2. Map application sensitivity to required posture tier
3. Define grace periods for remediation (24h standard, 4h for critical)

## Phase 2: MDM Policy Configuration (Week 2-3)

### 2.1 Intune Compliance Policies
1. Create Windows compliance policy: BitLocker, Secure Boot, TPM, Defender, OS version
2. Create macOS compliance policy: FileVault, Gatekeeper, SIP, Firewall
3. Create iOS/Android compliance policy: Encryption, PIN, jailbreak detection
4. Configure non-compliance actions: email notification, mark non-compliant, block after grace
5. Assign policies to device groups

### 2.2 Jamf Pro Configuration
1. Create smart groups for compliant/non-compliant macOS devices
2. Configure compliance criteria: FileVault, SIP, Gatekeeper, OS version
3. Set up automated remediation scripts for common issues
4. Configure compliance reporting to Jamf Protect or SIEM

## Phase 3: EDR Integration (Week 3-4)

### 3.1 CrowdStrike ZTA Setup
1. Enable Zero Trust Assessment module in Falcon console
2. Configure ZTA score thresholds per access tier
3. Set up API integration for ZTNA platform (Zscaler, Cloudflare, Okta)
4. Create host groups for ZTA monitoring
5. Build dashboard for ZTA score distribution

### 3.2 Microsoft Defender for Endpoint
1. Enable device risk assessment in Defender Security Center
2. Configure risk levels: Low, Medium, High, Critical
3. Integrate with Intune compliance via Defender connector
4. Set up conditional access policy consuming device risk signal

## Phase 4: Conditional Access Configuration (Week 4-5)

### 4.1 Entra ID Conditional Access
1. Create policy: Require compliant device for all cloud apps
2. Create policy: Block high-risk devices from sensitive apps
3. Create policy: Require MFA + compliant device for admin portals
4. Configure break-glass exclusions for emergency access
5. Start in report-only mode, then switch to enforcement

### 4.2 Okta Device Trust
1. Configure device trust integration with MDM platforms
2. Create device assurance policies with CrowdStrike integration
3. Set up authentication policies requiring device trust
4. Test with enrolled and non-enrolled devices

## Phase 5: Monitoring and Remediation (Ongoing)

1. Build compliance dashboard showing real-time posture across fleet
2. Configure alerts for posture drift (encryption disabled, EDR stopped)
3. Automate remediation: push encryption enablement, deploy patches
4. Generate weekly compliance reports for security leadership
5. Conduct monthly review of posture requirements vs. threat landscape

---

## Working Template

## Organization Information
| Field | Value |
|-------|-------|
| Organization | HealthCorp Medical |
| Total Endpoints | 2,000 |
| MDM Platform | Microsoft Intune (Windows), Jamf Pro (macOS) |
| EDR Platform | CrowdStrike Falcon |
| IdP | Microsoft Entra ID |

## Device Posture Tiers

### Tier 1: Basic Access (General Applications)
| Requirement | Windows | macOS | iOS/Android |
|------------|---------|-------|-------------|
| OS Version | >= 10.0.19045 | >= 14.0 | Latest -2 |
| Screen Lock | Enabled | Enabled | Enabled (6-digit PIN) |
| Encryption | Recommended | Recommended | Required |
| Firewall | Enabled | Enabled | N/A |
| CrowdStrike ZTA | >= 50 | >= 50 | N/A |
| Applications | Email, Wiki, Chat | Email, Wiki, Chat | Email, Chat |

### Tier 2: Standard Access (Business Applications)
| Requirement | Windows | macOS |
|------------|---------|-------|
| OS Version | >= 10.0.22621 | >= 14.0 |
| Screen Lock | Enabled, 5min timeout | Enabled, 5min timeout |
| Disk Encryption | BitLocker Required | FileVault Required |
| Firewall | Enabled | Enabled |
| Antivirus | Defender Active | XProtect Active |
| CrowdStrike ZTA | >= 65 | >= 65 |
| Secure Boot | Required | N/A |
| Applications | CRM, Internal Tools, Intranet | CRM, Internal Tools, Intranet |

### Tier 3: Enhanced Access (Sensitive Data)
| Requirement | Windows | macOS |
|------------|---------|-------|
| OS Version | >= 10.0.22631 (latest) | >= 15.0 (latest) |
| Disk Encryption | BitLocker + TPM | FileVault + Secure Enclave |
| CrowdStrike ZTA | >= 80 | >= 80 |
| Patch Level | Within 14 days of release | Within 14 days of release |
| Admin Approval | Device admin-approved | Device admin-approved |
| MDM Managed | Required | Required |
| Applications | Financial Systems, HR Data, Source Code | Financial Systems, HR Data |

### Tier 4: Critical Access (Regulated Data)
| Requirement | Windows | macOS |
|------------|---------|-------|
| CrowdStrike ZTA | >= 90 | >= 90 |
| Patch Level | Within 7 days | Within 7 days |
| Code Integrity | HVCI Enabled | SIP Enabled |
| Certificate | Corporate certificate present | Corporate certificate present |
| Geo Restriction | US only | US only |
| Applications | Patient Records (HIPAA), PCI Data | Patient Records (HIPAA) |

## Compliance Policy Assignments

| Policy | Device Group | Grace Period | Non-Compliance Action |
|--------|-------------|-------------|----------------------|
| Tier 1 Baseline | All Managed Devices | 72 hours | Email notification |
| Tier 2 Standard | Corporate Workstations | 48 hours | Mark non-compliant |
| Tier 3 Enhanced | Sensitive Data Users | 24 hours | Block access |
| Tier 4 Critical | HIPAA/PCI Users | 4 hours | Block access + alert SOC |

## CrowdStrike ZTA Score Mapping

| ZTA Score Range | Access Tier | Conditional Access Action |
|----------------|-------------|--------------------------|
| 90-100 | Tier 4 (Critical) | Allow all applications |
| 80-89 | Tier 3 (Enhanced) | Allow up to sensitive apps |
| 65-79 | Tier 2 (Standard) | Allow business apps only |
| 50-64 | Tier 1 (Basic) | Allow general apps only |
| < 50 | BLOCKED | Block all access, notify IT |

## Current Compliance Dashboard

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Overall Compliance Rate | >= 95% | 93.2% | At Risk |
| Encryption Coverage | 100% | 97.8% | On Track |
| EDR Coverage | 100% | 99.1% | On Track |
| Average ZTA Score | >= 75 | 78.4 | Meeting |
| Devices Below ZTA 50 | 0 | 34 | Action Needed |
| Stale Devices (>30d) | < 1% | 0.8% | Meeting |
| Patch Compliance (14d) | >= 90% | 87.3% | At Risk |

## Remediation Actions

| Issue | Automated Remediation | Manual Escalation |
|-------|----------------------|-------------------|
| BitLocker Disabled | Intune policy pushes enablement | IT ticket after 24h |
| FileVault Disabled | Jamf policy enables FileVault | IT ticket after 24h |
| OS Outdated | Intune/Jamf pushes update | IT ticket after 48h |
| CrowdStrike Stopped | Auto-restart via watchdog | SOC alert after 30min |
| Firewall Disabled | GPO re-enables | IT ticket after 4h |

## Sign-Off

| Role | Name | Date | Approved |
|------|------|------|----------|
| CISO | _________________ | __________ | [ ] |
| IT Operations Director | _________________ | __________ | [ ] |
| Compliance Officer | _________________ | __________ | [ ] |
