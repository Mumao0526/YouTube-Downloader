# YouTube-Downloader

An easy-to-use YouTube downloader using `yt-dlp`, which supports downloading videos and audio in `.mp4` or `.mp3`, subtitle extraction, and playlist downloads.

---

## ✅ Installation

Clone the repository and install the required libraries.

```bash
# Clone this downloader
git clone https://github.com/Mumao0526/YouTube-Downloader.git

# Enter the directory
cd YouTube-Downloader

# Install required packages
pip install yt-dlp customtkinter
```

---

## 🚀 Usage Options

This script can be run using either:

```bash
python3 downloader.py <video_or_playlist_url> [options]
```

or

```bash
python3 downloader.py --link <video_or_playlist_url> [options]
```

### Available Options

| Option                | Description                                                                     |
| --------------------- | ------------------------------------------------------------------------------- |
| `link` / positional   | YouTube video or playlist URL (either as `--link` or directly as a parameter)  |
| `--format`            | `.mp4` (default) or `.mp3`                                                      |
| `--output_path`       | Target directory to save the file (default: `./save/`)                         |
| `--resolution`        | Max video resolution (e.g., `720p`)                                            |
| `--name`              | Custom filename for single video (no effect on playlist)                       |
| `--info`              | Show video information only, without downloading                               |
| `--sub-only`          | Only download subtitles (no audio/video)                                       |
| `--sub-lang`          | Subtitle language code (e.g., `en`, `zh-Hant`) (default: `en`)                 |

---

## 📦 Examples

### 🎬 Download as `.mp4` (default)

```bash
python3 downloader.py https://youtu.be/yAOU9Yi40EQ
```

### 🎵 Download audio as `.mp3`

```bash
python3 downloader.py https://youtu.be/yAOU9Yi40EQ --format .mp3
```

### 📂 Specify a custom output path

```bash
python3 downloader.py https://youtu.be/yAOU9Yi40EQ --output_path ./my_music
```

### 🎞️ Download a full playlist (saved into `./save/<PlaylistTitle>/`)

```bash
python3 downloader.py "https://youtube.com/playlist?list=PLM1j2JqVBQflDBzTRe35HAuJRON-WgnN7"
```

### 🔤 Download subtitles only (e.g. English)

```bash
python3 downloader.py https://youtu.be/yAOU9Yi40EQ --sub-only --sub-lang en
```

---

## 🖼️ GUI Version

If you prefer a graphical interface, launch the GUI with:

```bash
python3 downloader_gui.py
```

### Features:
- Auto-detects video information (title, available resolutions, and subtitles)
- Allows format selection: `.mp4`, `.mp3`, or **subtitles only**
- Resolution dropdown will be populated after fetching video info
- Subtitle language selection
- Output path selection with file browser
- Real-time status messages and error handling

> 💡 Ideal for users who prefer not to use the command line.

---

## ℹ️ Notes

- You can use either `--link <URL>` or pass the YouTube URL directly without any flags.
- The default save directory is `./save/`, and it will be automatically created.
- Playlist downloads are saved in a subdirectory named after the playlist title.
- Subtitles will be saved as `.vtt` format.

---

## ⚠️ Disclaimer

This script is intended for **personal and educational use only**.  
Please ensure you have the right to download content from YouTube under YouTube's [Terms of Service](https://www.youtube.com/t/terms).