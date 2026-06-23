from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    major = Column(String)
    current_xp = Column(Integer, default=0)
    level = Column(Integer, default=1)

class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    title = Column(String)
    description = Column(String)
    xp_reward = Column(Integer)
    is_completed = Column(Boolean, default=False)