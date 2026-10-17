"""Música original + colocación de SFX + máster del spec ad de ImperiOS.

Uso: python3 audio_mix.py <out_dir>
Lee timeline.json (mismos tiempos que la imagen) y ../assets_in/sfx/*.wav.
Escribe stems (music.wav, sfx.wav) y mix_premaster.wav. El máster a -14 LUFS / -1 dBTP se hace con ffmpeg loudnorm.
Sin VO todavía: cuando llegue, la música se automatiza ≥15 dB por debajo mientras habla.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, sosfilt_zi

SR = 48000
HERE = Path(__file__).resolve().parent
TL = json.loads((HERE / os.environ.get("TL", "timeline.json")).read_text())
B = TL["beats"]
DUR = TL["duration"]
N = int(DUR * SR)
rng = np.random.default_rng(3)


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lp_var(x, cut_curve, block=512):
    """Paso bajo con corte variable por bloques (estado continuo)."""
    out = np.zeros_like(x)
    zi = None
    for s in range(0, len(x), block):
        c = float(np.clip(cut_curve[min(s, len(cut_curve) - 1)], 60, SR / 2 - 200))
        sos = butter(2, c, fs=SR, output="sos")
        if zi is None:
            zi = sosfilt_zi(sos) * 0
        out[s:s + block], zi = sosfilt(sos, x[s:s + block], zi=zi)
    return out


def adsr(n, a, d, s, r, sus_len):
    e = np.zeros(n)
    A, D, R = int(a * SR), int(d * SR), int(r * SR)
    S = max(0, int(sus_len * SR) - A - D)
    seg = np.concatenate([np.linspace(0, 1, max(A, 1)), np.linspace(1, s, max(D, 1)), np.full(S, s), np.linspace(s, 0, max(R, 1))])
    e[:min(n, len(seg))] = seg[:n]
    return e


def saw(f, n, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((f * t + phase) % 1) - 1


# ---------- armonía ----------
BEAT = 0.6                     # 100 BPM
BAR = 4 * BEAT
V4 = bool(B.get("wt", {}).get("src"))   # campaña v4 (build_timeline_v4.py)
T0 = B.get("s0", B["s1"])      # el primer compás arranca con la captación (v4 larga: con «lo centralizas…»)
# acordes (notas MIDI) por compás; Re mayor / Si menor
CHORDS = [
    ("D", [50, 57, 62, 66, 69]),
    ("Bm", [47, 54, 59, 62, 66]),
    ("G", [43, 50, 55, 59, 62]),
    ("A", [45, 52, 57, 61, 64]),
    ("Bm", [47, 54, 59, 62, 66]),
    ("G", [43, 50, 55, 59, 62]),
    ("Em", [40, 52, 55, 59, 64]),
    ("Asus", [45, 52, 57, 62, 64]),
]
FINAL = [38, 50, 57, 62, 64, 66, 69, 76]   # Re add9 abierto


def chord_idx(b):
    # v4 dura más de 8 compases: repite el ciclo; las versiones anteriores sostienen el último acorde
    return b % len(CHORDS) if V4 else min(b, len(CHORDS) - 1)


def chord_at(t):
    i = int((t - T0) // BAR)
    return CHORDS[chord_idx(max(i, 0))]


def music():
    m = np.zeros((N, 2))
    t = np.arange(N) / SR
    dark = ((t > B["s3"]) & (t < B["s5"])).astype(float)
    dark = np.convolve(dark, np.ones(int(.4 * SR)) / int(.4 * SR), mode="same")
    end_music = B["logo"]

    # PAD: sierras desafinadas, filtro que se oscurece en el tramo oscuro
    pad = np.zeros(N)
    nbars = int(np.ceil((end_music - T0) / BAR))
    for b in range(nbars):
        s0 = T0 + b * BAR
        name, notes = CHORDS[chord_idx(b)]
        dur = min(BAR, end_music - s0) + .6
        i0, n = int(s0 * SR), int(dur * SR)
        if i0 >= N:
            break
        n = min(n, N - i0)
        env = adsr(n, .35, .4, .8, .6, dur - .6)
        for note in notes[1:]:
            for det in (-0.08, 0.0, 0.08):
                pad[i0:i0 + n] += saw(midi(note + det), n, rng.random()) * env * 0.05
    cut = 2400 - 1300 * dark
    cut *= np.clip((t - T0) / 1.5, 0.15, 1)       # abre en la entrada
    pad = lp_var(pad, cut)
    # PLUCK: arpegio en corcheas, con sidechain del kick
    pl = np.zeros(N)
    step = BEAT / 2
    k = 0
    tt = T0
    while tt < end_music - .05:
        _, notes = chord_at(tt)
        pattern = [notes[2], notes[3], notes[4], notes[3], notes[2] + 12, notes[4], notes[3], notes[1] + 12]
        note = pattern[k % len(pattern)]
        i0 = int(tt * SR)
        n = int(.45 * SR)
        n = min(n, N - i0)
        f = midi(note)
        tone = (saw(f, n) * .6 + np.sign(np.sin(2 * np.pi * f * np.arange(n) / SR)) * .4)
        env = np.exp(-np.arange(n) / SR * 9)
        # filtro con envolvente: brillante al ataque
        tone = lp_var(tone, 900 + 4200 * np.exp(-np.arange(n) / SR * 14) * (1 - .5 * dark[i0]), block=256)
        vel = .9 if k % 2 == 0 else .65
        pl[i0:i0 + n] += tone * env * .11 * vel
        k += 1
        tt += step
    pl *= np.clip((t - T0) / 0.3, 0, 1)
    # KICK suave + SUB desde el panel
    kick = np.zeros(N)
    side = np.ones(N)
    groove_on = B["s2"]
    groove_off = B["s6"] + .6
    tt = T0 + BAR  # desde el compás 2
    while tt < groove_off:
        if tt >= groove_on - .01:
            i0 = int(tt * SR)
            n = min(int(.35 * SR), N - i0)
            x = np.arange(n) / SR
            kick[i0:i0 + n] += np.sin(2 * np.pi * np.cumsum(48 + 90 * np.exp(-x * 30)) / SR) * np.exp(-x * 9) * .55
            sc = 1 - .55 * np.exp(-x * 7)
            side[i0:i0 + n] = np.minimum(side[i0:i0 + n], sc)
        tt += BEAT
    sub = np.zeros(N)
    for b in range(nbars):
        s0 = T0 + b * BAR
        if s0 + BAR < groove_on or s0 > groove_off:
            continue
        _, notes = CHORDS[chord_idx(b)]
        i0 = int(max(s0, groove_on) * SR)
        n = min(int(min(BAR, groove_off - max(s0, groove_on)) * SR), N - i0)
        if n <= 0:
            continue
        x = np.arange(n) / SR
        sub[i0:i0 + n] += np.sin(2 * np.pi * midi(notes[0] - 12 if notes[0] > 40 else notes[0]) * x) * adsr(n, .05, .2, .85, .2, n / SR - .2) * .22
    # HATS en el tramo oscuro (más pulso)
    hats = np.zeros(N)
    tt = B["s3"] + BEAT / 2
    while tt < B["s5"]:
        i0 = int(tt * SR)
        n = min(int(.06 * SR), N - i0)
        h = sosfilt(butter(2, 7000, btype="high", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-np.arange(n) / SR * 70)
        hats[i0:i0 + n] += h * .05
        tt += BEAT
    # ACORDE FINAL: campana aditiva que suena bajo el logo
    fin = np.zeros(N)
    i0 = int((B["logo"] + .55) * SR)
    n = N - i0
    x = np.arange(n) / SR
    for j, note in enumerate(FINAL):
        f = midi(note)
        fin[i0:] += (np.sin(2 * np.pi * f * x) * np.exp(-x * (.55 + j * .06)) + .25 * np.sin(2 * np.pi * f * 2.003 * x) * np.exp(-x * 2.2)) * (.11 if note > 45 else .16)
    fin[i0:] *= np.clip(x / .01, 0, 1)

    mono_bus = (pad * side + pl * side * 1.0 + sub * side)
    # estéreo: pluck alterna lados ligeramente, pad abierto
    d = int(.012 * SR)
    pad_r = np.concatenate([np.zeros(d), pad[:-d]])
    m[:, 0] = pad * side * .9 + pl * side * .8 + sub * side + kick + hats * .7 + fin
    m[:, 1] = pad_r * side * .9 + pl * side * 1.0 + sub * side + kick + hats * 1.0 + fin
    # fundido de salida en el último medio segundo
    fade = np.clip((DUR - t) / .5, 0, 1)
    m *= fade[:, None]
    return m


# ---------- SFX ----------
SFX_DIR = HERE.parent / "assets_in" / "sfx"
_cache = {}


def sfx(name):
    if name not in _cache:
        sr, x = wavfile.read(SFX_DIR / f"{name}.wav")
        assert sr == SR
        _cache[name] = x.astype(np.float64)
    return _cache[name]


def hp(x, f):
    return sosfilt(butter(2, f, btype="high", fs=SR, output="sos"), x, axis=0)


def cues():
    s1, s2, s3, s4, s5, s6, lg = (B[k] for k in ("s1", "s2", "s3", "s4", "s5", "s6", "logo"))
    h = B.get("hook", 0.0)
    if V4:
        return cues_v4()
    if h > 0:
        # gancho de campaña: caos de notificaciones que colapsa en el pixel
        hook = [
            (0.00, "pop_dock_01", -12, -.5, 0),
            (0.05, "whoosh_short_02", -15, 0, 300),
            (0.20, "glitch_wake", -17, .3, 0),
            *[(.1 + i * .09, ["click_ui_01", "pop_dock_02", "click_ui_02", "pop_dock_03", "click_ui_03", "pop_dock_01"][i], -17, [-.7, .6, -.1, -.6, .7, .1][i], 0) for i in range(6)],
            (h - 1.1, "riser_grid", -15, 0, 300),
            (h - .6, "suck_reverse", -12, 0, 200),
            (h - .5, "whoosh_long_02", -16, 0, 250),
            (h + .00, "hit_soft_03", -8, 0, 0),
            (h + .00, "shimmer_glow", -16, 0, 600),
            (h + .52, "pop_dock_01", -14, 0, 0),
        ]
    else:
        hook = [
            (0.00, "shimmer_glow", -16, 0, 600),
            (0.30, "whoosh_short_03", -14, 0, 300),
            (0.34, "hit_soft_03", -8, 0, 0),
            (0.52, "pop_dock_01", -14, 0, 0),
        ]
    c = [
        # (tiempo, sfx, ganancia dB, pan -1..1, hpf Hz)
        *hook,
        (s1 + .02, "whoosh_short_03", -16, 0, 300),
        (s1 + .00, "whoosh_short_02", -13, .1, 300),
        (s1 + .10, "whoosh_long_01", -17, -.6, 300),
        (s1 + .20, "whoosh_short_01", -15, .6, 300),
        (s1 + .60, "click_ui_01", -16, 0, 0),
        (s1 + 1.25, "click_ui_02", -16, -.5, 0),
        (s1 + 1.85, "click_ui_03", -16, .5, 0),
        (s1 + .85, "whoosh_short_04", -19, 0, 400),
        (s1 + 1.45, "whoosh_short_02", -19, -.3, 400),
        (s1 + 2.05, "whoosh_short_01", -19, .3, 400),
        (s1 + 1.55, "hit_soft_02", -18, 0, 0),
        (s1 + 2.15, "hit_soft_01", -18, 0, 0),
        (s1 + 2.75, "hit_soft_02", -18, 0, 0),
        # S2 panel
        (s2 - .05, "suck_reverse", -12, 0, 200),
        (s2 + .10, "whoosh_long_02", -15, 0, 250),
        (s2 + .58, "hit_soft_03", -9, 0, 0),
        *[(s2 + .5 + i * .09 + .3, f"click_ui_0{1 + i % 3}", -20, (i - 2) * .15, 0) for i in range(5)],
        (s2 + 1.32, "pop_dock_02", -12, .45, 0),
        (s2 + 1.45, "whoosh_long_01", -15, .7, 300),
        (s2 + 2.05, "hit_soft_01", -12, .4, 0),
        (s2 + 1.80, "ticks_granular_curve", -18, .4, 0),
        (s2 + 2.72, "pop_dock_03", -13, .55, 0),
        # transición a oscuro
        (s3 - .32, "whoosh_low_wipe", -9, 0, 0),
        # S3 match
        (s3 + .30, "pop_dock_01", -12, -.6, 0),
        (s3 + .55, "whoosh_long_02", -17, 0, 300),
        (s3 + .70, "ticks_granular_curve", -20, 0, 0),
        (s3 + .95, "hit_soft_02", -11, 0, 0),
        (s3 + .95, "click_mech_dial_1", -11, -.7, 0),
        (s3 + 1.35, "click_mech_dial_2", -11, -.5, 0),
        (s3 + 1.75, "click_mech_dial_3", -11, -.3, 0),
        (s3 + .95, "whoosh_short_01", -18, 0, 400),
        (s3 + 1.35, "whoosh_short_03", -18, 0, 400),
        (s3 + 1.75, "whoosh_short_02", -18, 0, 400),
        (s3 + 1.85, "whoosh_short_04", -17, 0, 400),
        (s3 + 2.40, "hit_metal_02", -15, .1, 0),
        (s3 + 2.20, "whoosh_short_01", -20, 0, 400),
        # S4 reactivar
        (s4 - .25, "whoosh_short_04", -14, 0, 300),
        (s4 + .05, "glitch_wake", -14, -.5, 0),
        (s4 + .28, "whoosh_short_01", -12, .2, 300),
        (s4 + .60, "click_ui_03", -14, .3, 0),
        (s4 + .50, "whoosh_long_01", -19, 0, 300),
        (s4 + 1.20, "shimmer_glow", -12, 0, 500),
        (s4 + 1.20, "hit_metal_01", -13, 0, 0),
        (s4 + 1.50, "pop_dock_02", -11, .55, 0),
        (s4 + 2.00, "click_mech_dial_2", -10, .55, 0),
        (s4 + 2.03, "hit_soft_02", -11, .5, 0),
        (s4 + .35, "whoosh_short_02", -19, 0, 400),
        # transición a claro
        (s5 - .2, "whoosh_low_wipe", -10, .3, 0),
        # S5 operativa
        (s5 + .20, "whoosh_long_02", -14, 0, 250),
        (s5 + .70, "pop_dock_01", -15, .4, 0),
        (s5 + .80, "pop_dock_02", -15, .5, 0),
        (s5 + .90, "pop_dock_03", -15, .6, 0),
        (s5 + .90, "ticks_granular_calendar", -19, 0, 0),
        *[(s5 + .95 + i * .14 + .3, "hit_soft_01" if i % 2 else "hit_soft_02", -15, (i - 2) * .2, 0) for i in range(5)],
        (s5 + 2.00, "pop_dock_02", -12, -.45, 0),
        (s5 + 2.30, "pop_dock_03", -12, .4, 0),
        (s5 + .30, "whoosh_short_03", -19, 0, 400),
        (s5 + 1.10, "whoosh_short_01", -20, 0, 400),
        # S6 titular
        (s6 - .15, "whoosh_long_01", -15, 0, 300),
        (s6 + .45, "whoosh_short_03", -14, 0, 300),
        (s6 + .72, "hit_soft_03", -10, 0, 0),
        (s6 + .95, "shimmer_glow", -16, 0, 600),
        (s6 + 1.20, "whoosh_short_02", -15, 0, 300),
        # logo
        (lg - .05, "whoosh_short_04", -11, 0, 300),
        (lg + .25, "riser_grid", -18, 0, 300),
        (lg + .55, "sub_drop", -9, 0, 0),
        (lg + .55, "logo_sting", -8, 0, 0),
        (lg + .95, "click_ui_01", -15, 0, 0),
    ]
    if "cta" in B:
        ct = B["cta"]
        c += [
            (ct - .05, "whoosh_short_04", -14, 0, 300),
            (ct + .35, "pop_dock_02", -9, 0, 0),
            (ct + .35, "logo_sting", -15, 0, 0),
            (ct + .40, "shimmer_glow", -15, 0, 600),
            (ct + 1.10, "click_ui_02", -17, 0, 0),
        ]
    return c


def hook_cues(h):
    """Gancho de campaña: caos de notificaciones que colapsa en el pixel."""
    return [
        (0.00, "pop_dock_01", -12, -.5, 0),
        (0.05, "whoosh_short_02", -15, 0, 300),
        (0.20, "glitch_wake", -17, .3, 0),
        *[(.1 + i * .09, ["click_ui_01", "pop_dock_02", "click_ui_02", "pop_dock_03", "click_ui_03", "pop_dock_01"][i], -17, [-.7, .6, -.1, -.6, .7, .1][i], 0) for i in range(6)],
        (h - 1.1, "riser_grid", -15, 0, 300),
        (h - .6, "suck_reverse", -12, 0, 200),
        (h - .5, "whoosh_long_02", -16, 0, 250),
        (h + .00, "hit_soft_03", -8, 0, 0),
        (h + .00, "shimmer_glow", -16, 0, 600),
        (h + .52, "pop_dock_01", -14, 0, 0),
    ]


def cues_v4():
    """Cues de la campaña v4, atadas a las mismas palabras que la imagen (B.wt)."""
    s1, s2, s3, s4, s5, s6, lg, h = (B[k] for k in ("s1", "s2", "s3", "s4", "s5", "s6", "logo", "hook"))
    wt, skip = B["wt"], B.get("skip", [])
    c = hook_cues(h)
    if "s0" in B:
        s0 = B["s0"]
        # latido del pixel (cada 1,2 s) y golpe en «todo»
        c += [(h + .5 + i * 1.2, "hit_soft_01", -19, 0, 0) for i in range(int((s1 - h - .5) / 1.2) + 1)]
        c += [(s0 + wt["kt0"][0] - .05, "whoosh_short_03", -17, 0, 400), (s0 + wt["kt0"][3], "hit_soft_02", -12, 0, 0),
              (s0 + wt["kt0"][3] + .05, "shimmer_glow", -18, 0, 600)]
    # S1: entran las 4 fuentes; cada una suena al nombrarla y su lead vuela al montón
    c += [(s1 + .00, "whoosh_short_02", -13, .1, 300), (s1 + .10, "whoosh_long_01", -17, -.6, 300), (s1 + .20, "whoosh_short_01", -15, .6, 300)]
    pans = [-.4, .5, -.5, .4]
    for i, f in enumerate(wt["src"]):
        c += [(s1 + f, f"click_ui_0{1 + i % 3}", -15, pans[i], 0),
              (s1 + f + .25, ["whoosh_short_04", "whoosh_short_02", "whoosh_short_01", "whoosh_short_03"][i], -19, pans[i] * .6, 400),
              (s1 + f + .95, "hit_soft_02" if i % 2 else "hit_soft_01", -18, 0, 0)]
    c += [(s1 + wt["src"][3] + .5, "shimmer_glow", -17, 0, 600), (s1 + wt["kt1"][6], "pop_dock_03", -17, 0, 0)]
    if "s2" not in skip:
        w2 = wt["kt2"]
        c0 = max(.7, w2[1] - .25)
        c += [(s2 - .05, "suck_reverse", -12, 0, 200), (s2 + .10, "whoosh_long_02", -15, 0, 250), (s2 + .58, "hit_soft_03", -9, 0, 0),
              *[(s2 + .5 + i * .09 + .3, f"click_ui_0{1 + i % 3}", -20, (i - 2) * .15, 0) for i in range(5)],
              (s2 + 1.32, "pop_dock_02", -12, .45, 0),
              (s2 + c0 - .05, "whoosh_long_01", -15, .7, 300), (s2 + c0 + .55, "hit_soft_01", -12, .4, 0),
              (s2 + c0 + .45, "ticks_granular_curve", -18, .4, 0),
              (s2 + w2[1] + .45, "pop_dock_03", -12, .5, 0), (s2 + w2[3] + .1, "pop_dock_01", -12, .5, 0)]
    else:
        c += [(s3 - .55, "suck_reverse", -12, 0, 200)]
    # transición a oscuro + S3 match
    m3 = wt["m3"]
    c += [(s3 - .32, "whoosh_low_wipe", -9, 0, 0),
          (s3 + .30, "pop_dock_01", -12, -.6, 0), (s3 + .55, "whoosh_long_02", -17, 0, 300), (s3 + .70, "ticks_granular_curve", -20, 0, 0),
          (s3 + m3[0], "hit_soft_02", -11, 0, 0),
          (s3 + m3[0], "click_mech_dial_1", -11, -.7, 0), (s3 + m3[1], "click_mech_dial_2", -11, -.5, 0), (s3 + m3[2], "click_mech_dial_3", -11, -.3, 0),
          (s3 + m3[0], "whoosh_short_01", -18, 0, 400), (s3 + m3[1], "whoosh_short_03", -18, 0, 400), (s3 + m3[2], "whoosh_short_02", -18, 0, 400),
          (s3 + m3[2] + .65, "hit_metal_02", -15, .1, 0)]
    # S4: notificación → móvil → las propiedades salen al chat → «enviado»
    e1, e2, e3 = (max(x, m) for x, m in zip(wt.get("s4ev", [1.0, 1.6, 2.2]), [1.0, 1.4, 1.8]))
    c += [(s4 - .25, "whoosh_short_04", -14, 0, 300), (s4 + .05, "glitch_wake", -14, -.5, 0), (s4 + .28, "whoosh_short_01", -12, .2, 300),
          (s4 + .60, "click_ui_03", -14, .3, 0), (s4 + .35, "whoosh_long_01", -17, 0, 300), (s4 + .75, "pop_dock_01", -15, -.3, 0),
          (s4 + e1 - .05, "whoosh_short_02", -14, .3, 300), (s4 + e1 + .2, "pop_dock_02", -11, .35, 0),
          (s4 + e2 - .05, "whoosh_short_03", -15, .3, 300), (s4 + e2 + .2, "pop_dock_03", -12, .35, 0),
          (s4 + e3, "shimmer_glow", -13, .3, 500), (s4 + e3 + .05, "click_mech_dial_2", -12, .4, 0), (s4 + e3 + .05, "hit_soft_02", -12, .3, 0)]
    if "s5" not in skip:
        ea, er = wt["s5ev"]
        c += [(s5 - .2, "whoosh_low_wipe", -10, .3, 0),
              (s5 + .20, "whoosh_long_02", -14, 0, 250),
              (s5 + .70, "pop_dock_01", -15, .4, 0), (s5 + .80, "pop_dock_02", -15, .5, 0), (s5 + .90, "pop_dock_03", -15, .6, 0),
              (s5 + .90, "ticks_granular_calendar", -19, 0, 0),
              *[(s5 + .95 + i * .14 + .3, "hit_soft_01" if i % 2 else "hit_soft_02", -15, (i - 2) * .2, 0) for i in range(5)],
              (s5 + ea, "pop_dock_03", -12, .4, 0), (s5 + er, "pop_dock_02", -12, -.45, 0),
              (s5 + .30, "whoosh_short_03", -19, 0, 400), (s5 + 1.10, "whoosh_short_01", -20, 0, 400)]
    if "s6" not in skip:
        c += [(s6 - .15, "whoosh_long_01", -15, 0, 300), (s6 + wt["kt6"][1] - .25, "whoosh_short_03", -14, 0, 300),
              (s6 + wt["kt6"][1] + .02, "hit_soft_03", -10, 0, 0), (s6 + wt["kt6"][1] + .25, "shimmer_glow", -16, 0, 600),
              (s6 + wt["kt6"][2] - .05, "whoosh_short_02", -15, 0, 300)]
    else:
        c += [(lg - .2, "whoosh_low_wipe", -10, .3, 0)]
    c += [(lg - .05, "whoosh_short_04", -11, 0, 300), (lg + .25, "riser_grid", -18, 0, 300), (lg + .55, "sub_drop", -9, 0, 0),
          (lg + .55, "logo_sting", -8, 0, 0), (lg + .95, "click_ui_01", -15, 0, 0)]
    ct = B["cta"]
    c += [(ct - .05, "whoosh_short_04", -14, 0, 300), (ct + .35, "pop_dock_02", -9, 0, 0), (ct + .35, "logo_sting", -15, 0, 0),
          (ct + .40, "shimmer_glow", -15, 0, 600), (ct + 1.10, "click_ui_02", -17, 0, 0)]
    return c


def place():
    bus = np.zeros((N + SR * 4, 2))
    for t0, name, db, pan, hpf in cues():
        x = sfx(name)
        if hpf:
            x = hp(x, hpf)
        g = 10 ** (db / 20)
        gl, gr = np.sqrt((1 - pan) / 2) * 1.414, np.sqrt((1 + pan) / 2) * 1.414
        i0 = int(max(0, t0) * SR)
        n = min(len(x), len(bus) - i0)
        bus[i0:i0 + n, 0] += x[:n, 0] * g * gl
        bus[i0:i0 + n, 1] += x[:n, 1] * g * gr
    bus = bus[:N]
    fade = np.clip((DUR - np.arange(N) / SR) / .5, 0, 1)
    return bus * fade[:, None]


def load_vo(path, offset):
    """VO preprocesada (wav 48k mono) colocada en su offset."""
    sr, x = wavfile.read(path)
    assert sr == SR
    x = x.astype(np.float64)
    if x.ndim == 2:
        x = x.mean(axis=1)
    v = np.zeros(N)
    i0 = int(offset * SR)
    n = min(len(x), N - i0)
    v[i0:i0 + n] = x[:n]
    return v


def speech_gate(v):
    """1 mientras hay voz (envolvente RMS con ataque rápido y suelta de 250 ms)."""
    win = int(.02 * SR)
    rms = np.sqrt(np.convolve(v ** 2, np.ones(win) / win, mode="same"))
    on = (rms > 10 ** (-45 / 20) * max(np.max(np.abs(v)), 1e-9) / 0.5).astype(float)
    # suaviza: ataque 40 ms, suelta 250 ms (seguidor de envolvente)
    g = np.zeros_like(on)
    a, r = np.exp(-1 / (.04 * SR)), np.exp(-1 / (.25 * SR))
    acc = 0.0
    for i in range(0, len(on), 64):
        tgt = on[i]
        coef = a if tgt > acc else r
        acc = tgt + (acc - tgt) * coef ** 64
        g[i:i + 64] = acc
    return g


def main(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    mus = music()
    fx = place()
    mus *= 10 ** (-3 / 20)
    vo_path = os.environ.get("VO")
    if vo_path:
        vo = load_vo(vo_path, float(os.environ.get("VO_OFFSET", "0")))
        g = speech_gate(vo)
        # la VO manda: ducking dinámico para que la música quede ≥15 dB (objetivo 18) bajo la voz
        # en cada ventana de 400 ms con voz; SFX -4 dB mientras habla
        w = int(.4 * SR)
        smooth = lambda x: np.sqrt(np.convolve(x ** 2, np.ones(w) / w, mode="same"))
        rv, rm = smooth(vo), smooth(mus.mean(axis=1))
        from scipy.ndimage import minimum_filter1d, uniform_filter1d
        sp_on = (rv > np.max(rv) * 10 ** (-24 / 20)).astype(float)
        need = np.clip(rv * 10 ** (-20 / 20) / np.maximum(rm, 1e-9), 0.02, 1.0)
        need = np.where(sp_on > 0, need, 1.0)
        need = minimum_filter1d(need, int(.3 * SR))          # se adelanta y sostiene el ducking
        need = uniform_filter1d(need, int(.12 * SR))         # sin escalones
        duck = need
        mus *= duck[:, None]
        fx *= (1 - np.maximum(g, uniform_filter1d(sp_on, int(.12 * SR))) * (1 - 10 ** (-4 / 20)))[:, None]
        sp = rv > np.max(rv) * 10 ** (-20 / 20)
        d = 20 * np.log10(rv[sp] / np.maximum(smooth(mus.mean(axis=1))[sp], 1e-9))
        print(f"VO vs música con voz: mediana {np.median(d):.1f} dB, percentil 5 {np.percentile(d, 5):.1f} dB")
        vo_st = np.stack([vo, vo], axis=1)
        mix = mus + fx + vo_st
    else:
        mix = mus + fx
    pk = np.max(np.abs(mix))
    print(f"pico premaster {20 * np.log10(pk):.1f} dBFS")
    # todos los stems con la misma escala que la mezcla (suman exactamente el premaster)
    stems = [("music.wav", mus), ("sfx.wav", fx), ("mix_premaster.wav", mix)]
    if vo_path:
        stems.append(("vo.wav", vo_st))
    for name, x in stems:
        wavfile.write(out / name, SR, (x * .5 / max(pk, 1e-9)).astype(np.float32))
    print("stems ->", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "out/audio")
