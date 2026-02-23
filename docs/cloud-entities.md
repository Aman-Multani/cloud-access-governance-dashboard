# Cloud Entities in Scope (AWS IAM)

## IAM entities we will collect and assess
- IAM Users (human accounts)
- IAM Roles (assumable identities)
- IAM Policies (AWS managed + customer managed + inline)
- Access Keys (existence + age/rotation)
- MFA status (enabled/disabled for console users)
- Role Trust Policies (who can assume a role)

## What we will extract (high-level fields)
Users:
- user_name
- console_access (yes/no)
- mfa_enabled (yes/no)
- access_keys_count
- key_age_days (if available)
- attached_policies (names)

Roles:
- role_name
- attached_policies
- trust_policy_summary (restricted vs broad)

Policies:
- policy_name
- indicators: has_admin, has_wildcards
