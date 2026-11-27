#!/usr/bin/env python3
"""
Draw the entry picture for make.fun's "Sum up 27 November's world news
in one image": a newspaper front page for Friday 27 November 2026.

Each story was reported on 27 Nov 2026 and cross-checked in at least
two independent outlets before it was drawn; SOURCES.md has the
per-story notes, including the items checked and left out.

The render is deterministic end to end: fixed canvas, fixed font
files, no randomness, no clock, no network. Two runs, same bytes.
Output: ../entry.png (1024 x 1024).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas

SIDE = 1024
PAPER = (247, 242, 232)
CARD = (255, 253, 246)
INK = (23, 20, 15)
FAINT = (105, 96, 80)
LINE = (208, 198, 174)
RED = (176, 36, 28)
BLUE = (30, 66, 112)
GOLD = (176, 130, 42)
BAND = (26, 27, 32)

F_SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
F_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
F_TEXT = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


page = Image.new("RGB", (SIDE, SIDE), PAPER)
pen = ImageDraw.Draw(page)

EDGE = 40
WIDE = SIDE - 2 * EDGE


def fit_lines(text, fnt, width):
    """Split text into lines that fit `width` pixels in font `fnt`."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if pen.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def para(x, y, text, fnt, colour, width, step):
    for line in fit_lines(text, fnt, width):
        pen.text((x, y), line, font=fnt, fill=colour)
        y += step
    return y


def centred(y, text, fnt, colour):
    w = pen.textlength(text, font=fnt)
    pen.text(((SIDE - w) / 2, y), text, font=fnt, fill=colour)


# ---------------------------------------------------------------- masthead

pen.text((EDGE, 24), "THE WORLD'S NEWS · ONE DAY · ONE PICTURE",
         font=F(F_BOLD, 22), fill=RED)
pen.line([(EDGE, 58), (SIDE - EDGE, 58)], fill=INK, width=3)

centred(70, "THE DAY IN FULL", F(F_SERIF, 64), INK)

pen.rectangle([EDGE, 152, SIDE - EDGE, 208], fill=RED)
centred(162, "FRIDAY  27 NOVEMBER 2026", F(F_BOLD, 40), (255, 250, 240))
pen.line([(EDGE, 220), (SIDE - EDGE, 220)], fill=INK, width=3)

# ---------------------------------------------------------------- icons
# Flat spot art, one per story. Each icon draws inside a box roughly
# 120 wide x 92 tall at (x, y), scaled by s.


def icon_drone(x, y, s):
    """Quadcopter drone with a burst beneath it (Iran war / Kuwait)."""
    bx, by = x + int(60 * s), y + int(30 * s)
    pen.rectangle([bx - int(17 * s), by - int(9 * s),
                   bx + int(17 * s), by + int(9 * s)], fill=INK)
    for dx, dy in ((-38, -16), (38, -16), (-38, 16), (38, 16)):
        ax, ay = bx + int(dx * s), by + int(dy * s)
        pen.line([(bx, by), (ax, ay)], fill=INK, width=max(2, int(3 * s)))
        rw = int(15 * s)
        pen.ellipse([ax - rw, ay - int(4 * s), ax + rw, ay + int(4 * s)],
                    outline=BLUE, width=max(2, int(3 * s)))
    r = int(5 * s)
    pen.ellipse([bx - r, by + int(12 * s), bx + r, by + int(12 * s) + 2 * r],
                fill=RED)
    sx, sy = bx + int(30 * s), y + int(70 * s)
    for ang in range(0, 360, 45):
        ex = sx + int(14 * s * math.cos(math.radians(ang)))
        ey = sy + int(14 * s * math.sin(math.radians(ang)))
        pen.line([(sx, sy), (ex, ey)], fill=RED, width=max(2, int(3 * s)))


def icon_ballot(x, y, s):
    """Ballot paper with a tick dropping into a box (New Zealand)."""
    px, py = x + int(38 * s), y
    pen.rectangle([px, py, px + int(44 * s), py + int(52 * s)], fill=CARD,
                  outline=INK, width=max(2, int(3 * s)))
    pen.line([(px + int(9 * s), py + int(30 * s)), (px + int(19 * s),
              py + int(41 * s)), (px + int(36 * s), py + int(14 * s))],
             fill=RED, width=max(2, int(5 * s)))
    bx, by = x + int(14 * s), y + int(58 * s)
    pen.polygon([(bx, by), (bx + int(92 * s), by), (bx + int(84 * s),
                  by + int(28 * s)), (bx + int(8 * s), by + int(28 * s))],
                fill=BLUE)
    pen.rectangle([bx + int(26 * s), by + int(5 * s), bx + int(66 * s),
                   by + int(10 * s)], fill=PAPER)


def icon_ban(x, y, s):
    """Shield behind a prohibition sign (Australia sanctions)."""
    cx, top = x + int(46 * s), y + int(2 * s)
    shield = [(cx - int(30 * s), top), (cx + int(30 * s), top),
              (cx + int(30 * s), top + int(38 * s)),
              (cx, top + int(66 * s)), (cx - int(30 * s), top + int(38 * s))]
    pen.polygon(shield, fill=BLUE)
    bx, by, r = x + int(84 * s), y + int(58 * s), int(24 * s)
    pen.ellipse([bx - r, by - r, bx + r, by + r], outline=RED,
                width=max(3, int(6 * s)))
    dxy = int(r * 0.72)
    pen.line([(bx - dxy, by + dxy), (bx + dxy, by - dxy)], fill=RED,
             width=max(3, int(6 * s)))


def icon_yen(x, y, s):
    """Rising bars and a yen coin (Japan defence plan)."""
    base = y + int(84 * s)
    for i, h in enumerate((26, 42, 60)):
        bx = x + int((6 + i * 26) * s)
        pen.rectangle([bx, base - int(h * s), bx + int(19 * s), base],
                      fill=BLUE if i < 2 else RED)
    pen.line([(x, base), (x + int(86 * s), base)], fill=INK,
             width=max(2, int(3 * s)))
    cx, cy, r = x + int(96 * s), y + int(22 * s), int(21 * s)
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    pen.text((cx, cy), "¥", font=F(F_BOLD, int(30 * s)), fill=INK,
             anchor="mm")


def icon_eu(x, y, s):
    """Ring of stars around a euro sign (EU budget talks)."""
    cx, cy = x + int(52 * s), y + int(42 * s)
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx = cx + int(38 * s * math.cos(a))
        sy = cy + int(38 * s * math.sin(a))
        r = max(2, int(4 * s))
        pen.ellipse([sx - r, sy - r, sx + r, sy + r], fill=GOLD)
    pen.text((cx, cy), "€", font=F(F_SERIF, int(46 * s)), fill=BLUE,
             anchor="mm")


def icon_barrel(x, y, s):
    """Oil drum with a droplet (markets / oil)."""
    bx, by = x + int(30 * s), y + int(8 * s)
    bw, bh = int(46 * s), int(76 * s)
    pen.rounded_rectangle([bx, by, bx + bw, by + bh], radius=int(8 * s),
                          fill=INK)
    for f in (0.3, 0.62):
        ry = by + int(bh * f)
        pen.line([(bx + int(3 * s), ry), (bx + bw - int(3 * s), ry)],
                 fill=PAPER, width=max(2, int(3 * s)))
    dx, dy = x + int(94 * s), y + int(30 * s)
    pen.polygon([(dx, dy - int(16 * s)), (dx + int(12 * s), dy + int(8 * s)),
                 (dx - int(12 * s), dy + int(8 * s))], fill=RED)
    r = int(11 * s)
    pen.ellipse([dx - r, dy, dx + r, dy + 2 * r], fill=RED)


def icon_storm(x, y, s):
    """Storm cloud, lightning bolt and wind streaks (US storm)."""
    pen.ellipse([x + int(10 * s), y + int(18 * s), x + int(62 * s),
                 y + int(58 * s)], fill=BLUE)
    pen.ellipse([x + int(42 * s), y + int(8 * s), x + int(102 * s),
                 y + int(58 * s)], fill=BLUE)
    pen.rectangle([x + int(16 * s), y + int(38 * s), x + int(96 * s),
                   y + int(58 * s)], fill=BLUE)
    bx, by = x + int(52 * s), y + int(52 * s)
    pen.polygon([(bx, by), (bx + int(20 * s), by), (bx + int(8 * s),
                  by + int(18 * s)), (bx + int(20 * s), by + int(18 * s)),
                 (bx - int(4 * s), by + int(42 * s)), (bx + int(2 * s),
                  by + int(22 * s)), (bx - int(10 * s), by + int(22 * s))],
                fill=GOLD)
    for i, ln in enumerate((30, 22)):
        wy = y + int((66 + i * 13) * s)
        pen.line([(x + int(4 * s), wy), (x + int((4 + ln) * s), wy)],
                 fill=FAINT, width=max(2, int(3 * s)))


# ---------------------------------------------------------------- lead story

LEAD = {
    "tag": "TOP STORY — IRAN WAR · KUWAIT",
    "title": "Trump claims 'victory at hand' in war on Iran",
    "body": ("In Thanksgiving calls to US troops, he said Washington has "
             "“victory at hand” and offered Tehran a deal. Iran denies "
             "the drone attack on Kuwait that killed two Italians in "
             "falling debris, calling it “suspicious”."),
}

LY = 238
pen.rectangle([EDGE, LY, SIDE - EDGE, LY + 244], fill=CARD)
pen.rectangle([EDGE, LY, EDGE + 10, LY + 244], fill=RED)
pen.text((EDGE + 30, LY + 18), LEAD["tag"], font=F(F_BOLD, 21), fill=RED)
ly = para(EDGE + 30, LY + 50, LEAD["title"], F(F_SERIF, 36), INK, 630, 44)
para(EDGE + 30, ly + 10, LEAD["body"], F(F_TEXT, 20), INK, 630, 26)
icon_drone(EDGE + 690, LY + 62, 1.55)

# ---------------------------------------------------------------- story grid

CARDS = [
    ("WELLINGTON · NEW ZEALAND", "NZ coalition one seat short",
     "Final count: Luxon's bloc holds 65 of 130 seats; the Opportunity "
     "Party holds the balance.", icon_ballot),
    ("CANBERRA · AUSTRALIA", "Australia sanctions two over IRGC arson",
     "Canberra blacklists two men over 2024 arson attacks run, it says, "
     "by Iran's Revolutionary Guards.", icon_ban),
    ("TOKYO · JAPAN", "Japan weighs $353bn defence plan",
     "¥56.3 trillion over five years from 2027 — more than today, below "
     "the military's bid.", icon_yen),
    ("BRUSSELS · EUROPEAN UNION", "EU budget talks called off",
     "No deal on the near-€2tn budget or a $49bn Ukraine loan; leaders "
     "retry on 17 December.", icon_eu),
    ("MARKETS · OIL", "Oil climbs on Hormuz attacks",
     "Brent neared $96, set for its first weekly gain in four as tanker "
     "attacks squeeze supply.", icon_barrel),
    ("US EAST COAST · STORM", "Storm leaves a million US homes dark",
     "Over a million customers lost power; 1,200 flights cancelled; the "
     "parade moves to Saturday.", icon_storm),
]


def headline(x, y, text):
    """Card headline: the first line is narrower so it clears the icon
    in the top-right corner; following lines use the full card width."""
    fnt = F(F_SERIF, 23)
    words = text.split()
    first, rest = "", words
    for i, word in enumerate(words):
        trial = word if not first else first + " " + word
        if pen.textlength(trial, font=fnt) <= 186:
            first = trial
        else:
            rest = words[i:]
            break
    else:
        rest = []
    if first:
        pen.text((x, y), first, font=fnt, fill=INK)
    if rest:
        para(x, y + 28, " ".join(rest), fnt, INK, CW - 28, 28)


GY = 496
CW = (WIDE - 2 * 18) // 3
CH = 206
for idx, (tag, title, body, icon) in enumerate(CARDS):
    cx = EDGE + (idx % 3) * (CW + 18)
    cy = GY + (idx // 3) * (CH + 8)
    pen.rectangle([cx, cy, cx + CW, cy + CH], fill=CARD)
    pen.line([(cx, cy), (cx + CW, cy)], fill=INK, width=3)
    pen.text((cx + 14, cy + 12), tag, font=F(F_BOLD, 17), fill=RED)
    icon(cx + CW - 80, cy + 34, 0.55)
    headline(cx + 14, cy + 48, title)
    para(cx + 14, cy + 140, body, F(F_TEXT, 17), INK, CW - 28, 21)

# ---------------------------------------------------------------- ticker

TY = 924
pen.rectangle([EDGE, TY, SIDE - EDGE, TY + 64], fill=BAND)
pen.text((EDGE + 16, TY + 6), "ALSO FRIDAY", font=F(F_BOLD, 17),
         fill=(240, 190, 90))
para(EDGE + 16, TY + 27,
     "Houthi attack on Saudi Arabia's Jazan refinery kills a worker, "
     "draws condemnation · Tokyo core inflation hits a 16-month high of "
     "2.9% · UK car output rises 4.8% after last year's cyber shutdown",
     F(F_TEXT, 16), (238, 234, 224), WIDE - 32, 19)

# ---------------------------------------------------------------- colophon

pen.line([(EDGE, 996), (SIDE - EDGE, 996)], fill=LINE, width=2)
centred(1000, "Compiled from reports by Reuters, AP, AFP, Al Jazeera, "
              "Dawn, Nikkei Asia and Kyodo — 27 November 2026",
        F(F_TEXT, 14), FAINT)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "entry.png")
page.save(out_path)
print("wrote", out_path, page.size)
