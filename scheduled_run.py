from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the SoundCloud weekly updater without starting the frontend/backend."
    )
    parser.add_argument(
        "--hours-back",
        type=int,
        default=None,
        help="Override the lookback window in hours. Defaults to the existing weekly Eastern-time calculation.",
    )
    return parser.parse_args()


def get_default_hours_back() -> int:
    now_utc = datetime.now(timezone.utc)
    local = ZoneInfo("America/New_York")
    start_local = (
        datetime.now(local).replace(hour=0, minute=0, second=0, microsecond=0)
        - timedelta(days=7)
    )
    start_utc = start_local.astimezone(timezone.utc)
    return int((now_utc - start_utc).total_seconds() // 3600)


def execute_run(hours_back: int) -> int:
    from backend.app.database import SessionLocal, init_db
    from backend.app.services.run_tracker import RunTracker
    from backend.app.services.sc_executor import ScriptExecutor

    init_db()
    db = SessionLocal()

    run = RunTracker.create_run(db, hours_back)
    print(f"Starting run {run.id} with a {hours_back}-hour window...")

    try:
        executor = ScriptExecutor(base_dir=Path(__file__).resolve().parent)
        results = executor.execute_full_run(hours_back)

        completed_run = RunTracker.complete_run(
            db,
            run.id,
            songs=results.get("songs", []),
            albums=results.get("albums", []),
        )
        print(
            f"Run {completed_run.id} completed: "
            f"{completed_run.songs_count} songs, {completed_run.albums_count} albums, "
            f"{completed_run.duration_seconds:.2f}s"
        )
        return 0
    except Exception as exc:
        RunTracker.fail_run(db, run.id, str(exc))
        print(f"Run {run.id} failed: {exc}", file=sys.stderr)
        return 1
    finally:
        db.close()


def main() -> int:
    args = parse_args()
    hours_back = args.hours_back if args.hours_back is not None else get_default_hours_back()
    return execute_run(hours_back)


if __name__ == "__main__":
    raise SystemExit(main())
