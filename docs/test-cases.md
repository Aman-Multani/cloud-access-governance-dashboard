## Risky IAM Test Cases (Week 4)

1) test-no-mfa
- Setup: Console access enabled, MFA not assigned.
- Expected finding: Missing MFA should be flagged (high/medium risk).

2) test-old-key
- Setup: Access key created for the user.
- Expected finding: Access key present and key rotation/age should be flagged (medium risk).

3) test-admin
- Setup: AdministratorAccess attached to the user.
- Expected finding: Admin-level permissions should be flagged (high risk).

Evidence: Screenshots saved from IAM console for each case.
