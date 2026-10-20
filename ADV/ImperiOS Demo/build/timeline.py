"""Timeline del vídeo demo: reparte la locución en escenas (una por párrafo del guion), mete aire entre ellas
y resuelve cada acción visual (cursor, clic, cambio de estado, cámara, foco) a un tiempo absoluto anclado a una palabra.

Uso: python3 build/timeline.py          → hyperframes/data.json + hyperframes/assets/audio/vo.wav
Entradas: vo/demo-toma-1.mp3, vo/demo-toma-1.words.json, ../ImperiOS Ad/capture/out/states/*.json
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATES = ROOT.parent / "ImperiOS Ad" / "capture" / "out" / "states"
HF = ROOT / "hyperframes"
VO = ROOT / "vo" / "demo-toma-1.mp3"
WORDS = json.loads((ROOT / "vo" / "demo-toma-1.words.json").read_text())

INTRO = 1.8      # la voz empieza tras la entrada del logo
GAP = 1.2        # aire entre escenas (transición + primer gesto)
TAIL = 3.2       # cola con el logo final

# Escenas: primera palabra del párrafo (orden del guion)
SCENES = [
    ("intro", "Esto", "Intro"), ("dashboard", "Nada", "Dashboard"), ("contactos", "Cada", "Contactos"),
    ("chat", "Desde", "Chat"), ("cliente", "Cuando", "Clientes"), ("propiedades", "En", "Propiedades"),
    ("ia", "Aquí", "Coincidencias IA"), ("agenda", "Las", "Agenda"), ("marketing", "Si", "Marketing"),
    ("rendimiento", "Cada", "Métricas"), ("direccion", "Y", "Dirección"), ("cierre", "Imperios.", ""),
]


def split_paragraphs():
    """Índices de inicio de cada párrafo, buscando la primera palabra de cada escena en orden."""
    idx, i = [], 0
    for _, first, _ in SCENES:
        while WORDS[i][0] != first:
            i += 1
        idx.append(i)
        i += 1
    return idx + [len(WORDS)]


def build():
    starts = split_paragraphs()
    scenes, words, t = [], [], INTRO
    for k, (sid, _, label) in enumerate(SCENES):
        a, b = starts[k], starts[k + 1]
        src0, src1 = WORDS[a][1], WORDS[b - 1][2]
        if k:
            t += GAP
        off = t - src0
        sw = [[w, round(s + off, 3), round(e + off, 3)] for w, s, e in WORDS[a:b]]
        scenes.append({"id": sid, "label": label, "n": k, "src": [src0, src1], "vo": [round(t, 3), round(t + src1 - src0, 3)], "words": sw})
        words += sw
        t += src1 - src0
    dur = round(t + TAIL, 2)
    # Inicio/fin visual de cada escena: arranca 0,5 s antes de su primera palabra
    for k, s in enumerate(scenes):
        s["start"] = 0.0 if k == 0 else round(s["vo"][0] - 0.5, 3)
        s["end"] = round(scenes[k + 1]["vo"][0] - 0.5, 3) if k + 1 < len(scenes) else dur
    return scenes, words, dur


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


def make_vo(scenes, dur):
    out = HF / "assets" / "audio"
    out.mkdir(parents=True, exist_ok=True)
    parts, labels = [], []
    for k, s in enumerate(scenes):
        a, b = s["src"][0] - 0.06, s["src"][1] + 0.25
        delay = int((s["vo"][0] - 0.06) * 1000)
        parts.append(f"[0]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b - a - 0.08:.3f}:d=0.08,adelay={delay}|{delay}[s{k}]")
        labels.append(f"[s{k}]")
    fc = ";".join(parts) + f";{''.join(labels)}amix=inputs={len(labels)}:normalize=0,apad=whole_dur={dur}[o]"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(VO), "-filter_complex", fc,
                    "-map", "[o]", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s24le", str(out / "vo.wav")], check=True)


if __name__ == "__main__":
    from spec import actions  # noqa: E402  (acciones visuales por escena)
    scenes, words, dur = build()
    states = {p.stem: json.loads(p.read_text()) for p in sorted(STATES.glob("*.json"))}
    data = {"duration": dur, "scenes": scenes, "words": words, "states": {k: {"pageH": v["pageH"], "boxes": v["boxes"]} for k, v in states.items()}}
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
    make_vo(scenes, dur)
    print(f"duración {dur:.2f} s · {len(words)} palabras · {len(data['actions'])} acciones")
    for s in scenes:
        print(f"  {s['n']:>2} {s['id']:<12} {s['start']:7.2f} → {s['end']:7.2f}   voz {s['vo'][0]:7.2f}–{s['vo'][1]:7.2f}")
