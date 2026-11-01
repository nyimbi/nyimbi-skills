# Building C2 Redirector Infrastructure

## API Reference

## nginx reverse-proxy directives

| Directive | Purpose |
|-----------|---------|
| `location ~ ^/regex` | Match profile C2 URIs |
| `proxy_pass https://TEAMSERVER;` | Forward matched traffic to team server |
| `proxy_ssl_verify off;` | Skip cert verification to backend |
| `proxy_set_header Host $host;` | Preserve Host header |
| `if ($http_user_agent != "...") { return 302 ...; }` | UA validation |
| `return 302 https://DECOY/;` | Divert non-C2 to a benign site |

## Apache mod_rewrite directives

| Directive | Purpose |
|-----------|---------|
| `RewriteEngine On` | Enable rewriting |
| `SSLProxyEngine On` | Allow HTTPS proxying |
| `RewriteCond %{HTTP_USER_AGENT} "..."` | Match implant User-Agent |
| `RewriteCond %{REQUEST_URI} ^/c2/path` | Match profile URIs |
| `RewriteRule ^.*$ https://TEAMSERVER%{REQUEST_URI} [P,L]` | Proxy match to backend |
| `RewriteRule ^.*$ https://DECOY/ [R=302,L]` | Redirect non-match to decoy |

Required modules: `rewrite proxy proxy_http ssl headers` (`a2enmod`).

## cs2modrewrite invocation

```bash
# Apache rules from a Cobalt Strike profile
python3 cs2modrewrite.py -i PROFILE.profile -c https://TEAMSERVER \
  -r https://DECOY -o redirect.rules

# nginx config
python3 cs2nginx.py -i PROFILE.profile -c https://TEAMSERVER \
  -r https://DECOY -H your.domain > c2.conf
```

| Flag | Meaning |
|------|---------|
| `-i` | Input Cobalt Strike malleable profile |
| `-c` | C2 team server URL (proxy target) |
| `-r` | Redirect URL for non-matching requests |
| `-o` | Output rules file (Apache) |
| `-H` | Hostname (nginx) |

## Dumb-pipe forwarders

```bash
socat TCP4-LISTEN:443,fork,reuseaddr TCP4:TEAMSERVER:443
iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination TEAMSERVER:443
```

## TLS (certbot)

```bash
certbot --nginx -d your.domain --agree-tos -m ops@you --redirect
certbot renew --dry-run
```

## External References

- mod_rewrite flags ([P], [R], [L]): https://httpd.apache.org/docs/current/rewrite/flags.html
- nginx proxy module: https://nginx.org/en/docs/http/ngx_http_proxy_module.html
- cs2modrewrite: https://github.com/threatexpress/cs2modrewrite

---

## Standards and Controls

## MITRE ATT&CK References

| Technique ID | Name | Tactic | Rationale |
|-------------|------|--------|-----------|
| T1090.002 | Proxy: External Proxy | Command and Control | The redirector is the external proxy node that hides the team server |
| T1090.004 | Proxy: Domain Fronting | Command and Control | CDN fronting routes C2 through a trusted high-reputation domain |
| T1071.001 | Application Layer Protocol: Web Protocols | Command and Control | C2 is tunneled over HTTP/HTTPS shaped by the malleable profile |
| T1573.002 | Encrypted Channel: Asymmetric Cryptography | Command and Control | TLS termination at the redirector encrypts the channel |
| T1583.006 | Acquire Infrastructure: Web Services | Resource Development | Disposable VPS/CDN edges acquired for resilient C2 |

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| DE.CM-01 | Networks and network services are monitored to find potentially adverse events | Redirector-fronted C2 is the adverse traffic defenders must detect; building it informs detection of T1090.002 |

## Official Resources

- MITRE ATT&CK T1090.002: https://attack.mitre.org/techniques/T1090/002/
- Apache mod_rewrite: https://httpd.apache.org/docs/current/mod/mod_rewrite.html
- nginx proxy_pass docs: https://nginx.org/en/docs/http/ngx_http_proxy_module.html
- cs2modrewrite: https://github.com/threatexpress/cs2modrewrite
- RedWarden: https://github.com/mgeeky/RedWarden
- ired.team redirectors/forwarders: https://www.ired.team/offensive-security/red-team-infrastructure/redirectors-forwarders

## Key Research

- RedOps: Cobalt Strike — CDN / Reverse Proxy Setup
- ired.team: Red Team Infrastructure Wiki
- threatexpress: cs2modrewrite project documentation
