import React, { useEffect, useState } from "react";
import {
  getDownloadedVideos,
  deleteDownloadedVideo,
} from "../services/api";

function DownloadedVideos({ onBack }) {
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadVideos = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getDownloadedVideos();

      setVideos(data.videos || []);
    } catch (error) {
      console.error("Failed to load videos:", error);
      setError(error.message || "Failed to load downloaded videos.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadVideos();
  }, []);

  const handleDeleteClick = (video) => {
    setSelectedVideo(video);
  };

  const handleDelete = async () => {
    if (!selectedVideo) {
      return;
    }

    try {
      await deleteDownloadedVideo(selectedVideo.filename);

      setVideos((currentVideos) =>
        currentVideos.filter(
          (video) =>
            video.filename !== selectedVideo.filename
        )
      );

      setSelectedVideo(null);
    } catch (error) {
      console.error("Delete error:", error);
      setError(error.message || "Failed to delete video.");
      setSelectedVideo(null);
    }
  };

  const handleCancel = () => {
    setSelectedVideo(null);
  };

  return (
    <main className="downloaded-page">

      {/* Back Button */}
      <button
        className="back-button"
        onClick={onBack}
      >
        ← Back
      </button>

      {/* Title */}
      <h1 className="downloaded-title">
        Downloaded Videos
      </h1>

      {/* Loading */}
      {loading && (
        <div className="empty-state">
          <div className="empty-state-title">
            Loading...
          </div>
        </div>
      )}

      {/* Error */}
      {!loading && error && (
        <div className="empty-state">
          <div className="empty-state-title">
            {error}
          </div>
        </div>
      )}

      {/* Videos */}
      {!loading && !error && videos.length > 0 && (
        <div className="video-list">

          {videos.map((video) => (
            <div
              className="video-item"
              key={video.filename}
            >

              <div className="video-info">

                <div className="video-icon">
                  ▶
                </div>

                <div className="video-details">

                  <div className="video-name">
                    {video.filename}
                  </div>

                  <div className="video-platform">
                    Downloaded Video
                  </div>

                </div>

              </div>

              <button
                className="delete-button"
                onClick={() => handleDeleteClick(video)}
              >
                Delete
              </button>

            </div>
          ))}

        </div>
      )}

      {/* Empty */}
      {!loading && !error && videos.length === 0 && (
        <div className="empty-state">

          <div className="empty-state-title">
            No downloaded videos
          </div>

          <div className="empty-state-text">
            Your downloaded videos will appear here.
          </div>

        </div>
      )}

      {/* Delete Confirmation */}
      {selectedVideo && (
        <div className="modal-overlay">

          <div className="modal">

            <h2 className="modal-title">
              Delete Video?
            </h2>

            <p className="modal-message">
              Are you sure you want to delete{" "}
              <strong>
                {selectedVideo.filename}
              </strong>
              ?
            </p>

            <div className="modal-buttons">

              <button
                className="cancel-button"
                onClick={handleCancel}
              >
                Cancel
              </button>

              <button
                className="confirm-delete-button"
                onClick={handleDelete}
              >
                Delete
              </button>

            </div>

          </div>

        </div>
      )}

    </main>
  );
}

export default DownloadedVideos;