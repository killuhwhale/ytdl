#!/usr/bin/env bash

# Get the directory of the script (to properly reference config.txt)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "${SCRIPT_DIR}/config.txt"

# Read config file
if [ -f "${SCRIPT_DIR}/config.txt" ]; then
    source "${SCRIPT_DIR}/config.txt"
else
    echo "Config file not found. Exiting..."
    exit 1
fi

# Check if out_base_dir is defined
if [ -z "$out_base_dir" ]; then
    echo "out_base_dir is not defined in config.txt. Exiting..."
    exit 1
fi

# Print the directory being used
echo "Using output directory: $out_base_dir"

# Run yt-dlp with the specified output directory
yt-dlp --verbose  --extract-audio --audio-format  'flac' -o "${out_base_dir}/%(title)s.%(ext)s" "$1"
