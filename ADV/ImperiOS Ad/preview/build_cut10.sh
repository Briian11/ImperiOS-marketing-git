#!/usr/bin/env bash
# Corte corto (~11 s) desde la versión con voz: gancho + «Y cuando hay match… oportunidad real.» + «Pide tu demo» y llamada a la acción.
# Los cortes caen en silencios de la VO (tiempos de timeline-campaign-vo.json + offset 0,2 s).
set -euo pipefail
cd "$(dirname "$0")"
F=out/campaign-vo/imperios-campana-v3-voz-A_9x16.mp4
O=out/campaign-vo/imperios-campana-v3-voz-corte-11s_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $F -filter_complex "\
[0:v]trim=0:3.90,setpts=PTS-STARTPTS[v1];[0:a]atrim=0:3.90,asetpts=PTS-STARTPTS[a1];\
[0:v]trim=12.98:17.06,setpts=PTS-STARTPTS[v2];[0:a]atrim=12.98:17.06,asetpts=PTS-STARTPTS[a2];\
[0:v]trim=24.90:28.2,setpts=PTS-STARTPTS[v3];[0:a]atrim=24.90:28.2,asetpts=PTS-STARTPTS[a3];\
[v1][v2]xfade=transition=fade:duration=0.12:offset=3.78[v12];[v12][v3]xfade=transition=fade:duration=0.12:offset=7.74[v];\
[a1][a2]acrossfade=d=0.08[a12];[a12][a3]acrossfade=d=0.06[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 15 -pix_fmt yuv420p -r 60 -c:a aac -b:a 320k -movflags +faststart $O
ffprobe -v error -show_entries format=duration -of csv=p=0 $O
ffmpeg -hide_banner -i $O -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
