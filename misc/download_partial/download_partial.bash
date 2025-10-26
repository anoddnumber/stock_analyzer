#!/usr/bin/env bash
# Some reason the downloaded video will have a 10 second delay or so from the start time..

url=$1
start_time=$2 # format of time should be something like this: 01:22:10 (HH:MM:SS)
end_time=$3

original_title="$(yt-dlp --print filename -o "%(title)s" "$url")"
# sanitize title to avoid path separators in filenames
sanitized_title=$(echo "${original_title}" | tr / _)
temp_output_name="${sanitized_title}"

counter=
# As long as the output_name exists, increment a counter and change the output_name
while [[ -f "${temp_output_name}.mp4" ]]
do
    if [[ -z ${counter} ]]
    then
        counter=1
    else
        counter=$((${counter}+1))
    fi
    temp_output_name="${original_title}-${counter}"
done

final_output_name="${temp_output_name}.mp4"

# Download only the requested section and let yt-dlp/ffmpeg handle the trim
yt-dlp "$url" \
--download-sections "*${start_time}-${end_time}" \
--merge-output-format mp4 \
--force-keyframes-at-cuts \
-o "${final_output_name}"

# Echo the final output name for callers to capture
echo "FINAL_OUTPUT_FILENAME=${final_output_name}"