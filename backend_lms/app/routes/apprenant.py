from flask import Blueprint, jsonify
from app.database import get_connection
from app.models.prediction import predire_batch

apprenants_bp = Blueprint("apprenants", __name__, url_prefix="/api/apprenants")

@apprenants_bp.route("/", methods=["GET"])
def get_apprenants():
    # 1. Connexion et récupération des données depuis la base de données
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM dataset_moodle_final"
    cursor.execute(query)
    data = cursor.fetchall()
    
    # 2. Exécution des prédictions directement avec les données de la BDD
    predictions = predire_batch(data)
    
    # 3. Formatage de la réponse
    apprenants = []
    for i, (row, pred) in enumerate(zip(data, predictions)):
        prob = pred["probabilite_decrochage"]
        
        # Calcul du niveau de risque en texte
        if prob >= 0.7:
            niveau = "élevé"
        elif prob >= 0.4:
            niveau = "modéré"
        else:
            niveau = "faible"
            
        # Utilisation des identifiants et emails générés 
        apprenants.append({
            "std_id": f"ID_{i+1}",
            "nom": f"Etudiant {i+1}",
            "email": f"etudiant{i+1}@fsts.ac.ma",
            "niveau_risque": niveau,
            "probabilite_decrochage": prob,
            "probabilite_non_decrochage": pred["probabilite_non_decrochage"]
        })
    
    # 4. Fermeture de la connexion
    cursor.close()
    connection.close()
    
    return jsonify(apprenants)