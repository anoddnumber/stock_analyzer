#!/usr/bin/env bash
# Some reason the downloaded video will have a 10 second delay or so from the start time..

url=$1
start_time=$2 # format of time should be something like this: 01:22:10 (HH:MM:SS)
end_time=$3

original_title="$(yt-dlp --print filename -o "%(title)s" "$url")"
original_output_name="$(yt-dlp --print filename -o "%(title)s.%(ext)s" "$url")"
final_output_name="${original_title}"

# replace all forward slashes with an underscore, otherwise ffmpeg will treat it as a path
valid_name=$(echo ${original_output_name} | tr / _)

if [[ ! -f "${valid_name}" ]]
then
  echo 'downloading!'
  # downloads the .webm version of the file
  yt-dlp "$url" -o "${valid_name}"
fi

# As long as the output_name exists, increment a counter and change the output_name
while [[ -f "${final_output_name}" ]]
do
    if [[ -z ${counter} ]]
    then
        counter=1
    else
        counter=$((${counter}+1))
    fi
    final_output_name="${final_output_name}-${counter}"
done

final_output_name="${final_output_name}.mp4"

ffmpeg -i "${valid_name}" \
-ss ${start_time} -to ${end_time} \
"${final_output_name}"