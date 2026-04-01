import sys
import importlib.util
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from .sc_client import SCClient
from .sc_auth import SCAuthService

class ScriptExecutor:
    """
    Wraps existing getNewSongs.py and getNewAlbums.py scripts
    Uses dynamic import and monkey-patching to inject SCClient
    """

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent.parent.parent
        self.auth_service = SCAuthService()
        self.sc_client = SCClient(self.auth_service)

        # Set up fake soundAuthen module BEFORE any imports
        self._setup_soundauthen_module()

    def _setup_soundauthen_module(self):
        """Set up fake soundAuthen module before any script imports"""
        if 'soundAuthen' not in sys.modules:
            import types
            soundAuthen = types.ModuleType('soundAuthen')
            soundAuthen.SCClient = lambda token_file=None: self.sc_client
            sys.modules['soundAuthen'] = soundAuthen

    def _import_module(self, module_name: str, file_path: Path):
        """Dynamically import a Python module from file path"""
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load module from {file_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def run_songs(self, hours_back: float) -> Dict[str, Any]:
        """
        Execute song fetching logic from getNewSongs.py

        Args:
            hours_back: Number of hours to look back

        Returns:
            Dict with 'songs' list
        """
        songs_script = self.base_dir / "getNewSongs.py"
        if not songs_script.exists():
            raise FileNotFoundError(f"Script not found: {songs_script}")

        # Import the module (soundAuthen already set up in __init__)
        songs_module = self._import_module("getNewSongs_dynamic", songs_script)

        try:
            # Call fetch_following_tracks_last_hours function
            songs_list, future_href = songs_module.fetch_following_tracks_last_hours(
                self.sc_client,
                int(hours_back)
            )

            # Extract track IDs
            new_ids = [song.get('track_id') for song in songs_list if song.get('track_id')]

            # Update playlist with new songs (replace-all strategy)
            if new_ids:
                playlist_id = songs_module.PLAYLIST_ID
                print(f"Updating playlist {playlist_id} with {len(new_ids)} songs...")
                songs_module.update_playlist_tracks(
                    self.sc_client,
                    playlist_id,
                    new_ids,
                    preserve_existing=False
                )
                print(f"✓ Playlist updated successfully")

            # Convert to expected format
            formatted_songs = []
            for song in songs_list:
                formatted_songs.append({
                    'track_id': song.get('track_id'),
                    'track_title': song.get('track_title', ''),
                    'track_permalink_url': song.get('track_permalink_url', ''),
                    'uploader_username': song.get('uploader_username', ''),
                    'uploaded_at': song.get('uploaded_at'),
                    'activity_created_at': song.get('activity_created_at')
                })

            return {
                'songs': formatted_songs,
                'future_href': future_href,
                'playlist_updated': len(new_ids) > 0
            }

        except Exception as e:
            print(f"Error in run_songs: {e}")
            import traceback
            traceback.print_exc()
            raise

    def run_albums(self, hours_back: float) -> Dict[str, Any]:
        """
        Execute album fetching logic from getNewAlbums.py

        Args:
            hours_back: Number of hours to look back

        Returns:
            Dict with 'albums' list
        """
        albums_script = self.base_dir / "getNewAlbums.py"
        if not albums_script.exists():
            raise FileNotFoundError(f"Script not found: {albums_script}")

        # Import the module (soundAuthen already set up in __init__)
        albums_module = self._import_module("getNewAlbums_dynamic", albums_script)

        try:
            # Call activities function to get albums
            albums_list, future_href = albums_module.activities(int(hours_back))

            # Also poll future_href if needed
            if future_href:
                new_albums, future_href = albums_module.poll_new_with_future_href(
                    future_href,
                    int(hours_back)
                )
                albums_list.extend(new_albums)

            # Deduplicate by playlist_id
            seen_ids = set()
            unique_albums = []
            for album in albums_list:
                playlist_id = str(album.get('playlist_id'))
                if playlist_id not in seen_ids:
                    seen_ids.add(playlist_id)
                    unique_albums.append(album)

            # Like each album and format response
            formatted_albums = []
            for album in unique_albums:
                playlist_id = str(album.get('playlist_id'))
                try:
                    success = self.sc_client.likeIt(playlist_id)
                    liked_status = 'yes' if success else 'failed'
                except Exception as e:
                    print(f"Error liking album {playlist_id}: {e}")
                    liked_status = 'failed'

                formatted_albums.append({
                    'playlist_id': playlist_id,
                    'title': album.get('title', ''),
                    'playlist_type': album.get('playlist_type', ''),
                    'permalink_url': album.get('permalink_url', ''),
                    'uploader': album.get('uploader', ''),
                    'track_count': album.get('Track Count', 0),
                    'activity_created_at': album.get('activity_created_at'),
                    'liked': liked_status
                })

            return {
                'albums': formatted_albums,
                'future_href': future_href
            }

        except Exception as e:
            print(f"Error in run_albums: {e}")
            import traceback
            traceback.print_exc()
            raise

    def execute_full_run(self, hours_back: float) -> Dict[str, Any]:
        """
        Execute both songs and albums fetching

        Args:
            hours_back: Number of hours to look back

        Returns:
            Dict with 'songs' and 'albums' lists
        """
        try:
            songs_result = self.run_songs(hours_back)
            albums_result = self.run_albums(hours_back)

            return {
                'songs': songs_result.get('songs', []),
                'albums': albums_result.get('albums', [])
            }
        except Exception as e:
            raise RuntimeError(f"Script execution failed: {str(e)}") from e
