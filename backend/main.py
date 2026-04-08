from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Student
import json
import ollama  # <- just import the module

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/")
def create_student(name: str, db: Session = Depends(get_db)):
    student = Student(name=name)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    return db.query(Student).filter(Student.id == student_id).first()

@app.get("/questions/")
def get_questions():
    with open("questions.json") as f:
        questions = json.load(f)
    return questions

@app.post("/quiz/")
def quiz_answer(student_id: int, question_id: int, answer: str, db: Session = Depends(get_db)):
    with open("questions.json") as f:
        questions = json.load(f)
    q = next(q for q in questions if q["id"] == question_id)
    if answer.strip() == q["answer"]:
        result = {"correct": True, "next_level": q["level"] + 1}
    else:
        result = {"correct": False, "explanation": q["explanation"], "retry": True}
    return result

@app.post("/explain/")
def explain_question(question: str):
    prompt = f"Explain this question in simple English for secondary students: {question}"
    # Use ollama.chat() directly
    response = ollama.chat(
        model="gemma3:1b",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"explanation": response}
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)