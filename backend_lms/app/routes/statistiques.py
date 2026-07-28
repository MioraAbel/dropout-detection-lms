from flask import Blueprint,jsonify
from app.database import get_connection

stat_bp=Blueprint("statistiques",__name__)
@stat_bp.route("/api/statistiques",methods=["GET"])
def get_statistiques ():
    connection=get_connection()
    cursor= connection.cursor(dictionary=True)
    try:
        #Nombre total d'apprenants réels dans la table :
        cursor.execute("SELECT COUNT(*) as total FROM student")
        total_apprenants=cursor.fetchone()['total']

        #Nonmbre d'apprenants ont vraiment abondonnée (risque élevé):
        cursor.execute("SELECT COUNT(*) as abandons FROM student WHERE niveau_risque = 'élevé' ")
        abandons=cursor.fetchone()['abandons']

        #Generation d'alertes:
        cursor.execute("SELECT COUNT(*) as alertes FROM prediction")
        alertes_generees=cursor.fetchone()['alertes']

        # Calcule de la répartition des risques (pour un graphique en camembert par exemple)
        cursor.execute("SELECT niveau_risque, COUNT(*) as total FROM student GROUP BY niveau_risque")
        repartition = cursor.fetchall()
        
        repartition_dict = {"faible": 0, "modéré": 0, "élevé": 0}
        for row in repartition:
            if row['niveau_risque'] in repartition_dict:
                repartition_dict[row['niveau_risque']] = row['total']
                
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
        "alertes_generees": alertes_generees,
        "repartition_risques": repartition_dict
    }
    return jsonify(data)






