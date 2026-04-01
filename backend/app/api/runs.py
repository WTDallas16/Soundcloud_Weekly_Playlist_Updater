from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import RunCreate, RunResponse
from ..services.sc_executor import ScriptExecutor
from ..services.run_tracker import RunTracker

router = APIRouter()

def execute_run_task(run_id: int, hours_back: float):
    """Background task to execute script and save results"""
    from ..database import SessionLocal

    db = SessionLocal()
    try:
        # Execute scripts
        executor = ScriptExecutor()
        results = executor.execute_full_run(hours_back)

        # Save results to database
        RunTracker.complete_run(
            db,
            run_id,
            songs=results.get('songs', []),
            albums=results.get('albums', [])
        )
    except Exception as e:
        # Mark run as failed
        RunTracker.fail_run(db, run_id, str(e))
    finally:
        db.close()

@router.post("/", response_model=RunResponse)
async def create_run(
    run_data: RunCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a new run and execute it in the background

    Returns run immediately with status='running'
    Client should poll GET /runs/{id} for completion
    """
    # Create run record
    run = RunTracker.create_run(db, run_data.hours_back)

    # Launch background task
    background_tasks.add_task(execute_run_task, run.id, run_data.hours_back)

    return run

@router.get("/{run_id}", response_model=RunResponse)
async def get_run(run_id: int, db: Session = Depends(get_db)):
    """
    Get a specific run with all songs and albums

    Use this endpoint to poll for run completion
    """
    run = RunTracker.get_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    return run

@router.get("/", response_model=List[RunResponse])
async def list_runs(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get recent completed runs

    Used for run history table in UI
    """
    runs = RunTracker.get_recent_runs(db, limit)
    return runs
