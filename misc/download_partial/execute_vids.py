import argparse
import csv
import os
import subprocess
import tempfile
import re
from dataclasses import dataclass
from typing import List, Tuple, Optional

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

_FILENAME_SLUG_MAP = {
    'R': 'racket_change',
    'F': 'fault_or_not',
    'E': 'epic_badminton',
    'S': 'ridiculous_badminton_saves',
    'B': 'i_dont_believe_it',
    'U': 'funny_moments',
}


# ---------------------------
# Data models and type aliases
# ---------------------------

TimeRange = Tuple[str, str]


@dataclass
class RowSpec:
    """Parsed specification for one CSV row."""
    url: str
    code: str
    letter: str
    digits: str
    no_title: bool
    crop_left: Optional[float]
    crop_right: Optional[float]
    ranges: List[TimeRange]


def _read_csv_rows(csv_path: str) -> List[List[str]]:
    """Read CSV rows, stripping comments and empty lines.

    Rows with fewer than 3 columns are kept; validation happens later.
    """
    rows: List[List[str]] = []
    with open(csv_path) as csvfile:
        def _cleaned_lines(f):
            for raw in f:
                line = raw.split('#', 1)[0].strip()
                if line:
                    yield line
        reader = csv.reader(_cleaned_lines(csvfile), delimiter=',')
        for row in reader:
            rows.append(row)
    return rows


# ---------------------------
# Parsing helpers (pure)
# ---------------------------

def parse_code(code: Optional[str]) -> Tuple[str, str, bool]:
    """Parse code into (letter, digits, no_title)."""
    if not code:
        return '', '', False
    code = code.strip()
    letter = code[:1].upper() if code else ''
    digits = ''.join(ch for ch in code[1:] if ch.isdigit()) if len(code) >= 2 else ''
    no_title = (letter == 'N')
    return letter, digits, no_title


def parse_crop_field(field: Optional[str]) -> Tuple[Optional[float], Optional[float]]:
    """Parse a crop field like "left:right" where values can be fractions or percentages.

    Returns (left, right) in 0..0.95 if valid, otherwise (None, None).
    """
    if not field:
        return None, None
    field = field.strip()
    # Heuristic aligned with previous logic: treat as crop only if it has ':' and no '-'
    if ':' not in field or '-' in field:
        return None, None

    m = re.match(r"^\s*(\d*\.?\d+%?)\s*:\s*(\d*\.?\d+%?)\s*$", field)
    if not m:
        return None, None

    def _parse_component(v: str) -> Optional[float]:
        v = v.strip()
        if v.endswith('%'):
            try:
                return float(v[:-1]) / 100.0
            except ValueError:
                return None
        try:
            return float(v)
        except ValueError:
            return None

    def _clamp(x: float) -> float:
        return max(0.0, min(0.95, x))

    left_raw = _parse_component(m.group(1))
    right_raw = _parse_component(m.group(2))
    if left_raw is None or right_raw is None:
        return None, None
    return _clamp(left_raw), _clamp(right_raw)


def parse_time_fields(fields: List[str]) -> List[TimeRange]:
    """Extract valid time ranges from fields of form "start-end" (strings kept as-is)."""
    ranges: List[TimeRange] = []
    for tf in fields:
        if '-' not in tf:
            continue
        s, e = [part.strip() for part in tf.split('-', 1)]
        if s and e:
            ranges.append((s, e))
    return ranges


# ---------------------------
# Title, download, and path helpers
# ---------------------------

def prepare_title_image(idx: int, letter: str, digits: str) -> Tuple[Optional[str], bool]:
    """Prepare per-row title image if code indicates it.

    Returns (title_path, created_this_call).
    """
    if not letter or not digits or letter not in _TITLE_BASE_MAP:
        return None, False
    out_title_path = os.path.join(_REPO_ROOT, 'misc', 'img', f'title_{idx}.png')
    base_filename = _TITLE_BASE_MAP[letter]
    base_path = os.path.join(_REPO_ROOT, 'misc', 'img', base_filename)
    created = False
    if not os.path.isfile(out_title_path):
        create_title_image(digits, base_path, out_title_path)
        created = True
    if os.path.isfile(out_title_path):
        return out_title_path, created
    return None, created


def download_and_maybe_merge(url: str, ranges: List[TimeRange], out_dir: str) -> str:
    """Download one or many ranges; merge if needed; return path to raw video."""
    if len(ranges) > 1:
        try:
            produced_paths = download_segments(url, ranges, out_dir=out_dir)
            merged_path = os.path.join(out_dir, f"merge_{os.getpid()}_{abs(hash((url, tuple(ranges)))) % 100000}.mp4")
            print("Merging segments from yt-dlp output...")
            return concat_segments(produced_paths, merged_path)
        except Exception as exc:
            print(f"Multi-section download failed ({exc}); falling back to per-segment downloads + merge")
            segment_paths: List[str] = []
            for seg_idx, (s, e) in enumerate(ranges, start=1):
                print(f"  - [{seg_idx}/{len(ranges)}] {s}-{e}")
                seg_path = download_segment(url, s, e, out_dir=out_dir)
                segment_paths.append(seg_path)
            if len(segment_paths) == 1:
                return segment_paths[0]
            merged_path = os.path.join(out_dir, f"merge_{os.getpid()}_{abs(hash((url, tuple(ranges)))) % 100000}.mp4")
            print("Merging segments...")
            return concat_segments(segment_paths, merged_path)
    # Single range
    s, e = ranges[0]
    return download_segment(url, s, e, out_dir=out_dir)


def compute_final_output_path(raw_path: str, letter: str, digits: str, out_dir: str) -> str:
    """Compute final output path name based on code or raw path."""
    if letter in _FILENAME_SLUG_MAP and digits:
        slug = _FILENAME_SLUG_MAP[letter]
        number = str(int(digits))
        final_filename = f"{slug}_{number}.mp4"
        return os.path.join(out_dir, final_filename)
    base, ext = os.path.splitext(raw_path)
    return f"{base}-done{ext}"


# ---------------------------
# Per-row processing
# ---------------------------

def process_one_row(idx: int, total: int, row: RowSpec, out_dir: str, dry_run: bool, skip_existing: bool) -> Tuple[bool, Optional[str], bool]:
    """Execute the pipeline for a single row.

    Returns (success, title_path_created, created_flag)
    """
    url = row.url
    print(f"[{idx}/{total}] Downloading {len(row.ranges)} segment(s) from: {url}")
    if dry_run:
        print("Dry run: skipping download and process")
        return True, None, False

    title_path = None
    created_title_this_row = False
    if not row.no_title:
        title_path, created_title_this_row = prepare_title_image(idx, row.letter, row.digits)

    raw_path = download_and_maybe_merge(url, row.ranges, out_dir=out_dir)

    final_path = compute_final_output_path(raw_path, row.letter, row.digits, out_dir)
    if skip_existing and os.path.isfile(final_path):
        print(f"Skipping processing, already exists: {final_path}")
        return True, title_path if created_title_this_row else None, created_title_this_row

    print(f"Processing: {raw_path}")
    opts = ProcessOptions()
    if row.crop_left is not None:
        opts.crop_left = row.crop_left
    if row.crop_right is not None:
        opts.crop_right = row.crop_right
    opts.title_path = None if row.no_title else (title_path if title_path and os.path.isfile(title_path) else None)

    produced = process_video(raw_path, final_path, opts)
    print(f"Created: {produced}")
    return True, title_path if created_title_this_row else None, created_title_this_row



def run(csv_path: str, out_dir: str, dry_run: bool = False, skip_existing: bool = True, keep_titles: bool = False) -> None:
    rows = _read_csv_rows(csv_path)
    total = len(rows)
    successes = 0
    failures = 0
    titles_to_cleanup: List[str] = []

    for idx, raw_row in enumerate(rows, start=1):
        try:
            if len(raw_row) < 3:
                print(f"[{idx}/{total}] Skipping row: expected at least 3 columns (url, code, start-end)")
                failures += 1
                continue

            url = raw_row[0]
            code = (raw_row[1] or '').strip()

            # Crop detection from column 3
            crop_left_val: Optional[float] = None
            crop_right_val: Optional[float] = None
            start_idx = 2
            if len(raw_row) >= 3 and raw_row[2]:
                l, r = parse_crop_field(raw_row[2])
                if l is not None and r is not None:
                    crop_left_val, crop_right_val = l, r
                    start_idx = 3

            # Time fields and validation prints (preserve behavior)
            time_fields = [c.strip() for c in raw_row[start_idx:] if c and c.strip()]
            # Print malformed notices just like before
            for tf in time_fields:
                if '-' not in tf:
                    print(f"[{idx}/{total}] Skipping malformed time range '{tf}', expected 'start-end'")
            ranges = parse_time_fields(time_fields)
            if not ranges:
                print(f"[{idx}/{total}] Skipping row: no valid time ranges found")
                failures += 1
                continue

            letter, digits, no_title = parse_code(code)

            row = RowSpec(
                url=url,
                code=code,
                letter=letter,
                digits=digits,
                no_title=no_title,
                crop_left=crop_left_val,
                crop_right=crop_right_val,
                ranges=ranges,
            )

            success, title_path_for_cleanup, created_title = process_one_row(
                idx, total, row, out_dir, dry_run, skip_existing
            )
            if success:
                successes += 1
                if created_title and title_path_for_cleanup and os.path.isfile(title_path_for_cleanup):
                    titles_to_cleanup.append(title_path_for_cleanup)
            else:
                failures += 1
        except Exception as exc:
            print(f"ERROR processing row {idx}: {exc}")
            failures += 1

    print(f"DONE. success={successes} failures={failures} total={total}")
    # Best-effort cleanup of generated title images
    if not keep_titles and titles_to_cleanup:
        for p in titles_to_cleanup:
            try:
                os.remove(p)
            except FileNotFoundError:
                pass


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Execute sequential video pipeline from CSV.')
    p.add_argument('--csv', default=os.path.join(_THIS_DIR, 'video_feed.csv'), help='CSV with url,code,[left:right],start-end[,start-end...] . Use code N to disable title overlay. left/right are fractions (e.g., .25:.30 or 25%%).')
    p.add_argument('--out-dir', default=_THIS_DIR, help='Directory to store outputs')
    p.add_argument('--dry-run', action='store_true', help='Only print actions, do not download/process')
    p.add_argument('--no-skip-existing', action='store_true', help='Re-process even if output exists')
    p.add_argument('--keep-titles', action='store_true', help='Do not delete generated title_*.png images after run')
    return p


def _main() -> None:
    args = _build_arg_parser().parse_args()
    run(args.csv, args.out_dir, dry_run=args.dry_run, skip_existing=not args.no_skip_existing, keep_titles=args.keep_titles)


if __name__ == '__main__':
    _main()


