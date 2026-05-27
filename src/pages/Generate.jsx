// src/pages/Generate.jsx
import { useEffect, useRef, useState } from "react";
import api from "../services/api";
import { exportQuestionsToPDF } from "../utils/exportPdf";
import "../styles/generate.css";

const QUESTION_TYPES = ["MCQ", "Fill in the Blanks", "True/False", "Short Answer"];
const BLOOM_LEVELS = ["Remember","Understand","Apply","Analyze","Evaluate","Create"];
const DIFFICULTY_LEVELS = ["Easy","Medium","Hard"];

const TYPE_MAPPING = {
  "MCQ": "mcq",
  "Fill in the Blanks": "fib",
  "True/False": "true_false",
  "Short Answer": "short_answer"
};

const TYPE_LABELS = {
  mcq: "MCQ",
  fib: "Fill in the Blanks",
  true_false: "True/False",
  short_answer: "Short Answer"
};

// ✅ CLEAN TEXT FUNCTION (REMOVES **)
const cleanText = (text) => {
  if (!text) return "";
  return text.replace(/\*\*/g, "").trim();
};

export default function Generate() {
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [numQuestions, setNumQuestions] = useState(5);
  const [questionTypes, setQuestionTypes] = useState(["MCQ"]);
  const [selectedBlooms, setSelectedBlooms] = useState([]);
  const [selectedDifficulties, setSelectedDifficulties] = useState([]);
  const [bloomDistribution, setBloomDistribution] = useState({});

  const pollingRef = useRef(null);

  useEffect(() => {
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, []);

  const toggleItem = (item, list, setList) => {
    setList(prev =>
      prev.includes(item)
        ? prev.filter(x => x !== item)
        : [...prev, item]
    );
  };

  const handleDistributionChange = (level, value) => {
    setBloomDistribution(prev => ({
      ...prev,
      [level]: Number(value)
    }));
  };

  const startPolling = (jobId) => {
    pollingRef.current = setInterval(async () => {
      try {
        const res = await api.get(`/generate/status/${jobId}`);
        const data = res.data;

        if (data.status === "completed") {
          const qs = data.result?.questions || [];
          setQuestions(qs);
          localStorage.setItem("generatedQuestions", JSON.stringify(qs));
          setLoading(false);
          clearInterval(pollingRef.current);
        }

        if (data.status === "failed") {
          alert(data.error || "Generation failed");
          setLoading(false);
          clearInterval(pollingRef.current);
        }

      } catch (err) {
        console.error("Polling error:", err.response?.data || err);
        setLoading(false);
        clearInterval(pollingRef.current);
      }
    }, 2000);
  };

  const handleGenerate = async () => {
    const sourceType = localStorage.getItem("sourceType");

    if (!sourceType) {
      alert("Please upload text or PDF first");
      return;
    }

    if (!questionTypes.length) {
      alert("Select at least one question type");
      return;
    }

    setLoading(true);
    setQuestions([]);
    localStorage.removeItem("generatedQuestions");

    const mappedTypes = questionTypes.map(qt => TYPE_MAPPING[qt]);

    const filteredDistribution = Object.fromEntries(
      Object.entries(bloomDistribution).filter(([k, v]) =>
        selectedBlooms.length === 0 || selectedBlooms.includes(k)
      )
    );

    const payload = {
      source_type: sourceType,
      num_questions: Number(numQuestions),
      question_types: mappedTypes,
      target_bloom_levels: selectedBlooms.length ? selectedBlooms : BLOOM_LEVELS,
      target_difficulty_levels: selectedDifficulties.length ? selectedDifficulties : DIFFICULTY_LEVELS,
      bloom_distribution: filteredDistribution,
      user_id: localStorage.getItem("userId") || 1
    };

    if (sourceType === "text") {
      const text = localStorage.getItem("contextText") || "";

      if (!text.trim()) {
        alert("No text found. Please upload again.");
        setLoading(false);
        return;
      }

      payload.text = text;
      localStorage.setItem("sourceContext", text);
    }

    if (sourceType === "pdf") {
      const docId = localStorage.getItem("documentId");

      if (!docId) {
        alert("No PDF uploaded. Please upload PDF first.");
        setLoading(false);
        return;
      }

      payload.document_id = docId;
      localStorage.setItem("sourceContext", docId);
    }

    try {
      const res = await api.post("/generate", payload);
      startPolling(res.data.job_id);
    } catch (err) {
      console.error("Generation error:", err.response?.data || err);
      alert("Failed to start generation.");
      setLoading(false);
    }
  };

  return (
    <div className="page-wrapper">
      <div className="content-wrapper">

        {/* LEFT PANEL */}
        <div className="left-panel">
          <div className="card">
            <h1>Question Generator</h1>

            <label>Total Questions</label>
            <input
              type="number"
              min={1}
              max={100}
              value={numQuestions}
              onChange={(e)=>setNumQuestions(Number(e.target.value))}
            />

            <h4>Question Types</h4>
            <div className="type-grid">
              {QUESTION_TYPES.map(type => (
                <button
                  key={type}
                  className={questionTypes.includes(type) ? "active" : ""}
                  onClick={() => toggleItem(type, questionTypes, setQuestionTypes)}
                >
                  {type}
                </button>
              ))}
            </div>

            <h4>Target Bloom Levels</h4>
            <div className="type-grid">
              {BLOOM_LEVELS.map(level => (
                <button
                  key={level}
                  className={selectedBlooms.includes(level) ? "active" : ""}
                  onClick={() => toggleItem(level, selectedBlooms, setSelectedBlooms)}
                >
                  {level}
                </button>
              ))}
            </div>

            <h4>Bloom Distribution (Optional)</h4>
            {BLOOM_LEVELS.map(level => (
              <div key={level} className="distribution-input">
                <label>{level}</label>
                <input
                  type="number"
                  min={0}
                  placeholder="0"
                  value={bloomDistribution[level] || ""}
                  onChange={(e)=>handleDistributionChange(level, e.target.value)}
                />
              </div>
            ))}

            <h4>Target Difficulty</h4>
            <div className="type-grid">
              {DIFFICULTY_LEVELS.map(level => (
                <button
                  key={level}
                  className={selectedDifficulties.includes(level) ? "active" : ""}
                  onClick={() => toggleItem(level, selectedDifficulties, setSelectedDifficulties)}
                >
                  {level}
                </button>
              ))}
            </div>

            <button
              className="generate-btn"
              onClick={handleGenerate}
              disabled={loading}
            >
              {loading ? "Generating..." : "Generate Questions"}
            </button>
          </div>
        </div>

        {/* RIGHT PANEL */}
        <div className="right-panel">
          <div className="card">
            <h1>Generated Questions</h1>

            {questions.length > 0 && (
              <div className="pdf-export-options">
                <button className="export-btn" onClick={() => exportQuestionsToPDF(questions, false)}>
                  Download Questions Only
                </button>
                <button className="export-btn" onClick={() => exportQuestionsToPDF(questions, true)}>
                  Download with Answers
                </button>
              </div>
            )}

            {loading && <p>Generating questions...</p>}
            {!loading && questions.length === 0 && (
              <p style={{color:"white"}}>Generated questions will appear here.</p>
            )}

            {questions.map((q, i) => (
              <div key={i} className="question-card">
                <strong>{i + 1}. {cleanText(q.question)}</strong>

                <div>
                  <span className="tag">{TYPE_LABELS[q.type] || q.type}</span>
                  <span className="tag">{q.difficulty}</span>
                  <span className="tag">{q.bloom_level}</span>
                </div>

                {q.options && (
                  <ul>
                    {q.options.map((opt, idx) => (
                      <li key={idx}>{cleanText(opt)}</li>
                    ))}
                  </ul>
                )}

                {q.answer && (
                  <div className="answer">
                    <strong>Answer:</strong> {cleanText(q.answer)}
                  </div>
                )}
              </div>
            ))}

          </div>
        </div>

      </div>
    </div>
  );
}