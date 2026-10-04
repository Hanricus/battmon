"""Tukar Media.jfif (logo bulatan merah) jadi PNG kecil base64 untuk battmon.pyw.

Letak fail ni sebelah Media.jfif, lepas tu run:  python make_logo.py
Hasil: base64 dicopy ke clipboard dan disimpan dalam logo_b64.txt
Perlu Pillow:  pip install pillow
"""
import base64, io, os, subprocess
from PIL import Image

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "Media.jfif")
im = Image.open(src).convert("RGB")
w, h = im.size
px = im.load()

# Cari kawasan merah (bulatan logo). Bintang kecil di bucu tak berwarna merah
# jadi ia terbuang sekali masa crop.
xs, ys = [], []
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        if r > 120 and r > g + 60 and r > b + 60:
            xs.append(x)
            ys.append(y)
if not xs:
    raise SystemExit("Tak jumpa warna merah dalam gambar.")

x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
side = max(x1 - x0, y1 - y0) + 8
cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
im = im.crop((cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2)).resize((112, 112), Image.LANCZOS)

# Latar hitam jadi lutsinar supaya ngam dengan widget
out = Image.new("RGBA", im.size)
ip, op = im.load(), out.load()
for y in range(112):
    for x in range(112):
        r, g, b = ip[x, y]
        a = max(r, g, b)
        if a < 12:
            op[x, y] = (0, 0, 0, 0)
        else:
            op[x, y] = (min(255, r * 255 // a), min(255, g * 255 // a), min(255, b * 255 // a), a)

out = out.resize((28, 28), Image.LANCZOS)
buf = io.BytesIO()
out.save(buf, "PNG", optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode()

with open(os.path.join(here, "logo_b64.txt"), "w") as f:
    f.write(b64)
subprocess.run("clip", input=b64.encode(), shell=True)
print("Siap. Base64 dah dicopy ke clipboard dan disimpan dalam logo_b64.txt")
