import React, { useState, useEffect } from "react";
import axios from "axios";
import ApprenantCard from "./ApprenantCard";
import RiskChart from "./RiskChart";

function Dashboard() {
  const [apprenants, setApprenants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erreur, setErreur] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/apprenants/")
      .then(response => {
        setApprenants(response.data);
        setLoading(false);
      })
      .catch(err => {
        setErreur("Impossible de contacter le serveur Flask.");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Chargement...</p>;
  if (erreur)  return <p style={{ color: "red" }}>{erreur}</p>;

  const aRisque = apprenants.filter(a => a.niveau_risque >= 0.5);
  const ok      = apprenants.filter(a => a.niveau_risque < 0.5);

  return (
    <div style={{ padding: "24px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ color: "#2c3e50" }}>
        Dashboard Enseignant
      </h1>
      <p style={{ color: "#777" }}>
        {apprenants.length} apprenants au total —{" "}
        <span style={{ color: "#e74c3c", fontWeight: "bold" }}>
          {aRisque.length} à risque
        </span>
      </p>

      <RiskChart apprenants={apprenants} />

      <h2 style={{ color: "#e74c3c", marginTop: "32px" }}>
        Apprenants à risque
      </h2>
      <div style={{ display: "flex", flexWrap: "wrap" }}>
        {aRisque.length === 0
          ? <p>Aucun apprenant à risque.</p>
          : aRisque.map(a => <ApprenantCard key={a.std_id} apprenant={a} />)
        }
      </div>

      <h2 style={{ color: "#2ecc71", marginTop: "32px" }}>
        Apprenants OK
      </h2>
      <div style={{ display: "flex", flexWrap: "wrap" }}>
        {ok.length === 0
          ? <p>Aucun apprenant.</p>
          : ok.map(a => <ApprenantCard key={a.std_id} apprenant={a} />)
        }
      </div>
    </div>
  );
}

export default Dashboard;