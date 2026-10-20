"""Audio del vídeo demo: música original muy leve (pad + arpegio suave), SFX discretos en cada clic y transición,
y máster con la voz a −14 LUFS / −1 dBTP. La música baja todavía más mientras habla la voz.

Uso: python3 build/audio.py   (después de build/timeline.py)
Lee hyperframes/data.json y hyperframes/assets/audio/vo.wav. Escribe music.wav, sfx.wav y master.wav en esa carpeta.
"""
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

ROOT = Path(__file__).resolve().parents[1]
HF = ROOT / "hyperframes"
AUD = HF / "assets" / "audio"
SFXDIR = ROOT.parent / "ImperiOS Ad" / "assets_in" / "sfx"
SR = 48000
D = json.loads((HF / "data.json").read_text())
DUR = D["duration"]
N = int(DUR * SR)
rng = np.random.default_rng(7)


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lp(x, f):
    return sosfilt(butter(2, f, fs=SR, output="sos"), x)


def hp(x, f):
    return sosfilt(butter(2, f, fs=SR, btype="high", output="sos"), x)


# ---------- música ----------
BPM = 84
BEAT = 60 / BPM
BAR = 4 * BEAT
# Re mayor: D – Bm – G – A (notas del pad, octava media) y raíces
CHORDS = [([62, 66, 69, 74], 38), ([59, 62, 66, 71], 35), ([55, 59, 62, 67], 31), ([57, 61, 64, 69], 33)]


def pad():
    out = np.zeros(N)
    t = np.arange(N) / SR
    nbar = int(np.ceil(DUR / BAR)) + 1
    for b in range(nbar):
        notes, root = CHORDS[b % 4]
        s0, s1 = int(b * BAR * SR), int(min(N, (b + 1.15) * BAR * SR))
        if s0 >= N:
            break
        n = s1 - s0
        tt = t[:n]
        env = np.minimum(1, tt / 1.2) * np.minimum(1, (n / SR - tt) / 0.9)
        seg = np.zeros(n)
        for m in notes:
            f = midi(m)
            for det in (-0.06, 0.06):
                seg += np.sin(2 * np.pi * f * (1 + det / 100) * tt + rng.uniform(0, 6.28)) * 0.5
                seg += 0.25 * np.sin(2 * np.pi * 2 * f * (1 + det / 100) * tt)
        seg += 0.9 * np.sin(2 * np.pi * midi(root) * tt)
        out[s0:s1] += seg * env
    return lp(out, 1800) * 0.03


def arp():
    out = np.zeros(N)
    step = BEAT / 2
    k = 0
    while k * step < DUR:
        b = int(k * step // BAR)
        notes, _ = CHORDS[b % 4]
        m = notes[[0, 2, 1, 3, 2, 1, 3, 0][k % 8]] + 12
        s = int(k * step * SR)
        n = min(int(0.9 * SR), N - s)
        tt = np.arange(n) / SR
        tone = np.sin(2 * np.pi * midi(m) * tt) + 0.2 * np.sin(2 * np.pi * 2 * midi(m) * tt)
        out[s:s + n] += tone * np.exp(-tt * 5.5) * (0.8 if k % 2 == 0 else 0.55)
        k += 1
    return lp(hp(out, 300), 4000) * 0.018


def speech_mask(vo):
    """1 mientras habla la voz (con colas), 0 en silencios; suavizado."""
    env = np.abs(vo).reshape(-1)
    win = int(0.05 * SR)
    e = np.convolve(env, np.ones(win) / win, mode="same")
    m = (e > 0.01).astype(float)
    hold = int(0.35 * SR)
    m = np.convolve(m, np.ones(hold), mode="same") > 0
    sm = int(0.25 * SR)
    return np.convolve(m.astype(float), np.ones(sm) / sm, mode="same")


def music(vo_mono):
    x = pad() + arp()
    t = np.arange(N) / SR
    fade = np.minimum(1, t / 1.5) * np.clip((DUR - t) / 2.5, 0, 1)
    duck = 1 - 0.75 * speech_mask(vo_mono)          # ≈ −12 dB extra bajo la voz
    y = x * fade * duck
    return np.stack([y, y], 1)


# ---------- SFX ----------
def load_sfx(name):
    sr, x = wavfile.read(SFXDIR / f"{name}.wav")
    x = x.astype(np.float32)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    return x


def sfx():
    out = np.zeros((N, 2))
    for a in D["actions"]:
        if a["t"] != "sfx":
            continue
        x = load_sfx(a["name"]) * a.get("gain", 1.0)
        s = int(max(0, a["at"]) * SR)
        n = min(len(x), N - s)
        out[s:s + n] += x[:n]
    return out * 0.35


def write(name, x):
    wavfile.write(AUD / name, SR, x.astype(np.float32))


if __name__ == "__main__":
    sr, vo = wavfile.read(AUD / "vo.wav")
    vo = vo.astype(np.float64)
    vo = vo / (np.abs(vo).max() or 1)
    vo_m = vo.mean(1)[:N] if vo.ndim == 2 else vo[:N]
    if len(vo_m) < N:
        vo_m = np.pad(vo_m, (0, N - len(vo_m)))
    write("music.wav", music(vo_m))
    write("sfx.wav", sfx())
    # Máster: voz (compresión suave + presencia) + lecho (música y SFX, muy por debajo) → −14 LUFS / −1 dBTP
    fc = ("[2]highpass=f=80,acompressor=threshold=0.1:ratio=2.5:attack=8:release=150:makeup=1.6,"
          "equalizer=f=3000:t=q:w=1.2:g=2[vo];"
          "[0][1]amix=inputs=2:weights='1 1':normalize=0,volume=-6dB[bed];"
          "[bed][vo]amix=inputs=2:weights='1 1':normalize=0[pre]")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(AUD / "music.wav"), "-i", str(AUD / "sfx.wav"),
                    "-i", str(AUD / "vo.wav"), "-filter_complex", fc, "-map", "[pre]", "-c:a", "pcm_f32le", str(AUD / "premix.wav")], check=True)
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(AUD / "premix.wav"), "-af", "ebur128", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    I = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    g = -14.0 - I
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(AUD / "premix.wav"), "-af",
                    f"volume={g:.2f}dB,aresample=192000,alimiter=limit=0.85:attack=1:release=40:level=disabled,aresample=48000",
                    "-c:a", "pcm_s24le", str(AUD / "master.wav")], check=True)
    (AUD / "premix.wav").unlink()
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(AUD / "master.wav"), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    print(f"ganancia {g:+.1f} dB ·", " · ".join(l.strip() for l in out.splitlines() if l.strip().startswith(("I:", "Peak:"))))
