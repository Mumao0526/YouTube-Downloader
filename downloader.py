import argparse
import os
import re
import logging
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("youtube_downloader.log"),
        logging.StreamHandler(),
    ],
)

# 預設儲存目錄
current_directory = os.getcwd()
save_directory = os.path.join(current_directory, "save")
os.makedirs(save_directory, exist_ok=True)


def clean_filename(filename: str) -> str:
    return re.sub(r'[\/:*?"<>|]', "_", filename)


def is_playlist(url: str) -> bool:
    return "playlist?" in url or "list=" in url


def download_with_ytdlp(
    url: str,
    output_path: str,
    format: str,
    resolution: str = None,
    info: bool = False,
    name: str = None,
    sub_only: bool = False,
    sub_lang: str = "en",
):

    ydl_opts = {
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        "quiet": False,
        "noplaylist": False,
    }

    if name:
        ydl_opts["outtmpl"] = os.path.join(
            output_path, clean_filename(name) + ".%(ext)s"
        )

    if sub_only:
        ydl_opts.update(
            {
                "writesubtitles": True,
                "skip_download": True,
                "subtitleslangs": [sub_lang],
                "subtitlesformat": "vtt",
            }
        )
    else:
        if format == ".mp3":
            ydl_opts.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                        }
                    ],
                }
            )
        elif format == ".mp4":
            if resolution:
                ydl_opts["format"] = (
                    f"bestvideo[height<={resolution[:-1]}][ext=mp4]+bestaudio[ext=m4a]/mp4"
                )
            else:
                ydl_opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"
            ydl_opts["merge_output_format"] = "mp4"

    if info:
        ydl_opts["dump_single_json"] = True
        ydl_opts["simulate"] = True

    if is_playlist(url):
        ydl_opts["outtmpl"] = os.path.join(
            output_path, "%(playlist_title)s", "%(title)s.%(ext)s"
        )
        ydl_opts["quiet"] = True

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            if is_playlist(url):
                with open("playlist_download.log", "a", encoding="utf-8") as log:
                    log.write(f"[{url}]\n")
        logging.info("Task finished.")
    except DownloadError as e:
        logging.error(f"DownloadError: {e}")
    except Exception as e:
        logging.error(f"Download failed: {e}")


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "link", nargs="?", help="YouTube video or playlist link (positional)"
    )
    parser.add_argument("--link", dest="link_flag", help="(Alternative) YouTube link")
    parser.add_argument("--format", default=".mp4", help=".mp4 or .mp3")
    parser.add_argument(
        "--output_path", default=save_directory, help="Save files to this path"
    )
    parser.add_argument(
        "--info", default=False, action="store_true", help="Show video information only"
    )
    parser.add_argument("--resolution", default=None, help="e.g. 720p")
    parser.add_argument(
        "--name", default=None, help="Custom filename (only for single video)"
    )
    parser.add_argument(
        "--sub-only", default=False, action="store_true", help="Only download subtitles"
    )
    parser.add_argument(
        "--sub-lang", default="en", help="Subtitle language code (e.g. en, zh-Hant)"
    )
    return parser, parser.parse_args()


def main():
    parser, opt = parse_opt()

    # 支援 --link 或位置參數
    if not opt.link and opt.link_flag:
        opt.link = opt.link_flag
    elif not opt.link and not opt.link_flag:
        parser.error(
            "You must provide a YouTube link either as a positional argument or with --link"
        )

    download_with_ytdlp(
        url=opt.link,
        output_path=opt.output_path,
        format=opt.format.lower(),
        resolution=opt.resolution,
        info=opt.info,
        name=opt.name,
        sub_only=opt.sub_only,
        sub_lang=opt.sub_lang,
    )


if __name__ == "__main__":
    main()
