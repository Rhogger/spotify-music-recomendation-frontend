"""
Token Manager for Spotify API
Handles authentication and access token generation with cookie-based caching
"""

import base64
import os
from datetime import datetime, timedelta

import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = "https://accounts.spotify.com/api/token"

# Cookie keys
TOKEN_COOKIE_KEY = "spotify_access_token"
TOKEN_EXPIRY_COOKIE_KEY = "spotify_token_expiry"
TOKEN_TTL_MINUTES = 50


class TokenManager:
    """Manages Spotify API access tokens with cookie-based caching."""

    def __init__(self):
        """Initialize TokenManager with credentials from environment."""
        if not CLIENT_ID or not CLIENT_SECRET:
            raise ValueError(
                "CLIENT_ID and CLIENT_SECRET must be set in .env file"
            )
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET

    def _create_auth_header(self) -> str:
        """Create base64 encoded authorization header."""
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        return f"Basic {auth_base64}"

    def _get_cached_token(self) -> tuple:
        """
        Get token from Streamlit session state (acts as client-side cookie).

        Returns:
            Tuple: (token, expiry_timestamp) or (None, None) if not found or expired
        """
        if not hasattr(st.session_state, TOKEN_COOKIE_KEY):
            return None, None

        token = st.session_state.get(TOKEN_COOKIE_KEY)
        expiry_str = st.session_state.get(TOKEN_EXPIRY_COOKIE_KEY)

        if not token or not expiry_str:
            return None, None

        try:
            expiry = datetime.fromisoformat(expiry_str)
            if datetime.now() < expiry:
                return token, expiry
        except (ValueError, TypeError):
            pass

        return None, None

    def _cache_token(self, token: str, expires_in: int) -> None:
        """
        Cache token in Streamlit session state.

        Args:
            token: Access token to cache
            expires_in: Seconds until token expires
        """
        st.session_state[TOKEN_COOKIE_KEY] = token
        expiry = datetime.now() + timedelta(seconds=expires_in - 300)  # Refresh 5min early
        st.session_state[TOKEN_EXPIRY_COOKIE_KEY] = expiry.isoformat()

    def get_access_token(self) -> str:
        """
        Get a valid access token, using cache or fetching a new one.

        Returns:
            str: Valid Spotify API access token

        Raises:
            requests.RequestException: If token request fails
            ValueError: If CLIENT_ID or CLIENT_SECRET are not set
        """
        # Check cached token first
        cached_token, expiry = self._get_cached_token()
        if cached_token:
            minutes_left = (expiry - datetime.now()).total_seconds() / 60
            print(f"✅ Using cached token ({minutes_left:.0f} minutes left)")
            return cached_token

        # Fetch new token
        headers = {
            "Authorization": self._create_auth_header(),
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {"grant_type": "client_credentials"}

        try:
            print("🔄 Fetching new Spotify access token...")
            response = requests.post(TOKEN_URL, headers=headers, data=data, timeout=10)
            response.raise_for_status()

            token_info = response.json()
            access_token = token_info["access_token"]
            expires_in = token_info.get("expires_in", 3600)

            # Cache the token
            self._cache_token(access_token, expires_in)
            print(f"✅ New token obtained (valid for {expires_in}s)")

            return access_token

        except requests.RequestException as e:
            raise RuntimeError(f"Failed to obtain Spotify access token: {e}")

    def clear_cache(self) -> None:
        """Clear cached token from session state."""
        if TOKEN_COOKIE_KEY in st.session_state:
            del st.session_state[TOKEN_COOKIE_KEY]
        if TOKEN_EXPIRY_COOKIE_KEY in st.session_state:
            del st.session_state[TOKEN_EXPIRY_COOKIE_KEY]
        print("🗑️ Token cache cleared")


# Global token manager instance
_token_manager = None


def get_token_manager() -> TokenManager:
    """Get or create the global token manager instance."""
    global _token_manager
    if _token_manager is None:
        _token_manager = TokenManager()
    return _token_manager


def get_access_token() -> str:
    """Convenience function to get access token."""
    return get_token_manager().get_access_token()


def clear_token_cache() -> None:
    """Clear the cached token."""
    get_token_manager().clear_cache()
