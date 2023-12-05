# YouTube-Downloader
An easy downloader that can save the video to .mp3 or .mp4


## Install the Required Libraries

Clone the repository, and install the library.

```bash
# Clone this downloader 
git clone https://github.com/Mumao0526/YouTube-Downloader.git

# install pytube
pip install pytube
```

## Usage Options

- `--link`: Specifies the link to the video from YouTube you want to download.
- `--format`: Select '.mp4' or '.mp3', it's default '.mp4'.
- `--output_path`: Specifies the path where you want to save files.

### Example

```bash
# If you want to save a video
python downloader.py --link "https://youtu.be/yAOU9Yi40EQ?si=6Y9eCGAl9ikMFPzu"

# If you want to save to .mp3
python downloader.py --link "https://youtu.be/yAOU9Yi40EQ?si=6Y9eCGAl9ikMFPzu" --format ".mp3"

# If you want to save to your path
python downloader.py --link "https://youtu.be/yAOU9Yi40EQ?si=6Y9eCGAl9ikMFPzu" --output_path "./path"

# If you want to save a video from playlist
python downloader.py --link "https://youtube.com/playlist?list=PLM1j2JqVBQflDBzTRe35HAuJRON-WgnN7&si=R7At42KJaVQg2JCG"
```
