"""
Music Recommender
Handles music recommendation logic using the trained ML model
"""

from typing import List

import pandas as pd

from .model_loader import get_dataframe, get_features, get_model, get_preprocessor


class MusicRecommender:
    """Generates music recommendations based on audio feature parameters."""

    def __init__(self):
        """Initialize recommender with loaded models."""
        self.model = get_model()
        self.preprocessor = get_preprocessor()
        self.df = get_dataframe()
        self.features = get_features()

    def recommend(
        self,
        popularity: float,
        danceability: float,
        energy: float,
        speechiness: float,
        acousticness: float,
        instrumentalness: float,
        top_n: int = 5,
    ) -> pd.DataFrame:
        """
        Generate music recommendations based on audio features.

        Args:
            popularity (float): Popularity score (0.0 - 1.0)
            danceability (float): Danceability score (0.0 - 1.0)
            energy (float): Energy score (0.0 - 1.0)
            speechiness (float): Speechiness score (0.0 - 1.0)
            acousticness (float): Acousticness score (0.0 - 1.0)
            instrumentalness (float): Instrumentalness score (0.0 - 1.0)
            top_n (int): Number of recommendations to return

        Returns:
            pd.DataFrame: DataFrame with recommended tracks sorted by distance

        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If model is not loaded
        """
        if self.model is None or self.df is None:
            raise RuntimeError("Model or dataframe not loaded")

        # Validate parameters
        params = {
            "popularity": popularity,
            "danceability": danceability,
            "energy": energy,
            "speechiness": speechiness,
            "acousticness": acousticness,
            "instrumentalness": instrumentalness,
        }

        for param, value in params.items():
            if not (0.0 <= value <= 1.0):
                raise ValueError(f"{param} must be between 0.0 and 1.0, got {value}")

        # Create input dataframe with selected features
        input_df = pd.DataFrame([params])[self.features]

        # Scale using preprocessor
        input_scaled = self.preprocessor.transform(input_df)

        # Get nearest neighbors
        distances, indices = self.model.kneighbors(input_scaled, n_neighbors=top_n)

        # Get results from dataframe
        resultados = self.df.iloc[indices[0]].copy().reset_index(drop=True)
        resultados["distancia"] = distances[0]

        # Sort by distance (closest first)
        resultados = resultados.sort_values("distancia").reset_index(drop=True)

        return resultados

    def get_features_list(self) -> List[str]:
        """Get list of features used by the model."""
        return self.features if self.features else []

    def get_dataset_size(self) -> int:
        """Get number of tracks in the dataset."""
        return len(self.df) if self.df is not None else 0


# Global recommender instance
_recommender = None


def get_recommender() -> MusicRecommender:
    """Get or create the global recommender instance."""
    global _recommender
    if _recommender is None:
        _recommender = MusicRecommender()
    return _recommender


def recommend(
    popularity: float,
    danceability: float,
    energy: float,
    speechiness: float,
    acousticness: float,
    instrumentalness: float,
    top_n: int = 5,
) -> pd.DataFrame:
    """
    Convenience function to get recommendations.

    Args:
        popularity: Popularity score (0.0 - 1.0)
        danceability: Danceability score (0.0 - 1.0)
        energy: Energy score (0.0 - 1.0)
        speechiness: Speechiness score (0.0 - 1.0)
        acousticness: Acousticness score (0.0 - 1.0)
        instrumentalness: Instrumentalness score (0.0 - 1.0)
        top_n: Number of recommendations to return

    Returns:
        pd.DataFrame: Recommended tracks
    """
    return get_recommender().recommend(
        popularity=popularity,
        danceability=danceability,
        energy=energy,
        speechiness=speechiness,
        acousticness=acousticness,
        instrumentalness=instrumentalness,
        top_n=top_n,
    )
