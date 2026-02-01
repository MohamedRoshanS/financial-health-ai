import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd
import io
import re
from datetime import datetime

def extract_text_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_scanned_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            img = page.to_image(resolution=300).original
            text += pytesseract.image_to_string(img)
    return text.strip()

def extract_financial_data(text: str) -> dict:
    """Extract comprehensive financial data from PDF text"""
    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "revenue": 0.0,
        "expense_amount": 0.0,
        "expense_category": "General",
        "accounts_receivable": 0.0,
        "accounts_payable": 0.0,
        "inventory_value": 0.0,
        "loan_emi": 0.0,
        "gst_paid": 0.0,
        "gst_due": 0.0,
        "cash_balance": 0.0,
        "fixed_assets": 0.0
    }
    
    # Clean the text
    text = text.lower()
    
    # Extract date (look for quarter ended date)
    date_match = re.search(r'quarter ended (\w+ \d{1,2}, \d{4})', text, re.IGNORECASE)
    if date_match:
        try:
            data["date"] = pd.to_datetime(date_match.group(1)).strftime("%Y-%m-%d")
        except:
            pass
    
    # REVENUE PATTERNS
    revenue_patterns = [
        r'revenue from operations.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'sales.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'total revenue.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'sales\s*\/\s*services.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    ]
    
    for pattern in revenue_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                data["revenue"] = float(match.group(1).replace(",", ""))
                break
            except:
                continue
    
    # EXPENSE PATTERNS (from cash flow - cash paid to suppliers/employees)
    expense_patterns = [
        r'cash paid to suppliers.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'cash paid.*?employees.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'expenses.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    ]
    
    for pattern in expense_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                data["expense_amount"] = float(match.group(1).replace(",", ""))
                break
            except:
                continue
    
    # ACCOUNTS RECEIVABLE (Trade Receivables from balance sheet)
    ar_patterns = [
        r'trade receivables.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'receivables.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'accounts receivable.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    ]
    
    for pattern in ar_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                data["accounts_receivable"] = float(match.group(1).replace(",", ""))
                break
            except:
                continue
    
    # ACCOUNTS PAYABLE (Trade Payables from balance sheet)
    ap_patterns = [
        r'trade payables.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'payables.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'accounts payable.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    ]
    
    for pattern in ap_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                data["accounts_payable"] = float(match.group(1).replace(",", ""))
                break
            except:
                continue
    
    # INVENTORY VALUE
    inventory_patterns = [
        r'inventories.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'inventory.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'stock.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    ]
    
    for pattern in inventory_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                data["inventory_value"] = float(match.group(1).replace(",", ""))
                break
            except:
                continue
    
    # LOAN EMI (from financing activities - loan repayments)
    loan_patterns = [
        r'loan repayments.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'loan.*?repayment.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'emi.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    ]
    
    for pattern in loan_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                data["loan_emi"] = float(match.group(1).replace(",", ""))
                break
            except:
                continue
    
    # CASH BALANCE (from cash flow statement)
    cash_patterns = [
        r'cash at end.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'cash and bank.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'cash balance.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    ]
    
    for pattern in cash_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                data["cash_balance"] = float(match.group(1).replace(",", ""))
                break
            except:
                continue
    
    # GST - if mentioned (common in Indian financials)
    gst_patterns = [
        r'gst.*?paid.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'tax.*?paid.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'direct taxes.*?paid.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    ]
    
    for pattern in gst_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                data["gst_paid"] = float(match.group(1).replace(",", ""))
                break
            except:
                continue
    
    return data

def parse_pdf(file_bytes: bytes):
    text = extract_text_pdf(file_bytes)

    if not text or len(text.strip()) < 50:
        text = extract_scanned_pdf(file_bytes)
        confidence = 0.65
    else:
        confidence = 0.85

    if not text:
        raise ValueError("Unable to extract text from PDF")

    financial_data = extract_financial_data(text)
    df = pd.DataFrame([financial_data])

    return df, confidence
