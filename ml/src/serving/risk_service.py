from dataclasses import dataclass
from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / 'ml' / 'artifacts'


@dataclass
class RiskPrediction:
    monitoring_tier: int
    probability_vector: list[float]


class MonitoringTierModel:
    def __init__(self) -> None:
        self.model = joblib.load(ARTIFACTS / 'nacc_monitoring_tier_rf.joblib')

    def predict(self, features: dict) -> RiskPrediction:
        frame = pd.DataFrame([features])
        probs = self.model.predict_proba(frame)[0].tolist()
        pred = int(self.model.predict(frame)[0])
        return RiskPrediction(monitoring_tier=pred, probability_vector=[float(x) for x in probs])
