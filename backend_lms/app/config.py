import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_USER = "root"
    DB_PASSWORD = ""  # Mets ton mot de passe ici si tu en as un
    DB_NAME = "moodle_dataset"