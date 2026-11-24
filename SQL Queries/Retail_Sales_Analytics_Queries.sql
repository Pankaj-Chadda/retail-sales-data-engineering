
-- Monthly Revenue Trend
SELECT
    DATE_TRUNC('MONTH', transaction_date) AS sales_month,
    ROUND(SUM(total_sales_amount), 2) AS monthly_revenue
FROM retail_gold_sales_summary
GROUP BY DATE_TRUNC('MONTH', transaction_date)
ORDER BY sales_month;

--Retail Sales KPIs
SELECT
    SUM(total_sales_amount) AS total_revenue,
    SUM(total_quantity_sold) AS total_quantity_sold,
    SUM(number_of_transactions) AS total_transactions,
    ROUND(
        SUM(total_sales_amount) /
        NULLIF(SUM(number_of_transactions), 0),
        2
    ) AS average_transaction_value
FROM retail_gold_sales_summary;

--Category Sales

SELECT
    category,
    ROUND(SUM(total_sales_amount), 2) AS total_revenue
FROM retail_gold_sales_summary
GROUP BY category
ORDER BY total_revenue DESC;

--Top Products
SELECT
    product_name,
    SUM(total_quantity_sold) AS quantity_sold,
    ROUND(SUM(total_sales_amount), 2) AS revenue
FROM retail_gold_sales_summary
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 10;

-- Store Performance

SELECT
    location,
    ROUND(SUM(total_sales_amount), 2) AS total_revenue,
    SUM(number_of_transactions) AS total_transactions,
    ROW_NUMBER() OVER (
        ORDER BY SUM(total_sales_amount) DESC
    ) AS revenue_rank
FROM retail_gold_sales_summary
GROUP BY location
ORDER BY revenue_rank;

--Store Revenue

SELECT
    store_name,
    location,
    category,
    transaction_date,
    SUM(total_sales_amount) AS total_revenue,
    SUM(number_of_transactions) AS total_transactions
FROM retail_gold_sales_summary
GROUP BY
    store_name,
    location,
    category,
    transaction_date;


