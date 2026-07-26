import mysql.connector
from mysql.connector import Error
from app.config import Config
def get_connection() :
    try:
        connection = mysql.connector.connect (
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER, 
            password=Config.DB_PASSWORD,                
            database=Config.DB_NAME
        )  
        return connection
    except Error as e :
        print(f" Erreur de connexion à la base de données : {e}")
        return None