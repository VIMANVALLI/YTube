import os
import shutil
from yt_dlp import YoutubeDL


# =========================================
# DOWNLOAD FOLDER
# =========================================

DOWNLOAD_DIR = "downloads"

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


# =========================================
# FFMPEG
# =========================================

# Automatically find FFmpeg from system PATH
FFMPEG_PATH = shutil.which("ffmpeg")


# =========================================
# DOWNLOAD PROGRESS
# =========================================

download_progress = {
    "progress": 0,
    "status": "Idle",
    "downloaded_bytes": 0,
    "total_bytes": 0,
    "speed": 0,
    "eta": 0,
    "filename": "",
    "completed": False,
    "error": None
}


# =========================================
# RESET PROGRESS
# =========================================

def reset_progress():

    download_progress["progress"] = 0
    download_progress["status"] = "Starting download..."
    download_progress["downloaded_bytes"] = 0
    download_progress["total_bytes"] = 0
    download_progress["speed"] = 0
    download_progress["eta"] = 0
    download_progress["filename"] = ""
    download_progress["completed"] = False
    download_progress["error"] = None


# =========================================
# PROGRESS HOOK
# =========================================

def progress_hook(data):

    status = data.get("status")

    # =====================================
    # Downloading
    # =====================================

    if status == "downloading":

        downloaded = data.get(
            "downloaded_bytes",
            0
        )

        total = (
            data.get("total_bytes")
            or data.get("total_bytes_estimate")
            or 0
        )

        if total:

            percentage = (
                downloaded / total
            ) * 100

            percentage = min(
                100,
                max(0, percentage)
            )

            download_progress["progress"] = round(
                percentage,
                1
            )

        download_progress["downloaded_bytes"] = (
            downloaded
        )

        download_progress["total_bytes"] = (
            total
        )

        download_progress["speed"] = (
            data.get("speed") or 0
        )

        download_progress["eta"] = (
            data.get("eta") or 0
        )

        filename = data.get(
            "filename",
            ""
        )

        if filename:

            download_progress["filename"] = (
                os.path.basename(filename)
            )

        download_progress["status"] = (
            "Downloading..."
        )

    # =====================================
    # Download finished
    # =====================================

    elif status == "finished":

        download_progress["progress"] = 100

        download_progress["status"] = (
            "Processing video..."
        )

        filename = data.get(
            "filename",
            ""
        )

        if filename:

            download_progress["filename"] = (
                os.path.basename(filename)
            )


# =========================================
# DOWNLOAD VIDEO
# =========================================

def download_video(
    url: str,
    platform: str
):

    reset_progress()


    # =====================================
    # Validate platform
    # =====================================

    if platform not in [
        "youtube",
        "instagram"
    ]:

        download_progress["status"] = "Error"

        download_progress["error"] = (
            "Invalid platform. "
            "Use youtube or instagram."
        )

        return {
            "success": False,
            "error": download_progress["error"]
        }


    # =====================================
    # Validate URL
    # =====================================

    if not url or not url.strip():

        download_progress["status"] = "Error"

        download_progress["error"] = (
            "URL is required."
        )

        return {
            "success": False,
            "error": download_progress["error"]
        }


    url = url.strip()


    # =====================================
    # Check FFmpeg
    # =====================================

    if not FFMPEG_PATH:

        download_progress["status"] = "Error"

        download_progress["error"] = (
            "FFmpeg was not found. "
            "Please install FFmpeg and add it to PATH."
        )

        return {
            "success": False,
            "error": download_progress["error"]
        }


    # =====================================
    # yt-dlp options
    # =====================================

    options = {

        # Best video + audio
        "format": "bv*+ba/b",

        # Merge into MP4
        "merge_output_format": "mp4",

        # FFmpeg
        "ffmpeg_location": FFMPEG_PATH,

        # Output
        "outtmpl": os.path.join(
            DOWNLOAD_DIR,
            "%(title)s.%(ext)s"
        ),

        # No playlist
        "noplaylist": True,

        # Show terminal output
        "quiet": False,

        # Don't ignore errors
        "ignoreerrors": False,

        # Safe filenames
        "restrictfilenames": True,

        # Overwrite
        "overwrites": True,

        # Progress hook
        "progress_hooks": [
            progress_hook
        ],
    }


    # =====================================
    # Download
    # =====================================

    try:

        print("=========================================")
        print("Starting download...")
        print("Platform:", platform)
        print("URL:", url)
        print("FFmpeg:", FFMPEG_PATH)
        print("=========================================")


        with YoutubeDL(options) as ydl:

            # ---------------------------------
            # Extract information
            # ---------------------------------

            info = ydl.extract_info(
                url,
                download=False
            )


            if not info:

                download_progress["status"] = "Error"

                download_progress["error"] = (
                    "Could not extract "
                    "video information."
                )

                return {
                    "success": False,
                    "error": download_progress["error"]
                }


            title = info.get(
                "title",
                "video"
            )


            print("Title:", title)


            # ---------------------------------
            # Download
            # ---------------------------------

            ydl.download([url])


            # ---------------------------------
            # Filename
            # ---------------------------------

            filename = ydl.prepare_filename(
                info
            )


            filename_without_extension = (
                os.path.splitext(filename)[0]
            )


            final_filename = (
                filename_without_extension
                + ".mp4"
            )


            # ---------------------------------
            # Find output
            # ---------------------------------

            if not os.path.exists(
                final_filename
            ):

                possible_extensions = [
                    ".mp4",
                    ".mkv",
                    ".webm",
                    ".mov"
                ]


                found_file = None


                for extension in possible_extensions:

                    possible_file = (
                        filename_without_extension
                        + extension
                    )


                    if os.path.exists(
                        possible_file
                    ):

                        found_file = possible_file

                        break


                if found_file:

                    final_filename = found_file

                else:

                    download_progress["status"] = (
                        "Error"
                    )

                    download_progress["error"] = (
                        "Download completed, "
                        "but output file was not found."
                    )

                    return {
                        "success": False,
                        "error": download_progress["error"]
                    }


            # ---------------------------------
            # Completed
            # ---------------------------------

            download_progress["progress"] = 100

            download_progress["status"] = (
                "Completed"
            )

            download_progress["filename"] = (
                os.path.basename(final_filename)
            )

            download_progress["completed"] = True

            download_progress["error"] = None


            print("=========================================")
            print("DOWNLOAD COMPLETED")
            print("File:", final_filename)
            print("=========================================")


            return {

                "success": True,

                "title": title,

                "filename": os.path.basename(
                    final_filename
                ),

                "path": final_filename

            }


    except Exception as e:

        download_progress["status"] = "Error"

        download_progress["error"] = str(e)

        download_progress["completed"] = False


        print("=========================================")
        print("DOWNLOAD ERROR")
        print(str(e))
        print("=========================================")


        return {

            "success": False,

            "error": str(e)

        }