import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import DashboardTeacher from './components/Dashboard_teacher';
import ProfilUtilisateur from './components/ProfilUtilisateur';
import Login from './components/Login';
import './App.css';

function App() {
  // Gère l'état de l'utilisateur connecté (ex: { role: "etudiant", email: "etudiant5@fsts.ac.ma" })
  const [user, setUser] = useState(null); 

  return (
    <div className="App">
      {/* 1. Si aucun utilisateur n'est connecté, on affiche le Login */}
      {!user && <Login onLogin={setUser} />}

      {/* 2. Si c'est l'Admin, on affiche le Dashboard */}
      {user && user.role === "admin" && (
          <div>
              <div style={{ padding: "10px", backgroundColor: "#fff", borderBottom: "1px solid #ccc", textAlign: "right" }}>
                  <span style={{ marginRight: "20px", fontWeight: "bold" }}>Connecté en tant que: {user.email}</span>
                  <button onClick={() => setUser(null)} style={{ padding: "8px 15px", cursor: "pointer", backgroundColor: "#ef4444", color: "white", border: "none", borderRadius: "5px" }}>
                      Se déconnecter
                  </button>
              </div>
              <Dashboard />
          </div>
      )}

      {/* Si c'est l'Enseignant, on affiche le DashboardTeacher */}
      {user && user.role === "enseignant" && (
          <div>
              <div style={{ padding: "10px", backgroundColor: "#fff", borderBottom: "1px solid #ccc", textAlign: "right" }}>
                  <span style={{ marginRight: "20px", fontWeight: "bold" }}>Connecté en tant que: {user.email}</span>
                  <button onClick={() => setUser(null)} style={{ padding: "8px 15px", cursor: "pointer", backgroundColor: "#ef4444", color: "white", border: "none", borderRadius: "5px" }}>
                      Se déconnecter
                  </button>
              </div>
              <DashboardTeacher />
          </div>
      )}

      {/* 3. Si c'est un Étudiant, on affiche son Profil spécifique */}
      {user && user.role === "etudiant" && (
          <div style={{ padding: "50px", backgroundColor: "#f1f5f9", minHeight: "100vh" }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "20px" }}>
                  <h1 style={{ margin: 0, color: "#1e293b" }}>Espace Étudiant</h1>
                  <button onClick={() => setUser(null)} style={{ padding: "10px 20px", cursor: "pointer", backgroundColor: "#ef4444", color: "white", border: "none", borderRadius: "5px" }}>
                      Se déconnecter
                  </button>
              </div>
              
              {/* On passe l'email de l'étudiant connecté au composant pour qu'il cherche ses propres données */}
              <ProfilUtilisateur emailConnecte={user.email} />
          </div>
      )}
    </div>
  );
}

export default App;
