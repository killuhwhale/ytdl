#! /usr/bin/env bash

yt-dlp --verbose --extract-audio --audio-format 'mp3' -o '~/Music/yt_dl/%(title)s.%(ext)s' "$1"