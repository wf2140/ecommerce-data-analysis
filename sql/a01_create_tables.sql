-- ============================================
   -- 电商数据分析项目 - 建表SQL
   -- 创建数据库和表结构
   -- ============================================

   -- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS ecommerce_analysis
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE ecommerce_analysis;

-- ============================================
-- 创建订单表（主表）
-- ============================================

DROP TABLE IF EXISTS orders;

CREATE TABLE orders(
    -- 原始字段
    InvoiceNo VARCHAR(20) COMMENT '订单号',
    StockCode VARCHAR(20) COMMENT '商品编码',
    Description VARCHAR(255) COMMENT '商品描述',
    Quantity INT COMMENT '数量',
    InvoiceDate DATETIME COMMENT '订单日期',
    UnitPrice DECIMAL(10, 4) COMMENT '单价',
    CustomerID VARCHAR(20) COMMENT '客户ID',
    Country VARCHAR(50) COMMENT '国家',
    -- 计算字段
    TotalAmount DECIMAL(10, 2) COMMENT '订单金额（数量×单价）',
     -- 时间维度字段
     Year INT COMMENT '年份',
     Month INT COMMENT '月份',
     Day INT COMMENT '日期',
     Hour INT COMMENT '小时',
     Weekday INT COMMENT '星期（0=周一，6=周日）',
     WeekOfYear INT COMMENT '一年中的第几周',

     -- 标识字段
     IsAnonymous TINYINT(1) COMMENT '是否匿名订单（1=是，0=否）',
    -- 加索引 = 全表扫描 + 排序 + 构建 B+Tree 结构
    PRIMARY KEY(InvoiceNo,StockCode),
    INDEX idx_invoice_date (InvoiceDate),
    INDEX idx_customer_date (CustomerID),
    INDEX idx_country_date (Country),
    INDEX idx_year_month (Year,Month),
    INDEX idx_total_amount (TotalAmount)
    -- 空表/小表：1000 行 → 瞬间完成
    -- 大表：1亿行 → 逐行读取、排序、写入索引文件
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='电商订单明细表';
   -- ============================================
   -- 创建月度销售汇总表
   -- ============================================
DROP TABLE IF EXISTS monthly_sales;

CREATE TABLE monthly_sales(
    Year INT NOT NULL COMMENT '年份',
    Month INT NOT NULL COMMENT '月份',
    OrderCount INT COMMENT '订单数',
    TotalAmount DECIMAL(15, 2) COMMENT '总销售额',
    AvgOrderValue DECIMAL(10, 2) COMMENT '平均订单金额',
    TotalQuantity INT COMMENT '总销售数量',
    UniqueCustomers INT COMMENT '唯一客户数',
    AvgQuantityPerOrder DECIMAL(10, 2) COMMENT '平均每单商品数量',
    PRIMARY KEY (Year, Month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='月度销售汇总表';

 -- ============================================
 -- 创建城市销售汇总表
 -- ============================================
DROP TABLE IF EXISTS country_sales;
CREATE TABLE country_sales (
    Country VARCHAR(50) NOT NULL COMMENT '国家',
    OrderCount INT COMMENT '订单数',
    TotalAmount DECIMAL(15, 2) COMMENT '总销售额',
    AvgOrderValue DECIMAL(10, 2) COMMENT '平均订单金额',
    TotalQuantity INT COMMENT '总销售数量',
    UniqueCustomers INT COMMENT '唯一客户数',
    MarketShare DECIMAL(5, 2) COMMENT '市场份额（%）',

    PRIMARY KEY (Country),
    INDEX idx_total_amount (TotalAmount)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='国家/地区销售汇总表';

-- ============================================
-- 创建商品销售汇总表
-- ============================================
DROP TABLE IF EXISTS product_sales;

CREATE TABLE product_sales (
    StockCode VARCHAR(20) NOT NULL COMMENT '商品编码',
    ProductName VARCHAR(255) COMMENT '商品名称',
    TotalQuantity INT COMMENT '总销售数量',
    TotalAmount DECIMAL(15, 2) COMMENT '总销售额',
    OrderCount INT COMMENT '订单数',
    AvgPrice DECIMAL(10, 4) COMMENT '平均单价',
    UniqueCustomers INT COMMENT '购买客户数',
    RevenueRank INT COMMENT '销售额排名',

    PRIMARY KEY (StockCode),
    INDEX idx_total_amount (TotalAmount),
    INDEX idx_revenue_rank (RevenueRank)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品销售汇总表';

-- ============================================
-- 创建客户汇总表
-- ============================================
DROP TABLE IF EXISTS customer_summary;

CREATE TABLE customer_summary (
    CustomerID VARCHAR(20) NOT NULL COMMENT '客户ID',
    IsAnonymous TINYINT(1) COMMENT '是否匿名客户',
    Country VARCHAR(50) COMMENT '国家',
    TotalOrders INT COMMENT '总订单数',
    TotalAmount DECIMAL(15, 2) COMMENT '总消费金额',
    AvgOrderValue DECIMAL(10, 2) COMMENT '平均订单金额',
    FirstOrderDate DATETIME COMMENT '首次订单日期',
    LastOrderDate DATETIME COMMENT '最后订单日期',
    CustomerLifetimeDays INT COMMENT '客户生命周期（天）',
    TotalProducts INT COMMENT '购买商品种类数',
    AvgQuantityPerOrder DECIMAL(10, 2) COMMENT '平均每单商品数量',
    CustomerSegment VARCHAR(50) COMMENT '客户分层',
    PRIMARY KEY (CustomerID),
    INDEX idx_total_amount (TotalAmount),
    INDEX idx_customer_segment (CustomerSegment),
    INDEX idx_country (Country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='客户汇总表';

-- ============================================
   -- 显示已创建的表
   -- ============================================
SHOW TABLES;
-- ============================================
   -- 显示表结构
   -- ============================================
DESCRIBE orders;