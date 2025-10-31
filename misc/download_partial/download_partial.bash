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

# Derive a unique suffix from the requested time ranges to avoid collisions
ranges_parts=( )
idx=0
for arg in "${section_args[@]}"; do
  if (( idx % 2 == 1 )); then
    ranges_parts+=("${arg}")
  fi
  ((idx++))
done
ranges_key=$(printf '%s|' "${ranges_parts[@]}")

if command -v shasum >/dev/null 2>&1; then
  suffix=$(printf '%s' "${ranges_key}" | shasum | awk '{print $1}' | cut -c1-8)
elif command -v sha1sum >/dev/null 2>&1; then
  suffix=$(printf '%s' "${ranges_key}" | sha1sum | awk '{print $1}' | cut -c1-8)
elif command -v md5 >/dev/null 2>&1; then
  suffix=$(printf '%s' "${ranges_key}" | md5 | awk '{print $NF}' | cut -c1-8)
else
  suffix=$(printf '%s' "${ranges_key}" | cksum | awk '{print $1}' | cut -c1-8)
fi

temp_output_name="${sanitized_title}-${suffix}"

# If files already exist with this base, append a counter
counter=
while compgen -G "${temp_output_name}-"*.mp4 > /dev/null; do
  if [[ -z ${counter} ]]; then
    counter=1
  else
    counter=$((counter+1))
  fi
  temp_output_name="${sanitized_title}-${suffix}-${counter}"
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
if [[ ${#produced[@]} -eq 1 ]]; then
  echo "FINAL_OUTPUT_FILENAME=${produced[0]}"
fi