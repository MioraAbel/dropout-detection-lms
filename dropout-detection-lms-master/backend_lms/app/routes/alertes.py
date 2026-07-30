from flask import Blueprint, jsonify, request
from flask_mail import Message
from app.database import get_connection
from app import mail

alertes_bp = Blueprint("alertes", __name__, url_prefix="/api/alertes")

@alertes_bp.route("/", methods=["GET"])
def get_alertes():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alert")
    alertes = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(alertes)


@alertes_bp.route("/", methods=["POST"])
def create_alerte():
    data = request.get_json()
    message = data.get("message")
    alert_id = data.get("alert_id")
    email_enseignant = data.get("email_enseignant")

    if not message or not alert_id:
        return jsonify({"erreur": "message et alert_id sont obligatoires"}), 400

    # Sauvegarde en base de données
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO alert (alert_id, message, date_alert) VALUES (%s, %s, NOW())",
        (alert_id, message)
    )
    connection.commit()
    cursor.close()
    connection.close()

    # Vérifier si les alertes auto sont activées
    connection2 = get_connection()
    cursor2 = connection2.cursor(dictionary=True)
    cursor2.execute("SELECT valeur FROM configuration WHERE cle = 'alertes_auto'")
    config = cursor2.fetchone()
    cursor2.close()
    connection2.close()

    alertes_actives = config and config["valeur"] == "true"

    # Envoi email seulement si alertes activées et email fourni
    if email_enseignant and alertes_actives:
        try:
            msg = Message(
                subject="⚠️ Alerte décrochage — Étudiant à risque détecté",
                recipients=[email_enseignant],
                body=f"Bonjour,\n\nUne alerte a été générée :\n\n{message}\n\nVeuillez consulter votre tableau de bord pour plus de détails.\n\nSystème de détection du décrochage LMS"
            )
            mail.send(msg)
            return jsonify({"message": "Alerte créée et email envoyé"}), 201
        except Exception as e:
            return jsonify({"message": "Alerte créée mais email non envoyé", "erreur": str(e)}), 201

    return jsonify({"message": "Alerte créée avec succès"}), 201

@alertes_bp.route("/config/alertes-auto", methods=["GET"])
def get_alertes_auto():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT valeur FROM configuration WHERE cle = 'alertes_auto'")
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return jsonify({"alertes_auto": result["valeur"] == "true"})


@alertes_bp.route("/config/alertes-auto", methods=["PUT"])
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