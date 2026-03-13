from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Service
from app.schemas import ServiceCreate, ServiceRead
from app.database import get_db

router = APIRouter()

@router.post("/services", response_model=ServiceRead)
def create_service(service: ServiceCreate, db : Session = Depends(get_db)):
    
    db_service = Service(service_type = service.service_type, cost = service.cost)
    db.add(db_service)

    db.commit()
    db.refresh(db_service)
    return db_service

