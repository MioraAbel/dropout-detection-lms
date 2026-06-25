from flask import Blueprint, jsonify, request
from app.database import get_connection

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
    
    if not message or not alert_id:
        return jsonify({"erreur": "message et alert_id sont obligatoires"}), 400
    
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute(
        "INSERT INTO alert (alert_id, message, date_alert) VALUES (%s, %s, NOW())",
        (alert_id, message)
    )
    
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return jsonify({"message": "Alerte créée avec succès"}), 201