from flask import Blueprint , request, jsonify
from flask_mail import Message
from app.database import get_connection
from app import mail
import os


alertes_bp=Blueprint("alertes",__name__,"/api/alertes")
@alertes_bp.route("/",methods=["GET"])

def get_alertes():
    connection=get_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alert")
    alertes = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(alertes)

@alertes_bp.route("/",methods=["POST"])
def create_alerte():
    data=request.get_json()
    message=data.get("message")
    alert_id=data.get("alert_id")
    email_enseignant=data.get("email_enseignant")
    if not message or not alert_id :
        return jsonify({"Erreur": "alert_id et message sont obligatoire"}),400

    alertes_actives = os.getenv("ALERTES_ACTIVE", "true").lower() == "true"
    connection2=get_connection()
    cursor=connection2.cursor(dictionary=True)
    cursor.execute("INSERT INTO alert (alert_id,message,date_alert)VALUES(%s,%s,NOW()"),(alert_id,message)
    connection2.commit()
    cursor.close()
    connection2.close()

    alertes_acive = config and config["valeur"] =="true"
    if email_enseignant and alertes_acive :
        try :
            msg=Message(
                subject="Alerte décrochage - Étudiant en risque de décrochage",
                recipients=[email_enseignant],
                body=f"Bonjour,\n\nUne alerte a été générée :\n\n{message}\n\nVeuillez consulter votre tableau de bord pour plus de détails.\n\nSystème de détection du décrochage LMS"
            )
            mail.send(msg)
            return jsonify({"Message":"Alerte crée et email envoyé avec succès"}),201
        except Exception as e:
            return jsonify({"Message":"Alerte crée mais email non envoyée","Erreur":str(e)}),201
    return jsonify({"Message":"Alerte crée et email envoyée avec succées"}),201

@alertes_bp.route("/config/alertes-auto",methods=["GET"])
def get_alertes_auto():
    connection=get_connection()
    cursor=connection.cursor(dictionary=True)
    cursor.execute("SELECT valeur FROM configuration WHERE cle= 'alertes_auto'")
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return jsonify({"alerte_auto": result["valeur"] == "true"})

@alertes_bp.route("/config/alertes-auto",methods=["PUT"])
def toggle_alertes_auto():
    data = request.get_json()
    valeur = "true" if data.get("alertes_auto") else "false"

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE configuration SET valeur = %s WHERE cle = 'alertes_auto'",
        (valeur,)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": f"Alertes auto : {valeur}"})