import boto3
import json
from datetime import datetime, timezone

print("Connecting to AWS IAM...")
iam = boto3.client("iam")

snapshot = {"users": [], "roles": []}

# ── Users ────────────────────────────────────────────────────────────────────
users = iam.list_users()["Users"]
print(f"Found {len(users)} users. Collecting data...")

for user in users:
    username = user["UserName"]
    print(f"  → {username}")

    # MFA devices
    mfa = iam.list_mfa_devices(UserName=username)["MFADevices"]
    has_mfa = len(mfa) > 0

    # Access keys
    keys = iam.list_access_keys(UserName=username)["AccessKeyMetadata"]
    key_list = []
    for k in keys:
        created = k["CreateDate"].replace(tzinfo=timezone.utc)
        age_days = (datetime.now(timezone.utc) - created).days
        key_list.append({
            "KeyId": k["AccessKeyId"],
            "Status": k["Status"],
            "AgeDays": age_days
        })

    # Attached managed policies
    attached = iam.list_attached_user_policies(UserName=username)["AttachedPolicies"]
    policy_names = [p["PolicyName"] for p in attached]

    # Inline policies (needed for WildcardPermissions check)
    inline_names = iam.list_user_policies(UserName=username)["PolicyNames"]
    inline_policies = {}
    for policy_name in inline_names:
        doc = iam.get_user_policy(UserName=username, PolicyName=policy_name)
        # Policy document comes URL-encoded — boto3 auto-decodes it for us
        inline_policies[policy_name] = doc["PolicyDocument"]

    snapshot["users"].append({
        "UserName": username,
        "HasMFA": has_mfa,
        "AccessKeys": key_list,
        "AttachedPolicies": policy_names,
        "InlinePolicies": inline_policies
    })

# ── Roles (needed for RiskTrustPolicy check) ─────────────────────────────────
print("\nCollecting IAM roles...")
paginator = iam.get_paginator("list_roles")
role_count = 0

for page in paginator.paginate():
    for role in page["Roles"]:
        role_name = role["RoleName"]

        # Skip AWS service-linked roles — they are managed by AWS and not relevant
        if role_name.startswith("AWSServiceRole") or \
           role.get("Path", "").startswith("/aws-service-role/"):
            continue

        trust_doc = role.get("AssumeRolePolicyDocument", {})

        snapshot["roles"].append({
            "RoleName": role_name,
            "TrustPolicyDocument": trust_doc
        })
        role_count += 1

print(f"  → {role_count} non-service roles collected")

# ── Save ──────────────────────────────────────────────────────────────────────
with open("iam_snapshot.json", "w") as f:
    json.dump(snapshot, f, indent=2)

print("\nDone! Saved to iam_snapshot.json")
