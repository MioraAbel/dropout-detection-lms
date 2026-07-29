import React from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";

function RiskChart({ apprenants }) {
  const aRisque = apprenants.filter(a => a.niveau_risque === "élevé" || a.niveau_risque === "modéré").length;
  const ok = apprenants.filter(a => a.niveau_risque === "faible").length;

  const data = [
    { name: "À risque", value: aRisque, color: "#e74c3c" },
    { name: "Non à risque", value: ok, color: "#2ecc71" }
  ];

  return (
    <div style={{ width: "100%", height: 220 }}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={0}
            outerRadius={80}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip />
          <Legend layout="vertical" verticalAlign="middle" align="right" />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RiskChart;