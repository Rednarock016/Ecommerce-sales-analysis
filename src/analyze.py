from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT/"data"/"processed"/"sales_clean.csv"

OUTPUT_DIR = ROOT/"output"

def save_chart(fig, filename):
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / filename, dpi=160, bbox_inches="tight")
    plt.close(fig)
    
def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Run load_data.py")
        
    OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
    df = pd.read_csv(INPUT_FILE,parse_dates=["InvoiceDate"])
    df["Customer ID"] = pd.to_numeric(df["Customer ID"],errors="coerce")
    
    #business KPIs
    total_revenue = df["Revenue"].sum()
    total_orders = df["Invoice"].nunique()
    total_customers = df["Customer ID"].nunique()
    total_units = df["Quantity"].sum()
    average_order_value  =  (total_revenue/total_orders if total_orders else 0)
    
    kpis = pd.DataFrame({
        "KPI": ["Total Revenue", "Total Orders", "Total Customer",
            "Total Units Sold", "Average Order Value"],
        "Value": [total_revenue, total_orders, total_customers,
            total_units, average_order_value]})
    kpis.to_csv( OUTPUT_DIR/"kpis.csv", index=False)
    
    print("\nBUSINESS KPIs")
    print(kpis.to_string(index=False))
    
    # Monthly sales analysis
    monthly_sales = (df.groupby("YearMonth",as_index=False)["Revenue"].sum().sort_values("YearMonth"))
    monthly_sales.to_csv(OUTPUT_DIR/"monthly_sales.csv",index=False)
    best_month = monthly_sales.loc[monthly_sales["Revenue"].idxmax()]
    print("\nBEST SALES MONTH")
    print(best_month)
    
    # Country-wise sales
    country_sales = (df.groupby("Country", as_index=False)["Revenue"]
                     .sum().sort_values("Revenue", ascending=False))
    country_sales.to_csv(OUTPUT_DIR/"country_sales.csv", index=False)
    print("\nTop 10 Countries")
    print(country_sales.head(10))
    
    # Product analysis
    product_sales = (df.groupby(["StockCode","Description"], as_index=False)
                     .agg(Revenue=("Revenue","sum"), UnitsSold=("Quantity","sum"))
                     .sort_values("Revenue",ascending=False))
    product_sales.to_csv(OUTPUT_DIR/"product_sales.csv",index=False)
    print("\n Top 10 Product")
    print(product_sales.head(10))
    
    # Invoice analysis
    invoice_summary = (df.groupby("Invoice",as_index=False).agg(OrderRevenue=("Revenue","sum"),Orderdate=("InvoiceDate","min"),Country=("Country","first"),CustomerID=("Customer ID","first")))
    invoice_summary.to_csv(OUTPUT_DIR/"invoice_summary.csv",index=False)

    # Customer RFM analysis
    customer_data = df.dropna(subset=["Customer ID"]).copy()
    if not customer_data.empty:
        reference_data=(customer_data["InvoiceDate"].max()+pd.Timedelta(days=1))
        rfm=customer_data.groupby("Customer ID").agg(Recency=("InvoiceDate",lambda x:(reference_data-x.max()).days),Frequency=("Invoice","nunique"),Monetary=("Revenue","sum")).reset_index()
        rfm.to_csv(OUTPUT_DIR/"customer_rfm.csv",index=False)
        rfm["CustomerType"]=rfm["Frequency"].apply(lambda x:("Repeat" if x>1 else "one-time"))
        customer_summary = (rfm.groupby("CustomerType").agg(Customers=("Customer ID","count"),Revenue=("Monetary","sum")).reset_index())
        customer_summary.to_csv(OUTPUT_DIR/"customer_type_summary.csv",index=False)
        print("\nCustomer Summary")
        print(customer_summary)
        
    # Data visualization
    sns.set_theme(style="whitegrid")
    
        # Monthly revenue chart
    fig, ax = plt.subplots(figsize=(12,5))
    
    sns.lineplot(data=monthly_sales,x="YearMonth",y="Revenue",marker="o",ax=ax)
    ax.set_title("Monthly Revenue Analysis")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x",rotation=60)
    save_chart(fig,"monthly_revenue.png")
    
        # Country
    top_countries = country_sales.head(10).sort_values("Revenue") 
    fig,ax = plt.subplots(figsize=(10,6))
    sns.barplot(data=top_countries,x="Revenue",y="Country",ax=ax)
    ax.set_title("Top 10 Countries by Revenue")
    save_chart(fig,"top_countries.png")
    
        # Product
    top_product = (product_sales.head(10).sort_values("Revenue"))
    fig,ax = plt.subplots(figsize=(11,7))
    sns.barplot(data=top_product,x="Revenue",y="Description",ax=ax)
    ax.set_title("Top 10 Product by Revenue")
    save_chart(fig,"top_products.png")
    print("\nEDA COMPLETED SUCCESSFULLY")
    print("Charts saved in outputs folder.")
if __name__=="__main__":
    main()      

    
    
    

