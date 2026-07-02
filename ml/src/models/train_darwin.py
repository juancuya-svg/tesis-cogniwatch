from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[3]
DATASET = ROOT / 'data' / 'raw' / 'DARWIN.csv'
OUT = ROOT / 'ml' / 'artifacts'
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    df = pd.read_csv(DATASET)
    X = df.drop(columns=['ID', 'class'])
    y = (df['class'] == 'P').astype(int)

    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('model', ExtraTreesClassifier(n_estimators=300, min_samples_leaf=2, random_state=42, n_jobs=-1)),
    ])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_auc = cross_val_score(pipeline, X, y, cv=cv, scoring='roc_auc')
    cv_acc = cross_val_score(pipeline, X, y, cv=cv, scoring='accuracy')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    pipeline.fit(X_train, y_train)
    probs = pipeline.predict_proba(X_test)[:, 1]
    preds = (probs >= 0.5).astype(int)

    metrics = {
        'cv_auc_mean': float(cv_auc.mean()),
        'cv_auc_std': float(cv_auc.std()),
        'cv_acc_mean': float(cv_acc.mean()),
        'cv_acc_std': float(cv_acc.std()),
        'holdout_auc': float(roc_auc_score(y_test, probs)),
        'holdout_accuracy': float(accuracy_score(y_test, preds)),
        'n_rows': int(len(df)),
        'n_features': int(X.shape[1]),
    }

    joblib.dump(pipeline, OUT / 'darwin_extratrees.joblib')
    (OUT / 'darwin_metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')

    feature_importances = pd.DataFrame({
        'feature': X.columns,
        'importance': pipeline.named_steps['model'].feature_importances_,
    }).sort_values('importance', ascending=False)
    feature_importances.to_csv(OUT / 'darwin_top_features.csv', index=False)
    print(json.dumps(metrics, indent=2))


if __name__ == '__main__':
    main()
