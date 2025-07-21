import pandas as pd

def receipts_to_df(data):
    return pd.DataFrame(data, columns=["ID", "Vendor", "Date", "Amount", "Category"])

def aggregate_stats(df):
    return {
        "Total Spend": df["Amount"].sum(),
        "Average Spend": df["Amount"].mean(),
        "Top Vendor": df["Vendor"].value_counts().idxmax()
    }

def monthly_trend(df):
    df['Date'] = pd.to_datetime(df['Date'])
    return df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum()
