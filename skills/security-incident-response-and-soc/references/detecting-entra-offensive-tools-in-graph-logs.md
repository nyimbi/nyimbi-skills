# Detecting Entra Offensive Tools In Graph Logs

## API Reference

## Tables

| Table | Covers | Key fields |
|-------|--------|------------|
| `MicrosoftGraphActivityLogs` | graph.microsoft.com requests | `RequestUri`, `RequestMethod`, `UserAgent`, `UserId`, `AppId`, `IPAddress`/`CallerIpAddress`, `ResponseStatusCode`, `SignInActivityId`, `TimeGenerated` |
| `AADGraphActivityLogs` | legacy graph.windows.net requests | `RequestUri`, `RequestMethod`, `UserAgent`, `UserId`, `AppId`, `CallerIpAddress`, `SignInActivityId`, `TimeGenerated` |

## Correlation keys

| Field | Joins to | Note |
|-------|----------|------|
| `SignInActivityId` | `SigninLogs.UniqueTokenIdentifier` | AADGraphActivityLogs value may carry `==` padding; trim before join |
| `SessionId` | SigninLogs / MicrosoftGraphActivityLogs / Unified Audit Log | Cross-source session correlation |
| `UserId` | `SigninLogs.UserId` | Account entity |
| `AppId` | `SigninLogs.AppId` | Calling application |

## Reusable KQL building blocks

```kusto
// Confirm ingestion
union withsource=Tbl MicrosoftGraphActivityLogs, AADGraphActivityLogs
| where TimeGenerated > ago(1d)
| summarize count() by Tbl

// aiohttp / python UA (ROADtools)
AADGraphActivityLogs
| where UserAgent contains "python" and UserAgent contains "aiohttp"

// Toolkit UA strings
union MicrosoftGraphActivityLogs, AADGraphActivityLogs
| where UserAgent has_any ("AADInternals","azurehound","BloodHound","Go-http-client")

// Extract top-level Graph resource from RequestUri
| extend TopLevelResource = tolower(tostring(split(split(RequestUri,"?")[0],"/")[3]))

// Trim SignInActivityId padding for correlation
| extend TokenId = trim_end("=", tostring(SignInActivityId))
```

## Enabling the diagnostic settings (Azure CLI)

```bash
az monitor diagnostic-settings create \
  --name entra-graph-logs \
  --resource "/providers/microsoft.aadiam/diagnosticSettings" \
  --logs '[{"category":"MicrosoftGraphActivityLogs","enabled":true},{"category":"AADGraphActivityLogs","enabled":true}]' \
  --workspace "<log-analytics-workspace-id>"
```

## Sentinel analytics rule (REST API) — outline

| Method | Endpoint | Purpose |
|--------|----------|---------|
| PUT | `/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.OperationalInsights/workspaces/{ws}/providers/Microsoft.SecurityInsights/alertRules/{ruleId}?api-version=2023-02-01` | Create/update a Scheduled analytics rule (body holds the KQL `query`, `queryFrequency`, `queryPeriod`, `tactics`, `techniques: ["T1078.004"]`, and `entityMappings`) |

---

## Standards and Controls

## NIST CSF 2.0

| ID | Name | Rationale |
|----|------|-----------|
| DE.CM-09 | Computing hardware and software, runtime environments, and their data are monitored to find potentially adverse events | Hunting the Graph activity tables continuously monitors directory API usage to find offensive-tool activity. |

## MITRE ATT&CK

| ID | Name | Rationale |
|----|------|-----------|
| T1078.004 | Valid Accounts: Cloud Accounts | Core technique: adversaries use valid cloud credentials/tokens to query the Graph APIs; these hunts detect that usage. |
| T1087.004 | Account Discovery: Cloud Account | The detected enumeration sweeps cloud accounts. |
| T1069.003 | Permission Groups Discovery: Cloud Groups | Sweeps enumerate cloud groups and roles. |
| T1526 | Cloud Service Discovery | Broad directory enumeration is cloud service discovery. |

## Supporting References

- AADGraphActivityLogs (Microsoft Learn) — https://learn.microsoft.com/entra/identity/monitoring-health/concept-aad-graph-activity-logs
- MicrosoftGraphActivityLogs overview — https://learn.microsoft.com/graph/microsoft-graph-activity-logs-overview
- Invictus-IR detection writeup — https://www.invictus-ir.com/news/the-missing-link-aadgraphactivitylogs-finally-arrives
- MITRE T1078.004 — https://attack.mitre.org/techniques/T1078/004/
