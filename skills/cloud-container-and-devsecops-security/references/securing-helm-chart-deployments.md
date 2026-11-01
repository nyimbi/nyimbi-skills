# Securing Helm Chart Deployments

## API Reference

## Helm Security Commands

| Command | Description |
|---------|-------------|
| `helm lint ./chart --strict` | Lint chart with strict mode |
| `helm template release ./chart` | Render templates locally |
| `helm verify chart.tgz` | Verify chart signature |
| `helm package ./chart --sign --key <key>` | Package and sign |
| `helm pull repo/chart --verify` | Pull with verification |

## Security Context Fields

| Field | Recommended | Description |
|-------|------------|-------------|
| `runAsNonRoot` | true | Prevent root execution |
| `readOnlyRootFilesystem` | true | Immutable filesystem |
| `allowPrivilegeEscalation` | false | Block privilege escalation |
| `capabilities.drop` | [ALL] | Drop all Linux capabilities |
| `seccompProfile.type` | RuntimeDefault | Syscall filtering |

## Security Checks

| Check | Severity | Risk |
|-------|----------|------|
| Privileged container | High | Full host access |
| hostNetwork enabled | High | Network namespace escape |
| hostPID enabled | High | Process namespace escape |
| :latest image tag | Medium | Non-reproducible builds |
| Missing resource limits | Medium | Resource exhaustion DoS |
| Missing readOnlyRootFilesystem | Medium | Writable filesystem |

## Template Scanning Tools

| Tool | Command |
|------|---------|
| kubesec | `kubesec scan rendered.yaml` |
| checkov | `checkov -f rendered.yaml --framework kubernetes` |
| trivy | `trivy config rendered.yaml` |
| kube-linter | `kube-linter lint rendered.yaml` |

## Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | stdlib | Execute helm/kubesec CLI |
| `re` | stdlib | Pattern matching in rendered YAML |
| `yaml` | PyYAML >=6.0 | Parse YAML content |
| `json` | stdlib | Report generation |

## References

- Helm Security: https://helm.sh/docs/topics/provenance/
- Helm Secrets Plugin: https://github.com/jkroepke/helm-secrets
- Kubesec: https://kubesec.io/

---

## Standards and Controls

## NIST SP 800-190
- Section 4.1: Image vulnerabilities and configuration defects
- Section 5.2: Registry security and chart provenance
- Section 5.4: Secure deployment configuration

## CIS Kubernetes Benchmark v1.8
- 5.2.1-5.2.9: Pod Security Standards enforced via chart defaults
- 5.7.3: Apply security context to pods and containers

## SLSA (Supply chain Levels for Software Artifacts)
- Level 1: Documented build process (Helm chart CI)
- Level 2: Source version controlled, signed provenance
- Level 3: Hardened build platform, signed artifacts
- Level 4: Two-party review, hermetic builds

## Helm Security Resources

| Resource | URL |
|----------|-----|
| Helm Security Best Practices | https://helm.sh/docs/chart_best_practices/ |
| Helm Provenance and Integrity | https://helm.sh/docs/topics/provenance/ |
| kube-linter | https://github.com/stackrox/kube-linter |
| checkov Kubernetes checks | https://www.checkov.io/5.Policy%20Index/kubernetes.html |
| helm-secrets plugin | https://github.com/jkroepke/helm-secrets |

## Compliance Mappings

### PCI DSS v4.0
- Req 6.3.1: Security vulnerabilities identified and managed
- Req 6.5.1: Changes controlled by change control processes

### SOC 2
- CC8.1: Change management - Controlled deployment processes

---

## Workflows

## Phase 1: Chart Development Security
1. Set secure defaults in values.yaml (non-root, read-only fs, resource limits)
2. Add network policy templates
3. Use external secrets references
4. Lint with `helm lint --strict`

## Phase 2: CI Pipeline
1. Render templates: `helm template test ./chart -f values.yaml > rendered.yaml`
2. Lint: `helm lint ./chart --strict`
3. Scan: `kube-linter lint rendered.yaml`
4. Scan: `checkov -f rendered.yaml --framework kubernetes`
5. Sign chart: `helm package ./chart --sign`

## Phase 3: Deployment
1. Verify chart signature: `helm verify chart.tgz`
2. Deploy with production values: `helm install release ./chart -f values-prod.yaml`
3. Verify deployment: `helm test release`

## Phase 4: Post-Deployment
1. Validate security contexts: `kubectl get pods -o jsonpath='{.items[*].spec.securityContext}'`
2. Check network policies applied
3. Verify secrets sourced from external store

## Phase 5: Maintenance
1. Update chart versions in lockfile
2. Rescan after dependency updates
3. Rotate signing keys annually

---

## Working Template

## Chart Metadata
- [ ] Chart.yaml has accurate appVersion and version
- [ ] No deprecated API versions in templates
- [ ] Chart signed with GPG key

## Security Context Defaults
- [ ] runAsNonRoot: true
- [ ] readOnlyRootFilesystem: true
- [ ] allowPrivilegeEscalation: false
- [ ] capabilities.drop: ALL
- [ ] seccompProfile: RuntimeDefault

## Resource Management
- [ ] CPU limits set
- [ ] Memory limits set
- [ ] CPU requests set
- [ ] Memory requests set

## Image Security
- [ ] Image uses digest or pinned tag (not :latest)
- [ ] imagePullPolicy: Always
- [ ] Images from trusted registries only

## Secrets Handling
- [ ] No secrets in values.yaml
- [ ] External secrets integration configured
- [ ] ServiceAccount token auto-mount disabled

## Network
- [ ] NetworkPolicy template included
- [ ] hostNetwork: false
- [ ] hostPID: false
- [ ] hostIPC: false

## RBAC
- [ ] ServiceAccount created per release
- [ ] Minimal RBAC permissions
- [ ] No cluster-admin bindings
