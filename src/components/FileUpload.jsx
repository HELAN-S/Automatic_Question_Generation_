import { useState } from "react";
import axios from "axios";

export default function FileUpload({ onUploadSuccess }) {
  const [dragActive, setDragActive] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleFile = async (file) => {
    if (!file || file.type !== "application/pdf") {
      alert("Please upload a PDF file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const res = await axios.post(
        "http://127.0.0.1:8000/upload/pdf",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      onUploadSuccess(res.data.document_id);
    } catch (err) {
      alert("PDF upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className={`upload-box ${dragActive ? "active" : ""}`}
      onDragOver={(e) => {
        e.preventDefault();
        setDragActive(true);
      }}
      onDragLeave={() => setDragActive(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDragActive(false);
        handleFile(e.dataTransfer.files[0]);
      }}
    >
      <input
        type="file"
        accept="application/pdf"
        hidden
        id="pdfUpload"
        onChange={(e) => handleFile(e.target.files[0])}
      />

      <label htmlFor="pdfUpload">
        {loading ? (
          <p>Uploading PDF...</p>
        ) : (
          <>
            <strong>Drag & Drop PDF here</strong>
            <p>or click to upload</p>
          </>
        )}
      </label>
    </div>
  );
}