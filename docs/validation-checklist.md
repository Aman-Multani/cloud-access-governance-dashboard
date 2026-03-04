# Validation Checklist

## Test Case 1: test-no-mfa
- Setup: console access enabled, MFA not assigned
- Expected finding: MissingMFA
- Evidence: screenshot of IAM user security credentials page

## Test Case 2: test-old-key
- Setup: access key created
- Expected finding: AccessKeyPresent
- Evidence: screenshot of access keys section

## Test Case 3: test-admin
- Setup: AdministratorAccess attached
- Expected finding: AdminPermissions
- Evidence: screenshot of permissions tab

## Pass/Fail Log (to fill later)
- test-no-mfa: Pass / Fail
- test-old-key: Pass / Fail
- test-admin: Pass / Fail

  ## Required Evidence

The following screenshots should be collected during validation:

- AWS Console: IAM Users list
- AWS Console: User security credentials (showing MFA status)
- AWS Console: Access key configuration
- AWS Console: IAM permissions / policies
- Dashboard results page (when implemented)

Exports to capture later:

- findings.csv
- findings.json (optional)

