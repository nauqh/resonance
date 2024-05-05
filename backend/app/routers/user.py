from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import json
from .. import models
from ..schemas import User
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"},
               201: {"description": "Created"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(data: User, db: Session = Depends(get_db)):
    user = models.User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/{owner_id}/diagnoses/", status_code=status.HTTP_201_CREATED)
def create_diagnose(owner_id: int, data: dict, db: Session = Depends(get_db)):
    diagnose = models.Diagnose(owner_id=owner_id, content=json.dumps(data))
    db.add(diagnose)
    db.commit()
    db.refresh(diagnose)
    return diagnose
