from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP)
    total_cost = Column(Numeric(10,2))
    orders = relationship("Order", cascade="all, delete-orphan", passive_deletes=True)

class Service(Base):
    __tablename__ = "services"
    service_id = Column(Integer, primary_key=True)
    service_type = Column(String)
    base_price = Column(Numeric(10,2))

class Motor(Base):
    __tablename__ = "motors"
    motor_id = Column(Integer, primary_key=True)
    brand = Column(String)
    model = Column(String)

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transactions.transaction_id", ondelete="CASCADE"))
    service_id = Column(Integer, ForeignKey("services.service_id"))
    motor_id = Column(Integer, ForeignKey("motors.motor_id"))
    order_cost = Column(Numeric(10,2))
    quantity = Column(Integer)
    service = relationship("Service")
    motor = relationship("Motor")