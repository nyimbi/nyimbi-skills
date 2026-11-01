# Performing Wireless Network Penetration Test

## API Reference

## Aircrack-ng Suite

| Tool | Description |
|------|-------------|
| `airmon-ng start <iface>` | Enable monitor mode |
| `airodump-ng <mon_iface>` | Scan for wireless networks |
| `airodump-ng --bssid <bssid> -c <ch> -w <prefix> <iface>` | Capture handshake |
| `aireplay-ng -0 5 -a <bssid> <iface>` | Deauthentication attack |
| `aircrack-ng <cap> -w <wordlist>` | Crack WPA/WPA2 handshake |
| `wash -i <iface>` | Detect WPS-enabled APs |
| `reaver -i <iface> -b <bssid>` | WPS PIN brute force |

## airodump-ng CSV Fields

| Column | Description |
|--------|-------------|
| BSSID | Access point MAC address |
| Channel | Operating channel |
| Encryption | WPA2, WPA, WEP, OPN |
| ESSID | Network name |
| Power | Signal strength (dBm) |

## Encryption Risk Levels

| Encryption | Risk |
|-----------|------|
| Open (OPN) | Critical - No encryption |
| WEP | Critical - Easily crackable |
| WPA (TKIP) | High - Deprecated |
| WPA2 (CCMP) | Medium - Dictionary attacks |
| WPA3 (SAE) | Low - Current standard |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | stdlib | Execute aircrack-ng tools |
| `re` | stdlib | Parse tool output |
| `csv` | stdlib | Parse airodump CSV |

## References

- Aircrack-ng: https://www.aircrack-ng.org/doku.php
- Reaver: https://github.com/t6x/reaver-wps-fork-t6x
- WiFi Pineapple: https://www.hak5.org/products/wifi-pineapple

---

## Standards and Controls

## Standards
- IEEE 802.11: Wireless LAN standard
- WPA3 (WiFi Protected Access 3): Latest security protocol using SAE
- NIST SP 800-153: Guidelines for Securing Wireless Local Area Networks
- PCI DSS v4.0 Req 11.2: Wireless access point detection

## Wireless Encryption Comparison
| Protocol | Key Management | Crackable | Notes |
|----------|---------------|-----------|-------|
| WEP | Static IV | Trivially | Deprecated, never use |
| WPA-TKIP | PSK/Enterprise | Possible | Legacy, avoid |
| WPA2-PSK | PBKDF2/CCMP | Dictionary attacks | Requires strong passphrase |
| WPA2-Enterprise | 802.1X/RADIUS | Certificate attacks | Recommended with cert pinning |
| WPA3-SAE | Dragonfly handshake | Resistant | Best current option |

## Tools
| Tool | Purpose |
|------|---------|
| Aircrack-ng | Full wireless testing suite |
| Kismet | Wireless IDS and scanner |
| Bettercap | Network attack framework |
| Wifite | Automated WiFi attack tool |
| hcxdumptool | PMKID capture |
| Reaver | WPS PIN bruteforce |

---

## Workflows

## Attack Flow
```
Monitor Mode Activation
    │
    ├── Passive Reconnaissance
    │   ├── SSID/BSSID discovery
    │   ├── Client enumeration
    │   └── Channel mapping
    │
    ├── WPA2-PSK Attacks
    │   ├── Handshake capture (deauth + capture)
    │   ├── PMKID attack (clientless)
    │   └── Offline cracking (Hashcat/Aircrack)
    │
    ├── WPA2-Enterprise Attacks
    │   ├── Rogue AP (hostapd-mana)
    │   ├── EAP credential capture
    │   └── MSCHAP hash cracking
    │
    ├── Evil Twin / Captive Portal
    │   ├── Clone SSID
    │   ├── Deauth real AP
    │   └── Credential harvest
    │
    └── Segmentation Testing
        ├── Client isolation
        ├── VLAN traversal
        └── Corporate network reach
```

---

## Working Template

## Document Control
| Field | Value |
|-------|-------|
| Client | [Name] |
| Test Type | Wireless Network Security Assessment |
| Location(s) | [Physical locations tested] |
| SSIDs In Scope | [List] |
| Period | [Start] — [End] |

## Executive Summary
[Overview of wireless security posture including encryption weaknesses, rogue APs, segmentation issues]

## Findings Summary
| Severity | Count |
|----------|-------|
| Critical | [N] |
| High | [N] |
| Medium | [N] |
| Low | [N] |

## Detailed Findings
### Finding [N]: [Title]
| Attribute | Detail |
|-----------|--------|
| SSID / BSSID | [Values] |
| Severity | [Level] |
| Issue | [Description] |
| Remediation | [Fix] |

## Recommendations
1. [Priority recommendations]
