"""
Spotify API Service
Provides functions to interact with Spotify API for fetching tracks by ID
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

import requests

from .token_manager import get_access_token

SPOTIFY_API_BASE = "https://api.spotify.com/v1"


class SpotifyAPIError(Exception):
    """Custom exception for Spotify API errors."""

    pass


def get_track_by_id(track_id: str) -> Optional[Dict]:
    """
    Get track information from Spotify by track ID.

    Args:
        track_id (str): Spotify track ID

    Returns:
        Optional[Dict]: Track information dictionary containing:
            - id: Spotify track ID
            - name: Track name
            - artists: List of artist names
            - album: Album information with images
            - external_urls: Spotify URL to the track
            - genres: List of genres (if available)

    Raises:
        SpotifyAPIError: If the request fails
    """
    try:
        access_token = get_access_token()
    except RuntimeError as e:
        raise SpotifyAPIError(f"Could not obtain access token: {e}")

    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(
            f"{SPOTIFY_API_BASE}/tracks/{track_id}",
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise SpotifyAPIError(f"Failed to fetch track {track_id}: {e}")

    track = response.json()

    track_info = {
        "id": track["id"],
        "name": track["name"],
        "artists": [artist["name"] for artist in track["artists"]],
        "album": {
            "name": track["album"]["name"],
            "images": track["album"].get("images", []),
        },
        "external_urls": track.get("external_urls", {}),
    }

    return track_info


def get_best_album_image(images: List[Dict], size: str = "medium") -> Optional[str]:
    """
    Get the best album image URL based on size preference.

    Args:
        images (List[Dict]): List of image dictionaries from Spotify
        size (str): Size preference - 'small' (64x64), 'medium' (300x300), 'large' (640x640)

    Returns:
        Optional[str]: Image URL or None if no images available

    Sizes in Spotify:
        - 0: 640x640
        - 1: 300x300
        - 2: 64x64
    """
    if not images:
        return None

    size_map = {"small": 2, "medium": 1, "large": 0}
    preferred_index = size_map.get(size, 1)

    # Try to get the preferred size
    if preferred_index < len(images):
        return images[preferred_index]["url"]

    # Fallback to the first available image
    return images[0]["url"] if images else None


def _fetch_spotify_data_by_id(track_id: str) -> Dict:
    """
    Internal function to fetch Spotify data for a single track by ID.
    Used for parallel execution.

    Args:
        track_id: Spotify track ID

    Returns:
        Dict with title, artist, image_url, spotify_url, and genres
    """
    try:
        track = get_track_by_id(track_id)
        if track:
            image_url = get_best_album_image(track.get("album", {}).get("images", []))
            spotify_url = track.get("external_urls", {}).get("spotify", "")
            artists = ", ".join(track.get("artists", []))

            return {
                "title": track.get("name", "Unknown"),
                "artist": artists,
                "image_url": image_url,
                "spotify_url": spotify_url,
                "genres": "",
            }
    except Exception as e:
        print(f"⚠️ Error fetching Spotify data for track {track_id}: {e}")

    return {
        "title": "Unknown",
        "artist": "Unknown Artist",
        "image_url": None,
        "spotify_url": None,
        "genres": "",
    }


def fetch_spotify_data_parallel(tracks: List[Dict], max_workers: int = 5) -> List[Dict]:
    """
    Fetch Spotify data for multiple tracks in parallel using track IDs.

    Args:
        tracks (List[Dict]): List of track dictionaries with 'id' key (Spotify track ID)
        max_workers (int): Maximum number of parallel requests (default: 5)

    Returns:
        List[Dict]: List of enriched track data with title, artist, image_url, spotify_url, and genres

    This function uses ThreadPoolExecutor to make requests in parallel,
    significantly speeding up the enrichment process compared to sequential requests.
    """
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(
                _fetch_spotify_data_by_id,
                track.get("id", ""),
            ): track
            for track in tracks
        }

        # Collect results as they complete
        for future in as_completed(futures):
            try:
                spotify_data = future.result()
                original_track = futures[future]

                # Merge original track data with Spotify data
                results.append(
                    {
                        "title": spotify_data.get("title", "Unknown Title"),
                        "artist": spotify_data.get("artist", "Unknown Artist"),
                        "genres": original_track.get("genres", spotify_data.get("genres", "")),
                        "image_url": spotify_data.get("image_url"),
                        "spotify_url": spotify_data.get("spotify_url"),
                    }
                )
            except Exception as e:
                print(f"❌ Error processing track: {e}")

    return results
