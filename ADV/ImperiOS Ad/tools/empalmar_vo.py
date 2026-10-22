"""Empalma tomas de voz que ya tienen tiempos de palabra (Scribe) y une también sus tiempos.

Uso: python3 tools/empalmar_vo.py <salida.wav> <salida.words.json> <audio1> <words1.json> <hasta1> <pausa1> [<audio2> <words2.json> <hasta2> <pausa2> ...]
- <hasta>: índice de la última palabra que se queda de esa toma (-1 = todas). Si se corta antes del final,
  el corte cae en el punto de menos energía entre esa palabra y la siguiente (para no comerse ni añadir sílabas).
- Cada trozo se iguala en sonoridad a la mediana (como tools/ensamblar_vo.py) y lleva la pausa indicada (s) detrás.
Sirve para cambiar una frase de una locución sin regenerarla entera.
"""
import json
import sys

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from ensamblar_vo import SR, load, loudness  # noqa: E402


def cut_point(x, t0, t1):
    """Instante (s) de menos energía (ventanas de 10 ms) entre t0 y t1."""
    h = int(.01 * SR)
    i0, i1 = int(t0 * SR), min(int(t1 * SR), len(x) - h)
    if i1 <= i0:
        return t0
    rms = [np.sqrt(np.mean(x[i:i + h] ** 2)) for i in range(i0, i1, h)]
    return (i0 + int(np.argmin(rms)) * h + h / 2) / SR


def main():
    out_wav, out_json, *rest = sys.argv[1:]
    pieces = [rest[i:i + 4] for i in range(0, len(rest), 4)]
    segs, words, t = [], [], 0.0
    for path, wpath, upto, pause in pieces:
        x, W = load(path), json.load(open(wpath))
        upto = int(upto) % len(W)
        a = max(0.0, W[0][1] - .05)
        if upto < len(W) - 1:
            b = cut_point(x, W[upto][2] - .08, W[upto + 1][1] + .06)
        else:
            b = min(len(x) / SR, W[upto][2] + .25)
        seg = x[int(a * SR):int(b * SR)].copy()
        f = int(.012 * SR)
        seg[:f] *= np.linspace(0, 1, f)
        seg[-f:] *= np.linspace(1, 0, f)
        words += [[w, round(t + s - a, 3), round(t + min(e, b) - a, 3)] for w, s, e in W[:upto + 1]]
        segs.append((seg, float(pause)))
        t += len(seg) / SR + float(pause)
    lu = [loudness(s) for s, _ in segs]
    ref = float(np.median(lu))
    print("sonoridad por trozo (LUFS):", [round(v, 1) for v in lu], "-> todos a", round(ref, 1))
    y = np.concatenate([np.concatenate([s * np.float32(10 ** ((ref - l) / 20)), np.zeros(int(p * SR), np.float32)])
                        for (s, p), l in zip(segs, lu)])
    import subprocess
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-c:a", "pcm_s16le", out_wav], input=y.astype(np.float32).tobytes(), check=True)
    json.dump(words, open(out_json, "w"), ensure_ascii=False)
    print(f"{out_wav}: {len(y) / SR:.2f} s, {len(words)} palabras")


if __name__ == "__main__":
    main()
