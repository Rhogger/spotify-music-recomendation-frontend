import streamlit as st
from core.model_loader import load_models
from core.recommender import recommend
from dotenv import load_dotenv
from services.spotify_api import fetch_spotify_data_parallel
from ui.components import header, slider_with_label, track_card_html
from ui.styles import load_styles

# Load environment variables
load_dotenv()

# Load models once at startup using singleton pattern
model, preprocessor, df_model, features = load_models()


st.set_page_config(page_title="Recomendações Spotify", page_icon="🎵", layout="wide")
st.markdown(load_styles(), unsafe_allow_html=True)

header()

col1, col2 = st.columns([1, 2], gap=None)

with col1:
    with st.form(key="reco_form", border=False):
        with st.container():
            st.markdown("### Parâmetros")

            pop = slider_with_label(
                "Popularidade", "Indica a popularidade da música", "pop_slider"
            )
            dance = slider_with_label(
                "Dançabilidade", "Indica quão dançável é a música", "dance_slider"
            )
            energy = slider_with_label(
                "Energia",
                "Indica quão energética e vibrante é a música",
                "energy_slider",
            )
            speech = slider_with_label(
                "Discurso",
                "Indica quão a música tem presença de palavras faladas",
                "speechiness_slider",
            )
            acoustic = slider_with_label(
                "Acústica",
                "Indica quão presente são os sons com equipamentos musicais na música",
                "acoustic_slider",
            )
            instr = slider_with_label(
                "Instrumentalidade",
                "Indica quão a música tem presença de sons instrumentais",
                "instr_slider",
            )

        submit = st.form_submit_button(
            "Gerar recomendação", use_container_width=True, type="primary"
        )

    if submit:
        try:
            resultados = recommend(
                popularity=pop / 100.0,
                danceability=dance / 100.0,
                energy=energy / 100.0,
                speechiness=speech / 100.0,
                acousticness=acoustic / 100.0,
                instrumentalness=instr / 100.0,
                top_n=20,
            )
            st.session_state["last_recommendations"] = resultados
        except Exception as e:
            st.error(f"Erro ao gerar recomendação: {e}")

with col2:
    st.markdown("### Músicas Recomendadas")

    if (
        "last_recommendations" in st.session_state
        and st.session_state["last_recommendations"] is not None
    ):
        resultados = st.session_state["last_recommendations"]

        # Convert DataFrame to list of dictionaries
        tracks_list = resultados.to_dict("records")

        # Show progress while fetching Spotify data
        with st.spinner("🔍 Buscando dados das músicas no Spotify..."):
            display_list = fetch_spotify_data_parallel(tracks_list, max_workers=5)

    else:
        # Placeholder: orienta o usuário a ajustar parâmetros e gerar a recomendação
        display_list = []

        placeholder_html = """
        <div class="placeholder-instruction">
            <div class="icon">🎵</div>
            <h2>Comece a explorar</h2>
            <div class="content">
                <div class="step">
                    <div class="step-number">1</div>
                    <div class="step-text">Ajuste os <span class="highlight">sliders à esquerda</span> para personalizar os parâmetros da música</div>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <div class="step-text">Configure <span class="highlight">Popularidade, Dançabilidade, Energia</span> e mais</div>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <div class="step-text">Clique em <span class="highlight">Gerar recomendação</span> para descobrir novas músicas</div>
                </div>
                <div class="tip">
                    💡 <strong>Dica:</strong> Varie Popularidade e Energia para resultados diferentes!
                </div>
            </div>
        </div>
        """

        st.markdown(placeholder_html, unsafe_allow_html=True)

    # Se houver itens para exibir (recommendations), renderiza-os
    if len(display_list) > 0:
        html_tracks = '<div class="tracks-grid scrollable-list">'
        for song in display_list:
            html_tracks += track_card_html(song)

        st.markdown(html_tracks, unsafe_allow_html=True)
