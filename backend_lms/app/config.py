import os
from dotenv import load_dotenv

load_dotenv()

class Config:
<<<<<<< HEAD
    DB_HOST     = os.getenv("DB_HOST")
    DB_PORT     = int(os.getenv("DB_PORT", 3306))
    DB_USER     = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME     = os.getenv("DB_NAME")
    SECRET_KEY  = os.getenv("SECRET_KEY")

    # Flask-Mail
    MAIL_SERVER         = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT           = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS        = True
    MAIL_USE_SSL        = False
    MAIL_USERNAME       = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD       = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")
    MAIL_DEBUG          = True
=======
    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_USER = "root"
    DB_PASSWORD = ""  # Mets ton mot de passe ici si tu en as un
    DB_NAME = "moodle_dataset"
>>>>>>> yassir
