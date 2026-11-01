# Zero trust network access — one decision, many vendors

ZTNA answers a single question: *for this request, from this user on this device,
to this application, is access allowed?* Pick the enforcement model first, then
the product. Ten of the techniques in this skill are the same decision with a
different vendor CLI, so treat them as options in one table, not ten designs.

## What every ZTNA design must specify

| Decision | Options | Wrong answer |
|---|---|---|
| Trust anchor | IdP assertion (SAML/OIDC) + device posture, mTLS workload cert | "The user is on the corporate network" |
| Application exposure | App connector / tunnel outbound-only, or private endpoint | Publishing the app to the internet with a WAF in front |
| Policy inputs | User/group, device compliance, geo/IP reputation, risk score, app sensitivity | User identity alone |
| Default | Deny; no implicit reachability from any network | Allow by network location |
| Session | Continuous or step-up re-evaluation, short-lived credentials | One login that lasts until logout |
| Fallback | Explicit break-glass path with post-facto review | Shadow VPN "just for admins" |

## Vendor options

| Product | Enforcement point | Best fit | Technique file |
|---|---|---|---|
| Google IAP / BeyondCorp | Google edge, per-request | GCP-hosted and Google-protected apps | `configuring-identity-aware-proxy-with-google-iap.md`, `implementing-beyondcorp-zero-trust-access-model.md`, `implementing-zero-trust-with-beyondcorp.md` |
| AWS Verified Access | AWS edge, Cedar policy | Private apps behind ALB/NLB in AWS | `configuring-aws-verified-access-for-ztna.md` |
| Azure Private Link + Conditional Access | Azure private endpoint + CA | Azure PaaS and internal apps | [`implementing-zero-trust-network-access.md`](../../cloud-container-and-devsecops-security/references/implementing-zero-trust-network-access.md) |
| Zscaler Private Access | Zscaler Zero Trust Exchange, App Connectors | Existing Zscaler/SASE estate, VPN replacement | `configuring-zscaler-private-access-for-ztna.md`, `implementing-zero-trust-network-access-with-zscaler.md` |
| Cloudflare Access + Tunnel | Cloudflare edge, WARP posture | Self-hosted and mixed-hosting apps | `deploying-cloudflare-access-for-zero-trust.md` |
| Palo Alto Prisma Access | GlobalProtect + ZTNA Connectors | Existing Palo Alto policy estate | `deploying-palo-alto-prisma-access-zero-trust.md` |
| Hashicorp Boundary | Brokered SSH/RDP/db sessions | Infrastructure access with session recording | `implementing-zero-trust-with-hashicorp-boundary.md` |
| Tailscale | WireGuard mesh + ACLs | Small fleets, dev and hybrid mesh | `deploying-tailscale-for-zero-trust-vpn.md` |
| CSA SDP (SPA + mTLS) | Controller/gateway, single packet auth | Highest-assurance, low-latency-tolerant | `deploying-software-defined-perimeter.md` |

## Migration pattern

1. Inventory applications and classify sensitivity; leave everything else on the
   legacy path.
2. Put one low-risk internal app behind the chosen product in monitor mode.
3. Write deny-by-default policy with device posture as a required input; verify
   that a non-compliant device is refused.
4. Move admin/infrastructure access next (highest payoff), with session recording.
5. Retire the VPN split-tunnel only after coverage and break-glass are proven.

Microsegmentation (`configuring-microsegmentation-for-zero-trust.md`,
`implementing-microsegmentation-with-guardicore.md`) is the east-west companion:
ZTNA governs who reaches the app, segmentation governs what the app can reach.
