#!/usr/bin/env bash
# Some reason the downloaded video will have a 10 second delay or so from the start time..

url=$1

original_title="$(yt-dlp --print filename -o "%(title)s" "$url")"
original_output_name="$(yt-dlp --print filename -o "%(title)s.%(ext)s" "$url")"
final_output_name="${original_title}"

# replace all forward slashes with an underscore, otherwise ffmpeg will treat it as a path
valid_name=$(echo ${original_output_name} | tr / _)

if [[ ! -f "${valid_name}" ]]
then
  echo 'downloading!'
  # downloads the .webm version of the file
  yt-dlp -x --audio-format mp3 "$url" -o "${valid_name}"
fi