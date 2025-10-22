"""
Spotify API Service
Provides functions to interact with Spotify API for searching tracks and getting images
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional
from urllib.parse import quote

import requests

from .token_manager import get_access_token

SPOTIFY_API_BASE = "https://api.spotify.com/v1"


class SpotifyAPIError(Exception):
    """Custom exception for Spotify API errors."""

    pass


def search_track(
    track_name: str,
    artist_name: str,
    limit: int = 1,
) -> List[Dict]:
    """
    Search for a track on Spotify by name and artist.

    Args:
        track_name (str): Name of the track to search
        artist_name (str): Name of the artist
        limit (int): Maximum number of results to return (default: 1)

    Returns:
        List[Dict]: List of track information dictionaries containing:
            - id: Spotify track ID
            - name: Track name
            - artists: List of artist names
            - album: Album information with images
            - external_urls: Spotify URL to the track

    Raises:
        SpotifyAPIError: If the search fails
    """
    try:
        access_token = get_access_token()
    except RuntimeError as e:
        raise SpotifyAPIError(f"Could not obtain access token: {e}")

    # Build search query
    query = f"track:{track_name} artist:{artist_name}"
    encoded_query = quote(query)

    # Make API request
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "q": encoded_query,
        "type": "track",
        "limit": limit,
    }

    try:
        response = requests.get(
            f"{SPOTIFY_API_BASE}/search",
            headers=headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise SpotifyAPIError(f"Failed to search tracks: {e}")

    data = response.json()
    items = data.get("tracks", {}).get("items", [])

    if not items:
        return []

    # Extract track information
    results = []
    for track in items:
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
        results.append(track_info)

    return results


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


def _fetch_spotify_data(track_name: str, artist_name: str) -> Dict:
    """
    Internal function to fetch Spotify data for a single track.
    Used for parallel execution.

    Args:
        track_name: Name of the track
        artist_name: Name of the artist

    Returns:
        Dict with image_url and spotify_url (or None if not found)
    """
    try:
        results = search_track(track_name, artist_name, limit=1)
        if results:
            track = results[0]
            image_url = get_best_album_image(track.get("album", {}).get("images", []))
            spotify_url = track.get("external_urls", {}).get("spotify", "")
            return {
                "image_url": image_url,
                "spotify_url": spotify_url,
            }
    except Exception as e:
        print(f"⚠️ Error fetching Spotify data for {track_name}: {e}")

    return {
        "image_url": None,
        "spotify_url": None,
    }


def fetch_spotify_data_parallel(tracks: List[Dict], max_workers: int = 5) -> List[Dict]:
    """
    Fetch Spotify data for multiple tracks in parallel.

    Args:
        tracks (List[Dict]): List of track dictionaries with 'title' and 'artist' keys
        max_workers (int): Maximum number of parallel requests (default: 5)

    Returns:
        List[Dict]: List of enriched track data with image_url and spotify_url

    This function uses ThreadPoolExecutor to make up to 20 requests in parallel,
    significantly speeding up the enrichment process compared to sequential requests.
    """
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(
                _fetch_spotify_data,
                track.get("title", track.get("song", "Unknown")),
                track.get("artist", track.get("artists", "Unknown")),
            ): track
            for track in tracks
        }

        # Collect results as they complete
        for future in as_completed(futures):
            try:
                spotify_data = future.result()
                original_track = futures[future]
                results.append({
                    "title": original_track.get("title", original_track.get("song", "Unknown Title")),
                    "artist": original_track.get("artist", original_track.get("artists", "Unknown Artist")),
                    "genres": original_track.get("genres", original_track.get("genre", "")),
                    "image_url": spotify_data.get("image_url"),
                    "spotify_url": spotify_data.get("spotify_url"),
                })
            except Exception as e:
                print(f"❌ Error processing track: {e}")

    return results
