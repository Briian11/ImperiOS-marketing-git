#!/usr/bin/env bash
# Versión «producto real» en HyperFrames: placas desde las capturas, audio, comprobación y render a 60 fps.
set -euo pipefail
cd "$(dirname "$0")"
export DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1
# Chromium headless del contenedor de Claude Code; en otro equipo: npx hyperframes browser ensure
[ -x /opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell ] && \
  export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
[ -d node_modules ] || npm install
[ -f assets/plates/calendar.png ] || python3 tools/make_plates.py      # requiere ../capture/out (capturas revisadas)
mkdir -p assets/audio renders
cp ../preview/out/campaign-vo/audio/master.wav assets/audio/master.wav  # VO Cristina toma 1 + música + SFX (−14 LUFS)
npx hyperframes check
OUT=renders/imperios-producto-real-v1_9x16.mp4
npx hyperframes render --quality looks --fps 60 --output "$OUT"
ffmpeg -hide_banner -loglevel error -y -i "$OUT" -vf "fps=1,scale=230:-1,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=0x0A0A0A:box=1:boxcolor=0xFFD500@0.9:boxborderw=3,pad=iw+8:ih+8:4:4:color=0x0A0A0A,tile=10x3" -frames:v 1 renders/contact-sheet-producto-real-v1.png
ffmpeg -hide_banner -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
