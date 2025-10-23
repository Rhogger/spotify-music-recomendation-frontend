import streamlit as st
from dotenv import load_dotenv

from ui.layout import init_app

# Carregar variáveis de ambiente
load_dotenv()

# Validar variáveis obrigatórias
# CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = st.secrets.spotify_credentials.client_id
CLIENT_SECRET = st.secrets.spotify_credentials.client_secret

if not CLIENT_ID or not CLIENT_SECRET:
    st.error(
        "❌ Erro de Configuração\n\n"
        "As variáveis de ambiente CLIENT_ID e CLIENT_SECRET não foram encontradas.\n\n"
        "Por favor, configure o arquivo `.env` com:\n"
        "```\n"
        "CLIENT_ID=seu_client_id\n"
        "CLIENT_SECRET=seu_client_secret\n"
        "```"
    )
    st.stop()


init_app()
