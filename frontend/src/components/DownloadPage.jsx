import React, { useState } from "react";
import ProgressBar from "./ProgressBar";
import { downloadVideo } from "../services/api";

function DownloadPage({ platform, onBack }) {
  const [url, setUrl] = useState("");
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [isDownloading, setIsDownloading] = useState(false);

  const isYouTube = platform === "youtube";

  const handleDownload = async () => {
    if (!url.trim()) {
      setStatus("Please enter a URL.");
      return;
    }

    setIsDownloading(true);
    setProgress(0);
    setStatus("Connecting to server...");

    try {
      const data = await downloadVideo(url.trim(), platform);

      console.log("Download result:", data);

      setProgress(100);
      setStatus("Download completed!");

      setUrl("");
    } catch (error) {
      console.error("Download error:", error);

      setProgress(0);
      setStatus(error.message || "Download failed.");
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <main className="download-page">

      {/* Back Button */}
      <button
        className="back-button"
        onClick={onBack}
        disabled={isDownloading}
      >
        ← Back
      </button>

      {/* Title */}
      <h1 className="download-title">
        {isYouTube
          ? "Download YouTube Video"
          : "Download Instagram Reel"}
      </h1>

      {/* Description */}
      <p className="download-description">
        {isYouTube
          ? "Paste the YouTube video URL below"
          : "Paste an Instagram Reel URL below"}
      </p>

      {/* Download Box */}
      <div className="download-box">

        {/* URL Input */}
        <input
          type="text"
          className="url-input"
          placeholder={
            isYouTube
              ? "Paste YouTube URL..."
              : "Paste Instagram Reel URL..."
          }
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={isDownloading}
        />

        {/* Download Button */}
        <button
          className="download-button"
          onClick={handleDownload}
          disabled={isDownloading}
        >
          {isDownloading ? "Downloading..." : "Download"}
        </button>

      </div>

      {/* Progress */}
      {(isDownloading || progress > 0 || status) && (
        <ProgressBar
          progress={progress}
          status={status}
        />
      )}

    </main>
  );
}

export default DownloadPage;