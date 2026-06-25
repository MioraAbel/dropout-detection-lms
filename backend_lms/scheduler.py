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
        password='monmotdepasse',
        database='lms_detection',
        connection_timeout=600
    )

features = ['login_count', 'activity_count', 'resources_viewed',
            'days_inactive', 'average_grade', 'assignments_submitted',
            'forum_posts', 'completion_rate', 'quiz_attempts_count']

def mise_a_jour_predictions():
    print(f"\n[{datetime.now()}] Mise à jour des prédictions...")
    
    # Récupérer les étudiants depuis MySQL
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM student", conn)
    conn.close()
    
    for _, row in df.iterrows():
        donnees = {
            'userid':                row['std_id'],
            'login_count':           0.0,
            'activity_count':        0.0,
            'resources_viewed':      0.0,
            'days_inactive':         row['niveau_risque'],
            'average_grade':         0.0,
            'assignments_submitted': 0.0,
            'forum_posts':           0.0,
            'completion_rate':       0.0,
            'quiz_attempts_count':   0.0
        }
        
        try:
            response = requests.post(
                'http://127.0.0.1:5000/api/predictions/predire',
                json=donnees
            )
            if response.status_code == 200:
                print(f"Etudiant {row['std_id']} mis à jour ✓")
        except Exception as e:
            print(f"Erreur étudiant {row['std_id']} : {e}")
    
    print(f"[{datetime.now()}] Mise à jour terminée.")

schedule.every().day.at("01:00").do(mise_a_jour_predictions)

print("Scheduler démarré. Lancement immédiat pour test...")
mise_a_jour_predictions()

while True:
    schedule.run_pending()
    time.sleep(60)