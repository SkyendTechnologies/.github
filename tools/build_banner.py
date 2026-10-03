from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "profile" / "assets" / "logo.png"
OUTPUT = ROOT / "profile" / "assets" / "banner.png"

W, H = 1600, 520
img = Image.new("RGB", (W, H), (4, 8, 17))
px = img.load()

for y in range(H):
    for x in range(W):
        t = (x / W) * 0.55 + (y / H) * 0.15
        base = (int(4 + 2 * t), int(8 + 8 * t), int(17 + 13 * t))
        dx = (x - 1220) / 520
        dy = (y - 225) / 330
        glow = max(0.0, 1.0 - math.sqrt(dx * dx + dy * dy))
        px[x, y] = (
            min(255, int(base[0] + 15 * glow)),
            min(255, int(base[1] + 44 * glow)),
            min(255, int(base[2] + 78 * glow)),
        )

draw = ImageDraw.Draw(img, "RGBA")

for bbox, start, end, fill, width in [
    ((690, -95, 1665, 500), 195, 342, (112, 181, 255, 95), 2),
    ((850, 105, 1710, 650), 195, 340, (112, 181, 255, 60), 2),
    ((960, -120, 1740, 660), 110, 260, (112, 181, 255, 40), 2),
]:
    draw.arc(bbox, start=start, end=end, fill=fill, width=width)

for x, y, r, alpha in [
    (1050, 92, 3, 160),
    (1290, 151, 2, 120),
    (1425, 74, 2, 120),
    (1185, 350, 2, 110),
    (1510, 330, 3, 140),
    (946, 402, 2, 100),
]:
    draw.ellipse((x-r, y-r, x+r, y+r), fill=(175, 218, 255, alpha))

# Original Skyend logo, slightly larger than the previous banner.
logo = Image.open(LOGO).convert("RGBA")
logo.thumbnail((148, 148), Image.Resampling.LANCZOS)
logo_x = 92
logo_y = 54 + (148 - logo.height) // 2
img.paste(logo, (logo_x, logo_y), logo)

brand_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 29)
tag_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

draw.text(
    (274, 96),
    "SKYEND TECHNOLOGIES",
    font=brand_font,
    fill=(169, 211, 247, 255),
)

draw.text(
    (96, 236),
    "Engineering secure,",
    font=tag_font,
    fill=(244, 248, 255, 255),
)
draw.text(
    (96, 296),
    "verifiable, distributed systems.",
    font=tag_font,
    fill=(244, 248, 255, 255),
)

draw.rounded_rectangle(
    (96, 365, 246, 367),
    radius=1,
    fill=(118, 185, 245, 220),
)

draw.text(
    (96, 398),
    "SECURITY  ·  CRYPTOGRAPHY  ·  DISTRIBUTED SYSTEMS  ·  INTELLIGENT SOFTWARE",
    font=small_font,
    fill=(168, 190, 214, 255),
)

draw.rounded_rectangle(
    (1, 1, W-2, H-2),
    radius=27,
    outline=(100, 150, 210, 40),
    width=2,
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUTPUT, "PNG", optimize=True, compress_level=9)
print(f"Generated {OUTPUT}")
