# %% [markdown]
# # Notebook d'entraînement du modèle de prédiction de décrochage
# 
# Ce notebook charge les données Moodle, prépare les features, entraîne un modèle de stacking (Random Forest + XGBoost + SVM) et sauvegarde les fichiers nécessaires pour le backend Flask.

# %% [markdown]
# ## 1. Installation des bibliothèques (si nécessaires)

# %%
import subprocess
import sys

required_libs = ['pandas', 'numpy', 'scikit-learn', 'xgboost', 'matplotlib', 'seaborn', 'joblib']
for lib in required_libs:
    try:
        __import__(lib.replace('-', '_'))
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])

print("Toutes les bibliothèques sont installées.")

# %% [markdown]
# ## 2. Chargement du dataset Moodle
# 
# Le dataset doit être dans le même dossier que ce notebook, sous le nom `dataset_moodle_final.csv`.
# Si le fichier n'existe pas, on le génère à partir du fichier original `dataset_moodle_features.csv` en recréant la cible `dropout`.

# %%
import pandas as pd
import numpy as np
import os

# Nom du fichier d'entrée
input_file = 'dataset_moodle_features.csv'
output_file = 'dataset_moodle_final.csv'

if not os.path.exists(input_file):
    raise FileNotFoundError(f"Le fichier {input_file} est introuvable. Veuillez le placer dans le répertoire courant.")

# Chargement des données brutes
df = pd.read_csv(input_file)
print(f"Dataset chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes")

# Recalcul du score de risque (identique à la logique du projet)
df['pts_connexion']  = (df['login_count']           < 3).astype(int) * 2
df['pts_activite']   = (df['activity_count']        < 47).astype(int) * 2
df['pts_ressources'] = (df['resources_viewed']      < 36).astype(int) * 1
df['pts_inactivite'] = (df['days_inactive']         >= 180).astype(int) * 3
df['pts_notes']      = (df['average_grade']         < 1).astype(int) * 2
df['pts_devoirs']    = (df['assignments_submitted'] == 0).astype(int) * 2
df['pts_completion'] = (df['completion_rate']       < 0.1).astype(int) * 2
df['pts_forum']      = (df['forum_posts']           == 0).astype(int) * 1
df['pts_quiz']       = (df['quiz_attempts_count']   == 0).astype(int) * 1

df['risk_score'] = df[['pts_connexion','pts_activite','pts_ressources','pts_inactivite',
                       'pts_notes','pts_devoirs','pts_completion','pts_forum','pts_quiz']].sum(axis=1)

# Création de la cible binaire (seuil = 9)
SEUIL = 9
df['dropout'] = (df['risk_score'] >= SEUIL).astype(int)

# Sélection des features et de la cible
features = ['login_count','activity_count','resources_viewed','days_inactive',
            'average_grade','assignments_submitted','forum_posts',
            'completion_rate','quiz_attempts_count']

X = df[features]
y = df['dropout']

print(f"Features : {len(features)} colonnes")
print(f"Répartition de la cible :\n{y.value_counts()}")

# Sauvegarde du dataset final (pour reproductibilité)
df_final = pd.concat([X, y], axis=1)
df_final.to_csv(output_file, index=False)
print(f"Dataset final sauvegardé sous {output_file}")

# %% [markdown]
# ## 3. Séparation entraînement / test et standardisation

# %%
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Séparation 80/20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Standardisation des données
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Entraînement : {X_train_scaled.shape[0]} échantillons")
print(f"Test : {X_test_scaled.shape[0]} échantillons")

# %% [markdown]
# ## 4. Entraînement des modèles de base (Random Forest, XGBoost, SVM)

# %%
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score

# Modèles avec des paramètres raisonnables
rf = RandomForestClassifier(n_estimators=100, random_state=42)
xgb = XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
svm = SVC(probability=True, random_state=42)

# Entraînement
rf.fit(X_train_scaled, y_train)
xgb.fit(X_train_scaled, y_train)
svm.fit(X_train_scaled, y_train)

# Évaluation rapide sur le test
for name, model in [('Random Forest', rf), ('XGBoost', xgb), ('SVM', svm)]:
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    print(f"{name}: Accuracy={accuracy_score(y_test, y_pred):.4f}, Recall={recall_score(y_test, y_pred):.4f}, AUC={roc_auc_score(y_test, y_prob):.4f}")

# %% [markdown]
# ## 5. Construction du modèle de stacking

# %%
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression

# Liste des estimateurs de base
base_estimators = [
    ('rf', rf),
    ('xgb', xgb),
    ('svm', svm)
]

# Méta-modèle : régression logistique
stacking_model = StackingClassifier(
    estimators=base_estimators,
    final_estimator=LogisticRegression(),
    cv=5  # validation croisée pour générer les prédictions d'entraînement
)

# Entraînement du stacking
stacking_model.fit(X_train_scaled, y_train)

# Évaluation
y_pred_stack = stacking_model.predict(X_test_scaled)
y_prob_stack = stacking_model.predict_proba(X_test_scaled)[:, 1]
print(f"Stacking: Accuracy={accuracy_score(y_test, y_pred_stack):.4f}, Recall={recall_score(y_test, y_pred_stack):.4f}, AUC={roc_auc_score(y_test, y_prob_stack):.4f}")

# %% [markdown]
# ## 6. Sauvegarde des fichiers .pkl pour le backend

# %%
import joblib

# Sauvegarde du modèle stacking
joblib.dump(stacking_model, 'stacking_model.pkl')
print("stacking_model.pkl sauvegarde")

# Sauvegarde du scaler
joblib.dump(scaler, 'scaler.pkl')
print("scaler.pkl sauvegarde")

# Sauvegarde de la liste des features (dans le bon ordre)
joblib.dump(features, 'features.pkl')
print("features.pkl sauvegarde")

print("\nLes 3 fichiers sont prêts à être utilisés par le backend Flask.")

# %% [markdown]
# ## 7. (Optionnel) Vérification du chargement des fichiers

# %%
# Test de rechargement pour s'assurer que tout fonctionne
loaded_model = joblib.load('stacking_model.pkl')
loaded_scaler = joblib.load('scaler.pkl')
loaded_features = joblib.load('features.pkl')

print("Fichiers rechargés avec succès.")
print(f"Features : {loaded_features}")
