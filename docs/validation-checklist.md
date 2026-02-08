# Validation Checklist (Week 4)

## Test Case 1: test-no-mfa
- Setup: console access enabled, MFA not assigned
- Expected finding: Missing MFA flagged
- Evidence: screenshot of IAM user security credentials page

## Test Case 2: test-old-key
- Setup: access key created
- Expected finding: Access key present / rotation recommended
- Evidence: screenshot of access keys section

## Test Case 3: test-admin
- Setup: AdministratorAccess attached
- Expected finding: Admin permissions flagged as high risk
- Evidence: screenshot of permissions tab

## Pass/Fail Log (to fill later)
- test-no-mfa: Pass / Fail
- test-old-key: Pass / Fail
- test-admin: Pass / Fail
