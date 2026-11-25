-- RetailPulse: SQLite-compatible business questions.
-- Revenue = units * unit_price_inr * (1 - discount_pct)
-- Profit = revenue - units * unit_cost_inr

-- 1. Executive KPIs
SELECT COUNT(DISTINCT order_id) AS orders,
 ROUND(SUM(units*unit_price_inr*(1-discount_pct)),2) AS revenue_inr,
 ROUND(SUM(units*unit_price_inr*(1-discount_pct)-units*unit_cost_inr),2) AS profit_inr
FROM sales_orders;

-- 2. Category performance
SELECT category,
 ROUND(SUM(units*unit_price_inr*(1-discount_pct)),2) AS revenue_inr,
 ROUND(SUM(units*unit_price_inr*(1-discount_pct)-units*unit_cost_inr),2) AS profit_inr
FROM sales_orders GROUP BY category ORDER BY revenue_inr DESC;

-- 3. Monthly revenue trend
SELECT substr(order_date,1,7) AS month,
 ROUND(SUM(units*unit_price_inr*(1-discount_pct)),2) AS revenue_inr
FROM sales_orders GROUP BY month ORDER BY month;

-- 4. Regional contribution
SELECT region,
 ROUND(SUM(units*unit_price_inr*(1-discount_pct)),2) AS revenue_inr
FROM sales_orders GROUP BY region ORDER BY revenue_inr DESC;

-- 5. Product margin
SELECT product,
 ROUND(100.0*SUM(units*unit_price_inr*(1-discount_pct)-units*unit_cost_inr)/
 NULLIF(SUM(units*unit_price_inr*(1-discount_pct)),0),2) AS margin_pct
FROM sales_orders GROUP BY product ORDER BY margin_pct DESC;

-- 6. Discount versus average profit
SELECT discount_pct, COUNT(*) AS orders,
 ROUND(AVG(units*unit_price_inr*(1-discount_pct)-units*unit_cost_inr),2) AS avg_profit_inr
FROM sales_orders GROUP BY discount_pct ORDER BY discount_pct;

-- 7. Channel mix
SELECT channel, COUNT(*) AS orders,
 ROUND(SUM(units*unit_price_inr*(1-discount_pct)),2) AS revenue_inr
FROM sales_orders GROUP BY channel ORDER BY revenue_inr DESC;
