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
        danceability: float,
        energy: float,
        acousticness: float,
        valence: float,
        is_popular: bool,
        is_explicit: bool,
        decade: str,
        top_n: int = 5,
    ) -> pd.DataFrame:
        """
        Generate music recommendations based on audio features.

        Args:
            danceability (float): Danceability score (0-100)
            energy (float): Energy score (0-100)
            acousticness (float): Acousticness score (0-100)
            valence (float): Valence score (0-100)
            is_popular (bool): Whether to filter for popular songs
            is_explicit (bool): Whether to filter for explicit songs
            decade (str): Decade filter (e.g., '2020', '2010', etc.)
            top_n (int): Number of recommendations to return

        Returns:
            pd.DataFrame: DataFrame with recommended tracks sorted by distance

        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If model is not loaded
        """
        if self.model is None or self.df is None:
            raise RuntimeError("Model or dataframe not loaded")

        # Validate parameters (0-100 range)
        params = {
            "danceability": danceability,
            "energy": energy,
            "acousticness": acousticness,
            "valence": valence,
        }

        for param, value in params.items():
            if not (0.0 <= value <= 100.0):
                raise ValueError(f"{param} must be between 0.0 and 100.0, got {value}")

        # Create input dataframe with numeric features only (for scaler)
        # Scaler was trained only on: acousticness, danceability, energy, valence
        numeric_data = {
            "acousticness": acousticness,
            "danceability": danceability,
            "energy": energy,
            "valence": valence,
        }

        numeric_df = pd.DataFrame([numeric_data])

        # Scale using the scaler (expects 0-100 range for numeric features)
        numeric_scaled = self.preprocessor.transform(numeric_df)

        # Convert scaled array back to DataFrame to add other features
        numeric_scaled_df = pd.DataFrame(
            numeric_scaled,
            columns=["acousticness", "danceability", "energy", "valence"],
        )

        # Add categorical features (not scaled)
        numeric_scaled_df["is_popular"] = 1 if is_popular else 0
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

        # Select only the features that the model was trained with, in correct order
        input_scaled = numeric_scaled_df[self.features].values

        # Get nearest neighbors
        distances, indices = self.model.kneighbors(input_scaled, n_neighbors=top_n * 2)

        # Get results from dataframe
        resultados = self.df.iloc[indices[0]].copy().reset_index(drop=True)
        resultados["distancia"] = distances[0]

        # Apply filters
        if is_popular:
            resultados = resultados[resultados["is_popular"] == 1]

        if is_explicit:
            resultados = resultados[resultados["explicit"] == 1]

        if decade:
            decade_col = decade + "s"
            resultados = resultados[resultados[decade_col] == 1]

        # Sort by distance and limit to top_n
        resultados = (
            resultados.sort_values("distancia").reset_index(drop=True).head(top_n)
        )

        # Ensure 'id' column exists for Spotify API (rename track_id if necessary)
        if "track_id" in resultados.columns and "id" not in resultados.columns:
            resultados["id"] = resultados["track_id"]

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
    danceability: float,
    energy: float,
    acousticness: float,
    valence: float,
    is_popular: bool,
    is_explicit: bool,
    decade: str,
    top_n: int = 5,
) -> pd.DataFrame:
    """
    Convenience function to get recommendations.

    Args:
        danceability: Danceability score (0-100)
        energy: Energy score (0-100)
        acousticness: Acousticness score (0-100)
        valence: Valence score (0-100)
        is_popular: Whether to filter for popular songs
        is_explicit: Whether to filter for explicit songs
        decade: Decade filter
        top_n: Number of recommendations to return

    Returns:
        pd.DataFrame: Recommended tracks
    """
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
