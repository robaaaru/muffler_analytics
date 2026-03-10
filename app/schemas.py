from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from typing import List

class OrderCreate(BaseModel):
    quantity: int
    motor_id: int
    service_id: int

class OrderRead(OrderCreate):
    order_id: int

class TransactionCreate(BaseModel):
    custom_price: Optional[float] = None
    orders: List[OrderCreate]

class TransactionRead(BaseModel):
    transaction_id: int
    created_at: datetime
    custom_price: Optional[float] = None
    total_cost: float

class ServiceCreate(BaseModel):
    service_type: str
    cost: float

class ServiceRead(ServiceCreate):
    service_id: int

class MotorCreate(BaseModel):
    brand: str
    model: str

class MotorRead(MotorCreate):
    motor_id: int