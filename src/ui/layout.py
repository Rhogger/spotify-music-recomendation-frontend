import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from core.model_loader import load_models
from core.recommender import recommend
from services.spotify_api import fetch_spotify_data_parallel
from ui.components import (
    centered_loader,
    decade_selector,
    header,
    is_explicit_checkbox,
    is_popular_checkbox,
    slider_with_label,
    track_card_html,
)
from ui.styles import get_text_overflow_script, load_styles


def init_app():
    load_dotenv()

    model, _, df_model, features = load_models()

    st.set_page_config(
        page_title="Recomendações Spotify",
        page_icon="🎵",
        layout="wide",
    )
    st.markdown(load_styles(), unsafe_allow_html=True)

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
                acoustic = slider_with_label(
                    "Acústica",
                    "Indica quão presente são os sons acústicos na música",
                    "acoustic_slider",
                )
                valence = slider_with_label(
                    "Valência",
                    "Indica quão positiva e alegre é a música",
                    "valence_slider",
                )

                decade = decade_selector()

                is_popular = is_popular_checkbox()

                is_explicit = is_explicit_checkbox()

            submit = st.form_submit_button(
                "Gerar recomendação", use_container_width=True, type="primary"
            )

        if submit:
            try:
                print("\n" + "=" * 60)
                print("🎵 GERANDO RECOMENDAÇÃO DE MÚSICAS")
                print("=" * 60)
                print("Parâmetros selecionados:")
                print(f"  Dançabilidade: {dance}%")
                print(f"  Energia: {energy}%")
                print(f"  Acústica: {acoustic}%")
                print(f"  Valência: {valence}%")
                print(f"  Década: {decade}")
                print(f"  Popular: {'Sim' if is_popular else 'Não'}")
                print(f"  Explicit: {'Sim' if is_explicit else 'Não'}")
                print("-" * 60)

                resultados = recommend(
                    danceability=dance,
                    energy=energy,
                    acousticness=acoustic,
                    valence=valence,
                    is_popular=is_popular,
                    is_explicit=is_explicit,
                    decade=decade,
                    top_n=100,
                )
                st.session_state["last_recommendations"] = resultados
                st.session_state["is_loading"] = True
            except Exception as e:
                st.error(f"Erro ao gerar recomendação: {e}")

    with col2:
        st.markdown("### Músicas Recomendadas")

        is_loading = st.session_state.get("is_loading", False)

        if is_loading and "last_recommendations" in st.session_state:
            centered_loader()

            resultados = st.session_state["last_recommendations"]
            tracks_list = resultados.to_dict("records")
            display_list = fetch_spotify_data_parallel(tracks_list, max_workers=5)

            st.session_state["is_loading"] = False

            st.rerun()

        elif (
            "last_recommendations" in st.session_state
            and st.session_state["last_recommendations"] is not None
        ):
            resultados = st.session_state["last_recommendations"]

            tracks_list = resultados.to_dict("records")

            display_list = fetch_spotify_data_parallel(tracks_list, max_workers=5)

        else:
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
                      <div class="step-text">Configure <span class="highlight">Dançabilidade, Energia</span> e Acústica</div>
                  </div>
                  <div class="step">
                      <div class="step-number">3</div>
                      <div class="step-text">Selecione a <span class="highlight">década</span> e marque se quer <span class="highlight">músicas populares</span></div>
                  </div>
                  <div class="step">
                      <div class="step-number">4</div>
                      <div class="step-text">Clique em <span class="highlight">Gerar recomendação</span> para descobrir novas músicas</div>
                  </div>
              </div>
          </div>
          """

            st.markdown(placeholder_html, unsafe_allow_html=True)

        if len(display_list) > 0 and not is_loading:
            html_tracks = '<div class="tracks-grid scrollable-list">'
            for song in display_list:
                html_tracks += track_card_html(song)

            html_tracks += "</div>"
            st.markdown(html_tracks, unsafe_allow_html=True)

        elif (
            "last_recommendations" in st.session_state
            and not is_loading
            and len(display_list) == 0
        ):
            no_results_html = """
            <div class="empty-state">
                <div class="icon">😔</div>
                <h3>Sem resultados</h3>
                <p>Nenhuma música encontrada com os parâmetros selecionados.<br>Tente ajustar os filtros ou mudar os valores dos sliders.</p>
            </div>
            """
            st.markdown(no_results_html, unsafe_allow_html=True)
