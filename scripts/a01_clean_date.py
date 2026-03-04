import pandas as pd
import numpy as np

df = pd.read_csv('../data/ecommerce_orders.csv', encoding='latin1')

print("=" *50)
print("数据概览")
print("=" * 50)
print(f"原始数据量：{len(df)}条")
# 查看数据形状（行数、列数）
print("查看数据形状")
print(df.shape)            # (行数, 列数)
print(f"\n数据字段：{df.columns.tolist()}")
print(f"\n前5行数据:")
print(df.head())
print(f"\n数据类型:")
print(df.dtypes)
# 数值型列的统计信息
print(f"\n数据统计信息:")
print(df.describe())
# 查看数据信息（内存使用、非空值数量等
print(df.info())
# 数据清洗步骤

print("\n" + "=" * 50)
print("开始数据清洗")
print("=" * 50)

# 1. 去除重复数据
# 模式2: 查看重复数据 → 决定是否删除

# 1. 查看重复数据
# keep=False 表示标记所有重复项（包括第一次出现的）
duplicates = df[df.duplicated(keep=False)]
duplicate_count = df.duplicated().sum()
print(f"发现 {duplicate_count} 条重复数据（仅计算重复的部分）")
print(f"总共 {len(duplicates)} 条记录涉及重复")

if len(duplicates) > 0:
    print("\n重复数据示例:")
    print(duplicates.head(10))
    df = df.drop_duplicates()
    print("重复数据已删除")
    print(df.shape)
else:
    print("没有发现重复数据")

# # 2. 决定是否删除
# if len(duplicates) > 0 and input("\n是否删除重复数据（保留第一次出现）? (y/n): ") == 'y':
#     df = df.drop_duplicates()
#     print(f"删除后剩余数据量：{len(df)}条")
# else:
#     print("保留所有数据")


# 2. 检查并处理缺失值
print(f"每列的缺失值数量:{df.isnull().sum()}")
missing_ratio = df.isnull().sum() / len(df)
print(f"缺失值比例{missing_ratio}")

print("\n" + "=" * 50)
# 删除关键字段的缺失值
"""关键字段（必填）：
   - 订单ID、用户ID、商品ID等
   -  删除：这类字段缺失无法恢复，直接删除整行
   重要业务字段：
   - 订单金额、数量、单价、时间等
   -  优先删除：缺失影响分析准确性
   - 或者根据其他字段计算推导（如：金额 = 数量 × 单价）
   辅助字段：
   - 收货地址、备注、优惠信息等
   -  填充默认值：如地址填"未知"，备注填"无"
   -  保留缺失：某些分析可能不需要这些字段"""
# df = df.dropna(subset=['CustomerID'])
print(df.shape)

# 填充
df = df.fillna({'Description':'unknow','CustomerID':'匿名'})
# 3. 数据类型转换
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['CustomerID'] = df['CustomerID'].astype(str)
# 4. 数据验证和清理

# 删除负数数量（退货记录）
df = df[df['Quantity']>0]
# 删除负数单价
df = df[df['UnitPrice']>0]
# 删除数量为0的记录
# 5. 计算订单金额
df['TotalAmount'] = df['UnitPrice']*df['Quantity']
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
# 6. 重命名字段（统一字段名，方便后续分析）
# 只重命名存在的字段
# 7. 添加一些衍生字段
# 8. 数据质量检查
# 9. 保存清洗后的数据
df.to_csv('../data/ecommerce_orders_clean.csv', index=False)