from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DialogueBase(BaseModel):
    role: str
    korean: str
    english: str
    order_index: int

class DialogueCreate(DialogueBase):
    pass

class Dialogue(DialogueBase):
    id: int
    day_id: int

    class Config:
        from_attributes = True


class ExpressionBase(BaseModel):
    korean: str
    english: str

class ExpressionCreate(ExpressionBase):
    pass

class Expression(ExpressionBase):
    id: int
    day_id: int

    class Config:
        from_attributes = True


class DayProgressBrief(BaseModel):
    day_id: int
    theme: str
    title: str
    completed: bool
    review_count: int
    last_completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DayProgressDetail(DayProgressBrief):
    dialogues: List[Dialogue] = []
    expressions: List[Expression] = []

    class Config:
        from_attributes = True


class EmergencyPhraseBase(BaseModel):
    id: int
    category: str
    korean: str
    english: str
    keywords: str

class EmergencyPhrase(EmergencyPhraseBase):
    class Config:
        from_attributes = True


class SearchResultItem(BaseModel):
    source: str # "emergency", "dialogue", "expression"
    day_id: Optional[int] = None
    category: Optional[str] = None
    korean: str
    english: str
    context: Optional[str] = None # 매칭된 문맥 설명 (예: "Day 1 다이얼로그")


class StatsResponse(BaseModel):
    total_days: int # 100
    completed_days: int # 완료한 일수
    total_reviews: int # 총 반복 횟수
    completion_rate: float # 진척도 (%)
    recent_activity: List[DayProgressBrief]
