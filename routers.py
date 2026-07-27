from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from schemas import *
from models import Quiz, Question, Answer, Session as GameSession

router = APIRouter()

@router.get("/quizzes", response_model=list[QuizCard])
def get_quizzes(db: Session=Depends(get_db)):
    quizzes = db.query(Quiz).all()
    result = []
    for q in quizzes:
        result.append(QuizCard(
            id=q.id, title=q.title, description=q.description,
            author=q.author, created_at=q.created_at,
            question_number=len(q.questions)
        ))
    return result

@router.post("/quizzes", response_model=QuizRead, status_code=201)
def create_quiz(data: QuizCreate, db: Session=Depends(get_db)):
    quiz = Quiz(title=data.title, description=data.description, author=data.author)
    db.add(quiz)
    db.flush()
    
    for q_data in data.questions:
        question = Question(quiz_id=quiz.id, text=q_data.text, order=q_data.order)
        db.add(question)
        db.flush()
        
        correct_count = sum(1 for a in q_data.answers if a.is_correct)
        if correct_count != 1:
            raise HTTPException(status_code=400, detail="wrong amounf of right answers")
        
        for a_data in q_data.answers:
            answer = Answer(question_id=question.id, text=a_data.text, is_correct=a_data.is_correct)
            db.add(answer)
            
    db.commit()
    db.refresh(quiz)
    return quiz


@router.get("/quizzes/{quiz_id}", response_model=QuizPublic)
def get_quiz(quiz_id: int, db: Session=Depends(get_db)):
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="no such quiz")
    return quiz
    
@router.get("/quizzes/{quiz_id}/full", response_model=QuizRead)
def get_quiz_full(quiz_id: int, db: Session=Depends(get_db)):
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="no such quiz")
    return quiz


@router.delete("/quizzes/{quiz_id}", status_code=204)
def delete_quiz(quiz_id: int, db: Session=Depends(get_db)):
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="no such quiz")
    db.delete(quiz)
    db.commit()
    
    
@router.get("/sessions/{session_id}", response_model=SessionRead)
def get_session(session_id: int, db:  Session=Depends(get_db)):
    session = db.get(GameSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="no such session")
    return session


@router.post("/quizzes/{quiz_id}/sessions", response_model=SessionRead, status_code=201)
def start_session(quiz_id: int, data: SessionCreate, db:  Session=Depends(get_db)):
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="no such quiz")
    session = GameSession(quiz_id=quiz_id, player_name=data.player_name, score=0)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.post("/sessions/{session_id}/answer", response_model=AnswerResult)
def submit_answer(session_id: int, data: AnswerSubmit, db:  Session=Depends(get_db)):
    session = db.get(GameSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="no such session")
    
    question = db.Get(Question, data.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="no such question")
    
    answer = db.Get(Answer, data.answer_id)
    if not answer or answer.question_id != data.question_id:
        raise HTTPException(status_code=404, detail="no such answer")
    
    correct_answer = next(a for a in question.answers if a.is_correct)
    
    points = 0
    if answer.is_correct:
        points += 1
        session.score += points
        db.commit()
        
    return AnswerResult(
        correct=answer.is_correct,
        correct_answer_id=correct_answer.id,
        points_earned=points
    )