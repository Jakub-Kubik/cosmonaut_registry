import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
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
    # Create a new session
    db = SessionLocal()

    # Query the database to find the cosmonaut
    db_cosmonaut = db.query(Cosmonaut).filter(Cosmonaut.id == cosmonaut_id).first()

    # Close the session
    db.close()

    if db_cosmonaut is None:
        raise HTTPException(status_code=404, detail="Cosmonaut not found")

    return {"cosmonaut": db_cosmonaut}


@app.get("/ping")
def ping():
    return {"message": "pong"}
