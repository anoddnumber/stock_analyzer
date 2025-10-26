from PIL import Image, ImageDraw, ImageFont
import sys
import os

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

def create_title_image(number):
    # Load image
    img = Image.open(BASE_IMAGE).convert("RGBA")
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

    # Make output folder
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"title_{number}.png")
    img.save(out_path)
    print(f"✅ Saved {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_title.py <number>")
    else:
        create_title_image(sys.argv[1])