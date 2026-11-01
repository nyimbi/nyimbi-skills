# Implementing GCP Binary Authorization

## API Reference

## gcloud CLI Commands

```bash
# Enable APIs
gcloud services enable binaryauthorization.googleapis.com containeranalysis.googleapis.com

# Enable on GKE cluster
gcloud container clusters update CLUSTER --enable-binauthz --zone ZONE

# Export policy
gcloud container binauthz policy export --project PROJECT_ID

# Import policy
gcloud container binauthz policy import policy.yaml

# Create attestor
gcloud container binauthz attestors create ATTESTOR_NAME \
  --attestation-authority-note=NOTE_ID \
  --attestation-authority-note-project=PROJECT_ID

# Create attestation
gcloud container binauthz attestations sign-and-create \
  --artifact-url="gcr.io/PROJECT/IMAGE@DIGEST" \
  --attestor="ATTESTOR" --attestor-project="PROJECT" \
  --keyversion-project=PROJECT --keyversion-location=global \
  --keyversion-keyring=KEYRING --keyversion-key=KEY --keyversion=1
```

## Policy Structure

| Field | Values | Description |
|-------|--------|-------------|
| `evaluationMode` | ALWAYS_ALLOW, ALWAYS_DENY, REQUIRE_ATTESTATION | How images are evaluated |
| `enforcementMode` | ENFORCED_BLOCK_AND_AUDIT_LOG, DRYRUN_AUDIT_LOG_ONLY | Block or audit-only |
| `globalPolicyEvaluationMode` | ENABLE, DISABLE | Google-maintained system policy |

## Break-Glass Annotation

```yaml
metadata:
  annotations:
    alpha.image-policy.k8s.io/break-glass: "Emergency - INC-12345"
```

## Cloud Logging Filter (CV Violations)

```
resource.type="k8s_cluster"
logName="projects/PROJECT/logs/binaryauthorization.googleapis.com%2Fcontinuous_validation"
```

### References

- GCP Binary Authorization: https://cloud.google.com/binary-authorization/docs
- Container Analysis API: https://cloud.google.com/container-analysis/docs
- SLSA Framework: https://slsa.dev

---

## Standards and Controls

## SLSA Framework Levels
- SLSA 1: Documentation of build process
- SLSA 2: Tamper resistance of build service
- SLSA 3: Extra resistance to threats
- SLSA 4: Highest levels of confidence and trust

## NIST 800-53
- SA-10: Developer Configuration Management
- SA-12: Supply Chain Protection
- SI-7: Software, Firmware, and Information Integrity

## CIS GKE Benchmark
- 6.10.4: Ensure Binary Authorization is enabled for GKE clusters

---

## Workflows

## Attestation Pipeline
```
1. Developer pushes code
2. Cloud Build triggers container build
3. Vulnerability scan runs on built image
4. If scan passes → Create cryptographic attestation
5. Push attested image to registry
6. GKE validates attestation at deploy time
7. Continuous validation monitors running pods
```

## Break-Glass Procedure
```
1. Emergency identified → Create incident ticket
2. Apply break-glass annotation to pod spec
3. Deploy with override documented
4. Alert security team of break-glass usage
5. Post-incident: Review and attest emergency image
6. Remove break-glass annotation
```

---

## Working Template

## Configuration
| Setting | Value |
|---------|-------|
| Project ID | |
| GKE Cluster | |
| Attestor Name | |
| KMS Key Location | |
| Policy Mode | Enforce / Dry-Run |

## Attestor Checklist
- [ ] KMS keyring and key created
- [ ] Container Analysis note created
- [ ] Attestor created and linked to note
- [ ] Public key added to attestor
- [ ] CI/CD pipeline creates attestations
- [ ] Break-glass procedure documented

## Policy Configuration
| Rule | Scope | Mode | Attestors Required |
|------|-------|------|--------------------|
| Default | All clusters | | |
| Production | prod-cluster | | |
| Staging | staging-cluster | | |
