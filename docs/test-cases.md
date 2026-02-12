
## Evidence screenshots (Week 4)
- Users list showing all created users
- amandeep-admin showing MFA enabled
- test-no-mfa showing enabled without MFA
- test-old-key showing access key exists
- test-admin showing AdministratorAccess attached

## Risky IAM Test Cases (Week 4)

### 1) test-no-mfa
- Setup: Console access enabled, MFA not assigned.
- Expected finding: Missing MFA should be flagged (High/Medium).

### 2) test-old-key
- Setup: Access key created.
- Expected finding: Access key present / key rotation recommended (Medium).

### 3) test-admin
- Setup: AdministratorAccess attached.
- Expected finding: Admin permissions flagged (High).

## Evidence screenshots saved
- Users list showing created users
- amandeep-admin showing MFA enabled
- test-no-mfa showing enabled without MFA
- test-old-key showing access key exists
- test-admin showing AdministratorAccess attached
