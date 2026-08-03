import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Charger le dataset
df = pd.read_csv("moodle_features_ready.csv")

# Nettoyage
df["login_count"] = df["login_count"].fillna(df["login_count"].median())
df["resources_viewed"] = df["resources_viewed"].fillna(df["resources_viewed"].median())
df["low_performance_count"] = df["low_performance_count"].fillna(df["low_performance_count"].median())
df["forum_posts"] = df["forum_posts"].fillna(0)

# Features et target
X = df.drop(columns=["userid", "dropout_risk"])
y = df["dropout_risk"]

# Normalisation
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Séparation train/test
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Entraînement Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Évaluation complète
y_pred = rf.predict(X_test)

print("=" * 40)
print("   ÉVALUATION - Random Forest")
print("=" * 40)
print(f"  Accuracy  : {accuracy_score(y_test, y_pred):.3f}")
print(f"  Precision : {precision_score(y_test, y_pred):.3f}")
print(f"  Recall    : {recall_score(y_test, y_pred):.3f}")
print(f"  F1-score  : {f1_score(y_test, y_pred):.3f}")
print("=" * 40)

# Sauvegarde
joblib.dump(rf, "backend_lms/model.pkl")
joblib.dump(scaler, "backend_lms/scaler.pkl")
joblib.dump(list(X.columns), "backend_lms/features.pkl")

print("model.pkl    sauvegardé ✅")
print("scaler.pkl   sauvegardé ✅")
print("features.pkl sauvegardé ✅")