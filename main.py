import asyncio
import shlex
import re



playlist_re = re.compile(r'https:\/\/www\.youtube\.com\/watch\?v=[^&]+&list=[^&]+&index=\d+')

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

    # print(str(stdout))

    if proc.returncode == 0:
        print(f"Downloaded {url} to ~/Music/yt_dl/{folder}")
    else:
        print(f"Failed Download: {url} to ~/Music/yt_dl/{folder}")


def filter_vid_urls(url):
    match = playlist_re.match(url)

    if match:
        return url
    return None

async def main():
    vids = []
    print("Opening video.txt")

    with open("./folder.txt", 'r', encoding='utf-8') as f:
        folder = f.readlines()

    folder_name = folder[0] if len(folder) >= 0 else ""

    with open("./video.txt", 'r', encoding='utf-8') as f:
        _vids = {line:1 for line in f.readlines() if filter_vid_urls(line)}
        vids = _vids.keys()

    print(f"Downlading in {folder_name=} | {vids=}")
    [print(v) for v in vids]
    await asyncio.gather(*[download(url, folder_name) for url in vids])



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as err:
        print(f"Err in main: {err=}")