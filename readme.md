<!-- https://github.com/killuhwhale/ytdl -->


# Single run
yt-dlp --verbose --extract-audio --audio-format 'mp3' -o '~/Music/yt_dl/%(title)s.%(ext)s' URL_HERE

## Example
yt-dlp --verbose --extract-audio --audio-format 'mp3' -o '~/Music/yt_dl/%(title)s.%(ext)s' https://www.youtube.com/watch?v=LQj--Kjn0z8

# Install
python3 -m venv .

source bin/activate

python3 -m pip install -U "yt-dlp[default]"

# Setup
** Run Extension Link Klipper and copy links to video.txt **

# Run
run: python3 main.py


# Results store in
~/Music/yt_dl

# Link Klipper
https://chromewebstore.google.com/detail/link-klipper-extract-all/fahollcgofmpnehocdgofnhkkchiekoo/reviews?hl=en

# Call and Download audio
yt-dlp --verbose --extract-audio --audio-format 'mp3'  -o '~/Music/yt_dl/%(title)s%(ext)s' $1
