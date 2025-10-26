import argparse
import csv
import os
from typing import List, Tuple

from misc.download_partial.download_partial_vids import download_segment
from misc.download_partial.process_vid import process_video, ProcessOptions


_THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def _read_csv_rows(csv_path: str) -> List[Tuple[str, str, str]]:
    rows: List[Tuple[str, str, str]] = []
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if len(row) < 3:
                continue
            rows.append((row[0], row[1], row[2]))
    return rows


def run(csv_path: str, out_dir: str, dry_run: bool = False, skip_existing: bool = True) -> None:
    rows = _read_csv_rows(csv_path)
    total = len(rows)
    successes = 0
    failures = 0

    for idx, (url, start_time, end_time) in enumerate(rows, start=1):
        try:
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


