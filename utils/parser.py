import pandas as pd

def parse_bank_statement(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.lower().strip() for col in df.columns]

    date_col = next((col for col in df.columns if "date" in col), None)
    amount_col = next((col for col in df.columns if "amount" in col or "amt" in col), None)
    desc_col = next((col for col in df.columns if "desc" in col or "narration" in col), None)

    if not all([date_col, amount_col, desc_col]):
        return None

    df = df.rename(columns={
        date_col: "Date",
        amount_col: "Amount",
        desc_col: "Description"
    })

    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
    df = df.dropna(subset=["Date", "Amount"])
    df["Category"] = df["Description"].apply(categorize_transaction)

    return df[["Date", "Amount", "Description", "Category"]]


def categorize_transaction(description):
    desc = description.lower()

    if any(keyword in desc for keyword in ["paytm", "phonepe", "gpay"]):
        return "UPI Payment"
    elif any(keyword in desc for keyword in ["karb", "sbin", "yesb"]):
        return "Bank Transfer"
    elif any(keyword in desc for keyword in ["bill", "recharge", "electricity"]):
        return "Utilities"
    elif any(keyword in desc for keyword in ["fuel", "ioc"]):
        return "Fuel"
    elif any(keyword in desc for keyword in ["amazon", "flipkart", "shopping"]):
        return "Shopping"
    else:
        return "Others"