import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import xgboost as xgb
import joblib
import sys
sys.path.append('.')
from app.features import extract_features

df = pd.read_csv('data/training_data.csv')
print(f"Loaded {len(df)} samples")

print("Extracting features...")
feature_rows = []
for _, row in df.iterrows():
    features = extract_features(row['url'])
    features['label'] = row['label']
    feature_rows.append(features)

feature_df = pd.DataFrame(feature_rows)

feature_cols = [c for c in feature_df.columns if c not in ('label', 'index', 'Unnamed: 0')]
print(f"Extracted {len(feature_cols)} features")

X = feature_df[feature_cols]
y = feature_df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Training XGBoost...")

scale_pos = (y_train == 0).sum() / max((y_train == 1).sum(), 1)

model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=7,
    learning_rate=0.05,
    subsample=0.85,
    colsample_bytree=0.85,
    scale_pos_weight=scale_pos * 0.85,
    reg_alpha=0.05,
    reg_lambda=0.5,
    random_state=42,
    eval_metric='logloss'
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"\n=== Model Performance ===")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall: {recall_score(y_test, y_pred):.4f}")
print(f"F1 Score: {f1_score(y_test, y_pred):.4f}")

joblib.dump({
    'model': model,
    'feature_cols': feature_cols
}, 'app/model/phishing_model.joblib')

print ("Done!")
print("\nModel saved to app/model/phishing_model.joblib")