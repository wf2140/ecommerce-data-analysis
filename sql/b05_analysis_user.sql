-- ============================================
-- 用户行为分析
-- 功能：分析用户购买行为，识别高价值用户和用户分层
-- ============================================

USE ecommerce_analysis;

-- 高价值用户分析（消费额TOP100）
SELECT
    CustomerID,
    COUNT(*) AS order_count,
    SUM(TotalAmount) AS total_spent,
    AVG(TotalAmount) AS avg_order_value,
    MIN(InvoiceDate) AS first_order,
    MAX(InvoiceDate) AS last_order,
    DATEDIFF(MAX(InvoiceDate), MIN(InvoiceDate)) AS customer_lifetime_days,
    Country
FROM orders
WHERE CustomerID IS NOT NULL
GROUP BY CustomerID, Country
ORDER BY total_spent DESC
LIMIT 100;

-- 用户复购率分析
WITH user_orders AS (
    SELECT
        CustomerID,
        COUNT(*) AS order_count,
        MIN(InvoiceDate) AS first_order,
        MAX(InvoiceDate) AS last_order
    FROM orders
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
)
SELECT
    CASE
        WHEN order_count = 1 THEN '首次购买用户'
        WHEN order_count <= 5 THEN '低频用户(2-5次)'
        WHEN order_count <= 10 THEN '中频用户(6-10次)'
        WHEN order_count <= 20 THEN '高频用户(11-20次)'
        ELSE '超高频用户(>20次)'
    END AS user_segment,
    COUNT(*) AS user_count,
    ROUND(COUNT(*) / SUM(COUNT(*)) OVER() * 100, 2) AS user_percentage,
    AVG(order_count) AS avg_orders,
    SUM(order_count) OVER() / COUNT(*) AS overall_avg
FROM user_orders
GROUP BY user_segment
ORDER BY
    CASE user_segment
        WHEN '首次购买用户' THEN 1
        WHEN '低频用户(2-5次)' THEN 2
        WHEN '中频用户(6-10次)' THEN 3
        WHEN '高频用户(11-20次)' THEN 4
        ELSE 5
    END;

-- 用户消费分布（按消费金额分段）
WITH user_spending AS (
    SELECT
        CustomerID,
        SUM(TotalAmount) AS total_spent
    FROM orders
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
)
SELECT
    CASE
        WHEN total_spent < 100 THEN '小额消费(<100元)'
        WHEN total_spent < 500 THEN '中低消费(100-500元)'
        WHEN total_spent < 1000 THEN '中等消费(500-1000元)'
        WHEN total_spent < 5000 THEN '中高消费(1000-5000元)'
        ELSE '高消费(>=5000元)'
    END AS spending_segment,
    COUNT(*) AS user_count,
    ROUND(COUNT(*) / SUM(COUNT(*)) OVER() * 100, 2) AS user_percentage,
    ROUND(AVG(total_spent), 2) AS avg_spending
FROM user_spending
GROUP BY spending_segment
ORDER BY
    CASE spending_segment
        WHEN '小额消费(<100元)' THEN 1
        WHEN '中低消费(100-500元)' THEN 2
        WHEN '中等消费(500-1000元)' THEN 3
        WHEN '中高消费(1000-5000元)' THEN 4
        ELSE 5
    END;

-- 客单价分析
SELECT
    CustomerID,
    COUNT(*) AS order_count,
    SUM(TotalAmount) AS total_spent,
    ROUND(AVG(TotalAmount), 2) AS avg_order_value,
    ROUND(SUM(TotalAmount) / COUNT(*), 2) AS total_avg_order_value,
    Country
FROM orders
WHERE CustomerID IS NOT NULL
GROUP BY CustomerID, Country
ORDER BY avg_order_value DESC
LIMIT 20;

-- 用户购买间隔分析（复购用户）
WITH user_intervals AS (
    SELECT
        CustomerID,
        InvoiceDate,
        LAG(InvoiceDate) OVER(PARTITION BY CustomerID ORDER BY InvoiceDate) AS previous_order_date,
        DATEDIFF(InvoiceDate, LAG(InvoiceDate) OVER(PARTITION BY CustomerID ORDER BY InvoiceDate)) AS days_between_orders
    FROM orders
    WHERE CustomerID IS NOT NULL
)
SELECT
    CASE
        WHEN days_between_orders IS NULL THEN '首次购买'
        WHEN days_between_orders <= 7 THEN '1周内复购'
        WHEN days_between_orders <= 30 THEN '1月内复购'
        WHEN days_between_orders <= 90 THEN '3月内复购'
        ELSE '超过3月复购'
    END AS repeat_interval,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) / SUM(COUNT(*)) OVER() * 100, 2) AS percentage
FROM user_intervals
GROUP BY repeat_interval
ORDER BY
    CASE repeat_interval
        WHEN '首次购买' THEN 1
        WHEN '1周内复购' THEN 2
        WHEN '1月内复购' THEN 3
        WHEN '3月内复购' THEN 4
        ELSE 5
    END;

-- 匿名用户vs注册用户对比
SELECT
    IsAnonymous,
    COUNT(*) AS order_count,
    SUM(TotalAmount) AS total_sales,
    AVG(TotalAmount) AS avg_order_value,
    AVG(Quantity) AS avg_quantity,
    COUNT(DISTINCT Country) AS country_count
FROM orders
GROUP BY IsAnonymous;