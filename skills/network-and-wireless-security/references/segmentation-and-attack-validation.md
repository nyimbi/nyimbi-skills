# Segmentation and Attack Validation

Purpose: the test matrix for proving a network control works — each row pairs
the control with the authorized simulation that attacks it and the pass
criteria that make the result unambiguous.

All simulation rows require written authorization with a target list, time
box, and stop conditions (workflow step 1). They validate a control; they are
not an engagement.

## Control → test → pass criteria

| Control under test | Test (technique file) | How it is run | Pass criteria |
|---|---|---|---|
| Inter-VLAN deny rules | Reachability probes from each zone (nmap/ping/curl) | From a host in zone A, attempt the forbidden flows to zone B | All denied flows fail; all allowed flows succeed; the firewall logs each deny |
| Trunk/DTP hardening | VLAN hopping — switch spoofing ([performing-vlan-hopping-attack](performing-vlan-hopping-attack.md)) | Attempt DTP negotiation on an access port | Negotiation refused; port stays in its assigned VLAN |
| Native VLAN hygiene | Double-tagging ([performing-vlan-hopping-attack](performing-vlan-hopping-attack.md)) | Send 802.1Q double-tagged frames | Frames do not reach the target VLAN; no traffic accepted on the native VLAN |
| Dynamic ARP Inspection | ARP spoofing simulation ([performing-arp-spoofing-attack-simulation](performing-arp-spoofing-attack-simulation.md)) | arpspoof/Ettercap/Scapy gratuitous ARP on the segment | Spoofed ARPs dropped by the switch; no victim ARP cache poisoned; alert raised |
| ARP anomaly monitoring | Detection check ([detecting-arp-poisoning-in-network-traffic](detecting-arp-poisoning-in-network-traffic.md)) | Same spoofing traffic while ARPWatch/IDS runs | Alert fires with source MAC/IP within the test window |
| TLS enforcement / HSTS | MITM interception ([conducting-man-in-the-middle-attack-simulation](conducting-man-in-the-middle-attack-simulation.md)) | Ettercap/bettercap/mitmproxy on an authorized segment | TLS sessions fail closed with a certificate error; no plaintext captured |
| HSTS / upgrade enforcement | SSL stripping ([performing-ssl-stripping-attack](performing-ssl-stripping-attack.md)) | sslstrip/bettercap against a scoped target | Browser remains on HTTPS; downgrade blocked; no credentials sent in clear |
| IDS signatures (scan detection) | Port scan against monitored link ([scanning-network-with-nmap-advanced](scanning-network-with-nmap-advanced.md)) | Nmap SYN/FIN/Xmas/NULL/UDP scans at documented timing | Matching signature fires once per scan type with correct source IP |
| IPS blocking (inline) | Known-bad probe ([implementing-network-intrusion-prevention-with-suricata](implementing-network-intrusion-prevention-with-suricata.md)) | Send traffic matching a controlled local rule | Traffic blocked at the sensor; alert + drop logged; no service impact |
| Stateful firewall policy | Malformed/spoofed packet injection ([performing-packet-injection-attack](performing-packet-injection-attack.md)) | Scapy/hping3/Nemesis crafted and spoofed packets | Non-conforming packets dropped; firewall state table unaffected; no crash |
| IPv4-only controls | IPv6 parallel path ([exploiting-ipv6-vulnerabilities](exploiting-ipv6-vulnerabilities.md)) | SLAAC spoofing, RA flood, 6to4/Teredo tunnels | IPv6 policy matches IPv4 intent; rogue RAs ignored; tunnels blocked |
| QoS / rate limiting | Bandwidth degradation ([performing-bandwidth-throttling-attack-simulation](performing-bandwidth-throttling-attack-simulation.md)) | tc/iperf3 shaped traffic in a lab or approved window | Degradation contained to the shaped class; application SLA held; alert on anomaly |
| Enterprise wireless auth | Handshake/PSK audit ([performing-wifi-password-cracking-with-aircrack](performing-wifi-password-cracking-with-aircrack.md)) | Capture handshake on scoped SSID, crack offline | Documented crack time vs policy; PSK networks justified or converted to 802.1X |
| Rogue AP detection | Unauthorized AP advertisement ([performing-wireless-security-assessment-with-kismet](performing-wireless-security-assessment-with-kismet.md)) | Stand up an unsanctioned AP in range | WIDS/Kismet flags it as rogue within the agreed detection window |
| NAC port control | Unauthenticated/quarantine placement ([implementing-network-access-control](implementing-network-access-control.md)) | Connect unsupplicant device; fail RADIUS on purpose | Guest/quarantine VLAN assigned; critical VLAN on RADIUS outage; no full-access leak |

## Execution rules

1. **One control, one test, one owner.** Record who ran it, when, from which
   source host, and against which device — results are not reusable across
   change windows.
2. **Test from the inside out.** A rule tested only from the trusted side has
   not been tested; run both directions for every zone pair.
3. **Capture evidence with the test.** Screenshot or log the deny, the alert,
   or the refused handshake at the moment of the test; post-hoc
   reconstruction does not count.
4. **Failures are findings, not flukes.** A control that fails its test gets
   an owner, a fix, and a retest before the engagement closes.
5. **Never test DoS or production safety-critical paths** unless the written
   authorization explicitly names them — bandwidth and injection tests are
   time-boxed and scoped to lab or maintenance windows.
