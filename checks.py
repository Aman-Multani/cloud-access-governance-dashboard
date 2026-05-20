import json
import csv

# Load the snapshot
with open("iam_snapshot.json") as f:
    snapshot = json.load(f)

findings = []

print("Running checks...\n")

for user in snapshot["users"]:
    username = user["UserName"]

    # CHECK 1: Missing MFA
    if not user["HasMFA"]:
        findings.append({
            "UserName": username,
            "Check": "MissingMFA",
            "Severity": "CRITICAL",
            "Points": 10,
            "Detail": "User has no MFA device attached",
            "Recommendation": "Enable MFA immediately for this user"
        })
        print(f"  [CRITICAL] {username} → MissingMFA")

    # CHECK 2: Admin Permissions
    for policy in user["AttachedPolicies"]:
        if policy == "AdministratorAccess":
            findings.append({
                "UserName": username,
                "Check": "AdminPermissions",
                "Severity": "HIGH",
                "Points": 8,
                "Detail": "User has AdministratorAccess policy attached",
                "Recommendation": "Replace with a least-privilege policy scoped to job role"
            })
            print(f"  [HIGH]     {username} → AdminPermissions")

    # CHECK 3: Access Key Present / Old Key
    for key in user["AccessKeys"]:
        if key["Status"] == "Active":
            severity = "HIGH"   if key["AgeDays"] > 90 else "MEDIUM"
            points   = 8        if key["AgeDays"] > 90 else 5
            detail   = f"Active access key — age: {key['AgeDays']} days"
            rec      = "Rotate or disable this key" if key["AgeDays"] > 90 else "Monitor key age; rotate before 90 days"
            findings.append({
                "UserName": username,
                "Check": "AccessKeyPresent" if key["AgeDays"] <= 90 else "OldAccessKey",
                "Severity": severity,
                "Points": points,
                "Detail": detail,
                "Recommendation": rec
            })
            print(f"  [{severity}]{'    ' if severity == 'MEDIUM' else '     '}{username} → AccessKey ({key['AgeDays']} days old)")

    # CHECK 4: Wildcard Permissions
    # Flags any inline or managed policy where Action or Resource is set to "*"
    inline_policies = user.get("InlinePolicies", {})
    for policy_name, policy_doc in inline_policies.items():
        statements = policy_doc.get("Statement", [])
        # Statement can be a list or a single dict — normalize to list
        if isinstance(statements, dict):
            statements = [statements]
        for statement in statements:
            action   = statement.get("Action", [])
            resource = statement.get("Resource", [])
            # Normalize to lists
            if isinstance(action, str):
                action = [action]
            if isinstance(resource, str):
                resource = [resource]
            if "*" in action or "*" in resource:
                findings.append({
                    "UserName": username,
                    "Check": "WildcardPermissions",
                    "Severity": "HIGH",
                    "Points": 8,
                    "Detail": f"Inline policy '{policy_name}' contains wildcard Action or Resource (*)",
                    "Recommendation": "Replace wildcard statements with specific actions and resources scoped to job role"
                })
                print(f"  [HIGH]     {username} → WildcardPermissions (policy: {policy_name})")
                break  # one finding per policy is enough


# ── Role-level checks ────────────────────────────────────────────────────────
# CHECK 5: Risk Trust Policy
# Flags any IAM role whose trust policy allows Principal: * (anyone can assume it)
for role in snapshot.get("roles", []):
    role_name = role.get("RoleName", "unknown")
    trust_doc = role.get("TrustPolicyDocument", {})
    statements = trust_doc.get("Statement", [])
    if isinstance(statements, dict):
        statements = [statements]
    for statement in statements:
        principal = statement.get("Principal", {})
        # Principal can be "*" (string) or {"AWS": "*"} or {"Service": ...}
        is_wildcard = False
        if principal == "*":
            is_wildcard = True
        elif isinstance(principal, dict):
            aws_principal = principal.get("AWS", "")
            if aws_principal == "*" or (isinstance(aws_principal, list) and "*" in aws_principal):
                is_wildcard = True
        if is_wildcard:
            findings.append({
                "UserName": f"[ROLE] {role_name}",
                "Check": "RiskTrustPolicy",
                "Severity": "HIGH",
                "Points": 8,
                "Detail": f"Role '{role_name}' trust policy allows Principal: * — any AWS entity can assume this role",
                "Recommendation": "Restrict the trust policy Principal to specific trusted AWS accounts or services"
            })
            print(f"  [HIGH]     {role_name} → RiskTrustPolicy (wildcard principal in trust policy)")
            break  # one finding per role


# ── Sort & save ──────────────────────────────────────────────────────────────
# Sort by points descending (fix-first order)
findings.sort(key=lambda x: x["Points"], reverse=True)

# Save to CSV
with open("findings.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["UserName","Check","Severity","Points","Detail","Recommendation"])
    writer.writeheader()
    writer.writerows(findings)

# Save to JSON
with open("findings.json", "w") as f:
    json.dump(findings, f, indent=2)

# Print summary
print(f"\n{'='*50}")
print(f"  FINDINGS SUMMARY")
print(f"{'='*50}")
print(f"  Total findings : {len(findings)}")
critical = [f for f in findings if f['Severity'] == 'CRITICAL']
high     = [f for f in findings if f['Severity'] == 'HIGH']
medium   = [f for f in findings if f['Severity'] == 'MEDIUM']
print(f"  CRITICAL       : {len(critical)}")
print(f"  HIGH           : {len(high)}")
print(f"  MEDIUM         : {len(medium)}")
print(f"{'='*50}")
print(f"\nSaved to findings.csv and findings.json")
print(f"\nFIX-FIRST LIST:")
for i, f in enumerate(findings, 1):
    print(f"  {i}. [{f['Severity']}] {f['UserName']} — {f['Check']}")
