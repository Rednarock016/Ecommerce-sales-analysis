from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT/"data"/"processed"/"all_transactions.csv"

SALES_FILE = ROOT/"data"/"processed"/"sales_clean.csv"

CANCEL_FILE = ROOT/"data"/"processed"/"cancellations.csv"

QUALITY_FILE = ROOT/"output"/"data_quality_report.csv"


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "Run load_data.py first"
        )
    
    df = pd.read_csv(INPUT_FILE, parse_dates=["InvoiceDate"])
    
    initial_rows = len(df)
    
    df = df.drop_duplicates().copy()
    
    duplicates_removed = initial_rows - len(df)
    
    df["Price"]=pd.to_numeric(df["Price"], errors = "coerce")
    
    df["Quantity"]=pd.to_numeric(df["Quantity"], errors = "coerce")
    
    df["Customer ID"]=pd.to_numeric(df["Customer ID"], errors = "coerce")
    
    invoice_text = (df["Invoice"].astype(str).str.strip().str.upper())
    
    cancellation_mask = (invoice_text.str.startswith("C") | (df["Quantity"]<0))
    
    cancellations = df.loc[cancellation_mask].copy()
    
    sales = df.loc[-cancellation_mask].copy()
    
    sales = sales.dropna(subset=["InvoiceDate" , "Quantity" , "Price" , "Invoice"])
    
    sales = sales[(sales["Quantity"]>0) & (sales["Price"]>0)].copy()
    
    sales["Revenue"] = (sales["Quantity"]*sales["Price"])
    
    sales["Description"] = (sales["Description"].fillna("unknown").astype(str).str.strip())
    
    sales["Year"] = sales["InvoiceDate"].dt.year
    
    sales["Month"] = sales["InvoiceDate"].dt.month
    
    sales["YearMonth"] = (sales["InvoiceDate"].dt.to_period("M").astype(str))
    
    SALES_FILE.parent.mkdir(parents=True,exist_ok=True)
    
    QUALITY_FILE.parent.mkdir(parents=True,exist_ok=True)
    
    sales.to_csv(SALES_FILE,index=False)
    
    cancellations.to_csv(CANCEL_FILE,index=False)
    
    quality = pd.DataFrame([
        {"Metric": "Original rows", "Value": initial_rows },
        {"Metric": "Duplicates removed", "Value": duplicates_removed},
        {"Metric": "Cancellation records", "Value": len(cancellations)},
        {"Metric": "Clean sales rows", "Value": len(sales)},
        {"Metric": "Missing customer IDs", "Value": sales["Customer ID"].isna().sum()}
    ])
    
    quality.to_csv(QUALITY_FILE,index=True)
    
    print("Data cleeaning completed!")
    
    print("clean sales recods:", len(sales))
    
    print("cancellation records:",len(cancellations))
    
if __name__ == "__main__":
        main()

