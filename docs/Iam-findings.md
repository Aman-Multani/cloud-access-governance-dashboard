IAM Findings Report (v1)

Snapshot Date: 2026-02-23
Source: AWS IAM Lab Account

Method

The IAM governance checks defined in iam-risks-and-checks.md were applied to the snapshot data. Each triggered finding was scored using the defined points model:
	•	AdminPermissions → 5 points
	•	WildcardPermissions → 5 points
	•	MissingMFA → 3 points
	•	BroadTrust → 3 points
	•	OldKey (>=90 days) → 3 points
	•	AccessKeyPresent → 2 points

Severity classification:
	•	High: 7+
	•	Medium: 4–6
	•	Low: 1–3

⸻

Findings Table
principal_type
principal_name
finding_type
severity
points
recommendation
User
amandeep-admin
AdminPermissions
Medium
5
Remove admin policy and replace with least-privilege permissions.
User
test-no-mfa
MissingMFA
Low
3
Enable MFA for the user.
User
test-old-key
AccessKeyPresent
Low
2
Rotate keys and disable unused keys.
User
test-admin
AdminPermissions
High
5
Remove admin policy and replace with least-privilege permissions.
User
test-admin
MissingMFA


⸻

Risk Summary (Per Principal)
Principal
Risk Score
Severity
amandeep-admin
5
Medium
test-no-mfa
3
Low
test-old-key
2
Low
test-admin
8
High

Fix-First Priority Order (Applied)
	1.	test-admin (High – 8 points)
	2.	amandeep-admin (Medium – 5 points)
	3.	test-no-mfa (Low – 3 points)
	4.	test-old-key (Low – 2 points)

⸻

Notes
	•	No wildcard permissions were detected.
	•	No roles were present in this snapshot.
	•	Key age data was not available; therefore, OldKey checks were not triggered.
	•	Finding type names aligned with team schema.


