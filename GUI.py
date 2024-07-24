import ssl
import re
import os
from pytubefix import YouTube, Playlist
import tkinter as tk
from tkinter import filedialog, messagebox

current_directory = os.getcwd()  # 獲取當前工作目錄
ssl._create_default_https_context = ssl._create_stdlib_context  # fix ssl error


def clean_filename(filename: str) -> str:
    cleaned_filename = re.sub(r'[\/:*?"<>|]', "_", filename)
    return cleaned_filename


def onProgress(stream, chunk, remains):
    total = stream.filesize
    percent = (total - remains) / total * 100
    progress_var.set(f"Downloading… {percent:05.2f}%")
    progress_label.update_idletasks()


def toMp3(yt: YouTube, output_path: str):
    print(yt.title + "\tdownload start")
    yt.streams.filter().get_audio_only().download(
        filename=clean_filename(yt.title) + ".mp3", output_path=output_path
    )
    print()
    print("OK")


def toMp4(yt: YouTube, output_path: str, resolution: str = None):
    print(yt.title + "\tdownload start")
    if resolution:
        try:
            yt.streams.filter(res=resolution).first().download(
                filename=clean_filename(yt.title) + ".mp4", output_path=output_path
            )
        except Exception:
            print(f"Resolution {resolution} is not available, download the highest resolution.")
            yt.streams.filter().order_by("resolution")[-1].download(
                filename=clean_filename(yt.title) + ".mp4", output_path=output_path
            )
    else:
        yt.streams.filter().order_by("resolution")[-1].download(
            filename=clean_filename(yt.title) + ".mp4", output_path=output_path
        )
    print()
    print("OK")


def information(yt: YouTube):
    print(yt.title)
    print(yt.streams)
    print()


def run(link: str, format: str = ".mp4", output_path: str = current_directory, info: bool = False, resolution: str = None, oauth: bool = False):
    playlist = []
    if "playlist?" in link:
        playlist = Playlist(link).video_urls
    else:
        playlist.append(link)

    if format.lower() == ".mp3":
        for songlink in playlist:
            yt = YouTube(songlink, on_progress_callback=onProgress, use_oauth=oauth, allow_oauth_cache=oauth)
            if info:
                information(yt)
            toMp3(yt, output_path)
    if format.lower() == ".mp4":
        for songlink in playlist:
            yt = YouTube(songlink, on_progress_callback=onProgress, use_oauth=oauth, allow_oauth_cache=oauth)
            if info:
                information(yt)
            toMp4(yt, output_path, resolution)


def browse_output_path(entry):
    path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, path)


def download():
    link = link_entry.get()
    format = format_var.get()
    output_path = output_path_entry.get()
    info = info_var.get()
    resolution = resolution_entry.get()
    oauth = oauth_var.get()

    if not link:
        messagebox.showerror("Error", "Link is required")
        return

    run(link, format, output_path, info, resolution, oauth)
    messagebox.showinfo("Success", "Download completed")
    progress_var.set("")


# 建立主窗口
root = tk.Tk()
root.title("YouTube Downloader")

# 建立並放置GUI元件
tk.Label(root, text="YouTube Link:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
link_entry = tk.Entry(root, width=50)
link_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Format:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
format_var = tk.StringVar(value=".mp4")
tk.Radiobutton(root, text=".mp4", variable=format_var, value=".mp4").grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
tk.Radiobutton(root, text=".mp3", variable=format_var, value=".mp3").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

tk.Label(root, text="Output Path:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
output_path_entry = tk.Entry(root, width=50)
output_path_entry.grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=lambda: browse_output_path(output_path_entry)).grid(row=2, column=2, padx=5, pady=5)

tk.Label(root, text="Resolution:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
resolution_entry = tk.Entry(root, width=20)
resolution_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

info_var = tk.BooleanVar()
tk.Checkbutton(root, text="Show Info", variable=info_var).grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

oauth_var = tk.BooleanVar()
tk.Checkbutton(root, text="Use OAuth", variable=oauth_var).grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

tk.Button(root, text="Download", command=download).grid(row=5, column=0, columnspan=3, padx=5, pady=10)

progress_var = tk.StringVar()
progress_label = tk.Label(root, textvariable=progress_var)
progress_label.grid(row=6, column=0, columnspan=3, padx=5, pady=10)

root.mainloop()
