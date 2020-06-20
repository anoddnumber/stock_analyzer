#!/usr/bin/env bash

echo "Converting mp4 files into mov files"
# Converts all .mp4 files in the current directory into .mov files then deletes all .mp4 files.

for file in *.mp4
do
  ffmpeg -i "$file" -acodec copy -vcodec copy -f mov "${file%.mp4}.mov"
done

echo "Deleting mp4 files"
rm *.mp4

echo "CONVERSION COMPLETE"