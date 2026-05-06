"""
download_report_simple.py

Generate a PDF report with a title page and one image + caption per page.
Requires: pip install fpdf2
"""

import os
from fpdf import FPDF

from Helper.H1_constants import PLOTS_DIR, DEFAULT_PLOTS, DEFAULT_HYPOTHESES
from Helper.helper import ensure_reports_dir


def clean(text):
    """Replace common unicode characters that latin-1 can't encode."""
    return (
        text
        .replace("\u2014", "-")   # em dash —
        .replace("\u2013", "-")   # en dash –
        .replace("\u2018", "'")   # left single quote
        .replace("\u2019", "'")   # right single quote
        .replace("\u201c", '"')   # left double quote
        .replace("\u201d", '"')   # right double quote
        .replace("\u2026", "...")  # ellipsis
    )


def generate_report(filename="report.pdf", title="H1 Analysis Report"):
    reports_dir = ensure_reports_dir()
    output_path = os.path.join(reports_dir, filename)

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)

    # --- Title Page ---
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 140, clean(title), align="C")

    # --- One image + caption per page ---
    for filename in DEFAULT_PLOTS:
        path = os.path.join(PLOTS_DIR, filename)
        if not os.path.exists(path):
            print(f"Skipping missing file: {filename}")
            continue

        caption = clean(DEFAULT_HYPOTHESES.get(filename, ""))

        pdf.add_page()
        pdf.image(path, x=10, y=10, w=190)

        pdf.set_y(260)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, caption, align="C")

    pdf.output(output_path)
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    generate_report(filename="report.pdf", title="Analysis Report")