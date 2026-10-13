"""Sintetiza la biblioteca de SFX original del spec ad de ImperiOS.

Uso: python3 tools/sfx_synth.py <carpeta_salida>
Genera WAV estéreo 48 kHz float32 (pico -3 dBFS), un índice y una escucha previa.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
rng = np.random.default_rng(6)


def t(dur):
    return np.arange(int(dur * SR)) / SR


def env_ad(n, attack, decay_pow=1.0):
    a = max(1, int(attack * SR))
    e = np.ones(n)
    e[:a] = np.linspace(0, 1, a)
    tail = np.linspace(1, 0, n - a) ** decay_pow
    e[a:] = tail
    return e


def bandsweep(x, f0, f1, q=1.2, steps=48):
    """Filtro paso banda que barre de f0 a f1 por bloques (cross-fade)."""
    out = np.zeros_like(x)
    n = len(x)
    edges = np.linspace(0, n, steps + 1).astype(int)
    freqs = np.geomspace(f0, f1, steps)
    win = 512
    for i, f in enumerate(freqs):
        lo, hi = f / (1 + 1 / q), min(f * (1 + 1 / q), SR / 2 - 100)
        sos = butter(2, [max(lo, 20), hi], btype="band", fs=SR, output="sos")
        s, e = max(0, edges[i] - win), min(n, edges[i + 1] + win)
        seg = sosfilt(sos, x[s:e])
        w = np.ones(e - s)
        if edges[i] - s > 0:
            w[: edges[i] - s] = np.linspace(0, 1, edges[i] - s)
        if e - edges[i + 1] > 0:
            w[-(e - edges[i + 1]):] = np.linspace(1, 0, e - edges[i + 1])
        out[s:e] += seg * w
    return out


def hp(x, f):
    return sosfilt(butter(2, f, btype="high", fs=SR, output="sos"), x)


def lp(x, f):
    return sosfilt(butter(2, f, btype="low", fs=SR, output="sos"), x)


def reverb(x, size=0.6, mix=0.25):
    n = int(size * SR)
    ir = rng.standard_normal(n) * np.exp(-np.linspace(0, 7, n))
    ir = lp(ir, 7000)
    wet = np.concatenate([fftconvolve(x, ir), [0.0]])[: len(x) + n]
    dry = np.concatenate([x, np.zeros(n)])
    wet /= np.max(np.abs(wet)) + 1e-9
    return dry * (1 - mix) + wet * mix * np.max(np.abs(x))


def stereo(x, pan=0.0, width=0.0):
    """pan -1..1; width añade un lado (side) decorrelado, compatible con mono."""
    l, r = x * np.sqrt((1 - pan) / 2) * 1.414, x * np.sqrt((1 + pan) / 2) * 1.414
    return widen(np.stack([l, r], axis=1), width)


def widen(st, amount):
    """Mid/side: side = versión retardada y filtrada del mid. El balance L/R se mantiene."""
    if not amount:
        return st
    d = int(0.013 * SR)
    mid = st.mean(axis=1)
    side = hp(np.concatenate([np.zeros(d), mid[:-d]]), 700) * 0.35 * amount
    return np.stack([st[:, 0] + side, st[:, 1] - side], axis=1)


def norm(x, peak_db=-3.0):
    fade = min(len(x) // 4, int(0.01 * SR))
    x = x.copy()
    x[-fade:] *= np.linspace(1, 0, fade)[:, None] if x.ndim == 2 else np.linspace(1, 0, fade)
    return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (peak_db / 20)


# ---------- generadores ----------

def whoosh(dur, f0, f1, shape=1.6, width=0.6, pan_sweep=0.0):
    n = int(dur * SR)
    x = bandsweep(rng.standard_normal(n), f0, f1, q=1.4)
    pos = np.linspace(0, 1, n)
    e = np.sin(np.pi * pos ** 0.7) ** shape
    x *= e
    l = x * (1 - pan_sweep * (pos - 0.5))
    r = x * (1 + pan_sweep * (pos - 0.5))
    return widen(np.stack([l, r], axis=1), width)


def ui_thud(f=95, dur=0.35):
    tt = t(dur)
    pitch = f * (1 + 1.6 * np.exp(-tt * 40))
    body = np.sin(2 * np.pi * np.cumsum(pitch) / SR) * np.exp(-tt * 14)
    click = hp(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 300) * 0.35
    return stereo(reverb(body + click, 0.35, 0.12), width=0.3)


def metal_hit(base=410, dur=1.4):
    tt = t(dur)
    ratios = [1, 2.76, 5.40, 8.93, 13.34]
    x = sum(np.sin(2 * np.pi * base * r * tt + rng.random() * 6) * np.exp(-tt * (3 + i * 2.5)) / (i + 1)
            for i, r in enumerate(ratios))
    x += hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 120) * 0.5
    return stereo(reverb(x, 0.9, 0.3), width=0.5)


def tick(f=3200, dur=0.06):
    tt = t(dur)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 180) + hp(rng.standard_normal(len(tt)), 5000) * np.exp(-tt * 400) * 0.4
    return stereo(x)


def mech_click(f=1800, dur=0.18):
    tt = t(dur)
    a = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 220)
    b = np.zeros_like(tt)
    k = int(0.022 * SR)
    b[k:] = np.sin(2 * np.pi * f * 1.5 * tt[:-k]) * np.exp(-tt[:-k] * 260) * 0.7
    noise = hp(rng.standard_normal(len(tt)), 1500) * np.exp(-tt * 300) * 0.5
    body = np.sin(2 * np.pi * 160 * tt) * np.exp(-tt * 60) * 0.5
    return stereo(a + b + noise + body)


def pop(f=620, dur=0.16):
    tt = t(dur)
    pitch = f * (1 + 0.9 * np.exp(-tt * 70))
    x = np.sin(2 * np.pi * np.cumsum(pitch) / SR) * np.exp(-tt * 38)
    return stereo(x)


def riser(dur=1.2):
    tt = t(dur)
    pos = tt / dur
    noise = bandsweep(rng.standard_normal(len(tt)), 400, 9000, q=2.0) * pos ** 2
    tone = sum(np.sin(2 * np.pi * np.cumsum(220 * h * 2 ** (2 * pos)) / SR) / h for h in (1, 2, 3)) * pos ** 3 * 0.25
    return stereo(noise + tone, width=0.7)


def shimmer(dur=1.6):
    tt = t(dur)
    notes = [1174.66, 1479.98, 1760.0, 2349.32]  # Re6 Fa#6 La6 Re7
    x = sum(np.sin(2 * np.pi * f * tt + i) * (1 + 0.5 * np.sin(2 * np.pi * (7 + i) * tt)) for i, f in enumerate(notes))
    x *= env_ad(len(tt), 0.25, 2.0)
    return stereo(reverb(x, 1.2, 0.45), width=0.8)


def granular_ticks(dur=0.9, n=26):
    out = np.zeros(int(dur * SR))
    for i in range(n):
        p = int((i / n) ** 1.3 * (len(out) - 3000))
        g = tick(2400 + i * 90, 0.04)[:, 0] * (0.4 + 0.6 * i / n)
        out[p:p + len(g)] += g
    return stereo(out, width=0.5)


def glitch(dur=0.35):
    n = int(dur * SR)
    x = np.zeros(n)
    pos = 0
    while pos < n:
        seg = rng.integers(300, 2200)
        f = rng.choice([180, 420, 880, 1600, 3200])
        tt = np.arange(min(seg, n - pos)) / SR
        sq = np.sign(np.sin(2 * np.pi * f * tt)) * rng.uniform(0.3, 1)
        x[pos:pos + len(tt)] = np.round(sq * 6) / 6 if rng.random() > 0.3 else 0
        pos += seg
    return stereo(lp(x, 9000) * env_ad(n, 0.002, 0.6), width=0.6)


def sub_drop(dur=1.3):
    tt = t(dur)
    pitch = 110 * np.exp(-tt * 2.2) + 32
    x = np.sin(2 * np.pi * np.cumsum(pitch) / SR) * env_ad(len(tt), 0.005, 1.4)
    return stereo(np.tanh(x * 1.4))


def low_whoosh(dur=0.9):
    w = whoosh(dur, 90, 900, shape=1.2)
    return w + sub_drop(dur)[: len(w)] * 0.5


def suck(dur=0.6):
    return whoosh(dur, 6000, 300, shape=1.0)[::-1].copy()


def logo_sting(dur=3.2):
    tt = t(dur)
    chord = [146.83, 220.0, 293.66, 369.99, 440.0, 587.33]  # Re mayor abierto
    bell = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * (0.9 + i * 0.25)) * (0.9 ** i) +
               0.3 * np.sin(2 * np.pi * f * 2.01 * tt) * np.exp(-tt * 3) for i, f in enumerate(chord))
    x = reverb(bell * env_ad(len(tt), 0.004, 1.0), 2.0, 0.4)
    sd = sub_drop(1.3)[:, 0]
    x[: len(sd)] += sd * 0.6
    sh = shimmer(1.6)[:, 0]
    x[: len(sh)] += sh * 0.25
    return stereo(x, width=0.7)


LIBRARY = {
    # categoria_nombre: (generador, uso en el brief)
    "whoosh_short_01": (lambda: whoosh(0.28, 600, 5000, pan_sweep=0.8), "entrada de palabra"),
    "whoosh_short_02": (lambda: whoosh(0.34, 400, 4200, pan_sweep=-0.8), "entrada de palabra"),
    "whoosh_short_03": (lambda: whoosh(0.30, 900, 7000, shape=2.2), "entrada de palabra"),
    "whoosh_short_04": (lambda: whoosh(0.42, 300, 3500, pan_sweep=0.5), "entrada de título"),
    "whoosh_long_01": (lambda: whoosh(0.9, 250, 6000, shape=1.3, pan_sweep=1.0), "edge-slingshot / funnel"),
    "whoosh_long_02": (lambda: whoosh(1.1, 5000, 350, shape=1.3, pan_sweep=-1.0), "funnel (salida)"),
    "whoosh_low_wipe": (lambda: low_whoosh(0.9), "wipe a negro"),
    "suck_reverse": (lambda: suck(0.6), "magnetic funnel"),
    "hit_soft_01": (lambda: ui_thud(95), "aterrizaje de chip/tarjeta"),
    "hit_soft_02": (lambda: ui_thud(120, 0.3), "aterrizaje de chip/tarjeta"),
    "hit_soft_03": (lambda: ui_thud(75, 0.45), "aterrizaje de panel"),
    "hit_metal_01": (lambda: metal_hit(410), "bezier snap (match)"),
    "hit_metal_02": (lambda: metal_hit(530, 1.1), "reactivar"),
    "click_ui_01": (lambda: tick(3200), "UI"),
    "click_ui_02": (lambda: tick(2600), "UI"),
    "click_ui_03": (lambda: tick(4100), "UI"),
    "click_mech_dial_1": (lambda: mech_click(1500), "dial Zona"),
    "click_mech_dial_2": (lambda: mech_click(1800), "dial Tipo"),
    "click_mech_dial_3": (lambda: mech_click(2150), "dial Presupuesto"),
    "pop_dock_01": (lambda: pop(520), "dock & lock izq."),
    "pop_dock_02": (lambda: pop(620), "dock & lock dcha."),
    "pop_dock_03": (lambda: pop(740), "dock & lock centro"),
    "riser_grid": (lambda: riser(1.1), "grid ignition"),
    "shimmer_glow": (lambda: shimmer(1.6), "grid ignition / wake pulse"),
    "ticks_granular_curve": (lambda: granular_ticks(0.9), "curve draw"),
    "ticks_granular_calendar": (lambda: granular_ticks(0.7, 18), "calendar cascade"),
    "glitch_wake": (lambda: glitch(0.35), "wake pulse"),
    "sub_drop": (lambda: sub_drop(1.3), "dot-iris"),
    "logo_sting": (lambda: logo_sting(3.2), "logo"),
}


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows, preview = [], []
    gap = np.zeros((int(0.45 * SR), 2))
    for name, (gen, use) in LIBRARY.items():
        x = norm(gen()).astype(np.float32)
        wavfile.write(out / f"{name}.wav", SR, x)
        rows.append(f"| `{name}.wav` | {len(x) / SR:.2f} s | {use} |")
        preview += [x, gap]
    wavfile.write(out / "_preview_all.wav", SR, np.concatenate(preview).astype(np.float32))
    (out / "INDEX.md").write_text(
        "# SFX originales sintetizados en código\n\n"
        "Generados con `tools/sfx_synth.py` (seed 6). WAV estéreo 48 kHz float32, pico −3 dBFS. "
        "Obra original, sin muestras de terceros.\n\n"
        "| Archivo | Duración | Uso |\n|---|---|---|\n" + "\n".join(rows) + "\n"
    )
    print(f"{len(rows)} SFX -> {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "assets_in/sfx")
