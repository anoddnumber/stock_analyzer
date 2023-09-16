#!/usr/bin/env bash
# Some reason the downloaded video will have a 10 second delay or so from the start time..

url=$1
start_time=$2 # format of time should be something like this: 01:22:10 (HH:MM:SS)
end_time=$3

original_output_name="$(youtube-dl -f 22 --get-title "$url")"

# replace all forward slashes with an underscore, otherwise ffmpeg will treat it as a path
valid_name=$(echo ${original_output_name} | tr / _)
#output_name="${valid_name}.mp4"
output_name="${valid_name}"

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
#    output_name="${valid_name}-${counter}.mp4"
    output_name="${valid_name}-${counter}"
done

# youtube-dl --get-url "$url" returns 2 URLs since BWF's video and audio file are separate for 1080p
videoUrl=$(youtube-dl --get-url "$url" | head -n 1)
audioUrl=$(youtube-dl --get-url "$url" | tail -n 1)

videoName="${output_name}-video.mp4"
audioName="${output_name}-audio.mp4"
output_name="${output_name}.mp4"

# There were issues with the audio (unknown reason) when trying to combine the video and audio all in the same ffmpeg command
# So, I split it up into 3 commands - 1 for the video and 1 for the audio and then merged them together with 1 more ffmpeg command

ffmpeg -i ${audioUrl} \
-ss ${start_time} -to ${end_time} \
"${audioName}"

ffmpeg -i ${videoUrl} \
-ss ${start_time} -to ${end_time} \
"${videoName}"

ffmpeg -i "${videoName}" -i "${audioName}" -c:v copy -c:a copy "${output_name}"

# "-c:v copy" means to copy the video without re-encoding
# "-c:a copy" means to copy the audio without re-encoding
