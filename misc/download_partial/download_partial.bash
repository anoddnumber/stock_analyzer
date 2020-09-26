#!/usr/bin/env bash

# Some reason the downloaded video will have a 10 second delay or so from the start time..

url=$1
start_time=$2 # format of time should be something like this: 01:22:10 (HH:MM:SS)
end_time=$3

original_output_name="$(youtube-dl --get-title "$url")"

# replace all forward slashes with an underscore, otherwise ffmpeg will treat it as a path
valid_name=$(echo ${original_output_name} | tr / _)
output_name="${valid_name}.mp4"

counter=

# As long as the output_name exists, increment a counter and change the output_name
while [[ -f "${output_name}" ]]
do
    if [[ -z ${counter} ]]
    then
        counter=1
    else
        counter=$((${counter}+1))
    fi
    output_name="${valid_name}-${counter}.mp4"
done

echo ${output_name}

# -f 22 indicates 720p with video and audio. Some reason 1080p only comes with video for BWF videos...
ffmpeg -i $(youtube-dl -f 22 --get-url "$url") \
-ss ${start_time} -to ${end_time} -c:v copy -c:a copy \
"${output_name}" > /dev/null 2>&1