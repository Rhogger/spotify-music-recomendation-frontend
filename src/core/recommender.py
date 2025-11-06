from typing import List

import pandas as pd

from .model_loader import get_dataframe, get_features, get_model, get_preprocessor


class MusicRecommender:
    def __init__(self):
        self.model = get_model()
        self.preprocessor = get_preprocessor()
        self.df = get_dataframe()
        self.features = get_features()

    def recommend(
        self,
        danceability: float,
        energy: float,
        acousticness: float,
        valence: float,
        is_popular: bool,
        is_explicit: bool,
        decade: str,
        top_n: int = 5,
    ) -> pd.DataFrame:
        if self.model is None or self.df is None:
            raise RuntimeError("Model or dataframe not loaded")

        params = {
            "danceability": danceability,
            "energy": energy,
            "acousticness": acousticness,
            "valence": valence,
        }

        for param, value in params.items():
            if not (0.0 <= value <= 100.0):
                raise ValueError(f"{param} must be between 0.0 and 100.0, got {value}")

        numeric_data = {
            "acousticness": acousticness / 100.0,
            "danceability": danceability / 100.0,
            "energy": energy / 100.0,
            "valence": valence / 100.0,
        }

        numeric_df = pd.DataFrame([numeric_data])

        numeric_scaled = self.preprocessor.transform(numeric_df)

        numeric_scaled_df = pd.DataFrame(
            numeric_scaled,
            columns=["acousticness", "danceability", "energy", "valence"],
        )

        numeric_scaled_df["is_popular"] = 1 if is_popular else 0
        numeric_scaled_df["explicit"] = 1 if is_explicit else 0
        numeric_scaled_df["1920s"] = 1 if decade == "1920" else 0
        numeric_scaled_df["1930s"] = 1 if decade == "1930" else 0
        numeric_scaled_df["1940s"] = 1 if decade == "1940" else 0
        numeric_scaled_df["1950s"] = 1 if decade == "1950" else 0
        numeric_scaled_df["1960s"] = 1 if decade == "1960" else 0
        numeric_scaled_df["1970s"] = 1 if decade == "1970" else 0
        numeric_scaled_df["1980s"] = 1 if decade == "1980" else 0
        numeric_scaled_df["1990s"] = 1 if decade == "1990" else 0
        numeric_scaled_df["2000s"] = 1 if decade == "2000" else 0
        numeric_scaled_df["2010s"] = 1 if decade == "2010" else 0
        numeric_scaled_df["2020s"] = 1 if decade == "2020" else 0

        input_scaled = numeric_scaled_df[self.features].values

        distances, indices = self.model.kneighbors(input_scaled, n_neighbors=top_n * 5)

        resultados = self.df.iloc[indices[0]].copy().reset_index(drop=True)
        resultados["distancia"] = distances[0]

        if is_popular:
            resultados = resultados[resultados["is_popular"] == 1]

        if is_explicit:
            if "explicit" in resultados.columns:
                resultados = resultados[resultados["explicit"] == 1]

        if decade:
            decade_col = decade + "s"
            resultados = resultados[resultados[decade_col] == 1]

        artist_col = "artist" if "artist" in resultados.columns else "artists"
        title_col = "title" if "title" in resultados.columns else "name"

        resultados = resultados[
            (resultados[artist_col].notna())
            & (resultados[artist_col] != "")
            & (resultados[title_col].notna())
            & (resultados[title_col] != "")
        ].reset_index(drop=True)

        resultados = (
            resultados.sort_values("distancia")
            .reset_index(drop=True)
            .head(min(top_n, 20))
        )

        if "track_id" in resultados.columns and "id" not in resultados.columns:
            resultados["id"] = resultados["track_id"]

        return resultados

    def get_features_list(self) -> List[str]:
        return self.features if self.features else []

    def get_dataset_size(self) -> int:
        return len(self.df) if self.df is not None else 0


_recommender = None


def get_recommender() -> MusicRecommender:
    global _recommender
    if _recommender is None:
        _recommender = MusicRecommender()
    return _recommender


def recommend(
    danceability: float,
    energy: float,
    acousticness: float,
    valence: float,
    is_popular: bool,
    is_explicit: bool,
    decade: str,
    top_n: int = 5,
) -> pd.DataFrame:
    return get_recommender().recommend(
        danceability=danceability,
        energy=energy,
        acousticness=acousticness,
        valence=valence,
        is_popular=is_popular,
        is_explicit=is_explicit,
        decade=decade,
        top_n=top_n,
    )
