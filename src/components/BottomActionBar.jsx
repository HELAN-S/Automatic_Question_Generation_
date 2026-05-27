import { downloadQuestionsAsPDF } from "../utils/pdfGenerator";

export default function BottomActionBar({ questions, onRegenerate }) {
  return (
    <div className="bottom-bar">
      <button
        className="btn-teal"
        onClick={() => downloadQuestionsAsPDF(questions)}
        disabled={!questions.length}
      >
        Download PDF
      </button>

      <button className="btn-outline" onClick={onRegenerate}>
        Regenerate
      </button>

      <button className="btn-outline">
        Save
      </button>
    </div>
  );
}