import argparse
import ssl
from pytubefix import YouTube
from pytubefix import Playlist
import re
import os


current_directory = os.getcwd()  # 獲取當前工作目錄
ssl._create_default_https_context = ssl._create_stdlib_context  # fix ssl error


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
    # subtract the remaining size
    # (the remaining size will capture the accessed file size)
    percent = (total - remains) / total * 100
    # show progress, \r means no line break, update on the same line
    print(f"Downloading… {percent:05.2f}", end="\r")


def toMp3(yt: YouTube, output_path: str):

    print(yt.title + "\tdownload start")
    # get audio and save to .mp3
    yt.streams.filter().get_audio_only().download(
        filename=clean_filename(yt.title) + ".mp3", output_path=output_path
    )
    print()
    print("OK")


def toMp4(yt: YouTube, output_path: str, resolution: str = None):
    print(yt.title + "\tdownload start")

    if resolution:
        # get video with specified resolution and save to .mp4
        try:
            yt.streams.filter(res=resolution).first().download(
                filename=clean_filename(yt.title) + ".mp4", output_path=output_path
            )
        except Exception:
            print(
                f"Resolution {resolution} is not available, download the highest resolution."
            )
            yt.streams.filter().order_by("resolution")[-1].download(
                filename=clean_filename(yt.title) + ".mp4", output_path=output_path
            )
    else:
        # get HIGHEST resolution video and save to .mp4
        # BUG: yt.streams.filter().get_highest_resolution().download(
        #     filename=clean_filename(yt.title) + ".mp4", output_path=output_path
        # )
        yt.streams.filter().order_by("resolution")[-1].download(
            filename=clean_filename(yt.title) + ".mp4", output_path=output_path
        )
    print()
    print("OK")


def information(yt: YouTube):
    print(yt.title)
    print(yt.streams)
    print()


def run(
    link: str,
    format: str = ".mp4",
    output_path: str = current_directory,
    info: bool = False,
    resolution: str = None,
    oauth: bool = False,
):
    playlist = []
    if "playlist?" in link:  # check link is or not playlist link
        playlist = Playlist(link).video_urls
    else:
        playlist.append(link)

    if format.lower() == ".mp3":
        for songlink in playlist:
            yt = YouTube(
                songlink,
                on_progress_callback=onProgress,
                use_oauth=oauth,
                allow_oauth_cache=oauth,
            )
            if info:
                information(yt)
            toMp3(yt, output_path)
    if format.lower() == ".mp4":
        for songlink in playlist:
            yt = YouTube(
                songlink,
                on_progress_callback=onProgress,
                use_oauth=oauth,
                allow_oauth_cache=oauth,
            )
            if info:
                information(yt)
            toMp4(yt, output_path, resolution)


def parse_opt():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--link", type=str, required=True, help="Youtube video link")
    parser.add_argument("--format", default=".mp4", help=".mp4 or .mp3")
    parser.add_argument(
        "--output_path",
        default=None,
        help="Specifies the path where you want to save files.",
    )
    parser.add_argument("--info", default=False, help="Show video information")
    parser.add_argument(
        "--resolution",
        default=None,
        help="Specifies the resolution of the video you want to download. '720p' or '1080p' etc.",
    )
    parser.add_argument("--oauth", default=False, action="store_true", help="Use OAuth")

    return parser.parse_args()


def main(opt):
    """Main function."""
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
