# Operating Havoc C2

## API Reference

Source: Havoc Documentation (https://havocframework.com/docs) and Demon console.

## Build (from source)

| Command | Description |
|---------|-------------|
| `git clone https://github.com/HavocFramework/Havoc.git` | Clone the framework |
| `make ts-build` | Build the team server binary |
| `make client-build` | Build the Qt client binary |

## Team server

| Command / flag | Description |
|----------------|-------------|
| `./havoc server --profile FILE.yaotl` | Run team server with a Yaotl profile |
| `-v`, `--verbose` | Show timestamps with messages |
| `--debug` | Detailed operational logging |
| `--debug-dev` | Compile agents with debug output |
| `-d`, `--default` | Use built-in configuration values |
| `./havoc client` | Launch the operator GUI client |

## Yaotl profile blocks

| Block | Purpose |
|-------|---------|
| `Teamserver { Host, Port, Build {...} }` | Bind address/port and compiler/nasm paths |
| `Operators { user "name" { Password } }` | Operator accounts |
| `Listeners { Http {...} / Smb {...} }` | HTTP(S) and SMB listeners |
| `Demon { Sleep, Jitter, Injection {...} }` | Demon agent defaults |

## Demon agent commands

| Command | Description |
|---------|-------------|
| `whoami`, `pwd`, `ls`, `ps`, `ipconfig` | Situational awareness |
| `getprivs`, `token list` | Privilege/token enumeration |
| `download FILE` / `upload SRC DST` | File transfer |
| `dotnet inline-execute ASM ARGS` | Run a .NET assembly in-memory |
| `inline-execute BOF.o ARGS` | Run a Beacon Object File |
| `shellcode inject ARCH PID FILE` | Inject shellcode into a process |
| `proc create PATH` | Spawn a sacrificial process |
| `socks add PORT` | Start a SOCKS5 proxy through the Demon |
| `rportfwd add LPORT RHOST RPORT` | Reverse port forward |
| `rm FILE` | Delete a file |
| `exit` | Terminate the agent |

## Payload generation (GUI: Attack -> Payload)

| Option | Values |
|--------|--------|
| Format | Windows Exe / Dll / Shellcode / Service Exe |
| Architecture | x64 / x86 |
| Sleep / Jitter | seconds / percent |
| Indirect Syscalls | Enabled (Hell's Gate / Halo's Gate) |
| Sleep Technique | Ekko / Zilean / WaitForSingleObjectEx |
| Stack Spoofing | Enabled / Disabled |
| Proxy Loading | Enabled / Disabled |

---

## Standards and Controls

## MITRE ATT&CK

| ID | Name | Rationale |
|----|------|-----------|
| T1071.001 | Application Layer Protocol: Web Protocols | The Havoc Demon's HTTP(S) listener carries C2 over web protocols to blend with legitimate traffic and evade egress filtering. |

### Related techniques exercised

| ID | Name | Rationale |
|----|------|-----------|
| T1027.007 | Obfuscated Files or Information: Dynamic API Resolution | The Demon resolves syscalls indirectly (Hell's/Halo's Gate) to bypass user-mode hooks. |
| T1620 | Reflective Code Loading | `dotnet inline-execute` and BOFs run code in-memory without touching disk. |
| T1055 | Process Injection | The Demon injects shellcode into spawned/sacrificial processes. |
| T1090.001 | Proxy: Internal Proxy | SOCKS and reverse port-forwards route operator traffic through the compromised host. |

## NIST CSF 2.0

| ID | Name | Rationale |
|----|------|-----------|
| DE.CM-01 | Networks and network services are monitored to find potentially adverse events | This skill validates that network and endpoint monitoring detect Havoc's HTTP(S) C2 and in-memory evasion techniques, the controls DE.CM-01 governs. |

## References

- Havoc Framework: https://github.com/HavocFramework/Havoc
- Havoc Documentation: https://havocframework.com/docs
- MITRE ATT&CK: https://attack.mitre.org/techniques/T1071/001/
- NIST CSF 2.0: https://www.nist.gov/cyberframework
