import argparse
import csv
import os
import re
from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Tuple

import requests


YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


def load_video_ids(inline_ids: str | None, file_path: str | None) -> List[str]:
    ids: List[str] = []
    if inline_ids:
        for tok in inline_ids.split(","):
            tok = tok.strip()
            if tok:
                ids.append(tok)
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                for tok in line.split(","):
                    tok = tok.strip()
                    if tok:
                        ids.append(tok)
    # de-dup while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for vid in ids:
        if vid not in seen:
            seen.add(vid)
            unique.append(vid)
    return unique


def fetch_all_comments(
    api_key: str,
    video_id: str,
    pages: int = 50,
    order: str = "relevance",
) -> List[str]:
    comments: List[str] = []
    page_token: str | None = None
    fetched_pages = 0

    while fetched_pages < pages:
        resp = requests.get(
            f"{YOUTUBE_API_BASE}/commentThreads",
            params={
                "part": "snippet,replies",
                "videoId": video_id,
                "maxResults": 100,
                "textFormat": "plainText",
                "order": order,
                "pageToken": page_token,
                "key": api_key,
            },
            timeout=30,
        )
        if resp.status_code == 403:
            # comments disabled or quota; return what we have
            break
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("items", []):
            top = (
                item.get("snippet", {})
                .get("topLevelComment", {})
                .get("snippet", {})
                .get("textOriginal", "")
            )
            if top:
                comments.append(top)
            for rep in item.get("replies", {}).get("comments", []):
                txt = rep.get("snippet", {}).get("textOriginal", "")
                if txt:
                    comments.append(txt)
        page_token = data.get("nextPageToken")
        fetched_pages += 1
        if not page_token:
            break

    return comments


# h:mm:ss or mm:ss (captures optional hours)
HMS = re.compile(r"\b(?:(\d+):)?([0-5]?\d):([0-5]\d)\b")

# 1h23m45s, 2m10s, 45s (case-insensitive)
HUM = re.compile(r"\b(?:(\d+)h)?(?:(\d{1,2})m)?(?:(\d{1,2})s)\b", re.IGNORECASE)


def to_minutes(h: int | str | None, m: int | str | None, s: int | str | None) -> int:
    hh = int(h or 0)
    mm = int(m or 0)
    ss = int(s or 0)
    return (hh * 3600 + mm * 60 + ss) // 60


def extract_timestamp_minutes(text: str) -> List[int]:
    minutes: List[int] = []
    for h, m, s in HMS.findall(text):
        minutes.append(to_minutes(h, m, s))
    for h, m, s in HUM.findall(text):
        # Ensure at least one component; regex already does, but keep consistent
        minutes.append(to_minutes(h, m, s))
    return minutes


def analyze_comments_minutes(comments: Iterable[str]) -> Counter:
    counts: Counter = Counter()
    for c in comments:
        for minute in extract_timestamp_minutes(c):
            counts[minute] += 1
    return counts


def write_csv(path: str, rows: Iterable[Tuple[str, int, int]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["videoId", "minute", "count"]) 
        for vid, minute, count in rows:
            w.writerow([vid, minute, count])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze comment timestamps for one or more YouTube videos."
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("YOUTUBE_API_KEY", ""),
        help="YouTube Data API key (or set YOUTUBE_API_KEY env var).",
    )
    parser.add_argument(
        "--video-ids",
        help="Comma-separated list of YouTube video IDs.",
    )
    parser.add_argument(
        "--video-ids-file",
        help="Path to a file containing video IDs (comma or newline separated).",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=50,
        help="Max comment pages per video (100 comments per page).",
    )
    parser.add_argument(
        "--order",
        choices=["relevance", "time"],
        default="relevance",
        help="Comment ordering (API fetch).",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="How many minute bins to print per video.",
    )
    parser.add_argument(
        "--out-csv",
        help="Optional path to write all bins as CSV (videoId,minute,count).",
    )

    args = parser.parse_args()

    if not args.api_key:
        raise SystemExit(
            "Missing API key. Provide --api-key or set env var YOUTUBE_API_KEY."
        )

    video_ids = load_video_ids(args.video_ids, args.video_ids_file)
    if not video_ids:
        raise SystemExit(
            "Provide video IDs via --video-ids or --video-ids-file (comma/newline separated)."
        )

    all_rows: List[Tuple[str, int, int]] = []

    for vid in video_ids:
        comments = fetch_all_comments(
            api_key=args.api_key,
            video_id=vid,
            pages=args.pages,
            order=args.order,
        )
        counts = analyze_comments_minutes(comments)
        if not counts:
            print(f"{vid}: no timestamps found (comments fetched: {len(comments)})")
            continue

        # collect rows for CSV and printing
        for minute, cnt in counts.items():
            all_rows.append((vid, minute, cnt))

        # print top N for this video
        print(vid)
        for minute, cnt in sorted(
            counts.items(), key=lambda kv: (-kv[1], kv[0])
        )[: args.top]:
            print(f"  minute={minute:>4}  count={cnt}")

    if args.out_csv and all_rows:
        write_csv(args.out_csv, all_rows)


if __name__ == "__main__":
    main()


