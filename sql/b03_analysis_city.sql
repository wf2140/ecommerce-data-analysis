-- ============================================
-- 城市/地区销售对比分析
-- 功能：分析各地区的销售情况，识别高潜力城市
-- ============================================

USE ecommerce_analysis;

-- 各城市销售汇总
SELECT
    Country,
    COUNT(*) AS order_count,
    SUM(TotalAmount) AS total_sales,
    AVG(TotalAmount) AS avg_order_value,
    SUM(Quantity) AS total_items,
    COUNT(DISTINCT CustomerID) AS unique_customers,
    ROUND(SUM(TotalAmount) / COUNT(DISTINCT CustomerID), 2) AS revenue_per_customer,
    ROUND(SUM(TotalAmount) / SUM(total_sales) OVER() * 100, 2) AS market_share
FROM orders
GROUP BY Country
ORDER BY total_sales DESC;

-- 城市销售排名
SELECT
    Country,
    SUM(TotalAmount) AS total_sales,
    COUNT(*) AS order_count,
    RANK() OVER(ORDER BY SUM(TotalAmount) DESC) AS sales_rank,
    ROW_NUMBER() OVER(ORDER BY SUM(TotalAmount) DESC) AS row_num
FROM orders
GROUP BY Country
ORDER BY total_sales DESC;

-- 各城市月度销售趋势
SELECT
    Country,
    YEAR(InvoiceDate) AS year,
    MONTH(InvoiceDate) AS month,
    SUM(TotalAmount) AS total_sales,
    COUNT(*) AS order_count
FROM orders
GROUP BY Country, YEAR(InvoiceDate), MONTH(InvoiceDate)
ORDER BY Country, year, month;

-- 高价值城市识别（销售额占比TOP5）
WITH city_sales AS (
    SELECT
        Country,
        SUM(TotalAmount) AS total_sales,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY Country
)
SELECT
    Country,
    total_sales,
    order_count,
    ROUND(total_sales / SUM(total_sales) OVER() * 100, 2) AS sales_percentage,
    'High Value' AS city_tier
FROM city_sales
WHERE Country IN (
    SELECT Country
    FROM city_sales
    ORDER BY total_sales DESC
    LIMIT 5
)
ORDER BY total_sales DESC;

-- 城市增长分析（同比）
WITH monthly_city_sales AS (
    SELECT
        Country,
        YEAR(InvoiceDate) AS year,
        MONTH(InvoiceDate) AS month,
        SUM(TotalAmount) AS total_sales
    FROM orders
    GROUP BY Country, YEAR(InvoiceDate), MONTH(InvoiceDate)
)
SELECT
    Country,
    year,
    month,
    total_sales,
    LAG(total_sales, 12) OVER(PARTITION BY Country ORDER BY year, month) AS last_year_same_month,
    ROUND(
        (total_sales - LAG(total_sales, 12) OVER(PARTITION BY Country ORDER BY year, month)) /
        NULLIF(LAG(total_sales, 12) OVER(PARTITION BY Country ORDER BY year, month), 0) * 100, 2
    ) AS yoy_growth_rate
FROM monthly_city_sales
ORDER BY Country, year, month;