import React from "react";

function ApprenantCard({ apprenant }) {
  const isRisque = apprenant.niveau_risque === "élevé" || apprenant.niveau_risque === "modéré";

  return (
    <div style={{
      border: isRisque ? "2px solid #e74c3c" : "2px solid #2ecc71",
      borderRadius: "8px",
      padding: "16px",
      margin: "8px",
      backgroundColor: isRisque ? "#fdecea" : "#eafaf1",
      width: "220px",
      boxShadow: "0 4px 6px rgba(0,0,0,0.1)" 
    }}>
      <h3 style={{ margin: "0 0 8px 0", fontSize: "16px" }}>
        {apprenant.nom}
      </h3>
      <p style={{ margin: "4px 0", fontSize: "14px", color: "#555" }}>
        {apprenant.email}
      </p>
      
      <p style={{ margin: "8px 0 0 0", fontWeight: "bold",
        color: isRisque ? "#e74c3c" : "#2ecc71" }}>
        {isRisque ? " À risque" : " Non à risque"}
      </p>
      <p style={{ margin: "4px 0", fontSize: "13px", textTransform: "capitalize" }}>
        Niveau : <strong>{apprenant.niveau_risque}</strong>
      </p>
      <p style={{ margin: "4px 0", fontSize: "12px", color: "#e74c3c" }}>
        Prob. Décrochage : {(apprenant.probabilite_decrochage * 100).toFixed(1)}%
      </p>
      <p style={{ margin: "4px 0", fontSize: "12px", color: "#2ecc71" }}>
        Prob. Succès : {(apprenant.probabilite_non_decrochage * 100).toFixed(1)}%
      </p>
    </div>
  );
}
export default ApprenantCard;