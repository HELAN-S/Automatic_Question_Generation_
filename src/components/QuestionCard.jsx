export default function QuestionCard({ question }) {
  return (
    <div className="question-card">
      <p>{question.text}</p>

      {question.options && (
        <ul>
          {question.options.map((opt, i) => (
            <li key={i}>{opt}</li>
          ))}
        </ul>
      )}

      <div className="tags">
        <span className="tag">{question.bloom}</span>
        <span className="tag">{question.difficulty}</span>
      </div>
    </div>
  );
}