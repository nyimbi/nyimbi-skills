---
name: identity-zero-trust-and-endpoint-security
description: >-
  Treat identity as the perimeter and the endpoint as its boundary. Cover
  conditional access, phishing-resistant MFA and FIDO2/passkeys, PAM with
  just-in-time and zero standing privilege, directory and AD tiering hardening,
  identity governance (joiner-mover-leaver, recertification, role mining,
  service accounts), zero trust maturity and ZTNA, plus endpoint controls —
  EDR, file integrity monitoring, application control, disk encryption, and CIS
  hardening baselines. Use when the user asks to "roll out passkeys", "set up
  conditional access", "eliminate standing privilege", "harden Active Directory",
  "deploy EDR", "replace the VPN with ZTNA", "which zero trust framework
  should we use", or "CIS baseline for Windows", and to run an access review. Do not
  use for Kubernetes RBAC, cloud workload IAM, or pipeline controls (see
  cloud-container-and-devsecops-security), for configuring or testing
  application login/OAuth code (see
  application-api-mobile-and-ai-security), or for how a credential is
  cryptographically protected (see cryptography-and-key-management).
license: Apache-2.0
---

# Identity, Zero Trust, and Endpoint Security

Identity work fails in predictable ways: MFA deployed but SMS still accepted,
a PAM vault nobody uses because standing access was faster, a conditional
access policy written in production and locking out administrators, an access
review where reviewers approve everything to clear the queue, an EDR agent
deployed with prevention policies still in detect-only.

Each of those is a *design* failure wearing an *implementation* costume. This
skill's job is to make the design explicit — who holds which credential at what
assurance, what signals gate each access decision, what happens when the
decision is wrong — and only then to configure the product.

## When to use

- Designing or reviewing conditional access, risk-based step-up, or session controls
- Rolling out FIDO2, passkeys, passwordless, or moving users off SMS/TOTP
- Standing up PAM, JIT/PIM activation, session recording, or killing standing privilege
- Hardening Active Directory, LDAP, Entra ID tenant config, or admin tiering
- Building joiner-mover-leaver, SCIM provisioning, role mining, access recertification, or service-account hygiene
- Choosing and migrating to a zero trust access model (ZTNA, BeyondCorp, maturity stages)
- Deploying or tuning EDR, FIM, application control, disk encryption, or endpoint DLP
- Applying CIS hardening baselines to Windows and Linux estates

**Do not use for** — `cloud-container-and-devsecops-security` when the subject is
workload rather than people: Kubernetes RBAC, workload identity, cloud IAM policy
design, admission control, or the CI pipeline; `application-api-mobile-and-ai-security`
when the question is how an application's login, OAuth flow, or session code is
*tested* for flaws rather than how the identity platform is configured;
`cryptography-and-key-management` when the question is how a credential, token,
or key is protected mathematically rather than who may use it;
`threat-hunting-and-detection` when the goal is writing SIEM detection rules
over the telemetry this skill produces.

## Workflow

1. **Inventory identities and entitlements before changing anything.** Enumerate
   humans, service accounts, privileged groups, OAuth/app consent grants, and
   orphaned accounts across AD/Entra ID, cloud IAM, and SaaS
   (`performing-privileged-account-discovery.md`,
   `performing-service-account-audit.md`,
   `performing-oauth-scope-minimization-review.md`). Output: a privileged-account
   register with owner, purpose, and last use — you cannot tier or revoke what is
   not listed.

2. **Establish the directory baseline.** Apply AD tiering (Tier 0/1/2 separation
   with privileged access workstations and no lateral logon across tiers),
   close dangerous ACLs, enforce LDAPS with channel binding and signing, and
   audit tenant configuration for risky CA policies, stale accounts, and guest
   exposure. Output: Tier-0 assets identified and reachable only from PAWs.

3. **Raise credential assurance to phish-resistant for privileged users.** Deploy
   FIDO2/passkeys, map methods to AAL, require AAL3 on admin resources, then
   disable SMS and legacy auth once telemetry shows no remaining users. Design
   rule: no method may be retired before the replacement covers 100% of its
   users, and one break-glass account always sits outside the policy set.
   See [`references/auth-assurance-and-phish-resistance.md`](references/auth-assurance-and-phish-resistance.md).

4. **Write conditional access from signals, not convenience.** Inputs: user risk,
   device compliance, credential strength, network location, app sensitivity.
   Pilot in report-only, read the impact report, exclude emergency accounts,
   then enforce. Output: a policy set where every rule names the signal it
   evaluates and the action for each risk band.

5. **Eliminate standing privilege.** Vault privileged credentials, require
   just-in-time activation with time-bound expiry and approval proportional to
   risk (self-approve low, single approver medium, dual for high, break-glass
   with post-facto review), record sessions, and run admins from hardened PAWs.
   Auto-revoke at expiry regardless of session state; an unexpired open session
   is the classic failure. Output: standing-privilege count trending to zero.

6. **Make entitlement lifecycle-driven.** Wire HR/IdP events to provisioning
   (SCIM), define lifecycle states and transitions with automated actions,
   mine roles from actual assignments instead of inventing them, and run
   certification campaigns where reviewers see last-used and risk context and
   revocations are ticketed with a 24–48 hour SLA and verified. Output: access
   that stops existing when the person changes role or leaves.

7. **Replace network trust with per-request decisions.** Choose one ZTNA
   enforcement model, write deny-by-default policy with device posture as a
   required input, migrate admin access first, and retire the VPN only after
   break-glass is proven; add microsegmentation for east-west traffic.
   See [`references/ztna-vendor-options.md`](references/ztna-vendor-options.md).

8. **Harden and instrument the endpoint.** Apply CIS baselines (L1 first,
   `enforce` only after an audit-mode pass), deploy EDR with prevention policies
   on and test-detection files verified, enable FIM on critical paths,
   application control in audit mode before enforce, full-disk encryption with
   key escrow, and USB/DLP restrictions. Output: per-control pass/fail against
   the baseline, with documented exceptions.

9. **Measure maturity, then re-run.** Score the estate against the CISA Zero
   Trust Maturity Model pillars (identity, devices, networks, applications,
   data) plus visibility/analytics, automation, and governance; record current
   and target tier per pillar and feed gaps back into steps 1–8.

## Quality bar

- [ ] Every privileged account has an owner, a stated purpose, and evidence of use within the last 90 days
- [ ] Administrators can authenticate only with a phish-resistant method, and a cloned-origin sign-in attempt demonstrably fails
- [ ] Conditional access policies were piloted in report-only, exclude tested break-glass accounts, and each names its signal and action
- [ ] Standing privileged access is time-bound with automatic revocation; the exception list is explicit and reviewed
- [ ] Session recording or full audit logging covers every Tier-0 administrative path
- [ ] Deprovisioning is event-driven from the HR/IdP source of truth, and revocation tickets are verified closed, not just opened
- [ ] Access reviews give reviewers last-used data and risk context; revoked access is re-checked as removed
- [ ] Every endpoint control was validated in audit mode before enforce, with a documented exception for each baseline deviation
- [ ] EDR coverage is measured as *reporting healthy*, not *installed*, and a test detection fires
- [ ] Disk encryption keys are escrowed and the recovery path has been exercised
- [ ] Maturity scores are recorded with evidence per pillar, so the next assessment compares like with like

## Reference map

All 75 merged techniques are catalogued in
[`references/technique-index.md`](references/technique-index.md). Use it for
anything not named below.

Synthesized topic files:

| Situation | Open |
|---|---|
| Choosing a ZTNA model among vendor options; migration sequence | [ztna-vendor-options.md](references/ztna-vendor-options.md) |
| Mapping MFA methods to assurance levels; conditional access signal ladder | [auth-assurance-and-phish-resistance.md](references/auth-assurance-and-phish-resistance.md) |

Per-technique detail:

| Situation | Open |
|---|---|
| Conditional access policy design and device posture signals | [implementing-conditional-access-policies-azure-ad](references/implementing-conditional-access-policies-azure-ad.md) · [implementing-device-posture-assessment-in-zero-trust](references/implementing-device-posture-assessment-in-zero-trust.md) |
| FIDO2/WebAuthn registration and authentication ceremonies | [implementing-hardware-security-key-authentication](references/implementing-hardware-security-key-authentication.md) |
| Passwordless rollout — one topic across FIDO2 and Entra | [implementing-passwordless-authentication-with-fido2](references/implementing-passwordless-authentication-with-fido2.md) · [implementing-passwordless-auth-with-microsoft-entra](references/implementing-passwordless-auth-with-microsoft-entra.md) |
| Second-factor deployment outside Microsoft (Duo, adaptive policies) | [configuring-multi-factor-authentication-with-duo](references/configuring-multi-factor-authentication-with-duo.md) |
| OAuth 2.0 flow selection and PKCE configuration | [configuring-oauth2-authorization-flow](references/configuring-oauth2-authorization-flow.md) |
| AD admin tiering, PAWs, authentication policy silos | [configuring-active-directory-tiered-model](references/configuring-active-directory-tiered-model.md) · [implementing-privileged-access-workstation](references/implementing-privileged-access-workstation.md) |
| LDAP/LDAPS hardening: signing, channel binding, anonymous bind | [configuring-ldap-security-hardening](references/configuring-ldap-security-hardening.md) |
| Dangerous AD ACLs (GenericAll, WriteDACL) and abuse paths | [analyzing-active-directory-acl-abuse](references/analyzing-active-directory-acl-abuse.md) |
| SAML federation and SSO configuration | [building-identity-federation-with-saml-azure-ad](references/building-identity-federation-with-saml-azure-ad.md) · [implementing-saml-sso-with-okta](references/implementing-saml-sso-with-okta.md) · [implementing-google-workspace-sso-configuration](references/implementing-google-workspace-sso-configuration.md) |
| Just-in-time access and zero standing privilege — one topic, several products | [implementing-just-in-time-access-provisioning](references/implementing-just-in-time-access-provisioning.md) · [implementing-zero-standing-privilege-with-cyberark](references/implementing-zero-standing-privilege-with-cyberark.md) · [implementing-azure-ad-privileged-identity-management](references/implementing-azure-ad-privileged-identity-management.md) |
| PAM platform deployment: vaulting, rotation, session recording | [implementing-privileged-access-management-with-cyberark](references/implementing-privileged-access-management-with-cyberark.md) · [implementing-delinea-secret-server-for-pam](references/implementing-delinea-secret-server-for-pam.md) · [implementing-privileged-session-monitoring](references/implementing-privileged-session-monitoring.md) · [implementing-pam-for-database-access](references/implementing-pam-for-database-access.md) |
| Privileged account discovery and periodic privileged access review | [performing-privileged-account-discovery](references/performing-privileged-account-discovery.md) · [performing-privileged-account-access-review](references/performing-privileged-account-access-review.md) |
| Dynamic/ephemeral secrets for services instead of static credentials | [implementing-hashicorp-vault-dynamic-secrets](references/implementing-hashicorp-vault-dynamic-secrets.md) |
| Joiner-mover-leaver state machine and IGA platform rollout | [building-identity-governance-lifecycle-process](references/building-identity-governance-lifecycle-process.md) · [implementing-identity-governance-with-sailpoint](references/implementing-identity-governance-with-sailpoint.md) |
| Access certification campaigns and entitlement reviews | [performing-access-review-and-certification](references/performing-access-review-and-certification.md) · [performing-access-recertification-with-saviynt](references/performing-access-recertification-with-saviynt.md) · [performing-entitlement-review-with-sailpoint-iiq](references/performing-entitlement-review-with-sailpoint-iiq.md) |
| Role mining to stop RBAC role explosion | [building-role-mining-for-rbac-optimization](references/building-role-mining-for-rbac-optimization.md) |
| Provisioning/deprovisioning over SCIM | [implementing-scim-provisioning-with-okta](references/implementing-scim-provisioning-with-okta.md) |
| Service account audit and credential rotation | [performing-service-account-audit](references/performing-service-account-audit.md) · [performing-service-account-credential-rotation](references/performing-service-account-credential-rotation.md) |
| Over-permissioned third-party OAuth apps and consent grants | [performing-oauth-scope-minimization-review](references/performing-oauth-scope-minimization-review.md) |
| Zero trust maturity assessment (CISA five pillars) | [implementing-cisa-zero-trust-maturity-model](references/implementing-cisa-zero-trust-maturity-model.md) · [implementing-identity-verification-for-zero-trust](references/implementing-identity-verification-for-zero-trust.md) |
| Vendor ZTNA deployment (BeyondCorp, Zscaler, Cloudflare, Prisma, Boundary, SDP, Tailscale, IAP, Verified Access) | see [ztna-vendor-options.md](references/ztna-vendor-options.md), which indexes `implementing-zero-trust-with-beyondcorp.md`, `deploying-cloudflare-access-for-zero-trust.md`, `implementing-zero-trust-with-hashicorp-boundary.md`, `deploying-software-defined-perimeter.md`, `deploying-tailscale-for-zero-trust-vpn.md`, `configuring-aws-verified-access-for-ztna.md`, `configuring-identity-aware-proxy-with-google-iap.md`, `configuring-zscaler-private-access-for-ztna.md`, `deploying-palo-alto-prisma-access-zero-trust.md`, and `implementing-zero-trust-network-access-with-zscaler.md` |
| Microsegmentation for east-west traffic | [configuring-microsegmentation-for-zero-trust](references/configuring-microsegmentation-for-zero-trust.md) · [implementing-microsegmentation-with-guardicore](references/implementing-microsegmentation-with-guardicore.md) |
| Zero trust for SaaS (CASB, SSPM, session controls) and DNS filtering | [implementing-zero-trust-for-saas-applications](references/implementing-zero-trust-for-saas-applications.md) · [implementing-zero-trust-dns-with-nextdns](references/implementing-zero-trust-dns-with-nextdns.md) |
| EDR agent deployment and prevention/response policy | [deploying-edr-agent-with-crowdstrike](references/deploying-edr-agent-with-crowdstrike.md) · [configuring-windows-defender-advanced-settings](references/configuring-windows-defender-advanced-settings.md) |
| Endpoint telemetry and query-based fleet visibility | [deploying-osquery-for-endpoint-monitoring](references/deploying-osquery-for-endpoint-monitoring.md) · [configuring-windows-event-logging-for-detection](references/configuring-windows-event-logging-for-detection.md) |
| File integrity monitoring (host-based IDS) | [implementing-file-integrity-monitoring-with-aide](references/implementing-file-integrity-monitoring-with-aide.md) · [configuring-host-based-intrusion-detection](references/configuring-host-based-intrusion-detection.md) |
| Application control / allowlisting and LOLBin deny rules | [implementing-application-whitelisting-with-applocker](references/implementing-application-whitelisting-with-applocker.md) |
| Full-disk encryption and key escrow | [implementing-disk-encryption-with-bitlocker](references/implementing-disk-encryption-with-bitlocker.md) |
| Exploit mitigations: DEP, ASLR, CFG | [implementing-memory-protection-with-dep-aslr](references/implementing-memory-protection-with-dep-aslr.md) |
| Endpoint data loss prevention, USB/device control | [implementing-endpoint-dlp-controls](references/implementing-endpoint-dlp-controls.md) · [implementing-usb-device-control-policy](references/implementing-usb-device-control-policy.md) |
| CIS hardening baselines for Windows and Linux | [hardening-windows-endpoint-with-cis-benchmark](references/hardening-windows-endpoint-with-cis-benchmark.md) · [hardening-linux-endpoint-with-cis-benchmark](references/hardening-linux-endpoint-with-cis-benchmark.md) |
| Workspace tenant hardening (Google Workspace, Microsoft 365) | [implementing-google-workspace-admin-security](references/implementing-google-workspace-admin-security.md) |
| AWS permission boundaries for delegated role creation | [implementing-aws-iam-permission-boundaries](references/implementing-aws-iam-permission-boundaries.md) |
| Assessing tenant identity attack resilience (authorized testing) | [auditing-entra-id-with-aadinternals](references/auditing-entra-id-with-aadinternals.md) · [attacking-entra-id-with-roadtools](references/attacking-entra-id-with-roadtools.md) · [attacking-oauth-with-device-code-phishing](references/attacking-oauth-with-device-code-phishing.md) · [post-exploiting-microsoft-graph-with-graphrunner](references/post-exploiting-microsoft-graph-with-graphrunner.md) |
| Anomalous sign-in detection (impossible travel, stuffing, spraying) | [detecting-anomalous-authentication-patterns](references/detecting-anomalous-authentication-patterns.md) |
| Endpoint evasion and fileless-attack evidence in logs | [detecting-evasion-techniques-in-endpoint-logs](references/detecting-evasion-techniques-in-endpoint-logs.md) · [detecting-fileless-attacks-on-endpoints](references/detecting-fileless-attacks-on-endpoints.md) |
| Endpoint compromise investigation and patch validation | [performing-endpoint-forensics-investigation](references/performing-endpoint-forensics-investigation.md) · [performing-endpoint-vulnerability-remediation](references/performing-endpoint-vulnerability-remediation.md) |

Executable helpers for each technique live in `scripts/<technique-name>/` — read
the reference file first, then run it.

## Output format

For a design or assessment, deliver:

```markdown
# <Scope> — Identity / Zero Trust / Endpoint Assessment

## Decision
One paragraph: what was changed or recommended and which risk it retires.

## Identity inventory
Class | Count | Owner | Assurance level | Standing privilege? | Last use

## Control state
Control | Status | Evidence | Reference file

## Access decisions
Resource | Required assurance | Signals evaluated | Policy action | Break-glass path

## Privileged access
Account | Tier | Vaulted? | JIT? | Approval | Session recorded?

## Endpoint baseline
Control | Baseline (L1/L2) | Pass % | Exceptions | Owner

## Findings
Severity | Finding | Exact location (policy, group, GPO, agent) | Fix

## Maturity
CISA pillar | Current tier | Target tier | Evidence

## Exceptions
Finding | Owner | Compensating control | Expiry
```

Every finding must name the concrete object — the policy, group, GPO, or agent
policy — and the command or query that demonstrates the gap.
