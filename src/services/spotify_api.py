from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

import requests

from .token_manager import get_access_token

SPOTIFY_API_BASE = "https://api.spotify.com/v1"


class SpotifyAPIError(Exception):
    pass


def get_track_by_id(track_id: str) -> Optional[Dict]:
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
    if not images:
        return None

    size_map = {"small": 2, "medium": 1, "large": 0}
    preferred_index = size_map.get(size, 1)

    if preferred_index < len(images):
        return images[preferred_index]["url"]

    return images[0]["url"] if images else None


def _fetch_spotify_data_by_id(track_id: str) -> Dict:
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
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                _fetch_spotify_data_by_id,
                track.get("id", ""),
            ): track
            for track in tracks
        }

        for future in as_completed(futures):
            try:
                spotify_data = future.result()
                original_track = futures[future]

                results.append(
                    {
                        "title": spotify_data.get("title", "Unknown Title"),
                        "artist": spotify_data.get("artist", "Unknown Artist"),
                        "genres": original_track.get(
                            "genres", spotify_data.get("genres", "")
                        ),
                        "image_url": spotify_data.get("image_url"),
                        "spotify_url": spotify_data.get("spotify_url"),
                    }
                )
            except Exception as e:
                print(f"❌ Error processing track: {e}")

    return results
