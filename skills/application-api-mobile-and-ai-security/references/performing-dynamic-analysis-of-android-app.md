# Performing Dynamic Analysis Of Android App

## API Reference

## Libraries Used
- **frida**: Dynamic instrumentation for runtime hooking and SSL pinning detection
- **subprocess**: ADB commands for package management, traffic capture, component analysis

## CLI Interface

```
python agent.py [--device <id>] packages
python agent.py [--device <id>] ssl --package <pkg>
python agent.py [--device <id>] components --package <pkg>
python agent.py [--device <id>] storage --package <pkg>
python agent.py [--device <id>] network [--duration 30]
```

## Core Functions

### `check_ssl_pinning(package_name, device_id)`
Uses Frida to hook TrustManagerImpl and OkHostnameVerifier to detect SSL pinning.

### `analyze_exported_components(package_name, device_id)`
Runs `dumpsys package` to enumerate exported activities, services, receivers, providers.

### `check_data_storage(package_name, device_id)`
Checks shared_prefs and world-readable files via `run-as` for insecure storage.

### `capture_network_traffic(device_id, duration, output)`
Runs `tcpdump` on device and pulls pcap via ADB.

## Frida API Calls
- `frida.get_usb_device()` — Connect to USB device
- `device.spawn([package])` — Launch app
- `session.create_script(js)` — Inject JavaScript
- `script.on("message", callback)` — Receive hook results

## Dependencies
```
pip install frida frida-tools
# ADB must be installed and device connected
```

---

## Standards and Controls

## OWASP Mobile Top 10 2024 Mapping

| OWASP ID | Risk | Dynamic Analysis Coverage |
|----------|------|--------------------------|
| M1 | Improper Credential Usage | Intercept credentials at runtime, dump keystore |
| M3 | Insecure Authentication/Authorization | Hook auth methods, observe token generation |
| M5 | Insecure Communication | Monitor network calls, intercept decrypted payloads |
| M7 | Insufficient Binary Protections | Test root detection, Frida detection, tamper checks |
| M8 | Security Misconfiguration | Explore exported components, test IPC endpoints |
| M10 | Insufficient Cryptography | Hook Cipher/MessageDigest to observe crypto operations |

## OWASP MASVS v2.0 Control Mapping

| MASVS Category | Dynamic Test | Method |
|----------------|-------------|--------|
| MASVS-STORAGE | Runtime data extraction | Heap inspection, memory search |
| MASVS-CRYPTO | Algorithm observation | Hook javax.crypto.Cipher |
| MASVS-AUTH | Auth flow analysis | Hook login/token methods |
| MASVS-NETWORK | Traffic monitoring | Hook OkHttp, HttpURLConnection |
| MASVS-PLATFORM | IPC testing | Drozer, intent fuzzing |
| MASVS-RESILIENCE | Protection bypass | Root/Frida/debug detection bypass |

## OWASP MASTG Dynamic Test Cases

| Test ID | Description | Tool |
|---------|-------------|------|
| MASTG-TEST-0001 | Testing Local Storage (Runtime) | Objection, Frida |
| MASTG-TEST-0010 | Testing Custom URL Schemes | Frida hooks, ADB |
| MASTG-TEST-0013 | Testing WebView Security | Hook WebView methods |
| MASTG-TEST-0029 | Testing Root Detection | Frida bypass scripts |
| MASTG-TEST-0038 | Testing Anti-Debugging | ptrace hooks, Frida detection |

## CWE Mappings

| CWE ID | Title | Dynamic Detection |
|--------|-------|-------------------|
| CWE-312 | Cleartext Storage | Memory search for plaintext secrets |
| CWE-319 | Cleartext Transmission | Network method hooking |
| CWE-327 | Broken Crypto Algorithm | Cipher.getInstance() hooking |
| CWE-489 | Active Debug Code | Debug flag detection at runtime |
| CWE-693 | Protection Mechanism Failure | Root/tamper detection bypass |

---

## Workflows

## Workflow 1: Complete Android Dynamic Assessment

```
[Setup Frida Server] --> [Enumerate app surface] --> [Hook sensitive methods]
                                                            |
                                             +--------------+--------------+
                                             |              |              |
                                      [Auth hooks]   [Crypto hooks]  [Network hooks]
                                      [Login flow]   [Cipher ops]    [API calls]
                                      [Token mgmt]   [Key generation] [URL requests]
                                             |              |              |
                                             +--------------+--------------+
                                                            |
                                                     [Root detection test]
                                                     [Tamper detection test]
                                                     [Debug detection test]
                                                            |
                                                     [Memory/heap analysis]
                                                     [Extract runtime secrets]
                                                            |
                                                     [Document findings]
```

## Workflow 2: Protection Bypass Pipeline

```
[App refuses to run] --> [Identify protection]
                               |
              +----------------+----------------+
              |                |                |
       [Root detection]  [Frida detection]  [Emulator detection]
              |                |                |
       [File checks?]   [Port scan?]      [Build.prop?]
       [su binary?]     [Memory scan?]    [IMEI check?]
       [RootBeer?]      [Process name?]   [Sensor data?]
              |                |                |
       [Bypass script]  [Custom Frida]    [Prop override]
              |                |                |
              +----------------+----------------+
                               |
                        [Verify bypass works]
                        [Continue assessment]
```

## Decision Matrix: Hooking Strategy

| Scenario | Tool | Approach |
|----------|------|----------|
| Quick reconnaissance | Objection | `android hooking watch class` |
| Specific method analysis | Frida script | Custom JavaScript hook |
| Crypto algorithm discovery | frida-trace | Auto-trace javax.crypto.* |
| Memory forensics | Objection | `memory search` / `memory dump` |
| IPC testing | Drozer | Module-based component testing |
| Network analysis | Frida + Burp | Hook + proxy combination |

---

## Working Template

## Target Application

| Field | Value |
|-------|-------|
| Package Name | [PACKAGE] |
| Version | [VERSION] |
| Target SDK | [SDK] |
| Device | [MODEL] / Android [VERSION] |
| Rooted | [YES/NO] |
| Analysis Date | [DATE] |

## Component Enumeration

| Type | Count | Exported | Notable |
|------|-------|----------|---------|
| Activities | [N] | [N] | [DETAILS] |
| Services | [N] | [N] | [DETAILS] |
| Receivers | [N] | [N] | [DETAILS] |
| Providers | [N] | [N] | [DETAILS] |

## Runtime Security Findings

### Finding [N]: [TITLE]
- **Severity**: [LEVEL]
- **OWASP Mobile**: [M-ID]
- **Category**: [MASVS-CATEGORY]
- **Description**: [DESCRIPTION]
- **Evidence**: [RUNTIME_OUTPUT]
- **Recommendation**: [REMEDIATION]

## Protection Assessment

| Protection | Status | Bypass Difficulty |
|-----------|--------|------------------|
| Root Detection | [Present/Absent] | [Easy/Medium/Hard] |
| SSL Pinning | [Present/Absent] | [Easy/Medium/Hard] |
| Frida Detection | [Present/Absent] | [Easy/Medium/Hard] |
| Debug Detection | [Present/Absent] | [Easy/Medium/Hard] |
| Emulator Detection | [Present/Absent] | [Easy/Medium/Hard] |
| Tamper Detection | [Present/Absent] | [Easy/Medium/Hard] |

## Recommendations

1. [RECOMMENDATION]
