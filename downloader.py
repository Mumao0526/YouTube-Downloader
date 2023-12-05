import argparse
import ssl
from pytube import YouTube
from pytube import Playlist

ssl._create_default_https_context = ssl._create_stdlib_context


def onProgress(stream, chunk, remains):
    total = stream.filesize  # 取得完整尺寸
    percent = (total - remains) / total * 100  # 減去剩餘尺寸 ( 剩餘尺寸會抓取存取的檔案大小 )
    print(f"下載中… {percent:05.2f}", end="\r")  # 顯示進度，\r 表示不換行，在同一行更新


def toMp3(path: str, output_path: str = "."):
    yt = YouTube(path, on_progress_callback=onProgress)

    print(yt.title + "\tdownload...")
    # get audio and save to .mp3
    yt.streams.filter().get_audio_only().download(
        filename=yt.title + ".mp3", output_path=output_path
    )
    print()
    print("OK")


def toMp4(path: str, output_path: str = "."):
    yt = YouTube(path, on_progress_callback=onProgress)

    print(yt.title + "\tdownload...")
    # get HIGHEST resolution video and save to .mp4
    yt.streams.filter().get_highest_resolution().download(
        filename=yt.title + ".mp4", output_path=output_path
    )
    print()
    print("OK")


def run(link: str, format: str = ".mp4", output_path: str = "."):
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
    parser.add_argument("--link", type=str, required=True, help="Youtube video link")
    parser.add_argument("--format", default=".mp4", help=".mp4 or .mp3")
    parser.add_argument(
        "--output_path", default=".", help="Specifies the path where you want to save files."
    )
    return parser.parse_args()


def main(opt):
    """Main function."""
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
