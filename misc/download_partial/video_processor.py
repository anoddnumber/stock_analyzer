import os
import shlex
import subprocess
from typing import Any, Dict, List, Optional, Tuple


def _resolve_default_logo() -> str:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(repo_root, "misc", "img", "BB_logo_and_name-transparent-with-color.png")


def _is_fraction(value: float) -> bool:
    return isinstance(value, (int, float)) and 0.0 <= float(value) <= 1.0


def _even_expr(expr: str) -> str:
    # Ensure even integers for codecs like H.264. trunc(expr/2)*2 yields nearest even <= expr.
    return f"trunc(({expr})/2)*2"


def _build_crop_filter(crop: Dict[str, Any], in_label: str, out_label: str) -> str:
    # Supports either {x,y,width,height} OR {left,right,top,bottom}.
    if all(k in crop for k in ("x", "y", "width", "height")):
        x = crop["x"]
        y = crop["y"]
        w = crop["width"]
        h = crop["height"]
        x_expr = f"iw*{x}" if isinstance(x, float) and _is_fraction(x) else str(int(x))
        y_expr = f"ih*{y}" if isinstance(y, float) and _is_fraction(y) else str(int(y))
        w_expr = f"iw*{w}" if isinstance(w, float) and _is_fraction(w) else str(int(w))
        h_expr = f"ih*{h}" if isinstance(h, float) and _is_fraction(h) else str(int(h))
    else:
        left = crop.get("left", 0)
        right = crop.get("right", 0)
        top = crop.get("top", 0)
        bottom = crop.get("bottom", 0)

        def v_to_expr(v: Any, axis: str) -> str:
            if isinstance(v, float) and _is_fraction(v):
                return f"i{axis}*{v}"
            return str(int(v))

        left_expr = v_to_expr(left, "w")
        right_expr = v_to_expr(right, "w")
        top_expr = v_to_expr(top, "h")
        bottom_expr = v_to_expr(bottom, "h")

        # width = iw - left - right; height = ih - top - bottom
        x_expr = left_expr
        y_expr = top_expr
        w_expr = f"iw-({left_expr})-({right_expr})"
        h_expr = f"ih-({top_expr})-({bottom_expr})"

    w_expr = _even_expr(w_expr)
    h_expr = _even_expr(h_expr)
    return f"[{in_label}]crop={w_expr}:{h_expr}:{x_expr}:{y_expr}[{out_label}]"


def _build_resize_filter(resize: Dict[str, Any], in_label: str, out_label: str) -> Optional[str]:
    if not resize:
        return None
    keep_aspect = bool(resize.get("keep_aspect", True))
    width = resize.get("width")
    height = resize.get("height")

    if width and height:
        if keep_aspect:
            # Prefer fitting width; keep aspect using -2 for even rounding
            return f"[{in_label}]scale={int(width)}:-2[{out_label}]"
        return f"[{in_label}]scale={int(width)}:{int(height)}[{out_label}]"
    if width and not height:
        return f"[{in_label}]scale={int(width)}:-2[{out_label}]"
    if height and not width:
        return f"[{in_label}]scale=-2:{int(height)}[{out_label}]"
    return None


def _build_pad_to_aspect_filter(pad: Dict[str, Any], in_label: str, out_label: str) -> str:
    """
    Pad vertically to reach a target aspect ratio (e.g., 9:16) with black bars.

    Expects params: {"w": 9, "h": 16, "color": "black"}
    This implementation pads height to (iw * h / w), centering the input.
    """
    aw = int(pad.get("w", 9))
    ah = int(pad.get("h", 16))
    color = pad.get("color", "black")

    width_expr = _even_expr('iw')
    height_expr = _even_expr(f"iw*{ah}/{aw}")
    x_expr = "(ow-iw)/2"
    y_expr = "(oh-ih)/2"

    return f"[{in_label}]pad={width_expr}:{height_expr}:{x_expr}:{y_expr}:color={color}[{out_label}]"


def _overlay_position_expr(position: str, margin: int) -> (str, str):
    p = (position or "bottom-right").lower()
    m = int(margin)
    if p == "top-left":
        return str(m), str(m)
    if p == "top-right":
        return f"main_w-overlay_w-{m}", str(m)
    if p == "bottom-left":
        return str(m), f"main_h-overlay_h-{m}"
    if p == "center":
        return "(main_w-overlay_w)/2", "(main_h-overlay_h)/2"
    # default bottom-right
    return f"main_w-overlay_w-{m}", f"main_h-overlay_h-{m}"


def _build_overlay_chain(idx: int, overlay: Dict[str, Any], base_label: str, out_label: str) -> Tuple[str, List[str]]:
    # Returns (filter_string, additional_inputs)
    path = overlay.get("path")
    if not path:
        raise ValueError("overlay dict requires 'path'")
    add_inputs = ["-i", path]

    img_label_in = f"{idx}:v"
    work_label = f"ov{idx}"
    steps: List[str] = []

    # Optional scale
    scale_opt = overlay.get("scale")
    if isinstance(scale_opt, dict):
        if "factor" in scale_opt:
            factor = float(scale_opt["factor"])
            steps.append(f"[{img_label_in}]scale=iw*{factor}:ih*{factor}[{work_label}]")
        elif "width" in scale_opt and "height" in scale_opt:
            steps.append(f"[{img_label_in}]scale={int(scale_opt['width'])}:{int(scale_opt['height'])}[{work_label}]")
        elif "width" in scale_opt:
            steps.append(f"[{img_label_in}]scale={int(scale_opt['width'])}:-1[{work_label}]")
        elif "height" in scale_opt:
            steps.append(f"[{img_label_in}]scale=-1:{int(scale_opt['height'])}[{work_label}]")
        else:
            steps.append(f"[{img_label_in}]null[{work_label}]")
    else:
        steps.append(f"[{img_label_in}]null[{work_label}]")

    # Optional opacity
    opacity = overlay.get("opacity")
    if opacity is not None and float(opacity) < 1.0:
        prev = work_label
        work_label = f"ov{idx}o"
        steps.append(f"[{prev}]format=rgba,colorchannelmixer=aa={float(opacity):.4f}[{work_label}]")

    # Positioning
    margin = int(overlay.get("margin", 16))
    if "x" in overlay and "y" in overlay:
        x_expr = str(overlay["x"]) if isinstance(overlay["x"], int) else str(overlay["x"]).strip()
        y_expr = str(overlay["y"]) if isinstance(overlay["y"], int) else str(overlay["y"]).strip()
    else:
        x_expr, y_expr = _overlay_position_expr(overlay.get("position", "bottom-right"), margin)

    steps.append(f"[{base_label}][{work_label}]overlay={x_expr}:{y_expr}[{out_label}]")
    return ";".join(steps), add_inputs


def _build_filter_complex(
    crop: Optional[Dict[str, Any]],
    resize: Optional[Dict[str, Any]],
    overlays: Optional[List[Dict[str, Any]]]
) -> Tuple[str, List[str]]:
    parts: List[str] = []
    input_args: List[str] = []

    current = "0:v"
    next_label_id = 0

    if crop:
        out_label = f"v{next_label_id}"
        next_label_id += 1
        parts.append(_build_crop_filter(crop, current, out_label))
        current = out_label
    else:
        # pass-through
        out_label = f"v{next_label_id}"
        next_label_id += 1
        parts.append(f"[{current}]null[{out_label}]")
        current = out_label

    if resize:
        out_label = f"v{next_label_id}"
        next_label_id += 1
        rf = _build_resize_filter(resize, current, out_label)
        if rf:
            parts.append(rf)
            current = out_label

    if overlays:
        for i, ov in enumerate(overlays, start=1):
            out_label = f"v{next_label_id}"
            next_label_id += 1
            chain, add_in = _build_overlay_chain(i, ov, current, out_label)
            input_args.extend(add_in)
            parts.append(chain)
            current = out_label

    # Final ensure even dimensions to avoid codec errors
    out_label = "vout"
    parts.append(f"[{current}]scale={_even_expr('iw')}:{_even_expr('ih')}[{out_label}]")

    return ";".join(parts), input_args


def build_ffmpeg_command(
    input_path: str,
    output_path: str,
    *,
    crop: Optional[Dict[str, Any]] = None,
    resize: Optional[Dict[str, Any]] = None,
    overlays: Optional[List[Dict[str, Any]]] = None,
    codec: str = "libx264",
    crf: int = 18,
    preset: str = "medium",
    pix_fmt: str = "yuv420p",
    faststart: bool = True,
    audio_copy: bool = True,
) -> List[str]:
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input video not found: {input_path}")

    filter_complex, extra_inputs = _build_filter_complex(crop, resize, overlays)

    cmd: List[str] = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        *extra_inputs,
        "-filter_complex",
        filter_complex,
        "-map",
        "[vout]",
        "-map",
        "0:a?",
        "-c:v",
        codec,
        "-crf",
        str(int(crf)),
        "-preset",
        preset,
        "-pix_fmt",
        pix_fmt,
    ]

    if faststart:
        cmd += ["-movflags", "+faststart"]

    if audio_copy:
        cmd += ["-c:a", "copy"]

    cmd += [output_path]
    return cmd


def process_video(
    input_path: str,
    output_path: str,
    *,
    crop: Optional[Dict[str, Any]] = None,
    resize: Optional[Dict[str, Any]] = None,
    overlays: Optional[List[Dict[str, Any]]] = None,
    codec: str = "libx264",
    crf: int = 18,
    preset: str = "medium",
    pix_fmt: str = "yuv420p",
    faststart: bool = True,
    audio_copy: bool = True,
) -> str:
    cmd = build_ffmpeg_command(
        input_path=input_path,
        output_path=output_path,
        crop=crop,
        resize=resize,
        overlays=overlays,
        codec=codec,
        crf=crf,
        preset=preset,
        pix_fmt=pix_fmt,
        faststart=faststart,
        audio_copy=audio_copy,
    )
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        # Surface ffmpeg stderr for debugging
        raise RuntimeError(proc.stderr.decode("utf-8", errors="ignore"))
    return output_path


def _derive_output_path(input_path: str, suffix: str) -> str:
    base, ext = os.path.splitext(input_path)
    return f"{base}{suffix}{ext}"


def _build_filter_complex_from_steps(steps: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
    """
    Build a filter_complex string from an ordered list of steps.

    Each step is a dict with keys:
      {"op": "crop"|"resize"|"overlay", "params": {...}}

    Returns (filter_complex, extra_input_args)
    """
    parts: List[str] = []
    input_args: List[str] = []

    current = "0:v"
    next_label_id = 0
    overlay_input_idx = 1  # [1:v], [2:v], ... for additional -i inputs

    if not steps:
        out_label = "vout"
        parts.append(f"[{current}]scale={_even_expr('iw')}:{_even_expr('ih')}[{out_label}]")
        return ";".join(parts), input_args

    for step in steps:
        op = (step.get("op") or "").lower()
        params = step.get("params") or {}
        out_label = f"v{next_label_id}"
        next_label_id += 1

        if op == "crop":
            parts.append(_build_crop_filter(params, current, out_label))
            current = out_label
        elif op == "pad_to_aspect":
            parts.append(_build_pad_to_aspect_filter(params, current, out_label))
            current = out_label
        elif op == "resize":
            rf = _build_resize_filter(params, current, out_label)
            if rf:
                parts.append(rf)
                current = out_label
        elif op == "overlay":
            chain, add_in = _build_overlay_chain(overlay_input_idx, params, current, out_label)
            input_args.extend(add_in)
            parts.append(chain)
            current = out_label
            overlay_input_idx += 1
        elif op in ("null", "noop", "passthrough"):
            parts.append(f"[{current}]null[{out_label}]")
            current = out_label
        else:
            raise ValueError(f"Unsupported operation in steps: {op}")

    # Final ensure even dimensions
    out_label = "vout"
    parts.append(f"[{current}]scale={_even_expr('iw')}:{_even_expr('ih')}[{out_label}]")
    return ";".join(parts), input_args


def build_ffmpeg_command_from_steps(
    input_path: str,
    output_path: str,
    steps: List[Dict[str, Any]],
    *,
    codec: str = "libx264",
    crf: int = 18,
    preset: str = "medium",
    pix_fmt: str = "yuv420p",
    faststart: bool = True,
    audio_copy: bool = True,
) -> List[str]:
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input video not found: {input_path}")

    filter_complex, extra_inputs = _build_filter_complex_from_steps(steps)

    cmd: List[str] = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        *extra_inputs,
        "-filter_complex",
        filter_complex,
        "-map",
        "[vout]",
        "-map",
        "0:a?",
        "-c:v",
        codec,
        "-crf",
        str(int(crf)),
        "-preset",
        preset,
        "-pix_fmt",
        pix_fmt,
    ]

    if faststart:
        cmd += ["-movflags", "+faststart"]

    if audio_copy:
        cmd += ["-c:a", "copy"]

    cmd += [output_path]
    return cmd


def process_steps(
    input_path: str,
    output_path: str,
    steps: List[Dict[str, Any]],
    *,
    codec: str = "libx264",
    crf: int = 18,
    preset: str = "medium",
    pix_fmt: str = "yuv420p",
    faststart: bool = True,
    audio_copy: bool = True,
) -> str:
    """
    Execute an ordered pipeline of operations in a single ffmpeg run.

    Example steps:
        steps=[
            {"op": "crop", "params": {"left": 0.12, "right": 0.12}},
            {"op": "overlay", "params": {"path": "logo.png", "position": "top-right", "margin": 24}},
            {"op": "resize", "params": {"width": 1920, "keep_aspect": True}},
        ]
    """
    cmd = build_ffmpeg_command_from_steps(
        input_path=input_path,
        output_path=output_path,
        steps=steps,
        codec=codec,
        crf=crf,
        preset=preset,
        pix_fmt=pix_fmt,
        faststart=faststart,
        audio_copy=audio_copy,
    )
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="ignore"))
    return output_path


def add_logo_watermark(
    input_path: str,
    output_path: Optional[str] = None,
    *,
    margin_px: int = 16,
    crop_percent: Optional[float] = None,
    logo_path: Optional[str] = None,
    logo_scale: float = 0.75,
) -> str:
    if output_path is None:
        output_path = _derive_output_path(input_path, "-watermarked")

    if logo_path is None:
        logo_path = _resolve_default_logo()

    crop_cfg = None
    if crop_percent is not None:
        # Remove from left/right equally; no vertical crop by default
        cp = float(crop_percent)
        crop_cfg = {"left": cp, "right": cp, "top": 0, "bottom": 0}

    overlays = [
        {
            "path": logo_path,
            "position": "bottom-right",
            "margin": int(margin_px),
            "scale": {"factor": float(logo_scale)},
        }
    ]

    # Backward-compatible wrapper implemented via ordered steps
    steps: List[Dict[str, Any]] = []
    if crop_cfg:
        steps.append({"op": "crop", "params": crop_cfg})
    steps.append({"op": "overlay", "params": overlays[0]})

    return process_steps(
        input_path=input_path,
        output_path=output_path,
        steps=steps,
    )


class VideoPipeline:
    """
    Builder for composing ordered video operations and executing them in a
    single ffmpeg run. Example:

        pipeline = (
            VideoPipeline()
            .crop(left=0.12, right=0.12)
            .overlay(path="logo.png", position="top-right", margin=24)
            .resize(width=1920, keep_aspect=True)
        )
        pipeline.process("in.mp4", "out.mp4")
    """

    def __init__(self) -> None:
        self._steps: List[Dict[str, Any]] = []

    def crop(
        self,
        *,
        left: Optional[float] = None,
        right: Optional[float] = None,
        top: Optional[float] = None,
        bottom: Optional[float] = None,
        x: Optional[int] = None,
        y: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> "VideoPipeline":
        params: Dict[str, Any] = {}
        if any(v is not None for v in (x, y, width, height)):
            if None in (x, y, width, height):
                raise ValueError("When using x,y,width,height all four must be provided")
            params.update({"x": x, "y": y, "width": width, "height": height})
        else:
            params.update({
                "left": left or 0,
                "right": right or 0,
                "top": top or 0,
                "bottom": bottom or 0,
            })
        self._steps.append({"op": "crop", "params": params})
        return self

    def resize(
        self,
        *,
        width: Optional[int] = None,
        height: Optional[int] = None,
        keep_aspect: bool = True,
    ) -> "VideoPipeline":
        params: Dict[str, Any] = {"keep_aspect": keep_aspect}
        if width is not None:
            params["width"] = width
        if height is not None:
            params["height"] = height
        self._steps.append({"op": "resize", "params": params})
        return self

    def overlay(
        self,
        *,
        path: str,
        position: Optional[str] = None,
        margin: int = 16,
        x: Optional[str] = None,
        y: Optional[str] = None,
        opacity: Optional[float] = None,
        scale: Optional[Dict[str, Any]] = None,
    ) -> "VideoPipeline":
        params: Dict[str, Any] = {"path": path, "margin": margin}
        if position is not None:
            params["position"] = position
        if x is not None and y is not None:
            params["x"] = x
            params["y"] = y
        if opacity is not None:
            params["opacity"] = float(opacity)
        if scale is not None:
            params["scale"] = scale
        self._steps.append({"op": "overlay", "params": params})
        return self

    def pad_to_aspect(
        self,
        *,
        w: int = 9,
        h: int = 16,
        color: str = "black",
    ) -> "VideoPipeline":
        self._steps.append({
            "op": "pad_to_aspect",
            "params": {"w": int(w), "h": int(h), "color": color},
        })
        return self

    def process(
        self,
        input_path: str,
        output_path: str,
        *,
        codec: str = "libx264",
        crf: int = 18,
        preset: str = "medium",
        pix_fmt: str = "yuv420p",
        faststart: bool = True,
        audio_copy: bool = True,
    ) -> str:
        return process_steps(
            input_path=input_path,
            output_path=output_path,
            steps=self._steps,
            codec=codec,
            crf=crf,
            preset=preset,
            pix_fmt=pix_fmt,
            faststart=faststart,
            audio_copy=audio_copy,
        )


