"""
电商销售数据导入模块 - MySQL数据库导入
功能：分批读取CSV文件、数据预处理、批量导入MySQL、数据验证
作者：电商数据分析项目
日期：2026-03-03
"""
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class MySQLDataImporter:
 """MySQL数据导入器"""
    def __init__(self, env_file =' ../env'):
        """
        初始化导入器
        Args:
            env_file: 环境变量配置文件路径
        """
        # 加载环境变量,从文件到系统
        load_dotenv(env_file)

        # 数据库配置，从系统到内存
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'ecommerce_analysis'),
            'charset': os.getenv('DB_CHARSET', 'utf8mb4')
        }

        # 导入配置
        self.chunk_size = int(os.getenv('DB_CHUNK_SIZE', 100000))
        self.batch_size = int(os.getenv('BATCH_SIZE', 1000))

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
            'failed_batches': 0,
            'total_amount': 0,
            'unique_orders': 0,
            'unique_customers': 0
        }

    def create_connection(self):
        """创建数据库连接"""
        print("\n" + "=" * 60)
        print("步骤1: 建立数据库连接")
        print("=" * 60)

        try:
            self.engine = create_engine(
                self.connection_string,
                pool_size = 5,# 连接池大小
                max_overflow = 10, # 最大溢出连接数
                pool_pre_ping = True,# 自动检测连接有效性
                pool_recycle = 3600,# 连接回收时间（1小时）
                echo = False,# 不打印SQL语句
            )

            # 测试连接
            with self.engine.connect() as conn:
                result = conn.execute(text("SHOW VERSION()"))
                version = result.fetchone()[0]
                print(f" 数据库连接成功!")
                print(f" MySQL版本: {version}")
                print(f" 数据库: {self.db_config['database']}")
                print(f" 主机: {self.db_config['host']}:{self.db_config['port']}")

            return True

        except Exception as e:
            print(f" 数据库连接失败: {str(e)}")
            print("\n 请检查:")
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
        # 1. 处理CustomerID：NULL
        if 'CustomerID' in chunk.columns:
            chunk['CustomerID'] = chunk['CustomerID'].astype(str)

        # 检查文件是否存在
        if not os.path.exists(csv_path):
            print(f"❌ 文件不存在: {csv_path}")
            return None

        print(f"📁 文件路径: {csv_path}")
        print(f"📦 分块大小: {self.chunk_size:,} 行/块")

        # 分批读取并合并
        total_rows = 0

        try:
            for i,chunk in enumerate(pd.read_csv(csv_path,encoding = 'latin1', chunksize=self.chunk_size), 1):

                total_rows += len(chunk)
                chunk.to_sql()
                print(f"   已读取块 {i}: {len(chunk):,} 行")

                df = pd.concat(chunks, ignore_index=True)



