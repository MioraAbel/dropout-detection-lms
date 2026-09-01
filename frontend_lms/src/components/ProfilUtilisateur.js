import React, { useState, useEffect } from "react";
import axios from "axios";

function ProfilUtilisateur({ emailConnecte }) {
    const [etudiant, setEtudiant] = useState(null);
    const [erreur, setErreur] = useState(false);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/apprenants/")
            .then(response => {
                const etudiantTrouve = response.data.find(s => s.email === emailConnecte) || response.data[0];
                if (etudiantTrouve) {
                    setEtudiant(etudiantTrouve);
                } else {
                    setErreur(true);
                }
            })
            .catch(() => setErreur(true));
    }, [emailConnecte]);

    if (!etudiant && !erreur) return <h3>Chargement...</h3>;
    if (erreur) return <h3 style={{ color: "red" }}>Erreur de base de données.</h3>;

    const isRisque = etudiant.niveau_risque === "élevé";

    return (
        <div style={{ textAlign: "center", marginTop: "50px", fontFamily: "sans-serif" }}>
            
            <div style={{ border: "1px solid #ccc", padding: "30px", display: "inline-block", width: "400px", borderRadius: "10px", backgroundColor: "white" }}>
                
                <h2 style={{ color: "#1e3a8a", margin: "0" }}>{etudiant.nom || "Étudiant Anonyme"}</h2>
                <p style={{ color: "gray" }}>{etudiant.email || emailConnecte}</p>
                <hr style={{ margin: "20px 0" }} />

                <h3 style={{ color: isRisque ? "red" : "green" }}>
                    Risque de décrochage : {etudiant.niveau_risque.toUpperCase()}
                </h3>



            </div>
        </div>
    );
}

export default ProfilUtilisateur;
