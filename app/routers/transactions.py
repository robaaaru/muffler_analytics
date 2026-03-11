from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Transaction, Service, Order
from app.schemas import TransactionCreate, TransactionRead

router = APIRouter()

@router.post("/transactions", response_model=TransactionRead)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    queried_cost = 0

    for order_item in transaction.orders:
        costs = db.query(Service).filter(Service.service_id == order_item.service_id).first()
        if costs is None:
            raise HTTPException(status_code=404, detail="Service doesn't exist!")
        queried_cost += order_item.quantity * costs.cost

    db_transaction = Transaction(created_at=transaction.created_at, custom_price=transaction.custom_price, total_cost=queried_cost)

    db.add(db_transaction)
    db.flush()

    for order_item in transaction.orders:
        db_order = Order(transaction_id=db_transaction.transaction_id, service_id=order_item.service_id, motor_id=order_item.motor_id, quantity=order_item.quantity)
        db.add(db_order)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/transactions", response_model=list[TransactionRead])
def get_transactions(db: Session = Depends(get_db)):
    db_transactions = db.query(Transaction).all()
    return db_transactions

@router.get("/transactions/{id}", response_model=TransactionRead)
def get_transaction(id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.transaction_id == id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail=f'Transaction {id} does not exist!')

    return db_transaction

@router.put("/transactions/{id}", response_model=TransactionRead)
def update_transaction(id: int, transaction: TransactionCreate, db: Session = Depends(get_db)):

    db_transaction = db.query(Transaction).filter(Transaction.transaction_id == id).first()

    if db_transaction is None:
        raise HTTPException(status_code=404, detail=f'Transaction {id} does not exist!')

    db_transaction.created_at = transaction.created_at
    db_transaction.custom_price = transaction.custom_price

    db.query(Order).filter(Order.transaction_id == id).delete()

    transaction_new_total = 0

    for order_item in transaction.orders:
        db_service = db.query(Service).filter(Service.service_id == order_item.service_id).first()
        if db_service is None:
            raise HTTPException(status_code=404, detail="Service doesn't exist!")
        db_order = Order(transaction_id=db_transaction.transaction_id, service_id=order_item.service_id, motor_id=order_item.motor_id, quantity=order_item.quantity)
        db.add(db_order)
        transaction_new_total += order_item.quantity * db_service.cost

    db_transaction.total_cost = transaction_new_total

    db.commit()
    db.refresh(db_transaction)
    return db_transaction