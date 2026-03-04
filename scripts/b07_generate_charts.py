"""
电商销售数据可视化脚本
功能：生成8张可视化图表，全面展示销售数据
作者：电商数据分析项目
日期：2026-03-03
"""

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
import os

# 设置图表样式
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 6)

# 设置中文字体（必须在seaborn之后设置）
import matplotlib.font_manager as fm

# 获取字体路径
font_path = None
for font in fm.fontManager.ttflist:
    if font.name == 'Microsoft YaHei':
        font_path = font.fname
        break

if font_path:
    # 添加字体到matplotlib
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
    print(f"✅ 中文字体已加载: {font_prop.get_name()}")
else:
    print("⚠️ 未找到Microsoft YaHei字体，使用备用字体")
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']

plt.rcParams['axes.unicode_minus'] = False

# 强制seaborn使用中文字体
sns.set(font=font_prop.get_name() if font_path else 'SimHei')

# 确保charts目录存在
os.makedirs('charts', exist_ok=True)

print("=" * 60)
print("📊 开始生成可视化图表")
print("=" * 60)

# 读取数据
print("\n📁 读取数据...")
df = pd.read_csv('data/ecommerce_orders_clean.csv', encoding='latin1', low_memory=False)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
print(f"✅ 数据加载成功: {len(df)} 条记录")

# ============================================
# 图表1: 月度销售趋势
# ============================================
print("\n📈 生成图表1: 月度销售趋势...")
# 先提取年月列
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
monthly_sales = df.groupby(['Year', 'Month'])['TotalAmount'].sum().reset_index()
monthly_sales.columns = ['year', 'month', 'total_sales']
monthly_sales['date_label'] = monthly_sales['year'].astype(str) + '-' + monthly_sales['month'].astype(str).str.zfill(2)

plt.figure(figsize=(14, 6))
plt.plot(range(len(monthly_sales)), monthly_sales['total_sales'], marker='o', linewidth=2, markersize=8, color='#2E86AB')
plt.title('月度销售趋势', fontsize=16, fontweight='bold')
plt.xlabel('月份', fontsize=12)
plt.ylabel('销售额(£)', fontsize=12)
plt.xticks(range(len(monthly_sales)), monthly_sales['date_label'], rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('charts/b图表1_月度销售趋势.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 图表1保存成功")

# ============================================
# 图表2: 城市销售对比
# ============================================
print("📊 生成图表2: 城市销售对比...")
city_sales = df.groupby('Country')['TotalAmount'].agg(['sum', 'count', 'mean']).reset_index()
city_sales.columns = ['city', 'total_sales', 'order_count', 'avg_order_value']
city_sales = city_sales.sort_values('total_sales', ascending=False).head(15)

plt.figure(figsize=(14, 6))
colors = plt.cm.viridis(np.linspace(0, 1, len(city_sales)))
bars = plt.bar(city_sales['city'], city_sales['total_sales'], color=colors)
plt.title('各城市销售对比（TOP15）', fontsize=16, fontweight='bold')
plt.xlabel('城市', fontsize=12)
plt.ylabel('销售额(£)', fontsize=12)
plt.xticks(rotation=45, ha='right')
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height/10000:.1f}万',
             ha='center', va='bottom', fontsize=9)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('charts/b图表2_城市销售对比.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 图表2保存成功")

# ============================================
# 图表3: 商品销量TOP10
# ============================================
print("🏆 生成图表3: 商品销量TOP10...")
product_sales = df.groupby(['StockCode', 'Description'])['TotalAmount'].agg(['sum', 'count']).reset_index()
product_sales.columns = ['StockCode', 'Description', 'total_sales', 'order_count']
product_sales = product_sales.sort_values('total_sales', ascending=False).head(10)
product_sales['short_desc'] = product_sales['Description'].str[:20] + '...'

plt.figure(figsize=(14, 6))
colors = plt.cm.plasma(np.linspace(0, 1, len(product_sales)))
bars = plt.barh(range(len(product_sales)), product_sales['total_sales'], color=colors)
plt.yticks(range(len(product_sales)), product_sales['short_desc'])
plt.title('商品销售额TOP10', fontsize=16, fontweight='bold')
plt.xlabel('销售额(£)', fontsize=12)
plt.gca().invert_yaxis()
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2.,
             f'{width/10000:.1f}万',
             ha='left', va='center', fontsize=9)
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('charts/b图表3_商品销量TOP10.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 图表3保存成功")

# ============================================
# 图表4: 各类别销售占比
# ============================================
print("🥧 生成图表4: 各类别销售占比...")
# 根据描述字段简单分类
def categorize_product(desc):
    desc = str(desc).upper()
    if any(x in desc for x in ['PACK', 'BOX', 'BAG', 'SET']):
        return '包装类'
    elif any(x in desc for x in ['HEART', 'HOLDER', 'SIGN', 'DECORATION']):
        return '装饰类'
    elif any(x in desc for x in ['TIN', 'JUG', 'CUP', 'MUG', 'GLASS']):
        return '容器类'
    elif any(x in desc for x in ['CAKE', 'CHOCOLATE', 'BISCUIT', 'CANDY']):
        return '食品类'
    elif any(x in desc for x in ['CHRISTMAS', 'XMAS', 'SNOWMAN', 'TREE']):
        return '节日类'
    else:
        return '其他'

df['category'] = df['Description'].apply(categorize_product)
category_sales = df.groupby('category')['TotalAmount'].sum().reset_index()
category_sales.columns = ['category', 'total_sales']  # 重命名列
category_sales = category_sales.sort_values('total_sales', ascending=False)

plt.figure(figsize=(10, 10))
colors = plt.cm.Set3(np.linspace(0, 1, len(category_sales)))
wedges, texts, autotexts = plt.pie(category_sales['total_sales'], labels=category_sales['category'],
                                    autopct='%1.1f%%', startangle=90, colors=colors,
                                    textprops={'fontsize': 12})
plt.title('各类别销售占比', fontsize=16, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.savefig('charts/b图表4_各类别销售占比.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 图表4保存成功")

# ============================================
# 图表5: 用户消费分布
# ============================================
print("👥 生成图表5: 用户消费分布...")
user_spending = df.groupby('CustomerID')['TotalAmount'].sum().reset_index()
user_spending = user_spending[user_spending['TotalAmount'] > 0]

plt.figure(figsize=(12, 6))
plt.hist(user_spending['TotalAmount'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
plt.title('用户消费分布', fontsize=16, fontweight='bold')
plt.xlabel('消费金额(£)', fontsize=12)
plt.ylabel('用户数量', fontsize=12)
mean_val = user_spending['TotalAmount'].mean()
median_val = user_spending['TotalAmount'].median()
plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'平均值: £{mean_val:.2f}')
plt.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'中位数: £{median_val:.2f}')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('charts/b图表5_用户消费分布.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 图表5保存成功")

# ============================================
# 图表6: 订单金额分布
# ============================================
print("💰 生成图表6: 订单金额分布...")
top_cities = df.groupby('Country')['TotalAmount'].sum().nlargest(10).index
city_data = df[df['Country'].isin(top_cities)]

plt.figure(figsize=(14, 6))
box_data = [city_data[city_data['Country'] == city]['TotalAmount'].values for city in top_cities]
bp = plt.boxplot(box_data, tick_labels=top_cities, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('lightblue')
plt.title('各城市订单金额分布（TOP10）', fontsize=16, fontweight='bold')
plt.xlabel('城市', fontsize=12)
plt.ylabel('订单金额(£)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('charts/b图表6_订单金额分布.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 图表6保存成功")

# ============================================
# 图表7: 每周销售热力图
# ============================================
print("🔥 生成图表7: 每周销售热力图...")
df['weekday'] = df['InvoiceDate'].dt.dayofweek
df['week'] = df['InvoiceDate'].dt.isocalendar().week.astype(int)

weekly_sales = df.groupby(['week', 'weekday'])['TotalAmount'].sum().reset_index()
weekly_pivot = weekly_sales.pivot(index='week', columns='weekday', values='TotalAmount')

weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
if len(weekly_pivot.columns) == 6:
    weekday_names = weekday_names[:6]
weekly_pivot.columns = weekday_names

plt.figure(figsize=(14, 20))
sns.heatmap(weekly_pivot, annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': '销售额(£)'})
plt.title('每周销售热力图', fontsize=16, fontweight='bold')
plt.xlabel('星期', fontsize=12)
plt.ylabel('周数', fontsize=12)
plt.tight_layout()
plt.savefig('charts/b图表7_每周销售热力图.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 图表7保存成功")

# ============================================
# 图表8: 匿名用户vs注册用户对比
# ============================================
print("👤 生成图表8: 匿名用户vs注册用户对比...")
user_type_sales = df.groupby('IsAnonymous').agg({
    'TotalAmount': ['sum', 'count', 'mean']
}).reset_index()
user_type_sales.columns = ['IsAnonymous', 'total_sales', 'order_count', 'avg_order_value']
user_type_sales['user_type'] = user_type_sales['IsAnonymous'].map({0: '注册用户', 1: '匿名用户'})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 子图1: 订单数量
bars1 = ax1.bar(user_type_sales['user_type'], user_type_sales['order_count'], color=['#4ECDC4', '#FF6B6B'])
ax1.set_title('用户类型订单数量', fontsize=14, fontweight='bold')
ax1.set_xlabel('用户类型', fontsize=12)
ax1.set_ylabel('订单数量', fontsize=12)
for i, v in enumerate(user_type_sales['order_count']):
    ax1.text(i, v, f'{v:,}', ha='center', va='bottom', fontsize=10)

# 子图2: 销售额
bars2 = ax2.bar(user_type_sales['user_type'], user_type_sales['total_sales'], color=['#4ECDC4', '#FF6B6B'])
ax2.set_title('用户类型销售额', fontsize=14, fontweight='bold')
ax2.set_xlabel('用户类型', fontsize=12)
ax2.set_ylabel('销售额(£)', fontsize=12)
for i, v in enumerate(user_type_sales['total_sales']):
    ax2.text(i, v, f'£{v/10000:.1f}万', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('charts/b图表8_匿名用户vs注册用户.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ 图表8保存成功")

print("\n" + "=" * 60)
print("🎉 所有图表生成完成!")
print("=" * 60)
print(f"图表保存位置: charts/")
print(f"生成的图表数量: 8张")
print("\n图表列表:")
print("1. b图表1_月度销售趋势.png")
print("2. b图表2_城市销售对比.png")
print("3. b图表3_商品销量TOP10.png")
print("4. b图表4_各类别销售占比.png")
print("5. b图表5_用户消费分布.png")
print("6. b图表6_订单金额分布.png")
print("7. b图表7_每周销售热力图.png")
print("8. b图表8_匿名用户vs注册用户.png")
print("=" * 60)