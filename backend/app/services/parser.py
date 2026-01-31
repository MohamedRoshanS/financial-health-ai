import pandas as pd

def parse_file(file):
    if file.filename.endswith(".csv"):
        return pd.read_csv(file.file)
    elif file.filename.endswith(".xlsx"):
        return pd.read_excel(file.file)
    else:
        raise ValueError("Unsupported file format")
