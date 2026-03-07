from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from . import models
# Create FastAPI instance FIRST
app = FastAPI()

# Create tables in database
Base.metadata.create_all(bind=engine)
# Root endpoint
@app.get("/")
def read_root():
    return {"message": "EduMentor Backend Running 🚀"}


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Input schema
class IAInput(BaseModel):
    student_name: str
    subject_id: int
    ia1: float
    ia2: float
    attendance: float


# Upload IA endpoint
@app.post("/upload-ia/")
def upload_ia(data: IAInput, db: Session = Depends(get_db)):
    final_ia = (data.ia1 + data.ia2) / 2

    new_record = models.IAMarks(
        student_name=data.student_name,
        subject_id=data.subject_id,
        ia1=data.ia1,
        ia2=data.ia2,
        final_ia=final_ia,
        attendance=data.attendance
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "message": "IA uploaded successfully",
        "final_ia": final_ia
    }
