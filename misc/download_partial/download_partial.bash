#!/usr/bin/env bash
# Some reason the downloaded video will have a 10 second delay or so from the start time..

url=$1
start_time=$2 # format of time should be something like this: 01:22:10 (HH:MM:SS)
end_time=$3

original_output_name="$(youtube-dl -f 22 --get-title "$url")"

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

# youtube-dl --get-url "$url" returns 2 URLs since BWF's video and audio file are separate for 1080p
videoUrl=$(youtube-dl --get-url "$url" | head -n 1)
audioUrl=$(youtube-dl --get-url "$url" | tail -n 1)

ffmpeg -i ${videoUrl} -i ${audioUrl} \
-ss ${start_time} -to ${end_time} -c:v copy -c:a copy \
"${output_name}"
