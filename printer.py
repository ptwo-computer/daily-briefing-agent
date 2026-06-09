import subprocess
from datetime import datetime
from fpdf import FPDF


def _sanitize(text: str) -> str:
    """Replace common Unicode characters that Helvetica (Latin-1) can't encode."""
    replacements = {
        "—": "-", "–": "-",   # em dash, en dash
        "‘": "'", "’": "'",   # curly single quotes
        "“": '"', "”": '"',   # curly double quotes
        "…": "...",                 # ellipsis
        "•": "*",                  # bullet
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text.encode("latin-1", errors="replace").decode("latin-1")


class _BriefingPDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(200, 200, 200)
        self.cell(0, 5, "Daily Briefing  ·  Printed automatically at 8:00 AM", align="C")


def _section_label(pdf: FPDF, text: str) -> None:
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


def _divider(pdf: FPDF) -> None:
    pdf.set_draw_color(230, 230, 230)
    pdf.set_line_width(0.3)
    x = pdf.get_x()
    y = pdf.get_y()
    pdf.line(x, y, x + pdf.epw, y)
    pdf.ln(5)


def generate_pdf(weather: str, events: list[str], joke: str, fact: str) -> str:
    pdf = _BriefingPDF()
    pdf.add_page()
    pdf.set_margins(22, 22, 22)
    pdf.set_auto_page_break(auto=True, margin=18)

    date_str = datetime.now().strftime("%A, %B %-d, %Y").upper()

    # ── Header ──────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, "Good morning, Posadas Family", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, date_str, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # bold header rule
    pdf.set_draw_color(20, 20, 20)
    pdf.set_line_width(0.6)
    y = pdf.get_y()
    pdf.line(pdf.get_x(), y, pdf.get_x() + pdf.epw, y)
    pdf.ln(8)

    # ── Weather ─────────────────────────────────────────────
    _section_label(pdf, "WEATHER - BELLEVUE, WA")
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(0, 7, _sanitize(weather), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    _divider(pdf)

    # ── Calendar ────────────────────────────────────────────
    _section_label(pdf, "TODAY'S CALENDAR")
    if events:
        for event in events:
            pdf.set_font("Helvetica", "", 12)
            pdf.set_text_color(20, 20, 20)
            pdf.multi_cell(0, 7, _sanitize(f"  {event}"), new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.set_font("Helvetica", "I", 12)
        pdf.set_text_color(160, 160, 160)
        pdf.cell(0, 7, "Nothing on the calendar today.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    _divider(pdf)

    # ── Dad Joke ────────────────────────────────────────────
    _section_label(pdf, "DAD JOKE OF THE DAY")
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 7, _sanitize(joke), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    _divider(pdf)

    # ── Nature Fact ─────────────────────────────────────────
    _section_label(pdf, "NATURE FACT")
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 7, _sanitize(fact), new_x="LMARGIN", new_y="NEXT")

    output_path = "/tmp/daily_briefing.pdf"
    pdf.output(output_path)
    return output_path


def print_pdf(path: str) -> None:
    subprocess.run(["lp", path], check=True)
