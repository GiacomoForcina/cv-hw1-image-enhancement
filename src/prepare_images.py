import cv2
from pathlib import Path

SRC = Path("foto_raw")
DST = Path("data/original")
MAX_SIDE = 1000

DST.mkdir(parents=True, exist_ok=True)
for p in sorted(SRC.iterdir()):
    img = cv2.imread(str(p))
    if img is None:
        print(f"Error reading {p.name}")
        continue
    h, w = img.shape[:2]
    scale = MAX_SIDE / max(h, w)
    if scale < 1:
        img = cv2.resize(img, (round(w * scale), round(h * scale)),
                         interpolation=cv2.INTER_AREA)
    out = DST / (p.stem + ".png")
    cv2.imwrite(str(out), img)
    print(f"{p.name} -> {out}  {img.shape[1]}x{img.shape[0]}")