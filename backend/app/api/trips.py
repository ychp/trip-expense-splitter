from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.trip import Trip
from app.models.member import Member
from app.schemas.trip import TripCreate, TripUpdate, TripResponse

router = APIRouter()


@router.get("/", response_model=list[TripResponse])
def list_trips(db: Session = Depends(get_db)):
    trips = db.query(Trip).order_by(Trip.created_at.desc()).all()
    result = []
    for trip in trips:
        members = db.query(Member).filter(Member.trip_id == trip.id).all()
        trip_dict = {
            "id": trip.id,
            "name": trip.name,
            "description": trip.description,
            "start_date": trip.start_date.strftime('%Y-%m-%d') if trip.start_date else None,
            "end_date": trip.end_date.strftime('%Y-%m-%d') if trip.end_date else None,
            "status": trip.status,
            "created_at": trip.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": trip.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "members": [{"id": m.id, "name": m.name} for m in members]
        }
        result.append(trip_dict)
    return result


@router.post("/", response_model=TripResponse)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    db_trip = Trip(**trip.model_dump())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    
    members = db.query(Member).filter(Member.trip_id == trip.id).all()
    return {
        "id": trip.id,
        "name": trip.name,
        "description": trip.description,
        "start_date": trip.start_date.strftime('%Y-%m-%d') if trip.start_date else None,
        "end_date": trip.end_date.strftime('%Y-%m-%d') if trip.end_date else None,
        "status": trip.status,
        "created_at": trip.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "updated_at": trip.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        "members": [{"id": m.id, "name": m.name} for m in members]
    }


@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(trip_id: int, trip: TripUpdate, db: Session = Depends(get_db)):
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    
    update_data = trip.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_trip, key, value)
    
    db.commit()
    db.refresh(db_trip)
    return db_trip


@router.delete("/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    
    db.delete(db_trip)
    db.commit()
    return {"message": "行程已删除"}
