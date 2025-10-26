import argparse
import os
import subprocess
from typing import Optional, Iterable, Tuple, List


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
    # Echo downloader output to terminal for visibility
    if out_text:
        print(out_text, end="")
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


def download_segments(url: str, ranges: Iterable[Tuple[str, str]], out_dir: Optional[str] = None) -> List[str]:
    """Download multiple non-contiguous segments in one run and return list of produced files.

    Args:
        url: Video URL.
        ranges: Iterable of (start, end) strings (HH:MM:SS format recommended).
        out_dir: Optional output directory.

    Returns:
        List of absolute paths to the downloaded .mp4 files (ordered by autonumber).

    Raises:
        RuntimeError: On failure to download or resolve the output path.
    """
    script_path = os.path.join(_THIS_DIR, 'download_partial.bash')
    if not os.path.isfile(script_path):
        raise RuntimeError(f"Downloader script not found: {script_path}")

    cwd = out_dir if out_dir else _THIS_DIR
    if cwd and not os.path.isdir(cwd):
        os.makedirs(cwd, exist_ok=True)

    args = [script_path, url]
    for s, e in ranges:
        args.append(f"{s}-{e}")

    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    stdout, stderr = process.communicate()

    out_text = (stdout or b'').decode('utf-8', errors='ignore') + (stderr or b'').decode('utf-8', errors='ignore')
    # Echo downloader output to terminal for visibility
    if out_text:
        print(out_text, end="")
    produced_list = None
    for line in out_text.splitlines():
        if line.strip().startswith('FINAL_OUTPUT_FILENAMES='):
            produced_list = line.split('FINAL_OUTPUT_FILENAMES=', 1)[1].strip()
            break

    if not produced_list:
        raise RuntimeError(f"Could not determine output filenames. Output was:\n{out_text}")

    parts = [p for p in produced_list.split('|') if p]
    abs_paths: List[str] = [os.path.abspath(os.path.join(cwd, p)) for p in parts]
    for p in abs_paths:
        if not os.path.isfile(p):
            raise RuntimeError(f"Expected output not found: {p}\nLogs:\n{out_text}")

    return abs_paths


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