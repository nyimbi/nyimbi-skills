# C2 Framework Selection

Purpose: pick the right command-and-control framework, listener type, and
edge architecture for an engagement before building anything — the per-framework
build/run detail lives in the linked technique files.

## Framework comparison

| Criterion | Sliver | Havoc | Covenant |
|---|---|---|---|
| Source skills in this bundle | build + operate (one topic) | build + operate (one topic) | single skill |
| Implant/beacon | cross-platform implant + beacon; mTLS, HTTPS, HTTP, DNS, WireGuard listeners | Demon agent; HTTPS/HTTP listeners driven by a Yaotl profile | Grunt agent; HTTP/S listeners via the web UI |
| Operator model | CLI-first, `multiplayer` mode for multi-operator teams | GUI client, profile-gated operators | Web UI, lighter multi-operator support |
| Evasion surface | armory extensions, BOF/.NET execution, sleep migration | indirect syscalls, Ekko-style sleep obfuscation, in-memory .NET/BOF | simpler; expect louder telemetry |
| Pivoting | SOCKS5 over implant, TCP pivot listeners, chained beacons | SOCKS5 through Demon, port forwards | HTTP-based relays |
| Best fit | default choice for most engagements; strong protocol variety and scripting | Windows-heavy adversary emulation where Demon's evasion profile matches the threat actor | short engagements, labs, operators who want a UI quickly |
| Primary technique files | [building-c2-infrastructure-with-sliver-framework](building-c2-infrastructure-with-sliver-framework.md), [operating-sliver-c2](operating-sliver-c2.md) | [building-red-team-c2-infrastructure-with-havoc](building-red-team-c2-infrastructure-with-havoc.md), [operating-havoc-c2](operating-havoc-c2.md) | [performing-red-team-with-covenant](performing-red-team-with-covenant.md) |

Cobalt Strike and Mythic appear in source methodology material but are not
merged as skills here; if licensing or existing operator skill dictates them,
the listener/redirector architecture below still applies unchanged.

## Edge architecture decision

| Situation | Edge design |
|---|---|
| Target allows direct egress on 443, defenders lack JA3/sinking-hole capability | Native HTTPS listener with a real certificate on a dedicated redirector host |
| Defenders investigate first-seen domains or unknown certificates | Aged domain + legitimate fronting CDN/service; filter investigator traffic at the redirector |
| Egress restricted to proxy allow-lists | HTTPS behind the redirector; DNS listener only as the fallback channel |
| DNS-only egress | DNS listener on a delegated zone you control — expect slower tasking and higher detection risk |
| Multiple operators, long dwell time | Team server on separate infrastructure from redirectors; backup channel pre-tested |
| Short, noisy exercise (assumed breach, purple) | Direct listener with monitoring; stealth investment has no payoff |

Redirector mechanics (nginx/Apache reverse proxy, `cs2modrewrite`, dumb-pipe
forwarders, certbot) are in
[building-c2-redirector-infrastructure](building-c2-redirector-infrastructure.md).

## Implant vs beacon

- **Session (interactive implant):** active objective work, lateral movement,
  hands-on operator interaction. Higher exposure — short sleep, interactive
  traffic.
- **Beacon (asynchronous):** long-dwell or low-noise periods, staged objectives,
  backup access. Jitter and randomize the sleep; avoid fixed intervals, which
  beacon detectors key on.
- Run at least one asynchronous channel concurrently with the interactive one
  so a single detection does not lose the engagement.

## OPSEC checklist before going live

- [ ] Infrastructure tested against the same EDR/AV versions the target runs
- [ ] Domains aged and mail/SPF/DKIM/DMARC configured where phishing is in scope
- [ ] Redirector filters blue-team investigation ranges; team server is never directly reachable
- [ ] Backup channel established and exercised, not merely planned
- [ ] All infrastructure, payloads, and domains listed in the deconfliction matrix given to the SOC
