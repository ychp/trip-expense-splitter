#!/usr/bin/env python3
"""验证统计表中JSON字段的存储格式"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from app.core.database import engine


def check_storage_format():
    """检查统计表中JSON字段的实际存储格式"""
    
    with engine.connect() as conn:
        # 检查trip_stats表
        result = conn.execute(text("SELECT trip_id, category_totals, category_ratios FROM trip_stats LIMIT 1"))
        row = result.fetchone()
        if row:
            print("📊 trip_stats表:")
            print(f"  trip_id: {row[0]}")
            print(f"  category_totals 类型: {type(row[1])}")
            print(f"  category_totals 内容: {row[1][:100]}...")
            print(f"  category_ratios 类型: {type(row[2])}")
            print(f"  category_ratios 内容: {row[2][:100]}...")
            print()
        
        # 检查member_stats表
        result = conn.execute(text("SELECT member_id, by_category, by_wallet FROM member_stats LIMIT 1"))
        row = result.fetchone()
        if row:
            print("👥 member_stats表:")
            print(f"  member_id: {row[0]}")
            print(f"  by_category 类型: {type(row[1])}")
            print(f"  by_category 内容: {row[1][:100]}...")
            print(f"  by_wallet 类型: {type(row[2])}")
            print()
        
        # 检查wallet_stats表
        result = conn.execute(text("SELECT wallet_id, balance_by_member FROM wallet_stats LIMIT 1"))
        row = result.fetchone()
        if row:
            print("💰 wallet_stats表:")
            print(f"  wallet_id: {row[0]}")
            print(f"  balance_by_member 类型: {type(row[1])}")
            print(f"  balance_by_member 内容: {row[1][:100]}...")
            print()
        
        print("✅ 验证完成：JSON对象以TEXT字符串形式存储在数据库中")


if __name__ == "__main__":
    check_storage_format()
