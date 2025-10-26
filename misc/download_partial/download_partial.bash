#!/usr/bin/env bash
# Download one or multiple non-contiguous sections using yt-dlp
# Usage:
#   download_partial.bash <url> <start-end> [<start-end> ...]
#   download_partial.bash <url> <start> <end>    # backward-compatible

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <url> <start-end> [<start-end> ...] | <url> <start> <end>" >&2
  exit 1
fi

url=$1
shift

# Build --download-sections args
section_args=()
if [[ $# -ge 2 && "$1" != *-* && "$2" != *-* ]]; then
  start_time=$1
  end_time=$2
  section_args+=("--download-sections" "*${start_time}-${end_time}")
else
  for rng in "$@"; do
    section_args+=("--download-sections" "*${rng}")
  done
fi

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

# Download only the requested sections; let yt-dlp/ffmpeg trim and stitch cleanly
# Build command array for safe echo and execution. Use autonumber to emit 1 file per section.
cmd=(
  yt-dlp
  "$url"
  "${section_args[@]}"
  --merge-output-format mp4
  --force-keyframes-at-cuts
  -o "${temp_output_name}-%(autonumber)s.%(ext)s"
)

# Helpful diagnostics
echo "yt-dlp: output template: ${temp_output_name}-%(autonumber)s.%(ext)s"
if [[ ${#section_args[@]} -gt 0 ]]; then
  echo "yt-dlp: sections:"
  # Print just the section specs from section_args (every second item)
  idx=0
  for arg in "${section_args[@]}"; do
    if (( idx % 2 == 1 )); then
      echo "  - ${arg}"
    fi
    ((idx++))
  done
fi

# Print exact command with proper shell escaping
printf -v cmd_str '%q ' "${cmd[@]}"
echo "yt-dlp: running: ${cmd_str}"

"${cmd[@]}"

# Collect produced files (sorted) matching the template
produced=( )
while IFS= read -r f; do
  produced+=("$f")
done < <(ls -1 "${temp_output_name}-"*.mp4 2>/dev/null | sort)

if [[ ${#produced[@]} -eq 0 ]]; then
  echo "No output files found for pattern: ${temp_output_name}-*.mp4" >&2
  exit 2
fi

echo "yt-dlp: produced ${#produced[@]} file(s):"
for f in "${produced[@]}"; do
  echo "  - $f"
done

# Emit a machine-parseable list for the Python caller
IFS='|'
echo "FINAL_OUTPUT_FILENAMES=${produced[*]}"