import argparse
import ssl
from pytubefix import YouTube, Playlist
from pytubefix.exceptions import AgeRestrictedError
import re
import os
import logging
import subprocess

# 設置基本的日誌配置
logging.basicConfig(
    level=logging.INFO,  # 設置日誌等級
    format="%(asctime)s - %(levelname)s - %(message)s",  # 設置日誌格式
    handlers=[
        logging.FileHandler("youtube_downloader.log"),  # 日誌輸出到文件
        logging.StreamHandler(),  # 同時輸出到控制台
    ],
)

current_directory = os.getcwd()  # 獲取當前工作目錄
ssl._create_default_https_context = ssl._create_stdlib_context  # fix ssl error
save_directory = current_directory + "/save"
# create default save directory
if not os.path.exists(save_directory):
    os.makedirs(save_directory)


def clean_filename(filename: str) -> str:
    """
    Clean the file name to ensure it conforms
    to file path naming conventions.

    Args:
        filename (str): original file name.

    Returns:
        str: Cleaned file name.
    """
    cleaned_filename = re.sub(r'[\/:*?"<>|]', "_", filename)
    return cleaned_filename


def onProgress(stream, chunk, remains):
    total = stream.filesize  # get full-size
    percent = (total - remains) / total * 100
    logging.info(f"Downloading… {percent:05.2f}%")


def merge_video_audio(video_path: str, audio_path: str, output_path: str):
    try:
        logging.info(f"Starting merge for {video_path} and {audio_path}.")
        subprocess.run(
            ["ffmpeg", "-i", video_path, "-i", audio_path, "-c", "copy", output_path],
            check=True,
        )
        os.remove(video_path)
        os.remove(audio_path)
        logging.info(f"Merge completed successfully for {output_path}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Merge failed: {e}")
        logging.error(f"Command output: {e.output}")
    except Exception as e:
        logging.critical(f"Unexpected error during merge: {e}")


def download_stream(stream, filename, output_path):
    try:
        logging.info(f"Starting download for {filename}.")
        stream.download(filename=filename, output_path=output_path)
        logging.info(f"Download completed for {filename}.")
    except Exception as e:
        logging.error(f"Failed to download {filename}: {e}")


def toMp4(yt: YouTube, output_path: str, resolution: str = None):
    logging.info(f"{yt.title} download start")
    video_filename = clean_filename(yt.title) + "_video.mp4"
    audio_filename = clean_filename(yt.title) + "_audio.mp4"
    output_filename = clean_filename(yt.title) + ".mp4"

    try:
        if resolution:
            video = yt.streams.filter(res=resolution, mime_type="video/mp4").first()
            if video is None:
                raise ValueError(f"Resolution {resolution} is not available.")
            download_stream(video, video_filename, output_path)
        else:
            video = (
                yt.streams.filter(mime_type="video/mp4")
                .order_by("resolution")
                .desc()
                .first()
            )
            download_stream(video, video_filename, output_path)

        audio = yt.streams.filter(only_audio=True, mime_type="audio/mp4").first()
        if audio is None:
            logging.error(f"No audio stream available for {yt.title}.")
            return
        download_stream(audio, audio_filename, output_path)

        merge_video_audio(
            os.path.join(output_path, video_filename),
            os.path.join(output_path, audio_filename),
            os.path.join(output_path, output_filename),
        )
    except AgeRestrictedError as e:
        logging.error(
            f"Cannot download {yt.title}: {e}. Please use argument --oauth to login with browser."
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def toMp3(yt: YouTube, output_path: str):
    logging.info(f"{yt.title} download start")
    audio = yt.streams.filter(only_audio=True).first()
    if audio is None:
        logging.error(f"No audio stream available for {yt.title}.")
        return
    download_stream(audio, clean_filename(yt.title) + ".mp3", output_path)


def information(yt: YouTube):
    logging.info(f"Title: {yt.title}")
    logging.info(f"Length: {yt.length} seconds")
    logging.info(f"Views: {yt.views}")
    logging.info(f"Author: {yt.author}")
    logging.info(f"Publish date: {yt.publish_date}")
    logging.info("\nAvailable streams:")
    for stream in yt.streams:
        logging.info(stream)
    logging.info("\n")


def run(
    link: str,
    format: str = ".mp4",
    output_path: str = save_directory,
    info: bool = False,
    resolution: str = None,
    oauth: bool = False,
):
    playlist = []
    if "playlist?" in link:  # check if the link is a playlist link
        playlist = Playlist(link).video_urls
    else:
        playlist.append(link)

    for songlink in playlist:
        yt = YouTube(
            songlink,
            on_progress_callback=onProgress,
            use_oauth=oauth,
            allow_oauth_cache=oauth,
        )
        if info:
            information(yt)
        if format.lower() == ".mp3":
            toMp3(yt, output_path)
        elif format.lower() == ".mp4":
            toMp4(yt, output_path, resolution)


def parse_opt():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--link", type=str, required=True, help="YouTube video link")
    parser.add_argument("--format", default=".mp4", help=".mp4 or .mp3")
    parser.add_argument(
        "--output_path",
        default=save_directory,
        help="Specifies the path where you want to save files.",
    )
    parser.add_argument(
        "--info", default=False, action="store_true", help="Show video information"
    )
    parser.add_argument(
        "--resolution",
        default=None,
        help="Specifies the resolution of the video you want to download. '720p' or '1080p' etc.",
    )
    parser.add_argument(
        "--oauth", default=False, action="store_true", help="Log in Youtube with OAuth"
    )

    return parser.parse_args()


def main(opt):
    """Main function."""
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
