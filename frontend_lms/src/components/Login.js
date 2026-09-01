import React, { useState } from "react";

function Login({ onLogin }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [erreur, setErreur] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        
        // Exactement 3 comptes stricts, pas un de plus !
        if (email === "admin@fsts.ac.ma" && password !== "") {
            onLogin({ role: "admin", email: email });
        } 
        else if (email === "prof@fsts.ac.ma" && password !== "") {
            onLogin({ role: "enseignant", email: email });
        }
        else if (email.startsWith("etudiant") && email.endsWith("@fsts.ac.ma") && password !== "") {
            onLogin({ role: "etudiant", email: email });
        } 
        else {
            setErreur("Erreur d'identifiants.");
        }
    };

    return (
        <div style={{ display: "flex", justifyContent: "center", paddingTop: "100px", fontFamily: "sans-serif" }}>
            
            {/* Une simple boîte avec une bordure grise et juste un peu de CSS */}
            <form onSubmit={handleSubmit} style={{ width: "350px", textAlign: "center", border: "1px solid #ddd", padding: "30px", borderRadius: "8px" }}>
                
                <h2 style={{ color: "#1e3a8a", marginBottom: "20px" }}>LMS FST</h2>
                
                {erreur && <p style={{ color: "red", fontSize: "14px" }}>{erreur}</p>}

                <input 
                    type="email" 
                    placeholder="Email" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    style={{ width: "100%", padding: "10px", marginBottom: "15px", borderRadius: "4px", border: "1px solid #ccc", boxSizing: "border-box" }}
                />

                <input 
                    type="password" 
                    placeholder="Mot de passe" 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    style={{ width: "100%", padding: "10px", marginBottom: "20px", borderRadius: "4px", border: "1px solid #ccc", boxSizing: "border-box" }}
                />

                <button type="submit" style={{ width: "100%", padding: "10px", backgroundColor: "#1e3a8a", color: "white", border: "none", borderRadius: "4px", cursor: "pointer", fontWeight: "bold" }}>
                    Se connecter
                </button>
                
            </form>
        </div>
    );
}

export default Login;