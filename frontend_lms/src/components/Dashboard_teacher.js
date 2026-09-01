import React, { useState, useEffect } from "react";
import axios from "axios";
import ApprenantCard from "./ApprenantCard";
import RiskChart from "./RiskChart";

function DashboardTeacher() {
  const [apprenants, setApprenants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erreur, setErreur] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/apprenants/")
      .then(res => {
        setApprenants(res.data);
        setLoading(false);
      })
      .catch(err => {
        setErreur("Erreur de connexion à la base de données.");
        setLoading(false);
      });
  }, []);

  if (loading) return <h3 style={{ textAlign: "center", marginTop: "50px" }}>Chargement...</h3>;
  if (erreur)  return <h3 style={{ color: "red", textAlign: "center" }}>{erreur}</h3>;

  const aRisque = apprenants.filter(a => a.niveau_risque.toLowerCase().includes("élevé"));
  const ok = apprenants.filter(a => a.niveau_risque.toLowerCase().includes("faible"));

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "1200px", margin: "0 auto" }}>
      
      <h1 style={{ color: "#1e3a8a", borderBottom: "2px solid #ccc", paddingBottom: "10px" }}>
        Espace Enseignant
      </h1>
      
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "30px" }}>
          <p style={{ color: "gray", fontSize: "18px" }}>
            Total : <b>{apprenants.length} apprenants</b>
          </p>
          <p style={{ color: "#e74c3c", fontSize: "18px", fontWeight: "bold" }}>
            {aRisque.length} étudiants à surveiller
          </p>
      </div>

      <RiskChart apprenants={apprenants} />

      <h2 style={{ color: "#e74c3c", marginTop: "40px", textAlign: "center" }}>Apprenants à risque (Intervention requise)</h2>
      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center" }}>
        {aRisque.length === 0 ? <p>Aucun apprenant à risque.</p> : aRisque.map(a => <ApprenantCard key={a.std_id} apprenant={a} />)}
      </div>

      <h2 style={{ color: "#2ecc71", marginTop: "40px", textAlign: "center" }}>Apprenants sans risque</h2>
      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center" }}>
        {ok.length === 0 ? <p>Aucun apprenant.</p> : ok.map(a => <ApprenantCard key={a.std_id} apprenant={a} />)}
      </div>

    </div>
  );
}

export default DashboardTeacher;