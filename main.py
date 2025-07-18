import os
import random
import xml.etree.ElementTree as ET
from pathlib import Path
import subprocess
import argparse

# Import config
import config


def find_tv_shows(base_path):
	shows = {}
	for show_dir in base_path.iterdir():
		if show_dir.is_dir():
			episodes = []
			for root, dirs, files in os.walk(show_dir):
				for f in files:
					file_path = Path(f)
					if file_path.suffix.lower() in config.VIDEO_EXTENSIONS and "sample" not in file_path.name.lower():
						episodes.append(Path(root) / f)
			if episodes:
				shows[show_dir.name] = episodes
	return shows


def pick_random_episodes(shows, count):
	chosen = []
	show_names = list(shows.keys())
	while len(chosen) < count and show_names:
		show = random.choice(show_names)
		if shows[show]:
			episode = random.choice(shows[show])
			chosen.append(episode)
			shows[show].remove(episode)
		else:
			show_names.remove(show)
	return chosen


def create_xspf_playlist(files, output_path):
	ET.register_namespace('', "http://xspf.org/ns/0/")
	playlist = ET.Element("playlist", version="1", xmlns="http://xspf.org/ns/0/")
	tracklist = ET.SubElement(playlist, "trackList")

	for f in files:
		track = ET.SubElement(tracklist, "track")
		ET.SubElement(track, "location").text = f"file:///{f.resolve().as_posix()}"

	tree = ET.ElementTree(playlist)
	tree.write(output_path, encoding="utf-8", xml_declaration=True)
	print(f"Playlist saved to {output_path}")


def launch_vlc_playlist_file():
	subprocess.run([config.VLC_PATH, config.PLAYLIST_FILENAME])


def main():
	# Parse CLI arguments
	parser = argparse.ArgumentParser(description="Pick random episodes from TV shows.")
	parser.add_argument("count", nargs="?", type=int, default=config.NUM_EPISODES,
						help="Number of random episodes to pick (default from config)")
	args = parser.parse_args()

	print(f"Selecting {args.count} random episode(s)...")

	shows = find_tv_shows(config.BASE_DIR)
	if not shows:
		print("No TV shows found.")
		return

	selected = pick_random_episodes(shows, args.count)
	if not selected:
		print("No episodes found to select.")
		return

	for ep in selected:
		print("Selected:", ep)

	if config.CREATE_PLAYLIST_FILE:
		create_xspf_playlist(selected, Path(config.PLAYLIST_FILENAME))

	if config.OPEN_IN_VLC:
		launch_vlc_playlist_file()


if __name__ == "__main__":
	main()
