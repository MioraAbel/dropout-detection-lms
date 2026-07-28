from flask import Blueprint,jsonify

utilisateurs_bp=Blueprint("utilisateurs",__name__)
@utilisateurs_bp.route('/api/utilisateurs',methods=['GET'])
def get_utilisateurs():
    utilisateurs_mock= [
        {
            "id":1,
            "initiales":"PA",
            "nom":"Prof. Alami",
            "email":"p.alami@fsts.ac.ma",
            "role": "Enseignant"
        },
        {
            "id": 2,
            "initiales": "AO",
            "nom": "Ahmed Ouali",
            "email": "a.ouali@fsts.ac.ma",
            "role": "Apprenant"
        },
        {
            "id": 3,
            "initiales": "AS",
            "nom": "Admin Système",
            "email": "admin@fsts.ac.ma",
            "role": "Admin"
        }
    ]
    return jsonify(utilisateurs_mock)

