from app.core.database import engine, Base, SessionLocal
from app.models import Category, Trip, Member, Wallet
from datetime import datetime, timedelta


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    existing_categories = db.query(Category).first()
    if not existing_categories:
        default_categories = [
            {"name": "交通费", "type": "expense", "sort_order": 1},
            {"name": "住宿费", "type": "expense", "sort_order": 2},
            {"name": "餐饮费", "type": "expense", "sort_order": 3},
            {"name": "门票费", "type": "expense", "sort_order": 4},
            {"name": "购物费", "type": "expense", "sort_order": 5},
            {"name": "娱乐费", "type": "expense", "sort_order": 6},
            {"name": "其他", "type": "expense", "sort_order": 7},
        ]
        
        for cat_data in default_categories:
            category = Category(**cat_data)
            db.add(category)
        
        db.commit()
        print("✓ 旅行分类已创建")
    
    existing_trips = db.query(Trip).first()
    if not existing_trips:
        start_date = datetime.now() + timedelta(days=7)
        end_date = datetime.now() + timedelta(days=10)
        
        demo_trip = Trip(
            name="示例行程：周末出游",
            description="这是一个示例行程，您可以编辑或删除它",
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            status="planning"
        )
        db.add(demo_trip)
        db.flush()
        
        demo_members = [
            Member(name="张三", trip_id=demo_trip.id),
            Member(name="李四", trip_id=demo_trip.id),
            Member(name="王五", trip_id=demo_trip.id),
        ]
        for member in demo_members:
            db.add(member)
        db.flush()
        
        demo_wallet = Wallet(
            name="公共钱包",
            balance=3000.00,
            trip_id=demo_trip.id,
            ownership={demo_members[0].id: 0.4, demo_members[1].id: 0.35, demo_members[2].id: 0.25}
        )
        db.add(demo_wallet)
        
        db.commit()
        print("✓ 示例行程已创建")
        print("  - 行程名称：周末出游")
        print("  - 成员：张三、李四、王五")
        print("  - 公共钱包：¥3000.00")
        print(f"  - 归属比例：张三 40%、李四 35%、王五 25%")
    
    db.close()
    print("\n✅ 数据库初始化完成！")
    print("\n💡 提示：")
    print("  1. 访问 /trips 页面管理您的行程")
    print("  2. 为每个行程添加成员和钱包")
    print("  3. 在 /transactions 页面记录支出并选择分摊方式")
    print("  4. 在 /statistics 页面查看人均支出对比")


if __name__ == "__main__":
    init_db()
