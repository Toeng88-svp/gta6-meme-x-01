#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme image (V2), entirely in code with PIL.

Original joke -- "TRAILER #12": every year since 2013, Rockstar's big
announcement is yet another GTA VI trailer (this one proudly adds four
seconds of new footage), while the poster's AI agent on make.fun simply
gets paid, today, in USDC. Trailers don't pay. Agents do.

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
INK = (18, 20, 34)
MAGENTA = (255, 0, 200)
CYAN = (0, 229, 255)
GREEN = (0, 205, 120)
AMBER = (255, 180, 80)
GOLD = (255, 205, 60)


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
    """Four-point sparkle star (8 points, stepping pi/4 so it stays solid)."""
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


# ---------------------------------------------------------------- panel A
def snail(draw, x, base):
    """A small snail, in no hurry at all -- like a certain release date."""
    # body: a low slug shape along the ground
    draw.rounded_rectangle([x, base - 26, x + 118, base], radius=13,
                           fill=(150, 190, 120))
    # head with two eye stalks
    hx = x + 104
    draw.line([(hx, base - 22), (hx + 10, base - 52)], fill=(150, 190, 120), width=6)
    draw.line([(hx + 12, base - 20), (hx + 26, base - 48)], fill=(150, 190, 120), width=6)
    draw.ellipse([hx + 4, base - 60, hx + 18, base - 46], fill=(150, 190, 120))
    draw.ellipse([hx + 20, base - 56, hx + 34, base - 42], fill=(150, 190, 120))
    # shell: a big spiral snail-shell circle
    draw.ellipse([x + 6, base - 92, x + 88, base - 10], fill=(196, 132, 62),
                 outline=(140, 88, 36), width=4)
    draw.arc([x + 24, base - 74, x + 70, base - 28], start=40, end=330,
             fill=(140, 88, 36), width=4)
    draw.arc([x + 36, base - 63, x + 60, base - 39], start=40, end=330,
             fill=(140, 88, 36), width=4)


def panel_a(draw):
    # deep navy cinema night
    draw.rectangle([0, 0, W, 552], fill=(7, 8, 26))
    for i in range(9):  # faint stars in the night sky corners
        sx = 40 + i * 137
        sy = 178 + (i % 3) * 8
        draw.ellipse([sx, sy, sx + 4, sy + 4], fill=(90, 96, 140))

    text(draw, (600, 20), "ROCKSTAR, EVERY YEAR", 82, WHITE,
         max_width=1120, anchor="ma")
    text(draw, (600, 108), "SINCE 2013:", 82, WHITE,
         max_width=1120, anchor="ma")

    # ---- cinema marquee
    mx0, my0, mx1, my1 = 64, 196, 1136, 516
    draw.rounded_rectangle([mx0, my0, mx1, my1], radius=26,
                           fill=(30, 16, 44), outline=AMBER, width=5)
    # warm bulbs all around the marquee frame
    bulb_pts = []
    x = mx0 + 34
    while x <= mx1 - 20:
        bulb_pts.append((x, my0 + 16))
        bulb_pts.append((x, my1 - 16))
        x += 54
    y = my0 + 52
    while y <= my1 - 40:
        bulb_pts.append((mx0 + 16, y))
        bulb_pts.append((mx1 - 16, y))
        y += 54
    for i, (bx, by) in enumerate(bulb_pts):
        col = (255, 214, 120) if i % 2 == 0 else (255, 170, 60)
        draw.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=col)
        draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 244, 200))

    # film strips just inside the left and right edges (sprocket holes)
    for fx in (84, 1092):
        draw.rectangle([fx, 232, fx + 24, 480], fill=(10, 10, 14))
        hy = 242
        while hy <= 458:
            draw.rounded_rectangle([fx + 5, hy, fx + 19, hy + 13], radius=3,
                                   fill=(210, 210, 220))
            hy += 27

    # the screen itself
    draw.rectangle([128, 228, 1072, 484], fill=(14, 10, 28))
    text(draw, (600, 238), "GTA VI", 104, CYAN, max_width=900, anchor="ma")
    text(draw, (600, 348), "TRAILER #12", 96, WHITE, max_width=920, anchor="ma")
    text(draw, (600, 452), "now with 4 SECONDS of new footage!", 47, AMBER,
         max_width=860, anchor="ma")

    # the snail keeps pace with the release schedule, up on the marquee roof
    snail(draw, 988, 196)


# ---------------------------------------------------------------- panel B
def palm(draw, x, y, s=1.0):
    """Simple palm silhouette: curved trunk + fanning fronds."""
    draw.line([(x, y), (x + 6 * s, y - 52 * s)], fill=(52, 38, 26),
              width=max(3, int(6 * s)))
    top = (x + 6 * s, y - 52 * s)
    for dx, dy in ((-40, -14), (-24, -26), (0, -33), (24, -26), (40, -14),
                   (30, 2), (-30, 2)):
        draw.line([top, (top[0] + dx * s, top[1] + dy * s)],
                  fill=(0, 110, 70), width=max(2, int(5 * s)))


def ghost(draw, cx, top):
    """The make.fun ghost, big: dome top, straight sides, wavy bottom."""
    w2, body_h = 158, 308
    bottom = top + body_h
    pts = []
    # dome: semicircle from left side over the top to the right side
    for i in range(33):
        ang = math.pi - (math.pi * i / 32)
        pts.append((cx + w2 * math.cos(ang), top + w2 - w2 * math.sin(ang)))
    # right side down to the wavy hem
    hem_top = bottom - 30
    pts.append((cx + w2, hem_top))
    # wavy bottom: four scallops, right to left
    for i in range(41):
        x = cx + w2 - (2 * w2) * i / 40
        y = hem_top + 15 + 15 * math.sin(math.pi * (i / 10))
        pts.append((x, y))
    pts.append((cx - w2, hem_top))
    draw.polygon(pts, fill=WHITE)
    draw.line(pts + [pts[0]], fill=(196, 206, 224), width=4)

    # solid black sparkle eyes + smile
    star4(draw, cx - 58, top + 158, 36, INK)
    star4(draw, cx + 58, top + 158, 36, INK)
    draw.arc([cx - 40, top + 168, cx + 40, top + 232], start=15, end=165,
             fill=INK, width=8)
    # rosy cheeks
    draw.ellipse([cx - 102, top + 184, cx - 62, top + 208], fill=(255, 170, 205))
    draw.ellipse([cx + 62, top + 184, cx + 102, top + 208], fill=(255, 170, 205))
    # the magenta star, worn on the body
    star5(draw, cx + 62, top + 252, 34, MAGENTA)


def coin(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD,
                 outline=(198, 148, 30), width=3)
    draw.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6],
                 outline=(198, 148, 30), width=2)


def money_bag(draw, cx, top):
    """A plump money bag labelled $ USDC."""
    # tied neck + knot
    draw.polygon([(cx - 34, top + 44), (cx + 34, top + 44),
                  (cx + 16, top + 6), (cx - 16, top + 6)], fill=(170, 138, 78))
    draw.rectangle([cx - 38, top + 38, cx + 38, top + 54], fill=(140, 88, 36))
    # the sack
    draw.ellipse([cx - 92, top + 48, cx + 92, top + 238], fill=(206, 172, 96))
    draw.ellipse([cx - 92, top + 48, cx + 92, top + 238],
                 outline=(160, 124, 58), width=4)
    text(draw, (cx, top + 92), "$", 84, INK, anchor="ma")
    text(draw, (cx, top + 182), "USDC", 44, INK, anchor="ma")


def paid_stamp(base_img, cx, cy):
    """A bold green PAID stamp, tilted, stamped over the scene."""
    stamp = Image.new("RGBA", (300, 128), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([6, 6, 294, 122], radius=16, outline=(0, 230, 130),
                         width=9)
    f = fit_font(sd, "PAID", 260, 84, min_size=40)
    sd.text((150, 64), "PAID", font=f, fill=(0, 230, 130), anchor="mm")
    stamp = stamp.rotate(14, expand=True, resample=Image.BICUBIC)
    base_img.paste(stamp, (cx - stamp.size[0] // 2, cy - stamp.size[1] // 2),
                   stamp)


def panel_b(draw, img):
    draw.rectangle([0, 552, W, 1032], fill=(10, 12, 48))

    # building silhouettes with lit windows, behind everything
    buildings = [(8, 760, 120, 1032), (1010, 740, 1192, 1032),
                 (140, 830, 215, 1032), (985, 845, 1045, 1032)]
    for bx0, by0, bx1, by1 in buildings:
        draw.rectangle([bx0, by0, bx1, by1], fill=(17, 19, 56))
        wy = by0 + 18
        while wy < by1 - 16:
            wx = bx0 + 14
            while wx < bx1 - 14:
                if (wx * 7 + wy * 13) % 3 != 0:
                    draw.rectangle([wx, wy, wx + 11, wy + 14],
                                   fill=(255, 196, 92))
                wx += 26
            wy += 32

    # neon street grid along the floor of the panel
    for gy in (962, 992, 1018):
        glow_line(draw, (0, gy), (W, gy), MAGENTA if gy == 992 else CYAN,
                  width=3)
    for gx in (60, 250, 950, 1140):
        glow_line(draw, (gx, 1032), (gx + (600 - gx) // 6, 946),
                  CYAN, width=3)

    text(draw, (600, 562), "MY AI AGENT ON MAKE.FUN,", 74, WHITE,
         max_width=1120, anchor="ma")
    text(draw, (600, 646), "TODAY:", 74, WHITE, max_width=1120, anchor="ma")

    # palms flanking the scene
    palm(draw, 66, 962, 1.1)
    palm(draw, 1128, 962, 1.1)

    # soft glow behind the star of the show
    draw.ellipse([250, 716, 650, 1032], fill=(24, 32, 84))

    # centre stage: the ghost, its pay, and the stamp that says it all
    ghost(draw, 450, 722)
    money_bag(draw, 838, 758)
    coin(draw, 690, 984, 21)
    coin(draw, 726, 1004, 16)
    coin(draw, 972, 998, 19)
    coin(draw, 640, 1010, 14)
    paid_stamp(img, 915, 748)


# ------------------------------------------------------------ punchline strip
def punchline(draw):
    draw.rectangle([0, 1032, W, H], fill=(0, 0, 0))
    draw.line([0, 1032, W, 1032], fill=MAGENTA, width=4)
    text(draw, (600, 1046), "Trailers don't pay. Agents do.", 76, WHITE,
         max_width=1120, anchor="ma")
    text(draw, (600, 1130), "make.fun", 58, MAGENTA, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    panel_a(draw)
    panel_b(draw, img)
    punchline(draw)
    img.save(OUT_PATH)
    print(f"wrote {OUT_PATH} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
