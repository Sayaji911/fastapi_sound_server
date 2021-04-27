from sqlalchemy import DateTime, Column, String, Integer, CheckConstraint
from src.database import Base
from typing import Optional
import datetime


class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    uploadTime = Column(DateTime(timezone=True))
    __table_args__ = (
        CheckConstraint(duration >= 0, name='check_bar_positive'),
        {})



class Podcast(Base):
    __tablename__ = 'podcast'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    uploadTime = Column(DateTime(timezone=True))
    host = Column(String(100), nullable=False, )
    participants = Column(String)
    __table_args__ = (
        CheckConstraint(duration >= 0, name='check_bar_positive'),
        {})

class Audiobook(Base):
    __tablename__ = 'audiobook'
    id = Column(Integer, unique=True, primary_key=True ,nullable=False)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False, )
    narrator = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    uploadTime = Column(DateTime(timezone=True))
    __table_args__ = (
        CheckConstraint(duration >= 0, name='check_bar_positive'),
        {})

