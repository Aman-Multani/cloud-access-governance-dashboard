"""
run.py — Cloud Access Governance Dashboard
Group 12 | INFO49402

Single-command pipeline runner.
Chains: collect.py → checks.py → report.py

Usage:
    python run.py                   # full pipeline
    python run.py --skip-collect    # reuse existing iam_snapshot.json
    python run.py --skip-report     # skip PDF generation
    python run.py --skip-collect --skip-report  # checks only
"""

import subprocess
import sys
import os
import argparse
from datetime import datetime

# ── Colours for console output ──────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def log(msg, colour=RESET):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{colour}{BOLD}[{timestamp}]{RESET} {colour}{msg}{RESET}")

def divider():
    print(f"{CYAN}{'─' * 60}{RESET}")

# ── Run a single script and handle errors ───────────────────────────────────
def run_script(script_name, label):
    divider()
    log(f"Starting: {label}", CYAN)

    script_path = os.path.join(os.path.dirname(__file__), script_name)

    if not os.path.exists(script_path):
        log(f"ERROR — {script_name} not found at {script_path}", RED)
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=False  # let output print live to terminal
    )

    if result.returncode != 0:
        log(f"FAILED — {label} exited with code {result.returncode}", RED)
        log("Pipeline stopped. Fix the error above and re-run.", RED)
        sys.exit(result.returncode)

    log(f"Done: {label}", GREEN)

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Cloud Access Governance Pipeline — Group 12"
    )
    parser.add_argument(
        "--skip-collect",
        action="store_true",
        help="Skip collect.py and reuse the existing iam_snapshot.json"
    )
    parser.add_argument(
        "--skip-report",
        action="store_true",
        help="Skip report.py and do not generate the PDF"
    )
    args = parser.parse_args()

    # ── Banner ───────────────────────────────────────────────────────────────
    divider()
    print(f"{BOLD}{CYAN}")
    print("  Cloud Access Governance Dashboard")
    print("  Group 12 — Automated IAM Audit Pipeline")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{RESET}")
    divider()

    # ── Stage 1: Collect ─────────────────────────────────────────────────────
    if args.skip_collect:
        log("Skipping collect.py — using existing iam_snapshot.json", YELLOW)
        if not os.path.exists("iam_snapshot.json"):
            log("ERROR — iam_snapshot.json not found. Run without --skip-collect first.", RED)
            sys.exit(1)
    else:
        run_script("collect.py", "Stage 1 of 3 — Collecting IAM data from AWS")

    # ── Stage 2: Checks ──────────────────────────────────────────────────────
    run_script("checks.py", "Stage 2 of 3 — Running governance checks")

    # ── Stage 3: Report ──────────────────────────────────────────────────────
    if args.skip_report:
        log("Skipping report.py — PDF generation disabled", YELLOW)
    else:
        run_script("report.py", "Stage 3 of 3 — Generating PDF audit report")

    # ── Done ─────────────────────────────────────────────────────────────────
    divider()
    log("Pipeline complete.", GREEN)
    log(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", GREEN)

    # Show output files if they exist
    outputs = {
        "iam_snapshot.json": "IAM snapshot",
        "findings.json":     "Findings (JSON)",
        "findings.csv":      "Findings (CSV)",
    }
    # Look for any PDF in /reports/
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    if os.path.exists(reports_dir):
        for f in os.listdir(reports_dir):
            if f.endswith(".pdf"):
                outputs[os.path.join("reports", f)] = "PDF audit report"

    print()
    print(f"{BOLD}Output files:{RESET}")
    for path, label in outputs.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  {GREEN}✔{RESET}  {label:<22} → {path}  ({size:,} bytes)")
        else:
            print(f"  {YELLOW}–{RESET}  {label:<22} → not found")
    divider()

if __name__ == "__main__":
    main()
