from flask import Flask
from flask_cors import CORS  #qui autorise React à parler à Flask

def create_app(): #Application factory
    app = Flask(__name__)
    CORS(app) #active CORS sur toute l'application en une ligne

    from app.routes.apprenants import apprenants_bp
    from app.routes.predictions import predictions_bp
    from app.routes.alertes import alertes_bp

    app.register_blueprint(apprenants_bp)
    app.register_blueprint(predictions_bp)
    app.register_blueprint(alertes_bp)

    return app