# Auditing kubernetes RBAC Privilege Escalation

## API Reference

## kubectl auth can-i

| Command | Purpose |
|---------|---------|
| `kubectl auth can-i --list` | List all permissions for the current identity |
| `kubectl auth can-i --list --as=system:serviceaccount:NS:SA` | List permissions for a service account (impersonation) |
| `kubectl auth can-i <verb> <resource>` | Check a single permission |
| `kubectl auth can-i <verb> <resource> --all-namespaces` | Check across namespaces |
| `kubectl auth can-i '*' '*'` | Check for wildcard god-mode |
| `--as-group=<group>` | Impersonate a group (e.g. system:masters) |

## kubectl-who-can (krew: who-can)

| Command | Purpose |
|---------|---------|
| `kubectl who-can create pods` | List subjects that can create pods |
| `kubectl who-can get secrets -n NS` | Subjects that can read secrets in a namespace |
| `kubectl who-can '*' '*'` | Subjects with full wildcard access |
| `kubectl who-can create serviceaccounts/token` | Token-minting subjects |

## rakkess / access-matrix (krew: access-matrix)

| Command | Purpose |
|---------|---------|
| `kubectl access-matrix` | Verb x resource matrix for current subject |
| `kubectl access-matrix --as system:serviceaccount:NS:SA` | Matrix for another subject |
| `kubectl access-matrix resource pods` | Who can do what on pods (`resource` subcommand) |

## rbac-lookup (krew: rbac-lookup)

| Command | Purpose |
|---------|---------|
| `kubectl rbac-lookup <name>` | Show roles bound to a subject |
| `kubectl rbac-lookup <sa> --kind serviceaccount` | Filter to service accounts |
| `kubectl rbac-lookup --output wide` | Include the source binding |

## rbac-police

| Command | Purpose |
|---------|---------|
| `rbac-police eval ./lib/policies/` | Run all escalation policies against the live cluster |
| `rbac-police eval <policy.rego> -f json -o out.json` | Run one policy, JSON output |
| `rbac-police collect -o snapshot.json` | Snapshot RBAC for offline analysis |
| `rbac-police eval ./lib/policies/ --collect-results snapshot.json` | Evaluate from a snapshot |
| `--severity-threshold High` | Filter to high-severity findings |

## Dangerous Verbs / Resources

| Verb | Sensitive Resources |
|------|---------------------|
| `escalate` | roles, clusterroles |
| `bind` | clusterroles |
| `impersonate` | users, groups, serviceaccounts |
| `create`/`update`/`patch` | pods, deployments, daemonsets, mutatingwebhookconfigurations |
| `create` | pods/exec, pods/attach, pods/ephemeralcontainers, serviceaccounts/token |
| `get`/`list`/`watch` | secrets |
| `approve` | certificatesigningrequests/approval |

## External References

- Kubernetes RBAC Good Practices: https://kubernetes.io/docs/concepts/security/rbac-good-practices/
- RBAC reference: https://kubernetes.io/docs/reference/access-authn-authz/rbac/

---

## Standards and Controls

## MITRE ATT&CK

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| T1078 | Valid Accounts | Defense Evasion / Privilege Escalation | RBAC abuse leverages legitimate service-account credentials to gain higher access. |
| T1098 | Account Manipulation | Persistence | `escalate`/`bind`/`impersonate` and token minting create or modify accounts/bindings. |
| T1528 | Steal Application Access Token | Credential Access | Reading `secrets` or `serviceaccounts/token` yields other accounts' tokens. |
| T1613 | Container and Resource Discovery | Discovery | Enumerating roles, bindings, and pod-to-SA mappings. |
| T1611 | Escape to Host | Privilege Escalation | `create pods` plus node access yields a privileged host-mounting pod. |

## NIST CSF 2.0

| ID | Name | Rationale |
|----|------|-----------|
| PR.AA-05 | Access permissions, entitlements, and authorizations are defined, managed, and enforced incorporating least privilege | The audit directly measures and enforces least-privilege RBAC, removing escalation primitives. |

## Official Resources

- Kubernetes RBAC Good Practices: https://kubernetes.io/docs/concepts/security/rbac-good-practices/
- Using RBAC Authorization: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
- Authorization Overview (`auth can-i`): https://kubernetes.io/docs/reference/access-authn-authz/authorization/
- rbac-police: https://github.com/PaloAltoNetworks/rbac-police
- kubectl-who-can: https://github.com/aquasecurity/kubectl-who-can
- rakkess: https://github.com/corneliusweig/rakkess
- rbac-lookup: https://github.com/FairwindsOps/rbac-lookup

## Key Research

- Unit 42: Kubernetes RBAC privilege escalation research
- Kubernetes SIG-Auth: documented privilege-escalation primitives (escalate, bind, impersonate)
