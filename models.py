from datetime import datetime
from sqlalchemy import Boolean, ForeignKey, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Quiz(Base):
    __tablename__ = "quizes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500), default="no description")
    author: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    questions: Mapped[list["Question"]] = relationship(
        back_populates="quiz", cascade="all, delete-orphan"
    )
    
    sessions: Mapped[list["Session"]] = relationship(
        back_populates="quiz", cascade="all, delete-orphan"
    )
    

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizes.id"))
    text: Mapped[str] = mapped_column(String(500))
    order: Mapped[int] = mapped_column(Integer, default=0)
    
    quiz: Mapped["Quiz"] = relationship(back_populates="questions")
    
    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )
    
    
class Answer(Base):
    __tablename__ = "answers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    text: Mapped[str] = mapped_column(String(500))
    
    is_correct: Mapped[Boolean] = mapped_column(Boolean, default=False)
    answer: Mapped["Answer"] = relationship(back_populates="answers")
    

class Session(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizes.id"))
    player_name: Mapped[str] = mapped_column(String(500))
    score: Mapped[int] = mapped_column(Integer, default=0)
    
    quiz: Mapped["Quiz"] = relationship(back_populates="sessions")
    