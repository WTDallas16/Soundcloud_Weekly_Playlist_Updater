from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import HistoryStats
from ..services.run_tracker import RunTracker

router = APIRouter()

@router.get("/stats", response_model=List[HistoryStats])
async def get_history_stats(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get statistics for recent runs for graphing

    Returns minimal data optimized for charts:
    - run_id
    - created_at
    - songs_count
    - albums_count
    """
    runs = RunTracker.get_recent_runs(db, limit)

    # Convert to HistoryStats format
    stats = [
        HistoryStats(
            run_id=run.id,
            created_at=run.created_at,
            songs_count=run.songs_count,
            albums_count=run.albums_count
        )
        for run in runs
    ]

    # Return in chronological order (oldest first) for charts
    return list(reversed(stats))
