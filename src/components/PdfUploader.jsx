// src/components/PdfUploader.jsx
import { useState, useRef } from "react";
import api from "../services/api";

export default function PdfUploader({ onUploaded }) {

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleUpload = async (file) => {
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await api.post("/upload/pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      onUploaded(res.data.document_id);

      alert("PDF uploaded successfully!");

    } catch (err) {
      console.error("Upload failed:", err.response?.data || err);
      setError("PDF upload failed. Make sure you are logged in.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="upload-box"
      onClick={() => fileInputRef.current.click()}
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => {
        e.preventDefault();
        handleUpload(e.dataTransfer.files[0]);
      }}
    >
      <input
        type="file"
        accept="application/pdf"
        ref={fileInputRef}
        style={{ display: "none" }}
        onChange={(e) => handleUpload(e.target.files[0])}
      />

      <p>📄 Drag & drop PDF here or <b>click to upload</b></p>

      {loading && <p>Uploading...</p>}
      {error && <p className="error">{error}</p>}
    </div>
  );
}