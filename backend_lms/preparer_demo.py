import mysql.connector
import pandas as pd
import os
import sys

# Ajouter le chemin pour pouvoir importer les modules de l'application
sys.path.append(os.path.dirname(__file__))
from app.models.prediction import predire_batch

def preparer_base_de_donnees():
    print("🚀 Démarrage de la simulation de masse pour la BDD...")

    # 1. Connexion à la base
    conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='moodle_data')
    cursor = conn.cursor()

    # 2. Lire le vrai fichier CSV Moodle
    chemin_csv = os.path.join(os.path.dirname(__file__), "dataset_moodle_final.csv")
    df = pd.read_csv(chemin_csv)
    features_list = df.to_dict(orient="records")

    print(f"📊 {len(features_list)} étudiants trouvés. L'IA analyse les profils...")

    # 3. L'IA fait les prédictions pour TOUT LE MONDE
    predictions = predire_batch(features_list)

    print("💾 Enregistrement des prédictions dans MySQL (Cela peut prendre quelques secondes)...")

    # 4. Mettre à jour la base de données
    for i, pred in enumerate(predictions):
        std_id = i + 1 # L'ID commence à 1
        prob = pred["probabilite_decrochage"]
        
        if prob >= 0.7:
            niveau = "élevé"
        elif prob >= 0.4:
            niveau = "modéré"
        else:
            niveau = "faible"

        # Mettre à jour l'étudiant
        cursor.execute("""
            UPDATE student 
            SET niveau_risque = %s, probabilite_decrochage = %s, probabilite_non_decrochage = %s
            WHERE std_id = %s
        """, (niveau, float(prob), float(pred["probabilite_non_decrochage"]), std_id))

        # Si risque élevé, on génère une alerte
        if niveau == "élevé":
            cursor.execute("""
                INSERT INTO prediction (std_id, risk_score, status, prediction_date) 
                VALUES (%s, %s, %s, NOW())
            """, (std_id, float(prob), niveau))

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Terminé ! Votre base de données est maintenant remplie avec de VRAIES prédictions.")
    print("🌐 Allez tester http://localhost:5000/api/statistiques !")

if __name__ == "__main__":
    preparer_base_de_donnees()
