from sqlalchemy import Column, Integer, String
from .database import Base


class Diagnose(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)
