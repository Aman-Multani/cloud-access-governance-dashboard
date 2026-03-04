# System Flow (How the Solution Works)

1) Collect (IAM Inventory)
- Input: AWS IAM (users, roles, policies, MFA, access keys, trust policies)
- Output: iam_snapshot.json (raw inventory)

2) Analyze (Checks + Scoring)
- Input: iam_snapshot.json
- Process: run governance checklist checks and compute risk score/severity
- Output: findings.csv (fix-first list)

3) Display (Dashboard)
- Input: findings.csv (and optional snapshot)
- Display: summary counts + fix-first table + filters

4) Export (Audit Report)
- Output: downloadable findings CSV (PDF later as stretch)

5) Validate (Proof)
- Run tool against risky test identities:
  - test-no-mfa, test-old-key, test-admin
- Confirm findings match expected results (pass/fail checklist)
