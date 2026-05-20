"""
report.py — Cloud Access Governance Dashboard
Group 12 | INFO49402

Reads findings.json and generates a formatted PDF audit report.
Output saved to: reports/governance_report_YYYY-MM-DD.pdf

Usage:
    python report.py
"""

import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── Config ───────────────────────────────────────────────────────────────────
FINDINGS_FILE  = "findings.json"
REPORTS_DIR    = "reports"
REPORT_VERSION = "v2.0"
GROUP          = "Group 12"
COURSE         = "INFO49402"
PROJECT        = "Cloud Access Governance Dashboard"
TEAM           = "Amandeep Singh, Gurpreet Kaur, Yashdeep Singh, Amna Rafiq"

# ── Colours ──────────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#1F3864")
ACCENT    = colors.HexColor("#2E75B6")
LIGHT_BLU = colors.HexColor("#D6E8F5")
RED       = colors.HexColor("#C00000")
ORANGE    = colors.HexColor("#E36C09")
YELLOW    = colors.HexColor("#9C6500")
GREEN     = colors.HexColor("#375623")
GRAY_BG   = colors.HexColor("#F2F2F2")
GRAY_LINE = colors.HexColor("#AAAAAA")
WHITE     = colors.white
BLACK     = colors.HexColor("#222222")

SEV_COLOUR = {
    "CRITICAL": RED,
    "HIGH":     ORANGE,
    "MEDIUM":   YELLOW,
    "LOW":      GREEN,
}

SEV_BG = {
    "CRITICAL": colors.HexColor("#FDECEA"),
    "HIGH":     colors.HexColor("#FEF4E8"),
    "MEDIUM":   colors.HexColor("#FEFCE8"),
    "LOW":      colors.HexColor("#EDF7ED"),
}

# ── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def style(name, **kwargs):
    return ParagraphStyle(name, **kwargs)

TITLE_STYLE = style("Title",
    fontName="Helvetica-Bold", fontSize=20, textColor=NAVY,
    alignment=TA_CENTER, spaceAfter=4)

SUBTITLE_STYLE = style("Subtitle",
    fontName="Helvetica", fontSize=11, textColor=ACCENT,
    alignment=TA_CENTER, spaceAfter=2)

META_STYLE = style("Meta",
    fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#666666"),
    alignment=TA_CENTER, spaceAfter=2)

SECTION_STYLE = style("Section",
    fontName="Helvetica-Bold", fontSize=12, textColor=WHITE,
    backColor=NAVY, leftIndent=6, spaceBefore=14, spaceAfter=4)

BODY_STYLE = style("Body",
    fontName="Helvetica", fontSize=9, textColor=BLACK,
    leading=13, spaceAfter=4)

BODY_BOLD = style("BodyBold",
    fontName="Helvetica-Bold", fontSize=9, textColor=BLACK, leading=13)

SMALL_STYLE = style("Small",
    fontName="Helvetica", fontSize=8, textColor=colors.HexColor("#555555"),
    leading=11)

CELL_STYLE = style("Cell",
    fontName="Helvetica", fontSize=8, textColor=BLACK, leading=11)

CELL_BOLD = style("CellBold",
    fontName="Helvetica-Bold", fontSize=8, textColor=BLACK, leading=11)

# ── Header / Footer ──────────────────────────────────────────────────────────
RUN_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
RUN_DATE_FILE = datetime.now().strftime("%Y-%m-%d")

def on_page(canvas, doc):
    canvas.saveState()
    w, h = LETTER

    # Header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 0.45 * inch, w, 0.45 * inch, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(0.5 * inch, h - 0.29 * inch, PROJECT)
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(w - 0.5 * inch, h - 0.29 * inch,
                           f"{GROUP}  |  {COURSE}  |  {REPORT_VERSION}")

    # Footer bar
    canvas.setFillColor(GRAY_BG)
    canvas.rect(0, 0, w, 0.4 * inch, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#888888"))
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(0.5 * inch, 0.15 * inch,
                      f"Generated: {RUN_TIMESTAMP}  |  Confidential — Internal Use Only")
    canvas.drawRightString(w - 0.5 * inch, 0.15 * inch,
                           f"Page {doc.page}")
    canvas.restoreState()

# ── Helpers ──────────────────────────────────────────────────────────────────
def section_header(text):
    return Paragraph(f"&nbsp;&nbsp;{text}", SECTION_STYLE)

def sev_badge(sev):
    col = SEV_COLOUR.get(sev, BLACK)
    hex_col = col.hexval() if hasattr(col, 'hexval') else "#333333"
    # Use inline colour via HTML
    colour_map = {
        "CRITICAL": "#C00000",
        "HIGH":     "#E36C09",
        "MEDIUM":   "#9C6500",
        "LOW":      "#375623",
    }
    c = colour_map.get(sev, "#333333")
    return Paragraph(f'<font color="{c}"><b>{sev}</b></font>', CELL_STYLE)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=GRAY_LINE, spaceAfter=6)

# ── Load findings ─────────────────────────────────────────────────────────────
def load_findings():
    if not os.path.exists(FINDINGS_FILE):
        print(f"ERROR — {FINDINGS_FILE} not found. Run checks.py first.")
        exit(1)
    with open(FINDINGS_FILE) as f:
        return json.load(f)

# ── Build PDF ─────────────────────────────────────────────────────────────────
def build_report(findings):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    output_path = os.path.join(REPORTS_DIR, f"governance_report_{RUN_DATE_FILE}.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=LETTER,
        topMargin=0.65 * inch,
        bottomMargin=0.55 * inch,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
    )

    story = []

    # ── TITLE PAGE ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph(PROJECT, TITLE_STYLE))
    story.append(Paragraph("IAM Governance Audit Report", SUBTITLE_STYLE))
    story.append(Spacer(1, 0.08 * inch))
    story.append(hr())
    story.append(Paragraph(f"{GROUP}  &nbsp;|&nbsp;  {COURSE}  &nbsp;|&nbsp;  {REPORT_VERSION}", META_STYLE))
    story.append(Paragraph(f"Team: {TEAM}", META_STYLE))
    story.append(Paragraph(f"Report Date: {RUN_DATE_FILE}", META_STYLE))
    story.append(hr())
    story.append(Spacer(1, 0.2 * inch))

    # ── EXECUTIVE SUMMARY ─────────────────────────────────────────────────────
    story.append(section_header("Executive Summary"))
    story.append(Spacer(1, 0.08 * inch))

    total     = len(findings)
    critical  = sum(1 for f in findings if f.get("severity") == "CRITICAL")
    high      = sum(1 for f in findings if f.get("severity") == "HIGH")
    medium    = sum(1 for f in findings if f.get("severity") == "MEDIUM")
    low       = sum(1 for f in findings if f.get("severity") == "LOW")

    story.append(Paragraph(
        f"This report summarizes the results of an automated IAM governance audit "
        f"conducted against the AWS environment. The pipeline collected IAM user and "
        f"policy data, evaluated it against defined governance baselines, and scored "
        f"each finding by severity. A total of <b>{total} finding(s)</b> were identified "
        f"across <b>{len(set(f.get("UserName","?") for f in findings))} user(s)</b>.",
        BODY_STYLE
    ))
    story.append(Spacer(1, 0.1 * inch))

    # Severity summary table
    summary_data = [
        [Paragraph("<b>Severity</b>", CELL_BOLD), Paragraph("<b>Count</b>", CELL_BOLD),
         Paragraph("<b>Priority</b>", CELL_BOLD), Paragraph("<b>Action Required</b>", CELL_BOLD)],
        [sev_badge("CRITICAL"), Paragraph(str(critical), CELL_STYLE),
         Paragraph("Immediate", CELL_STYLE), Paragraph("Remediate within 24 hours", CELL_STYLE)],
        [sev_badge("HIGH"), Paragraph(str(high), CELL_STYLE),
         Paragraph("Urgent", CELL_STYLE), Paragraph("Remediate within 1 week", CELL_STYLE)],
        [sev_badge("MEDIUM"), Paragraph(str(medium), CELL_STYLE),
         Paragraph("Moderate", CELL_STYLE), Paragraph("Remediate within 1 month", CELL_STYLE)],
        [sev_badge("LOW"), Paragraph(str(low), CELL_STYLE),
         Paragraph("Low", CELL_STYLE), Paragraph("Address in next review cycle", CELL_STYLE)],
    ]

    summary_table = Table(summary_data, colWidths=[1.1*inch, 0.7*inch, 1.0*inch, 4.5*inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  LIGHT_BLU),
        ("GRID",        (0, 0), (-1, -1), 0.4, GRAY_LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GRAY_BG]),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph(
        "Findings are listed below in fix-first order (highest severity first). "
        "Each finding includes the affected user, the governance check that triggered it, "
        "and a recommended remediation action.",
        BODY_STYLE
    ))

    # ── FULL FINDINGS TABLE ───────────────────────────────────────────────────
    story.append(Spacer(1, 0.15 * inch))
    story.append(section_header("All Findings"))
    story.append(Spacer(1, 0.08 * inch))

    # Sort by severity score descending
    sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    sorted_findings = sorted(findings, key=lambda x: sev_order.get(x.get("Severity", "LOW"), 4))

    findings_data = [[
        Paragraph("<b>#</b>", CELL_BOLD),
        Paragraph("<b>User</b>", CELL_BOLD),
        Paragraph("<b>Severity</b>", CELL_BOLD),
        Paragraph("<b>Check</b>", CELL_BOLD),
        Paragraph("<b>Detail</b>", CELL_BOLD),
        Paragraph("<b>Score</b>", CELL_BOLD),
    ]]

    for i, f in enumerate(sorted_findings, 1):
        sev = f.get("Severity", "LOW")
        findings_data.append([
            Paragraph(str(i), CELL_STYLE),
            Paragraph(f.get("UserName", "—"), CELL_STYLE),
            sev_badge(sev),
            Paragraph(f.get("Check", "—"), CELL_STYLE),
            Paragraph(f.get("Detail", "—"), CELL_STYLE),
            Paragraph(str(f.get("Points", "—")), CELL_STYLE),
        ])

    row_bgs = []
    for i in range(1, len(findings_data)):
        sev = sorted_findings[i - 1].get("severity", "LOW")
        row_bgs.append(SEV_BG.get(sev, WHITE))

    findings_table = Table(
        findings_data,
        colWidths=[0.3*inch, 1.2*inch, 0.75*inch, 1.3*inch, 3.1*inch, 0.5*inch]
    )
    findings_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  LIGHT_BLU),
        ("GRID",          (0, 0), (-1, -1), 0.4, GRAY_LINE),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        *[("BACKGROUND", (0, i), (-1, i), row_bgs[i - 1]) for i in range(1, len(findings_data))],
    ]))
    story.append(findings_table)

    # ── PER-USER BREAKDOWN ────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(section_header("Per-User Risk Breakdown"))
    story.append(Spacer(1, 0.08 * inch))
    story.append(Paragraph(
        "The following section groups all findings by user and shows an individual "
        "risk score total for each account.",
        BODY_STYLE
    ))
    story.append(Spacer(1, 0.1 * inch))

    # Group by user
    users = {}
    for f in sorted_findings:
        u = f.get("UserName", "unknown")
        users.setdefault(u, []).append(f)

    for user, ufindings in sorted(users.items(), key=lambda x: -sum(f.get("Points", 0) for f in x[1])):
        total_score = sum(f.get("Points", 0) for f in ufindings)

        # User header
        user_header_data = [[
            Paragraph(f"<b>{user}</b>", CELL_BOLD),
            Paragraph(f"<b>Total Risk Score: {total_score}</b>", CELL_BOLD),
            Paragraph(f"<b>Findings: {len(ufindings)}</b>", CELL_BOLD),
        ]]
        user_header_table = Table(user_header_data, colWidths=[2.8*inch, 2.0*inch, 2.5*inch])
        user_header_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), ACCENT),
            ("TEXTCOLOR",     (0, 0), (-1, -1), WHITE),
            ("GRID",          (0, 0), (-1, -1), 0.3, WHITE),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ]))
        story.append(user_header_table)

        # User findings
        u_data = [[
            Paragraph("<b>Check</b>", CELL_BOLD),
            Paragraph("<b>Severity</b>", CELL_BOLD),
            Paragraph("<b>Detail</b>", CELL_BOLD),
            Paragraph("<b>Recommendation</b>", CELL_BOLD),
            Paragraph("<b>Score</b>", CELL_BOLD),
        ]]
        for f in ufindings:
            sev = f.get("Severity", "LOW")
            u_data.append([
                Paragraph(f.get("Check", "—"), CELL_STYLE),
                sev_badge(sev),
                Paragraph(f.get("Detail", "—"), CELL_STYLE),
                Paragraph(f.get("Recommendation", "—"), CELL_STYLE),
                Paragraph(str(f.get("Points", "—")), CELL_STYLE),
            ])

        u_row_bgs = [SEV_BG.get(f.get("Severity", "LOW"), WHITE) for f in ufindings]
        u_table = Table(u_data, colWidths=[1.3*inch, 0.75*inch, 1.9*inch, 2.3*inch, 0.5*inch])
        u_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0),  LIGHT_BLU),
            ("GRID",          (0, 0), (-1, -1), 0.4, GRAY_LINE),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 5),
            *[("BACKGROUND", (0, i), (-1, i), u_row_bgs[i - 1]) for i in range(1, len(u_data))],
        ]))
        story.append(u_table)
        story.append(Spacer(1, 0.15 * inch))

    # ── GOVERNANCE BASELINE ───────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(section_header("Governance Baseline Coverage"))
    story.append(Spacer(1, 0.08 * inch))
    story.append(Paragraph(
        "The table below maps each governance check to the security principle it enforces "
        "and its current coverage status.",
        BODY_STYLE
    ))
    story.append(Spacer(1, 0.1 * inch))

    baseline_data = [
        [Paragraph("<b>Check</b>", CELL_BOLD), Paragraph("<b>Principle</b>", CELL_BOLD),
         Paragraph("<b>Severity</b>", CELL_BOLD), Paragraph("<b>Status</b>", CELL_BOLD)],
        ["MissingMFA",       "MFA Enforcement",       "CRITICAL", "✔ Active"],
        ["AdminPermissions", "Least Privilege",        "HIGH",     "✔ Active"],
        ["AccessKeyPresent", "Key Rotation / Hygiene", "MEDIUM / HIGH", "✔ Active"],
        ["WildcardPermissions", "Least Privilege",     "HIGH",     "⏳ Phase 2"],
        ["RiskTrustPolicy",  "Trust Boundaries",       "HIGH",     "⏳ Phase 2"],
    ]

    b_table = Table(baseline_data, colWidths=[1.8*inch, 2.0*inch, 1.3*inch, 2.2*inch])
    b_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  LIGHT_BLU),
        ("GRID",          (0, 0), (-1, -1), 0.4, GRAY_LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GRAY_BG]),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 8),
    ]))
    story.append(b_table)
    story.append(Spacer(1, 0.15 * inch))

    # ── FOOTER NOTE ───────────────────────────────────────────────────────────
    story.append(hr())
    story.append(Paragraph(
        f"This report was automatically generated by the Cloud Access Governance Pipeline "
        f"on {RUN_TIMESTAMP}. Report version {REPORT_VERSION}. "
        f"For questions contact {GROUP} — {COURSE}.",
        SMALL_STYLE
    ))

    # ── BUILD ─────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return output_path


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Loading findings...")
    findings = load_findings()
    print(f"Found {len(findings)} findings. Generating PDF...")
    path = build_report(findings)
    print(f"Done! Report saved to: {path}")
