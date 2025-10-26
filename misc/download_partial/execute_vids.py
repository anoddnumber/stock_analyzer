import argparse
import csv
import os
from typing import List, Tuple

from misc.download_partial.download_partial_vids import download_segment
from misc.download_partial.process_vid import process_video, ProcessOptions
from misc.download_partial.make_title import create_title_image


_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_THIS_DIR, '..', '..'))

_TITLE_BASE_MAP = {
    'S': 'base_ridiculous_badminton_saves_title.png',
    'E': 'base_epic_badminton_title.png',
    'B': 'base_i_dont_believe_it_title.png',
    'F': 'base_fault_or_not_title.png',
    'U': 'base_funny_moments_title.png',
    'R': 'base_racket_change_title.png',
}


def _read_csv_rows(csv_path: str) -> List[List[str]]:
    rows: List[List[str]] = []
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if len(row) < 3:
                continue
            rows.append(row)
    return rows


def run(csv_path: str, out_dir: str, dry_run: bool = False, skip_existing: bool = True) -> None:
    rows = _read_csv_rows(csv_path)
    total = len(rows)
    successes = 0
    failures = 0

    for idx, row in enumerate(rows, start=1):
        try:
            url = row[0]
            start_time = row[1]
            end_time = row[2]

            # Optional 4th column: code like 'S56' → base image + number
            code = row[3].strip() if len(row) >= 4 and row[3] else ''
            letter = code[:1].upper() if code else ''
            digits = ''.join(ch for ch in code[1:] if ch.isdigit()) if len(code) >= 2 else ''

            # Pre-generate title image before any download
            # Output filename is per-row: misc/img/title_{idx}.png
            title_path = None
            out_title_path = os.path.join(_REPO_ROOT, 'misc', 'img', f'title_{idx}.png')
            if letter in _TITLE_BASE_MAP and digits:
                base_filename = _TITLE_BASE_MAP[letter]
                base_path = os.path.join(_REPO_ROOT, 'misc', 'img', base_filename)
                if not os.path.isfile(out_title_path):
                    # Create title image with requested base and number, saving to per-row filename
                    create_title_image(digits, base_path, out_title_path)
                if os.path.isfile(out_title_path):
                    title_path = out_title_path

            print(f"[{idx}/{total}] Downloading: {url} {start_time}-{end_time}")
            if dry_run:
                print("Dry run: skipping download and process")
                successes += 1
                continue

            raw_path = download_segment(url, start_time, end_time, out_dir=out_dir)
            base, ext = os.path.splitext(raw_path)
            final_path = f"{base}-done{ext}"

            if skip_existing and os.path.isfile(final_path):
                print(f"Skipping processing, already exists: {final_path}")
                successes += 1
                continue

            print(f"Processing: {raw_path}")
            opts = ProcessOptions()
            # Use generated title for this row if available
            opts.title_path = title_path if title_path and os.path.isfile(title_path) else None
            produced = process_video(raw_path, final_path, opts)
            print(f"Created: {produced}")
            successes += 1
        except Exception as exc:
            print(f"ERROR processing row {idx}: {exc}")
            failures += 1

    print(f"DONE. success={successes} failures={failures} total={total}")


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Execute sequential video pipeline from CSV.')
    p.add_argument('--csv', default=os.path.join(_THIS_DIR, 'video_feed.csv'), help='CSV path with url,start,end')
    p.add_argument('--out-dir', default=_THIS_DIR, help='Directory to store outputs')
    p.add_argument('--dry-run', action='store_true', help='Only print actions, do not download/process')
    p.add_argument('--no-skip-existing', action='store_true', help='Re-process even if output exists')
    return p


def _main() -> None:
    args = _build_arg_parser().parse_args()
    run(args.csv, args.out_dir, dry_run=args.dry_run, skip_existing=not args.no_skip_existing)


if __name__ == '__main__':
    _main()


