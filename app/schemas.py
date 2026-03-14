from pydantic import BaseModel
from datetime import datetime
from typing import List

class ServiceCreate(BaseModel):
    service_type: str
    base_price: float

class ServiceRead(ServiceCreate):
    class Config:
        from_attributes = True
    service_id: int

class MotorCreate(BaseModel):
    brand: str
    model: str

class MotorRead(MotorCreate):
    class Config:
        from_attributes = True
    motor_id: int

class OrderCreate(BaseModel):
    quantity: int
    motor_id: int
    service_id: int
    order_cost: float   

class OrderRead(OrderCreate):
    class Config:
        from_attributes = True
    order_id: int
    service: ServiceRead
    motor: MotorRead

class TransactionCreate(BaseModel):
    orders: List[OrderCreate]
    created_at: datetime

class TransactionRead(BaseModel):
    class Config:
        from_attributes = True
    transaction_id: int
    created_at: datetime
    total_cost: float
    orders: List[OrderRead]

