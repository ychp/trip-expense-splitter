from app.core.database import engine, Base, SessionLocal
from app.models import Account, Category


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    existing_categories = db.query(Category).first()
    if not existing_categories:
        default_expense_categories = [
            {"name": "餐饮", "type": "expense", "sort_order": 1},
            {"name": "交通", "type": "expense", "sort_order": 2},
            {"name": "购物", "type": "expense", "sort_order": 3},
            {"name": "娱乐", "type": "expense", "sort_order": 4},
            {"name": "医疗", "type": "expense", "sort_order": 5},
            {"name": "教育", "type": "expense", "sort_order": 6},
            {"name": "居住", "type": "expense", "sort_order": 7},
            {"name": "通讯", "type": "expense", "sort_order": 8},
            {"name": "其他支出", "type": "expense", "sort_order": 9},
        ]
        
        default_income_categories = [
            {"name": "工资", "type": "income", "sort_order": 1},
            {"name": "奖金", "type": "income", "sort_order": 2},
            {"name": "投资收益", "type": "income", "sort_order": 3},
            {"name": "其他收入", "type": "income", "sort_order": 4},
        ]
        
        for cat_data in default_expense_categories + default_income_categories:
            category = Category(**cat_data)
            db.add(category)
        
        db.commit()
        print("默认分类已创建")
    
    existing_accounts = db.query(Account).first()
    if not existing_accounts:
        default_accounts = [
            {"name": "现金", "type": "cash", "balance": 0},
            {"name": "支付宝", "type": "alipay", "balance": 0},
            {"name": "微信", "type": "wechat", "balance": 0},
        ]
        
        for acc_data in default_accounts:
            account = Account(**acc_data)
            db.add(account)
        
        db.commit()
        print("默认账户已创建")
    
    db.close()
    print("数据库初始化完成!")


if __name__ == "__main__":
    init_db()
