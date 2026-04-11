import pandas as pd
import numpy as np
import xgboost as xgb

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    make_scorer
)

# =========================
# LOAD DATA
# =========================
input_path = r"C:\Users\Admin\Desktop\Child-Vaccination-Alert-System\vaccines\bcg.csv"

df = pd.read_csv(input_path)

X = df[[
    "v012","v106","v190","v025","v101",
    "b4","bord","m14","m15","m17",
    "m18","h1","v113","v116"
]]

# 1 = missed vaccination
y = 1 - df["label"]

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# CLASS IMBALANCE HANDLING
# =========================
missed = (y_train == 1).sum()
vaccinated = (y_train == 0).sum()

ratio = vaccinated / missed
scale_weight = 1.5 * ratio   # bias toward recall

# =========================
# RECALL SCORER
# =========================
recall_scorer = make_scorer(recall_score)

# =========================
# BASE MODEL
# =========================
base_model = xgb.XGBClassifier(
    eval_metric="logloss",
    scale_pos_weight=scale_weight,
    random_state=42,
    tree_method="hist",
    n_jobs=-1
)

# =========================
# PARAMETER GRID (FAST)
# =========================
param_grid = {
    "n_estimators": [200, 400],
    "max_depth": [4, 6, 8],
    "learning_rate": [0.03, 0.07],
    "subsample": [0.8, 1],
    "colsample_bytree": [0.7, 1]
}

# =========================
# RANDOMIZED SEARCH
# =========================
search = RandomizedSearchCV(
    estimator=base_model,
    param_distributions=param_grid,
    n_iter=10,
    scoring=recall_scorer,
    cv=3,
    verbose=1,
    n_jobs=-1
)

search.fit(X_train, y_train)

# =========================
# FINAL MODEL TRAINING
# =========================
model = search.best_estimator_

model.fit(
    X_train,
    y_train,
    eval_set=[(X_test, y_test)],
    callbacks=[xgb.callback.EarlyStopping(rounds=20)],
    verbose=False
)

# =========================
# PREDICT PROBABILITIES
# =========================
y_prob = model.predict_proba(X_test)[:, 1]

# =========================
# THRESHOLD OPTIMIZATION
# =========================
best_recall = 0
best_threshold = 0.5

for t in np.arange(0.05, 0.6, 0.01):
    preds = (y_prob >= t).astype(int)
    r = recall_score(y_test, preds)

    if r > best_recall:
        best_recall = r
        best_threshold = t

print("\nBest Threshold:", best_threshold)

y_pred = (y_prob >= best_threshold).astype(int)

# =========================
# METRICS
# =========================
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))



