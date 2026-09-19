import React from "react";

function Home({ onSelectPlatform }) {
  const handleYouTube = () => {
    onSelectPlatform("youtube");
  };

  const handleInstagram = () => {
    onSelectPlatform("instagram");
  };

  return (
    <main className="home-page">

      {/* Title */}
      <h1 className="home-title">
        Download Your Videos
      </h1>

      {/* Subtitle */}
      <p className="home-subtitle">
        Download videos for offline viewing
      </p>

      {/* Platform Buttons */}
      <div className="platform-buttons">

        {/* YouTube */}
        <button
          className="platform-button"
          onClick={handleYouTube}
        >
          YouTube
        </button>

        {/* Instagram */}
        <button
          className="platform-button"
          onClick={handleInstagram}
        >
          Instagram
        </button>

      </div>

    </main>
  );
}

export default Home;