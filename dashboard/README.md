# Security Dashboard UI Plan

This dashboard will display security findings from IAM validation checks.

## Summary Section

Displays quick counts of detected issues.

Examples:
- Total IAM Users
- Users Missing MFA
- Users with Access Keys
- Users with Admin Permissions

## Fix-First Table

A prioritized table showing the most critical issues first.

Example columns:

| Issue Type | User | Severity | Recommendation |
|------------|------|----------|---------------|

Issues should be sorted by severity so the most critical problems appear first.

## Filters

Users will be able to filter findings by:

- Issue Type
- Severity
- User Name
- Status

## Export Options

The dashboard should allow exporting findings as:

- CSV
- JSON
- PDF (optional)

## Technology Decision

The dashboard framework is still being evaluated.

Possible options:

- Streamlit – faster to prototype
- Flask – more flexible backend architecture

Final decision will be made during implementation.

## Documentation Links

Related documentation:

- docs/report-template.md
- docs/validation-checklist.md
