from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import datetime
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

def generate_pdf_report(analysis: dict, ai_insights: str = None):
    """
    Generate a comprehensive PDF financial health report.
    
    Args:
        analysis: Dictionary containing financial analysis data
        ai_insights: AI-generated insights text (optional)
    
    Returns:
        BytesIO buffer containing PDF
    """
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            title="Financial Health Assessment Report",
            author="Financial Analysis System"
        )
        styles = getSampleStyleSheet()
        
        # =====================
        # CUSTOM STYLES
        # =====================
        styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            leading=12,
            spaceAfter=6
        ))
        
        styles.add(ParagraphStyle(
            name='RiskHigh',
            parent=styles['CustomNormal'],
            textColor=colors.red
        ))
        
        styles.add(ParagraphStyle(
            name='RiskMedium',
            parent=styles['CustomNormal'],
            textColor=colors.orange
        ))
        
        styles.add(ParagraphStyle(
            name='RiskLow',
            parent=styles['CustomNormal'],
            textColor=colors.green
        ))
        
        styles.add(ParagraphStyle(
            name='InsightBullet',
            parent=styles['CustomNormal'],
            leftIndent=20,
            bulletIndent=10,
            spaceBefore=4,
            spaceAfter=4
        ))
        
        elements = []

        # =====================
        # COVER PAGE (FIXED)
        # =====================
        elements.append(Paragraph(
            "<font size=24><b>FINANCIAL HEALTH ASSESSMENT REPORT</b></font>",
            styles["Title"]
        ))
        elements.append(Spacer(1, 24))
        
        # Company Info placeholder
        elements.append(Paragraph(
            "<font size=14><b>Business Financial Analysis</b></font>",
            styles["Heading2"]
        ))
        elements.append(Spacer(1, 36))
        
        # Score Card - FIXED COLOR HANDLING
        score = analysis.get('score', 0)
        status = analysis.get('status', 'Unknown')
        
        # Determine status color
        if status == "Healthy":
            status_color = colors.green
            color_hex = "#10B981"  # Green
        elif status == "Watch":
            status_color = colors.orange
            color_hex = "#F59E0B"  # Amber
        elif status == "Critical":
            status_color = colors.red
            color_hex = "#EF4444"  # Red
        else:
            status_color = colors.black
            color_hex = "#000000"  # Black
        
        elements.append(Paragraph(
            f"<font size=36><b>{score} / 100</b></font>",
            styles["Heading1"]
        ))
        elements.append(Paragraph(
            f"<font color={color_hex}><b>{status.upper()}</b></font>",
            styles["Heading2"]
        ))
        
        elements.append(Spacer(1, 48))
        elements.append(Paragraph(
            f"<i>Report Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}</i>",
            styles["Italic"]
        ))
        
        elements.append(PageBreak())

        # =====================
        # EXECUTIVE SUMMARY
        # =====================
        elements.append(Paragraph(
            "<font size=16><b>EXECUTIVE SUMMARY</b></font>",
            styles["Heading1"]
        ))
        elements.append(Spacer(1, 12))
        
        # Overall Health
        elements.append(Paragraph(
            "<b>Overall Financial Health</b>",
            styles["Heading2"]
        ))
        elements.append(Paragraph(
            f"Your business has achieved a financial health score of <b>{score}/100</b>, "
            f"which is categorized as <b>{status}</b>. "
            "This assessment considers multiple financial metrics including profitability, "
            "liquidity, efficiency, and growth potential.",
            styles["CustomNormal"]
        ))
        elements.append(Spacer(1, 12))
        
        # =====================
        # DETAILED BREAKDOWN
        # =====================
        elements.append(Paragraph(
            "<b>SCORE BREAKDOWN</b>",
            styles["Heading2"]
        ))
        
        # Create table for breakdown
        breakdown_data = [['Metric', 'Score', 'Weight']]
        breakdown = analysis.get('breakdown', {})
        
        if breakdown:
            # Simple equal weight distribution
            weight_per_item = 100 // len(breakdown) if len(breakdown) > 0 else 0
            remaining_weight = 100 - (weight_per_item * len(breakdown))
            
            for i, (metric, score_value) in enumerate(breakdown.items()):
                # Add remaining weight to the last item
                current_weight = weight_per_item + (remaining_weight if i == len(breakdown) - 1 else 0)
                breakdown_data.append([
                    metric.replace('_', ' ').title(),
                    str(score_value),
                    f"{current_weight}%"
                ])
            
            if len(breakdown_data) > 1:
                table = Table(breakdown_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
                ]))
                elements.append(table)
        
        elements.append(Spacer(1, 20))
        
        # =====================
        # RISK ASSESSMENT
        # =====================
        elements.append(Paragraph(
            "<b>RISK ASSESSMENT</b>",
            styles["Heading2"]
        ))
        
        risks = analysis.get('risks', [])
        if risks:
            for risk in risks:
                risk_type = risk.get('type', 'Unknown')
                severity = risk.get('severity', 'Medium')
                reason = risk.get('reason', '')
                
                # Choose style based on severity
                if severity == 'High':
                    risk_style = 'RiskHigh'
                elif severity == 'Medium':
                    risk_style = 'RiskMedium'
                else:
                    risk_style = 'RiskLow'
                
                elements.append(Paragraph(
                    f"<b>{risk_type}</b> ({severity} Risk): {reason}",
                    styles[risk_style]
                ))
                elements.append(Spacer(1, 4))
        else:
            elements.append(Paragraph(
                "<font color=green>✓ No major financial risks detected.</font>",
                styles["CustomNormal"]
            ))
        
        elements.append(Spacer(1, 20))
        
        # =====================
        # INDUSTRY BENCHMARKS
        # =====================
        elements.append(Paragraph(
            "<b>INDUSTRY BENCHMARK COMPARISON</b>",
            styles["Heading2"]
        ))
        
        benchmarks = analysis.get('benchmarks', {})
        if benchmarks:
            benchmark_data = [['Metric', 'Your Business', 'Industry Average', 'Status']]
            
            for metric, data in benchmarks.items():
                business_value = data.get('business', 'N/A')
                industry_avg = data.get('industry_avg', 'N/A')
                status = data.get('status', 'Neutral')
                
                benchmark_data.append([
                    metric.replace('_', ' ').title(),
                    str(business_value),
                    str(industry_avg),
                    status
                ])
            
            if len(benchmark_data) > 1:
                table = Table(benchmark_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ]))
                
                # Apply conditional coloring for status column
                for i in range(1, len(benchmark_data)):
                    status_val = benchmark_data[i][3]
                    if status_val == 'Better':
                        table.setStyle(TableStyle([
                            ('TEXTCOLOR', (-1, i), (-1, i), colors.green)
                        ]))
                    elif status_val == 'Worse':
                        table.setStyle(TableStyle([
                            ('TEXTCOLOR', (-1, i), (-1, i), colors.red)
                        ]))
                
                elements.append(table)
        
        elements.append(Spacer(1, 20))
        
        # =====================
        # WORKING CAPITAL
        # =====================
        working_capital = analysis.get('working_capital')
        if working_capital:
            elements.append(Paragraph(
                "<b>WORKING CAPITAL ANALYSIS</b>",
                styles["Heading2"]
            ))
            
            dso = working_capital.get('dso', 'N/A')
            dpo = working_capital.get('dpo', 'N/A')
            ccc = working_capital.get('cash_conversion_cycle', 'N/A')
            risk_level = working_capital.get('risk_level', 'N/A')
            
            wc_data = [
                ['Metric', 'Value', 'Risk Level'],
                ['DSO (Days Sales Outstanding)', f"{dso} days", ''],
                ['DPO (Days Payable Outstanding)', f"{dpo} days", ''],
                ['Cash Conversion Cycle', f"{ccc} days", risk_level]
            ]
            
            table = Table(wc_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ]))
            
            # Color code risk level
            if risk_level == 'High':
                table.setStyle(TableStyle([
                    ('TEXTCOLOR', (-1, -1), (-1, -1), colors.red)
                ]))
            elif risk_level == 'Medium':
                table.setStyle(TableStyle([
                    ('TEXTCOLOR', (-1, -1), (-1, -1), colors.orange)
                ]))
            elif risk_level == 'Low':
                table.setStyle(TableStyle([
                    ('TEXTCOLOR', (-1, -1), (-1, -1), colors.green)
                ]))
            
            elements.append(table)
            
            # Suggested actions
            actions = working_capital.get('actions', [])
            if actions:
                elements.append(Spacer(1, 10))
                elements.append(Paragraph("<b>Suggested Actions:</b>", styles["CustomNormal"]))
                for action in actions:
                    elements.append(Paragraph(f"• {action}", styles["InsightBullet"]))
        
        elements.append(Spacer(1, 20))
        
        # =====================
        # FORECAST
        # =====================
        forecast = analysis.get('forecast', {})
        if forecast:
            elements.append(Paragraph(
                "<b>FINANCIAL FORECAST</b>",
                styles["Heading2"]
            ))
            
            cash_runway = forecast.get('cash_runway_months', 'N/A')
            elements.append(Paragraph(
                f"<b>Estimated Cash Runway:</b> {cash_runway}",
                styles["CustomNormal"]
            ))
            
            revenue_forecast = forecast.get('revenue_forecast_6_months', [])
            if revenue_forecast and isinstance(revenue_forecast, list):
                elements.append(Spacer(1, 10))
                elements.append(Paragraph("<b>6-Month Revenue Forecast:</b>", styles["CustomNormal"]))
                
                forecast_data = []
                for i, amount in enumerate(revenue_forecast[:6], 1):
                    try:
                        formatted_amount = f"₹{int(amount):,}"
                    except (ValueError, TypeError):
                        formatted_amount = f"₹{amount}"
                    forecast_data.append([f"Month {i}", formatted_amount])
                
                if forecast_data:
                    table = Table(forecast_data, colWidths=[1.5*inch, 2*inch])
                    table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                    ]))
                    elements.append(table)
        
        elements.append(PageBreak())
        
        # =====================
        # AI INSIGHTS & RECOMMENDATIONS
        # =====================
        if ai_insights and ai_insights != "Error generating insights. Please try again later.":
            elements.append(Paragraph(
                "<font size=16><b>AI INSIGHTS & RECOMMENDATIONS</b></font>",
                styles["Heading1"]
            ))
            elements.append(Spacer(1, 12))
            
            # Clean and format AI insights
            cleaned_insights = ai_insights.strip()
            
            # Split into paragraphs and format
            paragraphs = cleaned_insights.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    # Check if paragraph contains bullet points
                    lines = para.split('\n')
                    has_bullets = any(
                        line.strip().startswith(('•', '-', '*')) or 
                        (len(line.strip()) > 1 and line.strip()[0].isdigit() and line.strip()[1] == '.')
                        for line in lines
                    )
                    
                    if has_bullets:
                        # Handle bullet points
                        for line in lines:
                            line = line.strip()
                            if line:
                                # Format bullet points
                                if line.startswith(('•', '-', '*')):
                                    elements.append(Paragraph(
                                        f"• {line[1:].strip()}",
                                        styles["InsightBullet"]
                                    ))
                                elif line[0].isdigit() and line[1] == '.':
                                    elements.append(Paragraph(
                                        f"{line}",
                                        styles["InsightBullet"]
                                    ))
                                else:
                                    elements.append(Paragraph(line, styles["CustomNormal"]))
                    else:
                        # Regular paragraph
                        elements.append(Paragraph(para, styles["CustomNormal"]))
                    elements.append(Spacer(1, 8))
            
            elements.append(Spacer(1, 20))
        
        # =====================
        # DISCLAIMER
        # =====================
        elements.append(Paragraph(
            "<font size=9><i>Disclaimer: This report is generated by AI and is for informational purposes only. "
            "It does not constitute financial advice. Please consult with a qualified financial advisor "
            "before making any business decisions. Generated on "
            f"{datetime.now().strftime('%d %B %Y')}.</i></font>",
            styles["Italic"]
        ))
        
        # =====================
        # ADD PAGE NUMBERS
        # =====================
        def add_page_numbers(canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 8)
            page_num = f"Page {doc.page}"
            canvas.drawRightString(A4[0] - 50, 30, page_num)
            canvas.restoreState()
        
        # Build document
        doc.build(elements, onFirstPage=add_page_numbers, onLaterPages=add_page_numbers)
        buffer.seek(0)
        logger.info("PDF report generated successfully")
        return buffer
        
    except Exception as e:
        logger.error(f"Error in PDF generation: {str(e)}", exc_info=True)
        raise