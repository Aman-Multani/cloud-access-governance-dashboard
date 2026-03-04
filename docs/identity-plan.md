# Identity Plan (Baseline vs Risky for Validation)

## Baseline (good) identities
- amandeep-admin: MFA enabled (compliant admin account)
- future: devops-role, developer-role, auditor-role (least privilege)

## Risky identities (bad examples for testing)
- test-no-mfa: console access without MFA
- test-old-key: access key exists (used for rotation/age checks)
- test-admin: admin permissions attached

## Validation method
Run collector + checks and confirm:
- risky identities trigger findings
- baseline identities show compliant state
