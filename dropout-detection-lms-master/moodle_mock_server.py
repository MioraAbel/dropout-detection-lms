from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/webservice/rest/server.php', methods=['GET', 'POST'])
def moodle_api():
    # Simuler la réponse de Moodle contenant l'activité d'un étudiant récent
    mock_data = [
        {
            "login_count": random.randint(1, 50),
            "activity_count": random.randint(10, 200),
            "resources_viewed": random.randint(5, 150),
            "days_inactive": random.randint(0, 200),
            "average_grade": round(random.uniform(0, 20), 1),
            "assignments_submitted": random.randint(0, 10),
            "forum_posts": random.randint(0, 5),
            "completion_rate": round(random.uniform(0, 1), 2),
            "quiz_attempts_count": random.randint(0, 15),
            "dropout": 0
        }
    ]
    return jsonify(mock_data)

if __name__ == '__main__':
    print("Serveur Moodle simule demarre sur http://127.0.0.1:5001")
    app.run(port=5001)
