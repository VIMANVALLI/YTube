import React from "react";

function ProgressBar({ progress, status }) {
  return (
    <div className="progress-container">
      
      <div className="progress-header">
        <span className="progress-text">
          {status}
        </span>

        <span className="progress-percentage">
          {progress}%
        </span>
      </div>

      <div className="progress-bar-background">
        <div
          className="progress-bar"
          style={{
            width: `${progress}%`,
          }}
        />
      </div>

    </div>
  );
}

export default ProgressBar;