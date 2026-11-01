# Performing Thick Client Application Penetration Test

## API Reference

## Analysis Tools

| Tool | Purpose | Target |
|------|---------|--------|
| dnSpy | .NET decompilation and debugging | .NET Framework/Core apps |
| ILSpy | .NET decompilation (read-only) | .NET assemblies |
| JD-GUI / JADX | Java decompilation | JAR/APK files |
| Ghidra / IDA Pro | Native binary reverse engineering | C/C++ executables |
| Procmon | File/registry/network activity monitoring | Any Windows app |
| Process Hacker | Process inspection, memory, DLLs | Running processes |
| Burp Suite | HTTP/HTTPS traffic interception | Client-server communication |
| Echo Mirage | TCP/UDP traffic interception | Non-HTTP protocols |
| Frida | Dynamic instrumentation | Any platform |

## Static Analysis Targets

| Target | Search Pattern | Risk |
|--------|---------------|------|
| Hardcoded credentials | `password`, `secret`, `apikey` in strings | Critical |
| Connection strings | `jdbc:`, `Server=`, `mongodb://` | Critical |
| SQL queries | `SELECT`, `INSERT`, `UPDATE` | Medium |
| URLs and endpoints | `http://`, `https://` | Info |
| Disabled SSL validation | `ServerCertificateValidationCallback` | High |

## DLL Hijacking Detection

| Step | Tool | Action |
|------|------|--------|
| 1 | Procmon | Filter: `Result = NAME NOT FOUND`, `Path ends with .dll` |
| 2 | Check | Verify if DLL search path includes writable directories |
| 3 | Validate | Test with benign DLL in writable directory |

## Local Storage Locations

| Location | Type | Risk |
|----------|------|------|
| `%APPDATA%\<app>` | Config, SQLite | Credential storage |
| `%LOCALAPPDATA%\<app>` | Cache, logs | Data leakage |
| `HKCU\Software\<app>` | Registry settings | Stored credentials |
| App install directory | Config files | Hardcoded secrets |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `sqlite3` | stdlib | Audit local SQLite databases |
| `re` | stdlib | Pattern matching for credentials/URLs |
| `subprocess` | stdlib | Execute system analysis tools |
| `pathlib` | stdlib | File system traversal |

## References

- OWASP Thick Client Top 10: https://owasp.org/www-project-thick-client-top-10/
- dnSpy: https://github.com/dnSpy/dnSpy
- Procmon: https://learn.microsoft.com/en-us/sysinternals/downloads/procmon
- Frida: https://frida.re/docs/home/

---

## Standards and Controls

## Frameworks
- OWASP Thick Client Top 10: https://owasp.org/www-project-thick-client-top-10/
- PTES Application Security: http://www.pentest-standard.org/
- CWE Top 25: https://cwe.mitre.org/top25/

## OWASP Thick Client Top 10
1. Improper Platform Usage
2. Insecure Data Storage
3. Insecure Communication
4. Insecure Authentication
5. Insufficient Cryptography
6. Insecure Authorization
7. Client Code Quality
8. Code Tampering
9. Reverse Engineering
10. Extraneous Functionality

---

## Workflows

## Attack Flow
```
Application Binary
    │
    ├── Static Analysis (dnSpy/Ghidra/JD-GUI)
    │   ├── Hardcoded credentials
    │   ├── Encryption analysis
    │   └── API endpoint discovery
    │
    ├── Dynamic Analysis (Procmon/Process Hacker)
    │   ├── File system monitoring
    │   ├── Registry access tracking
    │   └── Memory inspection
    │
    ├── Traffic Interception (Burp/Fiddler/Echo Mirage)
    │   ├── API security testing
    │   ├── Certificate pinning bypass
    │   └── Authentication token analysis
    │
    └── Binary Exploitation
        ├── DLL hijacking
        ├── Memory manipulation
        └── Binary patching
```

---

## Working Template

## Document Control
| Field | Value |
|-------|-------|
| Application | [Name and version] |
| Technology | [.NET / Java / C++ / Electron] |
| Platform | [Windows / macOS / Linux] |
| Period | [Start] — [End] |

## Executive Summary
[Overview of thick client security posture, key vulnerabilities found in binary, storage, and communication]

## Findings
### Finding [N]: [Title]
| Attribute | Detail |
|-----------|--------|
| Category | [Binary / Storage / Communication / Authentication] |
| Severity | [Level] |
| CVSS | [Score] |
| Remediation | [Fix] |

## Recommendations
1. [Priority recommendations for thick client hardening]
