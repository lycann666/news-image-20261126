#!/usr/bin/env python3
"""Render the news-image-20261126 front page (1024x1024 PNG).

Draws a newspaper front page summarising Thursday 26 November 2026:
lead = Houthi strike on Saudi Ras Tanura refinery (Brent > $94); grid =
Trump tariffs / Pakistan's first astronaut / Russia's Ukraine toll /
India 26/11 anniversary; strip = Bangladesh wage rise; ticker = four more
stories. Pure PIL, no network, deterministic output.
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 24, 39)
NAVY = (15, 27, 45)
NAVY2 = (27, 47, 74)
RED = (180, 35, 24)
GOLD = (212, 160, 23)
GREY = (68, 64, 58)
LIGHT = (216, 210, 196)
WHITE = (255, 255, 255)
BLUE = (30, 90, 160)
SLATE = (71, 85, 105)
SAFFRON = (217, 119, 6)
GREEN = (22, 101, 52)

F = "/usr/share/fonts/truetype"
SERIF_B = f"{F}/dejavu/DejaVuSerif-Bold.ttf"
BLACK = f"{F}/noto/NotoSans-Black.ttf"
BOLD = f"{F}/noto/NotoSans-Bold.ttf"
REG = f"{F}/noto/NotoSans-Regular.ttf"
ITALIC = f"{F}/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- top bar + masthead -------------------------------------------------
d.rectangle([0, 0, W, 10], fill=NAVY)
draw_center(d, 26, "THE WORLD IN ONE DAY", font(SERIF_B, 40), NAVY)
d.rectangle([312, 84, 712, 88], fill=RED)
draw_center(d, 100, "THURSDAY 26 NOVEMBER 2026", font(BLACK, 54), RED)
draw_center(d, 162, "Six stories that defined the day \u2014 from Riyadh to orbit",
            font(ITALIC, 22), GREY)

# ---- lead story: Houthi strike, oil > $94 -------------------------------
LX, LY, LW, LH = 24, 186, 976, 292
d.rounded_rectangle([LX, LY, LX + LW, LY + LH], radius=12, fill=NAVY)
# refinery silhouette, left zone
ix0, iy0 = LX + 18, LY + 14
d.rectangle([ix0, iy0 + 150, ix0 + 330, iy0 + 205], fill=NAVY2)  # ground
for x, wdt, hgt in [(ix0 + 10, 34, 130), (ix0 + 60, 26, 180), (ix0 + 100, 40, 105),
                    (ix0 + 160, 30, 150), (ix0 + 210, 36, 120), (ix0 + 260, 28, 160)]:
    d.rectangle([x, iy0 + 205 - hgt, x + wdt, iy0 + 205], fill=(58, 84, 120))
    d.polygon([(x, iy0 + 205 - hgt), (x + wdt / 2, iy0 + 205 - hgt - 20),
               (x + wdt, iy0 + 205 - hgt)], fill=(58, 84, 120))
for cx in (ix0 + 120, ix0 + 240):
    d.ellipse([cx - 26, iy0 + 153, cx + 26, iy0 + 205], fill=(58, 84, 120))
# flame above the tallest tower (top at iy0+25)
fx, fbase = ix0 + 73, iy0 + 25
d.polygon([(fx - 16, fbase), (fx, fbase - 24), (fx + 16, fbase),
           (fx + 7, fbase - 6), (fx, fbase + 4), (fx - 7, fbase - 6)], fill=(245, 158, 11))
d.polygon([(fx - 8, fbase), (fx, fbase - 14), (fx + 8, fbase)], fill=(250, 204, 21))
# smoke dots
for sx, sy, r in [(ix0 + 150, iy0 + 2, 9), (ix0 + 175, iy0 - 8, 12), (ix0 + 205, iy0 - 2, 9)]:
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(148, 163, 184))
# big $94, inside the panel
d.text((ix0 + 6, iy0 + 212), "$94", font=font(BLACK, 46), fill=GOLD)
d.text((ix0 + 150, iy0 + 226), "BRENT CRUDE / BARREL", font=font(BOLD, 18), fill=(203, 213, 225))
# lead text, right zone
tx = LX + 400
d.text((tx, LY + 26), "MIDDLE EAST  \u2022  ENERGY", font=font(BOLD, 19), fill=GOLD)
head = ["HOUTHIS HIT SAUDI'S", "BIGGEST REFINERY"]
y = LY + 56
for line in head:
    d.text((tx, y), line, font=font(BLACK, 44), fill=WHITE)
    y += 52
body = ("Yemen's Houthis claim strikes on Ras Tanura "
        "and Riyadh \u2014 oil jumps past $94 a barrel "
        "as markets fear supply disruption.")
y += 8
for line in wrap(d, body, font(REG, 23), LW - 400 - 36):
    d.text((tx, y), line, font=font(REG, 23), fill=(226, 232, 240))
    y += 30

# ---- 2x2 grid ------------------------------------------------------------
panels = [
    # (accent, kicker, headline, summary, icon)
    (RED, "TRADE  \u2022  UNITED STATES",
     "TRUMP UNVEILS NEW TARIFFS ON 14 ECONOMIES",
     "China, Japan and the EU among targets in the Section 301 plan.", "tariff"),
    (BLUE, "SPACE  \u2022  ASIA",
     "PAKISTAN'S FIRST ASTRONAUT TO TIANGONG",
     "Muhammad Zeeshan Ali joins China's Shenzhou-24 crew.", "rocket"),
    (SLATE, "WAR  \u2022  EUROPE",
     "RUSSIA: NEARLY 500,000 LOST IN UKRAINE",
     "Moscow's figures lay bare the war's human cost.", "tally"),
    (SAFFRON, "REMEMBRANCE  \u2022  INDIA",
     "INDIA MARKS 18 YEARS SINCE 26/11",
     "Mumbai honours the victims of the 2008 attacks.", "candle"),
]
GX, GY, PW, PH, GAP = 24, 494, 480, 164, 16
for i, (accent, kicker, head, summ, icon) in enumerate(panels):
    px = GX + (i % 2) * (PW + GAP)
    py = GY + (i // 2) * (PH + GAP)
    d.rounded_rectangle([px, py, px + PW, py + PH], radius=10, fill=WHITE,
                        outline=LIGHT, width=2)
    d.rounded_rectangle([px, py, px + PW, py + 7], radius=3, fill=accent)
    # icon zone
    cx, cy = px + 62, py + 92
    if icon == "tariff":
        for bx, bh, col in [(cx - 38, 34, (248, 113, 113)), (cx - 12, 52, RED),
                            (cx + 14, 70, (127, 29, 29))]:
            d.rectangle([bx, cy + 40 - bh, bx + 20, cy + 40], fill=col)
        d.text((cx + 30, cy - 52), "%", font=font(BLACK, 28), fill=INK)
    elif icon == "rocket":
        d.ellipse([cx - 46, cy - 48, cx + 46, cy + 48], outline=BLUE, width=3)
        d.polygon([(cx, cy - 46), (cx + 13, cy - 6), (cx + 9, cy + 22),
                   (cx - 9, cy + 22), (cx - 13, cy - 6)], fill=WHITE,
                  outline=INK, width=2)
        d.polygon([(cx - 13, cy - 6), (cx - 26, cy + 16), (cx - 9, cy + 10)], fill=RED)
        d.polygon([(cx + 13, cy - 6), (cx + 26, cy + 16), (cx + 9, cy + 10)], fill=RED)
        d.ellipse([cx - 6, cy - 34, cx + 6, cy - 22], fill=BLUE)
        d.polygon([(cx - 7, cy + 22), (cx, cy + 44), (cx + 7, cy + 22)], fill=(245, 158, 11))
        d.ellipse([cx + 34, cy - 44, cx + 40, cy - 38], fill=GOLD)
    elif icon == "tally":
        for bx, bh in [(cx - 40, 26), (cx - 14, 44), (cx + 12, 62)]:
            d.rectangle([bx, cy + 40 - bh, bx + 20, cy + 40], fill=SLATE)
        d.line([cx - 44, cy + 44, cx + 40, cy - 30], fill=RED, width=4)
        d.text((cx - 46, cy - 62), "500K", font=font(BLACK, 26), fill=INK)
    elif icon == "candle":
        d.ellipse([cx - 30, cy - 52, cx + 30, cy + 8], fill=(254, 243, 199))
        d.polygon([(cx, cy - 50), (cx + 12, cy - 22), (cx, cy - 8),
                   (cx - 12, cy - 22)], fill=(245, 158, 11))
        d.polygon([(cx, cy - 38), (cx + 6, cy - 20), (cx, cy - 12),
                   (cx - 6, cy - 20)], fill=(250, 204, 21))
        d.rectangle([cx - 11, cy - 8, cx + 11, cy + 44], fill=SAFFRON)
        d.rectangle([cx - 20, cy + 44, cx + 20, cy + 50], fill=INK)
    # text zone
    txp = px + 128
    d.text((txp, py + 18), kicker, font=font(BOLD, 15), fill=accent)
    y = py + 40
    for line in wrap(d, head, font(BLACK, 24), PW - 128 - 16):
        d.text((txp, y), line, font=font(BLACK, 24), fill=INK)
        y += 29
    y += 2
    for line in wrap(d, summ, font(REG, 18), PW - 128 - 16):
        d.text((txp, y), line, font=font(REG, 18), fill=GREY)
        y += 23

# ---- Bangladesh strip ----------------------------------------------------
BX, BY, BW, BH = 24, 850, 976, 86
d.rounded_rectangle([BX, BY, BX + BW, BY + BH], radius=10, fill=WHITE,
                    outline=LIGHT, width=2)
d.rounded_rectangle([BX, BY, BX + BW, BY + 7], radius=3, fill=GREEN)
# t-shirt icon
sx, sy = BX + 58, BY + 48
d.polygon([(sx - 34, sy - 22), (sx - 16, sy - 28), (sx, sy - 20), (sx + 16, sy - 28),
           (sx + 34, sy - 22), (sx + 26, sy + 2), (sx + 18, sy - 4), (sx + 18, sy + 26),
           (sx - 18, sy + 26), (sx - 18, sy - 4), (sx - 26, sy + 2)], fill=GREEN)
d.text((BX + 112, BY + 14), "ECONOMY  \u2022  BANGLADESH", font=font(BOLD, 15), fill=GREEN)
d.text((BX + 112, BY + 34), "GARMENT WORKERS WIN 36% PAY RISE",
       font=font(BLACK, 26), fill=INK)
d.text((BX + 112, BY + 63), "Minimum wage lifted for entry-level workers.",
       font=font(REG, 17), fill=GREY)

# ---- ticker ---------------------------------------------------------------
TX, TY, TW, TH = 24, 938, 976, 58
d.rounded_rectangle([TX, TY, TX + TW, TY + TH], radius=8, fill=NAVY)
d.text((TX + 16, TY + 18), "ALSO TODAY:", font=font(BLACK, 19), fill=GOLD)
tick = ("Colombia marks 10 years of peace  \u2022  N. Korea orders Swiss office shut  "
        "\u2022  Solomon Islands\u2013Australia security pact  \u2022  Norway voids "
        "disputed oil licences")
lines = wrap(d, tick, font(REG, 17), TW - 150)
yy = TY + 9
for line in lines:
    d.text((TX + 150, yy), line, font=font(REG, 17), fill=WHITE)
    yy += 21

# ---- footer ----------------------------------------------------------------
draw_center(d, 1002, "Drawn for this front page  \u2022  Summarised from wire reports of 25\u201326 November 2026",
            font(REG, 15), GREY)

out = "/home/hatch/workspace/makefun/news-image-20261126-build/entry.png"
img.save(out, "PNG", optimize=True)
import os
n = os.path.getsize(out)
print("bytes:", n, "size:", img.size)
print("sha256:", hashlib.sha256(open(out, "rb").read()).hexdigest())
assert n <= 1048576 and img.size[0] <= 1024 and img.size[1] <= 1024
print("GATE OK")
