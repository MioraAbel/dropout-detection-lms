import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

model    = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "features.pkl"))

def predire(donnees: dict) -> dict:
    df = pd.DataFrame([donnees])
    df = df.reindex(columns=features, fill_value=0)
    
    probas          = model.predict_proba(df)[0]
    prob_non_risque = round(float(probas[0]), 3)
    prob_risque     = round(float(probas[1]), 3)
    
    status = "risque" if prob_risque >= 0.5 else "non à risque"
    
    return {
        "probabilite_decrochage":     prob_risque,
        "probabilite_non_decrochage": prob_non_risque,
        "status": status
    }