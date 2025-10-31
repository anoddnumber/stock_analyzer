# YouTube Scripts

This directory contains scripts for working with YouTube data using the YouTube Data API and `youtube-transcript-api`.

## Scripts

1. **`youtube_transcript_download.py`** - Download SRT transcripts for public YouTube videos
2. **`youtube_bwf_popular.py`** - Fetch most popular videos from a YouTube channel

## Installation

### Requirements

Both scripts require Python 3 and the following packages:

```bash
pip install requests youtube-transcript-api
```

### YouTube Data API Setup (for `youtube_bwf_popular.py`)

For the popular videos script, you'll need a YouTube Data API v3 key:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3**
4. Create credentials (API Key)
5. Set the API key as an environment variable:
   ```bash
   export YOUTUBE_API_KEY="your-api-key-here"
   ```
   Or pass it directly via `--api-key` argument

## Usage

### 1. Download Video Transcripts

**Script:** `youtube_transcript_download.py`

Downloads SRT subtitle files for public YouTube videos. Works for any video with captions enabled (no OAuth required).

#### Basic Usage

```bash
# Using video URL
python misc/youtube/youtube_transcript_download.py --url "https://www.youtube.com/watch?v=HHW4fSmS7WI" --language en

# Using video ID
python misc/youtube/youtube_transcript_download.py --video-id HHW4fSmS7WI --language en
```

#### Arguments

- `--video-id VIDEO_ID` - YouTube video ID (alternative to `--url`)
- `--url URL` - YouTube video URL (supports `youtube.com/watch?v=...` or `youtu.be/...`)
- `--language LANG` - Preferred language code (e.g., `en`, `en-US`). Optional. If not provided, defaults to English or first available language.
- `--out-dir PATH` - Directory to save SRT files (default: `misc/youtube/transcripts`)

#### Examples

```bash
# Download English transcript
python misc/youtube/youtube_transcript_download.py --url "https://www.youtube.com/watch?v=HHW4fSmS7WI" --language en

# Download Spanish transcript
python misc/youtube/youtube_transcript_download.py --video-id HHW4fSmS7WI --language es

# Download without specifying language (uses default/available)
python misc/youtube/youtube_transcript_download.py --url "https://www.youtube.com/watch?v=HHW4fSmS7WI"

# Custom output directory
python misc/youtube/youtube_transcript_download.py --url "https://www.youtube.com/watch?v=HHW4fSmS7WI" --out-dir ./my_transcripts
```

#### Output

Transcripts are saved as SRT files in the specified output directory (default: `misc/youtube/transcripts/`).

Format: `<videoId>.<languageCode>.srt`

Example: `HHW4fSmS7WI.en.srt`

#### Error Handling

- **Transcripts disabled**: The video doesn't have captions enabled
- **No transcripts found**: No captions available for the requested language (or any language)
- **Failed to fetch**: Network or API errors

---

### 2. Fetch Popular Videos from a Channel

**Script:** `youtube_bwf_popular.py`

Fetches videos from a YouTube channel's uploads playlist and displays them sorted by view count. Defaults to the BWF (Badminton World Federation) channel.

#### Basic Usage

```bash
# Using default channel (@BWF)
python misc/youtube/youtube_bwf_popular.py --api-key YOUR_API_KEY

# Using environment variable
export YOUTUBE_API_KEY="your-api-key"
python misc/youtube/youtube_bwf_popular.py

# Custom channel and results
python misc/youtube/youtube_bwf_popular.py --api-key YOUR_API_KEY --handle "@MyChannel" --max-results 50
```

#### Arguments

- `--api-key KEY` - YouTube Data API v3 key (or set `YOUTUBE_API_KEY` environment variable)
- `--handle HANDLE` - Channel handle (e.g., `@BWF`). Default: `@BWF`
- `--max-results N` - Maximum number of videos to return (default: 25, max: 50 per page)
- `--pages N` - Number of pages to traverse (default: 1, each page has up to 50 results)

#### Examples

```bash
# Get top 25 videos from BWF channel
python misc/youtube/youtube_bwf_popular.py --api-key YOUR_API_KEY

# Get top 50 videos from a custom channel
python misc/youtube/youtube_bwf_popular.py --api-key YOUR_API_KEY --handle "@MyChannel" --max-results 50

# Get more results by fetching multiple pages
python misc/youtube/youtube_bwf_popular.py --api-key YOUR_API_KEY --max-results 100 --pages 2
```

#### Output Format

The script prints a table with the following columns:
- View count (right-aligned)
- Publication date (YYYY-MM-DD)
- Video title
- YouTube URL

Example output:
```
    12345678  2024-01-15  Amazing Badminton Rally  https://www.youtube.com/watch?v=abc123
     9876543  2024-01-10  Epic Match Highlights    https://www.youtube.com/watch?v=xyz789
```

---

## Output Directories

- **Transcripts**: `misc/youtube/transcripts/` (default for transcript downloads)
- Videos list is printed to stdout (can be redirected to a file)

## Notes

- **Transcript Script**: Works for any public video with captions. No authentication required.
- **Popular Videos Script**: Requires a YouTube Data API v3 key. Free tier has quota limits (10,000 units per day).
- Both scripts support standard YouTube URL formats (`youtube.com/watch?v=...` and `youtu.be/...`)

## Troubleshooting

### Transcript Script

- **"No transcripts found"**: The video may not have captions enabled, or the requested language isn't available
- **"Failed to fetch transcript"**: Check your internet connection or try again later (rate limiting)

### Popular Videos Script

- **"Missing API key"**: Set `YOUTUBE_API_KEY` environment variable or provide `--api-key`
- **"No channel found"**: Verify the channel handle is correct (include the `@` symbol)
- **API quota exceeded**: Wait until your daily quota resets or upgrade your API plan

