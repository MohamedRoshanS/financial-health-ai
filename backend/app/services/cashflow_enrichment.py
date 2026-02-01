import pandas as pd

def enrich_with_bank_data(df: pd.DataFrame, transactions: list):
    """
    Merge bank transactions into financial dataframe
    """

    bank_df = pd.DataFrame(transactions)

    if bank_df.empty:
        return df

    bank_df["date"] = pd.to_datetime(bank_df["date"]).dt.to_period("M")

    credits = bank_df[bank_df["type"] == "credit"].groupby("date")["amount"].sum()
    debits = bank_df[bank_df["type"] == "debit"].groupby("date")["amount"].sum()

    df = df.copy()

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.to_period("M")

    df["bank_inflows"] = df["date"].apply(
        lambda d: float(credits.get(d, 0)) if pd.notna(d) else 0
    )

    df["bank_outflows"] = df["date"].apply(
        lambda d: float(debits.get(d, 0)) if pd.notna(d) else 0
    )


    return df
