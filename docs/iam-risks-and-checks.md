# IAM Risks, Checks, Scoring (Draft)

## Risks / Checks we will detect
1) Missing MFA (User)
- Condition: user has console access and no MFA device
- Fix: enable MFA for the user

2) Access key exists
- Condition: user has 1+ access keys
- Fix: rotate keys, disable unused keys

3) Old access key
- Condition: key age >= 90 days (threshold adjustable)
- Fix: rotate keys, set rotation policy

4) Admin permissions
- Condition: attached policy includes AdministratorAccess or equivalent
- Fix: replace with least-privilege permissions

5) Wildcard permissions
- Condition: policy uses Action="*" or Resource="*"
- Fix: scope actions/resources to required services only

6) Overly broad role trust
- Condition: trust policy allows broad principal (e.g., "*", or wide account principal without conditions)
- Fix: restrict principal and add conditions (MFA/external ID)

## Simple scoring (points)
| Finding | Points |
|---|---|
| Admin permissions | 5 |
| Wildcard permissions | 5 |
| Missing MFA | 3 |
| Old key (>=90 days) | 3 |
| Access key exists | 2 |
| Broad role trust | 3 |

Severity:
- High: 7+
- Medium: 4–6
- Low: 1–3

## Fix-first priority
1) Admin / Wildcard
2) Missing MFA
3) Broad trust
4) Old keys / access keys

## Mapping to findings output (for dashboard/export)
Each finding should include:
principal_name, principal_type, finding_type, severity, points, recommendation
