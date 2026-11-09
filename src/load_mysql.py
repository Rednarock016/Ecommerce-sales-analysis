from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


ROOT = Path(__file__).resolve().parents[1]
print("1")
CSV_FILE = (ROOT/"data"/"processed"/"sales_clean.csv")
print("2")
def main():
    load_dotenv(dotenv_path=ROOT / ".env")
    
    host = os.getenv("DB_HOST")
    print("3")
    Port =os.getenv("DB_PORT")
    print("4")
    database = os.getenv("DB_NAME")
    print("5")
    username = os.getenv("DB_USER")
    print("6")
    password = os.getenv("DB_PASSWORD")
    print("7")
    if not all([host,Port,database,username,password]):
        raise ValueError("Please configure all database setting in .env")
    
    if not CSV_FILE.exists():
        raise FileExistsError("Cleaned CSV file not found.")
    
    
    connection_string = (f"mysql+pymysql://{username}:{password}"f"@{host}:{Port}/{database}")
    print("8")
    engine = create_engine(connection_string)
    print("9")
    df = pd.read_csv(CSV_FILE)
    print("10")
    df.to_sql(name="sales",con=engine,if_exists="replace",index=False,chunksize=5000)
    
    print("Data uploaded Successfully")
    
    print("Total records:",len(df))
    
if __name__ == "__main__":
    main()
    