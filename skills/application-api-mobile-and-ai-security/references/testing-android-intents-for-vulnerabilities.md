# Testing Android Intents For Vulnerabilities

## API Reference

## Drozer Modules

| Module | Description |
|--------|-------------|
| `app.package.attacksurface` | Enumerate exported components |
| `app.activity.info` | List exported activities |
| `app.service.info` | List exported services |
| `app.broadcast.info` | List exported receivers |
| `app.provider.info` | List content providers |
| `app.provider.query` | Query content provider URI |
| `scanner.provider.injection` | Test for SQL injection |
| `scanner.provider.traversal` | Test for path traversal |
| `app.broadcast.send` | Send broadcast intent |
| `app.activity.start` | Start exported activity |

## ADB Intent Commands

| Command | Description |
|---------|-------------|
| `adb shell am start -n <pkg>/<activity>` | Start activity |
| `adb shell am broadcast -a <action>` | Send broadcast |
| `adb shell am startservice -n <pkg>/<svc>` | Start service |
| `adb shell content query --uri <uri>` | Query provider |
| `adb shell dumpsys package <pkg>` | Package info |

## Component Types

| Type | Risk | Test |
|------|------|------|
| Exported Activity | Auth bypass | Direct launch without intent filters |
| Content Provider | Data leakage, SQLi | Query with modified URIs |
| Broadcast Receiver | Action spoofing | Send crafted broadcasts |
| Service | Unauthorized actions | Bind/start with extras |
| PendingIntent | Hijacking | Check FLAG_MUTABLE |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | stdlib | Execute adb/drozer CLI |
| `re` | stdlib | Parse command output |
| `json` | stdlib | Report generation |

## References

- Drozer: https://github.com/WithSecureLabs/drozer
- OWASP MASTG: https://mas.owasp.org/MASTG/
- Android IPC: https://developer.android.com/guide/components/intents-filters

---

## Standards and Controls

## OWASP Mobile Top 10 2024
| ID | Risk | Intent Relevance |
|----|------|-----------------|
| M4 | Insufficient Input/Output Validation | Intent parameter injection |
| M8 | Security Misconfiguration | Exported components without permission guards |

## OWASP MASVS v2.0 - MASVS-PLATFORM
| Control | Test |
|---------|------|
| MASVS-PLATFORM-1 | Verify exported components require appropriate permissions |
| MASVS-PLATFORM-2 | Verify intent data is validated before processing |

## CWE Mappings
| CWE | Title | Vector |
|-----|-------|--------|
| CWE-926 | Improper Export of Android Application Components | Exported without permission |
| CWE-927 | Use of Implicit Intent for Sensitive Communication | Sensitive data in implicit intents |
| CWE-925 | Improper Verification of Intent by Broadcast Receiver | Missing sender verification |
| CWE-89 | SQL Injection | Content provider query injection |
| CWE-22 | Path Traversal | Content provider path traversal |

---

## Workflows

## Workflow 1: IPC Security Assessment
```
[Decompile APK] --> [Parse AndroidManifest] --> [Enumerate exported components]
                                                        |
                                     +------------------+------------------+
                                     |          |           |              |
                              [Activities] [Services]  [Receivers]  [Providers]
                              [Direct launch] [Bind/Start] [Trigger] [Query/Inject]
                              [Auth bypass?]  [Data exfil?] [Sniff?] [SQLi? Traversal?]
                                     |          |           |              |
                                     +------------------+------------------+
                                                        |
                                                 [PendingIntent audit]
                                                 [Report findings]
```

---

## Working Template

## Target
| Field | Value |
|-------|-------|
| Package | [PACKAGE] |
| Target SDK | [SDK] |
| Exported Components | [COUNT] |

## Attack Surface
| Component Type | Exported | Unprotected | Risk |
|---------------|----------|-------------|------|
| Activities | [N] | [N] | [RISK] |
| Services | [N] | [N] | [RISK] |
| Receivers | [N] | [N] | [RISK] |
| Providers | [N] | [N] | [RISK] |

## Findings
### Finding [N]: [COMPONENT_NAME]
- **Type**: [Activity/Service/Receiver/Provider]
- **Exported**: Yes
- **Permission Protected**: [YES/NO]
- **Issue**: [DESCRIPTION]
- **Severity**: [LEVEL]
- **Test Command**: `[COMMAND]`
- **Result**: [OUTCOME]
- **Recommendation**: [REMEDIATION]

## Recommendations
1. [RECOMMENDATION]
