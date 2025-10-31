import re
from typing import Dict, Optional
from urllib.parse import urlparse, parse_qs

import requests


YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


def parse_video_id_from_url(url: str) -> Optional[str]:
    """Extract video ID from YouTube URL (supports youtube.com/watch?v=... and youtu.be/...)."""
    m = re.match(r"^https?://(?:www\.)?youtu\.be/([A-Za-z0-9_-]{6,})", url)
    if m:
        return m.group(1)
    if re.match(r"^https?://(?:www\.)?youtube\.com/watch\?", url):
        q = urlparse(url)
        vid = parse_qs(q.query).get("v", [None])[0]
        if vid:
            return vid
    return None


def get_video_metadata(api_key: str, video_id: str) -> Dict[str, str]:
    """Fetch video metadata (title, URL) using YouTube Data API v3.
    
    Args:
        api_key: YouTube Data API v3 key
        video_id: YouTube video ID
        
    Returns:
        Dictionary with 'title' and 'url' keys
        
    Raises:
        requests.RequestException: If API request fails
        ValueError: If video not found or invalid response
    """
    response = requests.get(
        f"{YOUTUBE_API_BASE}/videos",
        params={
            "part": "snippet",
            "id": video_id,
            "key": api_key,
        },
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    items = data.get("items", [])
    if not items:
        raise ValueError(f"Video not found: {video_id}")
    
    snippet = items[0].get("snippet", {})
    title = snippet.get("title", "")
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    return {
        "title": title,
        "url": url,
    }

