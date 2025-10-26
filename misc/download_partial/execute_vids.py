import argparse
import csv
import os
import subprocess
import tempfile
from typing import List, Tuple

from misc.download_partial.download_partial_vids import download_segment, download_segments
from misc.download_partial.process_vid import process_video, ProcessOptions
from misc.download_partial.make_title import create_title_image
from misc.download_partial.concat_utils import concat_segments


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
            if len(row) < 3:
                print(f"[{idx}/{total}] Skipping row: expected at least 3 columns (url, code, start-end)")
                failures += 1
                continue

            url = row[0]
            # Title code is now after the first comma (second column)
            code = row[1].strip() if row[1] else ''
            # Collect one or more time ranges from columns 3..N
            time_fields = [c.strip() for c in row[2:] if c and c.strip()]
            ranges: List[Tuple[str, str]] = []
            for tf in time_fields:
                if '-' not in tf:
                    print(f"[{idx}/{total}] Skipping malformed time range '{tf}', expected 'start-end'")
                    continue
                s, e = [part.strip() for part in tf.split('-', 1)]
                if s and e:
                    ranges.append((s, e))

            if not ranges:
                print(f"[{idx}/{total}] Skipping row: no valid time ranges found")
                failures += 1
                continue

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

            print(f"[{idx}/{total}] Downloading {len(ranges)} segment(s) from: {url}")
            if dry_run:
                print("Dry run: skipping download and process")
                successes += 1
                continue

            # Prefer yt-dlp multi-section when multiple ranges
            raw_path: str
            if len(ranges) > 1:
                try:
                    produced_paths = download_segments(url, ranges, out_dir=out_dir)
                    # Merge produced_paths in order
                    merged_path = os.path.join(out_dir, f"merge_{idx}.mp4")
                    print("Merging segments from yt-dlp output...")
                    raw_path = concat_segments(produced_paths, merged_path)
                except Exception as exc:
                    print(f"Multi-section download failed ({exc}); falling back to per-segment downloads + merge")
                    segment_paths: List[str] = []
                    for seg_idx, (s, e) in enumerate(ranges, start=1):
                        print(f"  - [{seg_idx}/{len(ranges)}] {s}-{e}")
                        seg_path = download_segment(url, s, e, out_dir=out_dir)
                        segment_paths.append(seg_path)
                    if len(segment_paths) == 1:
                        raw_path = segment_paths[0]
                    else:
                        merged_path = os.path.join(out_dir, f"merge_{idx}.mp4")
                        print("Merging segments...")
                        raw_path = concat_segments(segment_paths, merged_path)
            else:
                # Single range
                s, e = ranges[0]
                raw_path = download_segment(url, s, e, out_dir=out_dir)

            # Determine final output path (base-done.ext)
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
    p.add_argument('--csv', default=os.path.join(_THIS_DIR, 'video_feed.csv'), help='CSV path with url,code,start-end[,start-end...]')
    p.add_argument('--out-dir', default=_THIS_DIR, help='Directory to store outputs')
    p.add_argument('--dry-run', action='store_true', help='Only print actions, do not download/process')
    p.add_argument('--no-skip-existing', action='store_true', help='Re-process even if output exists')
    return p


def _main() -> None:
    args = _build_arg_parser().parse_args()
    run(args.csv, args.out_dir, dry_run=args.dry_run, skip_existing=not args.no_skip_existing)


if __name__ == '__main__':
    _main()


