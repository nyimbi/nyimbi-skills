# Reverse Engineering IOS App With Frida

## API Reference

## Frida CLI Tools

| Command | Description |
|---------|-------------|
| `frida-ps -Ua` | List running apps on USB device |
| `frida -U -n AppName -e "script"` | Attach to app and run script |
| `frida -U -f com.app.bundle -l script.js` | Spawn app with script |
| `frida-trace -U -n AppName -m "*[ClassName *]"` | Trace ObjC methods |
| `frida-discover -U -n AppName` | Discover available functions |

## Frida JavaScript API

| API | Description |
|-----|-------------|
| `ObjC.classes.ClassName` | Access Objective-C class |
| `ObjC.classes.Cls.$ownMethods` | List class methods |
| `Interceptor.attach(target, callbacks)` | Hook native function |
| `Interceptor.replace(target, replacement)` | Replace function implementation |
| `Module.findExportByName(null, "func")` | Find exported C function |
| `ObjC.Object(ptr)` | Wrap pointer as ObjC object |
| `Memory.readUtf8String(ptr)` | Read string from memory |

## Common iOS Security Hooks

| Target | Purpose |
|--------|---------|
| `SSLSetPeerDomainName` | Bypass SSL pinning |
| `NSFileManager fileExistsAtPath:` | Jailbreak detection |
| `CCCrypt` | Intercept encryption calls |
| `NSURLSession` | Monitor network requests |
| `SecItemCopyMatching` | Keychain access |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | stdlib | Execute frida CLI tools |
| `frida` | >=16.0 | Frida Python bindings |
| `json` | stdlib | Report generation |

## References

- Frida Documentation: https://frida.re/docs/home/
- Frida JavaScript API: https://frida.re/docs/javascript-api/
- objection: https://github.com/sensepost/objection
- OWASP Mobile Testing Guide: https://mas.owasp.org/MASTG/

---

## Standards and Controls

## OWASP Mobile Top 10 2024 Mapping

| OWASP ID | Risk | RE Assessment |
|----------|------|---------------|
| M1 | Improper Credential Usage | Extract hardcoded keys via runtime hooking |
| M7 | Insufficient Binary Protections | Assess anti-RE measures (obfuscation, anti-debug, anti-Frida) |
| M10 | Insufficient Cryptography | Hook CommonCrypto to extract keys and observe algorithms |

## OWASP MASVS v2.0 - MASVS-RESILIENCE Controls

| Control | Description | Frida Test Method |
|---------|-------------|-------------------|
| MASVS-RESILIENCE-1 | App detects and responds to reverse engineering | Test with Frida attachment, observe detection |
| MASVS-RESILIENCE-2 | App detects tampering | Modify binary, observe integrity checks |
| MASVS-RESILIENCE-3 | App uses obfuscation | Assess class/method name readability |
| MASVS-RESILIENCE-4 | App detects debuggers | Attach debugger, check ptrace/sysctl hooks |

## CWE Mappings

| CWE ID | Title | RE Discovery Method |
|--------|-------|-------------------|
| CWE-798 | Use of Hard-coded Credentials | Hook string initialization, NSUserDefaults access |
| CWE-321 | Use of Hard-coded Cryptographic Key | Hook CCCrypt, SecKeyCreateWithData |
| CWE-327 | Broken Crypto Algorithm | Observe algorithm parameter in CCCrypt calls |
| CWE-693 | Protection Mechanism Failure | Bypass jailbreak detection, Frida detection |

---

## Workflows

## Workflow 1: Full iOS RE Pipeline

```
[Obtain IPA/binary] --> [Decrypt FairPlay] --> [Static analysis] --> [Dynamic analysis]
                              |                      |                      |
                       [frida-ios-dump]        [class-dump]          [frida-trace]
                       [Clutch]                [Ghidra]              [Custom hooks]
                                               [Hopper]             [Method interception]
                                                                           |
                                                                    [Extract secrets]
                                                                    [Map logic flow]
                                                                    [Document findings]
```

## Workflow 2: Crypto Key Extraction

```
[Hook CommonCrypto] --> [Capture CCCrypt calls] --> [Extract key material]
                              |
                       [Log algorithm, mode, IV]
                       [Log input/output data]
                              |
                       [Reconstruct protocol]
                       [Document encryption scheme]
```

## Decision Matrix: iOS RE Approach

| Binary Type | Static Tool | Dynamic Tool | Notes |
|-------------|------------|-------------|-------|
| Objective-C | class-dump + Ghidra | Frida ObjC.classes | Full runtime visibility |
| Swift (NSObject-based) | dsdump + Ghidra | Frida ObjC.classes | Partial visibility |
| Pure Swift | Ghidra + Swift demangling | Frida Module.enumerateExports | Limited runtime access |
| C/C++ native | Ghidra | Frida Interceptor.attach | Address-based hooking |

---

## Working Template

## Target Application
| Field | Value |
|-------|-------|
| App Name | [NAME] |
| Bundle ID | [BUNDLE_ID] |
| Binary Type | [Objective-C/Swift/Mixed] |
| iOS Version | [VERSION] |
| FairPlay Encrypted | [YES/NO] |
| Analysis Date | [DATE] |

## Class Enumeration
| Class Name | Method Count | Category |
|-----------|-------------|----------|
| [CLASS] | [N] | [Auth/Crypto/Network/Storage] |

## Hooked Methods and Findings
### [METHOD_SIGNATURE]
- **Arguments observed**: [ARGS]
- **Return values**: [RETURNS]
- **Security implication**: [DESCRIPTION]

## Extracted Secrets
| Type | Location | Value (redacted) | Risk |
|------|----------|-----------------|------|
| [API Key/Token/Password] | [CLASS.METHOD] | [REDACTED] | [RISK] |

## Binary Protection Assessment
| Protection | Status | Details |
|-----------|--------|---------|
| Jailbreak Detection | [Present/Absent] | [DETAILS] |
| Frida Detection | [Present/Absent] | [DETAILS] |
| Code Obfuscation | [Yes/No] | [DETAILS] |
| Anti-Debug | [Present/Absent] | [DETAILS] |

## Recommendations
1. [RECOMMENDATION]
