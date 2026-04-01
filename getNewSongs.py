# getNewSongs.py
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from alive_progress import alive_bar
import os, requests

# ----------------------------
# Config
# ----------------------------
API_BASE = "https://api.soundcloud.com"
ACCESS_VALUES = "playable,preview,blocked"

# Default time filter logic:
#   "activity" -> filter by activity.created_at (when it hit your feed)
#   "upload"   -> filter by origin.created_at  (true upload time)
#   "both"     -> require BOTH to be inside window
FILTER_MODE = os.getenv("SC_FILTER_MODE", "activity").lower()  # activity|upload|both

# Target playlist (can also set SC_PLAYLIST_ID env var)
PLAYLIST_ID = os.getenv("SC_PLAYLIST_ID", "1907305003")


# ----------------------------
# Helpers
# ----------------------------
def _parse_sc_time(s: str) -> datetime:
    # supports "YYYY/MM/DD HH:MM:SS +0000" and ISO "YYYY-MM-DDTHH:MM:SSZ" variants
    if not s:
        raise ValueError("empty time")
    try:
        # legacy SoundCloud format
        dt = datetime.strptime(s, "%Y/%m/%d %H:%M:%S %z")
        return dt.astimezone(timezone.utc)
    except Exception:
        pass
    try:
        # ISO-ish
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        # last attempt: strip fractional seconds if present
        if "." in s:
            base, rest = s.split(".", 1)
            if "+" in rest:
                frac, tz = rest.split("+", 1)
                s2 = base + "+%s" % tz
            elif "-" in rest:
                frac, tz = rest.split("-", 1)
                s2 = base + "-%s" % tz
            else:
                s2 = base + "Z"
            return _parse_sc_time(s2)
        raise

def _is_original_track(activity: dict) -> bool:
    t = (activity.get("type") or "").lower()
    origin = activity.get("origin") or {}
    return origin.get("kind") == "track" and "repost" not in t

def _as_str(x):
    return x if isinstance(x, str) else (x or "")

def _ensure_access_in_url(url: str) -> str:
    if "access=" in url:
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}access={ACCESS_VALUES}"

def _get_page(sc, href_or_path: str, *, params: Optional[Dict] = None) -> Dict:
    """
    Always enforces access=playable,preview,blocked when calling SoundCloud.
    Works for both absolute URLs (next_href) and API paths.
    """
    if href_or_path.startswith("http"):
        url = _ensure_access_in_url(href_or_path)
        return sc.get(url)
    else:
        params = dict(params or {})
        params.setdefault("access", ACCESS_VALUES)
        return sc.get(href_or_path, **params)

def _within_window(activity_dt: Optional[datetime], upload_dt: Optional[datetime], cutoff: datetime) -> bool:
    """
    Interprets the time filter according to FILTER_MODE.
    cutoff = now_utc - hours
    """
    if FILTER_MODE == "activity":
        return bool(activity_dt and activity_dt >= cutoff)
    if FILTER_MODE == "upload":
        return bool(upload_dt and upload_dt >= cutoff)
    # both
    return bool(activity_dt and activity_dt >= cutoff and upload_dt and upload_dt >= cutoff)


# ----------------------------
# Core fetch logic
# ----------------------------
def fetch_following_tracks_last_hours(sc, hours: int) -> Tuple[List[Dict], Optional[str]]:
    """
    Walks /me/activities/tracks with pagination.
    Returns (items, future_href).
    Keeps ONLY ORIGINAL uploads within the last <hours>, using FILTER_MODE.
    """
    now_utc = datetime.now(timezone.utc)
    cutoff = now_utc - timedelta(hours=hours)

    url = "/me/activities/tracks"
    params = {
        "linked_partitioning": 1,
        "access": ACCESS_VALUES,
        "limit": 50,
    }

    out: List[Dict] = []
    page = _get_page(sc, url, params=params)
    future_href = page.get("future_href")

    def handle_page(p: Dict) -> Tuple[Optional[str], int, Optional[datetime]]:
        col = p.get("collection", []) or []
        kept_on_page = 0
        newest_activity_dt: Optional[datetime] = None

        with alive_bar(len(col), title="Going Through Artists", bar="filling") as bar:
            for a in col:
                bar()
                if not _is_original_track(a):
                    continue

                tr = a.get("origin") or {}
                # Parse both timestamps when available
                act_dt = None
                up_dt = None
                try:
                    if a.get("created_at"):
                        act_dt = _parse_sc_time(a["created_at"])
                except Exception:
                    pass
                try:
                    if tr.get("created_at"):
                        up_dt = _parse_sc_time(tr["created_at"])
                    else:
                        # fallback to activity if upload missing
                        up_dt = act_dt
                except Exception:
                    up_dt = None

                # track newest activity time on the page for early-stop
                if act_dt and (newest_activity_dt is None or act_dt > newest_activity_dt):
                    newest_activity_dt = act_dt

                # Strict window check according to mode
                if not _within_window(act_dt, up_dt, cutoff):
                    continue

                out.append({
                    "activity_created_at": a.get("created_at"),
                    "track_id": tr.get("id"),
                    "track_title": tr.get("title"),
                    "track_permalink_url": tr.get("permalink_url"),
                    "uploader_username": (tr.get("user") or {}).get("username"),
                    "access": _as_str(a.get("access")),
                    "sharing": _as_str(tr.get("sharing")),
                    "streamable": tr.get("streamable"),
                    "uploaded_at": up_dt.isoformat() if up_dt else None,
                })
                kept_on_page += 1

        next_href = p.get("next_href")
        if next_href:
            next_href = _ensure_access_in_url(next_href)
        return next_href, kept_on_page, newest_activity_dt

    next_href, kept, newest = handle_page(page)

    # Follow next_href EXACTLY; stop once the page's NEWEST activity is older than cutoff.
    while next_href:
        page = _get_page(sc, next_href)
        next_href, kept, newest = handle_page(page)

        # **Authoritative early-stop**: activities are reverse-chron; if newest on this page
        # is older than cutoff, all subsequent pages will be older too.
        if newest and newest < cutoff:
            break

    # Dedupe by id (stable)
    seen = set()
    deduped = []
    for it in out:
        tid = it.get("track_id")
        if tid and tid not in seen:
            seen.add(tid)
            deduped.append(it)

    return deduped, future_href


def get_playlist_track_ids(sc, playlist_id: str) -> List[int]:
    pl = _get_page(sc, f"/playlists/{playlist_id}")
    return [t["id"] for t in (pl.get("tracks") or []) if t and t.get("id")]


def update_playlist_tracks(sc, playlist_id: str, add_ids: List[int], preserve_existing: bool = False) -> Dict:
    """
    Replace-all update:
      - If preserve_existing, union(existing, add_ids) in stable order
      - Else, set playlist to exactly add_ids (this clears playlist if add_ids is empty).
    Sends URNs as required by the API.
    """
    if preserve_existing:
        existing = get_playlist_track_ids(sc, playlist_id)
    else:
        existing = []

    # Build desired order (stable, deduped)
    desired_order = []
    seen = set()
    for x in (existing + add_ids) if preserve_existing else add_ids:
        try:
            xi = int(x)
        except Exception:
            continue
        if xi not in seen:
            seen.add(xi)
            desired_order.append(xi)

    # Build headers from SCClient (token)
    if hasattr(sc, "_headers"):
        headers = sc._headers()
    elif hasattr(getattr(sc, "session", None), "headers"):
        headers = {"Authorization": sc.session.headers.get("Authorization", "")}
    else:
        raise RuntimeError("Can't extract token from SCClient; pass it manually.")
    headers.update({"Accept": "application/json", "Content-Type": "application/json"})

    # ✅ Always PUT — even if empty — to fully replace (clear) the playlist
    payload = {"playlist": {"tracks": [{"urn": f"soundcloud:tracks:{t}"} for t in desired_order]}}
    url = f"{API_BASE}/playlists/{playlist_id}"
    r = requests.put(url, headers=headers, json=payload, timeout=30)
    if r.status_code >= 400:
        try:
            print("PUT error body:", r.json())
        except Exception:
            print("PUT error text:", r.text)
        r.raise_for_status()
    return r.json()


# ----------------------------
# Public entrypoint (matches your runner)
# ----------------------------
from soundAuthen import SCClient  # your existing auth wrapper

def main(hours: int):
    """
    Finds ORIGINAL tracks within the last `hours` according to FILTER_MODE and adds them to PLAYLIST_ID.
    Returns the playlist update API response (dict).
    """
    sc = SCClient()

    # 1) Gather candidates within time window
    recent, _future = fetch_following_tracks_last_hours(sc, hours)
    new_ids = [i["track_id"] for i in recent if i.get("track_id")]

    # 2) Replace playlist with ONLY these tracks (no preserve)
    resp = update_playlist_tracks(sc, PLAYLIST_ID, new_ids, preserve_existing=False)

    mode = FILTER_MODE
    print(f"[Songs] Mode={mode} | Window last {hours} hour(s): {len(new_ids)} candidate(s).")
    track_count = resp.get("track_count", len(resp.get("tracks", []) or []))
    print(f"[Songs] Playlist now shows {track_count} visible track(s).")

    return resp
