import React, { useState } from "react";

function Login({ onLogin }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [erreur, setErreur] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        
        // Logique de vérification très simple pour la démo
        if (email === "admin@fsts.ac.ma" && password !== "") {
            onLogin({ role: "admin", email: email });
        } 
        else if (email.includes("@fsts.ac.ma") && password !== "") {
            // N'importe quelle autre adresse académique est considérée comme un étudiant
            onLogin({ role: "etudiant", email: email });
        } 
        else {
            setErreur("Email ou mot de passe incorrect.");
        }
    };

    return (
        <div style={{
            display: "flex", justifyContent: "center", alignItems: "center",
            height: "100vh", backgroundColor: "#f1f5f9"
        }}>
            <form onSubmit={handleSubmit} style={{
                backgroundColor: "white", padding: "40px", borderRadius: "10px",
                boxShadow: "0 4px 6px rgba(0,0,0,0.1)", textAlign: "center", width: "400px"
            }}>
                <div style={{ 
                    backgroundColor: "var(--fst-orange, #f97316)", width: "80px", height: "80px", 
                    borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center",
                    fontWeight: "bold", fontSize: "28px", margin: "0 auto 20px", color: "white"
                }}>
                    FST
                </div>
                
                <h1 style={{ color: "var(--fst-blue, #1e3a8a)", fontSize: "24px", marginBottom: "30px" }}>
                    Connexion LMS
                </h1>

                {erreur && <p style={{ color: "red", fontSize: "14px", marginBottom: "15px" }}>{erreur}</p>}

                <input 
                    type="email" 
                    placeholder="Adresse email (ex: admin@fsts.ac.ma)" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    style={{
                        width: "100%", padding: "12px", marginBottom: "15px",
                        border: "1px solid #ccc", borderRadius: "5px", boxSizing: "border-box"
                    }}
                />

                <input 
                    type="password" 
                    placeholder="Mot de passe" 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    style={{
                        width: "100%", padding: "12px", marginBottom: "25px",
                        border: "1px solid #ccc", borderRadius: "5px", boxSizing: "border-box"
                    }}
                />

                <button 
                    type="submit"
                    style={{
                        width: "100%", backgroundColor: "var(--fst-blue, #1e3a8a)",
                        color: "white", border: "none", padding: "12px", borderRadius: "6px",
                        fontSize: "16px", cursor: "pointer", fontWeight: "bold"
                    }}
                >
                    Se connecter
                </button>
            </form>
        </div>
    );
}

export default Login;
