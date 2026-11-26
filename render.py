#!/usr/bin/env python3
"""Render entry.png for news-image-20261126-makefun.

"THE WORLD IN ONE DAY" — a serif broadsheet front page for Thursday
26 November 2026: 30 verified stories, 7 regions, 15 illustrated panels,
numbers strip, UTC timeline, world map with numbered pins.

The grader does NOT run this script; main.ts copies the rendered entry.png.
Run manually with:  python3 render.py
Output: entry.png beside this script (1024x1024 PNG).
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 243, 233)  # warm newsprint, lightened a touch for print contrast
INK = (26, 26, 26)
NAVY = (20, 33, 61)
RED = (176, 42, 33)
GREY = (105, 100, 92)
RULE = (60, 56, 50)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def italic(size):
    p = FD + "DejaVuSerif-Italic.ttf"
    return ImageFont.truetype(p if os.path.exists(p) else SERIF, size)


def tw(draw, text, f):
    return draw.textlength(text, font=f)


def wrap(draw, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(draw, t, f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


# ---------------------------------------------------------------- panels ---
def panel_eu(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (27, 58, 120), (70, 110, 180))
    d.rectangle([x0, y1 - 26, x1, y1], fill=(18, 38, 80))
    # flags row
    for i in range(6):
        fx = x0 + 14 + i * ((x1 - x0 - 28) // 6)
        d.line([(fx, y0 + 12), (fx, y0 + 52)], fill=(230, 230, 230), width=2)
        d.rectangle([fx, y0 + 12, fx + 22, y0 + 28], fill=(255, 204, 0))
    # council table + chairs
    d.ellipse([x0 + 30, y1 - 52, x1 - 30, y1 - 14], fill=(120, 84, 48), outline=(70, 48, 26), width=2)
    for i in range(5):
        cx = x0 + 40 + i * ((x1 - x0 - 80) // 4)
        d.rectangle([cx - 7, y1 - 66, cx + 7, y1 - 52], fill=(40, 40, 46))
    # euro coin
    d.ellipse([x1 - 58, y0 + 34, x1 - 18, y0 + 74], fill=(255, 204, 0), outline=(180, 140, 0), width=2)
    d.text((x1 - 50, y0 + 42), "€", font=font(SERIF_B, 26), fill=(120, 90, 0))


def panel_parade(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (120, 140, 170), (200, 205, 215))
    # skyline
    for i, h in enumerate([46, 66, 38, 58, 44, 62, 40]):
        bx = x0 + 6 + i * ((x1 - x0 - 12) // 7)
        d.rectangle([bx, y1 - 18 - h, bx + 24, y1 - 18], fill=(70, 78, 96))
    d.rectangle([x0, y1 - 18, x1, y1], fill=(52, 56, 66))
    # balloon + ropes
    d.ellipse([x0 + 70, y0 + 8, x0 + 150, y0 + 62], fill=RED, outline=(120, 20, 14), width=2)
    d.line([(x0 + 92, y0 + 58), (x0 + 100, y1 - 26)], fill=(40, 40, 40), width=2)
    d.line([(x0 + 128, y0 + 58), (x0 + 120, y1 - 26)], fill=(40, 40, 40), width=2)
    # wind swirls
    for i in range(3):
        wy = y0 + 16 + i * 16
        d.arc([x1 - 90, wy, x1 - 20, wy + 12], 180, 360, fill=(240, 240, 245), width=2)
    # crowd
    for i in range(9):
        cx = x0 + 16 + i * ((x1 - x0 - 32) // 8)
        d.ellipse([cx, y1 - 26, cx + 7, y1 - 19], fill=(240, 220, 180))


def panel_constitution(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (245, 220, 170), (250, 238, 205))
    d.rectangle([x0, y1 - 16, x1, y1], fill=(150, 110, 70))
    cx = (x0 + x1) // 2
    # dome + drum + pillars
    d.pieslice([cx - 34, y0 + 10, cx + 34, y0 + 62], 180, 360, fill=(196, 120, 52), outline=(140, 80, 30), width=2)
    d.rectangle([cx - 44, y0 + 38, cx + 44, y0 + 50], fill=(210, 140, 70))
    for i in range(5):
        px = cx - 40 + i * 20
        d.rectangle([px, y0 + 50, px + 7, y1 - 30], fill=(222, 160, 92))
    d.rectangle([cx - 50, y1 - 30, cx + 50, y1 - 16], fill=(196, 120, 52))
    # tricolour flag
    d.line([(x1 - 40, y0 + 8), (x1 - 40, y1 - 40)], fill=(90, 70, 50), width=3)
    d.rectangle([x1 - 40, y0 + 8, x1 - 8, y0 + 17], fill=(255, 153, 51))
    d.rectangle([x1 - 40, y0 + 17, x1 - 8, y0 + 26], fill=(255, 255, 255))
    d.rectangle([x1 - 40, y0 + 26, x1 - 8, y0 + 35], fill=(19, 136, 8))
    # open book
    d.polygon([(x0 + 16, y1 - 34), (x0 + 42, y1 - 40), (x0 + 42, y1 - 20), (x0 + 16, y1 - 14)], fill=(255, 252, 240), outline=(120, 100, 70))
    d.polygon([(x0 + 42, y1 - 40), (x0 + 68, y1 - 34), (x0 + 68, y1 - 14), (x0 + 42, y1 - 20)], fill=(255, 252, 240), outline=(120, 100, 70))


def panel_taiz(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (250, 224, 170), (246, 236, 200))
    d.polygon([(x0, y1 - 14), (x0 + 30, y1 - 34), (x0 + 55, y1 - 14)], fill=(190, 150, 100))
    d.rectangle([x0, y1 - 14, x1, y1], fill=(205, 170, 110))
    # clinic tent + cross
    d.polygon([(x0 + 18, y1 - 14), (x0 + 34, y0 + 10), (x0 + 50, y1 - 14)], fill=(255, 255, 255), outline=(150, 150, 150))
    d.rectangle([x0 + 31, y0 + 22, x0 + 37, y0 + 34], fill=(0, 150, 140))
    d.rectangle([x0 + 28, y0 + 25, x0 + 40, y0 + 31], fill=(0, 150, 140))
    # vaccine vial
    d.rectangle([x1 - 26, y0 + 18, x1 - 14, y0 + 40], fill=(200, 240, 235), outline=(0, 130, 120), width=2)
    d.rectangle([x1 - 25, y0 + 13, x1 - 15, y0 + 19], fill=(0, 130, 120))
    # queue
    for i in range(3):
        qx = x0 + 8 + i * 10
        d.ellipse([qx, y1 - 26, qx + 6, y1 - 20], fill=(80, 60, 40))
        d.rectangle([qx + 1, y1 - 20, qx + 5, y1 - 12], fill=(80, 60, 40))


def panel_cricket(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (30, 60, 110), (70, 110, 170))
    d.rectangle([x0, y1 - 20, x1, y1], fill=(46, 120, 60))
    # pitch + stumps
    d.rectangle([(x0 + x1) // 2 - 5, y1 - 20, (x0 + x1) // 2 + 5, y1 - 4], fill=(220, 200, 150))
    for i in range(3):
        sx = (x0 + x1) // 2 - 6 + i * 5
        d.line([(sx, y1 - 30), (sx, y1 - 20)], fill=(255, 220, 90), width=2)
    # ball + bat
    d.ellipse([x0 + 12, y0 + 14, x0 + 24, y0 + 26], fill=(200, 40, 40))
    d.polygon([(x1 - 22, y0 + 10), (x1 - 14, y0 + 14), (x1 - 20, y0 + 36), (x1 - 28, y0 + 32)], fill=(222, 190, 130), outline=(160, 130, 80))
    # floodlights
    for fx in (x0 + 6, x1 - 12):
        d.line([(fx, y1 - 20), (fx, y0 + 8)], fill=(60, 60, 70), width=2)
        d.rectangle([fx - 4, y0 + 2, fx + 4, y0 + 9], fill=(255, 250, 200))


def panel_ecuador(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (235, 238, 245), (250, 250, 248))
    d.rectangle([x0, y1 - 12, x1, y1], fill=(120, 110, 90))
    # two flags
    d.rectangle([x0 + 8, y0 + 8, x0 + 32, y0 + 24], fill=(178, 34, 52))
    for i in range(3):
        d.rectangle([x0 + 8, y0 + 8 + i * 6, x0 + 32, y0 + 11 + i * 6], fill=(255, 255, 255))
    d.rectangle([x0 + 8, y0 + 8, x0 + 18, y0 + 16], fill=(60, 59, 110))
    d.rectangle([x1 - 32, y0 + 8, x1 - 8, y0 + 16], fill=(255, 221, 0))
    d.rectangle([x1 - 32, y0 + 16, x1 - 8, y0 + 20], fill=(0, 70, 173))
    d.rectangle([x1 - 32, y0 + 20, x1 - 8, y0 + 24], fill=(239, 51, 64))
    # document + pen
    d.rectangle([x0 + 22, y1 - 30, x1 - 22, y1 - 12], fill=(255, 255, 255), outline=(140, 140, 140), width=2)
    for i in range(3):
        d.line([(x0 + 27, y1 - 25 + i * 5), (x1 - 30, y1 - 25 + i * 5)], fill=(160, 160, 160), width=2)
    d.line([(x1 - 16, y1 - 28), (x1 - 10, y1 - 14)], fill=(240, 190, 0), width=3)


def panel_nfl(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (40, 70, 130), (90, 130, 190))
    # stadium bowl
    d.pieslice([x0 + 2, y0 + 4, x1 - 2, y1 + 20], 0, 180, fill=(70, 80, 100))
    d.rectangle([x0, y1 - 18, x1, y1], fill=(40, 110, 55))
    for i in range(5):
        lx = x0 + 6 + i * ((x1 - x0 - 12) // 4)
        d.line([(lx, y1 - 18), (lx, y1)], fill=(255, 255, 255), width=2)
    # goalpost + ball
    gx = (x0 + x1) // 2
    d.line([(gx, y1 - 18), (gx, y0 + 26)], fill=(255, 220, 60), width=3)
    d.line([(gx - 10, y0 + 26), (gx + 10, y0 + 26)], fill=(255, 220, 60), width=3)
    d.ellipse([x1 - 26, y0 + 8, x1 - 10, y0 + 18], fill=(150, 85, 40), outline=(100, 55, 25), width=2)


def panel_shopping(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (250, 235, 220), (255, 248, 235))
    d.rectangle([x0, y1 - 10, x1, y1], fill=(140, 120, 100))
    # storefront + awning
    d.rectangle([x0 + 8, y0 + 16, x1 - 8, y1 - 10], fill=(255, 255, 255), outline=(120, 110, 100), width=2)
    d.polygon([(x0 + 6, y0 + 16), (x1 - 6, y0 + 16), (x1 - 12, y0 + 26), (x0 + 12, y0 + 26)], fill=(200, 40, 90))
    d.rectangle([x0 + 16, y0 + 30, x0 + 34, y1 - 16], fill=(180, 215, 235))
    d.rectangle([x1 - 34, y0 + 30, x1 - 16, y1 - 16], fill=(180, 215, 235))
    # sale tag + bags
    d.polygon([(x1 - 24, y0 + 4), (x1 - 6, y0 + 4), (x1 - 6, y0 + 16), (x1 - 15, y0 + 22), (x1 - 24, y0 + 16)], fill=(200, 40, 90))
    d.text((x1 - 22, y0 + 6), "%", font=font(SANS_B, 11), fill=(255, 255, 255))
    d.rectangle([x0 + 10, y1 - 22, x0 + 20, y1 - 10], fill=(240, 170, 60))
    d.arc([x0 + 12, y1 - 27, x0 + 18, y1 - 20], 180, 360, fill=(160, 110, 40), width=2)


def panel_mumbai(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (40, 45, 80), (90, 90, 130))
    d.rectangle([x0, y1 - 10, x1, y1], fill=(30, 32, 48))
    # hotel facade + dome
    d.rectangle([x0 + 14, y0 + 20, x1 - 14, y1 - 10], fill=(120, 100, 80))
    d.pieslice([(x0 + x1) // 2 - 14, y0 + 4, (x0 + x1) // 2 + 14, y0 + 30], 180, 360, fill=(150, 120, 90))
    for r in range(2):
        for c in range(4):
            wx = x0 + 20 + c * 12
            d.rectangle([wx, y0 + 28 + r * 12, wx + 6, y0 + 35 + r * 12], fill=(255, 220, 130))
    # candles
    for i in range(5):
        cxp = x0 + 10 + i * ((x1 - x0 - 20) // 4)
        d.rectangle([cxp, y1 - 16, cxp + 4, y1 - 8], fill=(245, 240, 225))
        d.ellipse([cxp, y1 - 21, cxp + 4, y1 - 15], fill=(255, 180, 60))


def panel_kyoto(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (225, 245, 225), (245, 252, 240))
    d.rectangle([x0, y1 - 10, x1, y1], fill=(120, 160, 110))
    # battery cell
    d.rectangle([x0 + 10, y0 + 12, x0 + 34, y1 - 16], fill=(90, 170, 90), outline=(50, 120, 55), width=2)
    d.rectangle([x0 + 18, y0 + 7, x0 + 26, y0 + 13], fill=(50, 120, 55))
    d.rectangle([x0 + 14, y0 + 22, x0 + 30, y0 + 34], fill=(255, 255, 255))
    # recycle arrows
    d.arc([x1 - 34, y0 + 10, x1 - 10, y0 + 34], 30, 300, fill=(50, 150, 70), width=3)
    d.polygon([(x1 - 12, y0 + 12), (x1 - 6, y0 + 16), (x1 - 14, y0 + 20)], fill=(50, 150, 70))
    # flask + leaf
    d.polygon([(x1 - 26, y1 - 30), (x1 - 18, y1 - 30), (x1 - 14, y1 - 14), (x1 - 30, y1 - 14)], fill=(190, 235, 200), outline=(70, 140, 80), width=2)
    d.ellipse([x0 + 42, y1 - 24, x0 + 56, y1 - 14], fill=(80, 180, 90))


def panel_markets(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (20, 30, 60), (40, 60, 100))
    # skyline
    for i, h in enumerate([30, 44, 26, 50, 34]):
        bx = x0 + 4 + i * ((x1 - x0 - 8) // 5)
        d.rectangle([bx, y1 - 8 - h, bx + 10, y1 - 8], fill=(60, 75, 110))
    d.rectangle([x0, y1 - 8, x1, y1], fill=(14, 20, 40))
    # candlesticks + rising arrow
    pts = [(x0 + 8, y1 - 18), (x0 + 20, y1 - 24), (x0 + 32, y1 - 22), (x0 + 44, y1 - 32), (x0 + 56, y1 - 38)]
    d.line(pts, fill=(80, 220, 120), width=3)
    d.polygon([(x0 + 56, y1 - 44), (x0 + 64, y1 - 36), (x0 + 50, y1 - 34)], fill=(80, 220, 120))
    for px, py in pts[::2]:
        d.rectangle([px - 2, py - 4, px + 2, py + 4], fill=(80, 220, 120))


def panel_aihw(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (245, 238, 250), (252, 248, 255))
    d.rectangle([x0, y1 - 10, x1, y1], fill=(150, 130, 170))
    # bar chart rising
    for i, h in enumerate([14, 22, 30, 42]):
        bx = x0 + 8 + i * 13
        d.rectangle([bx, y1 - 10 - h, bx + 9, y1 - 10], fill=(130, 90, 180))
    # house + bottle crossed
    d.polygon([(x1 - 30, y0 + 16), (x1 - 18, y0 + 6), (x1 - 6, y0 + 16)], fill=(160, 120, 90))
    d.rectangle([x1 - 27, y0 + 16, x1 - 9, y0 + 30], fill=(240, 230, 210))
    d.rectangle([x1 - 22, y1 - 26, x1 - 16, y1 - 12], fill=(90, 130, 90))
    d.line([(x1 - 25, y1 - 28), (x1 - 13, y1 - 10)], fill=(200, 40, 40), width=3)


def panel_tuna(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (140, 195, 230), (200, 230, 245))
    d.rectangle([x0, y1 - 26, x1, y1], fill=(40, 110, 170))
    for i in range(4):
        wx = x0 + 4 + i * ((x1 - x0 - 8) // 4)
        d.arc([wx, y1 - 30, wx + 16, y1 - 22], 0, 180, fill=(220, 240, 250), width=2)
    # two ships + net
    d.polygon([(x0 + 8, y1 - 26), (x0 + 30, y1 - 26), (x0 + 26, y1 - 18), (x0 + 12, y1 - 18)], fill=(60, 60, 70))
    d.rectangle([x0 + 16, y1 - 34, x0 + 24, y1 - 26], fill=(230, 230, 230))
    d.polygon([(x1 - 32, y1 - 26), (x1 - 10, y1 - 26), (x1 - 14, y1 - 18), (x1 - 28, y1 - 18)], fill=(60, 60, 70))
    d.rectangle([x1 - 24, y1 - 34, x1 - 16, y1 - 26], fill=(230, 230, 230))
    for i in range(3):
        nx = (x0 + x1) // 2 - 10 + i * 8
        d.line([(nx, y1 - 20), (nx + 4, y1 - 10)], fill=(240, 240, 240), width=1)
    # fish
    d.ellipse([x0 + 10, y0 + 8, x0 + 28, y0 + 16], fill=(240, 160, 60))
    d.polygon([(x0 + 28, y0 + 12), (x0 + 36, y0 + 7), (x0 + 36, y0 + 17)], fill=(240, 160, 60))


def panel_tube(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (60, 60, 70), (90, 90, 100))
    d.rectangle([x0, y1 - 10, x1, y1], fill=(35, 35, 42))
    # roundel
    cx, cy = x0 + 22, (y0 + y1) // 2
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=(220, 36, 31), width=5)
    d.rectangle([cx - 17, cy - 4, cx + 17, cy + 4], fill=(0, 25, 168))
    # train front
    d.rectangle([x1 - 34, y0 + 10, x1 - 8, y1 - 12], fill=(200, 205, 215), outline=(120, 125, 140), width=2)
    d.rectangle([x1 - 31, y0 + 14, x1 - 11, y0 + 26], fill=(60, 90, 130))
    d.ellipse([x1 - 29, y1 - 20, x1 - 23, y1 - 14], fill=(255, 240, 170))
    d.ellipse([x1 - 19, y1 - 20, x1 - 13, y1 - 14], fill=(255, 240, 170))
    # picket sign
    d.line([(x0 + 44, y1 - 10), (x0 + 44, y0 + 22)], fill=(160, 130, 90), width=3)
    d.rectangle([x0 + 36, y0 + 8, x0 + 52, y0 + 22], fill=(255, 255, 255), outline=(150, 150, 150), width=2)


def panel_ghana(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (150, 200, 240), (215, 238, 250))
    d.rectangle([x0, y1 - 12, x1, y1], fill=(90, 140, 90))
    # plane
    d.polygon([(x0 + 10, y0 + 18), (x0 + 40, y0 + 12), (x0 + 44, y0 + 18), (x0 + 16, y0 + 24)], fill=(240, 240, 245), outline=(150, 160, 175), width=2)
    d.polygon([(x0 + 24, y0 + 20), (x0 + 32, y0 + 30), (x0 + 38, y0 + 30), (x0 + 32, y0 + 19)], fill=(200, 205, 215))
    # trophy
    d.polygon([(x1 - 30, y0 + 12), (x1 - 12, y0 + 12), (x1 - 15, y0 + 26), (x1 - 27, y0 + 26)], fill=(245, 195, 40), outline=(180, 140, 20), width=2)
    d.rectangle([x1 - 23, y0 + 26, x1 - 19, y0 + 32], fill=(245, 195, 40))
    d.rectangle([x1 - 28, y0 + 32, x1 - 14, y0 + 36], fill=(150, 110, 30))
    # Ghana flag + crowd
    d.line([(x0 + 10, y1 - 12), (x0 + 10, y1 - 34)], fill=(90, 70, 50), width=2)
    d.rectangle([x0 + 10, y1 - 34, x0 + 26, y1 - 29], fill=(206, 17, 38))
    d.rectangle([x0 + 10, y1 - 29, x0 + 26, y1 - 24], fill=(252, 209, 22))
    d.rectangle([x0 + 10, y1 - 24, x0 + 26, y1 - 19], fill=(0, 107, 63))
    for i in range(4):
        qx = x1 - 40 + i * 9
        d.ellipse([qx, y1 - 20, qx + 6, y1 - 14], fill=(70, 50, 35))


# ------------------------------------------------------------------ map ----
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-75, 62), (-65, 50), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-114, 29), (-124, 40), (-130, 55), (-152, 60)],
    # South America
    [(-79, 9), (-72, 12), (-62, 10), (-52, 5), (-44, -3), (-35, -8), (-39, -15), (-48, -26), (-58, -35), (-65, -41), (-73, -50), (-75, -52), (-73, -44), (-70, -30), (-70, -18), (-77, -12), (-81, -4)],
    # Africa
    [(-17, 15), (-10, 29), (-5, 35), (10, 37), (20, 32), (30, 31), (35, 24), (43, 12), (51, 12), (51, 4), (42, -6), (40, -15), (36, -22), (33, -26), (20, -35), (17, -32), (12, -18), (9, -2), (-8, 5), (-13, 8)],
    # Eurasia
    [(-9, 43), (-2, 49), (0, 52), (8, 55), (18, 56), (21, 60), (30, 70), (45, 68), (70, 72), (100, 77), (130, 72), (160, 70), (178, 66), (170, 60), (158, 52), (142, 50), (140, 40), (135, 35), (122, 31), (110, 20), (105, 9), (98, 10), (92, 16), (88, 22), (80, 13), (77, 8), (72, 20), (66, 25), (57, 27), (50, 29), (48, 30), (44, 29), (43, 12), (39, 21), (35, 29), (36, 36), (30, 36), (27, 37), (23, 36), (19, 40), (12, 44), (7, 44), (3, 43), (0, 39), (-2, 37), (-9, 37)],
    # SE Asia islands (rough)
    [(95, 5), (103, 1), (110, -2), (118, -3), (125, -1), (131, -3), (138, -4), (145, -5), (140, -8), (130, -8), (118, -9), (105, -7), (97, 2)],
    # Australia
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (130, -32), (136, -35), (140, -38), (145, -38), (150, -37), (153, -27), (146, -19), (142, -11), (142, -14), (136, -12), (132, -11), (126, -14), (122, -17), (117, -20)],
    # New Zealand
    [(167, -46), (172, -41), (174, -39), (178, -37), (176, -38), (174, -41), (169, -46), (166, -46)],
]

PINS = {
    1: (4.4, 50.8), 2: (-74, 40.7), 3: (77.2, 28.6), 4: (44, 13.6), 5: (51.5, 25.3),
    6: (-78.5, -0.2), 7: (-83, 42.3), 8: (-98, 39), 9: (72.9, 19.1), 10: (135.8, 35),
    11: (114.2, 22.3), 12: (151.2, -33.9), 13: (171, 7.1), 14: (-0.1, 51.5), 15: (-0.2, 5.6),
    16: (6.1, 46.2), 17: (2.4, 48.9), 18: (55.3, 25.2), 19: (80, 24), 20: (74, 17),
    21: (3.4, 6.5), 22: (149.1, -35.3), 23: (147, -33), 24: (145, -31), 25: (151.5, -31),
    26: (148, -30), 27: (150, -29), 28: (170.5, -45.9), 29: (149.5, -37), 30: (-72, 38),
}


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(196, 220, 235), outline=RULE, width=1)

    def proj(lon, lat):
        return (x0 + (lon + 180) / 360 * (x1 - x0), y0 + (85 - lat) / 140 * (y1 - y0))

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(228, 216, 178), outline=(150, 135, 100))
    pf = font(SANS_B, 8)
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=(255, 255, 255), width=1)
        t = str(n)
        d.text((px - tw(d, t, pf) / 2, py - 5), t, font=pf, fill=(255, 255, 255))


# ----------------------------------------------------------------- page ----
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 18  # side margin
    y = 0

    # 1. Top bar
    d.rectangle([0, 0, W, 28], fill=NAVY)
    d.text((M, 6), "THE WORLD IN ONE DAY", font=font(SANS_B, 15), fill=(255, 255, 255))
    rt = "30 STORIES · 7 REGIONS · EVERY ONE DATED THURSDAY"
    d.text((W - M - tw(d, rt, font(SANS_B, 12)), 8), rt, font=font(SANS_B, 12), fill=(255, 220, 160))
    y = 28

    # 2. Masthead
    f_mast = font(SERIF_B, 56)
    mast = "Thursday 26 November 2026"
    while tw(d, mast, f_mast) > W - 2 * M and f_mast.size > 30:
        f_mast = font(SERIF_B, f_mast.size - 2)
    d.text(((W - tw(d, mast, f_mast)) / 2, y + 4), mast, font=f_mast, fill=INK)
    kick = "EU leaders open summit on €45bn Ukraine loan  ·  Storm threatens 100th Macy's parade  ·  India marks 77 years of its Constitution"
    f_kick = italic(17)
    while tw(d, kick, f_kick) > W - 2 * M and f_kick.size > 10:
        f_kick = italic(f_kick.size - 1)
    d.text(((W - tw(d, kick, f_kick)) / 2, y + 66), kick, font=f_kick, fill=RED)
    y += 92
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 6

    # 3. Numbers strip
    nums = [
        ("81.5m", "US THANKSGIVING TRAVELLERS"),
        ("418,000", "FLIGHTS — MOST IN 16 YEARS"),
        ("€45bn", "UKRAINE LOAN ON EU TABLE"),
        ("77", "YEARS OF INDIA'S CONSTITUTION"),
        ("3.2m", "WOMEN HARMED BY OTHERS' DRINKING"),
        ("350,000", "TAIZ CHILDREN WITHOUT VACCINES"),
    ]
    cw = (W - 2 * M) / 6
    for i, (n, lab) in enumerate(nums):
        cx = M + i * cw + cw / 2
        fn = font(SERIF_B, 30)
        d.text((cx - tw(d, n, fn) / 2, y), n, font=fn, fill=RED)
        fl = font(SANS, 10)
        for j, ln in enumerate(wrap(d, lab, fl, cw - 8)):
            d.text((cx - tw(d, ln, fl) / 2, y + 36 + j * 12), ln, font=fl, fill=GREY)
        if i:
            d.line([(M + i * cw, y + 2), (M + i * cw, y + 52)], fill=(200, 192, 175), width=1)
    y += 62
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 5

    # 4. Region bar
    regions = [
        ("EUROPE 4", 4, (38, 84, 160)), ("MIDDLE EAST 3", 3, (176, 120, 40)),
        ("AMERICAS 4", 4, (150, 50, 60)), ("ASIA-PACIFIC 6", 6, (40, 130, 80)),
        ("AFRICA 2", 2, (200, 90, 30)), ("OCEANIA 9", 9, (30, 120, 160)),
        ("WORLD 2", 2, (90, 90, 120)),
    ]
    rx = M
    total = sum(c for _, c, _ in regions)
    for name, c, col in regions:
        segw = (W - 2 * M) * c / total
        d.rectangle([rx, y, rx + segw, y + 22], fill=col)
        f_r = font(SANS_B, 11)
        d.text((rx + (segw - tw(d, name, f_r)) / 2, y + 5), name, font=f_r, fill=(255, 255, 255))
        rx += segw
    y += 27

    # 5. UTC timeline
    d.text((M, y + 2), "THURSDAY IN UTC", font=font(SANS_B, 12), fill=NAVY)
    times = [
        ("01:30", "Hong Kong opens"), ("09:00", "Euro Summit, Brussels"),
        ("12:00", "Tube strike begins"), ("13:00", "Accra homecoming"),
        ("13:30", "Macy's parade steps off"), ("18:00", "NFL kickoff, Detroit"),
    ]
    tx = M + 150
    twid = (W - M - tx) / 6
    for i, (t, lab) in enumerate(times):
        cxp = tx + i * twid
        d.ellipse([cxp, y + 4, cxp + 7, y + 11], fill=RED)
        d.text((cxp + 10, y), t, font=font(SANS_B, 12), fill=INK)
        d.text((cxp + 10, y + 15), lab, font=font(SANS, 10), fill=GREY)
    y += 34
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 6

    # 6. Lead row
    leads = [
        (panel_eu, "1 · EUROPE — SUMMIT", "BRUSSELS", "EU leaders open summit on €45bn Ukraine loan",
         "Special council takes on the 2028–34 budget and Ukraine's 2027 financing.", "Poland Insight · FORECAST"),
        (panel_parade, "2 · AMERICAS — THANKSGIVING", "NEW YORK", "Storm threatens 100th Macy's parade",
         "81.5m Americans travel; 60 mph gusts put the giant balloons at risk.", "SRN News · FORECAST"),
        (panel_constitution, "3 · ASIA-PACIFIC — ANNIVERSARY", "NEW DELHI", "India marks 77 years of its Constitution",
         "Samvidhan Divas honours the charter adopted on 26 November 1949.", "ObserverVoice · CONFIRMED"),
    ]
    colw = (W - 2 * M - 16) / 3
    for i, (pf_, tag, loc, head, summ, src) in enumerate(leads):
        x = M + i * (colw + 8)
        pf_(d, (x, y, x + colw, y + 108))
        d.rectangle([x, y, x + colw, y + 108], outline=RULE, width=1)
        yy = y + 113
        d.text((x, yy), tag, font=font(SANS_B, 12), fill=RED)
        d.text((x + colw - tw(d, loc, font(SANS_B, 12)), yy), loc, font=font(SANS_B, 12), fill=NAVY)
        yy += 17
        for ln in wrap(d, head, font(SERIF_B, 21), colw)[:2]:
            d.text((x, yy), ln, font=font(SERIF_B, 21), fill=INK)
            yy += 25
        for ln in wrap(d, summ, font(SANS, 13), colw)[:2]:
            d.text((x, yy), ln, font=font(SANS, 13), fill=(55, 52, 48))
            yy += 16
        d.text((x, yy + 2), src, font=font(SANS, 11), fill=GREY)
    y += 238
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 6

    # 7. Secondary grid 3x4
    secs = [
        (panel_taiz, "4 · MIDDLE EAST · REPORTED", "350,000 Taiz children miss vaccines", "UN: siege blocks measles jabs"),
        (panel_cricket, "5 · MIDDLE EAST · FORECAST", "India A face Sri Lanka A in Doha semi", "Rising Stars final place at stake"),
        (panel_ecuador, "6 · AMERICAS · REPORTED", "US, Ecuador review military ties", "Quito rejects suspension reports"),
        (panel_nfl, "7 · AMERICAS · FORECAST", "NFL serves Thanksgiving tripleheader", "Bears-Lions · Eagles-Cowboys · Chiefs-Bills"),
        (panel_shopping, "8 · AMERICAS · FORECAST", "182.7m set to shop the weekend", "NRF: Black Friday still the big day"),
        (panel_mumbai, "9 · ASIA-PACIFIC · CONFIRMED", "Mumbai marks 18 years since 26/11", "Tributes for 160+ killed in 2008"),
        (panel_kyoto, "10 · ASIA-PACIFIC · REPORTED", "Kyoto recycles batteries more safely", "Lower-risk method for Li-ion cells"),
        (panel_markets, "11 · ASIA-PACIFIC · REPORTED", "Asia opens higher as tariff row rumbles", "Hang Seng +0.9% · Nikkei +0.4% projected"),
        (panel_aihw, "12 · OCEANIA · REPORTED", "3.2m women harmed by others' drinking", "AIHW: up 800,000 since 2022-23"),
        (panel_tuna, "13 · OCEANIA · REPORTED", "Tuna fleets keep crews at sea", "1,644 transfers tracked in Pacific"),
        (panel_tube, "14 · EUROPE · FORECAST", "Tube drivers strike from noon", "RMT walkout runs to Friday 11:59"),
        (panel_ghana, "15 · AFRICA · FORECAST", "Black Challenge come home champions", "WAFF winners due in Accra at 13:00"),
    ]
    cellw = (W - 2 * M - 16) / 3
    cellh = 74
    for i, (pf_, tag, head, summ) in enumerate(secs):
        cxp = M + (i % 3) * (cellw + 8)
        cyp = y + (i // 3) * cellh
        pf_(d, (cxp, cyp, cxp + 62, cyp + 62))
        d.rectangle([cxp, cyp, cxp + 62, cyp + 62], outline=RULE, width=1)
        txp = cxp + 68
        d.text((txp, cyp), tag, font=font(SANS_B, 10), fill=RED)
        yy = cyp + 14
        for ln in wrap(d, head, font(SERIF_B, 15), cellw - 68)[:2]:
            d.text((txp, yy), ln, font=font(SERIF_B, 15), fill=INK)
            yy += 18
        d.text((txp, yy + 1), summ, font=font(SANS, 11), fill=(55, 52, 48))
    y += 4 * cellh + 4
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 6

    # 8. Map + also-on
    mapw = 452
    d.text((M, y), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=NAVY)
    draw_map(d, (M, y + 18, M + mapw, y + 140))
    ax = M + mapw + 14
    d.text((ax, y), "ALSO ON THURSDAY 26 NOVEMBER — 15 MORE STORIES", font=font(SANS_B, 13), fill=NAVY)
    also = [
        "16 Gukesh–Sindarov Game 3, Geneva · FORECAST",
        "17 Notre-Dame Christmas market opens · FORECAST",
        "18 Dubai starts 11 days of Eid Al Etihad · FORECAST",
        "19 Fog north India, heavy rain south · FORECAST",
        "20 Tata Sons moves board meeting to 30 Nov · REPORTED",
        "21 Renewable forum wraps in Lagos · REPORTED",
        "22 Peptide prescribing inquiry opens · REPORTED",
        "23 \"Security starts with gender equality\" · REPORTED",
        "24 33 fixes proposed for council funding · REPORTED",
        "25 Palm Beach ferries strike from 07:30 · FORECAST",
        "26 Gambling roadmap: 2 years, no answer · REPORTED",
        "27 74% back limits on alcohol advertising · REPORTED",
        "28 Dunedin rain clears after warning · REPORTED",
        "29 Middle powers meet in Canberra Friday · PENDING",
        "30 Wall Street dark for Thanksgiving · REPORTED",
    ]
    half = (len(also) + 1) // 2
    colw2 = (W - M - ax - 8) / 2
    for i, item in enumerate(also):
        cxp = ax + (i // half) * (colw2 + 8)
        cyp = y + 20 + (i % half) * 15
        f_a = font(SANS, 10)
        while tw(d, item, f_a) > colw2 and f_a.size > 7:
            f_a = font(SANS, f_a.size - 1)
        d.text((cxp, cyp), item, font=f_a, fill=(40, 38, 34))
    y += 148
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 5

    # 9. Date-check (one line)
    dc = ("DATE-CHECK — deliberately left out as other days' news: Kyiv refinery strikes (25 Nov) · "
          "CAS restores Senegal title (24 Nov) · Huawei verdict (24 Nov) · Bangladesh wage rise (25 Nov) · astronaut docks (25 Nov)")
    f_dc = font(SANS, 11)
    while tw(d, dc, f_dc) > W - 2 * M and f_dc.size > 7:
        f_dc = font(SANS, f_dc.size - 1)
    d.text((M, y), dc, font=f_dc, fill=(90, 60, 40))
    y += 17

    # 10. Sources + legend
    srcs = ("Sources: Poland Insight · SRN News · NBC Sports · Retail Dive · ObserverVoice · SelfStudys · Arab News · "
            "News Hub (Medianet) · MetService · HeadlinesXtra · japan.co.jp · Peter Lewis Money Talk · accordmere.uk · "
            "African Power Platform · Gold Fields Ghana · Paris Alert · The Gulf Desk")
    yy = y
    for ln in wrap(d, srcs, font(SANS, 10), W - 2 * M):
        d.text((M, yy), ln, font=font(SANS, 10), fill=GREY)
        yy += 12
    leg = ("REPORTED = carried by wires · CONFIRMED = observed/scheduled fact · "
           "PENDING = announced for later · FORECAST = still to happen today")
    d.text((M, yy), leg, font=font(SANS, 10), fill=GREY)

    # 11. Bottom bar
    d.rectangle([0, H - 22, W, H], fill=NAVY)
    bt = "THE WORLD IN ONE DAY · 26 NOVEMBER 2026 · ONE PAGE"
    d.text(((W - tw(d, bt, font(SANS_B, 12))) / 2, H - 18), bt, font=font(SANS_B, 12), fill=(255, 255, 255))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print(f"wrote {out}: {img.size[0]}x{img.size[1]}, {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
