import customtkinter as ctk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL
import threading
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def fetch_video_info(url):
    ydl_opts = {'quiet': True, 'skip_download': True}
    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)


def populate_options():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL first.")
        return

    def fetch():
        try:
            fetch_button.configure(state="disabled", text="⏳ Fetching...")
            info = fetch_video_info(url)
            resolutions = set()
            subtitle_langs = []

            for f in info.get("formats", []):
                if f.get("ext") == "mp4" and f.get("height"):
                    resolutions.add(f"{f['height']}p")

            if info.get("subtitles"):
                subtitle_langs = list(info["subtitles"].keys())

            resolution_dropdown.configure(values=sorted(resolutions, key=lambda x: int(x[:-1])))
            if resolutions:
                resolution_var.set(sorted(resolutions, key=lambda x: int(x[:-1]))[-1])

            subtitle_dropdown.configure(values=subtitle_langs)
            if "en" in subtitle_langs:
                subtitle_var.set("en")
            elif subtitle_langs:
                subtitle_var.set(subtitle_langs[0])

        except Exception as e:
            messagebox.showerror("Error fetching info", str(e))
        finally:
            fetch_button.configure(state="normal", text="🔍 Fetch Info")

    threading.Thread(target=fetch).start()


def choose_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_path_var.set(folder)


def download_video():
    url = url_entry.get().strip()
    fmt = format_var.get()
    resolution = resolution_var.get()
    sub_only = sub_only_var.get()
    sub_lang = subtitle_var.get()
    output_path = output_path_var.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    if not output_path:
        output_path = os.path.join(os.getcwd(), "save")
        os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': False,
        'noplaylist': False,
    }

    if sub_only:
        ydl_opts.update({
            'writesubtitles': True,
            'skip_download': True,
            'subtitleslangs': [sub_lang],
            'subtitlesformat': 'vtt',
        })
    else:
        if fmt == ".mp3":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }]
            })
        elif fmt == ".mp4":
            if resolution:
                ydl_opts['format'] = f"bestvideo[height<={resolution[:-1]}][ext=mp4]+bestaudio[ext=m4a]/mp4"
            else:
                ydl_opts['format'] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"
            ydl_opts['merge_output_format'] = 'mp4'

    def thread_func():
        try:
            download_button.configure(state="disabled", text="⬇ Downloading...")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Success", "Download completed.")
        except Exception as e:
            messagebox.showerror("Download failed", str(e))
        finally:
            download_button.configure(state="normal", text="⬇ Download")

    threading.Thread(target=thread_func).start()


# === UI 建構 ===
app = ctk.CTk()
app.title("YouTube Downloader (Modern UI)")
app.geometry("700x400")
app.grid_columnconfigure(1, weight=1)

# row 0
ctk.CTkLabel(app, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
url_entry = ctk.CTkEntry(app, placeholder_text="Paste video or playlist link here")
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
fetch_button = ctk.CTkButton(app, text="🔍 Fetch Info", command=populate_options)
fetch_button.grid(row=0, column=2, padx=10, pady=10)

# row 1 - format
ctk.CTkLabel(app, text="Format:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
format_var = ctk.StringVar(value=".mp4")
ctk.CTkOptionMenu(app, variable=format_var, values=[".mp4", ".mp3"]).grid(row=1, column=1, padx=10, pady=5, sticky="w")

# row 2 - resolution
ctk.CTkLabel(app, text="Resolution:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
resolution_var = ctk.StringVar()
resolution_dropdown = ctk.CTkOptionMenu(app, variable=resolution_var, values=[])
resolution_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# row 3 - subtitle
sub_only_var = ctk.BooleanVar()
sub_checkbox = ctk.CTkCheckBox(app, text="Download Subtitles Only", variable=sub_only_var)
sub_checkbox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

ctk.CTkLabel(app, text="Subtitle Language:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
subtitle_var = ctk.StringVar()
subtitle_dropdown = ctk.CTkOptionMenu(app, variable=subtitle_var, values=[])
subtitle_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky="w")

# row 5 - output path
ctk.CTkLabel(app, text="Output Folder:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
output_path_var = ctk.StringVar()
ctk.CTkEntry(app, textvariable=output_path_var).grid(row=5, column=1, padx=10, pady=5, sticky="ew")
ctk.CTkButton(app, text="Browse", command=choose_output_folder).grid(row=5, column=2, padx=10, pady=5)

# row 6 - download
download_button = ctk.CTkButton(app, text="⬇ Download", command=download_video)
download_button.grid(row=6, column=1, padx=10, pady=20)

app.mainloop()
