import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

import configparser

config = configparser.ConfigParser()
config.read('config.txt')

AUDIO_TYPE = config['DEFAULT'].get('audio_type', None)
AUDIO_TYPE = AUDIO_TYPE.replace('"', "")



def add_metadata(directory, artist_name, album_name):
    if not os.path.isdir(directory):
        print(f"Directory '{directory}' not found.")
        return

    mp3_files = [f for f in os.listdir(directory) if f.endswith(AUDIO_TYPE)]

    if not mp3_files:
        print(f"No {AUDIO_TYPE} files found in '{directory}'.")
        return

    for file_name in mp3_files:
        file_path = os.path.join(directory, file_name)

        try:
            if file_path.endswith(".mp3"):
                audio = MP3(file_path, ID3=EasyID3)
                if "title" not in audio:
                    audio["title"] = file_name.replace(".mp3", "")

                audio["artist"] = artist_name
                audio["album"] = album_name
                audio.save()
                print(f"Metadata added successfully for MP3: {file_path}")

            elif file_path.endswith(".flac"):
                audio = FLAC(file_path)
                if "title" not in audio:
                    audio["title"] = file_name.replace(".flac", "")
                audio["artist"] = [artist_name]
                audio["album"] = [album_name]
                audio.save()
                print(f"Metadata added successfully for FLAC: {file_path}")
                print(f"Updated metadata for: {file_name}")

        except Exception as e:
            print(f"Failed to update {file_name}: {e}")

if __name__ == "__main__":
    # directory = input("Enter the path to the directory containing the .mp3 files: ").strip()
    # artist_name = input("Enter the artist name: ").strip()
    # album_name = input("Enter the album name: ").strip()

    directory = "/media/killuh/Crucial X9/yt_dl/Mac Miller - Macadelic"
    artist_name = "Mac Miller"
    album_name = "Macadelic"

    add_metadata(directory, artist_name, album_name)
