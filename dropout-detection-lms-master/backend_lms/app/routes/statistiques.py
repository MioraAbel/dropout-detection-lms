from flask import Blueprint, jsonify
from app.database import get_connection

stat_bp = Blueprint('statistiques', __name__)

@stat_bp.route('/api/statistiques', methods=['GET'])
def get_statistiques():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # On calcule le nombre total d'apprenants réels dans votre table
        cursor.execute("SELECT COUNT(*) as total FROM dataset_moodle_final")
        total_apprenants = cursor.fetchone()['total']
        
        # On calcule combien d'apprenants ont vraiment abandonné (dropout = 1)
        cursor.execute("SELECT COUNT(*) as abandons FROM dataset_moodle_final WHERE dropout = 1")
        abandons = cursor.fetchone()['abandons']
        
        # On calcule le vrai pourcentage de décrochage
        taux_decrochage = 0
        if total_apprenants > 0:
            taux_decrochage = round((abandons / total_apprenants) * 100, 1)
            
    except Exception as e:
        # S'il y a une erreur 
        return jsonify({"erreur": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

    data = {
        "total_apprenants": total_apprenants,
        "taux_decrochage": taux_decrochage,
        "recall": 100,          # Ce chiffre reste en dur, c'est la perf de votre modèle
        "alertes_generees": 982 # Ce chiffre reste en dur pour le moment
    }
    return jsonify(data)
