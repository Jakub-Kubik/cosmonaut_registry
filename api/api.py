import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.cosmonaut import Cosmonaut

# Load the .env file
load_dotenv(".env")

# Initialize FastAPI
app = FastAPI()

# Connect to the database
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Create tables
Cosmonaut.__table__.create(bind=engine, checkfirst=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/cosmonaut/{cosmonaut_id}")
def read_cosmonaut(cosmonaut_id: int):
    try:
        db = SessionLocal()
        db_cosmonaut = db.query(Cosmonaut).filter(Cosmonaut.id == cosmonaut_id).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

    if db_cosmonaut is None:
        raise HTTPException(status_code=404, detail="Cosmonaut not found")

    return {"cosmonaut": db_cosmonaut}


@app.get("/cosmonauts/")
def read_cosmonauts(skip: int = 0, limit: int = Query(1, le=1000), name_filter: str = None):
    try:
        db = SessionLocal()

        query = db.query(Cosmonaut)

        if name_filter:
            query = query.filter(Cosmonaut.name.ilike(f"%{name_filter}%"))

        cosmonauts = query.offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

    if len(cosmonauts) == 0:
        raise HTTPException(status_code=404, detail="No cosmonauts found")

    return {"cosmonauts": cosmonauts}


@app.get("/ping")
def ping():
    return {"message": "pong"}
