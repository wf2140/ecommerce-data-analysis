-- ============================================
-- 支付方式分析
-- 功能：分析不同支付方式的使用情况和销售额贡献
-- 注意：当前数据集没有明确的支付方式字段，此SQL作为示例模板
-- ============================================

USE ecommerce_analysis;

-- 支付方式分析示例（假设有payment_method字段）
-- 注意：实际使用时需要根据数据集的实际情况调整字段名

-- 如果数据集中有支付方式字段，可以使用以下查询：
/*
SELECT
    payment_method,
    COUNT(*) AS order_count,
    SUM(TotalAmount) AS total_revenue,
    AVG(TotalAmount) AS avg_order_value,
    ROUND(COUNT(*) / SUM(COUNT(*)) OVER() * 100, 2) AS order_percentage,
    ROUND(SUM(TotalAmount) / SUM(SUM(TotalAmount)) OVER() * 100, 2) AS revenue_percentage
FROM orders
GROUP BY payment_method
ORDER BY total_revenue DESC;
*/

-- 当前数据集分析：基于国家/地区分析
SELECT
    Country,
    COUNT(*) AS order_count,
    SUM(TotalAmount) AS total_revenue,
    AVG(TotalAmount) AS avg_order_value,
    ROUND(COUNT(*) / SUM(COUNT(*)) OVER() * 100, 2) AS order_percentage,
    ROUND(SUM(TotalAmount) / SUM(SUM(TotalAmount)) OVER() * 100, 2) AS revenue_percentage
FROM orders
GROUP BY Country
ORDER BY total_revenue DESC;

-- 各国家订单金额分布
SELECT
    Country,
    MIN(TotalAmount) AS min_amount,
    MAX(TotalAmount) AS max_amount,
    AVG(TotalAmount) AS avg_amount,
    ROUND(AVG(TotalAmount), 2) AS avg_amount_rounded,
    ROUND(STDDEV(TotalAmount), 2) AS std_amount
FROM orders
GROUP BY Country
ORDER BY avg_amount DESC;

-- 各国家用户购买行为
SELECT
    Country,
    COUNT(DISTINCT CustomerID) AS unique_customers,
    COUNT(*) AS total_orders,
    ROUND(COUNT(*) / COUNT(DISTINCT CustomerID), 2) AS orders_per_customer,
    ROUND(SUM(TotalAmount) / COUNT(DISTINCT CustomerID), 2) AS revenue_per_customer
FROM orders
WHERE CustomerID IS NOT NULL
GROUP BY Country
ORDER BY revenue_per_customer DESC;

-- 高额订单分析（>1000元）
SELECT
    Country,
    COUNT(*) AS high_value_order_count,
    SUM(TotalAmount) AS high_value_revenue,
    ROUND(SUM(TotalAmount) / COUNT(*), 2) AS avg_high_value_order,
    ROUND(COUNT(*) / SUM(COUNT(*)) OVER() * 100, 2) AS percentage_of_total_orders
FROM orders
WHERE TotalAmount > 1000
GROUP BY Country
ORDER BY high_value_revenue DESC;

-- 小额订单分析（<50元）
SELECT
    Country,
    COUNT(*) AS low_value_order_count,
    SUM(TotalAmount) AS low_value_revenue,
    ROUND(SUM(TotalAmount) / COUNT(*), 2) AS avg_low_value_order,
    ROUND(COUNT(*) / SUM(COUNT(*)) OVER() * 100, 2) AS percentage_of_total_orders
FROM orders
WHERE TotalAmount < 50
GROUP BY Country
ORDER BY low_value_revenue DESC;