import json
import os
from sqlalchemy.orm import Session
from .database import engine, Base
from . import models

def seed_data(db: Session):
    # DDL 실행하여 테이블 생성
    Base.metadata.create_all(bind=engine)

    # 이미 데이터가 있는지 검사 (DayProgress 개수로 판단)
    if db.query(models.DayProgress).count() > 0:
        print("Database already has data. Skipping seeding.")
        return

    # JSON 데이터 로드
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "travel_data.json")

    if not os.path.exists(json_path):
        print(f"Error: JSON data file not found at {json_path}")
        return

    print("Seeding database with travel english data...")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 100일 코스 시딩
    days_list = data.get("days", [])
    for d in days_list:
        # DayProgress 생성
        progress = models.DayProgress(
            day_id=d["day_id"],
            theme=d["theme"],
            title=d["title"],
            completed=False,
            review_count=0,
            last_completed_at=None
        )
        db.add(progress)
        db.flush() # Foreign key 연동을 위해 ID 확정

        # Dialogues 삽입
        for idx, dial in enumerate(d.get("dialogue", [])):
            dialogue_item = models.Dialogue(
                day_id=progress.day_id,
                role=dial["role"],
                korean=dial["korean"],
                english=dial["english"],
                order_index=idx
            )
            db.add(dialogue_item)

        # Expressions 삽입
        for exp in d.get("expressions", []):
            expression_item = models.Expression(
                day_id=progress.day_id,
                korean=exp["korean"],
                english=exp["english"]
            )
            db.add(expression_item)

    # 2. Emergency Phrases 시딩
    emergency_list = data.get("emergency_phrases", [])
    for em in emergency_list:
        phrase = models.EmergencyPhrase(
            id=em["id"],
            category=em["category"],
            korean=em["korean"],
            english=em["english"],
            keywords=em["keywords"]
        )
        db.add(phrase)

    # DB 반영
    db.commit()
    print("Database seeding completed successfully.")
