from flask import Blueprint,jsonify,request
from app.database import get_connection 
from app.models.prediction import predire 

predictions_bp=Blueprint("predictions",__name__,url_prefix="/api/predictions")
@predictions_bp.route("/",methods=["GET"])

def get_prediction():
    connection =get_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prediction")
    predictions=cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(predictions)

@predictions_bp.route("/<int:pred_id>",methods=["GET"])
def get_prediction(pred_id):
    connection=get_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prediction WHERE pred_id=%s",(pred_id,))
    prediction=cursor.fetchone()
    cursor.close()
    connection.close()
    if prediction is None :
        return jsonify({"Erreur":"predition non trouvé"}),404
    return jsonify(prediction)

@predictions_bp.route("/predire",methods=["POST"])
def faire_predire():
    data=request.get_json()
    if not data:
        return jsonify({"Erreur":"Aucune donnée trouvé"}),400
    resultats=predire(data)
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute ("""
    UPDATE student SET 
    niveau_risque       = %s,
    probabilite_decrochage      = %s,
    probabilite_non_decrochage      = %s,
    status      = %s WHERE std_id    = %s
    """, (
        resultats["risque_decrochage"], 
        resultats["probabilite_decrochage"],
        resultats["probabilite_decrochage"],
        resultats["probabilite_non_decrochage"],
        resultats["statut"],
        data.get("userid")
    ))

    if resultats["risque_decrochage"]  == "élevé":
        cursor.execute("""
        INSERT INTO prediction
        (std_id,risk_score,status,prediction_date) VALUES (%s,%s,%s,NOW())
        """, ( data.get("userid"),
            resultats["probabilite_decrochage"],
            resultats["risque_decrochage"]
        ))

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(resultats),200




