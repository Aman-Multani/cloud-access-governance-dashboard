import json
import http.server
import webbrowser
import os

# Load findings
with open("findings.json") as f:
    findings = json.load(f)

# Count severities
critical = len([f for f in findings if f["Severity"] == "CRITICAL"])
high     = len([f for f in findings if f["Severity"] == "HIGH"])
medium   = len([f for f in findings if f["Severity"] == "MEDIUM"])

# Severity colors
colors = {"CRITICAL": "#EF4444", "HIGH": "#F97316", "MEDIUM": "#F59E0B"}
bg_colors = {"CRITICAL": "#2A1A1A", "HIGH": "#2A1E14", "MEDIUM": "#2A2210"}

# Build findings rows
rows = ""
for i, f in enumerate(findings, 1):
    color = colors.get(f["Severity"], "#CBD5E1")
    bg    = bg_colors.get(f["Severity"], "#1B2A3D")
    rows += f"""
    <tr style="background:{bg}; border-bottom:1px solid #243447;">
      <td style="padding:12px 16px; color:#64748B; font-size:13px;">{i}</td>
      <td style="padding:12px 16px; color:#FFFFFF; font-weight:600; font-size:13px;">{f['UserName']}</td>
      <td style="padding:12px 16px;">
        <span style="background:{color}22; color:{color}; border:1px solid {color}; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:700; letter-spacing:1px;">{f['Severity']}</span>
      </td>
      <td style="padding:12px 16px; color:#14B8A6; font-size:13px; font-weight:600;">{f['Check']}</td>
      <td style="padding:12px 16px; color:#CBD5E1; font-size:12px;">{f['Detail']}</td>
      <td style="padding:12px 16px; color:#94A3B8; font-size:12px; font-style:italic;">{f['Recommendation']}</td>
    </tr>"""

# Build full HTML page
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>IAM Governance Dashboard</title>
  <style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ background:#0D1B2A; color:#FFFFFF; font-family:'Segoe UI', sans-serif; min-height:100vh; }}

    .header {{ background:#1B2A3D; border-bottom:2px solid #0D9488; padding:20px 40px; display:flex; align-items:center; justify-content:space-between; }}
    .header-left h1 {{ font-size:22px; color:#FFFFFF; font-weight:700; }}
    .header-left p  {{ font-size:13px; color:#64748B; margin-top:3px; }}
    .header-right   {{ font-size:12px; color:#0D9488; font-weight:600; letter-spacing:1px; }}

    .stats {{ display:flex; gap:20px; padding:30px 40px 10px; }}
    .stat-card {{ background:#1B2A3D; border:1px solid; border-radius:8px; padding:18px 28px; flex:1; text-align:center; }}
    .stat-card .num  {{ font-size:38px; font-weight:700; }}
    .stat-card .label{{ font-size:11px; color:#64748B; margin-top:4px; letter-spacing:1px; font-weight:600; }}
    .stat-total  {{ border-color:#0D9488; }}
    .stat-total .num  {{ color:#14B8A6; }}
    .stat-critical {{ border-color:#EF4444; }}
    .stat-critical .num {{ color:#EF4444; }}
    .stat-high   {{ border-color:#F97316; }}
    .stat-high .num   {{ color:#F97316; }}
    .stat-medium {{ border-color:#F59E0B; }}
    .stat-medium .num {{ color:#F59E0B; }}

    .section {{ padding:20px 40px 40px; }}
    .section-title {{ font-size:13px; color:#0D9488; font-weight:700; letter-spacing:2px; margin-bottom:14px; }}

    .table-wrap {{ border:1px solid #243447; border-radius:8px; overflow:hidden; }}
    table {{ width:100%; border-collapse:collapse; }}
    thead tr {{ background:#243447; }}
    thead th {{ padding:12px 16px; text-align:left; font-size:11px; color:#64748B; font-weight:700; letter-spacing:1px; text-transform:uppercase; }}
    tbody tr:hover {{ background:#1B2A3D !important; }}

    .footer {{ text-align:center; padding:20px; color:#243447; font-size:12px; border-top:1px solid #1B2A3D; }}
    .goal {{ background:#0B2A26; border:1px solid #0D9488; border-left:4px solid #0D9488; border-radius:4px; padding:14px 20px; margin:0 40px 20px; font-size:13px; color:#CBD5E1; font-style:italic; }}
    .goal span {{ color:#14B8A6; font-weight:700; font-style:normal; }}
  </style>
</head>
<body>
  <div class="header">
    <div class="header-left">
      <h1>Cloud Access Governance Dashboard</h1>
      <p>IAM Risk + Least Privilege Enforcement — Fix-First View</p>
    </div>
    <div class="header-right">PROOF OF CONCEPT v1</div>
  </div>

  <div class="stats">
    <div class="stat-card stat-total">
      <div class="num">{len(findings)}</div>
      <div class="label">TOTAL FINDINGS</div>
    </div>
    <div class="stat-card stat-critical">
      <div class="num">{critical}</div>
      <div class="label">CRITICAL</div>
    </div>
    <div class="stat-card stat-high">
      <div class="num">{high}</div>
      <div class="label">HIGH</div>
    </div>
    <div class="stat-card stat-medium">
      <div class="num">{medium}</div>
      <div class="label">MEDIUM</div>
    </div>
  </div>

  <div class="goal">
    <span>Goal:</span> Make IAM governance visible, measurable, and actionable — sorted by highest risk first.
  </div>

  <div class="section">
    <div class="section-title">FIX-FIRST RISK LIST</div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>User</th>
            <th>Severity</th>
            <th>Check</th>
            <th>Detail</th>
            <th>Recommendation</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
  </div>

  <div class="footer">
    IAM Governance Dashboard — POC v1 &nbsp;·&nbsp; Team: Amandeep Singh · Gurpreet Kaur · Yashdeep Singh · Amna Rafiq
  </div>
</body>
</html>"""

# Write HTML file
with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard ready! Opening in browser...")
webbrowser.open("file://" + os.path.abspath("dashboard.html"))
