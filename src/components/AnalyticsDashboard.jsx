//AnalyticsDashboard.jsx
import {
  PieChart, Pie, Cell, Tooltip,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from "recharts";

function AnalyticsDashboard({ analytics }) {
  if (!analytics) return null;

  const bloomData = Object.entries(
    analytics.bloom_distribution || {}
  ).map(([key, value]) => ({
    name: key,
    value
  }));

  const difficultyData = Object.entries(
    analytics.difficulty_distribution || {}
  ).map(([key, value]) => ({
    name: key,
    value
  }));

  const COLORS = ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed", "#111827"];

  return (
    <div className="analytics">
      <h2>Analytics</h2>

      <div className="chart-row">
        <div>
          <h3>Bloom Distribution</h3>
          <PieChart width={300} height={300}>
            <Pie
              data={bloomData}
              dataKey="value"
              outerRadius={100}
              label
            >
              {bloomData.map((_, index) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </div>

        <div>
          <h3>Difficulty Distribution</h3>
          <BarChart width={300} height={300} data={difficultyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#2563eb" />
          </BarChart>
        </div>
      </div>
    </div>
  );
}

export default AnalyticsDashboard;
