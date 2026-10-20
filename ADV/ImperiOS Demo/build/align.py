"""Tiempos por palabra estimados sin transcripción (plan B si Scribe no está disponible).

Detecta los tramos con voz del clip (pausas ≥ 0,12 s a −38 dB), asigna a cada tramo las frases del texto en orden
(cortando por la puntuación) y reparte la duración de cada tramo entre sus palabras en proporción a sus sílabas.
Uso: python3 build/align.py vo/v5-contactos.mp3 vo/VO_DEMO_v5_cambios.txt contactos  → vo/v5-contactos.words.json
"""
import json
import re
import subprocess
import sys
from pathlib import Path


def syllables(w):
    return max(1, len(re.findall(r"[aeiouáéíóúü]+", w.lower())))


def speech_spans(mp3):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp3, "-af", "silencedetect=n=-38dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3],
                               capture_output=True, text=True).stdout)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    # silencio inicial y final cortos (por debajo de 0,12 s) con un umbral más fino
    fine = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp3, "-af", "silencedetect=n=-42dB:d=0.02", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    fs = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", fine)]
    fe = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", fine)]
    lead = fe[0] if fs and fs[0] < 0.01 and fe else 0.0
    tail = fs[-1] if fs and len(fs) > len(fe) else dur
    spans, t = [], lead
    for s, e in zip(starts, ends + [dur]):
        if s <= lead:
            t = max(t, e)
            continue
        if s - t > 0.08:
            spans.append([t, s])
        t = e
    if tail - t > 0.08:
        spans.append([t, tail])
    elif spans and spans[-1][1] > tail:
        spans[-1][1] = tail
    return spans


def align(mp3, text):
    words = text.split()
    spans = speech_spans(mp3)
    # grupos de palabras separados por puntuación (candidatos a pausa)
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r"[.,:;?!]$", w):
            groups.append(cur); cur = []
    if cur:
        groups.append(cur)
    # emparejar grupos con tramos: se fusionan grupos hasta igualar el número de tramos
    while len(groups) > len(spans):
        k = min(range(len(groups) - 1), key=lambda i: len(groups[i]) + len(groups[i + 1]))
        groups[k:k + 2] = [groups[k] + groups[k + 1]]
    while len(spans) > len(groups):
        k = min(range(len(spans) - 1), key=lambda i: spans[i + 1][0] - spans[i][1])
        spans[k:k + 2] = [[spans[k][0], spans[k + 1][1]]]
    out = []
    for g, (a, b) in zip(groups, spans):
        syl = [syllables(w) for w in g]
        tot, t = sum(syl), a
        for w, s in zip(g, syl):
            d = (b - a) * s / tot
            out.append([w, round(t, 3), round(t + d, 3)])
            t += d
    return out


if __name__ == "__main__":
    mp3, txt, key = sys.argv[1:4]
    text = re.search(rf"\[{key}\]\n(.+)", Path(txt).read_text()).group(1).strip()
    w = align(mp3, text)
    Path(mp3).with_suffix(".words.json").write_text(json.dumps(w, ensure_ascii=False))
    print(f"{len(w)} palabras · {w[0]} … {w[-1]}")
