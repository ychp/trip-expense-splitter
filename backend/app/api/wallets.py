from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.core.database import get_db
from app.models.wallet import Wallet
from app.models.wallet_member import WalletMember
from app.models.member import Member
from app.schemas.wallet import WalletCreate, WalletUpdate, WalletResponse, WalletMemberResponse

router = APIRouter()


@router.get("/")
def list_wallets(trip_id: int = None, db: Session = Depends(get_db)):
    """获取钱包列表 - 优化版本（使用JOIN避免N+1）"""
    query = db.query(Wallet)
    if trip_id:
        query = query.filter(Wallet.trip_id == trip_id)
    wallets = query.order_by(Wallet.created_at.desc()).all()
    
    if not wallets:
        return []
    
    wallet_ids = [w.id for w in wallets]
    
    # 使用JOIN一次性获取所有钱包成员及其成员信息
    wallet_members_data = db.query(
        WalletMember.id,
        WalletMember.wallet_id,
        WalletMember.member_id,
        WalletMember.balance,
        Member.name.label('member_name')
    ).join(
        Member, Member.id == WalletMember.member_id
    ).filter(
        WalletMember.wallet_id.in_(wallet_ids)
    ).all()
    
    # 按钱包ID分组
    wallet_members_map = {}
    for wm in wallet_members_data:
        if wm.wallet_id not in wallet_members_map:
            wallet_members_map[wm.wallet_id] = []
        wallet_members_map[wm.wallet_id].append(wm)
    
    result = []
    for wallet in wallets:
        wallet_members = wallet_members_map.get(wallet.id, [])
        total_balance = sum(wm.balance for wm in wallet_members)
        
        members_data = [
            {
                "id": wm.id,
                "member_id": wm.member_id,
                "member_name": wm.member_name or "未知成员",
                "balance": wm.balance
            }
            for wm in wallet_members
        ]
        
        # 计算ownership（归属比例）
        ownership = {}
        if total_balance > 0:
            for wm in wallet_members:
                ownership[wm.member_id] = wm.balance / total_balance
        
        result.append({
            "id": wallet.id,
            "name": wallet.name,
            "balance": total_balance,
            "trip_id": wallet.trip_id,
            "created_at": wallet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": wallet.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "members": members_data,
            "ownership": ownership
        })
    
    return result


@router.post("/", response_model=WalletResponse)
def create_wallet(wallet: WalletCreate, db: Session = Depends(get_db)):
    db_wallet = Wallet(**wallet.model_dump())
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    
    return {
        "id": db_wallet.id,
        "name": db_wallet.name,
        "trip_id": db_wallet.trip_id,
        "created_at": db_wallet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "updated_at": db_wallet.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        "members": [],
        "total_balance": 0
    }


@router.get("/{wallet_id}", response_model=WalletResponse)
def get_wallet(wallet_id: int, db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="钱包不存在")
    
    wallet_members = db.query(WalletMember).filter(WalletMember.wallet_id == wallet.id).all()
    members_data = []
    for wm in wallet_members:
        member = db.query(Member).filter(Member.id == wm.member_id).first()
        members_data.append({
            "id": wm.id,
            "member_id": wm.member_id,
            "member_name": member.name if member else "未知成员",
            "balance": wm.balance
        })
    
    return {
        "id": wallet.id,
        "name": wallet.name,
        "trip_id": wallet.trip_id,
        "created_at": wallet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "updated_at": wallet.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        "members": members_data,
        "total_balance": sum(wm.balance for wm in wallet_members)
    }


@router.put("/{wallet_id}", response_model=WalletResponse)
def update_wallet(wallet_id: int, wallet: WalletUpdate, db: Session = Depends(get_db)):
    db_wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not db_wallet:
        raise HTTPException(status_code=404, detail="钱包不存在")
    
    update_data = wallet.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_wallet, key, value)
    
    db.commit()
    db.refresh(db_wallet)
    return db_wallet


@router.delete("/{wallet_id}")
def delete_wallet(wallet_id: int, db: Session = Depends(get_db)):
    db_wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not db_wallet:
        raise HTTPException(status_code=404, detail="钱包不存在")
    
    db.delete(db_wallet)
    db.commit()
    return {"message": "钱包已删除"}


@router.get("/{wallet_id}/members", response_model=list[WalletMemberResponse])
def get_wallet_members(wallet_id: int, db: Session = Depends(get_db)):
    """获取钱包的所有成员余额"""
    wallet_members = db.query(WalletMember).options(
        joinedload(WalletMember.member)
    ).filter(WalletMember.wallet_id == wallet_id).all()
    
    result = []
    for wm in wallet_members:
        result.append(WalletMemberResponse(
            id=wm.id,
            wallet_id=wm.wallet_id,
            member_id=wm.member_id,
            balance=wm.balance,
            member_name=wm.member.name if wm.member else ""
        ))
    return result


@router.put("/{wallet_id}/members")
def batch_update_wallet_members(
    wallet_id: int, 
    members: list[dict],
    db: Session = Depends(get_db)
):
    """批量设置钱包成员余额"""
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="钱包不存在")
    
    for member_data in members:
        member_id = member_data.get('member_id')
        balance = member_data.get('balance', 0)
        
        wallet_member = db.query(WalletMember).filter(
            WalletMember.wallet_id == wallet_id,
            WalletMember.member_id == member_id
        ).first()
        
        if wallet_member:
            wallet_member.balance = balance
        else:
            wallet_member = WalletMember(
                wallet_id=wallet_id,
                member_id=member_id,
                balance=balance
            )
            db.add(wallet_member)
    
    db.commit()
    return {"message": "成员余额已更新"}
