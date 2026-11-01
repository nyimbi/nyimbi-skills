# Implementing Scim Provisioning With Okta

## API Reference

## Libraries Used

| Library | Purpose |
|---------|---------|
| `requests` | HTTP client for SCIM 2.0 and Okta Management API |
| `json` | Parse SCIM user and group payloads |
| `os` | Read `OKTA_DOMAIN`, `OKTA_API_TOKEN`, `SCIM_BASE_URL` |

## Installation

```bash
pip install requests
```

## Authentication

### Okta Management API
```python
import requests
import os

OKTA_DOMAIN = os.environ["OKTA_DOMAIN"]  # e.g., "dev-12345.okta.com"
OKTA_TOKEN = os.environ["OKTA_API_TOKEN"]
headers = {
    "Authorization": f"SSWS {OKTA_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
```

### SCIM 2.0 Endpoint (Bearer Token)
```python
SCIM_URL = os.environ["SCIM_BASE_URL"]  # e.g., "https://app.example.com/scim/v2"
scim_headers = {
    "Authorization": f"Bearer {os.environ['SCIM_TOKEN']}",
    "Content-Type": "application/scim+json",
}
```

## SCIM 2.0 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/scim/v2/Users` | List users with filtering |
| GET | `/scim/v2/Users/{id}` | Get a specific user |
| POST | `/scim/v2/Users` | Create a new user |
| PUT | `/scim/v2/Users/{id}` | Replace a user (full update) |
| PATCH | `/scim/v2/Users/{id}` | Partial user update (activate/deactivate) |
| DELETE | `/scim/v2/Users/{id}` | Delete a user |
| GET | `/scim/v2/Groups` | List groups |
| GET | `/scim/v2/Groups/{id}` | Get a specific group |
| POST | `/scim/v2/Groups` | Create a group |
| PATCH | `/scim/v2/Groups/{id}` | Update group membership |
| GET | `/scim/v2/ServiceProviderConfig` | SCIM service capabilities |
| GET | `/scim/v2/Schemas` | Supported SCIM schemas |
| GET | `/scim/v2/ResourceTypes` | Available resource types |

## Core Operations

### List SCIM Users with Filtering
```python
resp = requests.get(
    f"{SCIM_URL}/Users",
    headers=scim_headers,
    params={
        "filter": 'userName eq "alice@example.com"',
        "startIndex": 1,
        "count": 100,
    },
    timeout=30,
)
users = resp.json()
for user in users.get("Resources", []):
    print(f"{user['userName']} — active: {user.get('active', True)}")
```

### Create a User
```python
new_user = {
    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
    "userName": "bob@example.com",
    "name": {"givenName": "Bob", "familyName": "Smith"},
    "emails": [
        {"value": "bob@example.com", "type": "work", "primary": True}
    ],
    "active": True,
}
resp = requests.post(
    f"{SCIM_URL}/Users",
    headers=scim_headers,
    json=new_user,
    timeout=30,
)
created = resp.json()
user_id = created["id"]
```

### Deactivate a User (PATCH)
```python
deactivate_payload = {
    "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
    "Operations": [
        {"op": "Replace", "path": "active", "value": False}
    ],
}
resp = requests.patch(
    f"{SCIM_URL}/Users/{user_id}",
    headers=scim_headers,
    json=deactivate_payload,
    timeout=30,
)
```

### Manage Group Membership
```python
add_member = {
    "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
    "Operations": [
        {
            "op": "Add",
            "path": "members",
            "value": [{"value": user_id, "display": "bob@example.com"}],
        }
    ],
}
resp = requests.patch(
    f"{SCIM_URL}/Groups/{group_id}",
    headers=scim_headers,
    json=add_member,
    timeout=30,
)
```

## Okta Management API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/apps` | List applications |
| GET | `/api/v1/apps/{appId}/users` | List users assigned to an app |
| POST | `/api/v1/apps/{appId}/users` | Assign user to app |
| GET | `/api/v1/users` | List Okta users |
| POST | `/api/v1/users/{userId}/lifecycle/deactivate` | Deactivate user |

### List Okta Applications with SCIM Provisioning
```python
resp = requests.get(
    f"https://{OKTA_DOMAIN}/api/v1/apps",
    headers=headers,
    params={"filter": 'status eq "ACTIVE"', "limit": 50},
    timeout=30,
)
for app in resp.json():
    features = app.get("features", [])
    if "PUSH_NEW_USERS" in features or "PUSH_PROFILE_UPDATES" in features:
        print(f"SCIM-enabled: {app['label']} — features: {features}")
```

## Output Format

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
  "totalResults": 42,
  "startIndex": 1,
  "itemsPerPage": 100,
  "Resources": [
    {
      "id": "2819c223-7f76-453a-919d-ab1234567890",
      "userName": "alice@example.com",
      "name": {"givenName": "Alice", "familyName": "Johnson"},
      "active": true,
      "emails": [{"value": "alice@example.com", "type": "work", "primary": true}]
    }
  ]
}
```

---

## Standards and Controls

## Protocol Standards

### RFC 7644 - SCIM Protocol
- Defines the RESTful API for managing identity resources
- Specifies HTTP methods, headers, and response formats
- Mandates JSON as the data interchange format
- Requires TLS for all communications

### RFC 7643 - SCIM Core Schema
- Defines User, Group, and EnterpriseUser schemas
- Specifies attribute types: string, boolean, decimal, integer, dateTime, reference, complex, binary
- Defines mutability: readOnly, readWrite, immutable, writeOnly
- Specifies attribute uniqueness: none, server, global

### RFC 7642 - SCIM Definitions, Overview, Concepts, and Requirements
- Provides context for the SCIM specification
- Defines terminology and use cases
- Outlines design requirements for cross-domain provisioning

## Okta SCIM Requirements

### Mandatory Endpoints
| Endpoint | Methods | Purpose |
|----------|---------|---------|
| /Users | GET, POST | User listing and creation |
| /Users/{id} | GET, PUT, PATCH, DELETE | Individual user operations |
| /Groups | GET, POST | Group listing and creation |
| /Groups/{id} | GET, PATCH, DELETE | Individual group operations |

### Required Filter Support
- `userName eq "value"` - Exact match on userName
- `id eq "value"` - Exact match on user ID
- `displayName eq "value"` - Exact match for groups

### Pagination Requirements
- Support `startIndex` and `count` query parameters
- Return `totalResults` in ListResponse
- Default `startIndex` is 1 (1-based indexing)
- Maximum `count` should be configurable

## Compliance Standards

### SOC 2 Type II
- Automated provisioning demonstrates access control effectiveness
- Deprovisioning within defined SLA shows timely access removal
- Audit logs of SCIM operations provide evidence for access reviews

### ISO 27001 - A.9.2 User Access Management
- A.9.2.1: User registration and deregistration (automated via SCIM)
- A.9.2.2: User access provisioning (role-based assignment)
- A.9.2.5: Review of user access rights (SCIM audit logs)
- A.9.2.6: Removal of access rights (automated deprovisioning)

### NIST SP 800-53 - AC (Access Control)
- AC-2: Account Management (automated lifecycle)
- AC-2(1): Automated System Account Management
- AC-2(4): Automated Audit Actions
- AC-6: Least Privilege (role-based provisioning)

---

## Workflows

## User Provisioning Workflow

```
1. Admin assigns user to Okta application
       │
2. Okta checks if user exists (GET /Users?filter=userName eq "user@domain.com")
       │
       ├── User NOT found → Okta sends POST /Users with user attributes
       │       │
       │       └── SCIM server creates user → Returns 201 Created
       │
       └── User found → Okta sends PUT /Users/{id} to update attributes
               │
               └── SCIM server updates user → Returns 200 OK
```

## User Deprovisioning Workflow

```
1. Admin unassigns user from Okta application (or user deactivated in Okta)
       │
2. Okta sends PATCH /Users/{id}
       Body: {"schemas":["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
              "Operations":[{"op":"replace","value":{"active":false}}]}
       │
3. SCIM server deactivates user (sets active=false, revokes sessions)
       │
4. Returns 200 OK with updated user object
```

## Group Push Workflow

```
1. Admin enables Group Push for Okta group
       │
2. Okta sends POST /Groups with group name and initial members
       │
3. When group membership changes in Okta:
       │
       ├── Member added → PATCH /Groups/{id}
       │     Op: add, path: members, value: [{value: userId}]
       │
       └── Member removed → PATCH /Groups/{id}
             Op: remove, path: members[value eq "userId"]
```

## Profile Sync Workflow

```
1. User profile updated in Okta (e.g., department change)
       │
2. Okta sends PUT /Users/{id} or PATCH /Users/{id}
       Body includes updated attributes
       │
3. SCIM server updates user attributes in local database
       │
4. Returns 200 OK with full updated user representation
```

## Error Recovery Workflow

```
1. SCIM operation fails (network timeout, server error)
       │
2. Okta logs failed task in Provisioning > Tasks
       │
3. Admin can retry individual failed tasks
       │
4. For persistent failures:
       ├── Check SCIM server logs for error details
       ├── Verify network connectivity and TLS certificate
       ├── Validate bearer token has not expired
       └── Review attribute mapping for data format issues
```

## Implementation Testing Workflow

```
1. Deploy SCIM server to staging environment
       │
2. Configure Okta SCIM integration with staging URL
       │
3. Run Okta SCIM validator test suite
       │
4. Test manual operations:
       ├── Assign test user → verify account created
       ├── Update user profile → verify attributes synced
       ├── Unassign user → verify account deactivated
       └── Push group → verify group and members created
       │
5. Review provisioning logs in Okta Admin Console
       │
6. Promote to production with production SCIM URL
```

---

## Working Template

## Project: _______________
## Date: _______________
## Engineer: _______________

## Pre-Implementation

- [ ] Okta tenant provisioned with admin access
- [ ] Application API supports user CRUD operations
- [ ] TLS certificate configured for SCIM endpoint
- [ ] Database schema supports SCIM user attributes
- [ ] Bearer token generated and securely stored

## SCIM Server Configuration

| Setting | Value |
|---------|-------|
| Base URL | `https://______/scim/v2` |
| Auth Method | Bearer Token / OAuth 2.0 |
| SCIM Version | 2.0 |
| Unique ID Field | userName |

## Attribute Mapping

| Okta Attribute | SCIM Attribute | Required | Notes |
|---------------|----------------|----------|-------|
| login | userName | Yes | |
| firstName | name.givenName | Yes | |
| lastName | name.familyName | Yes | |
| email | emails[0].value | Yes | |
| department | enterprise:department | No | |
| title | title | No | |

## Endpoint Testing Results

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| /Users | POST | [ ] Pass | Create user |
| /Users | GET | [ ] Pass | List/filter users |
| /Users/{id} | GET | [ ] Pass | Get single user |
| /Users/{id} | PUT | [ ] Pass | Replace user |
| /Users/{id} | PATCH | [ ] Pass | Partial update |
| /Users/{id} | DELETE | [ ] Pass | Delete user |
| /Groups | POST | [ ] Pass | Create group |
| /Groups | GET | [ ] Pass | List groups |
| /Groups/{id} | PATCH | [ ] Pass | Update members |

## Okta Configuration

- [ ] SCIM app integration created
- [ ] Provisioning tab configured with base URL and token
- [ ] "To App" provisioning enabled (Create, Update, Deactivate)
- [ ] Attribute mappings verified
- [ ] Group Push configured (if needed)
- [ ] Test user assigned and provisioned successfully
- [ ] Test user unassigned and deprovisioned successfully

## Validation

- [ ] Okta SCIM validator test suite passed
- [ ] Error responses return correct SCIM error format
- [ ] Pagination works with startIndex and count parameters
- [ ] Filter on userName eq works correctly
- [ ] Deactivation sets active=false (soft delete)
- [ ] PATCH operations handle add/replace/remove

## Production Readiness

- [ ] SCIM endpoint uses production TLS certificate
- [ ] Bearer token rotated from development value
- [ ] Rate limiting configured on SCIM endpoints
- [ ] Monitoring and alerting set up for provisioning failures
- [ ] Provisioning error handling and retry logic tested
- [ ] Documentation updated with SCIM integration details
