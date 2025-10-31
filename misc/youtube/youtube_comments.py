from typing import List

import requests


YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


def get_all_comments(
    api_key: str,
    video_id: str,
    max_pages: int = 50,
) -> List[str]:
    """Fetch all comments (top-level and replies) for a YouTube video.
    
    Args:
        api_key: YouTube Data API v3 key
        video_id: YouTube video ID
        max_pages: Maximum number of pages to fetch (100 comments per page)
        
    Returns:
        List of comment texts (strings)
        
    Note:
        Returns empty list if comments are disabled or API request fails.
    """
    comments: List[str] = []
    page_token: str | None = None
    fetched_pages = 0

    while fetched_pages < max_pages:
        resp = requests.get(
            f"{YOUTUBE_API_BASE}/commentThreads",
            params={
                "part": "snippet,replies",
                "videoId": video_id,
                "maxResults": 100,
                "textFormat": "plainText",
                "order": "relevance",
                "pageToken": page_token,
                "key": api_key,
            },
            timeout=30,
        )
        if resp.status_code == 403:
            # Comments disabled or quota exceeded; return what we have
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

