from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    hours_back = Column(Float, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String, default="running")  # 'running', 'completed', 'failed'
    songs_count = Column(Integer, default=0)
    albums_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    duration_seconds = Column(Float, nullable=True)

    # Relationships
    songs = relationship("Song", back_populates="run", cascade="all, delete-orphan")
    albums = relationship("Album", back_populates="run", cascade="all, delete-orphan")

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"), nullable=False)
    track_id = Column(String, nullable=False)
    track_title = Column(String, nullable=False)
    track_permalink_url = Column(String, nullable=False)
    uploader_username = Column(String, nullable=False)
    uploaded_at = Column(DateTime)
    activity_created_at = Column(DateTime)

    # Relationship
    run = relationship("Run", back_populates="songs")

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"), nullable=False)
    playlist_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    playlist_type = Column(String, nullable=False)
    permalink_url = Column(String, nullable=False)
    uploader = Column(String, nullable=False)
    track_count = Column(Integer, nullable=False)
    activity_created_at = Column(DateTime)
    liked = Column(String, default="no")  # 'yes', 'no', 'failed'

    # Relationship
    run = relationship("Run", back_populates="albums")
