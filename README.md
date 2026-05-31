# Cloud Access Governance Dashboard
### Group 12 — INFO49402 | Sheridan College

An automated AWS IAM governance auditing pipeline with a React dashboard and PDF report generator. The pipeline collects IAM data from AWS, runs governance checks, scores findings by severity, and presents results in a browser-based dashboard and a downloadable PDF audit report.

---

## Team

| Name | Role |
|---|---|
| Amandeep Singh | Lead — Pipeline orchestration, Terraform/infra, integration |
| Gurpreet Kaur | Checks engine — WildcardPermissions, RiskTrustPolicy, OldAccessKey |
| Yashdeep Singh | PDF report generator (ReportLab) |
| Amna Rafiq | React dashboard — filtering, sorting, drill-down |

---

## Project Structure

```
cloud-access-governance-dashboard/
├── collect.py          # Collects IAM users, roles, policies from AWS
├── checks.py           # Runs 5 governance checks and scores findings
├── report.py           # Generates PDF audit report from findings.json
├── run.py              # Single-command pipeline orchestrator
├── findings.json       # Latest findings output
├── findings.csv        # Latest findings in CSV format
├── iam_snapshot.json   # Latest IAM snapshot from AWS
├── reports/            # Generated PDF reports
└── iam-dashboard/      # React dashboard (Vite)
    └── src/
        └── App.jsx     # Main dashboard component
```

---

## Prerequisites

- Python 3.8+
- Node.js 18+
- AWS credentials configured (`~/.aws/credentials` or environment variables)
- pip packages: `boto3`, `reportlab`

---

## Installation

**1. Clone the repo**
```bash
git clone https://github.com/Aman-Multani/cloud-access-governance-dashboard.git
cd cloud-access-governance-dashboard
```

**2. Install Python dependencies**
```bash
pip install boto3 reportlab
```

**3. Install React dashboard dependencies**
```bash
cd iam-dashboard
npm install
cd ..
```

---

## Running the Pipeline

**Full pipeline (collect → checks → report):**
```bash
python run.py
```

**Skip AWS collection (reuse existing snapshot):**
```bash
python run.py --skip-collect
```

**Skip PDF generation:**
```bash
python run.py --skip-report
```

**Checks only (fastest, no AWS call, no PDF):**
```bash
python run.py --skip-collect --skip-report
```

---

## Running the React Dashboard

**1. Copy the latest findings to the dashboard:**
```bash
# Windows
copy findings.json iam-dashboard\public\data\findings.json

# Mac/Linux
cp findings.json iam-dashboard/public/data/findings.json
```

**2. Start the dev server:**
```bash
cd iam-dashboard
npm run dev
```

**3. Open in browser:** http://localhost:5173

**4. Build static production version:**
```bash
npm run build
```

---

## Governance Checks

| # | Check | Severity | Points | Description |
|---|---|---|---|---|
| 1 | MissingMFA | CRITICAL | 10 | User has no MFA device configured |
| 2 | AdminPermissions | HIGH | 8 | User has AdministratorAccess policy attached |
| 3 | OldAccessKey | HIGH / MEDIUM | 8 / 5 | Active access key older than 90 days (HIGH) or present (MEDIUM) |
| 4 | WildcardPermissions | HIGH | 8 | Inline policy contains Action: * or Resource: * |
| 5 | RiskTrustPolicy | HIGH | 8 | IAM role trust policy allows overly broad principal |

---

## Test Identities (AWS)

| Identity | Type | Purpose |
|---|---|---|
| test-no-mfa | IAM User | Triggers MissingMFA (CRITICAL) |
| test-admin | IAM User | Triggers MissingMFA + AdminPermissions |
| test-old-key | IAM User | Triggers OldAccessKey (key > 90 days) |
| test-wildcard | IAM User | Triggers WildcardPermissions (inline Action: *) |
| test-broad-trust | IAM Role | Triggers RiskTrustPolicy (account-root trust) |

---

## Dashboard Features

- **Summary cards** — Total findings, CRITICAL, HIGH, MEDIUM counts (clickable to filter)
- **Severity filter** — Filter findings by severity level
- **Sortable columns** — Click any column header to sort ascending/descending
- **Per-user drill-down** — Click any username to see all findings for that user with total risk score
- **Export CSV** — Download currently filtered findings as CSV
- **Last pipeline run timestamp** — Shows when data was last generated

---

## PDF Report

The PDF audit report is generated automatically by `report.py` and saved to the `reports/` folder with a dated filename (e.g. `governance_report_2026-05-30.pdf`).

The report includes:
- Executive summary with severity breakdown and action timelines
- Full findings table sorted by severity (highest first)
- Per-user risk breakdown with individual score totals
- Governance baseline coverage table
- Audit timestamp and report version on every page

---

## Phase 2 Improvements Over Phase 1

| Area | Phase 1 | Phase 2 |
|---|---|---|
| Pipeline | Manual script execution | Single `python run.py` command |
| Checks | 3 checks | 5 checks (+ WildcardPermissions, RiskTrustPolicy) |
| Report output | Raw JSON only | Formatted multi-page PDF |
| Dashboard | Basic HTML table | Full React app with filter, sort, drill-down |
| Data collection | Users only | Users + inline policies + IAM roles |

---

*Course: INFO49402 | Sheridan College | Group 12 | Phase 2*
