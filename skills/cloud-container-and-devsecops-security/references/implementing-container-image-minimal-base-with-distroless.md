# Implementing Container Image Minimal Base With Distroless

## API Reference

## Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| trivy CLI | >=0.50 | Container vulnerability scanning (subprocess) |
| docker CLI | >=24.0 | Image inspection and property checks (subprocess) |

## CLI Usage

```bash
python scripts/agent.py \
  --images gcr.io/distroless/static-debian12 python:3.12-slim \
  --compare python:3.12 gcr.io/distroless/python3-debian12 \
  --output-dir /reports/
```

## Functions

### `run_trivy_scan(image) -> dict`
Runs `trivy image --format json --severity CRITICAL,HIGH,MEDIUM`.

### `get_image_size(image) -> int`
Runs `docker inspect --format {{.Size}}` for byte count.

### `count_vulns_by_severity(scan_data) -> dict`
Parses Trivy JSON Results for CRITICAL/HIGH/MEDIUM/LOW counts.

### `compare_images(base_image, distroless_image) -> dict`
Scans both images, computes size and vulnerability reduction percentages.

### `check_distroless_properties(image) -> dict`
Tests for shell access and package manager presence via `docker run`.

### `generate_report(images, distroless_pairs) -> dict`
Full analysis with individual scans, comparisons, and summary.

## Distroless Properties Checked

| Property | Check Method |
|----------|-------------|
| Shell access | `docker run --entrypoint "" image sh -c "echo"` |
| Package manager | `docker run --entrypoint "" image which apt/apk/yum` |

## Output Schema

```json
{
  "summary": {"images_scanned": 4, "minimal_images": 2},
  "comparisons": [{"size_reduction_pct": 82.3, "vuln_reduction_pct": 95.0}],
  "image_scans": [{"image": "gcr.io/distroless/static", "is_minimal": true}]
}
```

---

## Standards and Controls

## NIST SP 800-190
- Section 3.1.1: Minimize image content to reduce attack surface
- Section 4.1.1: Use minimal base images for container builds

## CIS Docker Benchmark v1.6
- 4.1: Ensure a user for the container has been created
- 4.2: Ensure containers use trusted base images
- 4.6: Ensure HEALTHCHECK instructions have been added
- 4.9: Ensure COPY is used instead of ADD

## OWASP Docker Security
- D2: Patch Management Strategies (fewer packages = fewer patches)
- D3: Network Segmentation and Firewalling
- D4: Secure Defaults and Hardening (no shell = hardened by default)

---

## Workflows

## Migration Workflow
1. Identify current base image and its package footprint
2. Select appropriate distroless variant for your runtime
3. Create multi-stage Dockerfile with build and runtime stages
4. Test application functionality with distroless base
5. Scan both old and new images to compare CVE counts
6. Update debugging procedures (ephemeral containers, debug variants)
7. Deploy to staging and validate
8. Roll out to production

## Image Build Pipeline
1. Build application in builder stage (full SDK image)
2. Copy only runtime artifacts to distroless stage
3. Set non-root user via `:nonroot` tag
4. Scan final image with Trivy/Grype
5. Sign image with cosign
6. Push to registry with digest pinning

---

## Working Template

## Application Information
| Field | Value |
|-------|-------|
| Application Name | |
| Current Base Image | |
| Runtime | |
| Target Distroless Image | |

## Migration Checklist
- [ ] Multi-stage Dockerfile created
- [ ] Application tested with distroless base
- [ ] Image scanned for vulnerabilities (before/after comparison)
- [ ] Non-root user configured
- [ ] Debug procedures documented
- [ ] CI/CD pipeline updated

## Vulnerability Comparison
| Metric | Before | After |
|--------|--------|-------|
| Image Size | | |
| Critical CVEs | | |
| High CVEs | | |
| Total CVEs | | |

## Sign-Off
| Role | Name | Date |
|------|------|------|
| Developer | | |
| Security Engineer | | |
