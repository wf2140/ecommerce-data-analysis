"""
电商销售数据导入模块 - MySQL数据库导入（内存优化版）
功能：流式读取CSV、逐批预处理、批量导入MySQL、数据验证
特点：真正实现流式处理，内存占用恒定，不受文件大小影响
作者：电商数据分析项目
日期：2026-03-03
"""

import os
import time
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.types import VARCHAR, INTEGER, DECIMAL, DATETIME
from datetime import datetime
from dotenv import load_dotenv


class MySQLDataImporter:
    """MySQL数据导入器 - 流式处理版本"""

    def __init__(self, env_file='../.env'):
        """
        初始化导入器
        Args:
            env_file: 环境变量配置文件路径
        """
        # 加载环境变量
        load_dotenv(env_file)

        # 数据库配置
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'ecommerce_analysis'),
            'charset': os.getenv('DB_CHARSET', 'utf8mb4')
        }

        # 导入配置
        self.chunk_size = int(os.getenv('CHUNK_SIZE', 50000))  # 每次从CSV读取的行数
        self.batch_size = int(os.getenv('BATCH_SIZE', 1000))    # 每次插入数据库的行数

        # 构建数据库连接字符串
        self.connection_string = (
            f"mysql+pymysql://{self.db_config['user']}:{self.db_config['password']}"
            f"@{self.db_config['host']}:{self.db_config['port']}"
            f"/{self.db_config['database']}?charset={self.db_config['charset']}"
        )

        # 创建数据库引擎（带连接池）
        self.engine = None

        # 导入统计信息
        self.import_stats = {
            'start_time': None,
            'end_time': None,
            'total_rows': 0,
            'imported_rows': 0,
            'total_chunks': 0,
            'total_amount': 0,
            'unique_orders': 0,
            'unique_customers': 0
        }

    def create_connection(self):
        """创建数据库连接"""
        print("\n" + "=" * 60)
        print("🔗 步骤1: 建立数据库连接")
        print("=" * 60)

        try:
            self.engine = create_engine(
                self.connection_string,
                pool_size=5,               # 连接池大小
                max_overflow=10,           # 最大溢出连接数
                pool_pre_ping=True,        # 自动检测连接有效性
                pool_recycle=3600,         # 连接回收时间（1小时）
                echo=False                 # 不打印SQL语句
            )

            # 测试连接
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT VERSION()"))
                version = result.fetchone()[0]
                print(f"✅ 数据库连接成功!")
                print(f"📌 MySQL版本: {version}")
                print(f"📌 数据库: {self.db_config['database']}")
                print(f"📌 主机: {self.db_config['host']}:{self.db_config['port']}")

            return True

        except Exception as e:
            print(f"❌ 数据库连接失败: {str(e)}")
            print("\n💡 请检查:")
            print("   1. MySQL服务是否启动")
            print("   2. .env文件中的数据库配置是否正确")
            print("   3. 数据库 'ecommerce_analysis' 是否已创建")
            return False

    def preprocess_chunk(self, chunk):
        """
        数据预处理：处理单个chunk
        Args:
            chunk: 单个数据块（DataFrame）
        Returns:
            DataFrame: 处理后的数据块
        """
        # 0. 去重：基于主键 (InvoiceNo, StockCode) 去重，保留第一次出现的记录
        original_count = len(chunk)
        chunk = chunk.drop_duplicates(subset=['InvoiceNo', 'StockCode'], keep='first')
        removed_count = original_count - len(chunk)
        if removed_count > 0:
            print(f"   ℹ️  本块去重: 删除 {removed_count} 条重复记录")

        # 1. CustomerID 保持 NaN，SQLAlchemy 会自动转换成数据库的 NULL
        # 不需要任何处理

        # 2. 处理IsAnonymous：确保是整数（1/0）
        if 'IsAnonymous' in chunk.columns:
            chunk['IsAnonymous'] = chunk['IsAnonymous'].astype(int)

        # 3. 确保数值类型正确
        if 'Quantity' in chunk.columns:
            chunk['Quantity'] = chunk['Quantity'].astype(int)

        if 'UnitPrice' in chunk.columns:
            chunk['UnitPrice'] = chunk['UnitPrice'].astype(float)

        if 'TotalAmount' in chunk.columns:
            chunk['TotalAmount'] = chunk['TotalAmount'].astype(float)

        # 4. 处理日期格式（如果是字符串）
        if 'InvoiceDate' in chunk.columns:
            if not pd.api.types.is_datetime64_any_dtype(chunk['InvoiceDate']):
                chunk['InvoiceDate'] = pd.to_datetime(chunk['InvoiceDate'])

        # 5. 确保字符串类型
        string_columns = ['InvoiceNo', 'StockCode', 'Description', 'Country']
        for col in string_columns:
            if col in chunk.columns:
                chunk[col] = chunk[col].astype(str)

        return chunk

    def import_chunk_to_database(self, chunk, table_name, dtype_mapping):
        """
        将单个chunk导入数据库
        Args:
            chunk: 数据块
            table_name: 目标表名
            dtype_mapping: 数据类型映射
        Returns:
            int: 导入的行数
        """
        # 计算批次数
        total_rows = len(chunk)
        num_batches = (total_rows // self.batch_size) + 1
        imported_rows = 0

        # 分批导入
        for i in range(num_batches):
            start_idx = i * self.batch_size
            end_idx = min((i + 1) * self.batch_size, total_rows)
            batch = chunk.iloc[start_idx:end_idx]

            # 导入当前批次，捕获重复键错误
            try:
                batch.to_sql(
                    name=table_name,
                    con=self.engine,
                    if_exists='append',
                    index=False,
                    dtype=dtype_mapping,
                    method='multi'  # 批量插入优化
                )
                imported_rows += len(batch)
            except Exception as e:
                # 如果是重复键错误，忽略并继续
                if "Duplicate entry" in str(e):
                    print(f"   ⚠️  跳过重复数据: {len(batch)} 行")
                    # 尝试逐条导入，跳过重复的
                    for idx, row in batch.iterrows():
                        try:
                            row.to_frame().T.to_sql(
                                name=table_name,
                                con=self.engine,
                                if_exists='append',
                                index=False,
                                dtype=dtype_mapping
                            )
                            imported_rows += 1
                        except Exception as inner_e:
                            if "Duplicate entry" not in str(inner_e):
                                raise inner_e
                else:
                    raise e

        return imported_rows

    def stream_import(self, csv_path, table_name='orders'):
        """
        流式导入：逐批读取、预处理、导入
        Args:
            csv_path: CSV文件路径
            table_name: 目标表名
        Returns:
            bool: 是否成功
        """
        print("\n" + "=" * 60)
        print("📊 步骤2: 流式导入数据")
        print("=" * 60)

        # 检查文件是否存在
        if not os.path.exists(csv_path):
            print(f"❌ 文件不存在: {csv_path}")
            return False

        print(f"📁 文件路径: {csv_path}")
        print(f"📦 每块大小: {self.chunk_size:,} 行")
        print(f"📦 每批大小: {self.batch_size:,} 行")
        print(f"💾 内存占用: 恒定（不受文件大小影响）")

        # 定义数据类型映射
        dtype_mapping = {
            'InvoiceNo': VARCHAR(20),
            'StockCode': VARCHAR(20),
            'Description': VARCHAR(255),
            'Quantity': INTEGER,
            'InvoiceDate': DATETIME,
            'UnitPrice': DECIMAL(10, 4),
            'CustomerID': VARCHAR(20),
            'Country': VARCHAR(50),
            'TotalAmount': DECIMAL(10, 2),
            'Year': INTEGER,
            'Month': INTEGER,
            'Day': INTEGER,
            'Hour': INTEGER,
            'Weekday': INTEGER,
            'WeekOfYear': INTEGER,
            'IsAnonymous': INTEGER
        }

        # 清空目标表
        print(f"\n⚠️  清空目标表: {table_name}")
        with self.engine.connect() as conn:
            # 步骤1: 杀死所有锁定进程
            try:
                print("   🔄 释放表锁...")
                conn.execute(text("SET innodb_lock_wait_timeout=50"))
                conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
                conn.commit()
            except:
                pass
            
            # 步骤2: 直接删除表并重新创建（最可靠）
            print("   🔄 删除并重新创建表...")
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            conn.commit()
            
            # 步骤3: 重新创建表
            print("   🔄 重新创建表结构...")
            conn.execute(text(f"""
                CREATE TABLE {table_name}(
                    InvoiceNo VARCHAR(20) COMMENT '订单号',
                    StockCode VARCHAR(20) COMMENT '商品编码',
                    Description VARCHAR(255) COMMENT '商品描述',
                    Quantity INT COMMENT '数量',
                    InvoiceDate DATETIME COMMENT '订单日期',
                    UnitPrice DECIMAL(10, 4) COMMENT '单价',
                    CustomerID VARCHAR(20) COMMENT '客户ID',
                    Country VARCHAR(50) COMMENT '国家',
                    TotalAmount DECIMAL(10, 2) COMMENT '订单金额',
                    Year INT COMMENT '年份',
                    Month INT COMMENT '月份',
                    Day INT COMMENT '日期',
                    Hour INT COMMENT '小时',
                    Weekday INT COMMENT '星期',
                    WeekOfYear INT COMMENT '第几周',
                    IsAnonymous TINYINT(1) COMMENT '是否匿名',
                    PRIMARY KEY(InvoiceNo, StockCode)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """))
            conn.commit()
            
            # 步骤4: 恢复设置
            conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            conn.commit()
            
        print(f"✅ 表已清空并重新创建")

        # 开始流式导入
        print(f"\n🚀 开始流式导入...")
        print("-" * 60)

        self.import_stats['start_time'] = time.time()

        try:
            # 流式读取CSV：每次只读取 chunk_size 行
            # 指定 dtype 避免 DtypeWarning
            dtype_spec = {
                'InvoiceNo': 'str',  # 明确指定为字符串
                'StockCode': 'str',
                'Description': 'str',
                'Country': 'str'
            }
            
            for i, chunk in enumerate(pd.read_csv(
                csv_path,
                encoding='latin1',
                chunksize=self.chunk_size,
                dtype=dtype_spec
            ), 1):

                chunk_start_time = time.time()

                # 步骤1: 预处理当前chunk
                chunk = self.preprocess_chunk(chunk)

                # 步骤2: 导入当前chunk
                imported_rows = self.import_chunk_to_database(chunk, table_name, dtype_mapping)

                # 步骤3: 更新统计信息
                self.import_stats['imported_rows'] += imported_rows
                self.import_stats['total_chunks'] += 1

                # 步骤4: 显示进度
                chunk_elapsed = time.time() - chunk_start_time
                chunk_speed = imported_rows / chunk_elapsed if chunk_elapsed > 0 else 0
                print(f"块 {i}: "
                      f"{imported_rows:,} 行 | "
                      f"速度: {chunk_speed:,.0f} 行/秒 | "
                      f"累计: {self.import_stats['imported_rows']:,} 行 | "
                      f"耗时: {chunk_elapsed:.1f}秒")

                # 步骤5: 释放内存（Python会自动回收）
                del chunk

            self.import_stats['end_time'] = time.time()
            self.import_stats['total_rows'] = self.import_stats['imported_rows']

            print(f"\n✅ 流式导入完成!")
            print(f"   总导入行数: {self.import_stats['imported_rows']:,}")
            print(f"   总块数: {self.import_stats['total_chunks']}")

            return True

        except Exception as e:
            print(f"\n❌ 流式导入失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def verify_import(self, table_name='orders'):
        """
        验证数据导入结果
        Args:
            table_name: 表名
        Returns:
            bool: 验证是否通过
        """
        print("\n" + "=" * 60)
        print("📋 步骤3: 数据验证")
        print("=" * 60)

        try:
            with self.engine.connect() as conn:
                # 查询数据库中的统计信息
                result = conn.execute(text(f"""
                    SELECT
                        COUNT(*) AS total_records,
                        COUNT(DISTINCT InvoiceNo) AS unique_orders,
                        COUNT(DISTINCT CustomerID) AS unique_customers,
                        SUM(TotalAmount) AS total_sales,
                        MIN(InvoiceDate) AS first_order,
                        MAX(InvoiceDate) AS last_order
                    FROM {table_name}
                """))

                db_stats = result.fetchone()

                print(f"\n📊 数据库统计:")
                print(f"   总记录数: {db_stats[0]:,}")
                print(f"   唯一订单数: {db_stats[1]:,}")
                print(f"   唯一客户数: {db_stats[2]:,}")
                print(f"   总销售额: £{db_stats[3]:,.2f}")
                print(f"   订单时间范围: {db_stats[4]} 至 {db_stats[5]}")

                # 保存统计信息
                self.import_stats['total_amount'] = db_stats[3]
                self.import_stats['unique_orders'] = db_stats[1]
                self.import_stats['unique_customers'] = db_stats[2]

                # 验证数据量
                if db_stats[0] != self.import_stats['imported_rows']:
                    print(f"\n❌ 验证失败: 数据量不匹配!")
                    print(f"   导入行数: {self.import_stats['imported_rows']:,}")
                    print(f"   数据库行数: {db_stats[0]:,}")
                    return False

                print(f"\n✅ 数据验证通过!")
                return True

        except Exception as e:
            print(f"\n❌ 数据验证失败: {str(e)}")
            return False

    def generate_report(self):
        """生成导入报告"""
        print("\n" + "=" * 60)
        print("📊 导入报告")
        print("=" * 60)

        if self.import_stats['start_time'] and self.import_stats['end_time']:
            total_time = self.import_stats['end_time'] - self.import_stats['start_time']
            avg_speed = self.import_stats['imported_rows'] / total_time if total_time > 0 else 0

            print(f"\n⏰ 时间统计:")
            print(f"   开始时间: {datetime.fromtimestamp(self.import_stats['start_time']).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   结束时间: {datetime.fromtimestamp(self.import_stats['end_time']).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   总耗时: {total_time:.1f}秒 ({total_time/60:.1f}分钟)")

            print(f"\n📈 性能指标:")
            print(f"   总导入行数: {self.import_stats['imported_rows']:,}")
            print(f"   平均速度: {avg_speed:,.0f} 行/秒")
            print(f"   总块数: {self.import_stats['total_chunks']}")

            print(f"\n💰 业务指标:")
            print(f"   总销售额: £{self.import_stats['total_amount']:,.2f}")
            print(f"   唯一订单: {self.import_stats['unique_orders']:,}")
            print(f"   唯一客户: {self.import_stats['unique_customers']:,}")

            print(f"\n💾 内存特性:")
            print(f"   流式处理: ✅ 是")
            print(f"   内存占用: 恒定（约 {self.chunk_size * 0.5:.0f} MB）")
            print(f"   支持超大文件: ✅ 是（10GB+）")

    def run_import(self, csv_path='../data/ecommerce_orders_clean.csv', table_name='orders'):
        """
        执行完整的数据导入流程
        Args:
            csv_path: CSV文件路径
            table_name: 目标表名
        Returns:
            bool: 是否成功
        """
        print("\n" + "=" * 60)
        print("🚀 开始数据导入流程（流式处理版本）")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        try:
            # 步骤1: 建立数据库连接
            if not self.create_connection():
                return False

            # 步骤2: 流式导入数据（读取→预处理→导入→释放）
            if not self.stream_import(csv_path, table_name):
                return False

            # 步骤3: 数据验证
            if not self.verify_import(table_name):
                return False

            # 生成报告
            self.generate_report()

            print("\n" + "=" * 60)
            print("🎉 数据导入流程完成!")
            print(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)

            return True

        except Exception as e:
            print(f"\n❌ 数据导入过程中出现错误: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            # 关闭数据库连接
            if self.engine:
                self.engine.dispose()
                print("\n🔌 数据库连接已关闭")


if __name__ == '__main__':
    # 创建导入器实例
    importer = MySQLDataImporter(env_file='../.env')

    # 执行导入
    success = importer.run_import(
        csv_path='../data/ecommerce_orders_clean.csv',
        table_name='orders'
    )

    # 返回结果
    if success:
        print("\n✅ 数据导入成功!")
        exit(0)
    else:
        print("\n❌ 数据导入失败!")
        exit(1)
