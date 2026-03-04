-- ============================================
-- 商品销量排名分析
-- 功能：分析商品销售情况，识别畅销商品和滞销商品
-- ============================================

USE ecommerce_analysis;

-- 商品销量TOP10（按销售额）
SELECT
    StockCode,
    Description,
    SUM(Quantity) AS total_quantity,
    SUM(TotalAmount) AS total_revenue,
    COUNT(*) AS order_count,
    AVG(UnitPrice) AS avg_price,
    RANK() OVER(ORDER BY SUM(TotalAmount) DESC) AS revenue_rank
FROM orders
WHERE Description != 'unknown'
GROUP BY StockCode, Description
ORDER BY total_revenue DESC
LIMIT 10;

-- 商品销量TOP10（按销量）
SELECT
    StockCode,
    Description,
    SUM(Quantity) AS total_quantity,
    SUM(TotalAmount) AS total_revenue,
    COUNT(*) AS order_count,
    RANK() OVER(ORDER BY SUM(Quantity) DESC) AS quantity_rank
FROM orders
WHERE Description != 'unknown'
GROUP BY StockCode, Description
ORDER BY total_quantity DESC
LIMIT 10;

-- 各类别销售占比
SELECT
    CASE
        WHEN Description LIKE '%PACK%' THEN '包装类'
        WHEN Description LIKE '%BOX%' THEN '包装类'
        WHEN Description LIKE '%BAG%' THEN '包装类'
        WHEN Description LIKE '%HEART%' THEN '装饰类'
        WHEN Description LIKE '%HOLDER%' THEN '装饰类'
        WHEN Description LIKE '%SIGN%' THEN '装饰类'
        WHEN Description LIKE '%TIN%' THEN '容器类'
        WHEN Description LIKE '%JUG%' THEN '容器类'
        WHEN Description LIKE '%CUP%' THEN '容器类'
        WHEN Description LIKE '%CAKE%' THEN '食品类'
        WHEN Description LIKE '%CHOCOLATE%' THEN '食品类'
        WHEN Description LIKE '%BISCUIT%' THEN '食品类'
        ELSE '其他'
    END AS category,
    SUM(TotalAmount) AS total_revenue,
    ROUND(SUM(TotalAmount) / SUM(SUM(TotalAmount)) OVER() * 100, 2) AS revenue_percentage,
    COUNT(*) AS order_count,
    COUNT(DISTINCT StockCode) AS product_count
FROM orders
WHERE Description != 'unknown'
GROUP BY category
ORDER BY total_revenue DESC;

-- 高价值商品识别（单价>100元）
SELECT
    StockCode,
    Description,
    AVG(UnitPrice) AS avg_price,
    SUM(Quantity) AS total_quantity,
    SUM(TotalAmount) AS total_revenue,
    COUNT(*) AS order_count
FROM orders
WHERE Description != 'unknown'
GROUP BY StockCode, Description
HAVING AVG(UnitPrice) > 100
ORDER BY total_revenue DESC;

-- 商品复购率分析（有多少订单重复购买同一商品）
WITH product_repeat AS (
    SELECT
        StockCode,
        Description,
        CustomerID,
        COUNT(*) AS order_count
    FROM orders
    WHERE Description != 'unknown'
    GROUP BY StockCode, Description, CustomerID
)
SELECT
    StockCode,
    Description,
    COUNT(DISTINCT CustomerID) AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / COUNT(DISTINCT CustomerID) * 100, 2) AS repeat_rate
FROM product_repeat
GROUP BY StockCode, Description
HAVING COUNT(DISTINCT CustomerID) >= 5
ORDER BY repeat_rate DESC
LIMIT 10;

-- 商品销售趋势分析（TOP5商品）
WITH top_products AS (
    SELECT
        StockCode,
        Description
    FROM orders
    WHERE Description != 'unknown'
    GROUP BY StockCode, Description
    ORDER BY SUM(TotalAmount) DESC
    LIMIT 5
)
SELECT
    t.StockCode,
    t.Description,
    YEAR(o.InvoiceDate) AS year,
    MONTH(o.InvoiceDate) AS month,
    SUM(o.TotalAmount) AS total_sales,
    SUM(o.Quantity) AS total_quantity
FROM top_products t
JOIN orders o ON t.StockCode = o.StockCode
GROUP BY t.StockCode, t.Description, YEAR(o.InvoiceDate), MONTH(o.InvoiceDate)
ORDER BY t.StockCode, year, month;