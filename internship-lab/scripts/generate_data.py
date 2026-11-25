"""Generate deterministic synthetic datasets for the Internship Lab."""
from pathlib import Path
import csv, random
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
random.seed(42)
rng = np.random.default_rng(42)

products = {
 "Electronics":[("Wireless Earbuds",1899,920),("Smart Watch",3499,1950),("Bluetooth Speaker",2499,1280),("USB-C Hub",1299,560)],
 "Apparel":[("Everyday Hoodie",1199,490),("Classic Tee",599,210),("Running Shoes",2799,1420),("Denim Jacket",2199,980)],
 "Home":[("Desk Lamp",899,370),("Storage Rack",1599,840),("Cotton Bedsheet",1399,610),("Steel Bottle",499,170)],
 "Beauty":[("Skin Care Kit",999,420),("Hair Dryer",1899,950),("Daily Sunscreen",449,165),("Fragrance Mist",799,330)],
 "Sports":[("Yoga Mat",799,310),("Resistance Bands",499,145),("Gym Duffel",1299,560),("Protein Shaker",349,105)]
}
regions=["North","South","East","West"]
channels=["Online","Store","Marketplace"]
rows=[]
from datetime import date, timedelta
for i in range(1,481):
    category=random.choice(list(products)); product,price,cost=random.choice(products[category])
    units=int(rng.integers(1,6)); discount=float(rng.choice([0,.05,.10,.15,.20],p=[.25,.24,.28,.16,.07]))
    d=date(2025,1,1)+timedelta(days=int(rng.integers(0,365)))
    rows.append({"order_id":f"ORD-{i:04d}","order_date":d.isoformat(),"region":random.choice(regions),
      "category":category,"product":product,"units":units,"unit_price_inr":price,"unit_cost_inr":cost,
      "discount_pct":discount,"channel":random.choice(channels),
      "customer_type":random.choices(["New","Returning"],weights=[.38,.62])[0]})
(ROOT/"data").mkdir(exist_ok=True)
with (ROOT/"data/sales_orders.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

n=1400; churn=[]
for i in range(1,n+1):
    tenure=int(rng.integers(1,73)); monthly=float(np.clip(rng.normal(690,210),299,1499))
    contract=random.choices(["Monthly","Annual","Two-year"],weights=[.54,.30,.16])[0]
    tickets=int(min(rng.poisson(1.35),8)); dependents=int(rng.binomial(1,.34)); autopay=int(rng.binomial(1,.57))
    delay=int(np.clip(rng.normal(5.5,5),0,30)); internet=random.choices(["Fiber","DSL","None"],weights=[.46,.43,.11])[0]
    logit=-2.05+(1.25 if contract=="Monthly" else -.55 if contract=="Two-year" else .15)
    logit+=(.75 if tenure<12 else .20 if tenure<24 else -.25 if tenure>48 else 0)
    logit+=.33*tickets+.055*delay+(.28 if internet=="Fiber" else 0)
    logit+=(-.48 if autopay else .16)+(-.38 if dependents else 0)+.00045*(monthly-700)
    prob=1/(1+np.exp(-logit)); label=int(rng.binomial(1,prob))
    churn.append({"customer_id":f"CUS-{i:04d}","tenure_months":tenure,"monthly_charges_inr":round(monthly,2),
      "contract_type":contract,"support_tickets_90d":tickets,"has_dependents":dependents,
      "autopay_enabled":autopay,"payment_delay_days":delay,"internet_service":internet,"churned":label})
with (ROOT/"data/customer_churn.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(churn[0])); w.writeheader(); w.writerows(churn)
print(f"Generated {len(rows)} synthetic orders and {len(churn)} synthetic customers.")
