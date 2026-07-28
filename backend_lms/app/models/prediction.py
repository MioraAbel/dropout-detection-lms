import joblib
import pandas as pd
import os

BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

#Chargement du modele dee stacking et du Scaler
model = joblib.load(os.path.join(BASE_DIR,"stacking_model.pkl"))
scaler= joblib.load(os.path.join(BASE_DIR,"scaler.pkl"))
features = joblib.load(os.path.join(BASE_DIR,"features.pkl"))

def predire(donnees : dict) -> dict :
    df = pd.DataFrame([donnees])
    df=df.reindex(columns=features,fill_value=0)
    df=df.apply(pd.to_numeric,errors='coerce').fillna(0)

    df_sc=scaler.transform(df)

    probas= model.predict_proba(df_sc)[0]
    prob_non_risque=round(float(probas[0]),3)
    prob_risque=round(float(probas[1]),3)
    risque_texte="élevé" if prob_risque >=0.7 else ("modéré"if prob_risque >=0.4 else "faible")

    return {
        "risque_decrochage":risque_texte,
        "probabilite_non_decrochage": prob_non_risque,
        "probabilite_decrochage" : prob_risque,
        "statut":"succes"
    }

def predire_batch(liste_donnees : list) -> list :
    if not liste_donnees : return []
    df=pd.DataFrame(liste_donnees)
    df=df.reindex(columns=features,fill_value=0)
    df=df.apply(pd.to_numeric,errors="coerce").fillna(0)

    df_sc=scaler.transform(df)
    probas = model.predict_proba(df_sc)
    resultats=[]
    for proba in probas:
        resultats.append({
            "probabilite_non_decrochage":round(float(proba[0]),3),
            "probabilite_decrochage":round(float(proba[1]),3)
        })
    return resultats






