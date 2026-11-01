# Detecting Typosquatting Packages

## API Reference

## typomania (Rust library)

| Item | Description |
|------|-------------|
| `Harness` | Primary struct; `Harness::check(name)` compares a candidate against the corpus |
| `Corpus` trait | Implement to provide the popular-name reference set for any registry |
| `Package` trait | Implement to expose a package's name/metadata to the harness |
| `rayon` feature | Enabled by default; parallelizes `Harness::check` across many packages |
| `cargo run --example registry` | Runs the bundled example against a fake registry |

## OSSGadget oss-find-squats

| Command | Purpose |
|---------|---------|
| `oss-find-squats pkg:npm/<name>` | Generate squat candidates of an npm package and report which exist |
| `oss-find-squats pkg:pypi/<name>` | Same for PyPI |
| `oss-find-squats pkg:cargo/<name>` | Same for crates.io |
| `oss-find-squats --quiet <purl>` | Suppress non-finding output |

Package URL (purl) format: `pkg:<type>/<namespace>/<name>@<version>`

## pypi-scan (IQTLabs)

| Command | Purpose |
|---------|---------|
| `python pypi_scan.py -p <package>` | Find candidate typosquats of one package |
| `python pypi_scan.py -n <N>` | Scan the top-N most-downloaded PyPI packages |

## Registry metadata endpoints

| Endpoint | Returns |
|----------|---------|
| `https://registry.npmjs.org/<pkg>` | Full npm package doc (time, maintainers, versions, scripts) |
| `https://api.npmjs.org/downloads/point/last-week/<pkg>` | npm weekly download count |
| `https://pypi.org/pypi/<pkg>/json` | PyPI info, releases, author, urls |
| `https://crates.io/api/v1/crates/<pkg>` | crates.io crate metadata (requires User-Agent) |
| `https://registry.npmjs.org/-/v1/search?text=...&popularity=1.0` | npm popularity search |

## Risk-scoring signals

| Signal | High-risk value |
|--------|-----------------|
| Edit distance to popular name | 1–2 |
| Package age | < 90 days |
| Weekly downloads | < 1000 |
| Install scripts | `preinstall` / `postinstall` / network in `setup.py` |
| Maintainer overlap | Different maintainer than legit package |
| Repository URL | Missing, or points to legit project (impersonation) |

---

## Standards and Controls

## MITRE ATT&CK

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| T1195.002 | Supply Chain Compromise: Compromise Software Supply Chain | Initial Access | A typosquatted package is the malicious artifact the attacker gets installed in place of the legitimate dependency, compromising the victim's software supply chain at install time. |

## NIST Cybersecurity Framework 2.0

| ID | Name | Rationale |
|----|------|-----------|
| ID.RA-09 | The authenticity and integrity of hardware and software is assessed prior to acquisition and use | Pre-installation typosquat screening is exactly the activity of assessing a package's authenticity before it enters the environment. |

## Official Resources

- typomania (Rust Foundation): https://github.com/rustfoundation/typomania
- typogard (original research tool): https://github.com/mt3443/typogard
- "Defending Against Package Typosquatting" (Taylor et al., University of Kansas)
- Microsoft OSSGadget: https://github.com/microsoft/OSSGadget
- IQTLabs pypi-scan: https://github.com/IQTLabs/pypi-scan
- ecosyste-ms typosquatting-dataset: https://github.com/ecosyste-ms/typosquatting-dataset
- OWASP CI/CD Security Top 10: https://owasp.org/www-project-top-10-ci-cd-security-risks/
- top-pypi-packages corpus: https://hugovk.github.io/top-pypi-packages/

## Key Research

- Rust Foundation: typomania powers crates.io typosquatting detection
- JFrog / Sonatype: annual reports on registry typosquatting and "slopsquatting" trends
