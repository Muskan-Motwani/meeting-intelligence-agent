from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./meetings.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    transcript = Column(String)
    summary = Column(String)
    action_items = Column(JSON)
    decisions = Column(JSON)
    overall_tone = Column(String)


Base.metadata.create_all(bind=engine)

def save_meeting(transcript: str, insights: dict) -> int:
    db = SessionLocal()
    meeting = Meeting(
        transcript=transcript,
        summary=insights["summary"],
        action_items=insights["action_items"],
        decisions=insights["decisions"],
        overall_tone=insights["overall_tone"]
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    db.close()
    return meeting.id
def get_meeting(meeting_id: int):
    db = SessionLocal()
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    db.close()
    return meeting

def get_all_meetings():
    db = SessionLocal()
    meetings = db.query(Meeting).all()
    db.close()
    return meetings