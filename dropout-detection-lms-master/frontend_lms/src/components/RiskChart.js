import React from "react";
import {
  BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts";

function RiskChart({ apprenants }) {
  const aRisque = apprenants.filter(a => a.niveau_risque >= 0.5).length;
  const ok = apprenants.filter(a => a.niveau_risque < 0.5).length;

  const data = [
    { name: "À risque", nombre: aRisque, fill: "#e74c3c" },
    { name: "Non à risque",       nombre: ok,      fill: "#2ecc71" }
  ];

  return (
    <div style={{ width: "100%", height: 300 }}>
      <h3 style={{ textAlign: "center", color: "#333" }}>
        Répartition des apprenants
      </h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="nombre" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RiskChart;