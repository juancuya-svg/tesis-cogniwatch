from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd

from app.core.config import settings


class MLInferenceService:
    def __init__(self) -> None:
        self._darwin_model = None
        self._nacc_model = None

    @property
    def darwin_model(self):
        if self._darwin_model is None:
            model_path = Path(settings.ml_artifacts_dir) / 'darwin_extratrees.joblib'
            if model_path.exists():
                self._darwin_model = joblib.load(model_path)
        return self._darwin_model

    @property
    def nacc_model(self):
        if self._nacc_model is None:
            model_path = Path(settings.ml_artifacts_dir) / 'nacc_monitoring_tier_rf.joblib'
            if model_path.exists():
                self._nacc_model = joblib.load(model_path)
        return self._nacc_model

    def predict_cognitive_motor_probability(self, features: dict) -> float | None:
        model = self.darwin_model
        if model is None:
            return None
        df = pd.DataFrame([features])
        return float(model.predict_proba(df)[0, 1])

    def predict_monitoring_tier(self, features: dict) -> tuple[int, list[dict]]:
        model = self.nacc_model
        if model is None:
            return 1, []
        df = pd.DataFrame([features])
        pred = int(model.predict(df)[0])
        drivers = [
            {"feature": key, "value": value}
            for key, value in list(features.items())[:5]
            if value is not None
        ]
        return pred, drivers


ml_service = MLInferenceService()
