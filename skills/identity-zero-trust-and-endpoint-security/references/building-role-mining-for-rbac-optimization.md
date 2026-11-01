# Building Role Mining For RBAC Optimization

## API Reference

## Input Format (CSV)
```csv
user,entitlement,system
john.doe,read_files,FileServer
john.doe,write_files,FileServer
jane.smith,read_files,FileServer
```

## Role Mining Algorithms

### Bottom-Up Mining
Finds exact permission sets shared by >= N users.
- Input: user-permission matrix
- Output: candidate roles with exact permission sets
- Parameter: `min_users` (default: 2)

### Top-Down Mining (Jaccard Clustering)
Groups users by permission similarity.
```
Jaccard(A, B) = |A ∩ B| / |A ∪ B|
```
- Threshold >= 0.8: strict similarity
- Threshold >= 0.6: moderate clustering

## Optimization Metrics
| Metric | Description |
|--------|-------------|
| Total Assignments | Sum of all user-permission pairs |
| Candidate Roles | Discovered role count |
| Role Coverage | Users assigned to candidate roles |
| Avg Permissions/User | Assignment density |
| Outlier Count | Users with unique permissions |

## SailPoint IdentityNow Role Mining API
```
POST https://{tenant}.api.identitynow.com/beta/role-mining-sessions
Authorization: Bearer TOKEN
{
  "scope": {"included": {"identityIds": [...]}},
  "minEntitlementPopularity": 2,
  "pruneThreshold": 50
}
```

## SailPoint Role Mining Status
```
GET /beta/role-mining-sessions/{sessionId}
GET /beta/role-mining-sessions/{sessionId}/potential-roles
```

## CyberArk Identity Role Optimization
```
GET /Roles/GetRoleMembers?name={role}
POST /Roles/OptimizeRoles
{"minUsers": 3, "maxRoles": 50}
```

## NIST RBAC Model Levels
| Level | Description |
|-------|-------------|
| Core RBAC | Users, roles, permissions, sessions |
| Hierarchical | Role inheritance |
| Constrained | Separation of duty (SoD) |
| Symmetric | Permission-role review |

---

## Standards and Controls

## RBAC Standards

### ANSI/INCITS 359-2012 - Core RBAC
- Defines User, Role, Permission, Session abstractions
- Role assignment: users are assigned to roles
- Permission assignment: permissions are assigned to roles
- Role hierarchy: senior roles inherit junior role permissions
- Separation of Duty constraints (static and dynamic)

### NIST RBAC Model (SP 800-162)
- Core RBAC: Basic user-role and role-permission mappings
- Hierarchical RBAC: Role inheritance relationships
- Constrained RBAC: Static and dynamic separation of duties
- Symmetric RBAC: Combined user-centric and permission-centric views

## Identity Governance Standards

### ISO 27001:2022 - A.5.15 Access Control
- Access control policy based on business and security requirements
- Roles determined by job function
- Regular review of access rights
- Formal authorization for privilege changes

### NIST SP 800-53 Rev 5
- AC-2: Account Management
- AC-3: Access Enforcement
- AC-5: Separation of Duties
- AC-6: Least Privilege
- AC-16: Security and Privacy Attributes
- AC-24: Access Control Decisions

## Role Mining Research

### Key Algorithms
- **RoleMiner (Vaidya et al., 2007)**: Iterative role mining minimizing WSC
- **CompleteMiner / FastMiner (Vaidya et al., 2006)**: Complete vs. approximate algorithms
- **ORCA (Schlegelmilch & Steffens, 2005)**: Clustering-based approach
- **Graph Optimization (Lu et al., 2008)**: Graph-based role mining

### Quality Metrics
- Weighted Structural Complexity: min(|UA| + |PA| + |Roles|)
- Boolean Matrix Decomposition error
- Jaccard similarity between mined and original access
- Role coverage percentage

---

## Workflows

## End-to-End Role Mining Workflow

```
Phase 1: DATA COLLECTION (Week 1-2)
    ├── Export user-permission data from all identity sources
    │   ├── Active Directory group memberships
    │   ├── Cloud IAM role assignments
    │   ├── Application-level permissions
    │   └── Database access grants
    ├── Collect HR data (job titles, departments, cost centers)
    ├── Normalize data into User-Permission Assignment (UPA) matrix
    └── Clean data: remove disabled accounts, system accounts

Phase 2: ANALYSIS (Week 3-4)
    ├── Run clustering algorithms (hierarchical, k-means)
    ├── Run Formal Concept Analysis for exact role candidates
    ├── Compare results using WSC and coverage metrics
    ├── Identify optimal number of roles via silhouette analysis
    └── Map candidate roles to organizational structure

Phase 3: VALIDATION (Week 5-6)
    ├── Present candidate roles to business unit managers
    ├── Validate each role against job descriptions
    ├── Identify and resolve outlier permissions
    ├── Define role hierarchy (inheritance relationships)
    └── Agree on role names and descriptions

Phase 4: IMPLEMENTATION (Week 7-8)
    ├── Create roles in identity governance platform
    ├── Assign users to validated roles
    ├── Remove individual permission assignments
    ├── Test access for sample users in each role
    └── Document role definitions and approval chain

Phase 5: GOVERNANCE (Ongoing)
    ├── Monitor for permission drift
    ├── Quarterly role effectiveness review
    ├── Re-run mining annually to detect new patterns
    └── Track role count and WSC metrics over time
```

## Data Normalization Workflow

```
Raw Data Sources
    │
    ├── AD: user → group → permissions
    │       Normalize to: user_id, permission_id
    │
    ├── AWS: user/role → policy → actions
    │       Normalize to: user_id, permission_id
    │
    ├── Azure: user → role → permissions
    │       Normalize to: user_id, permission_id
    │
    └── Applications: user → app_role → features
            Normalize to: user_id, permission_id

Merge all sources → Deduplicate → Create UPA matrix
```

## Role Consolidation Workflow

```
Mining produces N candidate roles
    │
    ├── Remove roles with < 3 users (outliers)
    │
    ├── Merge roles with > 90% Jaccard similarity
    │
    ├── Identify hierarchical relationships:
    │   └── If Role A permissions ⊂ Role B permissions
    │       → Role A is junior to Role B
    │
    ├── Check for SoD violations:
    │   └── Does any role combine conflicting permissions?
    │       → Split into separate roles if needed
    │
    └── Final role set with hierarchy and constraints
```

---

## Working Template

## Project Overview

| Field | Value |
|-------|-------|
| Organization | |
| Project Lead | |
| Start Date | |
| Target Completion | |
| Identity Sources | AD / Azure / AWS / Applications |

## Data Collection Summary

| Source | Users | Permissions | Assignments |
|--------|-------|-------------|-------------|
| Active Directory | | | |
| AWS IAM | | | |
| Azure AD | | | |
| Applications | | | |
| **Total (Deduplicated)** | | | |

## Mining Results

| Algorithm | Roles Found | Coverage | Deviation | WSC |
|-----------|-------------|----------|-----------|-----|
| Clustering (k=___) | | | | |
| Intersection Mining | | | | |
| Selected Approach | | | | |

## Proposed Role Definitions

| Role Name | Department | Permissions | Users | Status |
|-----------|------------|-------------|-------|--------|
| | | | | Draft/Validated/Approved |
| | | | | |

## Stakeholder Validation

| Business Unit | Reviewer | Roles Reviewed | Approved | Date |
|--------------|----------|---------------|----------|------|
| | | | Yes/No | |

## Migration Plan

- [ ] Roles created in identity governance platform
- [ ] User-role assignments configured
- [ ] Individual permission grants removed
- [ ] Test users validated access
- [ ] Full migration completed
- [ ] Post-migration access verification
- [ ] Old permissions cleanup confirmed
