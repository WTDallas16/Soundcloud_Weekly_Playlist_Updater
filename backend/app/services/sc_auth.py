import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional
from ..config import settings

class SCAuthService:
    """Handles SoundCloud OAuth token management with automatic refresh"""

    TOKEN_URL = "https://secure.soundcloud.com/oauth/token"
    REFRESH_BUFFER_MINUTES = 5  # Refresh tokens 5 minutes before expiry

    def __init__(self, token_file: Optional[Path] = None):
        self.token_file = token_file or settings.token_file
        self._token_data: Optional[Dict] = None

    def load_token(self) -> Dict:
        """Load token from file"""
        if not self.token_file.exists():
            raise FileNotFoundError(f"Token file not found: {self.token_file}")

        with open(self.token_file, 'r') as f:
            self._token_data = json.load(f)

        return self._token_data

    def save_token(self, token_data: Dict) -> None:
        """Save token to file"""
        self._token_data = token_data
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f, indent=2)

    def is_token_expired(self) -> bool:
        """Check if token is expired or will expire soon"""
        if not self._token_data:
            self.load_token()

        expires_at = self._token_data.get('expires_at')
        if not expires_at:
            return True

        # Parse expires_at - could be timestamp or ISO string
        if isinstance(expires_at, (int, float)):
            expiry_time = datetime.fromtimestamp(expires_at)
        else:
            expiry_time = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))

        # Check if expired or will expire within buffer period
        buffer_time = datetime.now() + timedelta(minutes=self.REFRESH_BUFFER_MINUTES)
        return expiry_time <= buffer_time

    def refresh_token(self) -> Dict:
        """Refresh the access token using refresh_token"""
        if not self._token_data:
            self.load_token()

        refresh_token = self._token_data.get('refresh_token')
        if not refresh_token:
            raise ValueError("No refresh_token found in token data")

        payload = {
            'grant_type': 'refresh_token',
            'client_id': settings.sc_client_id,
            'client_secret': settings.sc_client_secret,
            'refresh_token': refresh_token
        }

        response = requests.post(self.TOKEN_URL, data=payload)
        response.raise_for_status()

        new_token_data = response.json()

        # Calculate expires_at timestamp
        expires_in = new_token_data.get('expires_in', 3600)
        new_token_data['expires_at'] = (datetime.now() + timedelta(seconds=expires_in)).timestamp()

        # Preserve refresh_token if not included in response
        if 'refresh_token' not in new_token_data:
            new_token_data['refresh_token'] = refresh_token

        self.save_token(new_token_data)
        return new_token_data

    def get_valid_token(self) -> str:
        """Get a valid access token, refreshing if necessary"""
        if not self._token_data:
            self.load_token()

        if self.is_token_expired():
            self.refresh_token()

        return self._token_data['access_token']

    def get_token_info(self) -> Dict:
        """Get token information for status checks"""
        if not self._token_data:
            try:
                self.load_token()
            except FileNotFoundError:
                return {'authenticated': False, 'message': 'Token file not found'}

        expires_at = self._token_data.get('expires_at')
        if expires_at:
            if isinstance(expires_at, (int, float)):
                expiry_time = datetime.fromtimestamp(expires_at)
            else:
                expiry_time = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
        else:
            expiry_time = None

        return {
            'authenticated': True,
            'token_expires_at': expiry_time,
            'is_expired': self.is_token_expired()
        }
