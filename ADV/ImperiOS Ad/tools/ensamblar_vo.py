"""Une tomas de voz generadas por frases y estima el tiempo de cada palabra sin transcribir.

Uso: python3 tools/ensamblar_vo.py <salida.wav> <salida.words.json> <audio1> "<texto1>" <pausa1> [<audio2> "<texto2>" <pausa2> ...]
- Cada audio se recorta a su voz (silencio inicial y final fuera) y se une con la pausa indicada (s) detrás.
- Tiempos de palabra: el tramo con voz de cada toma se reparte entre sus palabras según sus sílabas,
  saltando los silencios internos. Medido contra Scribe en frases sueltas: error medio 0,14 s (p90 0,35 s);
  por eso conviene generar la voz por frases. Suficiente para el texto animado.
Se usa cuando la transcripción (Scribe) no está disponible; mismo formato que los *.words.json de Scribe.
"""
import json
import re
import subprocess
import sys

import numpy as np

SR = 44100


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def voiced(x, thr_db=-38, hop=0.01):
    """Máscara de voz por ventanas de 10 ms (umbral relativo al pico)."""
    h = int(hop * SR)
    n = len(x) // h
    rms = np.sqrt(np.mean(x[:n * h].reshape(n, h) ** 2, axis=1))
    on = rms > np.max(rms) * 10 ** (thr_db / 20)
    # rellena huecos < 60 ms (oclusivas) para no partir palabras
    gap = 0
    for i in range(n):
        if on[i]:
            if 0 < gap < 6:
                on[i - gap:i] = True
            gap = 0
        else:
            gap += 1
    return on, hop


def syllables(word):
    w = word.lower().strip("¿?¡!.,:;«»\"")
    if w in ("whatsapp",):
        return 2
    if w in ("leads",):
        return 1
    groups = re.findall(r"[aeiouáéíóúü]+", w)
    n = 0
    for g in groups:   # hiato de vocales fuertes o con tilde = 2 sílabas
        n += 1 + len(re.findall(r"(?<=[aeoáéó])[aeoáéó]|[íú](?=[aeo])|(?<=[aeo])[íú]", g))
    return max(1, n)


def main():
    out_wav, out_json, *rest = sys.argv[1:]
    pieces = [(rest[i], rest[i + 1], float(rest[i + 2])) for i in range(0, len(rest), 3)]
    audio, words, t = [], [], 0.0
    for path, text, pause in pieces:
        x = load(path)
        on, hop = voiced(x)
        idx = np.flatnonzero(on)
        a, b = idx[0], idx[-1] + 1
        seg = x[int(a * hop * SR):int(b * hop * SR)]
        fade = int(0.008 * SR)
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
        on = on[a:b]
        frames = np.flatnonzero(on)                     # ventanas con voz, en orden
        toks = text.split()
        syl = np.array([syllables(w) for w in toks], float)
        edges = np.concatenate([[0], np.cumsum(syl)]) / syl.sum() * len(frames)
        for k, w in enumerate(toks):
            i0 = frames[min(int(edges[k]), len(frames) - 1)]
            i1 = frames[min(int(np.ceil(edges[k + 1])) - 1, len(frames) - 1)] + 1
            words.append([w, round(t + i0 * hop, 3), round(t + i1 * hop, 3)])
        audio += [seg, np.zeros(int(pause * SR), np.float32)]
        t += len(seg) / SR + pause
    y = np.concatenate(audio)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-c:a", "pcm_s16le", out_wav], input=y.tobytes(), check=True)
    json.dump(words, open(out_json, "w"), ensure_ascii=False)
    print(f"{out_wav}: {len(y) / SR:.2f} s, {len(words)} palabras")


if __name__ == "__main__":
    main()
