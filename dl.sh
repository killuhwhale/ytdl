#! /bin/sh

# bash dl.sh video_url folder_name

echo "Downloading {$1} to {$2}"

if [ -z "$2" ]; then
  # No second argument provided
  yt-dlp --verbose --extract-audio --audio-format 'mp3' -o '~/Music/yt_dl/%(title)s.%(ext)s' "$1"
else
  # Second argument is provided, use it as a subdirectory
  yt-dlp --verbose --extract-audio --audio-format 'mp3' -o "~/Music/yt_dl/$2/%(title)s.%(ext)s" "$1"
fi