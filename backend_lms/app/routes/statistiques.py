from flask import Blueprint,jsonify
from app.database import get_connection

stat_bp=Blueprint("statistiques",__name__)
@stat_bp.route("/api/statistiques",methods=["GET"])
def get_statistiques ():
    connection=get_connection()
    cursor= connection.cursor(dictionary=True)
    try:
        #Nombre total d'apprenants réels dans la table :
        cursor.execute("SELECT COUNT(*) as total FROM dataset_moodle_final")
        total_apprenants=cursor.fetchone()['total']

        #Nonmbre d'apprenants ont vraiment abondonnée:
        cursor.execute("SELECT COUNT(*) as abandons FROM dataset_moodle_final WHERE dropout = 1 ")
        abandons=cursor.fetchone()['abandons']

        #Generation d'alertes:
        cursor.execute("SELECT COUNT(*) as alertes FROM alert")
        alertes_generees=cursor.fetchone()['alertes']

        #Calcule du taux de decrochage :
        taux_decrochage=0
        if total_apprenants > 0:
            taux_decrochage=round((abandons/total_apprenants)*100,1)
    except Exception as e:
        return jsonify({"Erreur":str(e)}),500
    finally:
        cursor.close()
        connection.close()
    data = {
        "total_apprenants": total_apprenants,
        "taux_decrochage":taux_decrochage,
        "recall": 100,
        "alertes_generees": alertes_generees
    }
    return jsonify(data)






