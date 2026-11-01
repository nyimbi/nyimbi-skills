# Performing kubernetes Etcd Security Assessment

## API Reference

## Libraries Used
- **subprocess**: Execute kubectl, etcdctl commands
- **json**: Parse Kubernetes API resource output
- **re**: Extract etcd server URLs from API server arguments

## CLI Interface
```
python agent.py [--kubeconfig ~/.kube/config] encrypt
python agent.py access --endpoint https://127.0.0.1:2379 [--cert client.crt --key client.key --cacert ca.crt]
python agent.py secrets
python agent.py tls
python agent.py full [--endpoint https://127.0.0.1:2379]
```

## Core Functions

### `check_etcd_encryption(kubeconfig)` — Verify encryption at rest
Inspects kube-apiserver pod args for `--encryption-provider-config`, audit logging, TLS.

### `check_etcd_access(endpoint, cert, key, cacert)` — Test access controls
Uses etcdctl to check health and test for unauthenticated read access.
CRITICAL finding if data readable without credentials.

### `dump_secrets_check(kubeconfig)` — Audit stored secrets
Lists all cluster secrets, categorizes by type, identifies sensitive naming patterns.

### `check_etcd_tls_config()` — Verify TLS certificates
Checks etcd pod args for peer TLS, client TLS, and client certificate authentication.

### `full_assessment(kubeconfig, endpoint)` — Comprehensive security scan
Combines all checks into single report with risk level classification.

## Security Checks
| Check | Flag | Risk |
|-------|------|------|
| Encryption at rest | --encryption-provider-config | CRITICAL if missing |
| Client TLS | --cert-file / --key-file | HIGH if missing |
| Peer TLS | --peer-cert-file / --peer-key-file | HIGH if missing |
| Client cert auth | --client-cert-auth=true | MEDIUM if missing |
| Unauthenticated access | etcdctl get without certs | CRITICAL |

## Dependencies
System: kubectl, etcdctl (etcd client)
No Python packages required.

---

## Standards and Controls

## CIS Kubernetes Benchmark v1.9 - Section 2: etcd
- 2.1: Ensure cert-file and key-file arguments are set
- 2.2: Ensure client-cert-auth argument is set to true
- 2.3: Ensure auto-tls argument is not set to true
- 2.4: Ensure peer-cert-file and peer-key-file arguments are set
- 2.5: Ensure peer-client-cert-auth argument is set to true
- 2.6: Ensure peer-auto-tls argument is not set to true
- 2.7: Ensure a unique Certificate Authority is used for etcd

## NIST SP 800-190
- Section 3.4.4: Data store encryption requirements
- Section 4.4.2: Secrets management for orchestrators

## Compliance Mapping
| Control | PCI DSS | SOC 2 | HIPAA |
|---------|---------|-------|-------|
| Encryption at rest | 3.4 | CC6.1 | 164.312(a)(2)(iv) |
| TLS transport | 4.1 | CC6.7 | 164.312(e)(1) |
| Access control | 7.1 | CC6.3 | 164.312(a)(1) |
| Backup encryption | 3.4 | CC6.1 | 164.310(d)(2)(iv) |

---

## Workflows

## Assessment Workflow
1. Verify etcd TLS configuration (client and peer)
2. Check encryption at rest configuration
3. Validate secrets are encrypted in etcd storage
4. Audit network access restrictions to etcd ports
5. Review etcd certificate expiration dates
6. Validate backup encryption and storage security
7. Test key rotation procedure
8. Document findings and remediation plan

## Remediation Priority
1. Enable TLS for all etcd communication (Critical)
2. Configure encryption at rest for secrets (Critical)
3. Restrict network access to etcd (High)
4. Implement automated backup encryption (High)
5. Schedule certificate rotation (Medium)
6. Deploy etcd monitoring and alerting (Medium)

---

## Working Template

## Cluster Information
| Field | Value |
|-------|-------|
| Cluster Name | |
| etcd Version | |
| Node Count | |
| Assessment Date | |

## Assessment Results
| Check | Status | Notes |
|-------|--------|-------|
| TLS client communication | | |
| TLS peer communication | | |
| Client cert authentication | | |
| Encryption at rest | | |
| Network isolation | | |
| Backup encryption | | |
| Certificate expiration | | |

## Sign-Off
| Role | Name | Date |
|------|------|------|
| Security Engineer | | |
| Platform Lead | | |
