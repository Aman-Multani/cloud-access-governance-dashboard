# Governance Model (IAM Risk + Least Privilege)

## Governance assumptions
- Small organization using AWS with multiple job roles.
- Access is granted based on role (least privilege), not “everyone is admin”.
- Human console access must be protected with MFA.
- Access keys are controlled and rotated to reduce long-lived credential risk.
- IAM roles must have restricted trust policies (no overly broad assume-role).

## Baselines (what “good” looks like)
1) MFA baseline
- Any IAM user with console access must have MFA enabled.

2) Access key baseline
- Access keys are minimized (only when needed).
- Keys must be rotated within 90 days.
- Unused keys should be disabled.

3) Least privilege baseline
- No AdministratorAccess for normal users.
- Avoid wildcard permissions (Action="*" and/or Resource="*").

4) Role trust baseline
- Trust policies allow only specific principals.
- Avoid broad trust and add conditions when possible.

## What we want to achieve (measurable goals)
- Collect IAM inventory data (users/roles/policies, MFA, access keys, trust policies).
- Detect baseline violations and assign a simple risk score (High/Medium/Low).
- Produce a fix-first prioritized list and export results (CSV/PDF).
- Validate using intentionally risky IAM test cases.
