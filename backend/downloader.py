import os
import shutil
from yt_dlp import YoutubeDL


# =========================================
# DOWNLOAD DIRECTORY
# =========================================

DOWNLOAD_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "downloads"
)

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# =========================================
# FFMPEG
# =========================================

FFMPEG_PATH = shutil.which("ffmpeg")


# =========================================
# DENO / JAVASCRIPT RUNTIME
# =========================================

DENO_PATH = shutil.which("deno")

# Fallback: default Deno installation path
if not DENO_PATH:
    DEFAULT_DENO_PATH = os.path.expanduser(
        "~/.deno/bin/deno"
    )

    if os.path.exists(DEFAULT_DENO_PATH):
        DENO_PATH = DEFAULT_DENO_PATH


print("=" * 60)
print("Runtime configuration")
print(f"FFmpeg: {FFMPEG_PATH}")
print(f"Deno: {DENO_PATH}")
print("=" * 60)


# =========================================
# YOUTUBE COOKIES
# =========================================

# Render Secret File - READ ONLY
YOUTUBE_COOKIES_SOURCE = (
    "/etc/secrets/youtube_cookies.txt"
)

# Writable temporary location
YOUTUBE_COOKIES_PATH = (
    "/tmp/youtube_cookies.txt"
)


# =========================================
# COPY YOUTUBE COOKIES
# =========================================

def prepare_youtube_cookies():
    """
    Copy the Render Secret File to /tmp because
    /etc/secrets is read-only.
    """

    if not os.path.exists(
        YOUTUBE_COOKIES_SOURCE
    ):
        print(
            "WARNING: YouTube Secret File not found."
        )

        return False

    try:

        shutil.copyfile(
            YOUTUBE_COOKIES_SOURCE,
            YOUTUBE_COOKIES_PATH
        )

        print(
            "YouTube cookies copied to writable storage."
        )

        return True

    except Exception as e:

        print(
            "WARNING: Could not copy YouTube cookies:",
            str(e)
        )

        return False


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

        "status": "Starting download...",

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
                min(100, max(0, percentage)),
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
        ] = "Processing file..."


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
# DOWNLOAD VIDEO / AUDIO
# =========================================

def download_video(
    url: str,
    platform: str,
    format: str = "mp4"
):

    reset_progress()


    # =====================================
    # VALIDATE PLATFORM
    # =====================================

    if platform not in [
        "youtube",
        "instagram"
    ]:

        error = "Unsupported platform."

        download_progress[
            "status"
        ] = "Error"

        download_progress[
            "error"
        ] = error


        return {

            "success": False,

            "error": error

        }


    # =====================================
    # VALIDATE FORMAT
    # =====================================

    if format not in [
        "mp4",
        "mp3"
    ]:

        error = (
            "Please select a valid format."
        )

        download_progress[
            "status"
        ] = "Error"

        download_progress[
            "error"
        ] = error


        return {

            "success": False,

            "error": error

        }


    # =====================================
    # VALIDATE URL
    # =====================================

    if not url or not url.strip():

        error = (
            "Please provide a valid URL."
        )

        download_progress[
            "status"
        ] = "Error"

        download_progress[
            "error"
        ] = error


        return {

            "success": False,

            "error": error

        }


    url = url.strip()


    # =====================================
    # CHECK FFMPEG
    # =====================================

    if not FFMPEG_PATH:

        error = (
            "FFmpeg was not found on the server."
        )

        download_progress[
            "status"
        ] = "Error"

        download_progress[
            "error"
        ] = error


        return {

            "success": False,

            "error": error

        }


    # =====================================
    # PREPARE YOUTUBE COOKIES
    # =====================================

    youtube_cookies_ready = False


    if platform == "youtube":

        youtube_cookies_ready = (
            prepare_youtube_cookies()
        )


    # =====================================
    # YT-DLP OPTIONS
    # =====================================

    # MP3
    if format == "mp3":

        options = {

            # Best available audio
            "format": "bestaudio/best",

            # Convert audio to MP3
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],

            # FFmpeg
            "ffmpeg_location": FFMPEG_PATH,

            # Output file
            "outtmpl": os.path.join(
                DOWNLOAD_DIR,
                "%(title)s.%(ext)s"
            ),

            # Don't download playlists
            "noplaylist": True,

            # Console output
            "quiet": False,

            "no_warnings": False,

            # Don't ignore errors
            "ignoreerrors": False,

            # Safe filenames
            "restrictfilenames": True,

            # Replace existing files
            "overwrites": True,

            # Progress hook
            "progress_hooks": [
                progress_hook
            ],

            # Retry settings
            "retries": 5,

            "fragment_retries": 5,

            # Network timeout
            "socket_timeout": 30,

            # HTTP chunk size
            "http_chunk_size": 10485760,
        }

    # MP4
    else:

        options = {

            # Best available video + audio
            "format": "bv*+ba/b",

            # Merge into MP4
            "merge_output_format": "mp4",

            # FFmpeg
            "ffmpeg_location": FFMPEG_PATH,

            # Output file
            "outtmpl": os.path.join(
                DOWNLOAD_DIR,
                "%(title)s.%(ext)s"
            ),

            # Don't download playlists
            "noplaylist": True,

            # Console output
            "quiet": False,

            "no_warnings": False,

            # Don't ignore errors
            "ignoreerrors": False,

            # Safe filenames
            "restrictfilenames": True,

            # Replace existing files
            "overwrites": True,

            # Progress hook
            "progress_hooks": [
                progress_hook
            ],

            # Retry settings
            "retries": 5,

            "fragment_retries": 5,

            # Network timeout
            "socket_timeout": 30,

            # HTTP chunk size
            "http_chunk_size": 10485760,
        }


    # =====================================
    # YOUTUBE JAVASCRIPT RUNTIME
    # =====================================

    if platform == "youtube":

        if DENO_PATH:

            # yt-dlp expects:
            #
            # {
            #     "deno": {
            #         "path": "..."
            #     }
            # }

            options["js_runtimes"] = {

                "deno": {

                    "path": DENO_PATH

                }

            }


            print(
                "Deno JavaScript runtime enabled: "
                f"{DENO_PATH}"
            )

        else:

            print(
                "WARNING: Deno was not found."
            )

            print(
                "YouTube may fail because "
                "yt-dlp EJS requires a JavaScript runtime."
            )


    # =====================================
    # ENABLE YOUTUBE COOKIES
    # =====================================

    if (
        platform == "youtube"
        and youtube_cookies_ready
        and os.path.exists(
            YOUTUBE_COOKIES_PATH
        )
    ):

        options[
            "cookiefile"
        ] = YOUTUBE_COOKIES_PATH


        print(
            "YouTube cookies found and enabled."
        )


    elif platform == "youtube":

        print(
            "WARNING: Writable YouTube "
            "cookies file not found."
        )


    # =====================================
    # START DOWNLOAD
    # =====================================

    try:

        print("=" * 60)

        print(
            f"Starting {platform} {format} download:"
        )

        print(url)

        print(
            f"FFmpeg: {FFMPEG_PATH}"
        )

        print(
            f"Deno: {DENO_PATH}"
        )

        print(
            f"YouTube cookies: "
            f"{youtube_cookies_ready}"
        )

        print(
            f"Format: {format}"
        )

        print("=" * 60)


        # =================================
        # CREATE YT-DLP
        # =================================

        with YoutubeDL(options) as ydl:


            # =============================
            # GET VIDEO INFORMATION
            # =============================

            info = ydl.extract_info(
                url,
                download=False
            )


            if not info:

                error = (
                    "Could not retrieve "
                    "video information."
                )

                download_progress[
                    "status"
                ] = "Error"


                download_progress[
                    "error"
                ] = error


                return {

                    "success": False,

                    "error": error

                }


            # =============================
            # VIDEO TITLE
            # =============================

            title = info.get(
                "title",
                "Downloaded Video"
            )


            print(
                f"Video title: {title}"
            )


            # =============================
            # DOWNLOAD
            # =============================

            ydl.download([url])


            # =============================
            # GET GENERATED FILENAME
            # =============================

            filename = ydl.prepare_filename(
                info
            )


            base_filename = (
                os.path.splitext(
                    filename
                )[0]
            )


            # =============================
            # POSSIBLE OUTPUT FILES
            # =============================

            possible_files = [

                # MP4
                base_filename + ".mp4",

                # MP3
                base_filename + ".mp3",

                # Other video formats
                base_filename + ".mkv",

                base_filename + ".webm",

                base_filename + ".mov",

            ]


            final_filename = None


            # =============================
            # FIND FINAL FILE
            # =============================

            for file_path in possible_files:

                if os.path.exists(
                    file_path
                ):

                    final_filename = (
                        file_path
                    )

                    break


            # =============================
            # FALLBACK SEARCH
            # =============================

            if not final_filename:

                directory_files = (
                    os.listdir(
                        DOWNLOAD_DIR
                    )
                )


                target_name = (
                    os.path.splitext(
                        os.path.basename(
                            filename
                        )
                    )[0]
                )


                matching_files = [

                    os.path.join(
                        DOWNLOAD_DIR,
                        file
                    )

                    for file in directory_files

                    if os.path.splitext(
                        file
                    )[0] == target_name

                ]


                if matching_files:

                    # Prefer requested format
                    preferred_extension = (
                        ".mp3"
                        if format == "mp3"
                        else ".mp4"
                    )

                    preferred_file = next(
                        (
                            file
                            for file in matching_files
                            if file.lower().endswith(
                                preferred_extension
                            )
                        ),
                        None
                    )

                    final_filename = (
                        preferred_file
                        or matching_files[0]
                    )


            # =============================
            # FILE NOT FOUND
            # =============================

            if not final_filename:

                error = (
                    "Download completed, "
                    "but the output file "
                    "was not found."
                )


                download_progress[
                    "status"
                ] = "Error"


                download_progress[
                    "error"
                ] = error


                return {

                    "success": False,

                    "error": error

                }


            # =============================
            # SUCCESS
            # =============================

            final_filename = (
                os.path.abspath(
                    final_filename
                )
            )


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


            print("=" * 60)

            print(
                "Download completed successfully."
            )

            print(
                f"File: {final_filename}"
            )

            print("=" * 60)


            return {

                "success": True,

                "title": title,

                "filename": os.path.basename(
                    final_filename
                ),

                "path": final_filename,

            }


    # =====================================
    # ERROR HANDLING
    # =====================================

    except Exception as e:

        error = str(e)


        print("=" * 60)

        print(
            "DOWNLOAD ERROR:"
        )

        print(error)

        print("=" * 60)


        download_progress[
            "status"
        ] = "Error"


        download_progress[
            "error"
        ] = error


        download_progress[
            "completed"
        ] = False


        return {

            "success": False,

            "error": error

        }
