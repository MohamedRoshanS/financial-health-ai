from app.core.config import GROQ_API_KEY
from groq import Groq
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)
logger.info("Groq client initialized successfully")

# Define helper functions OUTSIDE the main function
def format_working_capital(wc):
    if not wc:
        return "No working capital data available."
    return f"""
   - DSO (Days Sales Outstanding): {wc.get('dso', 'N/A')} days
   - DPO (Days Payable Outstanding): {wc.get('dpo', 'N/A')} days  
   - Cash Conversion Cycle: {wc.get('cash_conversion_cycle', 'N/A')} days
   - Risk Level: {wc.get('risk_level', 'N/A')}
   - Suggested Actions: {', '.join(wc.get('actions', [])) if wc.get('actions') else 'None'}
    """

def format_bookkeeping(bk):
    if not bk:
        return "No bookkeeping data available."
    
    # Format ledger items safely
    ledger_text = "None"
    if bk.get('ledger'):
        ledger_items = []
        for item in bk.get('ledger', [])[:3]:  # Take only first 3
            account = item.get('account', 'Unknown')
            amount = item.get('expense_amount', 0)
            try:
                ledger_items.append(f"{account} (₹{amount:,.0f})")
            except:
                ledger_items.append(f"{account} (₹{amount})")
        ledger_text = ', '.join(ledger_items)
    
    issues_text = ', '.join(bk.get('issues', [])) if bk.get('issues') else 'None detected'
    
    total_expenses = bk.get('summary', {}).get('total_expenses', 0)
    
    return f"""
   - Total Expenses: ₹{total_expenses:,.0f}
   - Major Expense Categories: {ledger_text}
   - Bookkeeping Issues: {issues_text}
    """

def format_gst(gst_data):
    if not gst_data:
        return "No GST data available."
    
    gst_paid = gst_data.get('gst_paid', 0)
    gst_due = gst_data.get('gst_due', 0)
    
    return f"""
   - Status: {gst_data.get('status', 'N/A')}
   - GST Paid: ₹{gst_paid:,.0f}
   - GST Due: ₹{gst_due:,.0f}
    """

def format_bank_summary(bank):
    if not bank:
        return "No bank data available."
    
    inflows = bank.get('inflows', 0)
    outflows = bank.get('outflows', 0)
    net_flow = inflows - outflows
    
    return f"""
   - Total Inflows: ₹{inflows:,.0f}
   - Total Outflows: ₹{outflows:,.0f}
   - Net Cash Flow: ₹{net_flow:,.0f}
   - Transaction Count: {bank.get('transaction_count', 0)}
    """

def generate_ai_insights(analysis):
    logger.info(f"Starting AI insights generation for analysis with score: {analysis['score']}")
    
    # Get formatted sections
    wc_section = format_working_capital(analysis.get('working_capital', {}))
    bk_section = format_bookkeeping(analysis.get('bookkeeping', {}))
    gst_section = format_gst(analysis.get('gst', {}))
    bank_section = format_bank_summary(analysis.get('bank_summary', {}))
    
    prompt = f"""
You are a financial advisor for small and medium businesses in India.

GIVEN THIS COMPLETE FINANCIAL ANALYSIS:

OVERALL HEALTH:
- Score: {analysis['score']}/100
- Status: {analysis['status']}

SCORE BREAKDOWN:
{analysis['breakdown']}

IDENTIFIED RISKS:
{analysis['risks']}

INDUSTRY BENCHMARKS:
{analysis['benchmarks']}

FORECAST:
- Cash Runway: {analysis['forecast'].get('cash_runway_months', 'N/A')}
- 6-Month Revenue Forecast: {analysis['forecast'].get('revenue_forecast_6_months', [])}

ADDITIONAL FINANCIAL METRICS:

1. WORKING CAPITAL:
{wc_section}

2. BOOKKEEPING SUMMARY:
{bk_section}

3. GST COMPLIANCE:
{gst_section}

4. BANK ACTIVITY:
{bank_section}

TASKS:
1. Explain overall financial health in simple language for a non-finance business owner.
2. Highlight 2-3 positive aspects going well.
3. Identify 2-3 critical areas needing attention.
4. Provide 3-5 actionable recommendations specific to this business.
5. Mention any compliance risks (GST, etc.) if present.
6. Keep tone professional, friendly, and concise (max 400 words).
"""
    
    logger.info("Sending request to Llama 3.1 8B Instant model via Groq API")
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1024
        )
        
        logger.info("Successfully received response from Groq API")
        
        insights = response.choices[0].message.content
        logger.info(f"Generated insights length: {len(insights)} characters")
        
        return insights
        
    except Exception as e:
        logger.error(f"Error in generating AI insights: {str(e)}", exc_info=True)
        return f"Error generating insights. Please try again later."