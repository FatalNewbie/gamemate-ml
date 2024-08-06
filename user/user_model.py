from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from data.database import Base

# 중간 테이블 정의
user_genres_association = Table(
    'user_genres', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('genre_id', Integer, ForeignKey('genre.id'))
)

user_playtimes_association = Table(
    'user_playtimes', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('playtime_id', Integer, ForeignKey('playtime.id'))
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    nickname = Column(String(20))
    role = Column(String(50), default="ROLE_USER")
    deleted = Column(Boolean, default=False)

    preferred_genres = relationship("Genre", secondary=user_genres_association, back_populates="users")
    play_times = relationship("PlayTime", secondary=user_playtimes_association, back_populates="users")


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    users = relationship("User", secondary=user_genres_association, back_populates="preferred_genres")


class PlayTime(Base):
    __tablename__ = "playtime"

    id = Column(Integer, primary_key=True, index=True)
    time_slot = Column(String(50), unique=True)
    users = relationship("User", secondary=user_playtimes_association, back_populates="play_times")
