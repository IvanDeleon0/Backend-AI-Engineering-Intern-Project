import psycopg2
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def format_revenue(value):
    value = float(value)
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.0f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.0f}M"
    return f"${value:.0f}"


def fetch_companies():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="techrevenue",
        user="postgres",
        password="postgres",
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT name, sector, revenue, revenue_year FROM companies ORDER BY revenue DESC"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def build_pdf(rows, output_path="report.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []

    title = Paragraph("Tech Industry Revenue Ranking", styles["Title"])
    timestamp = Paragraph(
        f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]
    )
    elements.append(title)
    elements.append(timestamp)
    elements.append(Spacer(1, 0.3 * inch))

    table_data = [["Rank", "Company", "Sector", "Revenue"]]
    for i, (name, sector, revenue, year) in enumerate(rows, start=1):
        table_data.append([str(i), name, sector, format_revenue(revenue)])

    table = Table(table_data, colWidths=[0.6 * inch, 2 * inch, 2 * inch, 1.2 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
            ]
        )
    )
    elements.append(table)

    doc.build(elements)
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    rows = fetch_companies()
    build_pdf(rows)