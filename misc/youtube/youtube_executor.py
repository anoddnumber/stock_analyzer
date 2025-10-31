import argparse
import os
import sys
from typing import Optional

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from youtube_comments import get_all_comments
from youtube_metadata import get_video_metadata, parse_video_id_from_url
from youtube_transcript_helper import get_transcript_text


def extract_video_id(line: str) -> Optional[str]:
    """Extract video ID from a line (could be URL or ID)."""
    line = line.strip()
    if not line:
        return None
    
    # Try parsing as URL first
    video_id = parse_video_id_from_url(line)
    if video_id:
        return video_id
    
    # If not a URL, assume it's a direct video ID
    # Basic validation: should be alphanumeric with dashes/underscores, 11 chars typical
    if line and len(line) >= 6:
        return line
    
    return None


def process_video(
    api_key: str,
    video_id: str,
    results_dir: str,
    language: str = "",
    max_comment_pages: int = 50,
) -> bool:
    """Process a single video: fetch metadata, transcript, comments, and write to file.
    
    Returns:
        True if successful, False otherwise
    """
    output_path = os.path.join(results_dir, f"{video_id}.txt")
    
    # Fetch metadata
    try:
        metadata = get_video_metadata(api_key, video_id)
        title = metadata["title"]
        url = metadata["url"]
    except Exception as e:
        print(f"Warning: Failed to fetch metadata for {video_id}: {e}")
        title = "Unknown"
        url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Fetch transcript
    transcript_text = None
    try:
        transcript_text = get_transcript_text(video_id, language)
    except Exception as e:
        print(f"Warning: Failed to fetch transcript for {video_id}: {e}")
        transcript_text = None
    
    # Fetch comments
    comments = []
    try:
        comments = get_all_comments(api_key, video_id, max_pages=max_comment_pages)
    except Exception as e:
        print(f"Warning: Failed to fetch comments for {video_id}: {e}")
        comments = []
    
    # Write output file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\n")
            f.write(f"Title: {title}\n\n")
            
            f.write("--- TRANSCRIPT ---\n")
            if transcript_text:
                f.write(transcript_text)
            else:
                f.write("Transcript: Not available\n")
            
            f.write("\n\n--- COMMENTS ---\n")
            if comments:
                for comment in comments:
                    f.write(f"{comment}\n\n")
            else:
                f.write("Comments: Not available\n")
        
        print(f"Successfully processed {video_id}: {output_path}")
        return True
    except Exception as e:
        print(f"Error: Failed to write output file for {video_id}: {e}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Process YouTube videos from videos.txt and generate text files with metadata, transcripts, and comments."
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("YOUTUBE_API_KEY", ""),
        help="YouTube Data API key (or set YOUTUBE_API_KEY env var).",
    )
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parser.add_argument(
        "--videos-file",
        default=os.path.join(script_dir, "videos.txt"),
        help="Path to file containing YouTube URLs/IDs (one per line). Default: videos.txt in script directory",
    )
    parser.add_argument(
        "--results-dir",
        default=os.path.join(script_dir, "results"),
        help="Directory to save output text files. Default: results in script directory",
    )
    parser.add_argument(
        "--language",
        default="",
        help="Preferred language code for transcripts (e.g., en or en-US). Default: uses first available.",
    )
    parser.add_argument(
        "--max-comment-pages",
        type=int,
        default=50,
        help="Maximum number of comment pages to fetch per video (100 comments per page). Default: 50",
    )

    args = parser.parse_args()

    api_key = args.api_key.strip()
    if not api_key:
        raise SystemExit(
            "Missing API key. Provide --api-key or set env var YOUTUBE_API_KEY."
        )

    videos_file = args.videos_file
    if not os.path.exists(videos_file):
        raise SystemExit(f"Videos file not found: {videos_file}")

    results_dir = args.results_dir
    os.makedirs(results_dir, exist_ok=True)

    # Read video IDs/URLs from file
    video_ids = []
    with open(videos_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            video_id = extract_video_id(line)
            if video_id:
                video_ids.append(video_id)
            else:
                print(f"Warning: Skipping invalid line {line_num}: {line.strip()}")

    if not video_ids:
        raise SystemExit(f"No valid video IDs found in {videos_file}")

    print(f"Processing {len(video_ids)} video(s)...")

    # Process each video
    success_count = 0
    for video_id in video_ids:
        if process_video(
            api_key=api_key,
            video_id=video_id,
            results_dir=results_dir,
            language=args.language,
            max_comment_pages=args.max_comment_pages,
        ):
            success_count += 1

    print(f"\nCompleted: {success_count}/{len(video_ids)} video(s) processed successfully.")


if __name__ == "__main__":
    main()

