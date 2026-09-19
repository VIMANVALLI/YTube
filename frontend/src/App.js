import React, { useState } from "react";
import "./App.css";

import Header from "./components/Header";
import Home from "./components/Home";
import DownloadPage from "./components/DownloadPage";
import DownloadedVideos from "./components/DownloadedVideos";

function App() {
  const [page, setPage] = useState("home");
  const [platform, setPlatform] = useState("");

  const handleSelectPlatform = (selectedPlatform) => {
    setPlatform(selectedPlatform);
    setPage("download");
  };

  const handleBackHome = () => {
    setPage("home");
    setPlatform("");
  };

  const handleOpenDownloads = () => {
    setPage("downloads");
  };

  return (
    <div className="app">

      <Header
        onOpenDownloads={handleOpenDownloads}
      />

      {page === "home" && (
        <Home
          onSelectPlatform={handleSelectPlatform}
        />
      )}

      {page === "download" && (
        <DownloadPage
          platform={platform}
          onBack={handleBackHome}
        />
      )}

      {page === "downloads" && (
        <DownloadedVideos
          onBack={handleBackHome}
        />
      )}

    </div>
  );
}

export default App;