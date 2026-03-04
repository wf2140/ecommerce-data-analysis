-- ============================================
-- 月度销售趋势分析
-- 功能：分析每月销售数据，计算同比增长率和环比增长率
-- ============================================

USE ecommerce_analysis;

-- 基础月度销售数据
SELECT
    YEAR(InvoiceDate) AS year,
    MONTH(InvoiceDate) AS month,
    COUNT(*) AS order_count,
    SUM(TotalAmount) AS total_sales,
    AVG(TotalAmount) AS avg_order_value,
    SUM(Quantity) AS total_items_sold,
    COUNT(DISTINCT CustomerID) AS unique_customers
FROM orders
GROUP BY YEAR(InvoiceDate), MONTH(InvoiceDate)
ORDER BY year, month;

-- 计算同比增长率和环比增长率（使用窗口函数）
WITH monthly_sales AS (
    SELECT
        YEAR(InvoiceDate) AS year,
        MONTH(InvoiceDate) AS month,
        SUM(TotalAmount) AS total_sales,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY YEAR(InvoiceDate), MONTH(InvoiceDate)
)
SELECT
    year,
    month,
    total_sales,
    order_count,
    -- 环比增长率（与上月对比）
    LAG(total_sales) OVER(ORDER BY year, month) AS last_month_sales,
    ROUND(
        (total_sales - LAG(total_sales) OVER(ORDER BY year, month)) /
        LAG(total_sales) OVER(ORDER BY year, month) * 100, 2
    ) AS mom_growth_rate,
    -- 同比增长率（与去年同期对比）
    LAG(total_sales, 12) OVER(ORDER BY year, month) AS last_year_same_month_sales,
    ROUND(
        (total_sales - LAG(total_sales, 12) OVER(ORDER BY year, month)) /
        LAG(total_sales, 12) OVER(ORDER BY year, month) * 100, 2
    ) AS yoy_growth_rate
FROM monthly_sales
ORDER BY year, month;

-- 累计销售额分析
SELECT
    YEAR(InvoiceDate) AS year,
    MONTH(InvoiceDate) AS month,
    SUM(TotalAmount) AS monthly_sales,
    SUM(SUM(TotalAmount)) OVER(
        ORDER BY YEAR(InvoiceDate), MONTH(InvoiceDate)
    ) AS cumulative_sales,
    ROUND(
        SUM(SUM(TotalAmount)) OVER(
            ORDER BY YEAR(InvoiceDate), MONTH(InvoiceDate)
        ) / SUM(SUM(TotalAmount)) OVER() * 100, 2
    ) AS cumulative_percentage
FROM orders
GROUP BY YEAR(InvoiceDate), MONTH(InvoiceDate)
ORDER BY year, month;

-- 销售额排名（月度）
SELECT
    YEAR(InvoiceDate) AS year,
    MONTH(InvoiceDate) AS month,
    SUM(TotalAmount) AS total_sales,
    RANK() OVER(ORDER BY SUM(TotalAmount) DESC) AS sales_rank,
    DENSE_RANK() OVER(ORDER BY SUM(TotalAmount) DESC) AS dense_sales_rank
FROM orders
GROUP BY YEAR(InvoiceDate), MONTH(InvoiceDate)
ORDER BY year, month;