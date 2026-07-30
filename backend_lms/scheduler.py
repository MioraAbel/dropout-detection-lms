import schedule
import time
import requests
import pandas as pd
import mysql.connector
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='moodle_data',
        connection_timeout=600
    )

def mise_a_jour_predictions():
    print(f"\n[{datetime.now()}] Mise à jour des prédictions via l'API...")
    
    try:
        conn = get_connection()
        # On lit les vraies données des étudiants
        df = pd.read_sql("SELECT * FROM dataset_moodle_final", conn)
        conn.close()
        
        for index, row in df.iterrows():
            donnees = {
                'userid':                int(index + 1), # L'ID commence à 1
                'login_count':           float(row.get('login_count', 0)),
                'activity_count':        float(row.get('activity_count', 0)),
                'resources_viewed':      float(row.get('resources_viewed', 0)),
                'days_inactive':         float(row.get('days_inactive', 0)),
                'average_grade':         float(row.get('average_grade', 0)),
                'assignments_submitted': float(row.get('assignments_submitted', 0)),
                'forum_posts':           float(row.get('forum_posts', 0)),
                'completion_rate':       float(row.get('completion_rate', 0)),
                'quiz_attempts_count':   float(row.get('quiz_attempts_count', 0))
            }
            
            response = requests.post(
                'http://127.0.0.1:5000/api/predictions/predire',
                json=donnees
            )
            if response.status_code == 200:
                print(f"Etudiant ID_{index+1} mis à jour ✓")
            else:
                print(f"Erreur API pour l'étudiant ID_{index+1} : {response.text}")
                
    except Exception as e:
        print(f"Erreur globale du scheduler : {e}")
        
    print(f"[{datetime.now()}] Mise à jour terminée.")

schedule.every().day.at("01:00").do(mise_a_jour_predictions)

if __name__ == "__main__":
    print("Scheduler démarré. Lancement immédiat pour test...")
    mise_a_jour_predictions()
    
    while True:
        schedule.run_pending()
        time.sleep(60)