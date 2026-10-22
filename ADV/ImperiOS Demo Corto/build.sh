#!/usr/bin/env bash
# Vídeo demo corto 16:9 (~49 s) del CRM: mismas capturas, música y motor que el demo largo (../ImperiOS Demo),
# voz nueva más compacta (Cristina) y una escena final de tarjetas con los módulos que no se enseñan en detalle.
#   1) imágenes de estado  →  2) timeline + pista de voz  →  3) música, SFX y máster  →  4) check + render
set -euo pipefail
cd "$(dirname "$0")"
export DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1
[ -x /opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell ] && \
  export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
[ -d "../ImperiOS Ad/capture/out/states" ] || { echo "Faltan las capturas: cd '../ImperiOS Ad/capture' && node demo-states.mjs"; exit 1; }
PIPE="../ImperiOS Demo/build"
python3 "$PIPE/plates.py" . > /dev/null
python3 build/timeline.py
python3 "$PIPE/audio.py" .
# duración de la composición = la del timeline
DUR=$(python3 -c "import json; print(json.load(open('hyperframes/data.json'))['duration'])")
sed -i -E "s/data-duration=\"[0-9.]+\"/data-duration=\"$DUR\"/g" hyperframes/index.html
cd hyperframes
[ -d node_modules ] || npm install
npx hyperframes check
OUT=renders/imperios-demo-corto-v1_16x9.mp4
npx hyperframes render --quality "${QUALITY:-looks}" --fps 60 --output "$OUT"
# el render de HyperFrames vuelve a mezclar el audio: se sustituye por el máster (−14 LUFS) sin recodificar la imagen
ffmpeg -hide_banner -loglevel error -y -i "$OUT" -i assets/audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart renders/tmp.mp4 && mv renders/tmp.mp4 "$OUT"
ffmpeg -hide_banner -loglevel error -y -i "$OUT" -vf "fps=1/2,scale=320:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=16:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=5x5" -frames:v 1 renders/contact-sheet-demo-corto-v1.png
ffmpeg -hide_banner -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
