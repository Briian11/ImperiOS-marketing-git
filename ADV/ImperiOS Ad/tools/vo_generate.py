"""Genera las 2 tomas de VO del spec ad de ImperiOS con ElevenLabs.

Uso: python3 tools/vo_generate.py [--dry-run]
Necesita la variable de entorno ELEVENLABS_API_KEY y acceso a api.elevenlabs.io.
Guarda en assets_in/vo/: toma-1.mp3, toma-2.mp3 y sus tiempos por carácter (*.alignment.json)
para re-temporizar la imagen a la voz.
"""
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = (ROOT / "brief" / "VO_SCRIPT.txt").read_text().strip()
OUT = ROOT / "assets_in" / "vo"
API = "https://api.elevenlabs.io/v1"
VOICE_NAME = "Cristina"  # Cristina - Premium Spanish Female (PVC), de la biblioteca del usuario
MODEL = "eleven_multilingual_v2"
SETTINGS = {"stability": 0.50, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": True, "speed": 1.0}
SEEDS = [11, 23]  # una semilla por toma: 2 tomas distintas y reproducibles


def call(path, key, body=None):
    req = urllib.request.Request(
        API + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"xi-api-key": key, "Content-Type": "application/json"},
        method="POST" if body is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def main():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("Falta ELEVENLABS_API_KEY en el entorno.")
    voices = call("/voices", key)["voices"]
    match = [v for v in voices if VOICE_NAME.lower() in v["name"].lower()]
    if not match:
        sys.exit(f"No encuentro la voz «{VOICE_NAME}» en tu cuenta. Voces: {[v['name'] for v in voices]}")
    voice = match[0]
    chars = len(SCRIPT)
    print(f"Voz: {voice['name']} ({voice['voice_id']}) · {chars} caracteres × {len(SEEDS)} tomas ≈ {chars * len(SEEDS)} créditos")
    if "--dry-run" in sys.argv:
        return
    OUT.mkdir(parents=True, exist_ok=True)
    for i, seed in enumerate(SEEDS, 1):
        res = call(
            f"/text-to-speech/{voice['voice_id']}/with-timestamps?output_format=mp3_44100_128",
            key,
            {"text": SCRIPT, "model_id": MODEL, "voice_settings": SETTINGS, "seed": seed, "language_code": "es"},
        )
        (OUT / f"toma-{i}.mp3").write_bytes(base64.b64decode(res["audio_base64"]))
        (OUT / f"toma-{i}.alignment.json").write_text(json.dumps(res.get("alignment"), ensure_ascii=False))
        print(f"toma-{i}.mp3 guardada")


if __name__ == "__main__":
    main()
