import asyncio
import multiprocessing
import shlex
import re
import subprocess
import time
from urllib.parse import urlparse, parse_qs, urljoin

import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

import requests
from bs4 import BeautifulSoup


from playwright.sync_api import sync_playwright


import configparser

config = configparser.ConfigParser()
config.read('config.txt')
output_base_dir = config['DEFAULT'].get('out_base_dir', None)
output_base_dir = output_base_dir.replace('"', "")
print(f"{output_base_dir=}  - {output_base_dir[-1]}")


AUDIO_TYPE = config['DEFAULT'].get('audio_type', None)
AUDIO_TYPE = AUDIO_TYPE.replace('"', "")
# AUDIO_TYPE = ".flac"




def download(url, folder, artist):
    url = url.strip()

    command = [
        "yt-dlp",
        "--verbose",
        "--extract-audio",
        "--audio-format", "flac",
        "--no-playlist",
        "-o", os.path.expanduser(f"{output_base_dir}/{folder}/%(title)s.%(ext)s"),
        url
    ]

    try:
        proc = subprocess.run(command)
        print(f"Downloaded {url} successfully!")
    except Exception as err:

        print(f"\n\n\n\n\nFailed to download {url}: {err} \n\n\n\n\n\n")
        return



    # stdout, stderr = proc.communicate()

    # print(f"{proc.returncode=} - {str(stderr)}")

    if proc.returncode == 0 or proc.returncode == 1:
        print(f"Downloaded {url} to {output_base_dir}/{folder}")

    else:
        print(f"Failed Download: {url} to {output_base_dir}/{folder}")


def scrape_with_playwright(url, domain_filter):
    all_links = set()

    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Open the target URL
        print("Scraping url: ", url)
        page.goto(url)

        # Wait for network to be idle to make sure all dynamic content is loaded
        page.wait_for_load_state('networkidle')

        # print("Sleeping for 5s")
        # time.sleep(100)

        # Get the complete HTML after rendering
        # html_content = page.content()
        # soup = BeautifulSoup(html_content, "html.parser")
        # print(soup.prettify())

        # Extract all links from the rendered page
        a_tags = page.query_selector_all("a")
        for a_tag in a_tags:
            href = a_tag.get_attribute("href")
            print("Found tags: ", href)

            if href:
                absolute_url = urljoin(url, href)
                parsed_url = urlparse(absolute_url)

                if domain_filter in parsed_url.netloc:
                    all_links.add(absolute_url)

        browser.close()

    return list(all_links)



def filter_vid_urls(playlist_re, url):
    match = playlist_re.match(url)

    if match:
        return url
    return None

def add_metadata(output_base_dir, folder_name, artist, album_name):
    download_dir = f"{output_base_dir}/{folder_name}"
    try:
        print("Updating MD in: ", download_dir)
        for file_name in os.listdir(download_dir):
            if file_name.endswith(AUDIO_TYPE):
                file_path = os.path.join(download_dir, file_name)

                # Modify the metadata here
                title = file_name.replace(AUDIO_TYPE, "")
                artist = artist  # You can enhance this by parsing the title or using YouTube metadata
                album = album_name  # Using the folder name as the album name

                if file_path.endswith(".mp3"):
                    audio = MP3(file_path, ID3=EasyID3)
                    audio["title"] = title
                    audio["artist"] = artist
                    audio["album"] = album
                    audio.save()
                    print(f"Metadata added successfully for MP3: {file_path}")

                elif file_path.endswith(".flac"):
                    audio = FLAC(file_path)
                    audio["title"] = [title]
                    audio["artist"] = [artist]
                    audio["album"] = [album]
                    audio.save()
                    print(f"Metadata added successfully for FLAC: {file_path}")

                else:
                    print(f"Unsupported file type for metadata: {file_path}")

    except Exception as e:
        print(f"Error adding metadata to {download_dir}: {e}")



def download_videos_parallel(video_data):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.starmap(download, video_data)  # Use map instead of starmap

def extract_playlist_info(playlist):
    album_name = playlist[0].replace("\n", "").strip() if len(playlist) >= 0 else ""
    artist = playlist[1].replace("\n", "").strip() if len(playlist) >= 0 else ""
    target_url = playlist[2]
    list_name = parse_qs(urlparse(target_url).query)["list"][0] if len(playlist) >= 0 else ""

    folder_name  = f"{artist} - {album_name}".strip()
    print(f"{folder_name=}")
    print(f"{artist=}")
    print(f"{list_name=}")
    return folder_name, target_url, list_name, artist, album_name

def get_videos(target_url, list_name):
    links = scrape_with_playwright(target_url, urlparse(target_url).netloc)

    playlist_re = re.compile(rf'https:\/\/www\.youtube\.com\/watch\?v=[^&]+&list={list_name}+&index=\d+')
    _vids = {link:1 for link in links if filter_vid_urls(playlist_re, link)}
    return _vids.keys()

def main():
    playlists = []
    with open("./folder.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            playlist_info = line.split(",")
            playlists.append(playlist_info)

    for playlist in playlists:
        folder_name, target_url, list_name, artist, album_name = extract_playlist_info(playlist)

        vids = get_videos(target_url, list_name)
        print(f"Downlading {(len(vids))} vids to {folder_name=}")

        try:
            download_videos_parallel([(url, folder_name, artist,) for url in vids])
        except Exception as err:
            print(f"Err in main: {err}")

        try:
            add_metadata(output_base_dir, folder_name, artist, album_name)
            # download_dir = f"{output_base_dir}/{folder_name}"
            # print("Updating MD in: ", download_dir)
            # for file_name in os.listdir(download_dir):
            #     if file_name.endswith(AUDIO_TYPE):
            #         file_path = os.path.join(download_dir, file_name)

            #         # Modify the metadata here
            #         title = file_name.replace(AUDIO_TYPE, "")
            #         artist = artist  # You can enhance this by parsing the title or using YouTube metadata
            #         album = album_name  # Using the folder name as the album name

                    # add_metadata(output_base_dir, folder_name)

        except Exception as err:
            print("Error adding MD: ", err)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Err in Program: {err=}")