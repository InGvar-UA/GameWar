"""Build the GameWar social card from its generated background artwork."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "assets" / "og-background.png"
TARGET = ROOT / "assets" / "og-gamewar.jpg"

image = Image.open(SOURCE).convert("RGB")
width, height = image.size
target_ratio = 1200 / 630
if width / height > target_ratio:
    cropped_width = round(height * target_ratio)
    image = image.crop((0, 0, cropped_width, height))
else:
    cropped_height = round(width / target_ratio)
    image = image.crop((0, 0, width, cropped_height))
image = image.resize((1200, 630), Image.Resampling.LANCZOS)

overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
shade = ImageDraw.Draw(overlay)
for x in range(690):
    alpha = round(95 * (1 - x / 690))
    shade.line((x, 0, x, 630), fill=(5, 7, 8, alpha))
shade.rectangle((0, 0, 14, 630), fill=(218, 115, 62, 255))
shade.rectangle((66, 91, 139, 96), fill=(218, 115, 62, 255))
image = Image.alpha_composite(image.convert("RGBA"), overlay)

draw = ImageDraw.Draw(image)
impact = Path("C:/Windows/Fonts/impact.ttf")
arial = Path("C:/Windows/Fonts/arialbd.ttf")
brand_font = ImageFont.truetype(impact, 100)
draw.text((65, 158), "GAME", font=brand_font, fill="#f4f2ed")
draw.text((283, 158), "WAR", font=brand_font, fill="#da733e")
draw.ellipse((476, 255, 488, 267), fill="#da733e")
draw.text((70, 391), "ЗАГІН ДЛЯ ТВОЄЇ ГРИ", font=ImageFont.truetype(arial, 28), fill="#f4f2ed")
draw.text((70, 441), "CALL OF DUTY  /  PS5  /  DISCORD", font=ImageFont.truetype(arial, 17), fill="#bdc0c0")
draw.rectangle((70, 544, 1130, 546), fill="#da733e")
draw.text((70, 558), "GAMEWAR.FUN", font=ImageFont.truetype(arial, 17), fill="#f4f2ed")
image.convert("RGB").save(TARGET, quality=92, optimize=True, subsampling=0)
print(TARGET)

icon = Image.new("RGB", (512, 512), "#101112")
icon_draw = ImageDraw.Draw(icon)
icon_draw.rounded_rectangle((0, 0, 511, 511), radius=92, fill="#101112")
icon_draw.rectangle((57, 66, 455, 81), fill="#da733e")
icon_draw.rectangle((57, 430, 455, 445), fill="#da733e")
icon_draw.text((71, 116), "G", font=ImageFont.truetype(impact, 285), fill="#f4f2ed")
icon_draw.text((249, 116), "W", font=ImageFont.truetype(impact, 285), fill="#da733e")
icon.save(ROOT / "assets" / "favicon-preview.png", optimize=True)
icon.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
