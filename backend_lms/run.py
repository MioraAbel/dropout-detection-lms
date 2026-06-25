from app import create_app

app = create_app()

if __name__ == "__main__": #Si un autre fichier importe run.py, cette partie ne s'exécute pas
    app.run(debug=True, port=5000)