from pathlib import Path

# === CONFIGURATION ===
# BASE_DIR = Path(r"E:\series")  # folder with tv series
BASE_DIR = Path(r"E:\loop ready")  # folder with tv series
VLC_PATH = r"C:\Program1\VLC\vlc.exe"
NUM_EPISODES = 5                 # Total number of episodes to pick
CREATE_PLAYLIST_FILE = True      # Save to XSPF file
PLAYLIST_FILENAME = str(Path.home() / "random_episodes.xspf")
OPEN_IN_VLC = True               # Automatically open in VLC
CLOSE_EXISTING_VLC = True        # Set to False to disable auto-closing

# Supported video file extensions
VIDEO_EXTENSIONS = {".mkv", ".avi", ".mp4", ".mov", ".flv"}
