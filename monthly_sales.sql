CREATE VIEW monthly_sales AS
SELECT
    strftime('%Y-%m', order_date) AS sales_month,
    SUM(sales) AS total_monthly_sales
FROM sales_data 
GROUP BY sales_month