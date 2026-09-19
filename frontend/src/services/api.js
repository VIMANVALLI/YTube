const API_URL = "https://ytube-20.onrender.com";

export const downloadVideo = async (url, platform) => {
  const response = await fetch(`${API_URL}/download`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url,
      platform,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Download failed");
  }

  return data;
};


export const getDownloadedVideos = async () => {
  const response = await fetch(`${API_URL}/downloads`);

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to get downloads");
  }

  return data;
};


export const deleteDownloadedVideo = async (filename) => {
  const response = await fetch(
    `${API_URL}/downloads/${encodeURIComponent(filename)}`,
    {
      method: "DELETE",
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to delete video");
  }

  return data;
};
