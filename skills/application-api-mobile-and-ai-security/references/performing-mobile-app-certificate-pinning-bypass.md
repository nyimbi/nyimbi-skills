# Performing Mobile App Certificate Pinning Bypass

## API Reference

## Libraries Used
- **subprocess**: Execute frida, objection, apktool, adb commands
- **pathlib**: Read decompiled APK smali files

## CLI Interface
```
python agent.py detect --apk app.apk
python agent.py frida --package com.example.app [--device emulator-5554]
python agent.py objection --package com.example.app
python agent.py proxy
```

## Core Functions

### `detect_pinning_implementation(apk_path)` — Static APK analysis
Decompiles APK with apktool. Searches smali for pinning indicators:
OkHttp CertificatePinner, X509TrustManager, network_security_config,
WebView SSL error handler, Conscrypt TrustManagerImpl, Certificate Transparency.

### `run_frida_bypass(package_name, device_id)` — Dynamic Frida bypass
Injects JavaScript to bypass: TrustManagerImpl.verifyChain, OkHttp CertificatePinner.check,
WebViewClient.onReceivedSslError.

### `run_objection_bypass(package_name)` — Objection framework bypass
Runs `android sslpinning disable` via objection exploration mode.

### `check_proxy_setup()` — Verify interception environment
Checks: Android proxy settings, system CA certificates, user-installed CA certs.

## Pinning Strength Classification
| Level | Criteria |
|-------|----------|
| STRONG | 3+ pinning implementations detected |
| MODERATE | 1-2 implementations |
| NONE | No pinning indicators found |

## Dependencies
```
pip install frida-tools objection
```
System: apktool, adb (Android Debug Bridge)

---

## Standards and Controls

## OWASP Mobile Top 10 2024
| ID | Risk | Relevance |
|----|------|-----------|
| M5 | Insecure Communication | Pinning assessment as part of network security |
| M7 | Insufficient Binary Protections | Pinning as binary-level protection |

## OWASP MASVS v2.0
| Control | Description |
|---------|-------------|
| MASVS-NETWORK-1 | App uses TLS for all network communication |
| MASVS-NETWORK-2 | App performs certificate pinning for critical connections |
| MASVS-RESILIENCE-1 | App detects and responds to running in instrumented environment |

## CWE Mappings
| CWE | Title |
|-----|-------|
| CWE-295 | Improper Certificate Validation |
| CWE-297 | Improper Validation of Certificate with Host Mismatch |

---

## Workflows

## Workflow 1: Escalating Bypass Approach
```
[Configure Burp proxy] --> [App connection fails?] --> [Yes: Pinning active]
                                                              |
                                          [Try Objection generic bypass]
                                                              |
                                                    [Traffic visible?]
                                                    /              \
                                              [Yes: Done]    [No: Advanced]
                                                              |
                                          [Identify pinning library]
                                          [frida-trace *Trust* *Pin*]
                                                              |
                                          [Write custom Frida script]
                                          [Target specific implementation]
                                                              |
                                          [Verify traffic capture]
```

## Decision Matrix
| Pinning Method | Bypass Tool | Difficulty |
|---------------|-------------|-----------|
| OkHttp CertificatePinner | Objection | Easy |
| Network Security Config | Manifest modification | Easy |
| Custom TrustManager | Frida hook | Medium |
| TrustKit | Objection or Frida | Medium |
| Native C/C++ validation | Frida Interceptor.attach | Hard |
| Certificate Transparency | Custom Frida script | Hard |

---

## Working Template

## Target
| Field | Value |
|-------|-------|
| Application | [APP_NAME] |
| Platform | [Android/iOS] |
| Pinning Method | [OkHttp/TrustManager/NSURLSession/TrustKit/Custom] |
| Bypass Method | [Objection/Frida/Manual] |
| Bypass Difficulty | [Easy/Medium/Hard] |

## Pinning Implementation Analysis
| Layer | Implementation | Bypass Status |
|-------|---------------|---------------|
| [Java/ObjC/Native] | [DETAILS] | [Bypassed/Not Bypassed] |

## Findings
1. [FINDING]

## Recommendations
1. [RECOMMENDATION]
