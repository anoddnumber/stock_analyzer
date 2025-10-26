import subprocess
import csv
import os
from misc.download_partial.video_processor import process_steps


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

                    steps = [
                        {"op": "crop", "params": {"left": 0.15, "right": 0.15}},
                        {"op": "overlay", "params": {"path": logo_path, "position": "bottom-right", "margin": 16, "scale": {"factor": 0.75}}},
                    ]

                    base, ext = os.path.splitext(final_output)
                    output_path = f"{base}-watermarked{ext}"

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

    # No need to convert to MOV anymore, seems like iMovie works with mp4 now.
    # try:
    #     print('Executing convert_to_mov.bash')
    #     bashCommand = './convert_to_mov.bash'
    #     process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    #     output, error = process.communicate()
    # except Exception:
    #     print('ERROR: There was a problem executing convert_to_mov.bash')

print("DOWNLOAD COMPLETE")