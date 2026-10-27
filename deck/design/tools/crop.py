"""Pre-crop graded photos to the exact box each slide shows them in.
usage: python crop.py src dst W H cx cy zoom
cx, cy: focus point as fractions of the source; zoom >= 1 tightens the crop."""
import sys
from PIL import Image

src, dst, W, H, cx, cy, zoom = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7])
im = Image.open(src).convert("RGB")
w, h = im.size
ar = W / H
cw, ch = (w, w / ar) if w / h < ar else (h * ar, h)
cw, ch = cw / zoom, ch / zoom
x0 = min(max(cx * w - cw / 2, 0), w - cw)
y0 = min(max(cy * h - ch / 2, 0), h - ch)
im = im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch)))
scale = min(1.5, im.width / W) if im.width > W else im.width / W
out = im.resize((max(W, round(W * min(1.5, im.width / W))), max(H, round(H * min(1.5, im.width / W)))), Image.LANCZOS)
out.save(dst, quality=87, optimize=True, progressive=True)
print(dst, out.size)
