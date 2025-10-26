from PIL import Image, ImageDraw, ImageFont
import sys
import os
import argparse

# --- CONFIG ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_IMAGE = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "img", "base_fault_or_not_title.png"))
FONT_PATH = os.path.normpath(os.path.join(SCRIPT_DIR, "fonts", "gotham-bold.ttf"))  # change if font file name differs
OUTPUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "img"))
TEXT_COLOR = (255, 255, 255, 255)  # white
FONT_SIZE = 260  # adjust as needed
TEXT_SCALE = 0.4  # scale factor for text size
BACKGROUND_FILL_COLOR = (0, 0, 0, 255)  # black fill behind text
BOTTOM_MARGIN = 20  # distance from bottom of image to baseline area
TEXT_PADDING = 10  # extra pixels padding around text background
# ---------------

def create_title_image(number, base_image_path=None, output_path=None):
    # Load image
    base_path = base_image_path or BASE_IMAGE
    img = Image.open(base_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Load font
    try:
        effective_font_size = max(1, int(FONT_SIZE * TEXT_SCALE))
        font = ImageFont.truetype(FONT_PATH, effective_font_size)
    except Exception:
        print(f"⚠️ Could not load Gotham font at: {FONT_PATH}. Using default instead.")
        font = ImageFont.load_default()

    text = f"#{number}"
    W, H = img.size
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # Center the text horizontally, place near bottom
    x = (W - w) / 2
    y = H - h - BOTTOM_MARGIN

    # Fill background where text will be drawn, with padding
    text_area_bbox = draw.textbbox((x, y), text, font=font)
    x0, y0, x1, y1 = text_area_bbox
    x0 = max(0, int(x0 - TEXT_PADDING))
    y0 = max(0, int(y0 - TEXT_PADDING))
    x1 = min(W, int(x1 + TEXT_PADDING))
    y1 = min(H, int(y1 + TEXT_PADDING))
    draw.rectangle([x0, y0, x1, y1], fill=BACKGROUND_FILL_COLOR)

    # Draw text on top
    draw.text((x, y), text, font=font, fill=TEXT_COLOR)

    # Determine output path
    if output_path:
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.isdir(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        final_out = output_path
    else:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        final_out = os.path.join(OUTPUT_DIR, f"title_{number}.png")

    img.save(final_out)
    print(f"✅ Saved {final_out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a title image with a number overlay.")
    parser.add_argument("number", help="Number to render inside the title (e.g., 56)")
    parser.add_argument("--base", dest="base", default=None, help="Path to base title image to use")
    parser.add_argument("--out", dest="out", default=None, help="Output file path for the generated title image")
    args = parser.parse_args()

    create_title_image(args.number, args.base, args.out)