import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from core.model_loader import load_models
from core.recommender import recommend
from services.spotify_api import fetch_spotify_data_parallel
from ui.components import centered_loader, header, slider_with_label, track_card_html
from ui.styles import get_text_overflow_script, load_styles


def init_app():
    # Load environment variables
    load_dotenv()

    # Load models once at startup using singleton pattern
    model, preprocessor, df_model, features = load_models()

    st.set_page_config(
        page_title="Recomendações Spotify",
        page_icon="🎵",
        layout="wide",
    )
    st.markdown(load_styles(), unsafe_allow_html=True)

    # Injetar o script usando a API de componentes
    components.html(get_text_overflow_script(), height=0)

    header()

    col1, col2 = st.columns([1, 2], gap=None)

    with col1:
        with st.form(key="reco_form", border=False):
            with st.container():
                st.markdown("### Parâmetros")

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
                    danceability=dance / 100.0,
                    energy=energy / 100.0,
                    speechiness=speech / 100.0,
                    acousticness=acoustic / 100.0,
                    instrumentalness=instr / 100.0,
                    top_n=20,
                )
                st.session_state["last_recommendations"] = resultados
                st.session_state["is_loading"] = True
            except Exception as e:
                st.error(f"Erro ao gerar recomendação: {e}")

    with col2:
        st.markdown("### Músicas Recomendadas")

        # Verificar se está carregando
        is_loading = st.session_state.get("is_loading", False)

        if is_loading and "last_recommendations" in st.session_state:
            # Mostrar loader
            centered_loader()

            # Buscar dados do Spotify
            resultados = st.session_state["last_recommendations"]
            tracks_list = resultados.to_dict("records")
            display_list = fetch_spotify_data_parallel(tracks_list, max_workers=5)

            # Limpar flag de loading
            st.session_state["is_loading"] = False

            # Rerenderizar
            st.rerun()

        elif (
            "last_recommendations" in st.session_state
            and st.session_state["last_recommendations"] is not None
        ):
            resultados = st.session_state["last_recommendations"]

            # Convert DataFrame to list of dictionaries
            tracks_list = resultados.to_dict("records")

            # Fetch Spotify data (already cached from previous load)
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
                      <div class="step-text">Configure <span class="highlight">Dançabilidade, Energia, Discurso</span> e mais</div>
                  </div>
                  <div class="step">
                      <div class="step-number">3</div>
                      <div class="step-text">Clique em <span class="highlight">Gerar recomendação</span> para descobrir novas músicas</div>
                  </div>
                  <div class="tip">
                      💡 <strong>Dica:</strong> Varie Discurso e Instrumentalidade para resultados diferentes!
                  </div>
              </div>
          </div>
          """

            st.markdown(placeholder_html, unsafe_allow_html=True)

        # Se houver itens para exibir (recommendations), renderiza-os
        if len(display_list) > 0 and not is_loading:
            html_tracks = '<div class="tracks-grid scrollable-list">'
            for song in display_list:
                html_tracks += track_card_html(song)

            html_tracks += "</div>"
            st.markdown(html_tracks, unsafe_allow_html=True)
