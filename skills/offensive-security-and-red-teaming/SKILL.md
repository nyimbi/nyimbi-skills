---
name: offensive-security-and-red-teaming
description: >-
  Plan and run authorized offensive operations: red team engagements, adversary
  emulation, penetration tests (external, internal/assumed-breach, Active
  Directory, web, API, mobile, thick client, wireless), exploitation, lateral
  movement, privilege escalation, phishing and vishing simulation, physical
  assessment, and command-and-control operations with Sliver, Havoc, or
  Covenant. Use when the user asks to "run a red team exercise", "penetration
  test our network", "simulate an insider after a breach", "map attack paths to
  Domain Admin", "stand up C2 behind redirectors", "run a gophish campaign",
  "test whether we would detect this technique", or "which MITRE ATT&CK
  techniques did the engagement cover". Authorization comes first: the workflow
  gates on written rules of engagement, target list, emergency contacts,
  data-handling rules, and stop conditions before any active testing. Do not
  use for detecting or hunting attackers in your own environment
  (threat-hunting-and-detection), recovering evidence from a real compromise
  (digital-forensics-and-evidence), scanning and patching known weaknesses
  (vulnerability-management-and-compliance), or hardening and monitoring
  network infrastructure (network-and-wireless-security).
license: Apache-2.0
---

# Offensive Security and Red Teaming

This skill covers **authorized** offensive work only. Every engagement fails the
same three ways: activity outside the signed scope, no agreed stop condition
when something breaks, and execution without timestamps that let defenders
measure what they saw. Fix all three on paper before the first packet leaves
your machine.

Treat the rules of engagement as a hard gate, not paperwork. If authorization
cannot be produced, the correct deliverable is the ROE document itself — not a
scan.

## When to use

- Planning or executing a red team exercise, adversary emulation, or purple team session
- Running an external, internal/assumed-breach, or wireless penetration test
- Enumerating and exploiting Active Directory: BloodHound paths, Kerberoasting, ADCS, delegation, DCSync
- Gaining initial access: spearphishing, adversary-in-the-middle phishing, external service exploitation, physical entry
- Standing up and operating C2 (Sliver, Havoc, Covenant) with redirectors, listeners, and implants
- Post-exploitation: credential access, lateral movement, privilege escalation, persistence demonstration
- Application testing: web, API, mobile, thick client, SQL injection, XSS
- Deciding which ATT&CK techniques an engagement exercises — and which are explicitly out of scope

**Do not use for** — `threat-hunting-and-detection` when the question is how to
find an attacker already inside your network; `digital-forensics-and-evidence`
when the question is what happened on a compromised host;
`vulnerability-management-and-compliance` when the goal is scanning, scoring,
and tracking known CVEs rather than demonstrating exploitability;
`network-and-wireless-security` when the goal is to design segmentation,
deploy IDS/IPS, or monitor traffic rather than attack it.

## Workflow

1. **Clear the authorization gate before any active testing.** Input: the
   engagement request. Output: a signed rules-of-engagement packet containing
   (a) written scope — in-scope and out-of-scope IP ranges, domains, hosts,
   applications, personnel, physical sites, and third-party/cloud systems;
   (b) the explicit target list; (c) named emergency contacts and an escalation
   path with check-in times; (d) data-handling rules — what may be accessed,
   what may be copied, how evidence is stored and when it is destroyed, and the
   rule that real customer/PII data is never exfiltrated (use proof markers
   instead); (e) testing windows, blackout dates, and prohibited actions
   (destructive tests, denial of service, safety systems); (f) stop conditions
   that halt work immediately — production impact, safety-relevant system
   touched, unexpected exposure of real data, loss of contact — plus the
   emergency-stop code word; (g) the signed authorization ("get-out-of-jail")
   letter. If any element is missing, deliver the ROE template and stop.

2. **Fix the engagement type and the ATT&CK coverage contract.** Input:
   business objective and crown jewels. Output: a one-page coverage contract.
   Choose the model: **full scope** (people, process, technology, physical),
   **assumed breach** (start from a foothold, test blast radius), **objective
   based** (reach a defined crown jewel), or **purple team** (collaborative,
   detection-focused). Then write down the MITRE ATT&CK techniques in scope as
   a Navigator layer, and — just as important — the techniques explicitly out
   of scope (impact/destruction, denial of service, physical unless scoped,
   supply chain, third-party partners). Every later action must map to an
   in-scope technique ID; an action with no mapping is out of scope by default.

3. **Build the threat model, objectives, and reconnaissance plan.** Input:
   coverage contract plus threat intelligence on the sector (APT29/APT28 for
   government, FIN7 for retail/finance, Conti/Royal for ransomware scenarios).
   Output: prioritized objectives (e.g., "reach the cardholder environment",
   "demonstrate Domain Admin"), a target profile from passive recon, and a
   phased attack plan with go/no-go decision points. Start passive — OSINT,
   certificate transparency, DNS and attack-surface mapping — and only move to
   active interaction with target systems once step 1 is signed.

4. **Stand up C2 and phishing infrastructure — one topic per tool family.**
   Input: chosen initial-access vector and OPSEC constraints. Output: tested
   infrastructure verified against the same EDR/AV the target runs.
   - **Sliver** is one topic even though it ships as two source skills:
     build team server, listeners (mTLS, HTTPS, HTTP, DNS), redirector, and
     implants (`building-c2-infrastructure-with-sliver-framework`) then operate
     them — armory extensions, sessions vs beacons, SOCKS pivoting, cleanup
     (`operating-sliver-c2`).
   - **Havoc** is one topic likewise: build the team server, Yaotl profile,
     nginx redirector, and Demon payload (`building-red-team-c2-infrastructure-with-havoc`)
     then operate it — listeners, in-memory .NET/BOF execution, injection,
     pivoting, cleanup (`operating-havoc-c2`).
   - **Covenant** is a lighter single-file alternative for smaller engagements.
   Compare frameworks in
   [`references/c2-framework-selection.md`](references/c2-framework-selection.md);
   redirector/nginx/malleable-profile detail lives in
   [`references/building-c2-redirector-infrastructure.md`](references/building-c2-redirector-infrastructure.md).
   - **Phishing** is one topic across the three gophish variants
     (`performing-red-team-phishing-with-gophish`,
     `performing-phishing-simulation-with-gophish`,
     `executing-phishing-simulation-campaign`): deploy GoPhish, configure the
     SMTP sending profile, build the template and landing page, import the
     HR-approved target group, launch, and read open/click/submit/report rates.
     EvilGinx3 is the separate adversary-in-the-middle variant when the
     objective is session-token capture or MFA bypass.

5. **Gain initial access and confirm the beacon.** Input: coverage contract
   and prepared infrastructure. Output: an established foothold with a
   timestamped record. Select the vector from the contract — spearphishing
   payload, AiTM phishing, exploitation of a public-facing service, or physical
   entry — establish C2, add persistence, and log the technique ID and time
   for every step. Failed attempts are logged too; they are evidence of
   controls that worked.

6. **Escalate and move through the target.** Input: foothold plus a standard
   user (assumed breach) or nothing (external). Output: a documented attack
   chain ending at the objective. Enumerate first with BloodHound CE, then
   pick credential and movement techniques by precondition — Kerberoasting/
   AS-REP roasting for weak service accounts, NTLM relay and auth coercion
   (PetitPotam/Coercer) toward ADCS ESC8, certificate abuse via Certipy, delegation
   and shadow-credential abuse, DCSync and ticket forgery for domain dominance.
   The precondition→technique matrix is in
   [`references/active-directory-attack-path-selection.md`](references/active-directory-attack-path-selection.md).
   Demonstrate access with proof markers; do not copy real data out.

7. **Achieve objectives and measure detection.** Input: executed techniques
   with timestamps. Output: detection-gap measurement. Compare your timeline
   against the defender's — per technique: detected or missed, mean time to
   detect and respond, coverage as a Navigator heat map. Where the exercise is
   purple, run Atomic Red Team tests to validate each gap and write the Sigma
   rule or log source needed to close it.

8. **Clean up, verify, and report.** Input: everything created during the
   engagement. Output: a clean target and the engagement report. Remove
   implants, accounts, tickets, scheduled tasks, persistence, and DNS/C2
   infrastructure; revert configuration changes; re-scan to verify removal;
   confirm the cleanup list with the client. Handle or destroy captured
   evidence per the data-handling rules from step 1, then deliver the report.

## Quality bar

- [ ] Signed ROE with scope, target list, emergency contacts, data-handling rules, and stop conditions exists **before** any active testing — no exceptions
- [ ] Every action taken maps to an in-scope MITRE ATT&CK technique ID; out-of-scope techniques are documented and were not exercised
- [ ] Engagement type (full scope / assumed breach / objective-based / purple) and measurable objectives are stated up front
- [ ] Deconfliction is agreed with the SOC/IR team so red team activity is not mistaken for a real incident, and the emergency stop was tested
- [ ] C2 and phishing infrastructure was OPSEC-verified against the target's actual EDR/AV before use, with a backup channel
- [ ] Every technique execution has a timestamp, evidence, and detection outcome recorded as it happens
- [ ] Findings each carry a reproducible attack path (step chain with technique IDs), impact, and concrete remediation
- [ ] Sensitive data is handled per the ROE: no exfiltration of real customer/PII data, proof markers only, evidence destroyed on schedule
- [ ] Cleanup is verified by re-scan and confirmed with the client: no implants, accounts, tickets, or infrastructure left behind
- [ ] The report includes detection-gap analysis (detected vs. missed, MTTD/MTTR) and prioritized purple-team recommendations

## Reference map

The complete catalog of merged techniques is in
[`references/technique-index.md`](references/technique-index.md). Load the file
for the phase you are executing rather than reading the index end to end.

| Situation | Open |
|---|---|
| Writing the ROE, scoping, threat profile, engagement plan | [executing-red-team-engagement-planning](references/executing-red-team-engagement-planning.md) |
| Full-scope engagement lifecycle, OPSEC checklist, report template | [conducting-full-scope-red-team-engagement](references/conducting-full-scope-red-team-engagement.md) |
| Adversary emulation plan from a threat actor's ATT&CK TTPs | [executing-red-team-exercise](references/executing-red-team-exercise.md) |
| Choosing a C2 framework and listener/redirector strategy (Sliver, Havoc, Covenant) | [c2-framework-selection](references/c2-framework-selection.md) · [building-c2-redirector-infrastructure](references/building-c2-redirector-infrastructure.md) |
| Sliver: team server, listeners, implants, post-ex, cleanup (one topic) | [building-c2-infrastructure-with-sliver-framework](references/building-c2-infrastructure-with-sliver-framework.md) · [operating-sliver-c2](references/operating-sliver-c2.md) |
| Havoc: Yaotl profile, Demon agent, redirector, post-ex (one topic) | [building-red-team-c2-infrastructure-with-havoc](references/building-red-team-c2-infrastructure-with-havoc.md) · [operating-havoc-c2](references/operating-havoc-c2.md) |
| Covenant as a lighter C2 option | [performing-red-team-with-covenant](references/performing-red-team-with-covenant.md) |
| GoPhish campaign: templates, SMTP, landing pages, metrics (one topic) | [executing-phishing-simulation-campaign](references/executing-phishing-simulation-campaign.md) · [conducting-spearphishing-simulation-campaign](references/conducting-spearphishing-simulation-campaign.md) |
| Adversary-in-the-middle phishing, MFA bypass, session cookies | [performing-initial-access-with-evilginx3](references/performing-initial-access-with-evilginx3.md) |
| Vishing, smishing, physical pretexting campaigns | [conducting-social-engineering-penetration-test](references/conducting-social-engineering-penetration-test.md) · [conducting-social-engineering-pretext-call](references/conducting-social-engineering-pretext-call.md) |
| Physical entry: tailgating, badge cloning, lock bypass | [performing-physical-intrusion-assessment](references/performing-physical-intrusion-assessment.md) |
| External/perimeter network pentest (PTES phases, scanning to reporting) | [conducting-network-penetration-test](references/conducting-network-penetration-test.md) · [performing-external-network-penetration-test](references/performing-external-network-penetration-test.md) |
| Assumed-breach internal network test | [conducting-internal-network-penetration-test](references/conducting-internal-network-penetration-test.md) |
| End-to-end Active Directory penetration test | [performing-active-directory-penetration-test](references/performing-active-directory-penetration-test.md) |
| Picking an AD technique for a given precondition (Kerberos, relay, ADCS, DCSync) | [active-directory-attack-path-selection](references/active-directory-attack-path-selection.md) |
| BloodHound / BloodHound CE collection and attack-path analysis | [conducting-internal-reconnaissance-with-bloodhound-ce](references/conducting-internal-reconnaissance-with-bloodhound-ce.md) · [mapping-attack-paths-with-bloodhound-ce](references/mapping-attack-paths-with-bloodhound-ce.md) |
| Kerberoasting and AS-REP roasting with Impacket | [exploiting-kerberoasting-with-impacket](references/exploiting-kerberoasting-with-impacket.md) · [performing-kerberoasting-attack](references/performing-kerberoasting-attack.md) |
| AD Certificate Services misconfigurations (ESC1–ESC16) | [exploiting-adcs-with-certipy](references/exploiting-adcs-with-certipy.md) · [exploiting-active-directory-certificate-services-esc1](references/exploiting-active-directory-certificate-services-esc1.md) |
| NTLM relay to web enrollment (ESC8) and authentication coercion | [relaying-ntlm-for-adcs-esc8](references/relaying-ntlm-for-adcs-esc8.md) · [coercing-authentication-with-coercer-petitpotam](references/coercing-authentication-with-coercer-petitpotam.md) |
| Domain persistence: DCSync, KRBTGT, golden/silver tickets | [conducting-domain-persistence-with-dcsync](references/conducting-domain-persistence-with-dcsync.md) |
| Kerberos delegation abuse, pass-the-ticket, shadow credentials | [exploiting-constrained-delegation-abuse](references/exploiting-constrained-delegation-abuse.md) · [conducting-pass-the-ticket-attack](references/conducting-pass-the-ticket-attack.md) · [abusing-shadow-credentials-for-privesc](references/abusing-shadow-credentials-for-privesc.md) |
| Lateral movement over SMB/WinRM/WMI/MSSQL | [moving-laterally-with-netexec](references/moving-laterally-with-netexec.md) · [performing-lateral-movement-with-wmiexec](references/performing-lateral-movement-with-wmiexec.md) |
| Known-vulnerability exploitation (Zerologon, noPac, EternalBlue) | [exploiting-zerologon-vulnerability-cve-2020-1472](references/exploiting-zerologon-vulnerability-cve-2020-1472.md) · [exploiting-nopac-cve-2021-42278-42287](references/exploiting-nopac-cve-2021-42278-42287.md) · [exploiting-ms17-010-eternalblue-vulnerability](references/exploiting-ms17-010-eternalblue-vulnerability.md) |
| Local privilege escalation on Windows or Linux | [performing-privilege-escalation-on-linux](references/performing-privilege-escalation-on-linux.md) · [performing-privilege-escalation-assessment](references/performing-privilege-escalation-assessment.md) |
| Credential harvesting from a compromised endpoint (DPAPI, LaZagne) | [abusing-dpapi-for-credential-access](references/abusing-dpapi-for-credential-access.md) · [performing-credential-access-with-lazagne](references/performing-credential-access-with-lazagne.md) |
| Passive recon and external attack-surface mapping | [performing-open-source-intelligence-gathering](references/performing-open-source-intelligence-gathering.md) · [implementing-attack-surface-management](references/implementing-attack-surface-management.md) · [conducting-external-reconnaissance-with-osint](references/conducting-external-reconnaissance-with-osint.md) |
| Web application testing (WSTG), SQLi, XSS | [performing-web-application-penetration-test](references/performing-web-application-penetration-test.md) · [exploiting-sql-injection-vulnerabilities](references/exploiting-sql-injection-vulnerabilities.md) · [testing-for-xss-vulnerabilities](references/testing-for-xss-vulnerabilities.md) |
| API, mobile (MASTG), and thick-client application testing | [conducting-api-security-testing](references/conducting-api-security-testing.md) · [conducting-mobile-app-penetration-test](references/conducting-mobile-app-penetration-test.md) · [performing-thick-client-application-penetration-test](references/performing-thick-client-application-penetration-test.md) |
| Wireless penetration testing (in the offensive scope, not defensive hardening) | [conducting-wireless-network-penetration-test](references/conducting-wireless-network-penetration-test.md) · [performing-wireless-network-penetration-test](references/performing-wireless-network-penetration-test.md) |
| Vulnerability scanning as a recon input (Nessus) | [performing-vulnerability-scanning-with-nessus](references/performing-vulnerability-scanning-with-nessus.md) |
| Binary exploitation / exploit development with pwntools | [performing-binary-exploitation-analysis](references/performing-binary-exploitation-analysis.md) |
| Purple team: Atomic Red Team execution and ATT&CK coverage validation | [performing-purple-team-atomic-testing](references/performing-purple-team-atomic-testing.md) |
| IoT/embedded device assessment as part of an engagement | [performing-iot-security-assessment](references/performing-iot-security-assessment.md) |

Executable helpers for each technique live in `scripts/<technique-name>/` —
read the reference file first to learn what the script expects, then run it.

## Output format

Two documents are produced: the engagement plan (before testing) and the
engagement report (after).

```markdown
# <Client> — <Engagement Type> Plan / Report

## Authorization
Signed ROE date, scope summary, target list, emergency contacts, stop
conditions, data-handling rules. (Plan only — must exist before execution.)

## Objectives and ATT&CK coverage
Measurable objectives | Techniques in scope | Techniques explicitly out of scope

## Attack narrative
Timeline: phase → action → technique ID → timestamp → detected? (yes/no) → evidence

## Findings
| # | Title | Severity (CVSS) | Attack path (step chain) | Evidence | Remediation |

## Detection gap analysis
Techniques executed | detected | MTTD | MTTR | Navigator heat map summary

## Recommendations
Immediate (0–30 days) | Short term (30–90) | Long term (90–180), each tied to a gap

## Cleanup confirmation
Artifacts removed, verification method, client sign-off.
```

For a purple-team session, add a per-technique table with the log source that
should have fired and the detection rule needed, so the blue team can act on
each row directly.
