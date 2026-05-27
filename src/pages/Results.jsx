import { useLocation } from "react-router-dom";
import { useState } from "react";
import QuestionCard from "../components/QuestionCard";
import AnalyticsDashboard from "../components/AnalyticsDashboard";

function Results() {
  const location = useLocation();
  const data = location.state;
  const [activeTab, setActiveTab] = useState("ALL");

  if (!data || !data.questions) {
    return <h2>No data found</h2>;
  }

  const grouped = {
    ALL: data.questions,
    MCQ: data.questions.filter(q => q.question_type === "MCQ"),
    FIB: data.questions.filter(q => q.question_type === "FIB"),
    "True/False": data.questions.filter(q => q.question_type === "True/False"),
    "Short Answer": data.questions.filter(q => q.question_type === "Short Answer"),
  };

  return (
    <div className="container">
      <h1>Generated Questions</h1>

      {/* Tabs */}
      <div className="tabs">
        {Object.keys(grouped).map(type => (
          <button
            key={type}
            className={activeTab === type ? "active-tab" : ""}
            onClick={() => setActiveTab(type)}
          >
            {type}
          </button>
        ))}
      </div>

      {/* Questions */}
      {grouped[activeTab].length === 0 && (
        <p>No questions of this type.</p>
      )}

      {grouped[activeTab].map((q, i) => (
        <QuestionCard key={i} question={q} />
      ))}

      <AnalyticsDashboard analytics={data.evaluation_summary} />
    </div>
  );
}

export default Results;
