import React, { useState, useEffect } from "react";
import axios from "axios";

// Ce composant affiche le profil d'un étudiant spécifique en fonction de son email
function ProfilUtilisateur({ emailConnecte }) {
    const [etudiant, setEtudiant] = useState(null);
    const [erreur, setErreur] = useState(false);

    useEffect(() => {
        // On va chercher la liste de tous les étudiants depuis l'API
        axios.get("http://127.0.0.1:5000/api/apprenants/")
            .then(response => {
                // On cherche l'étudiant qui correspond à l'email tapé dans le Login
                const etudiantTrouve = response.data.find(s => s.email === emailConnecte);
                
                if (etudiantTrouve) {
                    setEtudiant(etudiantTrouve);
                } else {
                    setErreur(true); // L'email n'existe pas dans la base de données
                }
            })
            .catch(error => {
                console.error("Erreur de connexion API", error);
                setErreur(true);
            });
    }, [emailConnecte]);

    // Affichage pendant le chargement
    if (!etudiant && !erreur) {
        return <div style={{ padding: "20px", textAlign: "center", color: "#64748b" }}>Recherche de vos données en cours...</div>;
    }

    // Affichage si l'étudiant n'est pas trouvé
    if (erreur) {
        return (
            <div style={{ padding: "20px", textAlign: "center", color: "#ef4444", fontWeight: "bold" }}>
                Erreur : Impossible de trouver un étudiant avec l'adresse "{emailConnecte}".
            </div>
        );
    }

    const isRisque = etudiant.niveau_risque === "élevé";
    const badgeColor = isRisque ? "#ef4444" : "#10b981"; // Rouge ou Vert
    const backgroundColor = isRisque ? "#fef2f2" : "#f0fdf4"; // Rouge clair ou Vert clair

    return (
        <div style={{
            backgroundColor: "white", borderRadius: "10px", padding: "25px",
            boxShadow: "0 4px 6px rgba(0,0,0,0.05)", border: "1px solid #e2e8f0",
            maxWidth: "500px", margin: "0 auto"
        }}>
            {/* EN-TÊTE : Photo (initiales) et Nom */}
            <div style={{ display: "flex", alignItems: "center", gap: "15px", marginBottom: "20px" }}>
                <div style={{
                    width: "60px", height: "60px", borderRadius: "50%",
                    backgroundColor: "var(--fst-blue, #1e3a8a)", color: "white",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: "24px", fontWeight: "bold"
                }}>
                    {etudiant.nom ? etudiant.nom.substring(0, 2).toUpperCase() : "ET"}
                </div>
                <div>
                    <h2 style={{ margin: "0", fontSize: "20px", color: "#1e293b" }}>
                        {etudiant.nom || "Étudiant Inconnu"}
                    </h2>
                    <p style={{ margin: "0", color: "#64748b", fontSize: "14px" }}>
                        {etudiant.email || "email@fsts.ac.ma"}
                    </p>
                </div>
            </div>

            <hr style={{ border: "none", borderTop: "1px solid #e2e8f0", margin: "20px 0" }} />

            {/* SECTION 1 : Le résultat de l'Intelligence Artificielle */}
            <h3 style={{ fontSize: "16px", color: "#475569", marginBottom: "15px" }}>Prédiction de l'IA</h3>
            <div style={{
                backgroundColor: backgroundColor, borderLeft: `4px solid ${badgeColor}`,
                padding: "15px", borderRadius: "4px", display: "flex",
                justifyContent: "space-between", alignItems: "center"
            }}>
                <span style={{ fontWeight: "bold", color: "#1e293b" }}>Risque de décrochage :</span>
                <span style={{ 
                    backgroundColor: badgeColor, color: "white", padding: "4px 10px", 
                    borderRadius: "12px", fontSize: "12px", fontWeight: "bold", textTransform: "uppercase" 
                }}>
                    {etudiant.niveau_risque || "Inconnu"}
                </span>
            </div>

            {/* SECTION 2 : Statistiques Moodle (Comportement) */}
            <h3 style={{ fontSize: "16px", color: "#475569", marginTop: "25px", marginBottom: "15px" }}>
                Comportement sur Moodle
            </h3>
            
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "15px" }}>
                <div style={{ backgroundColor: "#f8fafc", padding: "15px", borderRadius: "8px", textAlign: "center" }}>
                    <p style={{ margin: "0 0 5px 0", fontSize: "12px", color: "#64748b" }}>Connexions</p>
                    <p style={{ margin: "0", fontSize: "20px", fontWeight: "bold", color: "#0f172a" }}>
                        {etudiant.login_count || 0}
                    </p>
                </div>
                <div style={{ backgroundColor: "#f8fafc", padding: "15px", borderRadius: "8px", textAlign: "center" }}>
                    <p style={{ margin: "0 0 5px 0", fontSize: "12px", color: "#64748b" }}>Note Moyenne</p>
                    <p style={{ margin: "0", fontSize: "20px", fontWeight: "bold", color: "#0f172a" }}>
                        {etudiant.average_grade !== undefined ? etudiant.average_grade + "/20" : "N/A"}
                    </p>
                </div>
            </div>
        </div>
    );
}

export default ProfilUtilisateur;
