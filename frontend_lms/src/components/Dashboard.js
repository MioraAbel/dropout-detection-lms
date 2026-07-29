import React, { useState, useEffect } from "react";
import axios from "axios";
import RiskChart from "./RiskChart";

function Dashboard() {
    const [apprenants, setApprenants] = useState([]);
    const [stats, setStats] = useState(null);
    const [utilisateurs, setUtilisateurs] = useState([]); 
    const [loading, setLoading] = useState(true);
    const [erreur, setErreur] = useState(null);
    
    // Nouvel état pour le bouton d'automatisation
    const [alertesAuto, setAlertesAuto] = useState(false);
    // État pour le menu interactif
    const [menuActif, setMenuActif] = useState("Tableau de bord");

    useEffect(() => {
        axios.all([
            axios.get("http://127.0.0.1:5000/api/apprenants/"),
            axios.get("http://127.0.0.1:5000/api/statistiques"),
            axios.get("http://127.0.0.1:5000/api/utilisateurs")
        ])
        .then(axios.spread((resApprenants, resStats, resUsers) => {
            setApprenants(resApprenants.data);
            setStats(resStats.data);
            setUtilisateurs(resUsers.data);
            setLoading(false);
        }))
        .catch(err => {
            setErreur("Impossible de contacter le serveur Flask.");
            setLoading(false);
        });
    }, []);

    if (loading) return <p>Chargement...</p>;
    if (erreur) return <p style={{color : "red"}}>{erreur}</p>;

    const aRisque = apprenants.filter(a => a.niveau_risque === "élevé" || a.niveau_risque === "modéré");
    const ok = apprenants.filter(a => a.niveau_risque === "faible");

    return (
        <div className="app-container">
            
            {/* --- 1. LA BARRE LATÉRALE BLEUE --- */}
            <div className="sidebar">
                <div style={{ padding: "30px 20px", borderBottom: "1px solid rgba(255,255,255,0.1)" }}>
                    <div style={{ 
                        backgroundColor: "var(--fst-orange)", width: "60px", height: "60px", 
                        borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center",
                        fontWeight: "bold", fontSize: "22px", marginBottom: "20px"
                    }}>
                        FST
                    </div>
                    <h2 style={{ fontSize: "18px", margin: "0", color: "white" }}>Détection décrochage</h2>
                    <p style={{ fontSize: "13px", color: "#94a3b8", margin: "5px 0 0 0" }}>Vue Administrateur</p>
                </div>
                
                {/* Menu supprimé pour épurer l'interface de soutenance */}
                
                <div style={{ marginTop: "auto", padding: "20px", borderTop: "1px solid rgba(255,255,255,0.1)" }}>
                    <p style={{ margin: "0", fontWeight: "bold", fontSize: "14px" }}>Admin Système</p>
                    <p style={{ margin: "0", fontSize: "12px", color: "#94a3b8" }}>Responsable IT</p>
                </div>
            </div>

            {/* --- 2. LA ZONE PRINCIPALE GRISE --- */}
            <div className="main-content">
                
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "20px 0", marginBottom: "30px" }}>
                    <h1 style={{ fontSize: "24px", color: "var(--fst-blue)", margin: "0", fontWeight: "600" }}>Administration système</h1>
                    <div style={{ display: "flex", alignItems: "center", gap: "20px" }}>
                        <span style={{ color: "#10b981", fontSize: "14px", fontWeight: "500" }}>● Système opérationnel</span>
                        <div style={{ backgroundColor: "var(--fst-orange)", color: "white", width: "45px", height: "45px", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "bold" }}>AS</div>
                    </div>
                </div>

                {/* --- 3. LES 4 CARTES KPI --- */}
                <div id="section-statistiques" style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "20px", marginBottom: "30px" }}>
                    <div className="fst-card">
                        <h3 style={{ margin: "0 0 15px 0", fontSize: "14px", color: "var(--text-gray)", fontWeight: "normal" }}>Total apprenants</h3>
                        <p style={{ margin: "0", fontSize: "32px", color: "var(--fst-blue)", fontWeight: "300" }}>{apprenants.length}</p>
                    </div>
                    <div className="fst-card">
                        <h3 style={{ margin: "0 0 15px 0", fontSize: "14px", color: "var(--text-gray)", fontWeight: "normal" }}>Taux de décrochage</h3>
                        <p style={{ margin: "0", fontSize: "32px", color: "#e74c3c", fontWeight: "300" }}>{stats ? stats.taux_decrochage : "0"}%</p>
                    </div>
                    <div className="fst-card">
                        <h3 style={{ margin: "0 0 15px 0", fontSize: "14px", color: "var(--text-gray)", fontWeight: "normal" }}>Recall du modèle</h3>
                        <p style={{ margin: "0", fontSize: "32px", color: "#10b981", fontWeight: "300" }}>{stats ? stats.recall : "100"}%</p>
                    </div>
                    <div className="fst-card">
                        <h3 style={{ margin: "0 0 15px 0", fontSize: "14px", color: "var(--text-gray)", fontWeight: "normal" }}>Alertes générées</h3>
                        <p style={{ margin: "0", fontSize: "32px", color: "var(--fst-orange)", fontWeight: "300" }}>{stats ? stats.alertes_generees : "0"}</p>
                    </div>
                </div>

                {/* --- 4. LES WIDGETS DU BAS --- */}
                <div id="section-configuration" style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "20px", paddingBottom: "50px" }}>
                    
                    {/* Widget 1 : Répartition */}
                    <div className="fst-card">
                        <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "20px" }}>
                            <div style={{ width: "4px", height: "16px", backgroundColor: "var(--fst-orange)" }}></div>
                            <h3 style={{ margin: "0", color: "var(--fst-blue)", fontSize: "16px" }}>Répartition apprenants</h3>
                        </div>
                        <RiskChart apprenants={apprenants} />
                    </div>

                    {/* Widget 2 : Configuration */}
                    <div className="fst-card">
                        <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "20px" }}>
                            <div style={{ width: "4px", height: "16px", backgroundColor: "var(--fst-orange)" }}></div>
                            <h3 style={{ margin: "0", color: "var(--fst-blue)", fontSize: "16px" }}>Configuration système</h3>
                        </div>
                        <div style={{ display: "flex", justifyContent: "space-between", borderBottom: "1px solid #f1f5f9", padding: "15px 0", fontSize: "14px" }}>
                            <span>Modèle actif</span>
                            <span style={{ color: "#10b981", fontWeight: "bold" }}>XGBoost</span>
                        </div>
                        <div style={{ display: "flex", justifyContent: "space-between", borderBottom: "1px solid #f1f5f9", padding: "15px 0", fontSize: "14px" }}>
                            <span>Seuil alerte</span>
                            <span>50%</span>
                        </div>
                        
                        {/* --- LE BOUTON D'ALERTE AUTO (Connecté à n8n) --- */}
                        <div style={{ display: "flex", justifyContent: "space-between", borderBottom: "1px solid #f1f5f9", padding: "15px 0", fontSize: "14px", alignItems: "center" }}>
                            <span>Alertes auto</span>
                            
                            <div 
                                onClick={() => {
                                    const nouvelEtat = !alertesAuto;
                                    setAlertesAuto(nouvelEtat);
                                    
                                    // Le Wow Effect pour la soutenance (Lancement vers n8n)
                                    if (nouvelEtat === true && aRisque.length > 0) {
                                        const etudiantEnDanger = aRisque[0]; 
                                        
                                        axios.post("http://localhost:5678/webhook-test/0391d78a-1e2f-4ff4-ab3e-e2b3cd814eb9", {
                                            etudiant: etudiantEnDanger.nom || etudiantEnDanger.email,
                                            risque: "Critique",
                                            message: "Détection automatique depuis le Dashboard IA !"
                                        }).then(() => {
                                            alert("🚨 Alerte envoyée à n8n avec succès pour " + (etudiantEnDanger.nom || etudiantEnDanger.email) + " !");
                                        }).catch(() => {
                                            alert("⚠️ Le webhook n8n ne répond pas. Avez-vous cliqué sur 'Listen for test event' ?");
                                        });
                                    }
                                }}
                                style={{ 
                                    width: "45px", height: "24px", 
                                    backgroundColor: alertesAuto ? "#10b981" : "#e2e8f0", 
                                    borderRadius: "12px", position: "relative", cursor: "pointer", transition: "background-color 0.3s"
                                }}
                            >
                                <div style={{
                                    width: "20px", height: "20px", backgroundColor: "white", borderRadius: "50%", 
                                    position: "absolute", top: "2px", 
                                    left: alertesAuto ? "23px" : "2px",
                                    transition: "left 0.3s", boxShadow: "0 1px 3px rgba(0,0,0,0.2)"
                                }}></div>
                            </div>
                        </div>
                        
                        <div style={{ display: "flex", justifyContent: "space-between", padding: "15px 0", fontSize: "14px" }}>
                            <span>Source données</span>
                            <span>MySQL</span>
                        </div>
                    </div>

                    {/* Widget 3 : Utilisateurs */}
                    <div className="fst-card">
                        <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "20px" }}>
                            <div style={{ width: "4px", height: "16px", backgroundColor: "var(--fst-orange)" }}></div>
                            <h3 style={{ margin: "0", color: "var(--fst-blue)", fontSize: "16px" }}>Gestion des utilisateurs</h3>
                        </div>
                        
                        {utilisateurs.map((user, index) => {
                            let bgColor = "#e0f2fe"; let textColor = "#0284c7"; 
                            let roleName = user.role ? user.role.toLowerCase() : "inconnu";
                            if (roleName.includes("apprenant") || roleName.includes("etudiant")) { bgColor = "#dcfce7"; textColor = "#16a34a"; } 
                            else if (roleName.includes("admin")) { bgColor = "#ffedd5"; textColor = "#ea580c"; }

                            const initiales = user.nom ? user.nom.split(' ').map(mot => mot[0]).join('').substring(0,2).toUpperCase() : "??";

                            return (
                                <div key={user.id || index} style={{ display: "flex", alignItems: "center", gap: "15px", marginBottom: "15px", borderBottom: index === utilisateurs.length -1 ? "none" : "1px solid #f1f5f9", paddingBottom: "15px" }}>
                                    <div style={{ width: "35px", height: "35px", borderRadius: "50%", backgroundColor: bgColor, color: textColor, display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "bold", fontSize: "12px" }}>
                                        {initiales}
                                    </div>
                                    <div style={{ flex: 1 }}>
                                        <p style={{ margin: "0", fontWeight: "bold", fontSize: "13px" }}>{user.nom}</p>
                                        <p style={{ margin: "0", fontSize: "11px", color: "var(--text-gray)" }}>{user.email}</p>
                                    </div>
                                    <span style={{ backgroundColor: bgColor, color: textColor, padding: "4px 10px", borderRadius: "12px", fontSize: "11px", textTransform: "capitalize" }}>
                                        {user.role}
                                    </span>
                                </div>
                            );
                        })}
                    </div>
                </div>

            </div>
        </div>
    );
}

export default Dashboard;