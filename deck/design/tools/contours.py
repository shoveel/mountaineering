"""Generate a topographic contour-line texture (SVG) for the deck."""
import math
import random
import sys

random.seed(7)
W, H = 1920, 1080
stroke = sys.argv[1]
out = sys.argv[2]

peaks = [(1500, 300, 15, 46), (360, 900, 10, 52), (1050, 1250, 8, 60)]
paths = []
for cx, cy, rings, step in peaks:
    harm = [(k, random.uniform(0.04, 0.12) / k ** 0.6, random.uniform(0, 6.28)) for k in range(2, 7)]
    for i in range(1, rings + 1):
        r0 = i * step
        pts = []
        n = 72
        for j in range(n):
            t = 2 * math.pi * j / n
            r = r0 * (1 + sum(a * math.sin(k * t + p + i * 0.07) for k, a, p in harm))
            pts.append((cx + r * math.cos(t) * 1.25, cy + r * math.sin(t)))
        d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + "Z"
        sw = 2.2 if i % 5 == 0 else 1.1
        paths.append(f'<path d="{d}" stroke-width="{sw}"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
       f'<g fill="none" stroke="{stroke}" stroke-linejoin="round">' + "".join(paths) + "</g></svg>")
open(out, "w").write(svg)
print(out, len(svg))
