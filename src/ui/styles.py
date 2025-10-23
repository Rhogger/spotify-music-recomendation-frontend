# =============================================================================
# Design System - Color Variables
# =============================================================================
# All colors extracted from .streamlit/config.toml for consistency across the app
# Use these variables throughout the frontend for a cohesive design system
# =============================================================================

# Primary Brand Colors
PRIMARY_COLOR = "#38E07B"  # Primary green - buttons, highlights, accents
BACKGROUND_COLOR = "#122017"  # Main application background
SECONDARY_BACKGROUND = "#292D2A"  # Sidebar background and slider track

# Text Colors
TEXT_COLOR = "#BFC2C0"  # Main text color
TEXT_SECONDARY = "#B3B3B3"  # Secondary text (labels, descriptions)
TEXT_LIGHT = "#FFFFFF"  # Light/bright text

# UI Elements
BORDER_COLOR = "#2A362E"  # Borders and separators
SPOTIFY_ACCENT = "#1DB954"  # Alternative green accent
DARK_BG = "#0A1612"  # Very dark background (gradients)
CARD_BG_LIGHT = "rgba(41, 45, 42, 0.3)"  # Card background with transparency


def get_color_variables() -> str:
    """Returns CSS color variables for use in styles."""
    return f"""
    :root {{
        --primary-color: {PRIMARY_COLOR};
        --background-color: {BACKGROUND_COLOR};
        --secondary-background: {SECONDARY_BACKGROUND};
        --text-color: {TEXT_COLOR};
        --text-secondary: {TEXT_SECONDARY};
        --text-light: {TEXT_LIGHT};
        --border-color: {BORDER_COLOR};
        --spotify-accent: {SPOTIFY_ACCENT};
        --dark-bg: {DARK_BG};
        --card-bg-light: {CARD_BG_LIGHT};
    }}
    """


def load_styles() -> str:
    return f"""
    <style>
        {get_color_variables()}
        
        ._container*, ._profileContainer* {{
            display: none;
        }}

        body, .main, .block-container {{
            background: linear-gradient(180deg, #1a3a2e 0%, var(--dark-bg) 100%) !important;
            color: var(--text-light) !important;
        }}
        
        .stAppHeader {{
            display: none;
        }}
        
        .stMainBlockContainer {{
            padding: 0px;
            overflow: hidden;
        }}
        
        .stMainBlockContainer {{
            background: var(--background-color) !important;
        }}
        
        .stMainBlockContainer > div {{
            gap: 0;
        }}
        
        .stMainBlockContainer > div > div:first-child{{
            display: none;
        }}
        
        .stMainBlockContainer > div > div:last-child{{
            padding-top: 71.4px;
        }}
        
        div:has(.stForm) {{
            height: 100%;
        }}
        
        .stForm{{
            padding: 0px;
        }}
        
        .stForm > div {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        
        .stColumn {{
            padding: 32px;
        }}
        
        .stColumn:first-child {{
            border-width: 0px 1px 0px 0px;
            border-color: var(--border-color);
            border-style: solid;
        }}
        
                
        .stColumn:last-child {{
            overflow-y: auto;
            height: calc(100vh - 71.4px);
        }}
        
        .stColumn:last-child::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .stColumn:last-child::-webkit-scrollbar-thumb {{
            background-color: var(--primary-color);
            border-radius: 10px;
        }}
        
        .stColumn:last-child::-webkit-scrollbar-track {{
            background: var(--secondary-background);
        }}

        .header-title {{
            position: absolute;
            top: 0px;
            left: 0px;
            
            width: 100%;
            display: flex;
            align-items: center;
            gap: 1rem;
            font-size: 1.5rem;
            font-weight: 700;
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .spotify-icon {{
            width: 32px;
            height: 32px;
            background: var(--primary-color);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 20px;
            color: var(--background-color);
        }}
        
        h3 {{
            padding: 0px !important;
            margin-bottom: 16px !important;
            color: var(--text-light) !important;
        }}
        
        h3 > span {{
            display: none !important;
        }}
        
        .slider-label {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.75rem;
            font-size: 0.95rem;
        }}
        
        .slider-label span:first-child {{
            color: var(--text-secondary);
        }}
        
        .slider-label span:last-child {{
            color: var(--text-light);
            font-weight: 600;
        }}

        button[data-testid="stBaseButton-primaryFormSubmit"] > div > p {{
            font-weight: 700;
            color: var(--background-color);
        }}
        
        .tracks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 0.35rem;
            grid-auto-rows: 1fr;
        }}
        
        .track-card {{
            background: var(--card-bg-light);
            border-radius: 12px;
            padding: 1rem;
            transition: background 0.3s, border-color 0.3s, transform 0.2s;
            cursor: pointer;
            border: 1px solid transparent;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        .track-card:hover {{
            background: rgba(0,0,0,0.5);
            border-color: var(--primary-color);
            transform: translateY(-4px);
        }}

        .track-card-link {{
            text-decoration: none !important;
            display: block;
            transition: transform 0.2s;
        }}
        
        .track-image {{
            width: 100%;
            aspect-ratio: 1;
            background: linear-gradient(135deg, var(--secondary-background) 0%, var(--border-color) 100%);
            border-radius: 8px;
            margin-bottom: 1rem;
            display: block;
            overflow: hidden;
            flex: 0 0 auto;
        }}

        .track-image-img {{
            width: 100%;
            height: 100%;
            aspect-ratio: 1;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 1rem;
            display: block;
        }}
        
        .track-title-wrapper {{
            width: 100%;
            overflow: hidden;
            margin-bottom: 0.25rem;
        }}
        
        .track-title {{
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-light);
            white-space: nowrap;
            width: auto;
            display: block;
            outline: none !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }}

        .track-title:focus {{
            outline: none !important;
            border: none !important;
            box-shadow: none !important;
        }}

        .track-title.has-overflow {{
            animation: none;
        }}

        .track-title.has-overflow:hover {{
            animation: scrollText 5s linear infinite;
        }}
        
        .track-artist-wrapper {{
            width: 100%;
            overflow: hidden;
            margin-bottom: 0.5rem;
        }}

        .track-artist {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            white-space: nowrap;
            width: auto;
            display: block;
            outline: none !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }}

        .track-artist:focus {{
            outline: none !important;
            border: none !important;
            box-shadow: none !important;
        }}

        .track-artist.has-overflow {{
            animation: none;
        }}

        .track-artist.has-overflow:hover {{
            animation: scrollText 5s linear infinite;
        }}
        
        .track-genres-wrapper {{
            width: 100%;
            overflow: hidden;
            margin-top: auto;
        }}
        
        .track-genres {{
            font-size: 0.8rem;
            color: var(--primary-color);
            font-weight: 500;
            white-space: nowrap;
            width: auto;
            display: block;
            text-transform: capitalize;
            outline: none !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }}

        .track-genres:focus {{
            outline: none !important;
            border: none !important;
            box-shadow: none !important;
        }}

        .track-genres.has-overflow {{
            animation: none;
        }}

        .track-genres.has-overflow:hover {{
            animation: scrollText 5s linear infinite;
        }}
        
        .scrollable-list {{
            padding-bottom: 32px;
        }}

        .placeholder-instruction {{
            background: linear-gradient(135deg, rgba(56, 224, 123, 0.1) 0%, rgba(41, 45, 42, 0.3) 100%);
            border: 2px solid var(--primary-color);
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            align-items: center;
            text-align: center;
        }}

        .placeholder-instruction .icon {{
            font-size: 3rem;
            animation: float 3s ease-in-out infinite;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}

        .placeholder-instruction h2 {{
            color: var(--primary-color);
            font-size: 1.5rem;
            margin: 0;
            font-weight: 700;
        }}

        .placeholder-instruction .content {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            color: var(--text-color);
            line-height: 1.6;
        }}

        .placeholder-instruction .step {{
            display: flex;
            align-items: flex-start;
            gap: 1rem;
        }}

        .placeholder-instruction .step-number {{
            background: var(--primary-color);
            color: var(--background-color);
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            flex-shrink: 0;
        }}

        .placeholder-instruction .step-text {{
            text-align: left;
            flex: 1;
        }}

        .placeholder-instruction .highlight {{
            color: var(--primary-color);
            font-weight: 600;
        }}

        .placeholder-instruction .tip {{
            background: rgba(56, 224, 123, 0.1);
            border-left: 3px solid var(--primary-color);
            padding: 0.75rem 1rem;
            border-radius: 6px;
            font-size: 0.9rem;
            color: var(--text-secondary);
            text-align: left;
        }}

        .loading-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            width: 100%;
            min-height: 400px;
            gap: 1.5rem;
        }}

        .loading-text {{
            color: var(--text-light);
            font-size: 1.1rem;
            font-weight: 500;
            letter-spacing: 0.5px;
        }}

        .spinner {{
            width: 50px;
            height: 50px;
            border: 4px solid var(--secondary-background);
            border-top: 4px solid var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}

        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        @keyframes scrollText {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-100%); }}
        }}
    </style>
    """


def get_text_overflow_script() -> str:
    """Returns the text overflow detection script to be injected in the app."""
    return """
        <script>
        function detectTextOverflow() {
            const doc = window.parent.document || window.document;
            
            const titles = doc.querySelectorAll('.track-title');
            const artists = doc.querySelectorAll('.track-artist');
            const genres = doc.querySelectorAll('.track-genres');
            
            function checkOverflow(element) {
                const wrapper = element.parentElement;
                if (!wrapper) return;
                
                const hasOverflow = element.scrollWidth > wrapper.clientWidth;
                
                if (hasOverflow) {
                    element.classList.add('has-overflow');
                } else {
                    element.classList.remove('has-overflow');
                }
            }
            
            titles.forEach(title => checkOverflow(title));
            artists.forEach(artist => checkOverflow(artist));
            genres.forEach(genre => checkOverflow(genre));
        }
        
        detectTextOverflow();
        
        setTimeout(detectTextOverflow, 100);
        setTimeout(detectTextOverflow, 500);
        setTimeout(detectTextOverflow, 1000);
        
        const observer = new MutationObserver(detectTextOverflow);
        const targetDoc = window.parent.document || window.document;
        observer.observe(targetDoc.body, {
            childList: true,
            subtree: true,
            characterData: true
        });
        
        setInterval(detectTextOverflow, 500);
        </script>
    """
