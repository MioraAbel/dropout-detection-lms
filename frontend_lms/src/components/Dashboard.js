import React, { useState, useEffect } from "react";
import axios from "axios";
import RiskChart from "./RiskChart";

// 1. NOTRE "MOULE" POUR LES CARTES KPI (Composant réutilisable)
const MaCarteKPI = ({ titre, valeur, couleur }) => (
    // flex-fill permet à la carte de s'étirer équitablement
    <div className={`card p-3 shadow-sm border-start border-${couleur} border-4 flex-fill mx-2 text-center`}>
        <p className="text-muted mb-1">{titre}</p>
        <h2 className={`text-${couleur}`}>{valeur}</h2>
    </div>
);
// 2. NOTRE "MOULE" POUR LES LIGNES DE STATISTIQUES
const LigneStat = ({ label, valeur, color = "" }) => (
    <li className="list-group-item d-flex justify-content-between">
        {label} <b className={color}>{valeur}</b>
    </li>
);

function Dashboard() {
    const [apprenants, setApprenants]       = useState([]);
    const [stats, setStats]                 = useState(null);
    const [loading, setLoading]             = useState(true);
    const [erreur, setErreur]               = useState(null);
    const [alertesAuto, setAlertesAuto]     = useState(false);
    const [activeSection, setActiveSection] = useState("statistiques");

    useEffect(() => {
        axios.all([
            axios.get("http://127.0.0.1:5000/api/apprenants/"),
            axios.get("http://127.0.0.1:5000/api/statistiques")
        ])
        .then(axios.spread((resApprenants, resStats) => {
            setApprenants(resApprenants.data);
            setStats(resStats.data);
            setLoading(false);
        }))
        .catch(() => {
            setErreur("Impossible de contacter le serveur Flask.");
            setLoading(false);
        });
    }, []);

    if (loading) return <p style={{ textAlign: "center", marginTop: "100px" }}>Chargement...</p>;
    if (erreur)  return <p style={{ color: "red", textAlign: "center", marginTop: "100px" }}>{erreur}</p>;

    const aRisque    = apprenants.filter(a => a.niveau_risque === "élevé");
    const nonARisque = apprenants.length - aRisque.length;

    const activerAlerte = () => {
    setAlertesAuto(!alertesAuto);
    if (alertesAuto === false && aRisque.length > 0) {
        
        // on prépare un tableau avec les vraies données
        const listeAlerte = aRisque.map(etudiant => ({
            etudiant: etudiant.nom || etudiant.email,
            niveau_risque: etudiant.niveau_risque, 
            message: `Attention : L'étudiant a un risque évalué à ${etudiant.niveau_risque}.`
        }));
        // On envoie la liste d'apprenant à n8n 
        axios.post("http://localhost:5678/webhook/1a67a5ab-d186-4fd5-9e5c-b95900e56a54", {
            alertes: listeAlerte,
            total_concernes: aRisque.length
        })
        .then(() => alert(`Le fichier contenant les ${aRisque.length} étudiants à risque a été transmis à n8n.`))
        .catch(() => alert("Erreur de connexion à n8n."));
    };
    };
return (
        <div className="container-fluid py-4 bg-light min-vh-100">
            {/* EN-TÊTE TRÈS SIMPLE */}
            <div className="mb-4">
                <h3 className="text-primary">LMS Analytics - FSTS</h3>
                <h2>Tableau de bord Administrateur</h2>
                <hr />
            </div>
               {/* LES 3 CARTES (Utilisation du composant réutilisable et de d-flex) */}
            <div className="d-flex justify-content-between mb-5">
                <MaCarteKPI titre="Total Apprenants" valeur={apprenants.length} couleur="primary" />
                <MaCarteKPI titre="Taux Décrochage"  valeur={stats ? stats.taux_decrochage + "%" : "0%"} couleur="danger" />
                <MaCarteKPI titre="Alertes Générées" valeur={stats ? stats.alertes_generees : 0} couleur="warning" />
            </div>
                        {/* LIGNE CENTRALE : GRAPHIQUE ET DÉTAILS */}
            <div className="d-flex justify-content-between gap-4 mb-5">
                
                {/* GRAPHIQUE */}
                <div className="card p-4 shadow-sm w-50">
                    <h4 className="mb-3">Répartition</h4>
                    <RiskChart apprenants={apprenants} />
                </div>

                {/* STATS GLOBALES */}
                <div className="card p-4 shadow-sm w-50">
                    <h4 className="mb-3">Détails Globaux</h4>
                    <ul className="list-group">
                        <LigneStat label="Total apprenants"   valeur={apprenants.length} />
                        <LigneStat label="À risque"           valeur={aRisque.length} color="text-danger" />
                        <LigneStat label="Non à risque"       valeur={nonARisque} color="text-success" />
                        <LigneStat label="Taux de décrochage" valeur={`${stats ? stats.taux_decrochage : 0}%`} color="text-danger" />
                        <LigneStat label="Alertes envoyées"   valeur={stats ? stats.alertes_generees : 0} />
                    </ul>
                </div>
            </div>
            {/* WORKFLOW N8N EN BAS */}
            <div className="card p-4 shadow-sm text-center">
                <h4 className="mb-3">Automatisation des alertes (n8n)</h4>
                <p className="text-muted mb-4">
                    Ce bouton permet de transmettre immédiatement la liste des étudiants en difficulté vers le flux d'envoi d'emails.
                </p>
                
                <button 
                    className={`btn btn-lg w-25 mx-auto mb-3 ${alertesAuto ? "btn-success" : "btn-secondary"}`} 
                    onClick={activerAlerte}
                >
                    {alertesAuto ? "Désactiver" : "Activer les alertes"}
                </button>
                <p className="fw-bold m-0">
                    État du système : {alertesAuto ? <span className="text-success">EN ÉCOUTE</span> : <span className="text-muted">PAUSE</span>}
                </p>
            </div>
        </div>
    );
}
export default Dashboard;
    