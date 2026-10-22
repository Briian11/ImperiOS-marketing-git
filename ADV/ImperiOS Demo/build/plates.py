"""Prepara las imágenes de estado para la composición: recorta cada captura @2x a la zona útil (alto máx. 2200 px CSS)
y la guarda como JPEG 4:4:4 de alta calidad. Fuente: ../ImperiOS Ad/capture/out/states/*.png (fuera de git)."""
import json
import sys
from pathlib import Path
from PIL import Image

# Proyecto: este (por defecto) u otro que reutilice el pipeline, p. ej. «ImperiOS Demo Corto»
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
SRC = ROOT.parent / "ImperiOS Ad" / "capture" / "out" / "states"
DST = ROOT / "hyperframes" / "assets" / "states"
MAXH = 2200
DST.mkdir(parents=True, exist_ok=True)
for p in sorted(SRC.glob("*.png")):
    meta = json.loads(p.with_suffix(".json").read_text())
    im = Image.open(p).convert("RGB")
    h = min(meta["pageH"], MAXH) * 2
    im = im.crop((0, 0, 3840, min(h, im.height)))
    im.save(DST / f"{p.stem}.jpg", quality=93, subsampling=0, optimize=True)
    print(f"{p.stem}: {im.size[0]}×{im.size[1]}")
