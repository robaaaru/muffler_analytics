from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Transaction, Service, Order
from app.schemas import TransactionCreate, TransactionRead

router = APIRouter()

@router.post("/transactions", response_model=TransactionRead)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    queried_cost = 0

    for a in transaction.orders:
        costs = db.query(Service).filter(Service.service_id == a.service_id).first()
        queried_cost += a.quantity * costs.cost 
    
    db_transaction = Transaction(created_at=transaction.created_at, custom_price=transaction.custom_price, total_cost = queried_cost)

    db.add(db_transaction)
    db.flush()

    transaction_id =  db_transaction.transaction_id

    for a in transaction.orders:
        db_order = Order(transaction_id = transaction_id, service_id = a.service_id, motor_id = a.motor_id, quantity = a.quantity)
        db.add(db_order)
  
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/transactions", response_model = list[TransactionRead])
def get_transactions(db: Session = Depends(get_db)):
    db_transactions = db.query(Transaction).all()
    return db_transactions