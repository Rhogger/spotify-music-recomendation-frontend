# Spotify API Services

Este diretório contém os serviços para integração com a Spotify Web API.

## Estrutura

### `token_manager.py`

Gerencia tokens de acesso do Spotify com cache automático e refresh.

```python
from services.token_manager import get_access_token

# Obter token (utiliza cache se disponível)
token = get_access_token()
```

### `spotify_api.py`

Funções para interagir com a Spotify API:

- `search_track()` - Buscar músicas por nome, artista e gêneros
- `get_track_audio_features()` - Obter características de áudio
- `get_track_details()` - Obter detalhes completos da música
- `get_best_album_image()` - Extrair melhor imagem do álbum

```python
from services.spotify_api import search_track, get_best_album_image

# Buscar música
results = search_track("Shape of You", "Ed Sheeran", limit=1)

# Extrair imagem
image_url = get_best_album_image(results[0]["album"]["images"])
```

## Configuração

Certifique-se de que as credenciais Spotify estão no arquivo `.env`:

```env
CLIENT_ID=sua_client_id
CLIENT_SECRET=seu_client_secret
```

## Tratamento de Erros

Todos os erros de API lançam `SpotifyAPIError`:

```python
from services.spotify_api import search_track, SpotifyAPIError

try:
    results = search_track("Música", "Artista")
except SpotifyAPIError as e:
    print(f"Erro: {e}")
```
