from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.mysql import JSON
from data.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    nickname = Column(String(20))
    role = Column(String(50), default="ROLE_USER")
    deleted = Column(Boolean, default=False)
    preferred_genres = Column(JSON)
    play_times = Column(JSON)
