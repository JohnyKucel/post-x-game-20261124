#!/usr/bin/env python3
"""Render the frames of the post-x-game video (1080x1920, 30fps).
Scene 1 (0-4s): the one prompt, typed out.
Scene 2 (4-12s): the agent working - code lines appear + terminal ticks.
Scene 3 (12-24s): the finished game actually running (deterministic sim of game.html).
Scene 4 handled by ffmpeg: last frame frozen + make.fun referral card overlay.
All frames are drawn fresh here in this session with PIL. No downloaded images.
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.expanduser("~/workspace/makefun/post-x-game-20261124/video/frames")
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
BG = (11, 11, 30)
GOLD = (255, 217, 77)
VIOLET = (124, 92, 255)
WHITE = (255, 255, 255)
MUTED = (157, 157, 196)
GREEN = (86, 220, 130)
RED = (255, 93, 93)

DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DJM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
DJMB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def star_poly(cx, cy, r, rot):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + rot + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
    return pts

# ---------------------------------------------------------------- scene 1
PROMPT = "Build me a tiny browser game \u2014 catch the falling stars. 60 seconds. With a score."
words = PROMPT.split(" ")
f_label = font(DJB, 44)
f_prompt = font(DJB, 72)
f_sub = font(DJ, 40)
for n in range(0, 4 * FPS):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for i in range(90):
        x, y = (i * 197) % W, (i * 353) % H
        d.ellipse([x, y, x + 3, y + 3], fill=(70, 70, 110))
    d.text((80, 300), "ONE PROMPT", font=f_label, fill=VIOLET)
    d.rounded_rectangle([60, 400, W - 60, 1000], radius=36, outline=(60, 60, 110), width=3, fill=(18, 18, 46))
    shown = words[: max(1, int(n / 4) + 1)] if n > 6 else []
    lines = wrap(d, " ".join(shown), f_prompt, W - 200)
    y = 470
    for ln in lines:
        d.text((100, y), ln, font=f_prompt, fill=WHITE)
        y += 96
    if n % 30 < 20 and shown:
        cx = 100 + d.textlength(lines[-1], font=f_prompt) if lines else 100
        d.rectangle([cx + 8, y - 96 + 12, cx + 18, y - 12], fill=GOLD)
    d.text((80, 1120), "my AI agent gets to work\u2026", font=f_sub, fill=MUTED)
    d.text((80, 1560), "no code written by hand", font=f_sub, fill=MUTED)
    img.save(f"{OUT}/f{n:04d}.png")

# ---------------------------------------------------------------- scene 2
CODE = [
    "const cv = document.getElementById('game');",
    "const ctx = cv.getContext('2d');",
    "let score = 0, lives = 3, timeLeft = 60;",
    "function spawnStar() {",
    "  stars.push({ x: rand(), y: -20, vy: 240 });",
    "}",
    "function drawStar(s) { /* gold glow */ }",
    "if (caught) { score++; burst(x, y); }",
    "requestAnimationFrame(step);",
]
TERM = [
    "$ agent working\u2026",
    "\u2713 canvas ready",
    "\u2713 stars falling",
    "\u2713 score counting",
    "\u2713 game running \u2014 play it!",
]
f_file = font(DJMB, 34)
f_code = font(DJM, 33)
f_term = font(DJM, 36)
for k in range(0, 8 * FPS):
    n = 4 * FPS + k
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([50, 140, W - 50, 1180], radius=28, fill=(16, 16, 40), outline=(60, 60, 110), width=3)
    for i, c in enumerate([(255, 93, 93), (255, 217, 77), (86, 220, 130)]):
        d.ellipse([90 + i * 52, 185, 118 + i * 52, 213], fill=c)
    d.text((300, 172), "game.html", font=f_file, fill=WHITE)
    nlines = min(len(CODE), int(k / 26) + 1)
    y = 270
    for i in range(nlines):
        d.text((80, y), f"{i+1:2d}", font=f_code, fill=(90, 90, 130))
        d.text((150, y), CODE[i], font=f_code, fill=WHITE)
        y += 62
    d.rounded_rectangle([50, 1260, W - 50, 1780], radius=28, fill=(8, 8, 22), outline=(60, 60, 110), width=3)
    tlines = min(len(TERM), max(0, int((k - 120) / 24) + 1)) if k >= 120 else 0
    y = 1310
    for i in range(tlines):
        col = GREEN if TERM[i].startswith("\u2713") else MUTED
        d.text((90, y), TERM[i], font=f_term, fill=col)
        y += 72
    img.save(f"{OUT}/f{n:04d}.png")

# ---------------------------------------------------------------- scene 3
random.seed(7)
GW, GH = 1080, 1920
pad = {"x": GW / 2, "w": 220, "h": 36, "y": GH - 150}
stars, rocks, parts = [], [], []
score, lives, tleft = 0, 3, 60.0
spawn_t = 0.0
bgdots = [(random.randint(0, GW), random.randint(0, GH), random.random()) for _ in range(70)]
f_hud = font(DJB, 58)
f_heart = font(DJB, 44)
f_big = font(DJB, 96)

def rnd(a, b):
    return a + random.random() * (b - a)

for k in range(0, 12 * FPS):
    n = 12 * FPS + k
    dt = 1.0 / FPS
    tleft = max(0.0, 60.0 - k * dt)
    spawn_t -= dt
    if spawn_t <= 0:
        stars.append({"x": rnd(40, GW - 40), "y": -30, "vy": rnd(300, 520), "r": rnd(24, 36), "rot": rnd(0, 6.28), "vr": rnd(-2, 2)})
        if random.random() < 0.35:
            rocks.append({"x": rnd(40, GW - 40), "y": -30, "vy": rnd(400, 640), "r": rnd(28, 40), "rot": rnd(0, 6.28), "vr": rnd(-3, 3)})
        spawn_t = rnd(0.35, 0.7)
    target = None
    if stars:
        target = min(stars, key=lambda s: s["y"])["x"] if False else max(stars, key=lambda s: s["y"])["x"]
    if target is not None:
        dx = target - pad["x"]
        step = max(-900 * dt, min(900 * dt, dx))
        pad["x"] += step
    pad["x"] = max(pad["w"] / 2, min(GW - pad["w"] / 2, pad["x"]))
    for s in stars:
        s["y"] += s["vy"] * dt
        s["rot"] += s["vr"] * dt
    for r in rocks:
        r["y"] += r["vy"] * dt
        r["rot"] += r["vr"] * dt
    keep = []
    for s in stars:
        if s["y"] - s["r"] > GH:
            continue
        if (s["y"] + s["r"] > pad["y"] and s["y"] - s["r"] < pad["y"] + pad["h"]
                and pad["x"] - pad["w"] / 2 < s["x"] < pad["x"] + pad["w"] / 2):
            score += 1
            for _ in range(12):
                a = rnd(0, 6.28)
                sp = rnd(120, 480)
                parts.append({"x": s["x"], "y": pad["y"], "vx": math.cos(a) * sp, "vy": math.sin(a) * sp, "life": 0.5, "c": GOLD})
            continue
        keep.append(s)
    stars = keep
    keep = []
    for r in rocks:
        if r["y"] - r["r"] > GH:
            continue
        if (r["y"] + r["r"] > pad["y"] and r["y"] - r["r"] < pad["y"] + pad["h"]
                and pad["x"] - pad["w"] / 2 < r["x"] < pad["x"] + pad["w"] / 2):
            lives -= 1
            for _ in range(12):
                a = rnd(0, 6.28)
                sp = rnd(120, 480)
                parts.append({"x": r["x"], "y": pad["y"], "vx": math.cos(a) * sp, "vy": math.sin(a) * sp, "life": 0.5, "c": RED})
            continue
        keep.append(r)
    rocks = keep
    for p in parts:
        p["x"] += p["vx"] * dt
        p["y"] += p["vy"] * dt
        p["life"] -= dt
    parts = [p for p in parts if p["life"] > 0]

    img = Image.new("RGB", (GW, GH), BG)
    d = ImageDraw.Draw(img, "RGBA")
    for (x, y, a) in bgdots:
        d.ellipse([x, y, x + 4, y + 4], fill=(255, 255, 255, int(60 + a * 120)))
    for s in stars:
        pts = star_poly(s["x"], s["y"], s["r"] + 10, s["rot"])
        d.polygon(pts, fill=(255, 217, 77, 60))
        d.polygon(star_poly(s["x"], s["y"], s["r"], s["rot"]), fill=GOLD)
    for r in rocks:
        pts = [(r["x"] + r["r"] * math.cos(r["rot"] + i * 1.256), r["y"] + r["r"] * math.sin(r["rot"] + i * 1.256)) for i in range(6)]
        d.polygon(pts, fill=(138, 143, 168))
    for p in parts:
        al = max(0, int(p["life"] * 2 * 255))
        d.rectangle([p["x"] - 6, p["y"] - 6, p["x"] + 6, p["y"] + 6], fill=p["c"] + (al,))
    d.rounded_rectangle([pad["x"] - pad["w"] / 2, pad["y"], pad["x"] + pad["w"] / 2, pad["y"] + pad["h"]], radius=18, fill=VIOLET)
    d.text((40, 60), f"SCORE {score}", font=f_hud, fill=WHITE)
    d.text((GW - 40, 60), f"{math.ceil(tleft)}s", font=f_hud, fill=WHITE, anchor="ra")
    d.text((40, 140), "\u2665" * max(0, lives), font=f_heart, fill=RED)
    if k < 45:
        d.rectangle([0, 0, GW, GH], fill=(11, 11, 30, int(200 * (1 - k / 45))))
        d.text((GW / 2, GH / 2 - 60), "STAR CATCH", font=f_big, fill=GOLD, anchor="mm")
        d.text((GW / 2, GH / 2 + 40), "catch the stars \u2022 dodge the rocks", font=font(DJ, 40), fill=WHITE, anchor="mm")
    img.save(f"{OUT}/f{n:04d}.png")

print("frames done:", len(os.listdir(OUT)), "score:", score, "lives:", lives)
