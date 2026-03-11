from fastapi import FastAPI
from app.routers import transactions, orders, motors, services

app = FastAPI()

app.include_router(transactions.router)
app.include_router(orders.router)
app.include_router(services.router)
app.include_router(motors.router)