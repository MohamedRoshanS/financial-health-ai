import datetime

def fetch_bank_transactions(account_id: str):
    """
    Mock bank API adapter (sandbox-style)
    Replace with real bank API later (RazorpayX, Setu, Plaid, etc.)
    """

    today = datetime.date.today()

    return [
        {
            "date": today.isoformat(),
            "amount": 150000,
            "type": "credit",
            "description": "Customer payment"
        },
        {
            "date": today.isoformat(),
            "amount": 45000,
            "type": "debit",
            "description": "Office rent"
        },
        {
            "date": today.isoformat(),
            "amount": 18000,
            "type": "debit",
            "description": "Electricity bill"
        }
    ]
