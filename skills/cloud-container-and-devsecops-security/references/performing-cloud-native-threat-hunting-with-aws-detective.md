# Performing Cloud Native Threat Hunting With AWS Detective

## API Reference

This reference covers the Amazon Detective API for cloud-native threat hunting, via the AWS SDK for Python (`boto3`) and the AWS CLI. Detective ingests CloudTrail, VPC Flow Logs, GuardDuty findings, and EKS audit logs into a **behavior graph** and exposes entity profiles, finding groups, and guided investigations.

## Authentication

Detective uses standard AWS IAM authentication — no separate API key. Credentials resolve through the SDK credential provider chain (environment variables, `~/.aws/credentials` profile, EC2/ECS/EKS/Lambda role, or SSO).

```python
import boto3

detective = boto3.client("detective", region_name="us-east-1")
```

Required IAM permissions (managed policy `AmazonDetectiveFullAccess`, or least-privilege custom):

| Action | Purpose |
|---|---|
| `detective:ListGraphs` | Discover behavior graphs |
| `detective:ListInvestigations` | List guided investigations |
| `detective:GetInvestigation` | Get an investigation's results |
| `detective:ListIndicators` | List indicators for an investigation |
| `detective:StartInvestigation` | Launch a new investigation on an entity |
| `detective:ListMembers` / `detective:GetMembers` | Multi-account graph membership |
| `guardduty:ListFindings`, `guardduty:GetFindings` | Correlate GuardDuty findings |

**Prerequisite:** Amazon GuardDuty must be enabled and active for at least 48 hours before Detective can build a usable behavior graph.

## Key Methods (boto3 `detective` client)

| Method | Description | Key Parameters |
|---|---|---|
| `list_graphs` | List behavior graphs the account administers. | `MaxResults`, `NextToken` |
| `start_investigation` | Run an automated investigation on an entity over a scope window. | `GraphArn` (required), `EntityArn` (required), `ScopeStartTime`, `ScopeEndTime` |
| `get_investigation` | Retrieve an investigation's results (severity, status, scope, entity). | `GraphArn` (required), `InvestigationId` (required) |
| `list_investigations` | List investigations, filterable/sortable. | `GraphArn` (required), `FilterCriteria`, `SortCriteria`, `MaxResults`, `NextToken` |
| `list_indicators` | List indicators (TTPs, anomalies) tied to an investigation. | `GraphArn` (required), `InvestigationId` (required), `IndicatorType`, `MaxResults`, `NextToken` |
| `list_members` / `get_members` | Member accounts in the behavior graph. | `GraphArn`, `AccountIds` |
| `create_members` / `delete_members` | Invite/remove member accounts. | `GraphArn`, `Accounts` |
| `list_datasource_packages` | Optional data sources enabled (EKS audit, etc.). | `GraphArn` |
| `update_investigation_state` | Mark an investigation `ARCHIVED` / `ACTIVE`. | `GraphArn`, `InvestigationId`, `State` |

### `list_indicators` — verified parameters

`GraphArn` (string, required), `InvestigationId` (string, required), `IndicatorType` (string, optional filter), `NextToken` (string — pagination token; **expires after 24 hours**), `MaxResults` (integer). Valid `IndicatorType` values:

`TTP_OBSERVED` · `IMPOSSIBLE_TRAVEL` · `FLAGGED_IP_ADDRESS` · `NEW_GEOLOCATION` · `NEW_ASO` (new autonomous system org) · `NEW_USER_AGENT` · `RELATED_FINDING` · `RELATED_FINDING_GROUP`

### `get_investigation` — verified

Request: `GraphArn` (the behavior graph ARN), `InvestigationId`. Response includes `CreatedTime` (UTC ISO8601, e.g. `2021-08-18T16:35:56.284Z`), `EntityArn`, `EntityType`, `GraphArn`, `InvestigationId`, `ScopeStartTime`, `ScopeEndTime`, plus severity/status/state.

### `list_investigations` filter / sort detail

```python
FilterCriteria = {
    "Severity":     {"Value": "CRITICAL"},   # INFORMATIONAL|LOW|MEDIUM|HIGH|CRITICAL
    "Status":       {"Value": "RUNNING"},     # RUNNING|FAILED|SUCCESSFUL
    "State":        {"Value": "ACTIVE"},      # ACTIVE|ARCHIVED
    "EntityArn":    {"Value": "arn:aws:iam::123456789012:user/suspicious"},
    "CreatedTime":  {"StartInclusive": <datetime>, "EndInclusive": <datetime>},
}
SortCriteria = {"Field": "SEVERITY", "SortOrder": "DESC"}  # CREATED_TIME|SEVERITY|STATUS
```

## Python SDK

```python
# Installation
pip install boto3

import boto3

detective = boto3.client("detective", region_name="us-east-1")

def hunt_critical(graph_arn):
    """List critical, currently-running investigations and their indicators."""
    inv = detective.list_investigations(
        GraphArn=graph_arn,
        FilterCriteria={
            "Severity": {"Value": "CRITICAL"},
            "Status":   {"Value": "RUNNING"},
        },
        SortCriteria={"Field": "SEVERITY", "SortOrder": "DESC"},
        MaxResults=20,
    )
    for d in inv.get("InvestigationDetails", []):
        print(d["InvestigationId"], d["EntityArn"], d["Severity"])
        ind = detective.list_indicators(
            GraphArn=graph_arn,
            InvestigationId=d["InvestigationId"],
            MaxResults=50,
        )
        for i in ind.get("Indicators", []):
            print("  ", i["IndicatorType"], i.get("IndicatorDetail"))

# Launch a fresh investigation on a suspect IAM principal
def investigate_entity(graph_arn, entity_arn, start, end):
    resp = detective.start_investigation(
        GraphArn=graph_arn,
        EntityArn=entity_arn,
        ScopeStartTime=start,   # datetime
        ScopeEndTime=end,       # datetime
    )
    return resp["InvestigationId"]

for g in detective.list_graphs().get("GraphList", []):
    hunt_critical(g["Arn"])
```

CLI equivalents:

```bash
aws detective list-graphs --output table

aws detective list-investigations \
  --graph-arn arn:aws:detective:us-east-1:123456789012:graph:abc \
  --filter-criteria '{"Severity":{"Value":"HIGH"}}' \
  --max-results 10

aws detective list-indicators \
  --graph-arn arn:aws:detective:us-east-1:123456789012:graph:abc \
  --investigation-id 000000000000000000001 --max-results 50
```

## Common Response Fields

`list_investigations` → `InvestigationDetails[]`:

| Field | Meaning |
|---|---|
| `InvestigationId` | Unique investigation ID |
| `Severity` | `INFORMATIONAL` \| `LOW` \| `MEDIUM` \| `HIGH` \| `CRITICAL` |
| `Status` | `RUNNING` \| `FAILED` \| `SUCCESSFUL` |
| `State` | `ACTIVE` \| `ARCHIVED` |
| `EntityArn` | The entity under investigation |
| `EntityType` | `IAM_USER` \| `IAM_ROLE` (etc.) |
| `CreatedTime` | Investigation creation timestamp (UTC ISO8601) |

`list_indicators` → `Indicators[]`: each has `IndicatorType` plus an `IndicatorDetail` union populated for the matching type (e.g. `FlaggedIpAddressDetail`, `ImpossibleTravelDetail`, `NewGeolocationDetail`, `TTPsObservedDetail` carrying MITRE ATT&CK tactic/technique).

## Rate Limits / Service Quotas

Detective enforces account-level, per-Region quotas (most adjustable via Service Quotas):

| Quota | Default |
|---|---|
| Member accounts per behavior graph | 1,200 |
| Behavior graphs (administrator) per Region | 1 |
| Data retention in behavior graph | 1 year of rolling history |
| Investigation scope window | up to 1 year |
| Pagination token (`list_indicators` `NextToken`) lifetime | 24 hours |
| API request rate | Throttled per standard AWS API limits |

Throttling returns `TooManyRequestsException`; boto3 retries with exponential backoff. There is no per-request monetary charge for the API itself — Detective is billed by **volume of log data ingested** into the behavior graph (GB/month, tiered).

## Error Codes

| Error | Meaning |
|---|---|
| `AccessDeniedException` | Caller lacks the required `detective:*` permission |
| `ValidationException` | Invalid parameter (bad ARN, malformed filter) |
| `ResourceNotFoundException` | Graph, investigation, or entity not found |
| `TooManyRequestsException` | API rate quota exceeded; back off and retry |
| `ConflictException` | Concurrent modification of graph membership |
| `InternalServerException` | Transient service-side error; retry |
| `ServiceQuotaExceededException` | Member/graph quota exceeded |

## Resources

- Detective API Reference: https://docs.aws.amazon.com/detective/latest/APIReference/Welcome.html
- `ListInvestigations`: https://docs.aws.amazon.com/detective/latest/APIReference/API_ListInvestigations.html
- `GetInvestigation`: https://docs.aws.amazon.com/detective/latest/APIReference/API_GetInvestigation.html
- `StartInvestigation`: https://docs.aws.amazon.com/detective/latest/APIReference/API_StartInvestigation.html
- boto3 `list_indicators`: https://docs.aws.amazon.com/boto3/latest/reference/services/detective/client/list_indicators.html
- boto3 Detective client: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html
- Detective + GuardDuty integration: https://docs.aws.amazon.com/detective/latest/userguide/detective-integration-guardduty.html

---

## Standards and Controls

## MITRE ATT&CK Cloud Matrix
- **TA0001** Initial Access: T1078 (Valid Accounts), T1190 (Exploit Public-Facing Application)
- **TA0003** Persistence: T1098 (Account Manipulation), T1136 (Create Account)
- **TA0004** Privilege Escalation: T1078, T1484 (Domain Policy Modification)
- **TA0005** Defense Evasion: T1562 (Impair Defenses), T1070 (Indicator Removal)
- **TA0006** Credential Access: T1528 (Steal Application Access Token)
- **TA0007** Discovery: T1580 (Cloud Infrastructure Discovery), T1526 (Cloud Service Discovery)
- **TA0009** Collection: T1530 (Data from Cloud Storage)
- **TA0010** Exfiltration: T1537 (Transfer Data to Cloud Account)

## AWS Documentation
- [AWS Detective User Guide](https://docs.aws.amazon.com/detective/latest/userguide/)
- [AWS Detective API Reference](https://docs.aws.amazon.com/detective/latest/APIReference/)
- [GuardDuty Finding Types](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-active.html)

## CIS AWS Foundations Benchmark
- Section 4: Monitoring (relevant to Detective integration)

---

## Workflows

## Phase 1: Triage
1. Review GuardDuty HIGH/CRITICAL findings
2. Open Detective console → Finding Groups
3. Identify clustered findings pointing to same entity

## Phase 2: Entity Investigation
1. Select entity (IAM user/role, EC2, IP)
2. Review 24h behavior timeline
3. Identify unusual API calls, new geolocations, impossible travel
4. Check for privilege escalation patterns (CreateAccessKey, AttachPolicy)

## Phase 3: Scope Assessment
1. Trace lateral movement via AssumeRole chains
2. Check S3 data access patterns
3. Review VPC Flow Logs for unusual outbound connections
4. Identify all compromised credentials

## Phase 4: Correlation
1. Map findings to MITRE ATT&CK techniques
2. Build attack timeline from entity profiles
3. Identify initial access vector
4. Document indicators of compromise (IOCs)

## Phase 5: Response
1. Preserve evidence (CloudTrail logs, flow logs, snapshots) when safe
2. Disable compromised credentials
3. Revoke active sessions
4. Isolate affected resources
5. If active impact is ongoing, contain first and document evidence trade-offs

---

## Working Template

## Pre-Investigation
- [ ] Confirm Detective is enabled and receiving data
- [ ] Identify trigger (GuardDuty finding, alert, manual hunt)
- [ ] Define scope time window
- [ ] Document initial IOCs

## Entity Investigation
- [ ] IAM User/Role profile reviewed
- [ ] API call timeline analyzed
- [ ] Geographic anomalies checked (impossible travel)
- [ ] New API calls identified (never seen before)
- [ ] Privilege escalation attempts documented
- [ ] AssumeRole chain traced

## Network Analysis
- [ ] VPC Flow Logs reviewed for entity
- [ ] Outbound connections to suspicious IPs identified
- [ ] Data transfer volumes assessed
- [ ] DNS query patterns checked

## Finding Correlation
- [ ] All related GuardDuty findings grouped
- [ ] MITRE ATT&CK techniques mapped
- [ ] Attack timeline constructed
- [ ] Initial access vector identified

## Response Actions
- [ ] Evidence preserved (or capture rationale if immediate containment required)
- [ ] Compromised credentials disabled
- [ ] Active sessions revoked
- [ ] Affected resources isolated
- [ ] Stakeholders notified
