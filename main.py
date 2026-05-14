# =========================
# HEART DISEASE PREDICTION AI PROJECT
# Random Forest Classifier
# =========================

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import matplotlib.pyplot as plt
import seaborn as sns


# =========================
# 1. LOAD DATA
# =========================
df = pd.read_csv("heart.csv")

print("\n[INFO] Dataset Loaded")
print(df.head())


# =========================
# 2. SPLIT FEATURES / TARGET
# =========================
X = df.drop("target", axis=1)
y = df["target"]


# =========================
# 3. TRAIN / TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# =========================
# 4. MODEL (RANDOM FOREST)
# =========================
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)


# =========================
# 5. PREDICTIONS
# =========================
y_pred = model.predict(X_test)


# =========================
# 6. EVALUATION
# =========================
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("\n[RESULTS]")
print("Accuracy:", accuracy)

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# =========================
# 7. CONFUSION MATRIX VISUALIZATION
# =========================
plt.figure(figsize=(5,4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")

plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()
plt.show()


# =========================
# 8. FEATURE IMPORTANCE
# =========================
importances = model.feature_importances_

plt.figure(figsize=(8,4))
plt.bar(X.columns, importances)

plt.title("Feature Importance (Random Forest)")
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()