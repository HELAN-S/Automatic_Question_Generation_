// Dashboard.jsx

import { useEffect, useState } from "react";
import api from "../services/api";
import "../styles/dashboard.css";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

import { Pie } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function Dashboard() {

  const [darkMode, setDarkMode] = useState(false);

  // ✅ FIXED STATE (added averageQuality)
  const [stats, setStats] = useState({
    totalPdfs: 0,
    totalQuestions: 0,
    averageQuality: 0,
    bloom: {},
    difficulty: {},
    types: {}
  });

  useEffect(() => {

    async function loadDashboard() {

      try {

        const res = await api.get("/dashboard/stats");

        // ✅ FIXED LOADER
        setStats({
          totalPdfs: res.data.total_pdfs || 0,
          totalQuestions: res.data.total_questions || 0,
          averageQuality: res.data.average_quality_score || 0,
          bloom: res.data.bloom_distribution || {},
          difficulty: res.data.difficulty_distribution || {},
          types: res.data.type_distribution || {}
        });

      } catch (err) {
        console.error("Dashboard error:", err);
      }
    }

    loadDashboard();

  }, []);

  const createChartData = (obj) => ({
    labels: Object.keys(obj),
    datasets: [
      {
        data: Object.values(obj),
        backgroundColor: [
          "#4F46E5",
          "#06B6D4",
          "#10B981",
          "#F59E0B",
          "#EF4444",
          "#8B5CF6"
        ],
        borderWidth: 0,
      },
    ],
  });

  return (
    <div className={`dashboard ${darkMode ? "dark" : ""}`}>

      {/* Header */}
      <div className="dashboard-header">

        <h1 className="dashboard-title">Dashboard</h1>

        

      </div>

      {/* Stats */}
      <div className="stats-grid">

        <StatCard
          title="📄 PDFs Uploaded"
          value={stats.totalPdfs}
        />

        <StatCard
          title="❓ Questions Generated"
          value={stats.totalQuestions}
        />

        

      </div>

      {/* Charts */}
      <div className="chart-grid">

        <div className="chart-card">
          <h3>Bloom Taxonomy Distribution</h3>
          {Object.keys(stats.bloom).length > 0 && (
            <Pie data={createChartData(stats.bloom)} />
          )}
        </div>

        <div className="chart-card">
          <h3>Difficulty Distribution</h3>
          {Object.keys(stats.difficulty).length > 0 && (
            <Pie data={createChartData(stats.difficulty)} />
          )}
        </div>

        <div className="chart-card">
          <h3>Question Type Distribution</h3>
          {Object.keys(stats.types).length > 0 && (
            <Pie data={createChartData(stats.types)} />
          )}
        </div>

      </div>

    </div>
  );
}


// ✅ Reusable Stat Card
function StatCard({ title, value }) {

  return (

    <div className="stat-card">
      <h4>{title}</h4>
      <h2>{value}</h2>
    </div>

  );

}