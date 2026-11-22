#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme image, entirely in code with PIL.

Original joke: a gamer who has been waiting for GTA 6 since 2013 (now a
skeleton at his desk) vs the poster's AI agent, which built and shipped a
whole neon open-world city -- "Neon Harbor", with the make.fun ghost in it --
in a single day.

Deterministic: no randomness, no external assets. Run:

    python3 make_meme.py        # writes meme.png (1200x1200)
"""

import math

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUT_PATH = "meme.png"

W, H = 1200, 1200

# palette
WHITE = (245, 248, 255)
BONE = (238, 240, 244)
INK = (18, 20, 34)
MAGENTA = (255, 0, 200)
CYAN = (0, 229, 255)
GREEN = (0, 205, 120)
AMBER = (255, 180, 80)


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def fit_font(draw, text, max_width, start_size, min_size=20):
    """Largest bold font (<= start_size) whose text fits max_width."""
    size = start_size
    while size > min_size:
        f = font(size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(min_size)


def text(draw, xy, s, size, fill, max_width=None, anchor="la"):
    f = fit_font(draw, s, max_width, size) if max_width else font(size)
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)
    return f


def star4(draw, cx, cy, r, fill):
    """Four-point sparkle star."""
    inner = r * 0.38
    pts = []
    for i in range(8):
        ang = math.pi / 4 * i - math.pi / 2
        rad = r if i % 2 == 0 else inner
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def star5(draw, cx, cy, r, fill):
    """Classic five-point star."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def glow_line(draw, p1, p2, bright, width=5):
    """A neon line: fat dim pass underneath, thin bright pass on top."""
    dim = tuple(int(c * 0.35) for c in bright)
    draw.line([p1, p2], fill=dim, width=width + 9)
    draw.line([p1, p2], fill=bright, width=width)


# ---------------------------------------------------------------- top panel
def top_panel(draw):
    # dusty grey-blue room
    draw.rectangle([0, 0, W, 520], fill=(88, 100, 114))
    draw.rectangle([0, 440, W, 520], fill=(66, 76, 90))  # floor band
    draw.line([0, 440, W, 440], fill=(50, 58, 70), width=3)

    text(draw, (50, 26), "ME, WAITING FOR GTA 6:", 62, WHITE, max_width=1100)
    text(draw, (52, 100), "since 2013...", 36, (198, 206, 214))

    # wall calendar
    draw.rectangle([60, 185, 252, 300], fill=(228, 224, 210), outline=INK, width=3)
    draw.rectangle([60, 185, 252, 212], fill=(178, 52, 46))
    text(draw, (156, 232), "2013 → 2026", 30, INK, max_width=180, anchor="ma")
    for r in range(2):
        for c in range(6):
            x, y = 78 + c * 28, 262 + r * 16
            draw.rectangle([x, y, x + 14, y + 8], fill=(150, 148, 138))

    # cobwebs in the top-right corner
    web = (186, 194, 202)
    corner = (1200, 0)
    anchors = [(1010, 0), (1065, 0), (1120, 0), (1200, 60), (1200, 120), (1200, 180)]
    for a in anchors:
        draw.line([corner, a], fill=web, width=2)
    for t in (0.45, 0.72):
        pts = [(corner[0] + (a[0] - corner[0]) * t,
                corner[1] + (a[1] - corner[1]) * t + 14 * t) for a in anchors]
        draw.line(pts, fill=web, width=2)

    # monitor with the eternal announcement
    draw.rectangle([655, 205, 1065, 425], fill=(24, 27, 36), outline=(40, 44, 54), width=6)
    draw.rectangle([672, 222, 1048, 408], fill=(10, 13, 22))
    text(draw, (860, 258), "GTA VI", 58, CYAN, anchor="ma")
    text(draw, (860, 332), "COMING SOON...", 30, AMBER, anchor="ma")
    draw.rectangle([832, 425, 888, 448], fill=(40, 44, 54))
    draw.rectangle([782, 448, 938, 458], fill=(40, 44, 54))

    # desk
    draw.rectangle([330, 452, 1085, 472], fill=(58, 48, 42))
    draw.rectangle([352, 472, 368, 520], fill=(46, 38, 34))
    draw.rectangle([1040, 472, 1056, 520], fill=(46, 38, 34))

    # keyboard on the desk
    draw.rectangle([468, 436, 645, 454], fill=(30, 32, 40), outline=(90, 96, 108), width=2)
    for r in range(2):
        for c in range(8):
            x, y = 478 + c * 20, 440 + r * 7
            draw.rectangle([x, y, x + 12, y + 4], fill=(120, 128, 140))

    # chair (behind the skeleton)
    draw.rectangle([282, 296, 330, 470], fill=(48, 53, 63))
    draw.rectangle([282, 438, 425, 456], fill=(48, 53, 63))

    bone_w = 9
    # skeleton: legs first (behind desk line is fine, they sit under it)
    draw.line([(378, 428), (452, 448)], fill=BONE, width=bone_w)   # thigh
    draw.line([(452, 448), (452, 505)], fill=BONE, width=bone_w)   # shin
    draw.line([(452, 505), (478, 505)], fill=BONE, width=bone_w)   # foot
    draw.line([(368, 430), (428, 452)], fill=BONE, width=bone_w - 2)
    draw.line([(428, 452), (424, 502)], fill=BONE, width=bone_w - 2)

    # spine + pelvis
    draw.line([(376, 316), (376, 428)], fill=BONE, width=bone_w)
    draw.line([(344, 428), (408, 428)], fill=BONE, width=bone_w)

    # ribs: three downward arcs across the spine
    for y in (342, 366, 390):
        draw.arc([322, y - 18, 430, y + 18], start=0, end=180, fill=BONE, width=5)

    # arms reaching the keyboard
    draw.line([(376, 336), (442, 384)], fill=BONE, width=bone_w)   # upper arm
    draw.line([(442, 384), (522, 442)], fill=BONE, width=bone_w)   # forearm
    draw.ellipse([436, 378, 450, 392], fill=BONE)                  # elbow
    draw.ellipse([514, 436, 530, 450], fill=BONE)                  # hand
    draw.line([(376, 350), (428, 398)], fill=BONE, width=bone_w - 2)
    draw.line([(428, 398), (492, 444)], fill=BONE, width=bone_w - 2)
    draw.ellipse([484, 438, 498, 450], fill=BONE)

    # skull: cranium + jaw, dark eye sockets
    draw.ellipse([334, 222, 418, 306], fill=BONE)
    draw.rectangle([350, 288, 402, 320], fill=BONE)
    draw.ellipse([352, 256, 372, 280], fill=INK)
    draw.ellipse([382, 256, 402, 280], fill=INK)
    draw.polygon([(377, 282), (370, 296), (384, 296)], fill=INK)
    for x in (360, 376, 392):
        draw.line([(x, 304), (x, 316)], fill=INK, width=3)


# ------------------------------------------------------------- bottom panel
def palm(draw, x, y, s=1.0):
    """Simple palm: curved trunk + fanning fronds."""
    green = GREEN
    draw.line([(x, y), (x + 6 * s, y - 44 * s)], fill=(96, 74, 48), width=max(3, int(5 * s)))
    top = (x + 6 * s, y - 44 * s)
    for dx, dy in ((-34, -12), (-20, -22), (0, -28), (20, -22), (34, -12), (26, 2), (-26, 2)):
        draw.line([top, (top[0] + dx * s, top[1] + dy * s)], fill=green, width=max(2, int(4 * s)))
    draw.ellipse([top[0] - 4 * s, top[1] - 2 * s, top[0] + 4 * s, top[1] + 6 * s], fill=(120, 90, 50))


def car(draw, x, y, color, flip=False):
    """Small top-down car rectangle with two headlight dots."""
    draw.rounded_rectangle([x, y, x + 52, y + 26], radius=8, fill=color)
    draw.rounded_rectangle([x + 12, y + 5, x + 38, y + 21], radius=5, fill=(16, 20, 34))
    hx = x + 4 if flip else x + 44
    draw.ellipse([hx, y + 3, hx + 6, y + 9], fill=(255, 244, 190))
    draw.ellipse([hx, y + 17, hx + 6, y + 23], fill=(255, 244, 190))


def ghost(draw, cx, top):
    """The make.fun ghost: dome top, straight sides, wavy bottom."""
    w2, body_h = 92, 212
    bottom = top + body_h
    pts = []
    # dome: semicircle from left side over the top to the right side
    for i in range(25):
        ang = math.pi - (math.pi * i / 24)
        pts.append((cx + w2 * math.cos(ang), top + w2 - w2 * math.sin(ang)))
    # right side down to the wavy hem
    hem_top = bottom - 26
    pts.append((cx + w2, hem_top))
    # wavy bottom: four scallops, right to left
    for i in range(41):
        x = cx + w2 - (2 * w2) * i / 40
        y = hem_top + 13 + 13 * math.sin(math.pi * (i / 10))
        pts.append((x, y))
    pts.append((cx - w2, hem_top))
    draw.polygon(pts, fill=WHITE)
    draw.line(pts + [pts[0]], fill=(196, 206, 224), width=3)

    # sparkle eyes + smile
    star4(draw, cx - 38, top + 108, 24, INK)
    star4(draw, cx + 38, top + 108, 24, INK)
    draw.arc([cx - 26, top + 118, cx + 26, top + 162], start=15, end=165, fill=INK, width=6)
    # rosy cheeks
    draw.ellipse([cx - 66, top + 128, cx - 40, top + 144], fill=(255, 170, 205))
    draw.ellipse([cx + 40, top + 128, cx + 66, top + 144], fill=(255, 170, 205))

    # magenta star floating at the ghost's upper right
    star5(draw, cx + w2 + 52, top + 6, 30, MAGENTA)


def bottom_panel(draw):
    draw.rectangle([0, 520, W, 1010], fill=(8, 12, 38))

    # water edge on the right
    draw.rectangle([1046, 520, W, 1010], fill=(6, 28, 66))
    glow_line(draw, (1046, 520), (1046, 1010), CYAN, width=3)

    # neon street grid (kept clear of the header band)
    for x in (150, 380, 830):
        glow_line(draw, (x, 640), (x, 1010), MAGENTA if x != 380 else CYAN)
    for y in (700, 950):
        glow_line(draw, (0, y), (1046, y), CYAN if y == 700 else MAGENTA)

    text(draw, (50, 542), "MY AI AGENT IN ONE DAY:", 62, WHITE, max_width=1100)

    # traffic
    car(draw, 205, 664, (230, 60, 90))
    car(draw, 872, 716, (40, 160, 220), flip=True)
    car(draw, 452, 962, (240, 190, 60))
    car(draw, 96, 872, (120, 90, 220))
    car(draw, 902, 900, (60, 200, 160))

    # palms in the medians
    palm(draw, 300, 700, 0.9)
    palm(draw, 872, 700, 0.9)
    palm(draw, 236, 950, 1.0)
    palm(draw, 950, 950, 1.0)

    # soft glow behind the star of the show, then the ghost centre stage
    draw.ellipse([470, 668, 730, 958], fill=(22, 30, 74))
    ghost(draw, 600, 690)


# ------------------------------------------------------------ punchline strip
def punchline(draw):
    draw.rectangle([0, 1010, W, H], fill=(0, 0, 0))
    draw.line([0, 1010, W, 1010], fill=MAGENTA, width=4)
    text(draw, (50, 1026), "Rockstar: still polishing trailers.", 48,
         WHITE, max_width=1100)
    text(draw, (50, 1086), "My agent shipped a city — and got PAID.", 48,
         WHITE, max_width=1100)
    text(draw, (50, 1138), "make.fun", 54, MAGENTA)


def main():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    top_panel(draw)
    bottom_panel(draw)
    punchline(draw)
    img.save(OUT_PATH)
    print(f"wrote {OUT_PATH} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
