#!/usr/bin/env python3
"""
创建统计表的迁移脚本（无外键约束版本）
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from app.core.database import engine


def create_stats_tables():
    """创建统计表（JSON对象以Text字符串存储）"""
    
    sql_statements = [
        # 删除旧表（如果存在）
        "DROP TABLE IF EXISTS wallet_stats",
        "DROP TABLE IF EXISTS member_stats",
        "DROP TABLE IF EXISTS trip_stats",
        
        # 创建trip_stats表
        """
        CREATE TABLE trip_stats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trip_id INT NOT NULL UNIQUE,
            total_expense FLOAT DEFAULT 0.0 COMMENT '总支出',
            average_expense FLOAT DEFAULT 0.0 COMMENT '人均支出',
            member_count INT DEFAULT 0 COMMENT '成员数量',
            category_totals TEXT COMMENT '分类汇总JSON字符串',
            category_ratios TEXT COMMENT '分类占比JSON字符串',
            transaction_count INT DEFAULT 0 COMMENT '交易总数',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_trip_stats_trip_id (trip_id),
            INDEX idx_trip_stats_updated_at (updated_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='行程统计表'
        """,
        
        # 创建member_stats表
        """
        CREATE TABLE member_stats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trip_id INT NOT NULL,
            member_id INT NOT NULL,
            member_name VARCHAR(100) COMMENT '成员名称冗余字段',
            total_amount FLOAT DEFAULT 0.0 COMMENT '总支出',
            by_category TEXT COMMENT '按分类统计JSON字符串',
            by_wallet TEXT COMMENT '按钱包统计JSON字符串',
            should_pay FLOAT DEFAULT 0.0 COMMENT '应付金额（平均值）',
            actual_paid FLOAT DEFAULT 0.0 COMMENT '实际支付金额',
            balance FLOAT DEFAULT 0.0 COMMENT '差额（实际-应付）',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_member_stats_trip_id (trip_id),
            INDEX idx_member_stats_member_id (member_id),
            UNIQUE INDEX idx_member_stats_trip_member (trip_id, member_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='成员统计表'
        """,
        
        # 创建wallet_stats表
        """
        CREATE TABLE wallet_stats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trip_id INT NOT NULL,
            wallet_id INT NOT NULL UNIQUE,
            wallet_name VARCHAR(100) COMMENT '钱包名称冗余字段',
            balance_by_member TEXT COMMENT '成员余额JSON字符串',
            total_balance FLOAT DEFAULT 0.0 COMMENT '总余额',
            transaction_count INT DEFAULT 0 COMMENT '交易数量',
            total_deposited FLOAT DEFAULT 0.0 COMMENT '总存入',
            total_spent FLOAT DEFAULT 0.0 COMMENT '总支出',
            remaining FLOAT DEFAULT 0.0 COMMENT '剩余金额',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_wallet_stats_trip_id (trip_id),
            INDEX idx_wallet_stats_wallet_id (wallet_id),
            INDEX idx_wallet_stats_updated_at (updated_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='钱包统计表'
        """
    ]
    
    with engine.connect() as conn:
        for i, sql in enumerate(sql_statements, 1):
            try:
                conn.execute(text(sql))
                conn.commit()
                print(f"✅ 操作 {i} 执行成功")
            except Exception as e:
                print(f"❌ 操作 {i} 执行失败: {e}")
    
    print("\n✅ 统计表迁移完成")


if __name__ == "__main__":
    create_stats_tables()
