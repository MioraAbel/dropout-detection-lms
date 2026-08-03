from flask import Blueprint, jsonify
from app.database import get_connection
from app.models.prediction import predire_batch

stat_bp = Blueprint("statistiques", __name__)

@stat_bp.route("/api/statistiques", methods=["GET"])
def get_statistiques():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        # 1. On lit les données brutes (depuis dataset_moodle_final)
        cursor.execute("SELECT * FROM dataset_moodle_final")
        data = cursor.fetchall()
        
        total_apprenants = len(data)
        
        # 2. On fait la prédiction en DIRECT pour tous les étudiants
        predictions = predire_batch(data)
        
        # 3. On calcule les couleurs du graphique en direct
        repartition_dict = {"faible": 0, "élevé": 0}
        abandons = 0
        
        for pred in predictions:
            prob = pred["probabilite_decrochage"]
            if prob >= 0.5:
                niveau = "élevé"
                abandons += 1
            else:
                niveau = "faible"
                
            repartition_dict[niveau] += 1

        # 4. Historique des alertes 
        cursor.execute("SELECT COUNT(*) as alertes FROM prediction")
        alertes_generees = cursor.fetchone()['alertes']
                
        taux_decrochage = 0
        if total_apprenants > 0:
            taux_decrochage = round((abandons / total_apprenants) * 100, 1)
            
    except Exception as e:
        return jsonify({"Erreur": str(e)}), 500
    finally:
        cursor.close()
        connection.close()
        
    data_response = {
        "total_apprenants": total_apprenants,
        "taux_decrochage": taux_decrochage,
        "recall": 100,
        "alertes_generees": alertes_generees,
        "repartition_risques": repartition_dict
    }
    return jsonify(data_response)