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

@router.get("/services", response_model=list[ServiceRead])
def get_services(db : Session = Depends(get_db)):
    db_services = db.query(Service).all()
    return db_services


@router.get("/services/{id}", response_model=ServiceRead)
def get_service(id: int, db : Session = Depends(get_db)):
    db_service = db.query(Service).filter(Service.service_id == id).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail=f"Service {id} doesn't exist!")
    return db_service


