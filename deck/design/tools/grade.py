"""Apply one shared cool 'glacier' grade to every photo so they read as one family."""
import sys
import numpy as np
from PIL import Image

SHADOW = np.array([14, 31, 43]) / 255.0     # deep glacier-ink
HIGHLIGHT = np.array([242, 245, 244]) / 255.0  # snow


def grade(src, dst, max_side=1920):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    s = min(1.0, max_side / max(w, h))
    if s < 1:
        im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0
    lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]
    # pull saturation down
    a = lum + (a - lum) * 0.66
    # gradient-map tint toward ink/snow
    tint = SHADOW + (HIGHLIGHT - SHADOW) * lum
    a = a * 0.8 + tint * 0.2
    # gentle cool split: lift blue in shadows, a hair of warmth kept in highlights
    a[..., 2] += (1 - lum[..., 0]) * 0.03
    a[..., 0] -= (1 - lum[..., 0]) * 0.015
    # soft contrast curve
    a = np.clip(a, 0, 1)
    a = a + 0.06 * np.sin((a - 0.5) * np.pi) * 0.5
    a = np.clip(a, 0, 1)
    Image.fromarray((a * 255).round().astype(np.uint8)).save(dst, quality=86, optimize=True, progressive=True)


if __name__ == "__main__":
    for pair in sys.argv[1:]:
        s, d = pair.split("=")
        grade(s, d)
        print("graded", d)
