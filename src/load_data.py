from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = ROOT/"data"/"raw"/"online_retail.xlsx"

OUTPUT_FILE = ROOT/"data"/"processed"/"all_transactions.csv"

def main():
    
    if not RAW_FILE.exists():
        raise FileExistsError(
            "Dataset not found. Put dataset inside data/ raw/"
        )
    
    worksheets = pd.read_excel(
        RAW_FILE,sheet_name=None,engine="openpyxl")
    frames=[]
    for sheet_name, frame in worksheets.items():
        frame=frame.copy()
        frame["SourceSheet"]= sheet_name
        frames.append(frame)
    
    data=pd.concat(frames,ignore_index=True)
    
    data.columns = [str(column).strip() for column in data.columns]
    
    expected = { "Invoice", "StockCode", "Description",
        "Quantity", "InvoiceDate", "Price", "Customer ID",
        "Country"
    }
    
    missing = expected.difference(data.columns)
    
    if missing:
        raise ValueError(f"Missing Columns:{sorted(missing)}")
    
    data["InvoiceDate"]=pd.to_datetime(data["InvoiceDate"], errors="coerce")
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    data.to_csv(OUTPUT_FILE, index=False)
    
    print("Dataset loaded successfully!")
    
    print("Total rows:",len(data))
    
    print("Total Columns:",len(data.columns))
    
    print("Saved to:",OUTPUT_FILE)
    
if __name__ == "__main__":
    main()
     