import docx
from docx.shared import Pt
import os

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
file_path = os.path.join(desktop, 'Test_Route_Statistiques_PFE.docx')

try:
    doc = docx.Document()
    
    # Titre principal
    title = doc.add_heading('Validation de la Route des Statistiques Globales (KPIs du Dashboard)', 0)
    title.alignment = 1 # Center
    
    # Introduction
    doc.add_heading('1. Objectif du Test', level=1)
    doc.add_paragraph(
        "Ce dernier test d'intégration a pour but de valider la route API dédiée aux statistiques "
        "(GET /api/statistiques). Cette route est essentielle car elle agit comme le moteur du futur Dashboard "
        "interactif de la direction. Son rôle est de synthétiser les milliers de données individuelles "
        "en indicateurs clés de performance (KPIs) lisibles et exploitables instantanément."
    )
    
    # Explication technique
    doc.add_heading('2. Processus Technique et Calculs', level=1)
    p = doc.add_paragraph()
    p.add_run("Lors de l'appel de cette route, le Backend exécute plusieurs requêtes d'agrégation SQL en temps réel sur la base de données :\n").bold = True
    p.add_run("• Volume total : ").bold = True
    p.add_run("Comptage du nombre exact d'étudiants enregistrés dans la table globale (ici, 3046 apprenants).\n")
    p.add_run("• Taux de décrochage : ").bold = True
    p.add_run("Calcul mathématique dynamique basé sur le ratio entre le nombre total d'étudiants et ceux ayant été classifiés avec un risque 'élevé' par le modèle de Machine Learning.\n")
    p.add_run("• Répartition des risques : ").bold = True
    p.add_run("Agrégation des profils (GROUP BY) pour obtenir le nombre précis d'étudiants dans chaque catégorie (Faible, Modéré, Élevé).\n")
    p.add_run("• Traçabilité des alertes : ").bold = True
    p.add_run("Comptage du nombre d'alertes historisées pour assurer un suivi de l'activité du système.")

    # Les résultats (les photos de l'utilisateur)
    doc.add_heading('3. Résultats Obtenus et Impact pour le Frontend', level=1)
    doc.add_paragraph(
        "L'exécution de la requête retourne un objet JSON propre et structuré. L'exactitude des calculs a été "
        "vérifiée avec succès (le nombre total correspond bien à la somme des différentes catégories de risque)."
    )
    
    doc.add_paragraph("[ ---> GLISSEZ LA CAPTURE D'ÉCRAN DU JSON DE LA ROUTE STATISTIQUES JUSTE ICI <--- ]").bold = True
    
    doc.add_paragraph(
        "L'intérêt majeur de cette structuration des données réside dans son interfaçage direct avec les bibliothèques "
        "graphiques du Frontend (ex: Chart.js, Recharts). Par exemple, l'objet 'repartition_risques' est conçu sur mesure "
        "pour générer instantanément un graphique en camembert (Pie Chart), tandis que le 'taux_decrochage' alimentera "
        "une carte d'indicateur d'alerte (Widget) sur le tableau de bord principal de l'administration."
    )
    
    # Sauvegarde
    doc.save(file_path)
    print("Le document a été créé avec succès !")
    
except Exception as e:
    print(f"Erreur : {e}")
