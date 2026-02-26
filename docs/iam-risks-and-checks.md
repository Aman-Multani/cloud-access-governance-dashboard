# IAM Risks, Checks, and Scoring (v1)

Goal:
Define the IAM risks we detect, what triggers them, how they are scored, and how they should be fixed.


## Risks / Checks We Detect

### 1. Missing MFA (User)

Condition:
- User has console access
- MFA is not enabled

Fix:
Enable MFA for the user.

Points: 3


### 2. Access Key Exists

Condition:
- User has one or more access keys

Fix:
Rotate keys and disable unused keys. Prefer short-term credentials where possible.

Points: 2


### 3. Old Access Key

Condition:
- Access key age is 90 days or more  
- (Threshold is configurable)

Fix:
Rotate or delete old keys and enforce key rotation policy.

Points: 3


### 4. Admin Permissions

Condition:
- Attached policy includes AdministratorAccess  
- Or equivalent full administrative access

Fix:
Replace with least-privilege permissions. Limit admin access to break-glass users only.

Points: 5



### 5. Wildcard Permissions

Condition:
- Policy contains "*" in Action or Resource  
- Or overly broad service permissions

Fix:
Scope permissions to specific actions and resources required.

Points: 5



### 6. Overly Broad Role Trust

Condition:
- Role trust policy allows broad principal (for example "*")  
- Or wide account principal without restrictive conditions

Fix:
Restrict trusted principals and add conditions such as MFA or external ID.

Points: 3


## Scoring Model

Total risk score is calculated by adding all finding points for a principal.

Severity Levels:

- High: 7 or more points
- Medium: 4 to 6 points
- Low: 1 to 3 points


## Fix-First Priority Order

1. Admin Permissions  
2. Wildcard Permissions  
3. Missing MFA  
4. Broad Role Trust  
5. Old Access Keys  
6. Access Key Exists  

Why this order?

Admin and wildcard permissions create the largest blast radius and highest impact if misused.  
Missing MFA increases account takeover risk.  
Broad trust allows unintended role assumption.  
Old and existing keys are important but lower immediate impact.


## Mapping to Findings Output (Dashboard / Export)

Each finding must include the following fields:

- principal_name  
- principal_type (user or role)  
- finding_type  
- severity  
- points  
- recommendation  
- condition_summary (why the check triggered)  
- detected_at (timestamp)

Next Step:
Confirm final key age threshold (default 90 days) and ensure finding_type names match the CSV export exactly.
