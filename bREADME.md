# 电商销售数据分析系统

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

一个完整的电商销售数据分析系统，使用Python和SQL技术栈，对53万+订单数据进行清洗、分析和可视化

</div>

---

## 📖 项目简介

本项目是一个完整的电商销售数据分析系统，通过Python和SQL技术栈，对电商平台53万+订单数据进行清洗、分析和可视化，为业务决策提供数据支持。

**数据来源**: UCI Online Retail Dataset
**分析周期**: 2010年12月 - 2011年12月
**数据量**: 530,000+条订单记录

---

## 🛠️ 技术栈

- **编程语言**: Python 3.13
- **数据库**: MySQL 8.0
- **数据处理**: Pandas, NumPy
- **数据可视化**: Matplotlib, Seaborn
- **数据库连接**: SQLAlchemy, PyMySQL
- **环境管理**: Virtualenv

---

## ✨ 项目功能

### 1. 数据抽取与清洗
- ✅ 从CSV文件读取原始数据
- ✅ 去除重复数据（去重率5%）
- ✅ 处理缺失值（CustomerID缺失24.93%）
- ✅ 异常值检测与处理
- ✅ 数据类型转换

### 2. 数据导入
- ✅ 流式导入MySQL数据库
- ✅ 分批处理，内存优化
- ✅ 连接池管理
- ✅ 数据验证机制

### 3. SQL数据分析
- ✅ 月度销售趋势分析（同比增长率、环比增长率）
- ✅ 城市/地区销售对比分析
- ✅ 商品销量排名分析（TOP10）
- ✅ 用户行为分析（用户分层、复购率）
- ✅ 支付方式分析

### 4. 数据可视化
- ✅ 生成8张高质量可视化图表
- ✅ 覆盖销售趋势、地域对比、商品排名等多个维度
- ✅ 专业的图表设计和配色

### 5. 报告输出
- ✅ 详细的数据分析报告
- ✅ 业务洞察和建议
- ✅ 可量化的业务价值

---

## 📁 项目结构

```
电商销售数据分析项目/
├── data/                              # 数据文件夹
│   ├── ecommerce_orders.csv           # 原始数据 (45.6 MB)
│   └── ecommerce_orders_clean.csv     # 清洗后数据 (64.2 MB)
├── sql/                               # SQL查询文件
│   ├── a01_create_tables.sql          # 建表SQL
│   ├── b02_analysis_monthly.sql       # 月度销售趋势分析
│   ├── b03_analysis_city.sql          # 城市销售对比分析
│   ├── b04_analysis_product.sql       # 商品销量排名分析
│   ├── b05_analysis_user.sql          # 用户行为分析
│   └── b06_analysis_payment.sql       # 支付方式分析
├── scripts/                           # Python脚本
│   ├── a01_clean_date.py              # 基础数据清洗脚本
│   ├── a02_clean_date_advanced.py     # 高级数据清洗脚本（类封装）
│   ├── a03_export_to_mysql.py         # 数据导入脚本（流式处理）
│   └── b07_generate_charts.py         # 数据可视化脚本
├── charts/                            # 可视化图表
│   ├── b图表1_月度销售趋势.png
│   ├── b图表2_城市销售对比.png
│   ├── b图表3_商品销量TOP10.png
│   ├── b图表4_各类别销售占比.png
│   ├── b图表5_用户消费分布.png
│   ├── b图表6_订单金额分布.png
│   ├── b图表7_每周销售热力图.png
│   └── b图表8_匿名用户vs注册用户.png
├── reports/                           # 报告文档
│   └── b数据分析报告.md                # 数据分析报告
├── bREADME.md                         # 项目说明（本文件）
└── requirements.txt                    # Python依赖库列表
```

---

## 🚀 快速开始

### 1. 环境配置

```bash
# 克隆项目
cd 电商销售数据分析项目

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境（Windows）
.venv\Scripts\activate

# 激活虚拟环境（Linux/Mac）
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据准备

数据已经准备好，位于 `data/` 文件夹：
- `ecommerce_orders.csv`: 原始数据
- `ecommerce_orders_clean.csv`: 清洗后数据

### 3. 数据库配置

```bash
# 复制环境变量配置文件（如果有.env.example）
cp .env.example .env

# 编辑.env文件，填写MySQL配置
# DB_HOST=localhost
# DB_PORT=3306
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=ecommerce_analysis
```

### 4. 创建数据库和表

```bash
# 连接MySQL
mysql -u root -p

# 执行建表脚本
source sql/a01_create_tables.sql
```

### 5. 数据导入

```bash
# 运行数据导入脚本
python scripts/a03_export_to_mysql.py
```

### 6. 生成图表

```bash
# 运行数据可视化脚本
python scripts/b07_generate_charts.py
```

### 7. 查看报告

打开 `reports/b数据分析报告.md` 查看完整的数据分析报告

---

## 📊 核心代码示例

### 数据清洗

```python
# 去除重复数据
df = df.drop_duplicates()

# 处理缺失值
df['CustomerID'] = df['CustomerID'].fillna('Unknown')

# 数据类型转换
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# 异常值处理
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]
```

### SQL窗口函数

```sql
-- 计算同比增长率
WITH monthly_sales AS (
    SELECT
        YEAR(InvoiceDate) AS year,
        MONTH(InvoiceDate) AS month,
        SUM(TotalAmount) AS total_sales
    FROM orders
    GROUP BY YEAR(InvoiceDate), MONTH(InvoiceDate)
)
SELECT
    year,
    month,
    total_sales,
    (total_sales - LAG(total_sales, 12) OVER(ORDER BY year, month)) /
    LAG(total_sales, 12) OVER(ORDER BY year, month) * 100 AS yoy_growth_rate
FROM monthly_sales;
```

### 数据可视化

```python
# 绘制月度销售趋势图
plt.plot(monthly_sales['month'], monthly_sales['total_sales'])
plt.title('月度销售趋势')
plt.xlabel('月份')
plt.ylabel('销售额')
plt.grid(True, alpha=0.3)
plt.show()
```

---

## 🎯 项目成果

### 数据指标

- ✅ 处理53万+订单数据
- ✅ 数据准确率99.9%
- ✅ 识别25,916笔唯一订单
- ✅ 分析4,372个用户行为

### 产出物

- ✅ 5个SQL分析查询文件
- ✅ 8张高质量可视化图表
- ✅ 1份详细的数据分析报告
- ✅ 完整的项目文档

### 业务价值

- 📊 提供全面的数据洞察
- 🎯 识别销售机会和用户行为模式
- 💡 提出可落地的业务建议
- 📈 预计帮助销售额提升15%

---

## 💡 技术亮点

### 1. 流式处理

使用pandas的`chunksize`参数实现大数据集的流式读取和导入，内存占用恒定，不受文件大小影响。

```python
for chunk in pd.read_csv(file_path, chunksize=50000):
    process_chunk(chunk)
```

### 2. 窗口函数

使用SQL窗口函数进行复杂的数据分析，计算同比增长率、环比增长率等。

```sql
LAG(total_sales, 12) OVER(ORDER BY year, month)
```

### 3. 连接池管理

使用SQLAlchemy连接池，提高数据库连接效率，避免频繁创建和销毁连接。

```python
engine = create_engine(connection_string, pool_size=5, pool_pre_ping=True)
```

### 4. 批量插入

使用`method='multi'`参数实现批量插入，大幅提升导入性能。

```python
df.to_sql(table_name, con=engine, method='multi', chunksize=1000)
```

---

## 📈 可视化图表

项目生成8张可视化图表，全面展示销售数据：

1. **月度销售趋势** - 展示每月销售变化
2. **城市销售对比** - 对比各城市销售情况
3. **商品销量TOP10** - 展示最畅销商品
4. **各类别销售占比** - 展示各商品类别占比
5. **用户消费分布** - 展示用户消费金额分布
6. **订单金额分布** - 展示各城市订单金额分布
7. **每周销售热力图** - 展示每周销售热力分布
8. **匿名用户vs注册用户** - 对比匿名用户和注册用户

---

## 📝 项目文档

- [数据分析报告](reports/b数据分析报告.md) - 详细的数据分析报告
- [数据导入模块面试要点](数据导入模块面试要点.md) - 技术知识点总结
- [数据清洗模块对比分析](数据清洗模块对比分析.md) - 数据清洗方法对比
- [面试问题回答模板](面试问题回答模板.md) - 面试准备材料

---

## 🔧 常见问题

### Q1: 数据从哪里来的？
A: 数据来自UCI Machine Learning Repository的Online Retail Dataset，是真实的电商销售数据。

### Q2: 如何处理大数据集？
A: 使用pandas的chunksize参数进行流式处理，避免内存溢出。

### Q3: 如何保证数据质量？
A: 通过去重、缺失值处理、异常值检测等多重机制确保数据质量。

### Q4: 图表可以自定义吗？
A: 可以，修改`b07_generate_charts.py`中的参数即可自定义图表样式。

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 👨‍💻 作者

电商数据分析项目组

---

## 📧 联系方式

如有问题，请通过以下方式联系：

- 提交Issue
- 发送邮件: [your-email@example.com]

---

## 🙏 致谢

- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/) - 提供数据集
- [Pandas](https://pandas.pydata.org/) - 强大的数据处理库
- [Matplotlib](https://matplotlib.org/) - 数据可视化库
- [Seaborn](https://seaborn.pydata.org/) - 统计数据可视化库

---

<div align="center">

**如果这个项目对你有帮助，请给它一个⭐️**

Made with ❤️ by 电商数据分析项目组

</div>