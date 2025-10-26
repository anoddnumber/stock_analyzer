import subprocess
import csv
import os
from misc.download_partial.video_processor import process_steps


def _compute_title_y_expr(
    video_path: str,
    *,
    crop_left: float,
    crop_right: float,
    crop_top: float = 0.0,
    crop_bottom: float = 0.0,
    target_aspect_w: int = 9,
    target_aspect_h: int = 16,
    top_ratio: float = 0.5,
    final_width: int = 1080,
    gap_px: int = 8,
) -> str:
    """Return an ffmpeg y-expression that places the overlay right above the video.

    Computes the top padding in the final frame (after pad to target aspect and resize),
    then returns an expression like "<top_padding_px>-overlay_h-<gap_px>" so the
    overlay's bottom sits just above the video with a small gap.
    """
    try:
        probe_cmd = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height', '-of', 'csv=p=0:s=x',
            video_path,
        ]
        probe_out = subprocess.check_output(probe_cmd).decode('utf-8').strip()
        src_w, src_h = [int(x) for x in probe_out.split('x')]
    except Exception:
        src_w, src_h = 1920, 1080

    cropped_w = src_w * max(0.0, (1.0 - crop_left - crop_right))
    cropped_h = src_h * max(0.0, (1.0 - crop_top - crop_bottom))
    cropped_ratio = (cropped_h / cropped_w) if cropped_w else 0.0

    target_ratio = float(target_aspect_h) / float(target_aspect_w)
    toppad_px = max(0.0, (target_ratio - cropped_ratio) * float(top_ratio) * float(final_width))
    return f"{int(round(toppad_px))}-overlay_h-{int(gap_px)}"


_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(_THIS_DIR, 'video_feed.csv')
with open(csv_path) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if len(row) < 3:
            print('Row does not have enough arguments, at least 3 expected: {}'.format(row))
            continue

        url = row[0]
        start_time = row[1]
        end_time = row[2]

        try:
            print('Trying to download video with url: {}, start time: {}, and end time: {}'.format(url, start_time, end_time))
            bashCommand = './download_partial.bash {} {} {}'.format(url, start_time, end_time)
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            # Parse the final output filename from the bash script output
            out_text = (output or b'').decode('utf-8', errors='ignore') + (error or b'').decode('utf-8', errors='ignore')
            print(out_text)
            final_output = None
            for line in out_text.splitlines():
                if line.strip().startswith('FINAL_OUTPUT_FILENAME='):
                    final_output = line.split('FINAL_OUTPUT_FILENAME=', 1)[1].strip()
                    break

            if final_output and os.path.isfile(final_output):
                print('Cropping and adding watermark to {}'.format(final_output))
                try:
                    # Build ordered steps: crop first, then overlay logo
                    repo_root = os.path.abspath(os.path.join(_THIS_DIR, '..', '..'))
                    logo_path = os.path.join(repo_root, 'misc', 'img', 'BB_logo_and_name-transparent-with-color.png')
                    title_path = os.path.join(repo_root, 'misc', 'img', 'title.png')

                    # Compute y-expr so the title sits just above the video (small gap)
                    title_y_expr = _compute_title_y_expr(
                        final_output,
                        crop_left=0.2,
                        crop_right=0.2,
                        crop_top=0.0,
                        crop_bottom=0.0,
                        target_aspect_w=9,
                        target_aspect_h=16,
                        top_ratio=0.6,
                        final_width=1080,
                        gap_px=8,
                    )

                    steps = [
                        {"op": "crop", "params": {"left": 0.2, "right": 0.2}},
                        {"op": "overlay", "params": {"path": logo_path, "position": "bottom-right", "margin": 16, "scale": {"factor": 0.75}}},
                        {"op": "pad_to_aspect", "params": {"w": 9, "h": 16, "color": "black", "top_ratio": 0.6}},
                        {"op": "resize", "params": {"width": 1080, "height": 1920, "keep_aspect": False}},
                        {"op": "overlay", "params": {"path": title_path, "x": "(main_w-overlay_w)/2", "y": title_y_expr, "scale": {"width": 864}}},
                    ]

                    base, ext = os.path.splitext(final_output)
                    output_path = f"{base}-done{ext}"

                    wm_output_name = process_steps(final_output, output_path, steps)
                    print('Processed file created: {}'.format(wm_output_name))
                except Exception as exc:
                    print('ERROR: Failed to process {}: {}'.format(final_output, exc))
            else:
                print('WARNING: Could not determine final output filename for url: {}'.format(url))
        except Exception as exc:
            print('ERROR: Could not download video with url: {url}, start time: {}, and end time: {}'
                  .format(start_time, end_time))
            print(exc)

print("DOWNLOAD COMPLETE")