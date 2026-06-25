from flask import Blueprint, jsonify
from app.database import get_connection

apprenants_bp = Blueprint("apprenants", __name__, url_prefix="/api/apprenants")

@apprenants_bp.route("/", methods=["GET"])
def get_apprenants():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM student")
    
    apprenants = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return jsonify(apprenants)