# Posture management — CSPM, CWP/CWPP, CIEM, and how they differ

Four labels that vendor decks use interchangeably. They answer different
questions, run at different times, and produce findings that must not be merged
into one undifferentiated queue.

| Layer | Question it answers | When it sees the problem | Typical finding | Representative tools |
|---|---|---|---|---|
| **CSPM** — Cloud Security Posture Management | Is the *configuration* of cloud resources wrong? | Continuously, at rest, from cloud APIs | "S3 bucket `logs-prod` allows public ACL" | Prowler, ScoutSuite, AWS Security Hub, Defender for Cloud, GCP Security Command Center |
| **CIEM** — Cloud Infrastructure Entitlement Management | Who can do *what* to which cloud resource, and can they escalate? | Continuously, from IAM policy graphs | "This role can `iam:PassRole` + `lambda:UpdateFunctionCode` → admin" | IAM Access Analyzer, Cloudsplaining, Policy Analyzer, IAM Recommender |
| **CWP / CWPP** — Cloud Workload Protection | Is the *running workload* behaving wrongly? | At runtime, on the host or in the node | "Unexpected `xmrig` process in container `api-7f3`" | Falco, Tetragon, Defender for Servers/Containers, Inspector Runtime Monitoring |
| **Vulnerability management on cloud assets** | Is there a known CVE in the image/AMI/package? | At build, at registry, and periodically on running assets | "Log4j 2.14.1 in image `app:sha`" | Trivy, Inspector, provider image scanning — prioritization and SLA belong to the vulnerability-management-and-compliance skill |

## Boundary rules

- CSPM findings are configuration facts. Auto-remediate the safe subset
  (public access block, encryption at rest, logging on) with Config rules /
  Azure Policy / Organization Policy; route the rest to an owner.
- CWPP findings are behavioral facts. They need a response playbook, not a
  ticket — a cryptominer or escape attempt is an incident trigger.
- A CSPM score is not a security outcome. CIS benchmark version must be pinned
  (AWS v5.0, Azure v4.0, GCP v4.0); silently tracking "latest" moves the goalposts
  under you and breaks period-over-period reporting.
- Multi-cloud aggregation (Security Hub, Defender, SCC, or a Prowler pipeline)
  must de-duplicate on (resource, control), not on (finding id), or the same
  broken control appears once per tool.

## CIS assessment pattern

1. Pin benchmark version and profile level per provider (L1 = hygiene without
   functional loss; L2 = defense in depth, expect exceptions).
2. Run `prowler <provider> --compliance cis_<ver>_<provider>` on a schedule into
   dated output directories.
3. Parse failures per section; prioritize L1 failures first, then L2 with a
   documented exception path.
4. Keep the raw JSON as evidence; dashboards are views over it, not the record.
