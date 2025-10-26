import os
import subprocess
from typing import List


def concat_segments(
    segments: List[str],
    out_path: str,
    *,
    video_codec: str = "libx264",
    crf: int = 18,
    preset: str = "medium",
    audio_codec: str = "aac",
    audio_bitrate: str = "192k",
) -> str:
    """
    Concatenate multiple media segments into a single output using ffmpeg.

    The implementation re-encodes using a concat filtergraph and resets PTS for
    each input (both video and audio) to avoid timestamp/keyframe issues (e.g.,
    initial black frames). Returns the output path on success; raises
    RuntimeError on failure.

    Args:
        segments: Absolute or relative paths to input segments, in order.
        out_path: Target output path.
        video_codec: Video codec to use for encoding (default: libx264).
        crf: Constant Rate Factor for video quality (lower is better, default 18).
        preset: x264 preset (e.g., veryslow..ultrafast). Default "medium".
        audio_codec: Audio codec to use (default: aac).
        audio_bitrate: Audio bitrate (default: 192k).

    Returns:
        The absolute path to the produced file.

    Raises:
        ValueError: If no segments are provided.
        RuntimeError: If ffmpeg fails or the output is not produced.
    """
    if not segments:
        raise ValueError("No segments to concatenate")

    out_dir = os.path.dirname(out_path) or os.getcwd()
    os.makedirs(out_dir, exist_ok=True)

    inputs: List[str] = []
    for p in segments:
        inputs += ["-i", p]

    n = len(segments)

    # Normalize PTS for each input to ensure each stream starts at 0
    pre_filters: List[str] = []
    for i in range(n):
        pre_filters.append(f"[{i}:v:0]setpts=PTS-STARTPTS[v{i}]")
        pre_filters.append(f"[{i}:a:0]asetpts=PTS-STARTPTS[a{i}]")

    av_pairs = "".join(f"[v{i}][a{i}]" for i in range(n))
    filter_complex = ";".join(pre_filters + [f"{av_pairs}concat=n={n}:v=1:a=1[v][a]"])

    cmd = [
        "ffmpeg",
        "-y",
        *inputs,
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-c:v",
        video_codec,
        "-crf",
        str(int(crf)),
        "-preset",
        preset,
        "-c:a",
        audio_codec,
        "-b:a",
        audio_bitrate,
        out_path,
    ]

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0 or not os.path.isfile(out_path):
        raise RuntimeError(proc.stderr.decode("utf-8", errors="ignore"))
    return os.path.abspath(out_path)


