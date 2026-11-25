"""Validate retail orders and calculate business KPIs."""
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
REQUIRED={"order_id","order_date","region","category","product","units","unit_price_inr","unit_cost_inr","discount_pct","channel","customer_type"}

def load_orders():
    df=pd.read_csv(ROOT/"data/sales_orders.csv")
    missing=REQUIRED-set(df.columns)
    if missing: raise ValueError(f"Missing columns: {sorted(missing)}")
    if df.order_id.duplicated().any(): raise ValueError("Duplicate order IDs")
    df["order_date"]=pd.to_datetime(df.order_date,errors="coerce")
    if df.order_date.isna().any(): raise ValueError("Invalid order dates")
    for col in ["units","unit_price_inr","unit_cost_inr","discount_pct"]:
        df[col]=pd.to_numeric(df[col],errors="coerce")
        if df[col].isna().any(): raise ValueError(f"Invalid values in {col}")
    if (df.units<=0).any() or (~df.discount_pct.between(0,1)).any(): raise ValueError("Units/discount outside valid range")
    df["revenue_inr"]=df.units*df.unit_price_inr*(1-df.discount_pct)
    df["cost_inr"]=df.units*df.unit_cost_inr
    df["profit_inr"]=df.revenue_inr-df.cost_inr
    return df

if __name__=="__main__":
    df=load_orders()
    print("Orders:",df.order_id.nunique())
    print("Revenue INR:",round(df.revenue_inr.sum(),2))
    print("Gross profit INR:",round(df.profit_inr.sum(),2))
    print("Margin %:",round(df.profit_inr.sum()/df.revenue_inr.sum()*100,2))
    print("\nCategory summary:")
    print(df.groupby("category").agg(revenue=("revenue_inr","sum"),profit=("profit_inr","sum")).round(2))
