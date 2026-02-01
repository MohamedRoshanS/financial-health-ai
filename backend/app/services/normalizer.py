import pandas as pd

COLUMN_MAP = {
    "date": ["date", "month"],
    "revenue": ["revenue", "sales", "income"],
    "expense_category": ["expense_category", "category"],
    "expense_amount": ["expense_amount", "expense", "cost"],
    "accounts_receivable": ["receivable", "accounts_receivable"],
    "accounts_payable": ["payable", "accounts_payable"],
    "inventory_value": ["inventory", "stock"],
    "loan_emi": ["loan_emi", "emi"],
    "gst_paid": ["gst_paid"],
    "gst_due": ["gst_due"]
}

def normalize_data(df):
    warnings = []
    
    # Make sure we're working with a DataFrame
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    
    df.columns = df.columns.str.lower().str.strip()
    normalized = {}
    
    # First, try to find exact matches for our required columns
    for standard, variants in COLUMN_MAP.items():
        column_found = False
        
        # Check variants
        for v in variants:
            if v in df.columns:
                normalized[standard] = df[v]
                column_found = True
                break
        
        # Check for approximate matches (for PDF data)
        if not column_found:
            for col in df.columns:
                if any(variant in col for variant in variants):
                    normalized[standard] = df[col]
                    column_found = True
                    break
        
        # If still not found, set to 0
        if not column_found:
            if standard == "date":
                # Use current date if no date column
                normalized[standard] = pd.Series([pd.Timestamp.now()])
                warnings.append("Date column missing, using current date")
            else:
                normalized[standard] = 0
                warnings.append(f"Missing column: {standard}")
    
    clean_df = pd.DataFrame(normalized)
    
    # Convert date to period
    try:
        clean_df["date"] = pd.to_datetime(clean_df["date"], errors='coerce')
        clean_df["date"] = clean_df["date"].dt.to_period("M")
    except:
        clean_df["date"] = pd.Period.now('M')
        warnings.append("Date conversion failed, using current month")
    
    # Group by month
    monthly_df = clean_df.groupby("date").sum(numeric_only=True).reset_index()
    
    return monthly_df, warnings