import os
import shutil

from yt_dlp import YoutubeDL


# =========================================
# YOUTUBE COOKIES
# =========================================

YOUTUBE_COOKIES_PATH = (
    "/etc/secrets/youtube_cookies.txt"
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
# FFMPEG
# =========================================

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
    "error": None,
}


# =========================================
# RESET PROGRESS
# =========================================

def reset_progress():

    download_progress.update({

        "progress": 0,

        "status": (
            "Starting download..."
        ),

        "downloaded_bytes": 0,

        "total_bytes": 0,

        "speed": 0,

        "eta": 0,

        "filename": "",

        "completed": False,

        "error": None,
    })


# =========================================
# PROGRESS HOOK
# =========================================

def progress_hook(data):

    status = data.get("status")


    # =====================================
    # DOWNLOADING
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

            download_progress["progress"] = round(
                min(
                    100,
                    max(
                        0,
                        percentage
                    )
                ),
                1
            )


        download_progress[
            "downloaded_bytes"
        ] = downloaded


        download_progress[
            "total_bytes"
        ] = total


        download_progress[
            "speed"
        ] = data.get("speed") or 0


        download_progress[
            "eta"
        ] = data.get("eta") or 0


        filename = data.get(
            "filename",
            ""
        )


        if filename:

            download_progress[
                "filename"
            ] = os.path.basename(
                filename
            )


        download_progress[
            "status"
        ] = "Downloading..."


    # =====================================
    # DOWNLOAD FINISHED
    # =====================================

    elif status == "finished":

        download_progress[
            "progress"
        ] = 100


        download_progress[
            "status"
        ] = "Processing video..."


        filename = data.get(
            "filename",
            ""
        )


        if filename:

            download_progress[
                "filename"
            ] = os.path.basename(
                filename
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
    # VALIDATE PLATFORM
    # =====================================

    if platform not in [
        "youtube",
        "instagram"
    ]:

        message = "Invalid platform."

        download_progress[
            "status"
        ] = "Error"

        download_progress[
            "error"
        ] = message


        return {
            "success": False,
            "error": message
        }


    # =====================================
    # VALIDATE URL
    # =====================================

    if not url.strip():

        message = "URL is required."

        download_progress[
            "status"
        ] = "Error"

        download_progress[
            "error"
        ] = message


        return {
            "success": False,
            "error": message
        }


    # =====================================
    # CHECK FFMPEG
    # =====================================

    if not FFMPEG_PATH:

        message = (
            "FFmpeg was not found "
            "on the server."
        )

        download_progress[
            "status"
        ] = "Error"

        download_progress[
            "error"
        ] = message


        return {
            "success": False,
            "error": message
        }


    url = url.strip()


    # =====================================
    # YT-DLP OPTIONS
    # =====================================

    options = {

        # Best video + audio
        "format": "bv*+ba/b",


        # Merge into MP4
        "merge_output_format": "mp4",


        # FFmpeg
        "ffmpeg_location": FFMPEG_PATH,


        # Output filename
        "outtmpl": os.path.join(
            DOWNLOAD_DIR,
            "%(title)s.%(ext)s"
        ),


        # Don't download playlists
        "noplaylist": True,


        # Show yt-dlp output
        "quiet": False,


        "no_warnings": False,


        # Don't ignore errors
        "ignoreerrors": False,


        # Safe filenames
        "restrictfilenames": True,


        # Overwrite existing files
        "overwrites": True,


        # Progress hook
        "progress_hooks": [
            progress_hook
        ],


        # =================================
        # CONNECTION SETTINGS
        # =================================

        "retries": 5,

        "fragment_retries": 5,

        "socket_timeout": 30,

        "http_chunk_size": 10485760,


        # =================================
        # YOUTUBE CLIENT
        # =================================

        "extractor_args": {

            "youtube": {

                "player_client": [
                    "android",
                    "web"
                ]

            }

        },

    }


    # =====================================
    # YOUTUBE COOKIES
    # =====================================

    if os.path.exists(
        YOUTUBE_COOKIES_PATH
    ):

        options["cookiefile"] = (
            YOUTUBE_COOKIES_PATH
        )

        print(
            "YouTube cookies found "
            "and enabled."
        )

    else:

        print(
            "WARNING: YouTube cookies "
            "file not found."
        )


    # =====================================
    # START DOWNLOAD
    # =====================================

    try:

        print(
            "========================================"
        )

        print(
            "STARTING DOWNLOAD"
        )

        print(
            "Platform:",
            platform
        )

        print(
            "URL:",
            url
        )

        print(
            "FFmpeg:",
            FFMPEG_PATH
        )

        print(
            "Download directory:",
            DOWNLOAD_DIR
        )

        print(
            "YouTube cookies:",
            os.path.exists(
                YOUTUBE_COOKIES_PATH
            )
        )

        print(
            "========================================"
        )


        # =================================
        # YOUTUBE-DL
        # =================================

        with YoutubeDL(options) as ydl:

            # -----------------------------
            # Extract information
            # -----------------------------

            info = ydl.extract_info(
                url,
                download=False
            )


            if not info:

                message = (
                    "Could not extract "
                    "video information."
                )

                download_progress[
                    "status"
                ] = "Error"

                download_progress[
                    "error"
                ] = message


                return {
                    "success": False,
                    "error": message
                }


            # -----------------------------
            # Video title
            # -----------------------------

            title = info.get(
                "title",
                "video"
            )


            print(
                "Video title:",
                title
            )


            # -----------------------------
            # Download
            # -----------------------------

            ydl.download([
                url
            ])


            # -----------------------------
            # Prepare filename
            # -----------------------------

            filename = ydl.prepare_filename(
                info
            )


            base_filename = (
                os.path.splitext(
                    filename
                )[0]
            )


            # -----------------------------
            # Possible output files
            # -----------------------------

            possible_files = [

                base_filename + ".mp4",

                base_filename + ".mkv",

                base_filename + ".webm",

                base_filename + ".mov",

            ]


            final_filename = None


            # -----------------------------
            # Find downloaded file
            # -----------------------------

            for file_path in possible_files:

                if os.path.exists(
                    file_path
                ):

                    final_filename = (
                        file_path
                    )

                    break


            # -----------------------------
            # File not found
            # -----------------------------

            if not final_filename:

                message = (
                    "Download completed "
                    "but output file was "
                    "not found."
                )

                download_progress[
                    "status"
                ] = "Error"

                download_progress[
                    "error"
                ] = message


                return {
                    "success": False,
                    "error": message
                }


            # =================================
            # DOWNLOAD COMPLETED
            # =================================

            download_progress[
                "progress"
            ] = 100


            download_progress[
                "status"
            ] = "Completed"


            download_progress[
                "filename"
            ] = os.path.basename(
                final_filename
            )


            download_progress[
                "completed"
            ] = True


            download_progress[
                "error"
            ] = None


            print(
                "========================================"
            )

            print(
                "DOWNLOAD COMPLETED"
            )

            print(
                "File:",
                final_filename
            )

            print(
                "========================================"
            )


            # =================================
            # RETURN RESULT
            # =================================

            return {

                "success": True,

                "title": title,

                "filename": os.path.basename(
                    final_filename
                ),

                "path": final_filename

            }


    # =====================================
    # ERROR
    # =====================================

    except Exception as e:

        error_message = str(e)


        download_progress[
            "status"
        ] = "Error"


        download_progress[
            "error"
        ] = error_message


        download_progress[
            "completed"
        ] = False


        print(
            "========================================"
        )

        print(
            "DOWNLOAD ERROR"
        )

        print(
            error_message
        )

        print(
            "========================================"
        )


        return {

            "success": False,

            "error": error_message

        }
        
