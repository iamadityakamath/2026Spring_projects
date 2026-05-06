"""
download_report_simple.py

Generate a PDF report with a title page and one image + caption per page.
Requires: pip install fpdf2
"""

import os
from fpdf import FPDF

import Helper.H1_constants as _h1
import Helper.H3_constants as _h3
from Helper.helper import ensure_reports_dir

_HYPOTHESIS_CONSTANTS = {
    "h1": _h1,
    "h3": _h3,
}


def clean(text):
    """Replace common unicode characters that latin-1 can't encode."""
    return (
        text
        .replace("—", "-")   # em dash —
        .replace("–", "-")   # en dash –
        .replace("‘", "'")   # left single quote
        .replace("’", "'")   # right single quote
        .replace("“", '"')   # left double quote
        .replace("”", '"')   # right double quote
        .replace("…", "...")  # ellipsis
    )


def generate_report(filename="report.pdf", title="Analysis Report", hypothesis="h1"):
    constants = _HYPOTHESIS_CONSTANTS.get(hypothesis.lower())
    if constants is None:
        raise ValueError(f"Unknown hypothesis '{hypothesis}'. Choose from: {list(_HYPOTHESIS_CONSTANTS)}")

    plots_dir = constants.PLOTS_DIR
    default_plots = constants.DEFAULT_PLOTS
    default_hypotheses = constants.DEFAULT_HYPOTHESES

    reports_dir = ensure_reports_dir()
    output_path = os.path.join(reports_dir, filename)

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)

    # --- Title Page ---
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 140, clean(title), align="C")

    # --- One image + caption per page ---
    for plot_file in default_plots:
        path = os.path.join(plots_dir, plot_file)
        if not os.path.exists(path):
            print(f"Skipping missing file: {plot_file}")
            continue

        caption = clean(default_hypotheses.get(plot_file, ""))

        pdf.add_page()
        pdf.image(path, x=10, y=10, w=190)

        pdf.set_y(260)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, caption, align="C")

    pdf.output(output_path)
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    generate_report(filename="report_h1.pdf", title="H1 Analysis Report", hypothesis="h1")
