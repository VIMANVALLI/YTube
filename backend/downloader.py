import os
import shutil
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "downloads"
)

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

FFMPEG_PATH = shutil.which("ffmpeg")

download_progress = {
    "progress": 0,
    "status": "Idle",
    "downloaded_bytes": 0,
    "total_bytes": 0,
    "speed": 0,
    "eta": 0,
    "filename": "",
    "completed": False,
    "error": None,
}


def reset_progress():
    download_progress.update({
        "progress": 0,
        "status": "Starting download...",
        "downloaded_bytes": 0,
        "total_bytes": 0,
        "speed": 0,
        "eta": 0,
        "filename": "",
        "completed": False,
        "error": None,
    })


def progress_hook(data):
    status = data.get("status")

    if status == "downloading":
        downloaded = data.get("downloaded_bytes", 0)
        total = (
            data.get("total_bytes")
            or data.get("total_bytes_estimate")
            or 0
        )

        if total:
            percentage = (downloaded / total) * 100
            download_progress["progress"] = round(
                min(100, max(0, percentage)), 1
            )

        download_progress["downloaded_bytes"] = downloaded
        download_progress["total_bytes"] = total
        download_progress["speed"] = data.get("speed") or 0
        download_progress["eta"] = data.get("eta") or 0

        filename = data.get("filename", "")

        if filename:
            download_progress["filename"] = os.path.basename(filename)

        download_progress["status"] = "Downloading..."

    elif status == "finished":
        download_progress["progress"] = 100
        download_progress["status"] = "Processing video..."

        filename = data.get("filename", "")

        if filename:
            download_progress["filename"] = os.path.basename(filename)


def download_video(url: str, platform: str):

    reset_progress()

    if platform not in ["youtube", "instagram"]:
        message = "Invalid platform."
        download_progress["status"] = "Error"
        download_progress["error"] = message

        return {
            "success": False,
            "error": message
        }

    if not url.strip():
        message = "URL is required."
        download_progress["status"] = "Error"
        download_progress["error"] = message

        return {
            "success": False,
            "error": message
        }

    if not FFMPEG_PATH:
        message = "FFmpeg was not found on the server."

        download_progress["status"] = "Error"
        download_progress["error"] = message

        return {
            "success": False,
            "error": message
        }

    url = url.strip()

    options = {
        "format": "bv*+ba/b",

        "merge_output_format": "mp4",

        "ffmpeg_location": FFMPEG_PATH,

        "outtmpl": os.path.join(
            DOWNLOAD_DIR,
            "%(title)s.%(ext)s"
        ),

        "noplaylist": True,

        "quiet": False,

        "no_warnings": False,

        "ignoreerrors": False,

        "restrictfilenames": True,

        "overwrites": True,

        "progress_hooks": [
            progress_hook
        ],

        # YouTube connection settings
        "retries": 5,

        "fragment_retries": 5,

        "socket_timeout": 30,

        "http_chunk_size": 10485760,

        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        },
    }

    try:

        print("========================================")
        print("STARTING DOWNLOAD")
        print("Platform:", platform)
        print("URL:", url)
        print("FFmpeg:", FFMPEG_PATH)
        print("Download directory:", DOWNLOAD_DIR)
        print("========================================")

        with YoutubeDL(options) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

            if not info:

                message = (
                    "Could not extract video information."
                )

                download_progress["status"] = "Error"
                download_progress["error"] = message

                return {
                    "success": False,
                    "error": message
                }

            title = info.get(
                "title",
                "video"
            )

            print("Video title:", title)

            ydl.download([url])

            filename = ydl.prepare_filename(info)

            base_filename = os.path.splitext(
                filename
            )[0]

            possible_files = [
                base_filename + ".mp4",
                base_filename + ".mkv",
                base_filename + ".webm",
                base_filename + ".mov",
            ]

            final_filename = None

            for file_path in possible_files:

                if os.path.exists(file_path):
                    final_filename = file_path
                    break

            if not final_filename:

                message = (
                    "Download completed but "
                    "output file was not found."
                )

                download_progress["status"] = "Error"
                download_progress["error"] = message

                return {
                    "success": False,
                    "error": message
                }

            download_progress["progress"] = 100
            download_progress["status"] = "Completed"
            download_progress["filename"] = os.path.basename(
                final_filename
            )
            download_progress["completed"] = True
            download_progress["error"] = None

            print("========================================")
            print("DOWNLOAD COMPLETED")
            print("File:", final_filename)
            print("========================================")

            return {
                "success": True,
                "title": title,
                "filename": os.path.basename(
                    final_filename
                ),
                "path": final_filename
            }

    except Exception as e:

        error_message = str(e)

        download_progress["status"] = "Error"
        download_progress["error"] = error_message
        download_progress["completed"] = False

        print("========================================")
        print("DOWNLOAD ERROR")
        print(error_message)
        print("========================================")

        return {
            "success": False,
            "error": error_message
        }
