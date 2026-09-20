import os

from pathlib import Path

from fastapi import (
    FastAPI,
    HTTPException
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.responses import (
    FileResponse
)

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
        "https://ytube-10.onrender.com",
        FRONTEND_URL,
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================
# DOWNLOAD FOLDER
# =========================================

DOWNLOAD_DIR = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    "downloads"
)


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

    format: str = "mp4"


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
# DOWNLOAD VIDEO / AUDIO
# =========================================

@app.post("/download")
def download(
    request: DownloadRequest
):

    # -------------------------------------
    # Validate platform
    # -------------------------------------

    if request.platform not in [
        "youtube",
        "instagram"
    ]:

        raise HTTPException(

            status_code=400,

            detail=(
                "Platform must be "
                "youtube or instagram"
            )

        )


    # -------------------------------------
    # Validate format
    # -------------------------------------

    if request.format not in [
        "mp4",
        "mp3"
    ]:

        raise HTTPException(

            status_code=400,

            detail=(
                "Format must be "
                "mp4 or mp3"
            )

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

        request.platform,

        request.format

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

        "format": request.format,

        "download_url": download_url

    }


# =========================================
# DOWNLOAD PROGRESS
# =========================================

@app.get("/progress")
def get_progress():

    return {

        "progress":
            download_progress["progress"],

        "status":
            download_progress["status"],

        "downloaded_bytes":
            download_progress[
                "downloaded_bytes"
            ],

        "total_bytes":
            download_progress[
                "total_bytes"
            ],

        "speed":
            download_progress["speed"],

        "eta":
            download_progress["eta"],

        "filename":
            download_progress["filename"],

        "completed":
            download_progress["completed"],

        "error":
            download_progress["error"]

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


        if os.path.isfile(
            file_path
        ):

            videos.append({

                "filename": filename,

                "path": file_path,

                "download_url":
                    "/downloads/"
                    + filename

            })


    return {

        "count": len(videos),

        "videos": videos

    }


# =========================================
# SERVE DOWNLOADED FILE
# =========================================

@app.get("/downloads/{filename}")
def serve_download(
    filename: str
):

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

    if not os.path.exists(
        file_path
    ):

        raise HTTPException(

            status_code=404,

            detail="File not found"

        )


    if not os.path.isfile(
        file_path
    ):

        raise HTTPException(

            status_code=404,

            detail="Invalid file"

        )


    # -------------------------------------
    # Detect media type
    # -------------------------------------

    extension = Path(
        safe_filename
    ).suffix.lower()


    media_types = {

        ".mp4":
            "video/mp4",

        ".mp3":
            "audio/mpeg",

        ".webm":
            "video/webm",

        ".mkv":
            "video/x-matroska",

        ".mov":
            "video/quicktime",

    }


    media_type = media_types.get(

        extension,

        "application/octet-stream"

    )


    # -------------------------------------
    # Serve file
    # -------------------------------------

    return FileResponse(

        path=file_path,

        filename=safe_filename,

        media_type=media_type

    )


# =========================================
# DELETE DOWNLOADED FILE
# =========================================

@app.delete(
    "/downloads/{filename}"
)
def delete_download(
    filename: str
):

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

    if not os.path.exists(
        file_path
    ):

        raise HTTPException(

            status_code=404,

            detail="File not found"

        )


    if not os.path.isfile(
        file_path
    ):

        raise HTTPException(

            status_code=404,

            detail="Invalid file"

        )


    # -------------------------------------
    # Delete file
    # -------------------------------------

    try:

        os.remove(
            file_path
        )


        return {

            "message":
                "File deleted successfully",

            "filename":
                safe_filename

        }


    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
