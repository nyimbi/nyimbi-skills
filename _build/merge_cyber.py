#!/usr/bin/env python3
"""Mechanical merge for the cybersecurity half of the skill bundle.

For every cluster in _build/cyber-clusters.json this creates:

    skills/<cluster>/
      LICENSE                          (Apache-2.0, if any source had one)
      references/technique-index.md    (generated; name/description/source)
      references/<technique>.md        (api-reference + standards + workflows + template)
      scripts/<technique>/<file>       (agent.py, process.py, ad-hoc helpers)

SKILL.md is deliberately NOT written here -- it is synthesized by hand/agent.

Idempotent: safe to re-run; overwrites its own outputs only.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path("/Users/nyimbiodero/src/ml/skills")
SRC = ROOT / "Cybersecurity-Skills" / "skills"
OUT = ROOT / "skill-bundle" / "skills"
BUILD = ROOT / "skill-bundle" / "_build"

# reference parts, in the order they get appended to the merged technique file
PARTS = [
    ("references/api-reference.md", "API Reference"),
    ("references/standards.md", "Standards and Controls"),
    ("references/workflows.md", "Workflows"),
    ("assets/template.md", "Working Template"),
    ("vulnerability-checklist.md", "Checklist"),
    ("secure-deployment-and-keys.md", "Secure Deployment and Keys"),
]

MEDIA = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".bin"}
SKIP_DIRS = {"__pycache__", ".DS_Store"}


_DESC_CACHE: dict[str, str] = {}


def titlecase(name: str) -> str:
    """configuring-tls-1-3-... -> Configuring TLS 1.3 ..."""
    keep = {"tls", "aes", "rsa", "dsa", "ml-kem", "ml-dsa", "x25519", "hsm",
            "jwt", "pqc", "tls1", "ntlm", "smb", "dcom", "ioc", "siem", "soar",
            "aws", "gcp", "azure", "k8s", "kubernetes", "docker", "ad", "ot",
            "ics", "scada", "modbus", "vpn", "dns", "http", "https", "smtp",
            "rest", "api", "sso", "mfa", "iam", "pam", "rbac", "cicd", "iac",
            "osint", "cti", "ttp", "yara", "sigma", "elf", "pe", "apk", "ios",
            "uuid", "url", "ssrf", "xss", "sqli", "rfi", "lfi", "rce", "xxe",
            "csrf", "csp", "ppc", "mft", "evtx", "mimikatz", "cobalt",
            "krb5", "saml", "oauth", "ldap", "pkcs", "ca", "crl", "ocsp"}
    out: list[str] = []
    for w in name.split("-"):
        lw = w.lower()
        if lw in keep:
            out.append(w.upper() if len(w) <= 4 else w)
        elif w.isdigit() and out and out[-1][-1:].isdigit():
            out[-1] = out[-1] + "." + w          # 1-3 -> 1.3
        elif w.isdigit():
            out.append(w)
        elif w[:1].isdigit():
            out.append(w)
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


def description_of(skill_dir: Path) -> str:
    """Full description from the source SKILL.md frontmatter (index.json truncates)."""
    p = skill_dir / "SKILL.md"
    if not p.is_file():
        return ""
    head = p.read_text(encoding="utf-8", errors="replace")
    if head.startswith("---"):
        end = head.find("\n---", 3)
        if end != -1:
            fm = head[3:end]
            m = re.search(r"^description:\s*(.*?)(?=^\w[\w-]*:|\Z)", fm,
                          re.M | re.S)
            if m:
                raw = m.group(1).strip()
                if raw[:1] in "'>\"":
                    raw = raw.lstrip(">-").strip().lstrip("'\"").strip()
                raw = raw.rstrip("'\"").strip()
                raw = " ".join(raw.split())
                if raw and raw != ">-":
                    return raw
    return _DESC_CACHE.get(p.parent.name, "")


def descriptions() -> dict[str, str]:
    idx = json.loads((ROOT / "Cybersecurity-Skills" / "index.json").read_text())
    _DESC_CACHE.update({s["name"]: " ".join(s["description"].split())
                        for s in idx["skills"]})
    return _DESC_CACHE


def merged_technique_md(skill_dir: Path, title: str) -> str | None:
    blocks: list[str] = []
    for rel, heading in PARTS:
        p = skill_dir / rel
        if not p.is_file():
            continue
        body = p.read_text(encoding="utf-8", errors="replace").strip()
        if not body:
            continue
        # strip a leading H1 that would clash with our own heading
        lines = body.splitlines()
        if lines and lines[0].startswith("# "):
            lines = lines[1:]
            while lines and not lines[0].strip():
                lines.pop(0)
        body = "\n".join(lines).strip()
        if not body:
            continue
        blocks.append(f"## {heading}\n\n{body}")
    if not blocks:
        return None
    return f"# {title}\n\n" + "\n\n---\n\n".join(blocks) + "\n"


def copy_scripts(skill_dir: Path, dest: Path) -> list[str]:
    copied: list[str] = []
    scripts = skill_dir / "scripts"
    if scripts.is_dir():
        target = dest / "scripts" / skill_dir.name
        for f in sorted(scripts.rglob("*")):
            if not f.is_file() or f.suffix in MEDIA:
                continue
            if SKIP_DIRS & {p.name for p in f.parents}:
                continue
            rel = f.relative_to(scripts)
            out = target / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, out)
            copied.append(str(out.relative_to(dest)))
    # loose helper scripts sitting at the technique root
    for f in sorted(skill_dir.iterdir()):
        if not f.is_file() or f.suffix not in {".py", ".ps1", ".sh"}:
            continue
        out = dest / "scripts" / skill_dir.name / f.name
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, out)
        copied.append(str(out.relative_to(dest)))
    return copied


def build() -> None:
    clusters = json.loads((BUILD / "cyber-clusters.json").read_text())
    descs = descriptions()
    provenance = {}
    totals = {"skills": 0, "technique_md": 0, "scripts": 0, "bytes": 0}

    for cluster, techniques in clusters.items():
        dest = OUT / cluster
        ref = dest / "references"
        ref.mkdir(parents=True, exist_ok=True)

        # --- licence -------------------------------------------------------
        lic_src = next(
            (SRC / t / "LICENSE" for t in techniques if (SRC / t / "LICENSE").is_file()),
            None,
        )
        if lic_src:
            shutil.copy2(lic_src, dest / "LICENSE")

        # --- per-technique merged reference + scripts -----------------------
        index_rows, copied_scripts = [], []
        for t in techniques:
            sd = SRC / t
            if not sd.is_dir():
                index_rows.append(f"| {t} | MISSING | — |")
                continue
            title = titlecase(t)
            md = merged_technique_md(sd, title)
            if md:
                (ref / f"{t}.md").write_text(md, encoding="utf-8")
                d = description_of(sd) or descs.get(t, "")
                index_rows.append(f"| [{t}]({t}.md) | {d} | `{t}/` |")
                totals["technique_md"] += 1
                totals["bytes"] += len(md)
            else:
                index_rows.append(f"| {t} | {descs.get(t, '')} | — |")
            copied_scripts += copy_scripts(sd, dest)

        # --- technique index ------------------------------------------------
        index = [
            f"# Technique index — {cluster.replace('-', ' ')}",
            "",
            f"Every technique merged into this skill ({len(techniques)} total).",
            "Generated — do not hand-edit. `Source` is the original skill directory",
            "in `Cybersecurity-Skills/skills/`, which holds its `agent.py` helpers.",
            "",
            "| Technique | What it covers | Source |",
            "|---|---|---|",
            *index_rows,
            "",
        ]
        (ref / "technique-index.md").write_text("\n".join(index), encoding="utf-8")

        # --- manifest --------------------------------------------------------
        n_scripts = len(copied_scripts)
        provenance[cluster] = {
            "skill": cluster,
            "merged_from_count": len(techniques),
            "near_duplicate_groups": near_dups(cluster),
            "source_roots": ["Cybersecurity-Skills"],
            "reference_files": sorted(f.name for f in ref.glob("*.md")),
            "scripts_copied": n_scripts,
        }
        totals["skills"] += 1
        totals["scripts"] += n_scripts
        print(
            f"{cluster:48s} techniques={len(techniques):4d} "
            f"refs={provenance[cluster]['reference_files'].__len__():4d} "
            f"scripts={n_scripts:4d}"
        )

    (BUILD / "provenance").mkdir(parents=True, exist_ok=True)
    for k, v in provenance.items():
        (BUILD / "provenance" / f"{k}.json").write_text(
            json.dumps(v, indent=2) + "\n", encoding="utf-8"
        )
    (BUILD / "cyber-totals.json").write_text(json.dumps(totals, indent=2) + "\n")
    print("\ntotals:", totals)


def near_dups(cluster: str) -> list[str]:
    """Known near-duplicate groups, merged into a single technique entry."""
    groups = {
        "cryptography-and-key-management": [
            "migrating-to-post-quantum-cryptography + performing-post-quantum-cryptography-migration",
            "configuring-hsm-for-key-storage + performing-hardware-security-module-integration",
        ],
        "threat-hunting-and-detection": [
            "detecting-fileless-attacks-on-endpoints + detecting-fileless-malware-techniques",
            "hunting-for-living-off-the-land-binaries + hunting-for-lolbins-execution-in-endpoint-logs + detecting-living-off-the-land-with-lolbas",
            "hunting-for-beaconing-with-frequency-analysis + hunting-for-command-and-control-beaconing",
        ],
        "security-incident-response-and-soc": [
            "triaging-security-incident + triaging-security-incident-with-ir-playbook",
            "building-soc-playbook-for-ransomware + building-ransomware-playbook-with-cisa-framework",
        ],
        "cloud-container-and-devsecops-security": [
            "implementing-container-network-policies-with-calico + implementing-kubernetes-network-policy-with-calico + implementing-network-policies-for-kubernetes",
            "implementing-pod-security-admission-controller + implementing-kubernetes-pod-security-standards",
            "scanning-docker-images-with-trivy + scanning-containers-with-trivy-in-cicd + scanning-iac-and-images-with-trivy + performing-container-security-scanning-with-trivy",
            "implementing-cloud-security-posture-management + implementing-cloud-vulnerability-posture-management",
        ],
        "application-api-mobile-and-ai-security": [
            "testing-for-xss-vulnerabilities + testing-for-xss-vulnerabilities-with-burpsuite",
            "testing-for-json-web-token-vulnerabilities + testing-jwt-token-security",
            "performing-api-security-testing-with-postman + performing-api-fuzzing-with-restler",
            "implementing-api-rate-limiting-and-throttling + implementing-api-abuse-detection-with-rate-limiting + performing-api-rate-limiting-bypass",
            "implementing-llm-guardrails-for-security + defending-llms-with-guardrails",
        ],
        "identity-zero-trust-and-endpoint-security": [
            "implementing-passwordless-authentication-with-fido2 + implementing-passwordless-auth-with-microsoft-entra",
            "implementing-just-in-time-access-provisioning + implementing-zero-standing-privilege-with-cyberark",
            "implementing-zero-trust-network-access + implementing-zero-trust-network-access-with-zscaler",
            "implementing-beyondcorp-zero-trust-access-model + implementing-zero-trust-with-beyondcorp",
        ],
        "threat-intelligence-osint-and-phishing-defense": [
            "implementing-stix-taxii-feed-integration + processing-stix-taxii-feeds + implementing-taxii-server-with-opentaxii",
            "performing-threat-intelligence-sharing-with-misp + collecting-threat-intelligence-with-misp + building-threat-feed-aggregation-with-misp",
            "performing-dark-web-monitoring-for-threats + monitoring-darkweb-sources",
            "detecting-typosquatting-packages + detecting-typosquatting-packages-in-npm-pypi",
        ],
        "network-and-wireless-security": [
            "implementing-next-generation-firewall-with-palo-alto + implementing-cloud-waf-rules + securing-api-gateway-with-aws-waf",
        ],
        "malware-analysis-and-reverse-engineering": [
            "performing-memory-forensics-with-volatility3 + performing-memory-forensics-with-volatility3-plugins + analyzing-memory-dumps-with-volatility + conducting-memory-forensics-with-volatility",
            "analyzing-windows-prefetch-with-python + analyzing-prefetch-files-for-execution-history",
        ],
        "digital-forensics-and-evidence": [
            "performing-network-forensics-with-wireshark + analyzing-network-traffic-with-wireshark",
            "performing-windows-artifact-analysis-with-eric-zimmerman-tools + parsing-artifacts-with-eric-zimmerman-tools",
        ],
        "offensive-security-and-red-teaming": [
            "performing-red-team-phishing-with-gophish + performing-phishing-simulation-with-gophish + executing-phishing-simulation-campaign",
            "building-c2-infrastructure-with-sliver-framework + operating-sliver-c2",
            "building-red-team-c2-infrastructure-with-havoc + operating-havoc-c2",
        ],
        "vulnerability-management-and-compliance": [
            "performing-authenticated-vulnerability-scan + performing-authenticated-scan-with-openvas",
            "implementing-vulnerability-remediation-sla + implementing-vulnerability-sla-breach-alerting",
        ],
    }
    return groups.get(cluster, [])


if __name__ == "__main__":
    build()
