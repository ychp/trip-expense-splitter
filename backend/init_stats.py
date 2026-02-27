#!/usr/bin/env python3
"""
初始化统计表 - 为现有行程数据生成统计记录
运行方式: python3 init_stats.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.models.trip import Trip
from app.services.stats_service import StatsService


def init_all_stats():
    """为所有现有行程生成统计数据"""
    db: Session = SessionLocal()
    try:
        print("🔍 开始查找现有行程...")
        
        # 获取所有行程
        trips = db.query(Trip).all()
        
        if not trips:
            print("❌ 数据库中没有行程数据")
            return
        
        print(f"✅ 找到 {len(trips)} 个行程")
        
        success_count = 0
        failed_count = 0
        
        for trip in trips:
            print(f"\n📊 正在处理行程: {trip.name} (ID: {trip.id})")
            try:
                StatsService.update_all_stats(trip.id, db)
                print(f"✅ 行程 {trip.name} 统计数据生成成功")
                success_count += 1
            except Exception as e:
                print(f"❌ 行程 {trip.name} 统计数据生成失败: {e}")
                failed_count += 1
        
        print(f"\n{'='*50}")
        print(f"📈 初始化完成")
        print(f"✅ 成功: {success_count} 个行程")
        print(f"❌ 失败: {failed_count} 个行程")
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_all_stats()
