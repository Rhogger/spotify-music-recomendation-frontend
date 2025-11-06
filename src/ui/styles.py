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
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
            height: 100% !important;
        }}
        
        .stForm > div {{
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
        }}
        
        .stForm > .stVerticalBlock {{
            justify-content: space-between !important;
        }}
        
        .stColumn {{
            padding-top: 32px;
            padding-left: 32px;
            padding-right: 32px;
        }}
        
        .stColumn:first-child {{
            border-width: 0px 1px 0px 0px;
            border-color: var(--border-color);
            border-style: solid;
            overflow-y: auto !important;
            height: calc(100vh - 71.4px) !important;
            display: flex !important;
            flex-direction: column !important;
        }}

        .stColumn:first-child > div {{
            height: 100%;
            display: flex;
            flex-direction: column;
        }}

        .stColumn:first-child::-webkit-scrollbar {{
            width: 8px;
        }}

        .stColumn:first-child::-webkit-scrollbar-thumb {{
            background-color: var(--primary-color);
            border-radius: 10px;
        }}

        .stColumn:first-child::-webkit-scrollbar-track {{
            background: var(--secondary-background);
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

        /* Tablet and mobile: allow normal scrolling, remove fixed height only for smaller screens */
        @media (max-width: 800px) {{
            /* Allow scroll on main container */
            .stMainBlockContainer {{
                overflow: auto !important;
            }}
            
            /* Responsive header */
            .header-title {{
                font-size: 1rem !important;
                gap: 0.5rem !important;
                padding: 0.75rem 1rem !important;
            }}
            
            .spotify-icon {{
                width: 24px !important;
                height: 24px !important;
            }}
            
            /* Responsive column padding */
            .stColumn {{
                padding-top: 16px !important;
                padding-left: 16px !important;
                padding-right: 16px !important;
            }}
            
            /* Stack columns vertically on mobile */
            .stHorizontalBlock {{
                flex-direction: column !important;
                flex-wrap: nowrap !important;
            }}
            
            /* Unified scroll: remove overflow from individual sections */
            .stColumn:first-child {{
                height: auto !important;
                max-height: none !important;
                padding-bottom: 2rem !important;
                border-width: 0px 0px 1px 0px !important;
                width: 100% !important;
                overflow-y: visible !important;
            }}
            
            .stColumn:last-child {{
                height: auto !important;
                max-height: none !important;
                padding-bottom: 2rem !important;
                width: 100% !important;
                overflow-y: visible !important;
            }}
            
            /* Responsive placeholder */
            .placeholder-instruction {{
                padding: 1.25rem !important;
                margin: 0.75rem 0 !important;
                gap: 1rem !important;
            }}
            
            .placeholder-instruction .icon {{
                font-size: 2rem !important;
            }}
            
            .placeholder-instruction h2 {{
                font-size: 1.1rem !important;
            }}
            
            .placeholder-instruction .content {{
                gap: 0.5rem !important;
                font-size: 0.85rem !important;
            }}
            
            .placeholder-instruction .step-number {{
                width: 24px !important;
                height: 24px !important;
                font-size: 0.8rem !important;
            }}
            
            .placeholder-instruction .tip {{
                font-size: 0.8rem !important;
                padding: 0.5rem 0.75rem !important;
            }}
            
            /* Responsive headings */
            h3 {{
                font-size: 1.2rem !important;
            }}
            
            /* Responsive slider labels */
            .slider-label {{
                font-size: 0.85rem !important;
            }}
            
            /* Responsive text */
            p {{
                font-size: 0.9rem !important;
            }}
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

        /* Accordion and Expander Styles */
        .streamlit-expanderHeader {{
            background: transparent;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px !important;
            margin-bottom: 12px;
        }}

        .streamlit-expanderHeader:hover {{
            background: rgba(56, 224, 123, 0.05);
        }}

        .streamlit-expanderHeader svg {{
            color: var(--primary-color);
        }}

        .streamlit-expanderContent {{
            padding: 12px !important;
            background: rgba(56, 224, 123, 0.02);
            border: 1px solid var(--border-color);
            border-top: none;
            border-radius: 0 0 8px 8px;
            overflow: visible !important;
            max-height: none !important;
        }}

        /* Radio Button Grid - Responsivo com auto-fill */
        .st-key-decade_radio {{
            width: 100% !important;
        }}

        .stElementContainer.st-key-decade_radio {{
            width: 100% !important;
            max-width: 100% !important;
        }}

        .stRadio {{
            display: block !important;
            width: 100% !important;
            max-width: 100% !important;
            flex: 1 !important;
        }}

        .stRadio [role="radiogroup"] {{
            display: grid !important;
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)) !important;
            gap: 12px !important;
            width: 100% !important;
            max-width: 100% !important;
        }}

        .stRadio > div {{
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            width: 100% !important;
        }}

        .stRadio input[type="radio"] {{
            width: 16px !important;
            height: 16px !important;
            cursor: pointer !important;
            accent-color: var(--primary-color) !important;
        }}

        .stRadio label {{
            color: var(--text-color) !important;
            cursor: pointer !important;
            margin: 0 !important;
            font-weight: 500 !important;
        }}

        /* Checkbox Styles */
        .stCheckbox label {{
            color: var(--text-light);
            cursor: pointer;
            margin: 0;
            font-weight: 500;
        }}

        .stCheckbox input[type="checkbox"] {{
            width: 18px;
            height: 18px;
            cursor: pointer;
            accent-color: var(--primary-color);
        }}

        button[data-testid="stBaseButton-primaryFormSubmit"] > div > p {{
            font-weight: 700;
            color: var(--background-color);
        }}

        button[data-testid="stBaseButton-primaryFormSubmit"] {{
            margin-bottom: 32px !important;
            margin-top: auto !important;
        }}

        .stForm button {{
            margin-top: auto !important;
        }}
        
        .tracks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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
        
        /* Mobile: Responsive card sizes with uniform height */
        @media (max-width: 800px) {{
            .tracks-grid {{
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)) !important;
                gap: 1rem !important;
                grid-auto-rows: 1fr !important;
                width: 100% !important;
            }}
            
            .track-card {{
                padding: 0.75rem !important;
                display: flex !important;
                flex-direction: column !important;
                height: 100% !important;
            }}
            
            .track-image {{
                width: 100%;
                aspect-ratio: 1;
                margin-bottom: 0.5rem !important;
            }}
            
            .track-image-img {{
                width: 100%;
                height: 100%;
                margin-bottom: 0.5rem !important;
            }}
            
            .track-title {{
                font-size: 0.75rem !important;
                line-height: 1.2 !important;
            }}
            
            .track-artist {{
                font-size: 0.65rem !important;
                line-height: 1.2 !important;
            }}
            
            .track-genres {{
                font-size: 0.6rem !important;
                line-height: 1.1 !important;
            }}
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
        
        /* Mobile/Tablet: Always animate text overflow without hover */
        @media (max-width: 800px) {{
            /* Reduce margins proportionally with font size reduction */
            .track-title-wrapper {{
                margin-bottom: 0.15rem !important;
            }}
            
            .track-artist-wrapper {{
                margin-bottom: 0.3rem !important;
            }}
            
            .track-title.has-overflow {{
                animation: scrollText 5s linear infinite !important;
            }}
            
            .track-artist.has-overflow {{
                animation: scrollText 5s linear infinite !important;
            }}
            
            .track-genres.has-overflow {{
                animation: scrollText 5s linear infinite !important;
            }}
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

        /* Empty state / No results */
        .empty-state {{
            background: linear-gradient(135deg, rgba(218, 60, 37, 0.1) 0%, rgba(41, 45, 42, 0.3) 100%);
            border: 2px solid rgba(218, 60, 37, 0.5);
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            align-items: center;
            text-align: center;
        }}

        .empty-state .icon {{
            font-size: 3rem;
            animation: pulse 2s ease-in-out infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}

        .empty-state h3 {{
            color: rgba(218, 60, 37, 0.8);
            font-size: 1.3rem;
            margin: 0;
            font-weight: 700;
        }}

        .empty-state p {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.5;
            margin: 0;
        }}
        
        @media (max-width: 800px) {{
            .empty-state {{
                padding: 1.25rem !important;
                margin: 0.75rem 0 !important;
                gap: 1rem !important;
            }}
            
            .empty-state .icon {{
                font-size: 2rem !important;
            }}
            
            .empty-state h3 {{
                font-size: 1.1rem !important;
            }}
            
            .empty-state p {{
                font-size: 0.85rem !important;
            }}
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
