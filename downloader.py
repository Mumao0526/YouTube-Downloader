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


def toMp3(path: str, output_path: str):
    yt = YouTube(path, on_progress_callback=onProgress)

    print(yt.title + "\tdownload start")
    # get audio and save to .mp3
    yt.streams.filter().get_audio_only().download(
        filename=clean_filename(yt.title) + ".mp3", output_path=output_path
    )
    print()
    print("OK")


def toMp4(path: str, output_path: str):
    yt = YouTube(path, on_progress_callback=onProgress)

    print(yt.title + "\tdownload start")
    # get HIGHEST resolution video and save to .mp4
    yt.streams.filter().get_highest_resolution().download(
        filename=clean_filename(yt.title) + ".mp4", output_path=output_path
    )
    print()
    print("OK")


def run(link: str, format: str = ".mp4", output_path: str = current_directory):
    playlist = []
    if "playlist?" in link:  # check link is or not playlist link
        playlist = Playlist(link).video_urls
    else:
        playlist.append(link)

    if format.lower() == ".mp3":
        for songlink in playlist:
            toMp3(songlink, output_path)
    if format.lower() == ".mp4":
        for songlink in playlist:
            toMp4(songlink, output_path)


def parse_opt():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--link", type=str, required=True,
                        help="Youtube video link")
    parser.add_argument("--format", default=".mp4", help=".mp4 or .mp3")
    parser.add_argument(
        "--output_path",
        default=None,
        help="Specifies the path where you want to save files.",
    )
    return parser.parse_args()


def main(opt):
    """Main function."""
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
