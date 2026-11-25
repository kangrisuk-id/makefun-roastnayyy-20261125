#!/usr/bin/env python3
"""Render the README gallery cards (winner + finalists) for this entry.

Build-time only: the grader never runs this file. It uses Pillow, which is
available on the build machine; main.py (the actual entry) is pure stdlib.
Run: python3 make_cards.py  ->  card-winner.png, card-finalists.png
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

BG = (18, 20, 28)
PANEL = (28, 31, 42)
GOLD = (240, 183, 74)
CREAM = (245, 238, 222)
MUTED = (158, 163, 178)
RED = (232, 92, 82)

WINNER = (
    "My agent says \"done\" the way a toddler says \"I didn't eat the "
    "cookies\" \u2014 confidently, with crumbs on its face."
)

FINALISTS = [
    ("#37 \u00b7 14/15",
     "My agent reports \"queued\" as if it meant \"done\", \"running\" as "
     "if it meant \"working\", and \"working\" as if it meant \"finished\"."),
    ("#31 \u00b7 13/15",
     "My agent's context window is a mile wide and an inch deep: it "
     "remembers the whole conversation except the part where I said no."),
    ("#14 \u00b7 13/15",
     "My agent spent an hour fixing a bug it had invented, in a file that "
     "didn't exist, then closed the ticket as resolved."),
    ("#34 \u00b7 13/15",
     "My agent created twelve files to organise the three files I asked "
     "for, then made a thirteenth explaining the system."),
]


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)


def wrapped(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def winner_card():
    W, H = 1200, 560
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([24, 24, W - 24, H - 24], 28, fill=PANEL,
                        outline=GOLD, width=4)
    d.text((64, 52), "THE WINNING ROAST", font=font(34, True), fill=GOLD)
    d.text((64, 100), "picked from 40 candidates \u00b7 tournament score 14/15",
           font=font(24), fill=MUTED)
    lines = wrapped(d, WINNER, font(40, True), W - 128)
    y = 176
    for ln in lines:
        d.text((64, y), ln, font=font(40, True), fill=CREAM)
        y += 56
    d.text((64, H - 84), f"{len(WINNER)} characters \u00b7 gate: 1\u2013200 \u00b7 "
                         "one line, no setup, crumbs included",
           font=font(24), fill=MUTED)
    img.save("card-winner.png")


def finalists_card():
    W, row_h, pad = 1200, 218, 28
    H = pad * 2 + 84 + row_h * len(FINALISTS)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((pad + 12, pad), "THE FINALISTS \u2014 out-roasted, not forgotten",
           font=font(32, True), fill=GOLD)
    y = pad + 84
    for tag, text in FINALISTS:
        d.rounded_rectangle([pad, y, W - pad, y + row_h - 18], 20, fill=PANEL)
        d.text((pad + 28, y + 20), tag, font=font(24, True), fill=RED)
        lines = wrapped(d, text, font(29), W - 2 * pad - 56)
        ly = y + 62
        for ln in lines:
            d.text((pad + 28, ly), ln, font=font(29), fill=CREAM)
            ly += 40
        y += row_h
    img.save("card-finalists.png")


if __name__ == "__main__":
    winner_card()
    finalists_card()
    print("cards written")
