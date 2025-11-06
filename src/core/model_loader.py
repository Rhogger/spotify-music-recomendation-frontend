import os
import pickle
from typing import Tuple

import joblib
import pandas as pd


class ModelLoader:
    _instance = None
    _model = None
    _scaler = None
    _df = None
    _features = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self) -> Tuple:
        if self._model is not None and self._features is not None:
            return self._model, self._scaler, self._df, self._features

        base_path = os.path.dirname(__file__)
        assets_path = os.path.abspath(os.path.join(base_path, "../assets"))

        path_model = os.path.join(assets_path, "models/music_recommender_model.joblib")
        path_scaler = os.path.join(assets_path, "models/scaler.joblib")
        path_df = os.path.join(assets_path, "datasets/pre_processing.csv")
        path_features = os.path.join(assets_path, "models/music_model_features.pkl")

        try:
            print(f"📂 Loading model from: {path_model}")
            self._model = joblib.load(path_model)

            print(f"📂 Loading scaler from: {path_scaler}")
            self._scaler = joblib.load(path_scaler)

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
            return self._model, self._scaler, self._df, self._features

        except FileNotFoundError as e:
            print(f"❌ Error: Model file not found: {e}")
            raise
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise

    def get_model(self):
        if self._model is None:
            self.load()
        return self._model

    def get_preprocessor(self):
        if self._scaler is None:
            self.load()
        return self._scaler

    def get_dataframe(self):
        if self._df is None:
            self.load()
        return self._df

    def get_features(self):
        if self._features is None:
            self.load()
        return self._features


_loader = ModelLoader()


def load_models() -> Tuple:
    return _loader.load()


def get_model():
    return _loader.get_model()


def get_preprocessor():
    return _loader.get_preprocessor()


def get_dataframe():
    return _loader.get_dataframe()


def get_features():
    return _loader.get_features()
