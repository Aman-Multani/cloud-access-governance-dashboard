# Organization Role Model (Example)

## Roles in the organization
1) Cloud Admin (limited)
- Purpose: manage IAM and account settings.
- Allowed: manage IAM users/roles/policies with strict controls + MFA.
- Not allowed: daily use of AdministratorAccess unless break-glass.

2) DevOps
- Purpose: manage deployments and infrastructure.
- Allowed: role-based access for CI/CD, logging, and limited infra changes.
- Not allowed: wildcard admin permissions.

3) Developer
- Purpose: build and test apps.
- Allowed: scoped access to specific dev resources/services only.
- Not allowed: IAM management and admin privileges.

4) Auditor (read-only)
- Purpose: review configurations and findings.
- Allowed: read-only access to view IAM/security state.
- Not allowed: any write permissions.

## Break-glass (optional)
- One emergency admin identity with MFA, used only for incidents.
