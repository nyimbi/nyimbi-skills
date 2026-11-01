# Conducting Internal Reconnaissance With Bloodhound Ce

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| neo4j | `pip install neo4j` | Neo4j graph database driver for Cypher queries |
| bloodhound | `pip install bloodhound` | Python ingestor for AD data collection |
| requests | `pip install requests` | BloodHound CE REST API client |

## Key neo4j Driver Methods

| Method | Description |
|--------|-------------|
| `GraphDatabase.driver(uri, auth=(user, pass))` | Connect to Neo4j |
| `driver.session()` | Open a session for queries |
| `session.run(cypher, **params)` | Execute Cypher query |
| `driver.close()` | Close driver connection |

## Critical Cypher Queries

| Query Purpose | Cypher Pattern |
|---------------|----------------|
| Path to DA | `MATCH p=shortestPath((u:User)-[*1..]->(g:Group {name:"DOMAIN ADMINS@..."}))` |
| Kerberoastable | `MATCH (u:User) WHERE u.hasspn = true AND u.enabled = true` |
| Unconstrained Delegation | `MATCH (c:Computer) WHERE c.unconstraineddelegation = true` |
| AS-REP Roastable | `MATCH (u:User) WHERE u.dontreqpreauth = true` |
| DCSync rights | `MATCH p=(u)-[:GetChanges|GetChangesAll]->(d:Domain)` |

## BloodHound Python Ingestor

```bash
bloodhound-python -d domain.local -u user -p pass -ns DC_IP -c all --zip
```

Collection methods: `all`, `group`, `localadmin`, `session`, `trusts`, `objectprops`, `acl`

## MITRE ATT&CK Mapping

| Technique | ID |
|-----------|----|
| Account Discovery | T1087 |
| Permission Groups Discovery | T1069 |
| Domain Trust Discovery | T1482 |

## External References

- [BloodHound CE Documentation](https://bloodhound.readthedocs.io/)
- [neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [BloodHound Cypher Cheatsheet](https://hausec.com/2019/09/09/bloodhound-cypher-cheatsheet/)

---

## Standards and Controls

## MITRE ATT&CK References

| Technique ID | Name | Tactic |
|-------------|------|--------|
| T1087.002 | Account Discovery: Domain Account | Discovery |
| T1069.002 | Permission Groups Discovery: Domain Groups | Discovery |
| T1482 | Domain Trust Discovery | Discovery |
| T1615 | Group Policy Discovery | Discovery |
| T1018 | Remote System Discovery | Discovery |
| T1033 | System Owner/User Discovery | Discovery |
| T1016 | System Network Configuration Discovery | Discovery |

## Official Resources

- BloodHound CE: https://github.com/SpecterOps/BloodHound
- SharpHound: https://github.com/BloodHoundAD/SharpHound
- BloodHound.py: https://github.com/dirkjanm/BloodHound.py
- BloodHound Query Library: https://queries.specterops.io/
- AzureHound: https://github.com/BloodHoundAD/AzureHound

## Key Research

- SpecterOps: An Ace in the Hole - Stealthy Data Collection with BloodHound
- Compass Security: BloodHound Community Edition Custom Queries (2025)
- SpecterOps: Introducing the BloodHound Query Library (2025)

---

## Workflows

## Complete Reconnaissance Workflow

```
1. Deployment
   ├── Pull BloodHound CE Docker images
   ├── Start services with docker compose up -d
   ├── Access web UI and set admin password
   └── Verify API connectivity

2. Data Collection
   ├── Choose collector: SharpHound v2 (Windows) or BloodHound.py (Linux)
   ├── Run All collection method for comprehensive data
   ├── Run Session collection in loop for user mapping
   ├── Collect from all reachable domains
   └── Exfiltrate ZIP data to analysis workstation

3. Import and Setup
   ├── Upload ZIP files via BloodHound CE web interface
   ├── Wait for data processing to complete
   ├── Mark owned/compromised principals
   └── Set high-value targets

4. Analysis
   ├── Run built-in attack path queries
   ├── Execute custom Cypher queries
   ├── Identify ACL abuse opportunities
   ├── Map delegation configurations
   ├── Find Kerberoastable / AS-REP roastable accounts
   └── Discover GPO modification paths

5. Attack Planning
   ├── Prioritize paths by hop count and stealth
   ├── Identify tools needed per hop
   ├── Plan OPSEC for each technique
   └── Document execution plan

6. Reporting
   ├── Export graph visualizations
   ├── Generate path summaries
   ├── Document all findings with evidence
   └── Provide remediation recommendations
```

## Stealthy Collection Workflow

```
Low-Noise Collection:
  1. DCOnly mode: Only queries domain controllers via LDAP
     SharpHound.exe -c DCOnly

  2. Targeted collection: Specific container/OU
     SharpHound.exe -c All --searchbase "OU=Servers,DC=domain,DC=local"

  3. Session loop: Passive session enumeration over time
     SharpHound.exe -c Session --loop --loopduration 04:00:00 --loopinterval 00:05:00
```

---

## Working Template

## Engagement Details

| Field | Value |
|-------|-------|
| Engagement Name | |
| Target Domain(s) | |
| Collection Date | |
| BloodHound CE Version | |
| SharpHound Version | |

## Collection Summary

| Metric | Count |
|--------|-------|
| Users | |
| Computers | |
| Groups | |
| GPOs | |
| OUs | |
| Domains | |
| Trusts | |
| Sessions | |

## Attack Paths Identified

| # | Path Description | Hops | Start Node | End Node | Risk |
|---|-----------------|------|------------|----------|------|
| 1 | | | | Domain Admins | |
| 2 | | | | Domain Admins | |

## High-Value Findings

| Finding | Count | Details |
|---------|-------|---------|
| Kerberoastable Users | | |
| AS-REP Roastable Users | | |
| Unconstrained Delegation | | |
| Users with DCSync Rights | | |
| Unsupported OS | | |

## Remediation Priority

| # | Finding | Remediation | Priority |
|---|---------|-------------|----------|
| 1 | | | Critical |
| 2 | | | High |
| 3 | | | Medium |
