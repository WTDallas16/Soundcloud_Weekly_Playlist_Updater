import requests
from typing import Dict, Any, Optional
from .sc_auth import SCAuthService

class SCClient:
    """
    Reimplementation of the external soundAuthen.SCClient
    Provides authenticated SoundCloud API access with automatic token refresh
    """

    API_BASE = "https://api.soundcloud.com"

    def __init__(self, auth_service: Optional[SCAuthService] = None):
        self.auth_service = auth_service or SCAuthService()

    def _headers(self) -> Dict[str, str]:
        """Get headers with valid access token"""
        token = self.auth_service.get_valid_token()
        return {
            'Authorization': f'OAuth {token}',
            'Accept': 'application/json'
        }

    def get(self, url: str, **params) -> Dict[str, Any]:
        """
        Make authenticated GET request to SoundCloud API

        Args:
            url: Either a full URL (for pagination) or an API path
            **params: Query parameters

        Returns:
            JSON response as dict
        """
        # Handle both full URLs (pagination) and API paths
        if url.startswith('http'):
            full_url = url
        else:
            # Ensure path starts with /
            path = url if url.startswith('/') else f'/{url}'
            full_url = f"{self.API_BASE}{path}"

        response = requests.get(full_url, headers=self._headers(), params=params)
        response.raise_for_status()
        return response.json()

    def likeIt(self, playlist_id: str) -> bool:
        """
        Like a playlist/album on SoundCloud

        Args:
            playlist_id: The SoundCloud playlist ID

        Returns:
            True if successful, False otherwise
        """
        # Match the original soundAuthen implementation
        headers = self._headers()
        headers.update({"accept": "application/json; charset=utf-8"})

        url = f"{self.API_BASE}/likes/playlists/{int(playlist_id)}"

        try:
            response = requests.post(url, headers=headers, timeout=20)
            # 200/201/204 are all success codes
            if response.status_code in (200, 201, 204):
                return True
            else:
                print(f"Failed to like playlist {playlist_id}: {response.status_code} {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Failed to like playlist {playlist_id}: {e}")
            return False

    def update_playlist(self, playlist_id: str, track_ids: list) -> Dict[str, Any]:
        """
        Update playlist with new tracks (replace-all strategy)

        Args:
            playlist_id: The SoundCloud playlist ID
            track_ids: List of track IDs to set as playlist content

        Returns:
            JSON response from API
        """
        url = f"{self.API_BASE}/playlists/{playlist_id}"

        # Convert track IDs to URN format
        track_urns = [{"id": f"soundcloud:tracks:{track_id}"} for track_id in track_ids]

        payload = {
            "playlist": {
                "tracks": track_urns
            }
        }

        response = requests.put(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()
