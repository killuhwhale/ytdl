import asyncio
import subprocess
import re



playlist_re = re.compile(r'https:\/\/www\.youtube\.com\/watch\?v=[^&]+&list=[^&]+&index=\d+')

async def download(url):
    url = url.strip()
    proc = await asyncio.create_subprocess_shell(
        f"bash ./dl.sh {url}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate()  # ?

    if proc.returncode == 0:
        print(f"Downloaded {url} to ~/Music/yt_dl")
    else:
        print(f"Failed Download: {url}")


def filter_vid_urls(url):
    match = playlist_re.match(url)

    if match:
        print("f{match.group=}")
        return url
    return None

async def main():
    vids = []
    print("Opening video.txt")
    with open("./video.txt", 'r', encoding='utf-8') as f:
        vids = [line for line in f.readlines() if filter_vid_urls(line)]

    print(f"Downlading {vids=}")
    await asyncio.gather(*[download(url) for url in vids])



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as err:
        print(f"Err in main: {err=}")