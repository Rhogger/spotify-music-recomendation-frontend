import streamlit as st


def slider_with_label(label, tooltip, key):
    return st.slider(label, 0, 100, 0, 1, key=key, help=tooltip)


def track_card_html(song: dict) -> str:
    """
    Generate HTML for a track card with optional image and Spotify link.

    Args:
        song (dict): Song information dictionary containing:
            - title: Track name
            - artist: Artist name(s)
            - genres: Genre(s)
            - image_url (optional): Album cover image URL
            - spotify_url (optional): Direct link to track on Spotify

    Returns:
        str: HTML string for the track card
    """
    image_url = song.get("image_url", "")
    spotify_url = song.get("spotify_url", "")
    
    # Generate image HTML
    if image_url:
        image_html = f'<img src="{image_url}" alt="{song["title"]}" class="track-image-img">'
    else:
        image_html = '<div class="track-image">🎵</div>'
    
    # Wrap card with link if spotify_url is available
    card_class = "track-card"
    if spotify_url:
        card_open = f'<a href="{spotify_url}" target="_blank" rel="noopener noreferrer" class="{card_class}-link">'
        card_close = '</a>'
    else:
        card_open = ""
        card_close = ""
    
    card_inner = f"""
        <div class="{card_class}">
            {image_html}
            <div class="track-title">{song.get("title", "Unknown")}</div>
            <div class="track-artist">{song.get("artist", "Unknown Artist")}</div>
            <div class="track-genres">{song.get("genres", "")}</div>
        </div>
    """
    
    if spotify_url:
        return f"\n{card_open}{card_inner}{card_close}\n"
    return f"\n{card_inner}\n"


def header():
    return st.markdown(
        '<div class="header-title"><div class="spotify-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="15%" fill="var(--primary-color)"/><circle cx="256" cy="256" fill="var(--text-light)" r="192"/><g fill="none" stroke="var(--primary-color)" stroke-linecap="round"><path d="m141 195c75-20 164-15 238 24" stroke-width="36"/><path d="m152 257c61-17 144-13 203 24" stroke-width="31"/><path d="m156 315c54-12 116-17 178 20" stroke-width="24"/></g></svg></div>Recomendações Spotify</div>',
        unsafe_allow_html=True,
    )
