# # # main.py
from pathlib import Path
from datetime import datetime, timedelta, timezone

from alive_progress import alive_bar
from soundAuthen import SCClient

sc = SCClient()

ALBUM_TYPES = {"ALBUM", "EP", "COMPILATION"}
ALBUMS_ADDED_FILE = Path(__file__).resolve().with_name("albums_added.txt")

# -------- helpers --------
def _parse_sc_time(s: str) -> datetime:
    # e.g. "2015/04/06 17:47:05 +0000"
    return datetime.strptime(s, "%Y/%m/%d %H:%M:%S %z")

def _is_original_track(activity: dict) -> bool:
    # Keep original uploads; skip repost activities
    t = (activity.get("type") or "").lower()
    origin = activity.get("origin") or {}
    return origin.get("kind") == "playlist" and "repost" not in t

def activities(hours):
    url = "/me/activities/all/own"   # fallback to "/me/activities" if needed
    params = {
        "linked_partitioning": 1,
        "access": "playable,preview,blocked",  # include blocked
        "limit": 200,                          # large page size; still filter by time in code
    }
    out = sc.get(url, **params)
    future_href = out.get("future_href")

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

    out_list = []

    def find_albums(p):
        ll = list(p.get("collection", []))
        with alive_bar(len(ll), title="Going Through Albums", bar="filling") as bar:
            for a in p.get("collection", []):
                bar()
                if not _is_original_track(a):
                    continue
                a_time = _parse_sc_time(a["created_at"])
                dd = a.get("origin")
                lowercased_elements = {item.lower() for item in ALBUM_TYPES}
                if dd.get("kind") == "playlist" and dd.get("playlist_type").lower() in lowercased_elements and dd.get("track_count") > 2 and a_time >= cutoff:
                    # playlistId = dd.get("id")
                    # sc.likeIt(playlistId)
                    out_dict = {
                        "activity_created_at": dd.get("created_at"),  # when it hit your feed
                        "playlist_id": dd.get("id"),
                        "playlist_urn": dd.get("urn"),
                        "title": dd.get("title"),
                        "playlist_type": dd.get("playlist_type") or dd.get("type"),
                        "permalink_url": dd.get("permalink_url"),
                        "uploader": (dd.get("user") or {}).get("username"),
                        "Track Count": dd.get("track_count")
                        }
                    out_list.append(out_dict)
            return p.get("next_href")
        
    next_href = find_albums(out)

    # 2) Older pages via next_href (follow EXACTLY; don't add params)
    while next_href:
        page = sc.get(next_href)
        next_href = find_albums(page)

        # Optional early break: if this whole page is older than cutoff, stop
        col = page.get("collection", [])
        if col:
            newest_this_page = max(_parse_sc_time(a["created_at"]) for a in col)
            if newest_this_page < cutoff:
                break

    return out_list, future_href

def poll_new_with_future_href(future_href, hours):
    """
    Use the saved future_href to fetch items that appeared AFTER your last baseline call.
    Returns (new_items, next_future_href).
    """
    if not future_href:
        return [], None
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    p_new = sc.get(future_href)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

    out_list = []

    ll = list(p_new.get("collection", []))
    with alive_bar(len(ll), title="Going Through Albums", bar="filling") as bar:
        for a in p_new.get("collection", []):
            bar()
            if not _is_original_track(a):
                continue
            a_time = _parse_sc_time(a["created_at"])
            dd = a.get("origin")
            if dd.get("kind") == "playlist" and dd.get("playlist_type") in ALBUM_TYPES and dd.get("track_count") > 2 and a_time >= cutoff:
                # playlistId = dd.get("id")
                # sc.likeIt(playlistId)
                out_dict = {
                    "activity_created_at": dd.get("created_at"),  # when it hit your feed
                    "playlist_id": dd.get("id"),
                    "playlist_urn": dd.get("urn"),
                    "title": dd.get("title"),
                    "playlist_type": dd.get("playlist_type") or dd.get("type"),
                    "permalink_url": dd.get("permalink_url"),
                    "uploader": (dd.get("user") or {}).get("username"),
                    "Track Count": dd.get("track_count")
                    }
                out_list.append(out_dict)
        return out_list, p_new.get("future_href")

def main(hours):
    hour_range = hours
    recent, future = activities(hour_range)
    new_items, future = poll_new_with_future_href(future, hour_range)

    all = recent + new_items

    new_ids = [i["playlist_id"] for i in all if i.get("playlist_id")]
    new_names = [i["title"] for i in all if i.get("title")]

    to_add = []

    ALBUMS_ADDED_FILE.touch(exist_ok=True)
    existing_ids = {line.strip() for line in ALBUMS_ADDED_FILE.read_text().splitlines() if line.strip()}

    with ALBUMS_ADDED_FILE.open("a", encoding="utf-8") as f:
        for i in new_ids:
            if str(i) in existing_ids:
                continue
            f.write(f"{i}\n")
            to_add.append(i)
            sc.likeIt(str(i))

    print(f"{len(to_add)} Albums have been liked!")
    if len(to_add) > 0:
        print(f"Albums liked: {to_add}")

# if __name__ == "__main__":
#     main(100)
