from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Motor
from app.schemas import MotorCreate, MotorRead
from app.database import get_db

router = APIRouter()

@router.post("/motors", response_model=MotorRead)
def create_motor(motor: MotorCreate, db: Session = Depends(get_db)):
    db_motor = Motor(brand=motor.brand, model=motor.model)
    db.add(db_motor)
    db.commit()
    db.refresh(db_motor)
    return db_motor

@router.get("/motors", response_model=list[MotorRead])
def get_motors(db: Session = Depends(get_db)):
    return db.query(Motor).all()

@router.get("/motors/{id}", response_model=MotorRead)
def get_motor(id: int, db: Session = Depends(get_db)):
    db_motor = db.query(Motor).filter(Motor.motor_id == id).first()
    if db_motor is None:
        raise HTTPException(status_code=404, detail=f"Motor {id} doesn't exist!")
    return db_motor

@router.put("/motors/{id}", response_model=MotorRead)
def update_motor(id: int, motor: MotorCreate, db: Session = Depends(get_db)):
    db_motor = db.query(Motor).filter(Motor.motor_id == id).first()
    if db_motor is None:
        raise HTTPException(status_code=404, detail=f"Motor {id} doesn't exist!")
    db_motor.brand = motor.brand
    db_motor.model = motor.model
    db.commit()
    db.refresh(db_motor)
    return db_motor

@router.delete("/motors/{id}")
def delete_motor(id: int, db: Session = Depends(get_db)):
    db_motor = db.query(Motor).filter(Motor.motor_id == id).first()
    if db_motor is None:
        raise HTTPException(status_code=404, detail=f"Motor {id} doesn't exist!")
    db.delete(db_motor)
    db.commit()
    return {"message": f"Motor {id} deleted!"}