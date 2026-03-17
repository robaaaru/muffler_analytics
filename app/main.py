from fastapi import FastAPI
from app.routers import transactions, motors, services, auth

app = FastAPI()

app.include_router(transactions.router)
app.include_router(services.router)
app.include_router(motors.router)
app.include_router(auth.router)