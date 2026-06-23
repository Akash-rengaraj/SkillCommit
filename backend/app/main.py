from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import engine, Base, get_db
from app.models import schemas
from app.services.rag_service import CareerRAGService

# Create the database tables automatically
schemas.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkillCommit API", version="1.0.0")
rag_service = CareerRAGService()

@app.get("/")
async def root():
    return {"message": "SkillCommit API is operational"}

@app.post("/quests/generate")
async def generate_quest(student_profile: dict, career_goal: str):
    """
    Triggers the RAG pipeline to generate a custom quest based on the student's goal.
    """
    try:
        new_quest = rag_service.generate_student_quest(student_profile, career_goal)
        return {"generated_quest": new_quest}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quests/{quest_id}/complete")
async def complete_quest(quest_id: int, db: Session = Depends(get_db)):
    """
    Marks a quest as complete and awards XP to the student.
    """
    quest = db.query(schemas.Quest).filter(schemas.Quest.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    
    quest.is_completed = True
    
    # Update student XP
    student = db.query(schemas.Student).filter(schemas.Student.id == quest.student_id).first()
    if student:
        student.current_xp += quest.xp_reward
        
    db.commit()
    return {"message": "Skill Committed!", "xp_awarded": quest.xp_reward}