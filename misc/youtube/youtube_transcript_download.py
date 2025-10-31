import argparse
import os
import re
from typing import Dict, List, Optional

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)


def to_srt_time(seconds: float) -> str:
    ms_total = int(round(seconds * 1000))
    hours, rem = divmod(ms_total, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1_000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def parse_video_id_from_url(url: str) -> Optional[str]:
    m = re.match(r"^https?://(?:www\.)?youtu\.be/([A-Za-z0-9_-]{6,})", url)
    if m:
        return m.group(1)
    if re.match(r"^https?://(?:www\.)?youtube\.com/watch\?", url):
        from urllib.parse import urlparse, parse_qs

        q = urlparse(url)
        vid = parse_qs(q.query).get("v", [None])[0]
        if vid:
            return vid
    return None


def write_srt(items: List[Dict], out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        for idx, it in enumerate(items, 1):
            start = to_srt_time(float(it.get("start", 0.0)))
            dur = float(it.get("duration", 0.0) or 0.0)
            end = to_srt_time(float(it.get("start", 0.0)) + dur)
            text = (it.get("text") or "")
            f.write(f"{idx}\n{start} --> {end}\n{text}\n\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Download SRT transcript for a public YouTube video using youtube-transcript-api (no OAuth)."
        )
    )
    parser.add_argument("--video-id", default="", help="YouTube video ID")
    parser.add_argument("--url", default="", help="YouTube video URL (alternative to --video-id)")
    parser.add_argument(
        "--language",
        default="",
        help="Preferred language code (e.g., en or en-US). Will attempt translation if not available.",
    )
    parser.add_argument(
        "--out-dir",
        default=os.path.join("misc", "youtube", "transcripts"),
        help="Directory to save SRT transcripts",
    )

    args = parser.parse_args()

    video_id = (args.video_id or "").strip()
    if not video_id:
        if args.url:
            video_id = parse_video_id_from_url(args.url.strip()) or ""
        if not video_id:
            raise SystemExit("Provide --video-id or a valid --url (youtube.com/watch?v=… or youtu.be/…).")

    preferred = (args.language or "").strip()

    api = YouTubeTranscriptApi()
    try:
        languages = [preferred] if preferred else None
        fetched_transcript = api.fetch(video_id, languages=languages)
        items = fetched_transcript.to_raw_data()
        lang_code = fetched_transcript.language_code
    except TranscriptsDisabled:
        raise SystemExit("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise SystemExit(
            "No transcripts found for this video or requested language." if preferred else "No transcripts found for this video."
        )
    except Exception as e:
        raise SystemExit(f"Failed to fetch transcript: {e}")

    os.makedirs(args.out_dir, exist_ok=True)
    suffix = f".{lang_code}" if lang_code else ""
    out_name = f"{video_id}{suffix}.srt"
    out_path = os.path.join(args.out_dir, out_name)

    try:
        write_srt(items, out_path)
    except Exception as e:
        raise SystemExit(f"Failed to write SRT: {e}")

    print(f"Saved SRT to: {out_path}")


if __name__ == "__main__":
    main()


