"""
Model Loader
Responsible for loading and caching the music recommendation model and preprocessor
"""

import os
import pickle
from typing import Tuple

import joblib
import pandas as pd


class ModelLoader:
    """Handles loading and caching of the ML model and preprocessor."""

    _instance = None
    _model = None
    _preprocessor = None
    _df = None
    _features = None

    def __new__(cls):
        """Implement singleton pattern for model loading."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self) -> Tuple:
        """
        Load model, preprocessor, dataframe, and features from disk.
        Uses singleton pattern to load only once.

        Returns:
            Tuple: (model, preprocessor, df, features)

        Raises:
            FileNotFoundError: If model files are not found
            Exception: If there's an error loading the files
        """
        # Return cached if already loaded
        if (
            self._model is not None
            and self._preprocessor is not None
            and self._features is not None
        ):
            return self._model, self._preprocessor, self._df, self._features

        # Get base paths
        base_path = os.path.dirname(__file__)
        assets_path = os.path.abspath(os.path.join(base_path, "../assets"))

        # Define file paths
        path_model = os.path.join(assets_path, "models/music_recommender_model.joblib")
        path_preprocessor = os.path.join(
            assets_path, "models/pipeline_preprocessor.joblib"
        )
        path_df = os.path.join(assets_path, "datasets/pre_processing.csv")
        path_features = os.path.join(assets_path, "models/music_model_features.pkl")

        # Load files with error handling
        try:
            print(f"📂 Loading model from: {path_model}")
            self._model = joblib.load(path_model)

            print(f"📂 Loading preprocessor from: {path_preprocessor}")
            self._preprocessor = joblib.load(path_preprocessor)

            print(f"📂 Loading features from: {path_features}")
            with open(path_features, "rb") as f:
                self._features = pickle.load(f)

            print(f"📂 Loading dataset from: {path_df}")
            try:
                self._df = pd.read_csv(path_df)
            except Exception as e:
                print(f"⚠️ Warning: Could not load CSV: {e}")
                self._df = None

            print("✅ All models loaded successfully!")
            return self._model, self._preprocessor, self._df, self._features

        except FileNotFoundError as e:
            print(f"❌ Error: Model file not found: {e}")
            raise
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise

    def get_model(self):
        """Get cached model or load if needed."""
        if self._model is None:
            self.load()
        return self._model

    def get_preprocessor(self):
        """Get cached preprocessor or load if needed."""
        if self._preprocessor is None:
            self.load()
        return self._preprocessor

    def get_dataframe(self):
        """Get cached dataframe or load if needed."""
        if self._df is None:
            self.load()
        return self._df

    def get_features(self):
        """Get cached features or load if needed."""
        if self._features is None:
            self.load()
        return self._features


# Global loader instance
_loader = ModelLoader()


def load_models() -> Tuple:
    """Convenience function to load all models."""
    return _loader.load()


def get_model():
    """Get the cached model."""
    return _loader.get_model()


def get_preprocessor():
    """Get the cached preprocessor."""
    return _loader.get_preprocessor()


def get_dataframe():
    """Get the cached dataframe."""
    return _loader.get_dataframe()


def get_features():
    """Get the cached features."""
    return _loader.get_features()
