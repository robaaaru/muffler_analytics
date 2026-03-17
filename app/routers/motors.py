from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Motor, Order
from app.schemas import MotorCreate, MotorRead
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(
    prefix="/motors",
    tags=["motors"],
    dependencies=[Depends(get_current_user)]
)

@router.post("", response_model=MotorRead)
def create_motor(motor: MotorCreate, db: Session = Depends(get_db)):
    db_motor = Motor(brand=motor.brand, model=motor.model)
    db.add(db_motor)
    db.commit()
    db.refresh(db_motor)
    return db_motor

@router.get("", response_model=list[MotorRead])
def get_motors(db: Session = Depends(get_db)):
    return db.query(Motor).all()

@router.get("/{id}", response_model=MotorRead)
def get_motor(id: int, db: Session = Depends(get_db)):
    db_motor = db.query(Motor).filter(Motor.motor_id == id).first()
    if db_motor is None:
        raise HTTPException(status_code=404, detail=f"Motor {id} doesn't exist!")
    return db_motor

@router.put("/{id}", response_model=MotorRead)
def update_motor(id: int, motor: MotorCreate, db: Session = Depends(get_db)):
    db_motor = db.query(Motor).filter(Motor.motor_id == id).first()
    if db_motor is None:
        raise HTTPException(status_code=404, detail=f"Motor {id} doesn't exist!")
    db_motor.brand = motor.brand
    db_motor.model = motor.model
    db.commit()
    db.refresh(db_motor)
    return db_motor

@router.delete("/{id}")
def delete_motor(id: int, db: Session = Depends(get_db)):
    db_motor = db.query(Motor).filter(Motor.motor_id == id).first()
    if db_motor is None:
        raise HTTPException(status_code=404, detail=f"Motor {id} doesn't exist!")
    
    # check if motor is used in any valid transaction
    in_use = db.query(Order).filter(Order.motor_id == id, Order.transaction_id.isnot(None)).first()
    if in_use:
        raise HTTPException(status_code=400, detail=f"Motor {id} is still used in existing orders and cannot be deleted!")
    
    # delete any orphaned orders referencing this motor
    db.query(Order).filter(Order.motor_id == id, Order.transaction_id.is_(None)).delete()

    db.delete(db_motor)
    db.commit()
    return {"message": f"Motor {id} deleted!"}