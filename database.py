import json
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings
from schemas import CodingAgentResponse

# 1. Connect to the Docker PostgreSQL container using DATABASE_URL from .env
engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Define the table columns using a Python class
class AgentHistory(Base):
    __tablename__ = "agent_history"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    code_snippet = Column(Text, nullable=False)
    language = Column(String(50), default="python")
    files_touched_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# 3. Function to automatically create the 'agent_history' table in Postgres
def init_db():
    Base.metadata.create_all(bind=engine)

# 4. Function to save a new AI response into Postgres
def save_interaction(prompt: str, response: CodingAgentResponse) -> int:
    db = SessionLocal()
    try:
        record = AgentHistory(
            prompt=prompt,
            explanation=response.explanation,
            code_snippet=response.code_snippet,
            language=response.language,
            files_touched_json=json.dumps([f.model_dump() for f in response.files_touched]),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record.id
    finally:
        db.close()

# 5. Function to read your past history from Postgres
def get_recent_history(limit: int = 5):
    db = SessionLocal()
    try:
        return (
            db.query(AgentHistory)
            .order_by(AgentHistory.created_at.desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()