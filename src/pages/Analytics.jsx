// src/pages/Analytics.jsx

import { useEffect, useState } from "react";
import api from "../services/api";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

import "../styles/analytics.css";

const COLORS = [
  "#6366f1",
  "#10b981",
  "#f59e0b",
  "#ef4444",
  "#8b5cf6",
  "#ec4899"
];

export default function Analytics() {

  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    // ✅ Get stored questions
    const questions = JSON.parse(
      localStorage.getItem("generatedQuestions") || "[]"
    );

    // ✅ Get stored context
    const context = localStorage.getItem(
      "sourceContext"
    );

    // 🔥 SAFETY CHECK (VERY IMPORTANT)
    if (!questions.length || !context) {

      console.warn(
        "Missing questions or context"
      );

      setLoading(false);
      return;
    }

    // ✅ Send analytics request
    api.post("/analytics/summary", {
      questions: questions,
      context: context
    })
      .then(res => {

        console.log(
          "Analytics response:",
          res.data
        );

        setSummary(res.data);
      })
      .catch(err => {

        console.error(
          "Analytics error:",
          err.response?.data || err
        );

        setSummary(null);
      })
      .finally(() => {

        setLoading(false);
      });

  }, []);

  // 🔄 Loading State

  if (loading) {

    return (

      <div className="analytics-wrapper">

        <h2 className="no-data">
          Loading analytics...
        </h2>

      </div>

    );
  }

  // ❌ No Data

  if (!summary) {

    return (

      <div className="analytics-wrapper">

        <h2 className="no-data">
          No analytics data available
        </h2>

      </div>

    );
  }

  // ✅ Safe Data Mapping

  const bloomData = Object.entries(
    summary.bloom_distribution || {}
  ).map(([name, value]) => ({
    name,
    value
  }));

  const difficultyData = Object.entries(
    summary.difficulty_distribution || {}
  ).map(([name, value]) => ({
    name,
    value
  }));

  const typeData = Object.entries(
    summary.question_type_distribution || {}
  ).map(([name, value]) => ({
    name,
    value
  }));

  return (

    <div className="analytics-wrapper">

      <h1 className="analytics-title">
        Analytics Dashboard
      </h1>

      {/* TOTAL QUESTIONS */}

      <div className="total-box">

        <p>
          Total Questions Generated
        </p>

        <h2>
          {summary.total_questions || 0}
        </h2>

      </div>

      {/* CHART GRID */}

      <div className="chart-grid">

        {/* BLOOM DISTRIBUTION */}

        <div className="chart-card">

          <h3>
            Bloom Distribution
          </h3>

          <ResponsiveContainer
            width="100%"
            height={300}
          >

            <PieChart>

              <Pie
                data={bloomData}
                dataKey="value"
                nameKey="name"
                outerRadius={100}
              >

                {bloomData.map(
                  (entry, index) => (

                    <Cell
                      key={index}
                      fill={
                        COLORS[
                          index % COLORS.length
                        ]
                      }
                    />

                  )
                )}

              </Pie>

              <Tooltip />

            </PieChart>

          </ResponsiveContainer>

        </div>

        {/* DIFFICULTY */}

        <div className="chart-card">

          <h3>
            Difficulty Distribution
          </h3>

          <ResponsiveContainer
            width="100%"
            height={300}
          >

            <BarChart
              data={difficultyData}
            >

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis dataKey="name" />

              <YAxis />

              <Tooltip />

              <Bar
                dataKey="value"
                fill="#6366f1"
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

        {/* QUESTION TYPE */}

        <div className="chart-card">

          <h3>
            Question Types
          </h3>

          <ResponsiveContainer
            width="100%"
            height={300}
          >

            <BarChart
              data={typeData}
            >

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis dataKey="name" />

              <YAxis />

              <Tooltip />

              <Bar
                dataKey="value"
                fill="#10b981"
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>

      {/* FINAL SCORE */}

      <div className="score-box">

        <span>
          Final Quality Score
        </span>

        <h2>
          {summary.final_quality_score || 0}
        </h2>

      </div>
    </div>

  );
}