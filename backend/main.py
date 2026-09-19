import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from downloader import (
    download_video,
    download_progress
)


# =========================================
# FASTAPI APPLICATION
# =========================================

app = FastAPI(
    title="Video Downloader API",
    description="YouTube and Instagram video downloader",
    version="1.0.0"
)


# =========================================
# CORS
# =========================================

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:3000"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://ytube-8.onrender.com",
        FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# DOWNLOAD FOLDER
# =========================================

DOWNLOAD_DIR = "downloads"

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


# =========================================
# REQUEST MODEL
# =========================================

class DownloadRequest(BaseModel):
    url: str
    platform: str


# =========================================
# HOME
# =========================================

@app.get("/")
def home():

    return {
        "message": "Video Downloader API is running",
        "status": "success"
    }


# =========================================
# DOWNLOAD VIDEO
# =========================================

@app.post("/download")
def download(request: DownloadRequest):

    # -------------------------------------
    # Validate platform
    # -------------------------------------

    if request.platform not in [
        "youtube",
        "instagram"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Platform must be youtube or instagram"
        )


    # -------------------------------------
    # Validate URL
    # -------------------------------------

    if not request.url.strip():

        raise HTTPException(
            status_code=400,
            detail="URL is required"
        )


    # -------------------------------------
    # Start download
    # -------------------------------------

    result = download_video(
        request.url.strip(),
        request.platform
    )


    # -------------------------------------
    # Handle download error
    # -------------------------------------

    if not result["success"]:

        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )


    # -------------------------------------
    # Download URL
    # -------------------------------------

    download_url = (
        "/downloads/"
        + result["filename"]
    )


    # -------------------------------------
    # Response
    # -------------------------------------

    return {
        "message": "Download completed",
        "title": result["title"],
        "filename": result["filename"],
        "path": result["path"],
        "download_url": download_url
    }


# =========================================
# DOWNLOAD PROGRESS
# =========================================

@app.get("/progress")
def get_progress():

    return {
        "progress": download_progress["progress"],
        "status": download_progress["status"],
        "downloaded_bytes": download_progress[
            "downloaded_bytes"
        ],
        "total_bytes": download_progress[
            "total_bytes"
        ],
        "speed": download_progress["speed"],
        "eta": download_progress["eta"],
        "filename": download_progress["filename"],
        "completed": download_progress["completed"],
        "error": download_progress["error"]
    }


# =========================================
# GET DOWNLOADED VIDEOS
# =========================================

@app.get("/downloads")
def get_downloads():

    videos = []

    for filename in os.listdir(
        DOWNLOAD_DIR
    ):

        file_path = os.path.join(
            DOWNLOAD_DIR,
            filename
        )

        if os.path.isfile(file_path):

            videos.append({
                "filename": filename,
                "path": file_path,
                "download_url": (
                    "/downloads/"
                    + filename
                )
            })

    return {
        "count": len(videos),
        "videos": videos
    }


# =========================================
# SERVE VIDEO
# =========================================

@app.get("/downloads/{filename}")
def serve_download(filename: str):

    # -------------------------------------
    # Prevent path traversal
    # -------------------------------------

    safe_filename = os.path.basename(
        filename
    )

    file_path = os.path.join(
        DOWNLOAD_DIR,
        safe_filename
    )


    # -------------------------------------
    # Check file
    # -------------------------------------

    if not os.path.exists(file_path):

        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    if not os.path.isfile(file_path):

        raise HTTPException(
            status_code=404,
            detail="Invalid file"
        )


    # -------------------------------------
    # Serve video
    # -------------------------------------

    return FileResponse(
        path=file_path,
        filename=safe_filename,
        media_type="video/mp4"
    )


# =========================================
# DELETE VIDEO
# =========================================

@app.delete("/downloads/{filename}")
def delete_download(filename: str):

    # -------------------------------------
    # Prevent path traversal
    # -------------------------------------

    safe_filename = os.path.basename(
        filename
    )

    file_path = os.path.join(
        DOWNLOAD_DIR,
        safe_filename
    )


    # -------------------------------------
    # Check file
    # -------------------------------------

    if not os.path.exists(file_path):

        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    if not os.path.isfile(file_path):

        raise HTTPException(
            status_code=404,
            detail="Invalid file"
        )


    # -------------------------------------
    # Delete video
    # -------------------------------------

    try:

        os.remove(file_path)

        return {
            "message": "Video deleted successfully",
            "filename": safe_filename
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
