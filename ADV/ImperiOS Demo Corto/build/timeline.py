"""Timeline del vídeo demo corto (~49 s): una sola toma de voz, partida en escenas (una por párrafo del guion) en el
silencio real entre párrafos, con poco aire entre escenas, y cada acción visual anclada a una palabra.

Uso: python3 build/timeline.py          → hyperframes/data.json + data.js + hyperframes/assets/audio/vo.wav
Entradas: vo/corto-toma-1.mp3 + .words.json (Scribe), clips de párrafos reescritos (vo/v2-*.mp3 + .words.json),
../ImperiOS Ad/capture/out/states/*.json
"""
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[1]
STATES = ROOT.parent / "ImperiOS Ad" / "capture" / "out" / "states"
HF = ROOT / "hyperframes"
VODIR = ROOT / "vo"
TAKE = "corto-toma-1"
SR = 48000

INTRO = 1.3      # la voz empieza con el logo ya en pantalla
GAP = 0.5        # aire entre escenas (la transición cabe en él)
TAIL = 2.2       # cola con el logo final

# Escenas: (id, primera palabra del párrafo en la toma, etiqueta, aire antes de la escena, clip propio o None)
# v2: el párrafo de IA se regrabó más largo (entrar en una coincidencia) y tiene su propio clip.
SCENES = [
    ("intro", "Esto", "Intro", 0, None), ("contactos", "Los", "Contactos", GAP, None), ("chat", "Sus", "Chat", GAP, None),
    ("ia", "La", "Coincidencias IA", GAP, "v2-ia"), ("marketing", "En", "Marketing", GAP, None),
    ("metricas", "En", "Métricas", GAP, None), ("ademas", "Y", "Y además", 0.6, None), ("cierre", "Imperios.", "", 0.8, None),
]


def decode(name):
    """Audio mono float a 48 kHz."""
    raw = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(VODIR / f"{name}.mp3"), "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def quietest(x, t0, t1):
    """Instante de menor energía (ventana de 20 ms) entre t0 y t1: el silencio real entre dos frases."""
    a, b = int(max(0, t0) * SR), int(min(len(x) / SR, t1) * SR)
    if b - a < int(0.03 * SR):
        return (t0 + t1) / 2
    win = int(0.02 * SR)
    e = np.convolve(x[a:b] ** 2, np.ones(win) / win, mode="same")
    return (a + int(np.argmin(e))) / SR


def sources():
    """Por escena: (audio, inicio, fin del tramo en ese audio, palabras con tiempos de ese audio)."""
    take, words = decode(TAKE), json.loads((VODIR / f"{TAKE}.words.json").read_text())
    idx, i = [], 0
    for _, first, _, _, _ in SCENES:
        while words[i][0] != first:
            i += 1
        idx.append(i)
        i += 1
    idx.append(len(words))
    cuts = [0.0]
    for k in range(1, len(SCENES)):
        cuts.append(quietest(take, words[idx[k] - 1][2] - 0.15, words[idx[k]][1] + 0.03))
    cuts.append(len(take) / SR)
    out = []
    for k, (*_, clip) in enumerate(SCENES):
        if clip:
            x, w = decode(clip), json.loads((VODIR / f"{clip}.words.json").read_text())
            out.append((x, max(0.0, w[0][1] - 0.3), min(len(x) / SR, w[-1][2] + 0.4), w))
        else:
            out.append((take, cuts[k], cuts[k + 1], words[idx[k]:idx[k + 1]]))
    return out


def build():
    src = sources()
    scenes, words, t = [], [], INTRO
    for k, ((sid, _, label, gap, clip), (_, c0, c1, w)) in enumerate(zip(SCENES, src)):
        t += gap
        off = t - w[0][1]                    # la primera palabra cae en t
        sw = [[x, round(a + off, 3), round(b + off, 3)] for x, a, b in w]
        scenes.append({"id": sid, "label": label, "n": k, "clip": clip or TAKE, "cut": [round(c0, 3), round(c1, 3)], "off": round(off, 3),
                       "vo": [sw[0][1], sw[-1][2]], "words": sw})
        words += sw
        t = sw[-1][2]
    dur = round(t + TAIL, 2)
    # Inicio/fin visual de cada escena: arranca 0,4 s antes de su primera palabra
    for k, s in enumerate(scenes):
        s["start"] = 0.0 if k == 0 else round(s["vo"][0] - 0.4, 3)
        s["end"] = round(scenes[k + 1]["vo"][0] - 0.4, 3) if k + 1 < len(scenes) else dur
    return scenes, words, dur, src


def _norm(w):
    return w.strip(".,:;¿?¡!")


def at(scene, word, occ=0, off=0.0):
    """Tiempo absoluto de la palabra exacta `word` (sin puntuación) dentro de la escena, ocurrencia `occ`.
    Si `word` empieza por mayúscula se distingue mayúsculas; si no, no."""
    q = _norm(word)
    same = (lambda w: _norm(w) == q) if q[:1].isupper() else (lambda w: _norm(w).lower() == q.lower())
    hits = [w for w in scene["words"] if same(w[0])]
    if len(hits) <= occ:
        raise KeyError(f"«{word}» (#{occ}) no está en la escena {scene['id']}")
    return round(hits[occ][1] + off, 3)


def make_vo(scenes, dur, src):
    """Pista de voz: cada párrafo en su sitio, cortado en silencio real y con fundidos de 8 ms."""
    out = HF / "assets" / "audio"
    out.mkdir(parents=True, exist_ok=True)
    y = np.zeros(int((dur + 1) * SR), dtype=np.float32)
    fade = int(0.008 * SR)
    for s, (x, c0, c1, _) in zip(scenes, src):
        seg = x[int(c0 * SR):int(c1 * SR)].copy()
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
        p = int(round((c0 + s["off"]) * SR))
        y[p:p + len(seg)] += seg[: len(y) - p]
    y = y[: int(dur * SR)]
    wavfile.write(out / "vo.wav", SR, np.stack([y, y], 1))


if __name__ == "__main__":
    from spec import actions  # noqa: E402  (acciones visuales por escena)
    scenes, words, dur, src = build()
    states = {p.stem: json.loads(p.read_text()) for p in sorted(STATES.glob("*.json"))}
    data = {"duration": dur, "scenes": scenes, "words": words,
            "states": {k: {"pageH": v["pageH"], "boxes": v["boxes"] or {}} for k, v in states.items()}}
    data["actions"] = actions(scenes, states, at)
    # Color de fondo bajo la tarjeta arrastrada (para "vaciar" su hueco durante el arrastre)
    from PIL import Image
    for a in data["actions"]:
        if a["t"] == "drag":
            im = Image.open(STATES / f"{a['img']}.png").convert("RGB")
            x, y, w, h = a["from"]
            a["bg"] = "#%02x%02x%02x" % im.getpixel((int((x + w / 2) * 2), int((y + h + 5) * 2)))
    (HF / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    (HF / "data.js").write_text("window.DEMO = " + json.dumps(data, ensure_ascii=False) + ";\n")
    make_vo(scenes, dur, src)
    print(f"duración {dur:.2f} s · {len(words)} palabras · {len(data['actions'])} acciones")
    for s in scenes:
        print(f"  {s['n']:>2} {s['id']:<10} {s['start']:6.2f} → {s['end']:6.2f}   voz {s['vo'][0]:6.2f}–{s['vo'][1]:6.2f}")
