from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from app.config import Config

mail = Mail()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(Config)
    
    mail.init_app(app)

    from app.routes.apprenants import apprenants_bp
    from app.routes.predictions import predictions_bp
    from app.routes.alertes import alertes_bp
    from app.routes.statistiques import stat_bp
    from app.routes.utilisateurs import utilisateurs_bp

    app.register_blueprint(apprenants_bp)
    app.register_blueprint(predictions_bp)
    app.register_blueprint(alertes_bp)
    app.register_blueprint(stat_bp)
    app.register_blueprint(utilisateurs_bp)

    return app