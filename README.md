# Cloud Access Governance Dashboard (AWS IAM Risk + Least Privilege)

## Goal
Build a beginner-friendly IAM governance tool that:
1) Collects AWS IAM data (users/roles/policies, MFA, access keys, trust policies)
2) Runs basic security checks + simple risk scoring
3) Shows a dashboard with a fix-first list and exports (CSV/PDF)

## Team
- Amandeep (Team Lead) - AWS lab + collector + integration
- Yashdeep - data formatting + export support
- Gurpreet - checks/risk scoring + recommendations
- Amna Rafiq - reporting + testing evidence + dashboard content layout



## Week 4 Focus
- Define data fields + collector output format
- Create risky IAM test cases
- Draft checks + scoring rules
- Prepare report template + validation checklist

# Week 5 Focus 
- Collector output v1 (even if sample)
- data/samples/iam_snapshot_sample.json
- a short note in collector/README.md explaining what fields you will collect
- Checks + scoring v1
- docs/iam-risks-and-checks.md (Gurpreet)
- optional: checks/checks_v1.md (just bullets of rule logic)
- Findings output format
- data/samples/findings_sample.csv (you already did)
- docs/output-schema.md (Yashdeep) listing the columns/fields

Dashboard “v1” evidence
If using Streamlit/anything: a simple table page
If not coding yet: dashboard/README.md with a table mock + screenshot/wireframe
Weekly report artifacts
docs/week5-summary.md (bullets: planned vs done, blockers, next steps)
docs/validation-checklist.md updated with Pass/Fail placeholders
