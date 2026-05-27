//UploadContent.jsx
import { useEffect, useState } from "react";
import PdfUploader from "../components/PdfUploader";
import TextInputBox from "../components/TextInputBox";
import InputModeSelector from "../components/InputModeSelector";
import "../styles/upload.css";

export default function UploadContent() {

  const [mode, setMode] = useState("pdf");
  const [text, setText] = useState("");
  const [documentId, setDocumentId] = useState(null);

  // Handle mode switching
  useEffect(() => {

    localStorage.removeItem("contextText");
    localStorage.removeItem("documentId");

    if (mode === "pdf") {
      localStorage.setItem("sourceType", "pdf");
    } else {
      localStorage.setItem("sourceType", "text");
    }

  }, [mode]);

  // Store text
  useEffect(() => {

    if (mode === "text" && text.trim().length > 0) {

      localStorage.setItem("sourceType", "text");
      localStorage.setItem("contextText", text);

    }

  }, [text, mode]);

  // Store uploaded pdf id
  useEffect(() => {

    if (mode === "pdf" && documentId) {

      localStorage.setItem("sourceType", "pdf");
      localStorage.setItem("documentId", documentId.toString());

    }

  }, [documentId, mode]);

  return (

    <div className="upload-page">

      <div className="upload-header">
        <h2>Upload Content</h2>
        <p>Provide content to generate intelligent questions</p>
      </div>

      {/* Mode Selector */}
      <InputModeSelector mode={mode} setMode={setMode} />

      <div className="upload-card">

        {mode === "pdf" ? (
          <PdfUploader onUploaded={setDocumentId} />
        ) : (
          <TextInputBox text={text} setText={setText} />
        )}

      </div>

      {documentId && mode === "pdf" && (
        <div className="status success">
          🎉 PDF uploaded successfully (ID: {documentId})
        </div>
      )}

      {mode === "text" && text.length > 0 && (
        <div className="status hint">
          ✍️ Text ready for question generation
        </div>
      )}

    </div>

  );

}