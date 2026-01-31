from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO

def generate_pdf_report(analysis: dict, ai_insights: str = None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(Paragraph("<b>Financial Health Assessment Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Health Score
    elements.append(Paragraph(
        f"<b>Overall Health Score:</b> {analysis['score']} / 100 ({analysis['status']})",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 12))

    # Breakdown
    elements.append(Paragraph("<b>Score Breakdown</b>", styles["Heading2"]))
    for k, v in analysis["breakdown"].items():
        elements.append(Paragraph(f"{k}: {v}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Risks
    elements.append(Paragraph("<b>Identified Risks</b>", styles["Heading2"]))
    if analysis["risks"]:
        for r in analysis["risks"]:
            elements.append(Paragraph(
                f"{r['type']} ({r['severity']}): {r['reason']}",
                styles["Normal"]
            ))
    else:
        elements.append(Paragraph("No major risks detected.", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Benchmarks
    elements.append(Paragraph("<b>Industry Benchmark Comparison</b>", styles["Heading2"]))
    for metric, data in analysis["benchmarks"].items():
        elements.append(Paragraph(
            f"{metric}: Your Business {data['business']} | Industry Avg {data['industry_avg']} ({data['status']})",
            styles["Normal"]
        ))
    elements.append(Spacer(1, 12))

    # Forecast
    elements.append(Paragraph("<b>Forecast & Cash Runway</b>", styles["Heading2"]))
    elements.append(Paragraph(
        f"Estimated Cash Runway: {analysis['forecast']['cash_runway_months']}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 12))

    # AI Insights
    if ai_insights:
        elements.append(Paragraph("<b>AI Insights & Recommendations</b>", styles["Heading2"]))
        for line in ai_insights.split("\n"):
            elements.append(Paragraph(line, styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer
