# Success Criteria (How We Prove It Works)

## Minimum success (v1)
- The tool generates an IAM snapshot output (JSON/CSV) from the lab account.
- The tool flags the risky test users correctly:
  - test-no-mfa → Missing MFA finding
  - test-old-key → Access key present/rotation finding
  - test-admin → Admin permissions finding
- The dashboard displays a “fix-first” list sorted by severity/score.
- A findings export (CSV) is generated and matches the dashboard results.

## Stretch success (v2)
- Detect wildcard permissions (Action="*" or Resource="*").
- Detect overly broad role trust policies.
- Generate a formatted PDF report with summary + top findings + recommendations.
