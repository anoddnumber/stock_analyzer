from typing import Dict, List

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)


def format_timestamp(seconds: float) -> str:
    """Format seconds to readable timestamp [HH:MM:SS]."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"


def get_transcript_text(video_id: str, language: str = "") -> str:
    """Fetch transcript for a YouTube video and return as plain text.
    
    Args:
        video_id: YouTube video ID
        language: Preferred language code (e.g., 'en' or 'en-US'). 
                  If empty, uses first available language.
                  
    Returns:
        Plain text transcript with newlines between segments
        
    Raises:
        TranscriptsDisabled: If transcripts are disabled for the video
        NoTranscriptFound: If no transcript is available
        Exception: For other API errors
    """
    api = YouTubeTranscriptApi()
    # Only pass languages parameter if a specific language is requested
    # When empty, don't pass it to use default/first available language
    if language and language.strip():
        preferred = language.strip()
        fetched_transcript = api.fetch(video_id, languages=[preferred])
    else:
        fetched_transcript = api.fetch(video_id)
    
    # Try to_raw_data() first, fall back to direct iteration if it returns None
    items = fetched_transcript.to_raw_data()
    
    # Join all transcript segments with timestamps
    transcript_lines = []
    
    if items is not None:
        # Use to_raw_data() result
        for item in items:
            text = item.get("text", "").strip()
            start_time = item.get("start", 0.0)
            if text:
                timestamp = format_timestamp(float(start_time))
                transcript_lines.append(f"{timestamp} {text}")
    else:
        # Fall back to direct iteration over transcript object
        for snippet in fetched_transcript:
            text = getattr(snippet, "text", "").strip()
            start_time = getattr(snippet, "start", 0.0)
            if text:
                timestamp = format_timestamp(float(start_time))
                transcript_lines.append(f"{timestamp} {text}")
    
    return "\n".join(transcript_lines)

