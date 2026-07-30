from flask import Blueprint, jsonify
from app.database import get_connection
from app.models.prediction import predire_batch
import pandas as pd
import os

apprenants_bp = Blueprint("apprenants", __name__, url_prefix="/api/apprenants")

@apprenants_bp.route("/", methods=["GET"])
def get_apprenants():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM student"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    chemin_csv = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "dataset_moodle_final.csv")
    
    try:
        df_features = pd.read_csv(chemin_csv)
        features_list = df_features.to_dict(orient="records")
    except Exception as e:
        print("Erreur lors de la lecture du CSV:", e)
        features_list = []

    predictions = predire_batch(features_list)

    apprenants = []
    for row, pred in zip(data, predictions):
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
            "niveau_risque": niveau,
            "probabilite_decrochage": prob,
            "probabilite_non_decrochage": pred["probabilite_non_decrochage"]
        })

    return jsonify(apprenants)
