from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models import Run, Song, Album

class RunTracker:
    """Handles database operations for runs, songs, and albums"""

    @staticmethod
    def create_run(db: Session, hours_back: float) -> Run:
        """Create a new run record with status='running'"""
        # Use naive datetime for SQLite compatibility
        run = Run(
            hours_back=hours_back,
            start_time=datetime.now(),
            status="running"
        )
        db.add(run)
        db.commit()
        db.refresh(run)
        return run

    @staticmethod
    def complete_run(
        db: Session,
        run_id: int,
        songs: List[Dict[str, Any]],
        albums: List[Dict[str, Any]]
    ) -> Run:
        """
        Complete a run by saving songs/albums and updating status

        Args:
            db: Database session
            run_id: Run ID to update
            songs: List of song dicts from script
            albums: List of album dicts from script

        Returns:
            Updated Run object
        """
        run = db.query(Run).filter(Run.id == run_id).first()
        if not run:
            raise ValueError(f"Run {run_id} not found")

        # Save songs
        for song_data in songs:
            song = Song(
                run_id=run_id,
                track_id=str(song_data.get('track_id', '')),
                track_title=song_data.get('track_title', ''),
                track_permalink_url=song_data.get('track_permalink_url', ''),
                uploader_username=song_data.get('uploader_username', ''),
                uploaded_at=RunTracker._parse_datetime(song_data.get('uploaded_at')),
                activity_created_at=RunTracker._parse_datetime(song_data.get('activity_created_at'))
            )
            db.add(song)

        # Save albums
        for album_data in albums:
            album = Album(
                run_id=run_id,
                playlist_id=str(album_data.get('playlist_id', '')),
                title=album_data.get('title', ''),
                playlist_type=album_data.get('playlist_type', ''),
                permalink_url=album_data.get('permalink_url', ''),
                uploader=album_data.get('uploader', ''),
                track_count=album_data.get('track_count', 0),
                activity_created_at=RunTracker._parse_datetime(album_data.get('activity_created_at')),
                liked=album_data.get('liked', 'no')
            )
            db.add(album)

        # Update run status
        run.end_time = datetime.now()
        run.status = "completed"
        run.songs_count = len(songs)
        run.albums_count = len(albums)

        # Calculate duration
        if run.start_time:
            run.duration_seconds = (run.end_time - run.start_time).total_seconds()
        else:
            run.duration_seconds = None

        db.commit()
        db.refresh(run)
        return run

    @staticmethod
    def fail_run(db: Session, run_id: int, error_message: str) -> Run:
        """Mark a run as failed with error message"""
        run = db.query(Run).filter(Run.id == run_id).first()
        if not run:
            raise ValueError(f"Run {run_id} not found")

        run.end_time = datetime.now()
        run.status = "failed"
        run.error_message = error_message
        if run.start_time:
            run.duration_seconds = (run.end_time - run.start_time).total_seconds()

        db.commit()
        db.refresh(run)
        return run

    @staticmethod
    def get_run(db: Session, run_id: int) -> Run:
        """Get a run with all songs and albums"""
        return db.query(Run).filter(Run.id == run_id).first()

    @staticmethod
    def get_recent_runs(db: Session, limit: int = 20) -> List[Run]:
        """Get recent completed runs for history"""
        return db.query(Run).filter(
            Run.status == "completed"
        ).order_by(
            Run.created_at.desc()
        ).limit(limit).all()

    @staticmethod
    def _parse_datetime(value) -> datetime | None:
        """Parse datetime from various formats"""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                # Try ISO format
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except:
                return None
        return None
