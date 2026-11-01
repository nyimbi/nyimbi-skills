# Configuring Identity Aware Proxy With Google Iap

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| google-cloud-iap | `pip install google-cloud-iap` | IAP admin and settings management |
| google-cloud-resource-manager | `pip install google-cloud-resource-manager` | GCP project enumeration |

## Key IAP Client Methods

| Method | Description |
|--------|-------------|
| `IdentityAwareProxyAdminServiceClient()` | Create IAP admin client |
| `get_iap_settings(name=)` | Get IAP configuration for a resource |
| `update_iap_settings(iap_settings=, update_mask=)` | Update IAP settings |
| `get_iam_policy(resource=)` | Get IAP IAM bindings |
| `set_iam_policy(resource=, policy=)` | Set IAP IAM bindings |
| `list_tunnel_dest_groups(parent=)` | List TCP forwarding tunnel groups |

## IAP IAM Roles

| Role | Description |
|------|-------------|
| `roles/iap.httpsResourceAccessor` | Access IAP-protected web resources |
| `roles/iap.tunnelResourceAccessor` | Access IAP TCP forwarding tunnels |
| `roles/iap.admin` | Full IAP administration |

## gcloud CLI Commands

```bash
gcloud iap web enable --resource-type=app-engine
gcloud iap tcp enable --resource-type=compute --dest-group=GROUP
gcloud iap web get-iam-policy --project=PROJECT
gcloud compute ssh INSTANCE --tunnel-through-iap
```

## External References

- [Google IAP Documentation](https://cloud.google.com/iap/docs)
- [google-cloud-iap Python Reference](https://cloud.google.com/python/docs/reference/iap/latest)
- [IAP Programmatic Auth](https://cloud.google.com/iap/docs/authentication-howto)

---

## Standards and Controls

## NIST SP 800-207: Zero Trust Architecture
- **Section 3.1**: Policy Engine - IAP evaluates identity and context per request
- **Section 3.2**: Trust Algorithm - Access Levels compute trust score
- **Section 4.2**: SDP Gateway Model - IAP acts as application-layer gateway
- **URL**: https://csrc.nist.gov/publications/detail/sp/800-207/final

## CISA Zero Trust Maturity Model v2.0
- **Identity Pillar**: Per-request identity verification via IAP
- **Application Pillar**: Application-level access controls
- **URL**: https://www.cisa.gov/zero-trust-maturity-model

## Google Cloud Documentation
- **IAP Overview**: https://cloud.google.com/iap/docs/concepts-overview
- **Enabling IAP for Compute Engine**: https://cloud.google.com/iap/docs/enabling-compute-howto
- **Enabling IAP for App Engine**: https://cloud.google.com/iap/docs/app-engine-quickstart
- **Enabling IAP for Cloud Run**: https://cloud.google.com/iap/docs/enabling-cloud-run
- **IAP TCP Forwarding**: https://cloud.google.com/iap/docs/using-tcp-forwarding
- **Context-Aware Access**: https://cloud.google.com/iap/docs/cloud-iap-context-aware-access-howto
- **Managing Access**: https://cloud.google.com/iap/docs/managing-access
- **Access Context Manager**: https://cloud.google.com/access-context-manager/docs
- **Programmatic Authentication**: https://cloud.google.com/iap/docs/authentication-howto

## Google BeyondCorp Papers
- **BeyondCorp: A New Approach to Enterprise Security** (2014): https://research.google/pubs/pub43231/
- **BeyondCorp: The Access Proxy** (2017): https://research.google/pubs/pub45728/

## FedRAMP
- Google Cloud IAP operates within FedRAMP High boundary
- **URL**: https://cloud.google.com/security/compliance/fedramp

---

## Workflows

## Phase 1: Prerequisites (Day 1)
1. Enable IAP API: `gcloud services enable iap.googleapis.com`
2. Enable Access Context Manager API
3. Configure OAuth consent screen with organization branding
4. Create OAuth client credentials for IAP
5. Verify applications are behind HTTPS Load Balancer or Cloud Run/App Engine

## Phase 2: IAP Enablement (Day 2-3)

### Compute Engine / GKE Backend Services
1. Enable IAP on each backend service with OAuth credentials
2. Configure health checks to work through IAP
3. Verify backend service firewall rules allow only load balancer and IAP ranges
4. Block direct access to backend instances (remove external IPs, restrict firewall)

### App Engine
1. Enable IAP on App Engine with OAuth credentials
2. Verify no App Engine firewall rules bypass IAP
3. Test authentication flow with pilot users

### Cloud Run
1. Grant IAP service account Cloud Run Invoker role
2. Configure Cloud Run service with `--no-allow-unauthenticated`
3. Enable IAP on the backend service fronting Cloud Run
4. Test end-to-end request flow

### TCP Forwarding (SSH/RDP)
1. Grant IAP Tunnel Resource Accessor role to user groups
2. Remove public IP addresses from VMs
3. Configure firewall rules to allow only IAP tunnel IP ranges (35.235.240.0/20)
4. Test SSH/RDP access through IAP tunnel

## Phase 3: Access Control (Day 4-5)
1. Create IAM bindings mapping Google Groups to backend services
2. Add access level conditions for sensitive applications
3. Configure time-based conditions for admin access
4. Set up path-based conditions for API access
5. Test each binding with authorized and unauthorized users

## Phase 4: Access Levels (Day 6-7)
1. Create basic access levels for device posture (encryption, OS, screen lock)
2. Create IP-based access levels for corporate network
3. Create custom access levels with CEL for complex conditions
4. Apply access levels as conditions on IAM bindings
5. Validate with compliant and non-compliant devices

## Phase 5: Session and Re-auth (Day 8)
1. Configure session duration per application tier
2. Set re-authentication method (LOGIN or SECURE_KEY)
3. Test session expiry and re-authentication flow
4. Document expected user experience

## Phase 6: Audit and Monitoring (Day 9-10)
1. Enable data access audit logs for IAP
2. Create log-based metrics for access denials
3. Set up alerting for anomalous patterns
4. Build dashboard for IAP access analytics
5. Test break-glass access procedures

---

## Working Template

## Project Information
| Field | Value |
|-------|-------|
| GCP Project | ecommerce-internal-prod |
| Organization | E-Commerce Corp |
| IAP OAuth Brand | Corporate Applications |
| Lead | Security Engineering |

## IAP Backend Service Configuration

| Service | Platform | IAP Enabled | Access Level | Re-auth | Groups |
|---------|----------|-------------|-------------|---------|--------|
| admin-dashboard | GKE | Yes | managed-device | 1h / SECURE_KEY | admins@ |
| internal-api | Cloud Run | Yes | corp-network | 8h / LOGIN | engineering@ |
| monitoring | GKE | Yes | None | 8h / LOGIN | sre@, engineering@ |
| hr-portal | Compute Engine | Yes | high-trust | 4h / LOGIN | hr@ |
| finance-app | Compute Engine | Yes | high-trust | 1h / SECURE_KEY | finance@ |
| wiki | App Engine | Yes | None | 8h / LOGIN | all-staff@ |

## Access Levels

| Level Name | Type | Device Policy | Encryption | IP Restriction | Region |
|-----------|------|--------------|------------|---------------|--------|
| managed-device | Basic | Admin-approved, Screen lock | ENCRYPTED | None | US, GB |
| corp-network | Basic | None | None | 203.0.113.0/24 | US |
| high-trust | Custom (CEL) | Admin-approved, Encrypted | ENCRYPTED | Corp network OR ChromeOS | US |

## IAP TCP Tunnel Access

| VM | Zone | IAP Tunnel | Groups | External IP Removed |
|----|------|-----------|--------|-------------------|
| bastion-1 | us-central1-a | SSH | sre@ | Yes |
| db-admin | us-central1-b | SSH | dba@ | Yes |
| windows-admin | us-east1-b | RDP | admins@ | Yes |

## Validation Checklist
- [x] IAP enabled on all internal backend services
- [x] Direct access blocked (no public IPs, firewall rules restrict to LB + IAP)
- [x] Access levels applied to sensitive services
- [x] Re-authentication configured per sensitivity tier
- [x] Break-glass IAM binding created without access level conditions
- [ ] Service account programmatic access tested
- [x] Audit logs enabled and flowing to BigQuery
- [x] Alert policies created for access denials

## Sign-Off
| Role | Name | Date | Approved |
|------|------|------|----------|
| Security Architect | _________________ | __________ | [ ] |
| Cloud Platform Lead | _________________ | __________ | [ ] |
