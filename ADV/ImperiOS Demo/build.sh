#!/usr/bin/env bash
# Vídeo demo 16:9 del CRM: estados reales de la cuenta demo + voz (Cristina) + música leve, compuesto en HyperFrames.
#   1) capturas (solo si hace falta): ../ImperiOS Ad/capture → node demo-states.mjs   (requiere IMPERIOS_DEMO_*)
#   2) imágenes de estado  →  3) timeline + pista de voz  →  4) música, SFX y máster  →  5) check + render
set -euo pipefail
cd "$(dirname "$0")"
export DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1
[ -x /opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell ] && \
  export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
[ -d "../ImperiOS Ad/capture/out/states" ] || { echo "Faltan las capturas: cd '../ImperiOS Ad/capture' && node demo-states.mjs"; exit 1; }
python3 build/plates.py > /dev/null
python3 build/timeline.py
python3 build/audio.py
cd hyperframes
[ -d node_modules ] || npm install
npx hyperframes check
OUT=renders/imperios-demo-crm-v1_16x9.mp4
npx hyperframes render --quality "${QUALITY:-looks}" --fps 60 --output "$OUT"
ffmpeg -hide_banner -loglevel error -y -i "$OUT" -vf "fps=1/5,scale=320:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=16:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=6x5" -frames:v 1 renders/contact-sheet-demo-v1.png
ffmpeg -hide_banner -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
