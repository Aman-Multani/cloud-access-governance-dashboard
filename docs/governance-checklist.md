# Governance Checklist (Derived from Baselines)

## IAM User Controls
- [ ] MFA enabled for all console users (PASS if 100% compliant)
- [ ] No inactive/unused console users (flag for cleanup)
- [ ] No shared human accounts (note as policy)

## Access Key Controls
- [ ] Access keys only for users that need programmatic access
- [ ] Access keys rotated within 90 days
- [ ] Unused keys disabled/deleted
- [ ] Max 1 active key per user (recommended)

## Permission Controls (Least Privilege)
- [ ] No regular users with AdministratorAccess
- [ ] No wildcard permissions (Action="*" or Resource="*") for regular identities
- [ ] Policies scoped to specific services/resources where possible

## Role Trust Controls
- [ ] Role trust policies restricted to specific principals
- [ ] No broad trust (e.g., “*” or wide principals without conditions)
- [ ] Add conditions when possible (MFA/external ID)

## Reporting / Audit
- [ ] Findings include severity + score + recommendation
- [ ] Exportable report generated (CSV first, PDF later)
