import argparse
import os
import subprocess
from dataclasses import dataclass
from typing import Optional

from misc.download_partial.video_processor import process_steps


_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_THIS_DIR, '..', '..'))


@dataclass
class ProcessOptions:
    crop_left: float = 0.2
    crop_right: float = 0.2
    crop_top: float = 0.0
    crop_bottom: float = 0.0
    target_aspect_w: int = 9
    target_aspect_h: int = 16
    top_ratio: float = 0.6
    final_width: int = 1080
    final_height: int = 1920
    gap_px: int = 8
    logo_path: str = os.path.join(_REPO_ROOT, 'misc', 'img', 'BB_logo_and_name-transparent-with-color.png')
    title_path: str = os.path.join(_REPO_ROOT, 'misc', 'img', 'title.png')


def _compute_title_y_expr(
    video_path: str,
    *,
    crop_left: float,
    crop_right: float,
    crop_top: float = 0.0,
    crop_bottom: float = 0.0,
    target_aspect_w: int = 9,
    target_aspect_h: int = 16,
    top_ratio: float = 0.5,
    final_width: int = 1080,
    gap_px: int = 8,
) -> str:
    """Return an ffmpeg y-expression that places the overlay right above the video."""
    try:
        probe_cmd = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height', '-of', 'csv=p=0:s=x',
            video_path,
        ]
        probe_out = subprocess.check_output(probe_cmd).decode('utf-8').strip()
        src_w, src_h = [int(x) for x in probe_out.split('x')]
    except Exception:
        src_w, src_h = 1920, 1080

    cropped_w = src_w * max(0.0, (1.0 - crop_left - crop_right))
    cropped_h = src_h * max(0.0, (1.0 - crop_top - crop_bottom))
    cropped_ratio = (cropped_h / cropped_w) if cropped_w else 0.0

    target_ratio = float(target_aspect_h) / float(target_aspect_w)
    toppad_px = max(0.0, (target_ratio - cropped_ratio) * float(top_ratio) * float(final_width))
    return f"{int(round(toppad_px))}-overlay_h-{int(gap_px)}"


def process_video(input_path: str, output_path: Optional[str] = None, options: ProcessOptions = ProcessOptions()) -> str:
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input video not found: {input_path}")

    title_y_expr = _compute_title_y_expr(
        input_path,
        crop_left=options.crop_left,
        crop_right=options.crop_right,
        crop_top=options.crop_top,
        crop_bottom=options.crop_bottom,
        target_aspect_w=options.target_aspect_w,
        target_aspect_h=options.target_aspect_h,
        top_ratio=options.top_ratio,
        final_width=options.final_width,
        gap_px=options.gap_px,
    )

    steps = [
        {"op": "crop", "params": {"left": options.crop_left, "right": options.crop_right}},
        {"op": "overlay", "params": {"path": options.logo_path, "position": "bottom-right", "margin": 16, "scale": {"factor": 0.75}}},
        {"op": "pad_to_aspect", "params": {"w": options.target_aspect_w, "h": options.target_aspect_h, "color": "black", "top_ratio": options.top_ratio}},
        {"op": "resize", "params": {"width": options.final_width, "height": options.final_height, "keep_aspect": False}},
        {"op": "overlay", "params": {"path": options.title_path, "x": "(main_w-overlay_w)/2", "y": title_y_expr, "scale": {"width": options.final_width}}},
    ]

    base, ext = os.path.splitext(input_path)
    out_path = output_path or f"{base}-done{ext}"
    out_dir = os.path.dirname(out_path)
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    return process_steps(input_path, out_path, steps)


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Process a downloaded video into final format.')
    p.add_argument('input', help='Input video path')
    p.add_argument('--out', dest='output', default=None, help='Output video path (defaults to <input>-done.mp4)')
    p.add_argument('--logo', default=None, help='Override logo path')
    p.add_argument('--title', default=None, help='Override title image path')
    p.add_argument('--crop-left', type=float, default=None)
    p.add_argument('--crop-right', type=float, default=None)
    p.add_argument('--top-ratio', type=float, default=None)
    p.add_argument('--width', type=int, default=None)
    p.add_argument('--height', type=int, default=None)
    return p


def _main() -> None:
    args = _build_arg_parser().parse_args()
    opts = ProcessOptions()
    if args.logo:
        opts.logo_path = args.logo
    if args.title:
        opts.title_path = args.title
    if args.crop_left is not None:
        opts.crop_left = args.crop_left
    if args.crop_right is not None:
        opts.crop_right = args.crop_right
    if args.top_ratio is not None:
        opts.top_ratio = args.top_ratio
    if args.width is not None:
        opts.final_width = args.width
    if args.height is not None:
        opts.final_height = args.height

    out_path = process_video(args.input, args.output, opts)
    print(out_path)


if __name__ == '__main__':
    _main()


