# File: models/cosmonaut.py

from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


# SQLAlchemy model for Cosmonaut
class Cosmonaut(Base):
    __tablename__ = "cosmonauts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    nationality = Column(String)
    specialization = Column(String)
    time_in_space = Column(Float)


# Pydantic model for data validation
class CosmonautCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: str
    nationality: str
    specialization: str
    time_in_space: float
