# Attacking Entra Id With Roadtools

## API Reference

## ROADrecon

| Command | Purpose | Key flags |
|---------|---------|-----------|
| `roadrecon auth` | Authenticate to Entra ID | `-u` user, `-p` password, `--device-code`, `--access-token`, `--refresh-token`, `--prt`, `--prt-sessionkey`, `--prt-cookie`, `--prt-init` |
| `roadrecon gather` | Gather directory into roadrecon.db | `--mfa` (needs privileged role) |
| `roadrecon gui` | Launch Angular GUI (http://127.0.0.1:5000) | — |
| `roadrecon plugin policies` | Analyze conditional-access policies | `-f` file, `-p` |
| `roadrecon plugin bloodhound` | Export to BloodHound format | — |

Auth state is stored in `.roadtools_auth`; directory data in `roadrecon.db`.

## roadtx (ROADtools Token eXchange)

### Token acquisition
| Command | Purpose | Key flags |
|---------|---------|-----------|
| `roadtx gettokens` | Acquire tokens (ROPC / refresh) | `-u`, `-p`, `-c` client, `-r` resource, `-s` scope, `--refresh-token`, `--cae`, `--tokens-stdout` |
| `roadtx interactiveauth` | Interactive (browser) auth | `-u`, `-p`, `-c`, `-r`, `-ru` redirect-url |
| `roadtx codeauth` | Exchange auth code for tokens | — |
| `roadtx refreshtokento` | Convert stored RT to another resource | `-r`, `-s`, `-c` |
| `roadtx appauth` | App (client-credential) auth | `-c`, `-p` secret, `-t` tenant, `-r`, `-s`, `--cert-pem`, `--key-pem`, `--cert-pfx`, `--pfx-pass` |
| `roadtx federatedappauth` | Federated app auth (workload identity) | `-c`, `--cert-pem`, `--key-pem`, `--subject`, `-t`, `--issuer`, `-s`, `--kid` |

### Device + PRT
| Command | Purpose | Key flags |
|---------|---------|-----------|
| `roadtx device` | Register/delete a device | `-n` name, `-a` action, `-c` cert, `-k` key |
| `roadtx hybriddevice` | Register hybrid-joined device | — |
| `roadtx prt` | Request/renew a PRT | `-u`, `-p`, `--key-pem`, `--cert-pem`, `-a` action, `-r` refresh-token |
| `roadtx prtauth` | Auth a client using a PRT | `-c`, `-r`, `-f` prt-file, `--prt`, `--prt-sessionkey`, `--tokens-stdout` |
| `roadtx browserprtauth` | Browser auth using PRT | `-url`, `-c`, `-r`, `-f` |
| `roadtx browserprtinject` | Inject PRT compliance claims | `-u`, `-r`, `-c` |
| `roadtx prtenrich` | Add MFA claim to PRT | `-u` |
| `roadtx prtcookie` | Mint browser cookie from PRT | — |

### Utility
| Command | Purpose | Key flags |
|---------|---------|-----------|
| `roadtx describe` | Decode token claims | `-t` token (or stdin) |
| `roadtx decrypt` | Decrypt JWE tokens | — |
| `roadtx getscope` | Find clients holding a scope | `-s`, `--foci` |
| `roadtx getotp` | Generate TOTP from a seed | `<seed>` |
| `roadtx listaliases` | List client/resource aliases | — |
| `roadtx keepassauth` | Selenium auth from KeePass | `-c`, `-u`, `-kp`, `-kpp`, `-url`, `--keep-open` |
| `roadtx sharepointlogin` | Authenticate to SharePoint/OneDrive | `<token>`, `--host` |

### Common client (`-c`) and resource (`-r`) aliases
Clients: `azcli`, `msteams`, `msgraph` (as client where applicable), `office`, `broker`.
Resources: `msgraph`, `azrm`, `aadgraph`, `devicereg`. Use `roadtx listaliases` for the full list.

---

## Standards and Controls

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| ID.AM-03 | Representations of the organization's authorized network communication and internal/external network data flows are maintained | ROADrecon enumeration produces the directory/identity asset inventory that defenders must maintain and that attackers exploit; the engagement validates visibility of this asset surface. |

## MITRE ATT&CK (Enterprise)

| ID | Name | Rationale |
|----|------|-----------|
| T1087.004 | Account Discovery: Cloud Account | ROADrecon enumerates Entra ID user/account objects. |
| T1069.003 | Permission Groups Discovery: Cloud Groups | ROADrecon enumerates Entra groups and directory roles. |
| T1538 | Cloud Service Dashboard | GUI exploration of tenant configuration and policies. |
| T1550.001 | Use Alternate Authentication Material: Application Access Token | roadtx refresh-token exchange across resources (FOCI). |
| T1528 | Steal Application Access Token | roadtx token/PRT acquisition. |

## Reference standards

| Standard | Relevance |
|----------|-----------|
| Microsoft identity platform (OAuth 2.0 / OIDC) | Defines the auth-code, ROPC, device-code, and refresh-token flows roadtx exercises. |
| FOCI (Family of Client IDs) | Microsoft first-party client family enabling cross-client refresh-token redemption. |
| Primary Refresh Token (PRT) | Device-bound SSO artifact abused via roadtx prt/prtauth. |
