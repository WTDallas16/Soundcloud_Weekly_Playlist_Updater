from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import getNewSongs
import getNewAlbums

def get_hours_past_week():
    now_utc = datetime.now(timezone.utc)
    local = ZoneInfo("America/New_York")
    start_local = (datetime.now(local).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7))
    start_utc = start_local.astimezone(timezone.utc)
    hours = int((now_utc - start_utc).total_seconds() // 3600)
    return hours

def main(hours):
    playlist_up = getNewSongs.main(hours)
    album_up = getNewAlbums.main(hours)
    return playlist_up, album_up
    # return playlist_up

if __name__ == "__main__":
    time_frame = get_hours_past_week()
    main(time_frame)