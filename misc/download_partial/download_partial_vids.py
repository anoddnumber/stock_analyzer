import argparse
import os
import subprocess
from typing import Optional


_THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def download_segment(url: str, start_time: str, end_time: str, out_dir: Optional[str] = None) -> str:
    """Download a video segment using the existing bash script and return the file path.

    Args:
        url: Video URL.
        start_time: HH:MM:SS start time.
        end_time: HH:MM:SS end time.
        out_dir: Optional directory to place the downloaded file. Created if missing.

    Returns:
        Absolute path to the downloaded .mp4 file.

    Raises:
        RuntimeError: If the download fails or the output cannot be determined.
    """
    script_path = os.path.join(_THIS_DIR, 'download_partial.bash')
    if not os.path.isfile(script_path):
        raise RuntimeError(f"Downloader script not found: {script_path}")

    cwd = out_dir if out_dir else _THIS_DIR
    if cwd and not os.path.isdir(cwd):
        os.makedirs(cwd, exist_ok=True)

    cmd = [script_path, url, start_time, end_time]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    stdout, stderr = process.communicate()

    out_text = (stdout or b'').decode('utf-8', errors='ignore') + (stderr or b'').decode('utf-8', errors='ignore')
    final_output_name = None
    for line in out_text.splitlines():
        if line.strip().startswith('FINAL_OUTPUT_FILENAME='):
            final_output_name = line.split('FINAL_OUTPUT_FILENAME=', 1)[1].strip()
            break

    if not final_output_name:
        raise RuntimeError(f"Could not determine output filename. Output was:\n{out_text}")

    abs_output_path = os.path.abspath(os.path.join(cwd, final_output_name))
    if not os.path.isfile(abs_output_path):
        raise RuntimeError(f"Expected output not found: {abs_output_path}\nLogs:\n{out_text}")

    return abs_output_path


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Download a partial video segment.')
    parser.add_argument('url', help='Video URL')
    parser.add_argument('start_time', help='Start time HH:MM:SS')
    parser.add_argument('end_time', help='End time HH:MM:SS')
    parser.add_argument('--out-dir', default=None, help='Directory to save the downloaded file')
    return parser


def _main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()
    output_path = download_segment(args.url, args.start_time, args.end_time, args.out_dir)
    print(output_path)


if __name__ == '__main__':
    _main()