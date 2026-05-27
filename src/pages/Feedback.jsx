//Feedback.jsx
import { useEffect, useState } from "react";
import api from "../services/api";
import "../styles/feedback.css";

export default function Feedback() {

  const [questions, setQuestions] = useState([]);
  const [submitted, setSubmitted] = useState({});
  const [stats, setStats] = useState({
    avgUsefulness: 0,
    avgRelevance: 0,
    total: 0
  });

  useEffect(() => {

    const saved = JSON.parse(
      localStorage.getItem("generatedQuestions") || "[]"
    );

    setQuestions(saved);

  }, []);

  const submitFeedback = async (q, usefulness, relevance, comments) => {

    try {

      const payload = {
        question_id: q.id || 1,
        usefulness: Number(usefulness),
        relevance: Number(relevance),
        comments: comments || null
      };

      await api.post("/feedback/submit", payload);

      alert("Feedback submitted");

      setSubmitted(prev => ({
        ...prev,
        [q.question]: true
      }));

      updateStats(usefulness, relevance);

    } catch (err) {

      console.error(err);
      alert("Failed to submit feedback");

    }

  };

  const updateStats = (u, r) => {

    setStats(prev => {

      const total = prev.total + 1;

      return {
        avgUsefulness:
          ((prev.avgUsefulness * prev.total) + u) / total,
        avgRelevance:
          ((prev.avgRelevance * prev.total) + r) / total,
        total
      };

    });

  };

  if (!questions.length) {
    return (
      <div className="page-wrapper">
        <h2>No feedback available</h2>
      </div>
    );
  }

  return (
    <div className="page-wrapper">

      <h2>Question Feedback</h2>

      {/* Feedback Analytics */}
      <div className="feedback-summary">

        <div className="summary-card">
          ⭐ Average Usefulness
          <h3>{stats.avgUsefulness.toFixed(2)}</h3>
        </div>

        <div className="summary-card">
          ⭐ Average Relevance
          <h3>{stats.avgRelevance.toFixed(2)}</h3>
        </div>

        <div className="summary-card">
          📝 Total Feedback
          <h3>{stats.total}</h3>
        </div>

      </div>

      {questions.map((q, i) => (

        <FeedbackCard
          key={i}
          question={q}
          index={i}
          submitFeedback={submitFeedback}
          submitted={submitted[q.question]}
        />

      ))}

    </div>
  );
}

function FeedbackCard({
  question,
  index,
  submitFeedback,
  submitted
}) {

  const [usefulness, setUsefulness] = useState(3);
  const [relevance, setRelevance] = useState(3);
  const [comments, setComments] = useState("");

  const StarRating = ({ value, onChange }) => {

    return (
      <div className="star-rating">
        {[1,2,3,4,5].map(star => (
          <span
            key={star}
            className={`star ${star <= value ? "filled" : ""}`}
            onClick={() => onChange(star)}
          >
            ★
          </span>
        ))}
      </div>
    );

  };

  const isLowQuality = usefulness <= 2 || relevance <= 2;

  return (

    <div className={`feedback-card ${isLowQuality ? "low-quality" : ""}`}>

      <strong>
        {index + 1}. {question.question}
      </strong>

      <p>Type: {question.type}</p>
      <p>Bloom Level: {question.bloom_level}</p>
      <p>Difficulty: {question.difficulty}</p>

      {isLowQuality && (
        <p className="warning">⚠ Low Quality Question</p>
      )}

      <label>Rate Usefulness</label>
      <StarRating value={usefulness} onChange={setUsefulness} />

      <label>Rate Relevance</label>
      <StarRating value={relevance} onChange={setRelevance} />

      <label>Comments</label>
      <textarea
        value={comments}
        onChange={(e)=>setComments(e.target.value)}
      />

      <button
        disabled={submitted}
        onClick={()=>submitFeedback(
          question,
          usefulness,
          relevance,
          comments
        )}
      >
        {submitted ? "Submitted ✓" : "Submit Feedback"}
      </button>

    </div>

  );

}