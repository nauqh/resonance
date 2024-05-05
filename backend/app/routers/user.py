from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import json
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"},
               201: {"description": "Created"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(data: schemas.User, db: Session = Depends(get_db)):
    user = models.User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{email}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email: {email} does not exist")
    return user


@router.post("/{owner_id}/diagnoses", status_code=status.HTTP_201_CREATED)
def create_diagnose(owner_id: int, data: dict, db: Session = Depends(get_db)):
    diagnose = models.Diagnose(owner_id=owner_id, content=json.dumps(data))
    db.add(diagnose)
    db.commit()
    db.refresh(diagnose)
    return diagnose


@router.get("/{email}/diagnoses", status_code=status.HTTP_200_OK, response_model=list[schemas.DiagnosisOut])
def get_diagnoses(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email: {email} does not exist")
    for diagnosis in user.diagnoses:
        diagnosis.content = json.loads(diagnosis.content)
    return user.diagnoses
