import asyncio
import shlex
import re
from urllib.parse import urlparse, parse_qs





async def download(url, folder):
    url = url.strip()
    cmd = f"bash ./dl.sh {shlex.quote(url)} {shlex.quote(folder)}"

    # print(f"Python {cmd=}")

    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate()  # ?

    print(f"{proc.returncode=} - {str(stderr)}")

    if proc.returncode == 0:
        print(f"Downloaded {url} to ~/Music/yt_dl/{folder}")
    else:
        print(f"Failed Download: {url} to ~/Music/yt_dl/{folder}")



def filter_vid_urls(playlist_re, url):
    match = playlist_re.match(url)

    if match:
        return url
    return None


def extract_list_name(url):
    s = url

    return s

async def main():

    with open("./folder.txt", 'r', encoding='utf-8') as f:
        folder = f.readlines()

    folder_name = folder[0].replace("\n", "") if len(folder) >= 0 else ""
    list_name = parse_qs(urlparse(folder[1]).query)["list"][0] if len(folder) >= 0 else ""

    print(f"{folder_name=}")
    print(f"{list_name=}")

    playlist_re = re.compile(rf'https:\/\/www\.youtube\.com\/watch\?v=[^&]+&list={list_name}+&index=\d+')


    with open("./video.txt", 'r', encoding='utf-8') as f:
        _vids = {line:1 for line in f.readlines() if filter_vid_urls(playlist_re, line)}
        vids = _vids.keys()

    # print(f"Downlading in {folder_name=} | {vids=}")
    # [print(v) for v in vids]

    await asyncio.gather(*[download(url, folder_name) for url in vids])



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as err:
        print(f"Err in main: {err=}")