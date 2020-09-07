#!/usr/bin/env bash

# Some reason the downloaded video will have a 10 second delay or so from the start time..

url=$1
start_time=$2 # format of time should be something like this: 00:00:10
end_time=$3

original_output_name="$(youtube-dl --get-title "$url")"
output_name="$(youtube-dl --get-title "$url").mp4"

# replace all forward slashes with an underscore, otherwise ffmpeg will treat it as a path
output_name=$(echo "$output_name"| tr / _)

counter=

# As long as the output_name exists, increment a counter and change the output_name
while [ -f "$output_name" ]
do
    if [ -z $counter ]
    then
        counter=1
    else
        counter=$(($counter+1))
    fi
    output_name="$original_output_name-$counter.mp4"
done

echo $output_name

ffmpeg -i $(youtube-dl -f 22 --get-url "$url") \
-ss $start_time -to $end_time -c:v copy -c:a copy \
"$output_name" > /dev/null 2>&1