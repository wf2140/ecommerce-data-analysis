"""
电商销售数据清洗模块 - 高级版本
功能：数据探索、重复处理、缺失值填充、异常值检测、数据转换、质量报告
"""

import pandas as pd
import numpy as np
from datetime import datetime


class EcommerceDataCleaner:
    """电商数据清洗类"""

    def __init__(self, file_path, encoding='latin1'):
        """初始化数据清洗器"""
        self.file_path = file_path
        self.encoding = encoding
        self.df = None
        self.cleaning_report = {
            'original_count': 0,
            'duplicates_removed': 0,
            'negative_quantity_removed': 0,
            'negative_price_removed': 0,
            'final_count': 0,
            'missing_filled': 0,
            'cleaning_steps': []
        }

    def load_data(self):
        """加载数据"""
        print("\n" + "="*60)
        print("📊 步骤1: 加载数据")
        print("="*60)
        self.df = pd.read_csv(self.file_path, encoding=self.encoding)
        self.cleaning_report['original_count'] = len(self.df)
        print(f"✅ 数据加载成功: {len(self.df)} 条记录")
        print(f"📋 字段列表: {self.df.columns.tolist()}")
        return self.df

    def data_exploration(self):
        """数据探索分析"""
        print("\n" + "="*60)
        print("🔍 步骤2: 数据探索")
        print("="*60)

        # 基本统计
        print(f"数据形状: {self.df.shape}")
        print(f"\n数据类型:\n{self.df.dtypes}")

        # 缺失值分析
        missing_count = self.df.isnull().sum()
        missing_ratio = (missing_count / len(self.df) * 100).round(2)
        missing_df = pd.DataFrame({
            '缺失数量': missing_count,
            '缺失比例(%)': missing_ratio
        })
        print(f"\n缺失值分析:\n{missing_df[missing_df['缺失数量'] > 0]}")

        # 数值统计
        print(f"\n数值统计:\n{self.df.describe()}")

    def handle_duplicates(self):
        """处理重复数据"""
        print("\n" + "="*60)
        print("🔄 步骤3: 处理重复数据")
        print("="*60)

        # 检查完全重复的行
        duplicates = self.df[self.df.duplicated(keep=False)]
        duplicate_count = self.df.duplicated().sum()

        # 检查主键重复（基于 InvoiceNo 和 StockCode）
        pk_duplicates = self.df[self.df.duplicated(subset=['InvoiceNo', 'StockCode'], keep=False)]
        pk_duplicate_count = self.df.duplicated(subset=['InvoiceNo', 'StockCode']).sum()

        if len(pk_duplicates) > 0:
            print(f"⚠️  发现 {len(pk_duplicates)} 条主键重复记录")
            print(f"📌 主键: (InvoiceNo, StockCode)")
            print(f"⚠️  注意：主键重复可能是同一订单中同一商品被记录多次")
            print("\n主键重复记录示例:")
            print(pk_duplicates[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice']].head(5))

            # 删除主键重复数据，保留第一次出现
            self.df = self.df.drop_duplicates(subset=['InvoiceNo', 'StockCode'], keep='first')
            self.cleaning_report['duplicates_removed'] = pk_duplicate_count
            print(f"✅ 已删除主键重复数据，保留 {len(self.df)} 条记录")
        else:
            print("✅ 未发现主键重复数据")

    def handle_missing_values(self):
        """处理缺失值"""
        print("\n" + "="*60)
        print("🔧 步骤4: 处理缺失值")
        print("="*60)

        missing_before = self.df.isnull().sum().sum()

        # 分析各字段缺失情况，制定策略
        if self.df['CustomerID'].isnull().any():
            print(f"⚠️  CustomerID 缺失: {self.df['CustomerID'].isnull().sum()} 条")
            print("💡 策略：保持 NaN，添加 IsAnonymous 标识便于分析匿名订单")
            # 在 CustomerID 还是 NaN 的时候创建 IsAnonymous 标识
            self.df['IsAnonymous'] = self.df['CustomerID'].isna().astype(int)

        if self.df['Description'].isnull().any():
            print(f"⚠️  Description 缺失: {self.df['Description'].isnull().sum()} 条")
            print("💡 策略: 填充为 'unknown'，不影响销售分析")
            self.df['Description'] = self.df['Description'].fillna('unknown')

        missing_after = self.df.isnull().sum().sum()
        self.cleaning_report['missing_filled'] = missing_before - missing_after
        print(f"✅ 缺失值处理完成，填充 {self.cleaning_report['missing_filled']} 个")

    def detect_and_remove_outliers(self):
        """检测并移除异常值"""
        print("\n" + "="*60)
        print("🎯 步骤5: 异常值检测与清理")
        print("="*60)

        original_count = len(self.df)

        # 检测负数数量（退货记录）
        negative_qty = (self.df['Quantity'] <= 0).sum()
        if negative_qty > 0:
            print(f"⚠️  检测到 {negative_qty} 条数量<=0的记录（可能是退货）")
            print("💡 策略: 本分析聚焦销售数据，移除退货记录")
            self.df = self.df[self.df['Quantity'] > 0]

        # 检测负数或零单价
        invalid_price = (self.df['UnitPrice'] <= 0).sum()
        if invalid_price > 0:
            print(f"⚠️  检测到 {invalid_price} 条单价<=0的记录")
            print("💡 策略: 移除异常定价记录")
            self.df = self.df[self.df['UnitPrice'] > 0]

        # 高级异常值检测：使用IQR方法检测极端值
        for col in ['Quantity', 'UnitPrice']:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            outliers = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
            if outliers > 0:
                print(f"📊 {col} 极端值检测: {outliers} 条（范围: {lower_bound:.2f} - {upper_bound:.2f}）")
                print(f"💡 策略: 保留但记录，可能包含大额订单或特殊商品")

        self.cleaning_report['negative_quantity_removed'] = negative_qty
        self.cleaning_report['negative_price_removed'] = invalid_price
        print(f"✅ 异常值清理完成，剩余 {len(self.df)} 条记录")

    def transform_data_types(self):
        """数据类型转换"""
        print("\n" + "="*60)
        print("🔄 步骤6: 数据类型转换")
        print("="*60)

        # 转换时间字段
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])
        print("✅ InvoiceDate: str → datetime")

        # CustomerID 保持 NaN，导入时 SQLAlchemy 会自动转换成数据库的 NULL
        print("✅ CustomerID: 保持 NaN（导入时自动转为数据库 NULL）")

        print(f"\n转换后数据类型:\n{self.df.dtypes}")

    def create_derived_features(self):
        """创建衍生特征"""
        print("\n" + "="*60)
        print("✨ 步骤7: 创建衍生特征")
        print("="*60)

        # 计算订单金额
        self.df['TotalAmount'] = self.df['Quantity'] * self.df['UnitPrice']
        print("✅ 创建字段: TotalAmount (订单金额)")

        # 查询唯一用户数和商品数
        print(f"唯一用户数：{self.df['CustomerID'].nunique()}")
        print(f"股票编码数：{self.df['StockCode'].nunique()}")
        print(f"涉及的国家地区数:{self.df['Country'].nunique()}")

        # 时间维度特征
        self.df['Year'] = self.df['InvoiceDate'].dt.year
        self.df['Month'] = self.df['InvoiceDate'].dt.month
        self.df['Day'] = self.df['InvoiceDate'].dt.day
        self.df['Hour'] = self.df['InvoiceDate'].dt.hour
        self.df['Weekday'] = self.df['InvoiceDate'].dt.dayofweek  # 0=周一
        self.df['WeekOfYear'] = self.df['InvoiceDate'].dt.isocalendar().week
        print("✅ 创建字段: Year, Month, Day, Hour, Weekday, WeekOfYear")

        # 业务特征：IsAnonymous 已在 handle_missing_values 中创建
        print("✅ 字段: IsAnonymous (已在步骤4创建)")

    def generate_quality_report(self):
        """生成数据质量报告"""
        print("\n" + "="*60)
        print("📋 数据清洗质量报告")
        print("="*60)

        self.cleaning_report['final_count'] = len(self.df)
        total_removed = self.cleaning_report['original_count'] - self.cleaning_report['final_count']
        removal_rate = round(total_removed / self.cleaning_report['original_count'] * 100, 2)

        print(f"\n📊 数据量变化:")
        print(f"   原始数据: {self.cleaning_report['original_count']:,} 条")
        print(f"   重复数据删除: -{self.cleaning_report['duplicates_removed']:,} 条")
        print(f"   数量异常删除: -{self.cleaning_report['negative_quantity_removed']:,} 条")
        print(f"   价格异常删除: -{self.cleaning_report['negative_price_removed']:,} 条")
        print(f"   清洗后数据: {self.cleaning_report['final_count']:,} 条")
        print(f"   删除比例: {removal_rate}%")

        print(f"\n📋 数据质量指标:")
        print(f"   缺失值填充: {self.cleaning_report['missing_filled']} 个")
        print(f"   当前缺失值: {self.df.isnull().sum().sum()} 个")
        print(f"   数据完整性: {((len(self.df) - self.df.isnull().sum().sum()) / (len(self.df) * len(self.df.columns)) * 100):.2f}%")

        print(f"\n💰 业务指标概览:")
        print(f"   总销售额: ¥{self.df['TotalAmount'].sum():,.2f}")
        print(f"   平均订单金额: ¥{self.df['TotalAmount'].mean():.2f}")
        print(f"   订单数量: {self.df['InvoiceNo'].nunique():,}")
        print(f"   客户数量: {self.df['CustomerID'].nunique():,}")
        print(f"   商品数量: {self.df['StockCode'].nunique():,}")
        print(f"   匿名订单占比: {(self.df['IsAnonymous'].sum() / len(self.df) * 100):.2f}%")

    def save_cleaned_data(self, output_path):
        """保存清洗后的数据"""
        print("\n" + "="*60)
        print("💾 步骤8: 保存清洗数据")
        print("="*60)

        self.df.to_csv(output_path, index=False, encoding='latin1')
        print(f"✅ 数据已保存至: {output_path}")

    def run_cleaning_pipeline(self, output_path='../data/ecommerce_orders_clean.csv'):
        """执行完整的数据清洗流程"""
        print("\n" + "="*60)
        print("🚀 开始电商数据清洗流程")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        try:
            self.load_data()
            self.data_exploration()
            self.handle_duplicates()
            self.handle_missing_values()
            self.detect_and_remove_outliers()
            self.transform_data_types()
            self.create_derived_features()
            self.generate_quality_report()
            self.save_cleaned_data(output_path)

            print("\n" + "="*60)
            print("🎉 数据清洗流程完成!")
            print(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60)

            return self.df

        except Exception as e:
            print(f"\n❌ 数据清洗过程中出现错误: {str(e)}")
            raise


if __name__ == '__main__':
    # 执行数据清洗
    cleaner = EcommerceDataCleaner(
        file_path='../data/ecommerce_orders.csv',
        encoding='latin1'
    )
    cleaned_df = cleaner.run_cleaning_pipeline()
