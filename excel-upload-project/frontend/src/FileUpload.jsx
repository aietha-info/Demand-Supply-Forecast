import React, { useState } from "react";
import axios from "axios";

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    if (!f) return;

    const allowed =
      f.type ===
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ||
      f.type === "application/vnd.ms-excel";

    if (!allowed) {
      setStatus("Only .xls or .xlsx allowed");
      setFile(null);
      return;
    }

    setFile(f);
    setStatus("");
  };

  const uploadFile = async () => {
    if (!file) {
      setStatus("No file selected");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setStatus("Uploading...");

      await axios.post("http://localhost:8000/api/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (evt) => {
          const percent = Math.round((evt.loaded * 100) / evt.total);
          setProgress(percent);
        }
      });

      setStatus("Upload complete");
    } catch {
      setStatus("Upload failed");
    }
  };

  return (
    <div>
      <input type="file" accept=".xls,.xlsx" onChange={handleFileChange} />
      <br /><br />
      <button onClick={uploadFile}>Upload</button>

      {progress > 0 && (
        <div style={{ width: "100%", height: 12, background: "#ddd", marginTop: 15 }}>
          <div
            style={{
              width: `${progress}%`,
              height: "100%",
              background: "#4caf50",
              transition: "width 0.2s"
            }}
          />
        </div>
      )}

      <p>{status}</p>
    </div>
  );
}
