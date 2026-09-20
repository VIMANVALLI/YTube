import React, { useState } from "react";
import ProgressBar from "./ProgressBar";
import {
  downloadVideo,
  getDownloadFileUrl,
} from "../services/api";

function DownloadPage({ platform, onBack }) {
  const [url, setUrl] = useState("");
  const [format, setFormat] = useState("");
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [isDownloading, setIsDownloading] = useState(false);

  const isYouTube = platform === "youtube";
  const isInstagram = platform === "instagram";

  // ===============================
  // URL VALIDATION
  // ===============================
  const validateUrl = () => {
    if (!url.trim()) {
      setStatus("Please enter a URL.");
      return false;
    }

    // YouTube validation
    if (isYouTube) {
      const youtubeRegex =
        /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\//i;

      if (!youtubeRegex.test(url.trim())) {
        setStatus("Please enter a valid YouTube URL.");
        return false;
      }
    }

    // Instagram validation
    if (isInstagram) {
      const instagramRegex =
        /^(https?:\/\/)?(www\.)?instagram\.com\//i;

      if (!instagramRegex.test(url.trim())) {
        setStatus("Please enter a valid Instagram URL.");
        return false;
      }
    }

    // Format validation for both platforms
    if (!format) {
      setStatus("Please select a format.");
      return false;
    }

    return true;
  };

  // ===============================
  // DOWNLOAD
  // ===============================
  const handleDownload = async () => {
    if (!validateUrl()) {
      return;
    }

    setIsDownloading(true);
    setProgress(10);
    setStatus("Connecting to server...");

    try {
      setProgress(20);
      setStatus("Starting download...");

      const data = await downloadVideo(
        url.trim(),
        platform,
        format
      );

      console.log("Download result:", data);

      if (!data || !data.download_url) {
        throw new Error(
          "Download completed, but the download file was not found."
        );
      }

      setProgress(80);
      setStatus("Preparing file...");

      // ===============================
      // START BROWSER DOWNLOAD
      // ===============================
      const downloadUrl = getDownloadFileUrl(
        data.download_url
      );

      const link = document.createElement("a");

      link.href = downloadUrl;

      if (data.filename) {
        link.download = data.filename;
      }

      link.target = "_blank";
      link.rel = "noopener noreferrer";

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      setProgress(100);

      setStatus(
        "Download started. Check your Downloads folder."
      );

      // Clear form
      setUrl("");
      setFormat("");
    } catch (error) {
      console.error("Download error:", error);

      setProgress(0);

      setStatus(
        error.message ||
          "Download failed. Please try again."
      );
    } finally {
      setIsDownloading(false);
    }
  };

  // ===============================
  // URL CHANGE
  // ===============================
  const handleUrlChange = (event) => {
    setUrl(event.target.value);

    if (status) {
      setStatus("");
    }

    if (progress > 0) {
      setProgress(0);
    }
  };

  // ===============================
  // FORMAT CHANGE
  // ===============================
  const handleFormatChange = (event) => {
    setFormat(event.target.value);

    if (status) {
      setStatus("");
    }
  };

  // ===============================
  // TITLE
  // ===============================
  const getTitle = () => {
    if (isYouTube) {
      return "Download YouTube Video";
    }

    if (isInstagram) {
      return "Download Instagram Reel";
    }

    return "Download Video";
  };

  // ===============================
  // DESCRIPTION
  // ===============================
  const getDescription = () => {
    if (isYouTube) {
      return "Paste a YouTube video URL below and choose your format.";
    }

    if (isInstagram) {
      return "Paste an Instagram Reel URL below and choose your format.";
    }

    return "Paste your video URL below.";
  };

  // ===============================
  // PLACEHOLDER
  // ===============================
  const getPlaceholder = () => {
    if (isYouTube) {
      return "Paste YouTube URL...";
    }

    if (isInstagram) {
      return "Paste Instagram Reel URL...";
    }

    return "Paste video URL...";
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
        {getTitle()}
      </h1>

      {/* Description */}
      <p className="download-description">
        {getDescription()}
      </p>

      {/* Download Box */}
      <div className="download-box">

        {/* URL Input */}
        <input
          type="text"
          className="url-input"
          placeholder={getPlaceholder()}
          value={url}
          onChange={handleUrlChange}
          disabled={isDownloading}
        />

        {/* Format Dropdown */}
        {(isYouTube || isInstagram) && (
          <select
            className="format-select"
            value={format}
            onChange={handleFormatChange}
            disabled={isDownloading}
          >
            <option value="">
              Select format
            </option>

            <option value="mp4">
              MP4 - Video
            </option>

            <option value="mp3">
              MP3 - Audio
            </option>
          </select>
        )}

        {/* Download Button */}
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

      {/* Progress */}
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
