import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

# 1. Charger les donnees
df = pd.read_csv(r'C:\Users\HP\Desktop\dropout-detection-lms\dataset_moodle_features.csv')

# 2. Systeme de score (reprise exacte de justification_stacking.ipynb)
df['pts_connexion']  = (df['login_count']           <  3   ).astype(int) * 2
df['pts_activite']   = (df['activity_count']         < 47   ).astype(int) * 2
df['pts_ressources'] = (df['resources_viewed']       < 36   ).astype(int) * 1
df['pts_inactivite'] = (df['days_inactive']          >= 180  ).astype(int) * 3
df['pts_notes']      = (df['average_grade']          <  1   ).astype(int) * 2
df['pts_devoirs']    = (df['assignments_submitted']  == 0   ).astype(int) * 2
df['pts_completion'] = (df['completion_rate']        <  0.1 ).astype(int) * 2
df['pts_forum']      = (df['forum_posts']            == 0   ).astype(int) * 1
df['pts_quiz']       = (df['quiz_attempts_count']    == 0   ).astype(int) * 1

pts_cols = ['pts_connexion','pts_activite','pts_ressources','pts_inactivite',
            'pts_notes','pts_devoirs','pts_completion','pts_forum','pts_quiz']
df['risk_score'] = df[pts_cols].sum(axis=1)

SEUIL = 9
y = (df['risk_score'] >= SEUIL).astype(int)

features = ['login_count','activity_count','resources_viewed','days_inactive',
            'average_grade','assignments_submitted','forum_posts',
            'completion_rate','quiz_attempts_count']
X = df[features]

# 3. Standardisation (Cruciale pour SVM et Stacking)
scaler = StandardScaler()
X_sc = scaler.fit_transform(X) # On l'entraine sur TOUT le dataset pour avoir le modele final le plus performant

# 4. Definition du Stacking (Niveau 2)
base_models = [
    ('rf',  RandomForestClassifier(random_state=42)),
    ('xgb', XGBClassifier(random_state=42, eval_metric='logloss')),
    ('svm', SVC(probability=True, random_state=42))
]
stacking = StackingClassifier(
    estimators=base_models,
    final_estimator=LogisticRegression(),
    cv=5
)

# 5. Entrainement
print("Entrainement du Stacking en cours...")
stacking.fit(X_sc, y)
print("Entrainement termine!")

# 6. Sauvegarde dans le Backend
backend_dir = r"C:\Users\HP\Desktop\dropout-detection-lms\backend_lms"
joblib.dump(stacking, os.path.join(backend_dir, 'stacking_model.pkl'))
joblib.dump(scaler, os.path.join(backend_dir, 'scaler.pkl'))
joblib.dump(features, os.path.join(backend_dir, 'features.pkl'))
print("Fichiers sauvegardes dans le backend!")
