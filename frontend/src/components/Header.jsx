import React, { useState } from "react";

function Header({ onOpenDownloads }) {
  const [showMenu, setShowMenu] = useState(false);

  const handleDownloads = () => {
    setShowMenu(false);

    if (onOpenDownloads) {
      onOpenDownloads();
    }
  };

  return (
    <header className="header">

      {/* App Name */}
      <div className="app-name">
        Video Downloader
      </div>

      {/* Three Dot Menu */}
      <div className="menu-container">

        <button
          className="menu-button"
          onClick={() => setShowMenu(!showMenu)}
        >
          ⋮
        </button>

        {showMenu && (
          <div className="dropdown-menu">

            <button
              className="dropdown-item"
              onClick={handleDownloads}
            >
              Downloaded Videos
            </button>

          </div>
        )}

      </div>

    </header>
  );
}

export default Header;