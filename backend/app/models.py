from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class DayProgress(Base):
    __tablename__ = "day_progress"

    day_id = Column(Integer, primary_key=True, index=True)
    theme = Column(String)
    title = Column(String)
    completed = Column(Boolean, default=False)
    review_count = Column(Integer, default=0)
    last_completed_at = Column(DateTime, nullable=True)

    # 1:N 관계 설정
    dialogues = relationship("Dialogue", back_populates="day_progress")
    expressions = relationship("Expression", back_populates="day_progress")


class Dialogue(Base):
    __tablename__ = "dialogues"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    day_id = Column(Integer, ForeignKey("day_progress.day_id"))
    role = Column(String)
    korean = Column(String)
    english = Column(String)
    order_index = Column(Integer)

    day_progress = relationship("DayProgress", back_populates="dialogues")


class Expression(Base):
    __tablename__ = "expressions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    day_id = Column(Integer, ForeignKey("day_progress.day_id"))
    korean = Column(String)
    english = Column(String)

    day_progress = relationship("DayProgress", back_populates="expressions")


class EmergencyPhrase(Base):
    __tablename__ = "emergency_phrases"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    korean = Column(String)
    english = Column(String)
    keywords = Column(String) # 빠른 한글 상황 검색을 위한 키워드
