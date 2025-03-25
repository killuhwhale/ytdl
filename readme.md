#Global config
/etc/youtube-dl.conf // OLD , might be true


# Install
python3 -m pip install -U "yt-dlp[default]"

# Link Klipper
https://chromewebstore.google.com/detail/link-klipper-extract-all/fahollcgofmpnehocdgofnhkkchiekoo/reviews?hl=en

# Call and DOnwload audio
yt-dlp --verbose --extract-audio --audio-format 'mp3'  -o '~/Music/yt_dl/%(title)s%(ext)s' $1