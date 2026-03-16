# Output Schema (Snapshot + Findings)

## 1) IAM Snapshot (iam_snapshot.json)
Purpose: raw inventory collected from AWS IAM.

### Users (per user)
- principal_type: "User"
- principal_name
- console_access (true/false)
- mfa_enabled (true/false)
- access_keys_count (0/1/2)
- key_age_days (optional v2)
- has_admin (true/false)
- has_wildcard (true/false)
- attached_policies (list, optional v2)

### Roles (per role)
- principal_type: "Role"
- principal_name
- trust_is_broad (true/false)
- has_admin (true/false)
- has_wildcard (true/false)

## 2) Findings Export (findings.csv)
Purpose: scored fix-first list used by dashboard and exports.

Columns (exact order):
1) principal_type
2) principal_name
3) finding_type (MissingMFA, AccessKeyPresent, OldKey, AdminPermissions, WildcardPermissions, BroadTrust)
4) severity (High/Medium/Low)
5) points (integer)
6) recommendation (1 sentence)

Sorting rule:
- severity High → Medium → Low, then points descending
