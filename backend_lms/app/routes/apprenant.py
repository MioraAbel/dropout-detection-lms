from flask import Blueprint,jsonify
from app.database import get_connection
from app.models.prediction import predire

apprenants_bp=Blueprint("apprenants",__name__,url_prefix="/api/apprenants")
@apprenants_bp.route("/",methods=["GET"])
def get_apprenants():
    connection=get_connection()
    cursor=connection.cursor(dictionary=True)
    query="SELECT * FROM moodle_dataset_final"
    cursor.execute(query)
    data = cursor.fetchall()

    from app.models.prediction import predire_batch
    predictions=predire_batch(data)

    apprenants=[]
    for i, (row,pred) in enumerate (zip(data,predictions)):
        apprenants.append({
            "std_id": f"ID_{i+1}",
            "nom": f"Etudiant_{i+1}",
            "email":f"etudiants{i+1}@fsts.ac.ma",

            "niveau_risque": pred["probabilite_decrochage"],
            "probabilite_decrochage":pred["probabilite_decrochage"],
            "probabilite_non_decrochage":pred["probabilite_non_decrochage"]
        })
    cursor.close()
    connection.close()
    return jsonify(apprenants)

