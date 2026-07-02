from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[3]
DATASET = ROOT / 'data' / 'raw' / 'nacc_monitoring_sample.csv'
OUT = ROOT / 'ml' / 'artifacts'
OUT.mkdir(parents=True, exist_ok=True)

FEATURES = [
    'age_at_visit', 'SEX', 'EDUC', 'INDEPEND', 'MEMORY', 'MEMPROB', 'CDRSUM', 'CDRGLOB',
    'NACCGDS', 'NACCMMSE', 'NACCMOCA', 'TRAILA', 'TRAILB', 'ANXIETY', 'AGIT',
    'HALL', 'DEL', 'GAIT', 'SLEEPAP', 'BPSYS', 'BPDIAS', 'PARKSIGN', 'NACCAPOE'
]


def main() -> None:
    df = pd.read_csv(DATASET)
    X = df[FEATURES].copy()
    y = df['monitoring_tier'].astype(int)

    numeric = FEATURES
    preprocessor = ColumnTransformer([
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
        ]), numeric)
    ])

    pipeline = Pipeline([
        ('preprocess', preprocessor),
        ('model', RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            class_weight='balanced_subsample',
            min_samples_leaf=4,
            n_jobs=-1,
        )),
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    metrics = {
        'accuracy': float(accuracy_score(y_test, preds)),
        'macro_f1': float(f1_score(y_test, preds, average='macro')),
        'class_distribution': {str(k): int(v) for k, v in y.value_counts().sort_index().items()},
        'features': FEATURES,
    }

    joblib.dump(pipeline, OUT / 'nacc_monitoring_tier_rf.joblib')
    (OUT / 'nacc_metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    print(json.dumps(metrics, indent=2))


if __name__ == '__main__':
    main()
