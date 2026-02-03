 ----problem statment-----
 
 ---Perform a Pareto (80/20) analysis to identify the percentage of customers contributing to the majority of total sales.----
 
 CREATE VIEW pareto_customers AS
 SELECT
    customer_id,
    customer_name,
    total_sales,
    cumulative_sales,
    ROUND(
        (cumulative_sales * 100.0) / overall_sales,
        2
    ) AS cumulative_sales_pct
FROM (
    SELECT
        c.customer_id,
        c.customer_name,
        SUM(oi.sales) AS total_sales,
        SUM(SUM(oi.sales)) OVER (
            ORDER BY SUM(oi.sales) DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_sales,
        SUM(SUM(oi.sales)) OVER () AS overall_sales
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id, c.customer_name
)
WHERE cumulative_sales_pct <= 85
ORDER BY total_sales DESC;
