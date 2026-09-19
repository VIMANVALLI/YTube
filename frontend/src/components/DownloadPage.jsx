import React, { useState } from "react";
import ProgressBar from "./ProgressBar";
import {
  downloadVideo,
  getDownloadFileUrl,
} from "../services/api";

function DownloadPage({ platform, onBack }) {
  const [url, setUrl] = useState("");
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [isDownloading, setIsDownloading] = useState(false);

  const isYouTube = platform === "youtube";

  const handleDownload = async () => {
    // =========================================
    // VALIDATE URL
    // =========================================

    if (!url.trim()) {
      setStatus("Please enter a URL.");
      return;
    }

    setIsDownloading(true);
    setProgress(0);
    setStatus("Connecting to server...");

    try {
      // =========================================
      // DOWNLOAD VIDEO ON SERVER
      // =========================================

      const data = await downloadVideo(
        url.trim(),
        platform
      );

      console.log(
        "Download result:",
        data
      );

      // =========================================
      // SERVER DOWNLOAD COMPLETED
      // =========================================

      setProgress(100);
      setStatus(
        "Video downloaded on server."
      );

      // =========================================
      // GET FILE URL
      // =========================================

      if (!data.download_url) {
        throw new Error(
          "Download completed, but file URL was not returned."
        );
      }

      const fileUrl = getDownloadFileUrl(
        data.download_url
      );

      console.log(
        "File URL:",
        fileUrl
      );

      // =========================================
      // START PHONE / BROWSER DOWNLOAD
      // =========================================

      setStatus(
        "Starting download to your device..."
      );

      const link = document.createElement("a");

      link.href = fileUrl;

      link.download =
        data.filename || "video.mp4";

      link.target = "_blank";

      link.rel = "noopener noreferrer";

      document.body.appendChild(link);

      link.click();

      document.body.removeChild(link);

      // =========================================
      // SUCCESS
      // =========================================

      setStatus(
        "Download started. Check your Downloads folder."
      );

      setUrl("");

    } catch (error) {

      console.error(
        "Download error:",
        error
      );

      setProgress(0);

      setStatus(
        error.message ||
        "Download failed."
      );

    } finally {

      setIsDownloading(false);
    }
  };

  return (
    <main className="download-page">

      {/* =========================================
          BACK BUTTON
      ========================================= */}

      <button
        className="back-button"
        onClick={onBack}
        disabled={isDownloading}
      >
        ← Back
      </button>


      {/* =========================================
          TITLE
      ========================================= */}

      <h1 className="download-title">
        {isYouTube
          ? "Download YouTube Video"
          : "Download Instagram Reel"}
      </h1>


      {/* =========================================
          DESCRIPTION
      ========================================= */}

      <p className="download-description">
        {isYouTube
          ? "Paste the YouTube video URL below"
          : "Paste an Instagram Reel URL below"}
      </p>


      {/* =========================================
          DOWNLOAD BOX
      ========================================= */}

      <div className="download-box">

        {/* URL INPUT */}

        <input
          type="text"
          className="url-input"
          placeholder={
            isYouTube
              ? "Paste YouTube URL..."
              : "Paste Instagram Reel URL..."
          }
          value={url}
          onChange={(e) =>
            setUrl(e.target.value)
          }
          disabled={isDownloading}
        />


        {/* DOWNLOAD BUTTON */}

        <button
          className="download-button"
          onClick={handleDownload}
          disabled={isDownloading}
        >
          {isDownloading
            ? "Downloading..."
            : "Download"}
        </button>

      </div>


      {/* =========================================
          PROGRESS
      ========================================= */}

      {(isDownloading ||
        progress > 0 ||
        status) && (

        <ProgressBar
          progress={progress}
          status={status}
        />

      )}

    </main>
  );
}

export default DownloadPage;
