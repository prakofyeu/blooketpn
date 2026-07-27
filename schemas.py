from datetime import datetime
from pydantic import BaseModel, Field

class AnswerCreate(BaseModel):
    text: str = Field(min_length=1, max_length=500)
    is_correct: bool = False
    
    
class AnswerRead(BaseModel):
    id: int
    text: str
    is_correct: bool
    
    model_config = {"from_attributes": True}
    
    
class AnswerPublic(BaseModel):
    id: int
    text: str
    
    model_config = {"from_attributes": True}
    

class QuestionCreate(BaseModel):
    text: str = Field(min_length=1, max_length=500)
    order: int = 0
    answers: list[AnswerCreate] = Field(min_length=1, max_length=5)
    

class QuestionRead(BaseModel):
    id: int
    text: str
    order: int
    answers: list[AnswerRead]
    
    model_config = {"from_attributes": True}
    
    
class QuestionPublic(BaseModel):
    id: int
    text: str
    order: int
    answers: list[AnswerPublic]
    
    model_config = {"from_attributes": True}
    
    
class QuizCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(default="no description", max_length=500)
    author: str = Field(min_length=2, max_length=100)
    questions: list[QuestionCreate] = Field(min_length=1)
    
    
class QuizPublic(BaseModel):
    id: int
    title: str
    description: str
    author: str
    created_at: datetime
    questions: list[QuestionPublic]
    
    model_config = {"from_attributes": True}
    

class QuizRead(BaseModel):
    id: int
    title: str
    description: str
    author: str
    created_at: datetime
    questions: list[QuestionRead]
    
    model_config = {"from_attributes": True}
    
    
    
class QuizCard(BaseModel):
    id: int
    title: str
    description: str
    author: str
    created_at: datetime
    question_number: int
    
    model_config = {"from_attributes": True}
    
    
class SessionCreate(BaseModel):
    player_name: str = Field(min_length=2, max_length=500)
    
    
class SessionRead(BaseModel):
    id: int
    quiz_id: int
    player_name: str
    score: int
    
    model_config = {"from_attributes": True}
    
    
class AnswerSubmit(BaseModel):
    question_id: int
    answer_id: int


class AnswerResult(BaseModel):
    correct: bool
    correct_answer_id: int
    points_earned: int    