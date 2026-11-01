# Analyzing IOS App Security With Objection

## API Reference

## Objection CLI

### Launch
```bash
objection -g com.example.app explore          # Attach to running app
objection -g com.example.app explore -s "command"  # Run startup command
objection patchipa --source app.ipa           # Patch IPA with Frida gadget
```

### Keychain & Data Storage
```bash
ios keychain dump                    # Dump keychain items
ios keychain dump --json             # JSON output
ios cookies get                      # List HTTP cookies
ios nsuserdefaults get               # Read NSUserDefaults
ios plist cat Info.plist             # Read plist file
```

### SSL Pinning
```bash
ios sslpinning disable               # Bypass SSL pinning
ios sslpinning disable --quiet        # Quiet mode
```

### Jailbreak Detection
```bash
ios jailbreak disable                 # Bypass jailbreak detection
ios jailbreak simulate                # Simulate jailbroken device
```

### Hooking
```bash
ios hooking list classes                        # List all classes
ios hooking list classes --include Auth          # Filter classes
ios hooking list class_methods ClassName         # List methods
ios hooking watch method "-[Class method]"       # Watch method calls
ios hooking set return_value "-[Class isJB]" false  # Override return
```

### Filesystem
```bash
ls /                                  # List app sandbox root
ls /Documents                         # List Documents directory
file download /path/to/file local.out  # Download file
file upload local.file /remote/path    # Upload file
```

### Memory
```bash
memory dump all dump.bin              # Dump all memory
memory search "password"              # Search memory for string
memory list modules                   # List loaded modules
memory list exports libModule.dylib   # List module exports
```

## Frida CLI

### Syntax
```bash
frida -U -n AppName                   # Attach by name
frida -U -f com.app.id                # Spawn and attach
frida -U -n AppName -l script.js      # Load script
frida-ps -U                           # List running processes
frida-ls-devices                      # List connected devices
```

### Common Frida Scripts
```javascript
// Hook method and log arguments
ObjC.choose(ObjC.classes.ClassName, {
    onMatch: function(instance) {
        Interceptor.attach(instance['- methodName:'].implementation, {
            onEnter: function(args) {
                console.log('arg1:', ObjC.Object(args[2]));
            }
        });
    }, onComplete: function() {}
});
```

## OWASP Mobile Top 10 (2024)

| ID | Category | Objection Check |
|----|----------|-----------------|
| M1 | Improper Credential Usage | `ios keychain dump` |
| M2 | Inadequate Supply Chain Security | Binary analysis |
| M3 | Insecure Authentication | Hook auth classes |
| M4 | Insufficient Input/Output Validation | Hook input methods |
| M5 | Insecure Communication | `ios sslpinning disable` |
| M6 | Inadequate Privacy Controls | `ios nsuserdefaults get` |
| M7 | Insufficient Binary Protections | Check PIE, ARC, stack canary |
| M8 | Security Misconfiguration | `ios plist cat Info.plist` |
| M9 | Insecure Data Storage | Filesystem + keychain review |
| M10 | Insufficient Cryptography | Hook crypto classes |

## iOS App Sandbox Paths
| Path | Contents |
|------|----------|
| `/Documents` | User-generated data |
| `/Library/Caches` | Cached data |
| `/Library/Preferences` | Plist settings |
| `/tmp` | Temporary files |
| `/Library/Cookies` | Cookie storage |

---

## Standards and Controls

## OWASP Mobile Top 10 2024 Mapping

| OWASP ID | Risk | Objection Testing Coverage |
|----------|------|---------------------------|
| M1 | Improper Credential Usage | Keychain dumping, memory string search for hardcoded credentials |
| M3 | Insecure Authentication/Authorization | Hook authentication methods, bypass biometric checks |
| M5 | Insecure Communication | SSL pinning bypass, network class hooking |
| M7 | Insufficient Binary Protections | Jailbreak detection bypass, Frida detection assessment |
| M8 | Security Misconfiguration | Info.plist review, URL scheme analysis, ATS configuration |
| M9 | Insecure Data Storage | NSUserDefaults inspection, SQLite database access, file system review |

## OWASP MASVS v2.0 Control Mapping

| MASVS Category | Objection Commands | Assessment Area |
|----------------|-------------------|-----------------|
| MASVS-STORAGE | `ios keychain dump`, `ios nsuserdefaults get`, `sqlite connect` | Sensitive data in keychain, NSUserDefaults, databases |
| MASVS-CRYPTO | `memory search`, hook crypto framework calls | Key storage, algorithm selection |
| MASVS-AUTH | Hook LAContext, authentication classes | Biometric bypass, session management |
| MASVS-NETWORK | `ios sslpinning disable`, hook NSURLSession | Certificate pinning, cleartext traffic |
| MASVS-PLATFORM | Hook URL scheme handlers, pasteboard monitor | Deep link security, clipboard exposure |
| MASVS-CODE | `memory list modules`, binary inspection | Debugging symbols, framework analysis |
| MASVS-RESILIENCE | `ios jailbreak disable`, Frida detection hooks | Anti-tampering, anti-debugging |

## OWASP MASTG Test Cases

| Test ID | Description | Objection Approach |
|---------|-------------|-------------------|
| MASTG-TEST-0053 | Testing Local Storage for Sensitive Data | `ios keychain dump`, filesystem inspection |
| MASTG-TEST-0057 | Testing Backups for Sensitive Data | Check backup exclusion attributes |
| MASTG-TEST-0060 | Testing Custom URL Schemes | Hook `application:openURL:options:` |
| MASTG-TEST-0063 | Testing for Sensitive Data in Logs | Monitor NSLog calls via hooking |
| MASTG-TEST-0066 | Testing Enforced App Transport Security | Inspect Info.plist ATS configuration |

## Apple Platform Security Requirements

| Requirement | Assessment Method |
|-------------|-------------------|
| Keychain Access Control | Verify kSecAttrAccessible values via keychain dump |
| App Transport Security | Check Info.plist for NSAllowsArbitraryLoads exceptions |
| Data Protection API | Verify file protection attributes on sensitive files |
| Secure Enclave Usage | Hook SecKey operations for biometric-protected keys |

---

## Workflows

## Workflow 1: iOS Runtime Security Assessment

```
[Setup Environment] --> [Prepare Device] --> [Attach Objection] --> [Runtime Analysis]
       |                      |                     |                      |
       v                      v                     v                      v
[Install Frida]      [Jailbroken: Start    [Connect via USB]    [Data Storage Check]
[Install Objection]   frida-server]        [Spawn target app]   [Network Security]
                     [Non-JB: Patch IPA]                        [Auth Mechanism Review]
                                                                [Binary Protection Test]
                                                                         |
                                                                         v
                                                                [Document Findings]
                                                                [Generate Report]
```

## Workflow 2: SSL Pinning Bypass for Traffic Interception

```
[Configure Burp Proxy] --> [Set device proxy] --> [Attach Objection]
                                                        |
                                                        v
                                              [ios sslpinning disable]
                                                        |
                                                        v
                                              [Navigate app in browser/UI]
                                                        |
                                                        v
                                              [Capture HTTPS traffic in Burp]
                                              [Analyze API endpoints]
                                              [Test authentication flows]
                                              [Check for sensitive data in transit]
```

## Workflow 3: Keychain and Data Storage Assessment

```
[Attach Objection] --> [ios keychain dump] --> [Analyze keychain items]
                              |                        |
                              v                        v
                    [ios nsuserdefaults get]   [Check protection classes]
                              |               [Identify sensitive tokens]
                              v               [Verify encryption at rest]
                    [List app sandbox files]
                              |
                              v
                    [sqlite connect *.db]
                    [Query sensitive tables]
                              |
                              v
                    [memory search "password"]
                    [memory search "token"]
                    [memory search "secret"]
```

## Workflow 4: Jailbreak Detection Assessment

```
[Attach Objection] --> [ios jailbreak disable] --> [Navigate app]
                              |                          |
                              v                   [App functions normally?]
                    [Hook detection methods]        /           \
                    [Monitor file checks]       [Yes]          [No]
                    [Monitor Cydia URL scheme]    |              |
                              |               [Detection       [Additional detection
                              v                bypassed]        methods exist]
                    [Document detection                          |
                     methods found]                    [Hook deeper: search
                    [Assess bypass                      for custom checks]
                     difficulty]                       [Frida script for
                                                       targeted bypass]
```

## Decision Matrix: Testing Approach

| Device State | IPA Access | Approach |
|-------------|-----------|----------|
| Jailbroken | Not needed | Direct Frida server + Objection attach |
| Non-jailbroken | Available | Patch IPA with `objection patchipa` |
| Non-jailbroken | Not available | Request IPA from client or use device management |
| Emulator | N/A | Limited: Frida on Corellium or similar platform |

---

## Working Template

## Engagement Information

| Field | Value |
|-------|-------|
| Application | [APP_NAME] |
| Bundle ID | [BUNDLE_ID] |
| iOS Version | [IOS_VERSION] |
| Device | [DEVICE_MODEL] |
| Device State | [Jailbroken/Non-Jailbroken] |
| Assessment Date | [DATE] |
| Analyst | [ANALYST] |
| Objection Version | [VERSION] |

## Executive Summary

[Brief narrative of findings from Objection runtime analysis]

## Keychain Analysis

| Service | Account | Data Type | Protection Class | Risk |
|---------|---------|-----------|-----------------|------|
| [SERVICE] | [ACCOUNT] | [TYPE] | [CLASS] | [RISK] |

**Findings**: [Description of sensitive data found in keychain]

## Data Storage Assessment

### NSUserDefaults
| Key | Contains Sensitive Data | Risk |
|-----|----------------------|------|
| [KEY] | [YES/NO] | [RISK] |

### SQLite Databases
| Database | Encrypted | Sensitive Tables | Risk |
|----------|-----------|-----------------|------|
| [DB_NAME] | [YES/NO] | [TABLES] | [RISK] |

### Filesystem
| Path | Contents | Protection | Risk |
|------|----------|-----------|------|
| [PATH] | [DESCRIPTION] | [ATTRIBUTE] | [RISK] |

## Network Security

| Check | Result | Details |
|-------|--------|---------|
| SSL Pinning Present | [YES/NO] | [IMPLEMENTATION_DETAILS] |
| SSL Pinning Bypass | [SUCCESS/FAIL] | [METHOD_USED] |
| ATS Configuration | [STRICT/RELAXED] | [EXCEPTIONS] |

## Binary Protection Assessment

| Protection | Status | Details |
|-----------|--------|---------|
| Jailbreak Detection | [Present/Absent] | [BYPASS_DIFFICULTY] |
| Frida Detection | [Present/Absent] | [DETAILS] |
| Debug Detection | [Present/Absent] | [DETAILS] |
| Code Obfuscation | [Yes/No] | [DETAILS] |

## Memory Analysis

| Search Pattern | Found | Risk | Details |
|---------------|-------|------|---------|
| Passwords | [YES/NO] | [RISK] | [DETAILS] |
| Auth Tokens | [YES/NO] | [RISK] | [DETAILS] |
| API Keys | [YES/NO] | [RISK] | [DETAILS] |
| JWTs | [YES/NO] | [RISK] | [DETAILS] |

## Recommendations

### Critical
1. [RECOMMENDATION]

### High
1. [RECOMMENDATION]

### Medium
1. [RECOMMENDATION]
