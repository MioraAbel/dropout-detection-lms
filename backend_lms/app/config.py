import os 
from dotenv import load_dotenv 
load_dotenv()
class Config : 
    DB_HOST=os.getenv("DB_HOST","127.0.0.1")
    DB_PORT=int(os.getenv("DB_PORT",3306))
    DB_USER=os.getenv("DB_USER","root")
    DB_PASSWORD=os.getenv("DB_PASSWORD","")
    DB_NAME     = os.getenv("DB_NAME", "moodle_dataset")
    DB_SECRET_KEY=os.getenv("SECRET_KEY","ma_cle_secret")

    MAIL_SERVER=os.getenv("MAIL_SERVER","stmp@gmail.com")
    MAIL_PORT=int(os.getenv("MAIL_PORT",587))
    MAIL_USE_TLS=True
    MAIL_USE_UDP=False
    MAIL_USERNAME=os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER=os.getenv("")