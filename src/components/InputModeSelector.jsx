//src/components/InputModeSelector.jsx
export default function InputModeSelector({ mode, setMode }) {

  return (

    <div className="source-toggle">

      <button
        className={mode === "pdf" ? "active" : ""}
        onClick={() => setMode("pdf")}
      >
        Upload PDF
      </button>

      <button
        className={mode === "text" ? "active" : ""}
        onClick={() => setMode("text")}
      >
        Paste Text
      </button>

    </div>

  );

}