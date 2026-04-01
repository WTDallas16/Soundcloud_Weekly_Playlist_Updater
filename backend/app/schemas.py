from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Song schemas
class SongBase(BaseModel):
    track_id: str
    track_title: str
    track_permalink_url: str
    uploader_username: str
    uploaded_at: Optional[datetime] = None
    activity_created_at: Optional[datetime] = None

class SongResponse(SongBase):
    id: int
    run_id: int

    class Config:
        from_attributes = True

# Album schemas
class AlbumBase(BaseModel):
    playlist_id: str
    title: str
    playlist_type: str
    permalink_url: str
    uploader: str
    track_count: int
    activity_created_at: Optional[datetime] = None
    liked: str

class AlbumResponse(AlbumBase):
    id: int
    run_id: int

    class Config:
        from_attributes = True

# Run schemas
class RunCreate(BaseModel):
    hours_back: float = 168.0  # Default 7 days

class RunResponse(BaseModel):
    id: int
    created_at: datetime
    hours_back: float
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: str
    songs_count: int
    albums_count: int
    error_message: Optional[str]
    duration_seconds: Optional[float]
    songs: List[SongResponse] = []
    albums: List[AlbumResponse] = []

    class Config:
        from_attributes = True

class HistoryStats(BaseModel):
    run_id: int
    created_at: datetime
    songs_count: int
    albums_count: int

class AuthStatus(BaseModel):
    authenticated: bool
    token_expires_at: Optional[datetime]
    message: Optional[str]
