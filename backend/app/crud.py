from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from . import models, schemas
from datetime import datetime

def get_days_progress(db: Session):
    return db.query(models.DayProgress).order_by(models.DayProgress.day_id).all()

def get_day_detail(db: Session, day_id: int):
    return db.query(models.DayProgress).filter(models.DayProgress.day_id == day_id).first()

def complete_day(db: Session, day_id: int):
    day = db.query(models.DayProgress).filter(models.DayProgress.day_id == day_id).first()
    if day:
        day.completed = True
        day.review_count += 1
        day.last_completed_at = datetime.now()
        db.commit()
        db.refresh(day)
    return day

def search_phrases(db: Session, query: str):
    results = []
    
    # 1. Emergency Phrases 검색
    emergency_matches = db.query(models.EmergencyPhrase).filter(
        or_(
            models.EmergencyPhrase.korean.like(f"%{query}%"),
            models.EmergencyPhrase.category.like(f"%{query}%"),
            models.EmergencyPhrase.keywords.like(f"%{query}%")
        )
    ).all()
    
    for item in emergency_matches:
        results.append(schemas.SearchResultItem(
            source="emergency",
            category=item.category,
            korean=item.korean,
            english=item.english,
            context=f"긴급상황 ({item.category})"
        ))

    # 2. Dialogue 검색
    dialogue_matches = db.query(models.Dialogue).filter(
        models.Dialogue.korean.like(f"%{query}%")
    ).all()
    
    for item in dialogue_matches:
        results.append(schemas.SearchResultItem(
            source="dialogue",
            day_id=item.day_id,
            korean=item.korean,
            english=item.english,
            context=f"Day {item.day_id} 대화 ({item.role})"
        ))

    # 3. Expression 검색
    expression_matches = db.query(models.Expression).filter(
        models.Expression.korean.like(f"%{query}%")
    ).all()
    
    for item in expression_matches:
        results.append(schemas.SearchResultItem(
            source="expression",
            day_id=item.day_id,
            korean=item.korean,
            english=item.english,
            context=f"Day {item.day_id} 핵심표현"
        ))

    # 결과 리스트 반환 (우선순위: 긴급상황 -> 다이얼로그 -> 표현)
    return results

def get_stats(db: Session):
    total_days = 100
    completed_days = db.query(models.DayProgress).filter(models.DayProgress.completed == True).count()
    
    # 총 반복 복습 횟수 합산
    total_reviews = 0
    all_days = db.query(models.DayProgress).all()
    for d in all_days:
        total_reviews += d.review_count

    completion_rate = round((completed_days / total_days) * 100, 1) if total_days > 0 else 0.0
    
    # 최근 완료한 5개 학습 내역
    recent_activity = db.query(models.DayProgress)\
        .filter(models.DayProgress.completed == True)\
        .order_by(desc(models.DayProgress.last_completed_at))\
        .limit(5)\
        .all()

    return schemas.StatsResponse(
        total_days=total_days,
        completed_days=completed_days,
        total_reviews=total_reviews,
        completion_rate=completion_rate,
        recent_activity=recent_activity
    )

def reset_progress(db: Session):
    days = db.query(models.DayProgress).all()
    for d in days:
        d.completed = False
        d.review_count = 0
        d.last_completed_at = None
    db.commit()
    return True
