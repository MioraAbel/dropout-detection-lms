from flask import Blueprint, jsonify
from app.database import get_connection
from app.models.prediction import predire_batch
import pandas as pd
import os

apprenants_bp = Blueprint("apprenants", __name__, url_prefix="/api/apprenants")

@apprenants_bp.route("/", methods=["GET"])
def get_apprenants():
    # 1. On récupère les étudiants depuis la base de données (pour avoir les ID, noms, emails)
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM student"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    # 2. On lit les statistiques Moodle depuis le CSV pour faire les prédictions
    # On cherche le fichier à la racine du projet
    chemin_csv = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "dataset_moodle_final.csv")
    
    try:
        df_features = pd.read_csv(chemin_csv)
        # On convertit le dataframe en liste de dictionnaires pour le modèle
        features_list = df_features.to_dict(orient="records")
    except Exception as e:
        print("Erreur lors de la lecture du CSV:", e)
        features_list = [] # Sécurité si le fichier n'est pas trouvé

    # 3. On fait les prédictions sur les VRAIES statistiques !
    predictions = predire_batch(features_list)

    # 4. On combine les données de la BDD et les prédictions
    apprenants = []
    # On s'assure qu'on boucle bien sur les deux listes en même temps
    for row, pred in zip(data, predictions):
        
        # Le modèle renvoie une probabilité (ex: 0.85). On détermine le texte associé :
        prob = pred["probabilite_decrochage"]
        if prob >= 0.7:
            niveau = "élevé"
        elif prob >= 0.4:
            niveau = "modéré"
        else:
            niveau = "faible"
            
        apprenants.append({
            "std_id": row["std_id"],
            "nom": row["nom"],
            "email": row["email"],
            "niveau_risque": niveau, # <-- Texte lisible ("élevé", "faible"...) au lieu du chiffre brut
            "probabilite_decrochage": prob,
            "probabilite_non_decrochage": pred["probabilite_non_decrochage"]
        })

    return jsonify(apprenants)

