import argparse
import os
from typing import Dict, List

import requests


YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


def resolve_channel_id(api_key: str, handle: str) -> str:
    """Resolve a YouTube channel handle (e.g., @BWF) to channelId."""
    response = requests.get(
        f"{YOUTUBE_API_BASE}/channels",
        params={"part": "id", "forHandle": handle, "key": api_key},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    items = data.get("items", [])
    if not items:
        raise ValueError(f"No channel found for handle '{handle}'. Response: {data}")
    return items[0]["id"]


def get_uploads_playlist_id(api_key: str, channel_id: str) -> str:
    """Return the uploads playlist ID for the given channel."""
    r = requests.get(
        f"{YOUTUBE_API_BASE}/channels",
        params={"part": "contentDetails", "id": channel_id, "key": api_key},
        timeout=20,
    )
    r.raise_for_status()
    data = r.json()
    items = data.get("items", [])
    if not items:
        raise ValueError(
            f"No contentDetails for channel '{channel_id}'. Response: {data}"
        )
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]


def fetch_video_ids_from_uploads(
    api_key: str, uploads_playlist_id: str, pages: int = 1, per_page: int = 50
) -> List[str]:
    """Collect video IDs from the channel uploads playlist across pages."""
    ids: List[str] = []
    page_token: str | None = None
    fetched_pages = 0

    while fetched_pages < pages:
        resp = requests.get(
            f"{YOUTUBE_API_BASE}/playlistItems",
            params={
                "part": "contentDetails",
                "playlistId": uploads_playlist_id,
                "maxResults": min(per_page, 50),
                "pageToken": page_token,
                "key": api_key,
            },
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        for it in data.get("items", []):
            vid = it.get("contentDetails", {}).get("videoId")
            if vid:
                ids.append(vid)

        page_token = data.get("nextPageToken")
        fetched_pages += 1
        if not page_token:
            break

    return ids


def fetch_most_popular_video_ids(
    api_key: str,
    channel_id: str,
    max_results: int = 25,
    pages: int = 1,
) -> List[str]:
    """Fetch video IDs from a channel ordered by viewCount using search.list.

    Note: search.list returns metadata but not statistics. We use it to rank by viewCount
    and then retrieve statistics via videos.list.
    """
    video_ids: List[str] = []
    page_token: str | None = None
    fetched_pages = 0

    while fetched_pages < pages:
        response = requests.get(
            f"{YOUTUBE_API_BASE}/search",
            params={
                "part": "snippet",
                "channelId": channel_id,
                "order": "viewCount",
                "type": "video",
                "maxResults": min(max_results, 50),
                "pageToken": page_token,
                "key": api_key,
            },
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])
        for item in items:
            id_obj = item.get("id", {})
            vid = id_obj.get("videoId")
            if vid:
                video_ids.append(vid)

        page_token = data.get("nextPageToken")
        fetched_pages += 1
        if not page_token:
            break

        if len(video_ids) >= max_results:
            break

    return video_ids[:max_results]


def chunked(iterable: List[str], size: int) -> List[List[str]]:
    return [iterable[i : i + size] for i in range(0, len(iterable), size)]


def fetch_video_stats(api_key: str, video_ids: List[str]) -> List[Dict]:
    """Fetch statistics and snippet for the given video IDs via videos.list."""
    results: List[Dict] = []
    for batch in chunked(video_ids, 50):
        response = requests.get(
            f"{YOUTUBE_API_BASE}/videos",
            params={
                "part": "statistics,snippet",
                "id": ",".join(batch),
                "key": api_key,
            },
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        for item in data.get("items", []):
            stats = item.get("statistics", {})
            snippet = item.get("snippet", {})
            try:
                view_count = int(stats.get("viewCount", 0))
            except (TypeError, ValueError):
                view_count = 0
            results.append(
                {
                    "id": item.get("id"),
                    "title": snippet.get("title", ""),
                    "publishedAt": snippet.get("publishedAt", ""),
                    "viewCount": view_count,
                }
            )
    return results


def title_matches_requirements(title: str, required_terms: List[str]) -> bool:
    """Return True if title contains all required substrings (case-insensitive)."""
    if not required_terms:
        return True
    lowered_title = title.lower()
    return all(term.lower() in lowered_title for term in required_terms)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch most-popular videos from a YouTube channel by handle (@BWF)."
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("YOUTUBE_API_KEY", ""),
        help="YouTube Data API key (or set YOUTUBE_API_KEY env var).",
    )
    parser.add_argument(
        "--handle",
        default="@BWF",
        help="Channel handle, e.g. @BWF.",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=25,
        help="Max videos to return (<=50 per page).",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help="How many pages to traverse (each up to 50 results).",
    )
    parser.add_argument(
        "--require",
        action="append",
        default=[],
        help=(
            "Require video titles to contain these substrings; "
            "repeatable, AND semantics, case-insensitive"
        ),
    )

    args = parser.parse_args()

    api_key = args.api_key
    if not api_key:
        raise SystemExit(
            "Missing API key. Provide --api-key or set env var YOUTUBE_API_KEY."
        )

    channel_id = resolve_channel_id(api_key, args.handle)
    uploads_id = get_uploads_playlist_id(api_key, channel_id)
    video_ids = fetch_video_ids_from_uploads(
        api_key=api_key,
        uploads_playlist_id=uploads_id,
        pages=args.pages,
        per_page=50,
    )

    if not video_ids:
        print("No videos found.")
        return

    videos = fetch_video_stats(api_key, video_ids)
    if args.require:
        videos = [
            v
            for v in videos
            if title_matches_requirements(v.get("title", ""), args.require)
        ]
        if not videos:
            print("No videos matched the title filter.")
            return
    videos.sort(key=lambda v: v.get("viewCount", 0), reverse=True)
    videos = videos[:args.max_results]

    for v in videos:
        vid = v.get("id")
        views = v.get("viewCount", 0)
        published = v.get("publishedAt", "")
        title = v.get("title", "")
        url = f"https://www.youtube.com/watch?v={vid}" if vid else ""
        print(f"{views:>12}  {published[:10]}  {title}  {url}")


if __name__ == "__main__":
    main()


